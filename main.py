# main.py — FastAPI backend with WebSocket dual-path processing + post-call evaluation

import re
import json
import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from data.members import get_member
from graph.graph import build_graph
from tools.llm import generate_post_call_evaluation

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("call-intelligence")

# ─── Build the LangGraph at startup ─── #
graph = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global graph
    logger.info("🚀 Building LangGraph pipeline...")
    graph = build_graph()
    logger.info("✅ LangGraph ready. Server is live.")
    yield
    logger.info("🛑 Server shutting down.")


app = FastAPI(
    title="Super/PF Call Intelligence",
    description="Real-time FNOL call intelligence demo with post-call evaluation",
    version="1.0.0",
    lifespan=lifespan,
)

# ─── CORS for dev mode (Vite runs on :5173) ─── #
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Regex patterns for the FAST PATH ─── #
POLICY_REGEX = re.compile(r"\b(CAR-\d{4,}|LIFE-\d{4,})\b", re.IGNORECASE)


# ─── Health check ─── #
@app.get("/health")
async def health():
    return {"status": "ok", "graph_ready": graph is not None}


# ─── Azure Speech Token Endpoint ─── #
# The frontend fetches a short-lived token from here instead of holding the key
import os
import httpx

@app.get("/api/speech-token")
async def get_speech_token():
    """
    Issue a short-lived Azure Speech authorization token.
    The token is valid for 10 minutes. The frontend uses this token
    with SpeechConfig.fromAuthorizationToken() so the API key never
    leaves the server.
    """
    speech_key = os.getenv("AZURE_SPEECH_KEY", "")
    speech_region = os.getenv("AZURE_SPEECH_REGION", "eastus")

    if not speech_key:
        return {"error": "AZURE_SPEECH_KEY not configured on the server"}, 500

    token_url = f"https://{speech_region}.api.cognitive.microsoft.com/sts/v1.0/issueToken"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            token_url,
            headers={
                "Ocp-Apim-Subscription-Key": speech_key,
                "Content-Length": "0",
            },
        )

    if response.status_code == 200:
        return {
            "token": response.text,
            "region": speech_region,
        }
    else:
        logger.error(f"Failed to fetch speech token: {response.status_code} {response.text}")
        return {"error": "Failed to fetch speech token"}, 500



