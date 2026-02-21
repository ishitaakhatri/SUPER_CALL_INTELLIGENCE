# graph/nodes.py — LangGraph node functions for Insurance FNOL

import re
from data.members import get_member
from data.knowledge import search_knowledge, get_compliance_alerts
from tools.llm import classify_intent, generate_agent_suggestion


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
    Extract policy IDs from the transcript using regex.
    Supports CAR-XXXXXX and LIFE-XXXXXX formats.
    """
    text = state["transcript"]
    entities: dict = {}

    # Look for car policy IDs
    car_match = re.search(r"CAR-\d{4,}", text, re.IGNORECASE)
    if car_match:
        entities["policyId"] = car_match.group().upper()

    # Look for life policy IDs
    life_match = re.search(r"LIFE-\d{4,}", text, re.IGNORECASE)
    if life_match:
        entities["policyId"] = life_match.group().upper()

    return {"entities": entities}


# ─────────────── MEMBER NODE ─────────────── #

async def member_node(state: dict) -> dict:
    """
    Fetch policyholder details from mock CRM using the extracted policy ID.
    """
    entities = state.get("entities") or {}
    member = None

    policy_id = entities.get("policyId")
    if policy_id:
        member = get_member(policy_id)

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
    Match compliance rules based on the detected intent and transcript.
    """
    intent = state.get("intent") or ""
    alerts = get_compliance_alerts(intent, state["transcript"])
    return {"compliance_alerts": alerts}


# ─────────────── SUGGESTION NODE ─────────────── #

async def suggestion_node(state: dict) -> dict:
    """
    Generate a suggested response for the agent using the LLM.
    Combines all gathered context into a coherent recommendation.
    """
    suggestion = await generate_agent_suggestion(
        transcript=state["transcript"],
        intent=state.get("intent"),
        member_data=state.get("member_data"),
        knowledge_docs=state.get("knowledge_docs"),
        compliance_alerts=state.get("compliance_alerts"),
    )
    return {"suggestion": suggestion}
