# data/knowledge.py

KNOWLEDGE_BASE = [
    {
        "docId": "POL-001",
        "title": "Hardship Withdrawal – Medical",
        "tags": ["medical", "hardship"],
        "content": """
Members may withdraw early on medical hardship.
Tax applies at marginal rate.
Processing time: 7-10 business days.
Required: Medical bills and doctor letter.
"""
    },
    {
        "docId": "POL-002",
        "title": "Tax Implications",
        "tags": ["tax", "withdrawal"],
        "content": """
Early withdrawals may be taxed.
Agents must disclose:
- Tax impact
- Retirement savings impact
- Alternative options
"""
    }
]


def search_knowledge(query: str):
    results = []
    for doc in KNOWLEDGE_BASE:
        if any(tag in query.lower() for tag in doc["tags"]):
            results.append(doc)
    return results
