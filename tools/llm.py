# tools/llm.py — OpenAI LLM utilities for Insurance FNOL + Post-Call Evaluation

import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4.1-mini"


async def classify_intent(transcript: str) -> dict:
    """Use LLM to classify the caller's intent into an FNOL category."""

    system_prompt = """You are an insurance call classification system.
Analyze the caller's statement and return ONLY a JSON object with two keys:
- "intent": one of ["car_accident", "car_theft", "car_vandalism", "life_death_claim", "life_accidental_death", "general_inquiry"]
- "claim_type": one of ["car_insurance", "life_insurance", "general"]

Return ONLY the JSON object, no markdown, no explanation."""

    response = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcript},
        ],
        temperature=0.0,
        max_tokens=100,
    )

    text = response.choices[0].message.content.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"intent": "general_inquiry", "claim_type": "general"}


async def generate_agent_suggestion(
    transcript: str,
    intent: str | None,
    member_data: dict | None,
    knowledge_docs: list[dict] | None,
    compliance_alerts: list[dict] | None,
) -> str:
    """Generate a contextual suggested response for the call center agent."""

    system_prompt = """You are an AI assistant for insurance call center agents handling First Notice of Loss (FNOL) claims.
Generate a professional, empathetic, and compliance-aware suggested response for the agent to say to the caller.

Rules:
- Be warm and empathetic, especially for life insurance death claims.
- Include specific next steps based on the knowledge articles provided.
- Reference compliance requirements naturally (don't read compliance codes).
- If member data is available, use their name.
- Keep the response concise (3-5 sentences max).
- Format as a direct script the agent can read aloud."""

    user_prompt = f"""Caller's Statement:
{transcript}

Detected Intent: {intent or 'unknown'}

Policyholder Data:
{member_data or 'Not yet identified'}

Relevant Policy Articles:
{_format_docs(knowledge_docs)}

Active Compliance Alerts:
{_format_alerts(compliance_alerts)}

Generate the agent's suggested response:"""

    response = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
        max_tokens=300,
    )

    return response.choices[0].message.content


# ═══════════════════════════════════════════════════════
# POST-CALL EVALUATION — Agent performance scorecard
# ═══════════════════════════════════════════════════════

async def generate_post_call_evaluation(
    transcript_lines: list[dict],
    call_duration: float,
    detected_intent: str | None,
    member_data: dict | None,
) -> dict:
    """
    Generate a comprehensive post-call evaluation scorecard.
    Returns structured JSON with scores and feedback.
    """

    # Format transcript for LLM
    formatted_transcript = "\n".join(
        f"[{line['speaker']} {line['timestamp']}]: \"{line['text']}\""
        for line in transcript_lines
    )

    system_prompt = """You are an insurance call center quality assurance analyst.
Evaluate the agent's performance on an FNOL (First Notice of Loss) call.

Return a JSON object with this EXACT structure:
{
  "overall_score": <number 1-100>,
  "call_summary": "<2-3 sentence summary of what happened on the call>",
  "claim_type_detected": "<the type of claim>",
  "scores": {
    "empathy_and_tone": {
      "score": <1-10>,
      "feedback": "<specific feedback>"
    },
    "information_gathering": {
      "score": <1-10>,
      "feedback": "<specific feedback>"
    },
    "compliance_adherence": {
      "score": <1-10>,
      "feedback": "<specific feedback>"
    },
    "process_knowledge": {
      "score": <1-10>,
      "feedback": "<specific feedback>"
    },
    "resolution_and_next_steps": {
      "score": <1-10>,
      "feedback": "<specific feedback>"
    }
  },
  "strengths": ["<strength 1>", "<strength 2>"],
  "improvements": ["<improvement 1>", "<improvement 2>"],
  "compliance_violations": ["<violation or 'None detected'>"],
  "coaching_notes": "<1-2 sentences of coaching advice>"
}

Scoring criteria:
- Empathy: Did the agent show appropriate concern? Warm opening?
- Information Gathering: Did they collect all required FNOL details (date, location, parties, damage, police report)?
- Compliance: Privacy disclosures, call recording notice, no fault admission advice?
- Process Knowledge: Did agent know the correct procedures and requirements?
- Resolution: Clear next steps, timeline, follow-up expectations?

Return ONLY the JSON, no markdown fences."""

    user_prompt = f"""Call Transcript:
{formatted_transcript}

Call Duration: {int(call_duration)} seconds
Detected Claim Type: {detected_intent or 'unknown'}
Policyholder Identified: {member_data.get('name') if member_data else 'Not identified'}

Evaluate this agent's performance:"""

    response = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=800,
    )

    text = response.choices[0].message.content.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    try:
        evaluation = json.loads(text)
    except json.JSONDecodeError:
        evaluation = {
            "overall_score": 0,
            "call_summary": "Failed to generate evaluation",
            "scores": {},
            "strengths": [],
            "improvements": [],
            "compliance_violations": [],
            "coaching_notes": "Error in evaluation generation",
        }

    # Add metadata
    evaluation["call_duration_seconds"] = int(call_duration)
    evaluation["total_utterances"] = len(transcript_lines)
    evaluation["agent_utterances"] = sum(1 for l in transcript_lines if l["speaker"] == "Agent")
    evaluation["customer_utterances"] = sum(1 for l in transcript_lines if l["speaker"] == "Customer")

    return evaluation


def _format_docs(docs: list[dict] | None) -> str:
    if not docs:
        return "None found"
    return "\n".join(f"- {d['title']}: {d['content'][:200]}..." for d in docs)


def _format_alerts(alerts: list[dict] | None) -> str:
    if not alerts:
        return "None"
    return "\n".join(f"- [{a['severity'].upper()}] {a['message']}" for a in alerts)
