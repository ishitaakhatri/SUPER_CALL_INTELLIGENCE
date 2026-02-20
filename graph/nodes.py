# graph/nodes.py

import re
from data.members import get_member
from data.knowledge import search_knowledge
from tools.llm import generate_agent_suggestion


# ---------------- INTENT NODE ---------------- #

async def intent_node(state):
    """
    Detect high-level customer intent.
    Only returns the key it updates.
    """
    text = state["transcript"].lower()

    if "withdraw" in text:
        intent = "hardship_withdrawal"
    elif "complaint" in text:
        intent = "complaint"
    else:
        intent = "general_query"

    return {
        "intent": intent
    }


# ---------------- ENTITY NODE ---------------- #

async def entity_node(state):
    """
    Extract entities like Member ID.
    Only returns the key it updates.
    """
    text = state["transcript"]

    match = re.search(r"SUP-\d+", text)
    entities = {"memberId": match.group()} if match else {}

    return {
        "entities": entities
    }


# ---------------- MEMBER NODE ---------------- #

async def member_node(state):
    """
    Fetch member details from mock DB.
    Only returns the key it updates.
    """
    entities = state.get("entities", {})
    member = None

    if "memberId" in entities:
        member = get_member(entities["memberId"])

    return {
        "member_data": member
    }


# ---------------- KNOWLEDGE NODE ---------------- #

async def knowledge_node(state):
    """
    Retrieve relevant knowledge documents.
    Only returns the key it updates.
    """
    docs = search_knowledge(state["transcript"])

    return {
        "knowledge_docs": docs
    }


# ---------------- SUGGESTION NODE ---------------- #

async def suggestion_node(state):
    """
    Generate final suggested response using LLM.
    Only returns the key it updates.
    """

    suggestion = await generate_agent_suggestion(
        transcript=state["transcript"],
        member_data=state.get("member_data"),
        knowledge_docs=state.get("knowledge_docs"),
    )

    return {
        "suggestion": suggestion
    }
