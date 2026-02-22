# graph/nodes.py — LangGraph node functions for Insurance FNOL

import re
from data.members import get_member
from data.knowledge import search_knowledge, get_compliance_alerts
from tools.llm import classify_intent, generate_agent_suggestion, extract_entities


# ─────────────── INTENT NODE ─────────────── #

async def intent_node(state: dict) -> dict:
    """
    Classify the caller's intent using the LLM.
    Returns intent and claim_type.
    """
    result = await classify_intent(state["transcript"])
    return {
        "intent": result.get("intent", "general_inquiry"),
        "claim_type": result.get("claim_type", "general"),
    }


# ─────────────── ENTITY NODE ─────────────── #

async def entity_node(state: dict) -> dict:
    """
    Extract policy IDs, names, and phones from the transcript using LLM.
    """
    text = state["transcript"]
    entities = await extract_entities(text)

    # Clean up empty entities to keep state clean
    cleaned_entities = {k: v for k, v in entities.items() if v is not None}

    return {"entities": cleaned_entities}


# ─────────────── MEMBER NODE ─────────────── #

async def member_node(state: dict) -> dict:
    """
    Fetch policyholder details from mock CRM using extracted entities.
    """
    entities = state.get("entities") or {}
    member = None

    if entities:
        member = get_member(
            policy_id=entities.get("policy_id"),
            name=entities.get("name"),
            phone=entities.get("phone")
        )

    return {"member_data": member}


# ─────────────── KNOWLEDGE NODE ─────────────── #

async def knowledge_node(state: dict) -> dict:
    """
    Retrieve relevant knowledge articles based on the transcript.
    """
    docs = search_knowledge(state["transcript"])
    return {"knowledge_docs": docs}


# ─────────────── COMPLIANCE NODE ─────────────── #

async def compliance_node(state: dict) -> dict:
    """
    Match compliance rules based on the detected claim type and transcript.
    """
    claim_type = state.get("claim_type") or state.get("intent") or ""
    alerts = get_compliance_alerts(claim_type, state["transcript"])
    return {"compliance_alerts": alerts}


# ─────────────── SUGGESTION NODE ─────────────── #

async def suggestion_node(state: dict) -> dict:
    """
    Generate a suggested response for the agent using the LLM.
    Combines all gathered context into a coherent recommendation.
    """
    suggestion = await generate_agent_suggestion(
        transcript=state["transcript"],
        full_transcript=state.get("full_transcript", ""),
        intent=state.get("intent"),
        member_data=state.get("member_data"),
        knowledge_docs=state.get("knowledge_docs"),
        compliance_alerts=state.get("compliance_alerts"),
    )
    return {"suggestion": suggestion}
