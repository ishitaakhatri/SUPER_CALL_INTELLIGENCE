# data/knowledge.py — Knowledge & Compliance search (JSON-backed, no VectorDB)

import json
import os

_DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── Load JSON files once at import time ─── #
with open(os.path.join(_DATA_DIR, "knowledge_base.json"), "r", encoding="utf-8") as f:
    KNOWLEDGE_BASE: list[dict] = json.load(f)

with open(os.path.join(_DATA_DIR, "compliance_rules.json"), "r", encoding="utf-8") as f:
    COMPLIANCE_RULES: list[dict] = json.load(f)


def search_knowledge(query: str, top_k: int = 3) -> list[dict]:
    """
    Simple keyword-match search over the knowledge base.
    Scores each doc by how many of its tags appear in the query.
    Returns the top-k results sorted by relevance.
    """
    query_lower = query.lower()
    scored: list[tuple[int, dict]] = []

    for doc in KNOWLEDGE_BASE:
        score = sum(1 for tag in doc["tags"] if tag in query_lower)
        if score > 0:
            scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def get_compliance_alerts(intent: str, transcript: str) -> list[dict]:
    """
    Match compliance rules based on the detected intent and transcript keywords.
    Rules with trigger '_always' are included for every call.
    """
    transcript_lower = transcript.lower()
    matched: list[dict] = []

    for rule in COMPLIANCE_RULES:
        # Always-on rules
        if "_always" in rule["triggers"]:
            matched.append(rule)
            continue
        # Check if any trigger keyword appears in the transcript or intent
        for trigger in rule["triggers"]:
            if trigger in transcript_lower or trigger in intent.lower():
                matched.append(rule)
                break

    return matched