# ─── WebSocket endpoint for real-time streaming ─── #
@app.websocket("/stream")
async def stream_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("📞 WebSocket connected")

    # Track full call transcript for post-call analysis
    call_transcript: list[dict] = []
    call_start_time = time.time()
    detected_intent = None
    detected_member = None

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)

            msg_type = data.get("type", "transcript")

            # ═══════════════════════════════════════════
            # 📋 END CALL — Generate post-call evaluation
            # ═══════════════════════════════════════════
            if msg_type == "end_call":
                logger.info("📋 Call ended — generating post-call evaluation...")
                await websocket.send_json({
                    "type": "processing",
                    "data": {"message": "Generating post-call evaluation..."},
                })

                call_duration = time.time() - call_start_time
                evaluation = await generate_post_call_evaluation(
                    transcript_lines=call_transcript,
                    call_duration=call_duration,
                    detected_intent=detected_intent,
                    member_data=detected_member,
                )

                await websocket.send_json({
                    "type": "post_call_evaluation",
                    "data": evaluation,
                })
                logger.info("📋 Post-call evaluation sent")
                continue

            # ═══════════════════════════════════════════
            # 🎙️ TRANSCRIPT MESSAGE — Process normally
            # ═══════════════════════════════════════════
            text: str = data.get("text", "")
            is_finalized: bool = data.get("is_finalized", False)
            speaker: str = data.get("speaker", "Unknown")
            offset: int = data.get("offset", 0)

            if not text.strip():
                continue

            # Map Azure diarization speaker IDs to roles
            speaker_label = _map_speaker(speaker)

            logger.info(
                f"{'📝 FINAL' if is_finalized else '💬 Partial'} "
                f"[{speaker_label}]: {text[:80]}"
            )

            # Store in call transcript (only finalized)
            if is_finalized:
                timestamp = _format_timestamp(offset)
                call_transcript.append({
                    "speaker": speaker_label,
                    "text": text,
                    "timestamp": timestamp,
                    "offset": offset,
                })

            # ═══════════════════════════════════════════
            # ⚡ FAST PATH — Regex policy ID extraction
            # ═══════════════════════════════════════════
            policy_match = POLICY_REGEX.search(text)
            if policy_match:
                policy_id = policy_match.group().upper()
                member = get_member(policy_id)
                if member:
                    detected_member = member
                    await websocket.send_json({
                        "type": "member_profile",
                        "data": member,
                    })
                    logger.info(f"⚡ Fast path: sent profile for {policy_id}")

            # ═══════════════════════════════════════════
            # 🧠 SLOW PATH — LangGraph (only on finalized)
            # ═══════════════════════════════════════════
            if is_finalized and graph:
                await websocket.send_json({
                    "type": "processing",
                    "data": {"message": "Analyzing transcript..."},
                })

                state = {
                    "transcript": text,
                    "is_finalized": True,
                    "intent": None,
                    "claim_type": None,
                    "entities": None,
                    "member_data": None,
                    "knowledge_docs": None,
                    "compliance_alerts": None,
                    "suggestion": None,
                }

                result = await graph.ainvoke(state)

                # Track detected intent
                if result.get("intent"):
                    detected_intent = result["intent"]
                    await websocket.send_json({
                        "type": "intent",
                        "data": {
                            "intent": result["intent"],
                            "claim_type": result.get("claim_type", ""),
                        },
                    })

                # Send member data (slow path backup)
                if result.get("member_data"):
                    detected_member = result["member_data"]
                    await websocket.send_json({
                        "type": "member_profile",
                        "data": result["member_data"],
                    })

                # Send knowledge articles
                if result.get("knowledge_docs"):
                    await websocket.send_json({
                        "type": "knowledge",
                        "data": result["knowledge_docs"],
                    })

                # Send compliance alerts
                if result.get("compliance_alerts"):
                    await websocket.send_json({
                        "type": "compliance",
                        "data": result["compliance_alerts"],
                    })

                # Send suggested response
                if result.get("suggestion"):
                    await websocket.send_json({
                        "type": "suggestion",
                        "data": {"text": result["suggestion"]},
                    })

                logger.info("🧠 Slow path: all cards sent")

            # Always echo the transcript back for display
            await websocket.send_json({
                "type": "transcript",
                "data": {
                    "text": text,
                    "is_finalized": is_finalized,
                    "speaker": speaker_label,
                    "timestamp": _format_timestamp(offset),
                },
            })

    except WebSocketDisconnect:
        logger.info("📞 WebSocket disconnected")
    except Exception as e:
        logger.error(f"❌ WebSocket error: {e}", exc_info=True)
        try:
            await websocket.send_json({
                "type": "error",
                "data": {"message": str(e)},
            })
        except Exception:
            pass


def _map_speaker(speaker_id: str) -> str:
    """Map Azure diarization speaker IDs to human-readable labels."""
    mapping = {
        "Guest-1": "Agent",
        "Guest-2": "Customer",
        "Unknown": "Speaker",
    }
    return mapping.get(speaker_id, f"Speaker {speaker_id}")


def _format_timestamp(offset_ticks: int) -> str:
    """Convert Azure Speech offset (in 100-nanosecond ticks) to HH:MM:SS format."""
    if not offset_ticks:
        return "00:00:00"
    total_seconds = offset_ticks / 10_000_000
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


# ─── Serve frontend static files (production) ─── #
import os

frontend_dist = os.path.join(os.path.dirname(__file__), "frontend", "dist")
if os.path.isdir(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/")
    async def serve_frontend():
        return FileResponse(os.path.join(frontend_dist, "index.html"))
