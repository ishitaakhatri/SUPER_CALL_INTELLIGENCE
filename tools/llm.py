# tools/llm.py — OpenAI LLM utilities for Insurance FNOL + Post-Call Evaluation

import os
from typing import Literal
from openai import AsyncOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4.1-mini"


# ═══════════════════════════════════════════════════════
# PYDANTIC SCHEMAS — used by OpenAI Structured Outputs
# ═══════════════════════════════════════════════════════

class IntentClassification(BaseModel):
    intent: Literal[
        "car_accident",
        "car_theft",
        "car_vandalism",
        "life_death_claim",
        "life_accidental_death",
        "general_inquiry",
    ]
    claim_type: Literal["car_insurance", "life_insurance", "general"]


class EntityExtraction(BaseModel):
    policy_id: str | None
    name: str | None
    phone: str | None


class ScoreDetail(BaseModel):
    score: int
    feedback: str


class EvaluationScores(BaseModel):
    empathy_and_tone: ScoreDetail
    information_gathering: ScoreDetail
    compliance_adherence: ScoreDetail
    process_knowledge: ScoreDetail
    resolution_and_next_steps: ScoreDetail


class PostCallEvaluation(BaseModel):
    overall_score: int
    call_summary: str
    claim_type_detected: str
    scores: EvaluationScores
    strengths: list[str]
    improvements: list[str]
    compliance_violations: list[str]
    coaching_notes: str


# ═══════════════════════════════════════════════════════
# INTENT CLASSIFICATION — Structured Output
# ═══════════════════════════════════════════════════════

async def classify_intent(transcript: str) -> dict:
    """Use LLM to classify the caller's intent into an FNOL category."""

    system_prompt = """You are an insurance call classification system.
Analyze the caller's statement and classify it.
- "intent": the most fitting FNOL category.
- "claim_type": the broad insurance line the intent falls under."""

    response = await client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcript},
        ],
        temperature=0.0,
        max_tokens=100,
        response_format=IntentClassification,
    )

    return response.choices[0].message.parsed.model_dump()


# ═══════════════════════════════════════════════════════
# ENTITY EXTRACTION — Structured Output
# ═══════════════════════════════════════════════════════

async def extract_entities(transcript: str) -> dict:
    """Use LLM to extract names, phone numbers, and policy IDs from transcript."""
    
    system_prompt = """You are an insurance entity extraction system.
Analyze the caller's statement and extract the following if present:
- "policy_id": formatted as CAR-XXXXXX or LIFE-XXXXXX (fix spacing/hyphens if spoken like "car 12345").
- "name": full or partial name of the caller.
- "phone": phone number referenced.
Return null for fields not found."""

    response = await client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcript},
        ],
        temperature=0.0,
        max_tokens=150,
        response_format=EntityExtraction,
    )

    return response.choices[0].message.parsed.model_dump()


# ═══════════════════════════════════════════════════════
# AGENT SUGGESTION — free-text (no structured output)
# ═══════════════════════════════════════════════════════

async def generate_agent_suggestion(
    transcript: str,
    full_transcript: str,
    intent: str | None,
    member_data: dict | None,
    knowledge_docs: list[dict] | None,
    compliance_alerts: list[dict] | None,
) -> str:
    """Generate a contextual suggested response for the call center agent."""

    system_prompt = """You are an AI assistant for insurance call center agents handling First Notice of Loss (FNOL) claims.
Generate a professional, empathetic, and compliance-aware suggested response for the agent to say to the caller.

Rules:
- NEVER address the customer directly. You are writing a script/talking points FOR the agent to read.
- Be warm and empathetic, especially for life insurance death claims.
- Include specific next steps based on the knowledge articles provided.
- Reference compliance requirements naturally (don't read compliance codes).
- If member data is available, use their name in the script.
- If the customer provided a policy number but Policyholder Data is "Not yet identified", instruct the agent to inform the customer that the policy couldn't be found and ask them to verify or repeat the number.
- CRITICAL: Keep responses extremely short and conversational like a real human. 1-2 sentences MAX.
- CRITICAL: NEVER ask more than ONE question at a time. Do not overwhelm the caller. Wait for their response to one question before asking the next.
- Start immediately with the script (e.g., "Hi [Name], I'm so sorry...")."""

    user_prompt = f"""Recent Caller's Statement:
{transcript}

Full Conversation Context:
{full_transcript or 'None yet'}

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


async def generate_agent_suggestion_stream(
    transcript: str,
    full_transcript: str,
    intent: str | None,
    member_data: dict | None,
    knowledge_docs: list[dict] | None,
    compliance_alerts: list[dict] | None,
):
    """Generate a contextual suggested response for the call center agent, streaming chunks."""

    system_prompt = """You are an AI assistant for insurance call center agents handling First Notice of Loss (FNOL) claims.
Generate a professional, empathetic, and compliance-aware suggested response for the agent to say to the caller.

Rules:
- NEVER address the customer directly. You are writing a script/talking points FOR the agent to read.
- Be warm and empathetic, especially for life insurance death claims.
- Include specific next steps based on the knowledge articles provided.
- Reference compliance requirements naturally (don't read compliance codes).
- If member data is available, use their name in the script.
- If the customer provided a policy number but Policyholder Data is "Not yet identified", instruct the agent to inform the customer that the policy couldn't be found and ask them to verify or repeat the number.
- CRITICAL: Keep responses short and conversational like a real human. 1-2 sentences MAX.
- CRITICAL: NEVER ask more than ONE question at a time. Do not overwhelm the caller. Wait for their response to one question before asking the next.
- Start immediately with the script (e.g., "Hi [Name], I'm so sorry...")."""

    user_prompt = f"""Recent Caller's Statement:
{transcript}

Full Conversation Context:
{full_transcript or 'None yet'}

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
        stream=True,
    )

    async for chunk in response:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            yield delta
# ═══════════════════════════════════════════════════════
# POST-CALL EVALUATION — Structured Output
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

Scoring criteria:
- Empathy: Did the agent show appropriate concern? Warm opening?
- Information Gathering: Did they collect all required FNOL details (date, location, parties, damage, police report)?
- Compliance: Privacy disclosures, call recording notice, no fault admission advice?
- Process Knowledge: Did agent know the correct procedures and requirements?
- Resolution: Clear next steps, timeline, follow-up expectations?

Scores use a 1-10 scale per category and 1-100 overall."""

    user_prompt = f"""Call Transcript:
{formatted_transcript}

Call Duration: {int(call_duration)} seconds
Detected Claim Type: {detected_intent or 'unknown'}
Policyholder Identified: {member_data.get('name') if member_data else 'Not identified'}

Evaluate this agent's performance:"""

    response = await client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=800,
        response_format=PostCallEvaluation,
    )

    evaluation = response.choices[0].message.parsed.model_dump()

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
