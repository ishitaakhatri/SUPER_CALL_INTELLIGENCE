# data/knowledge.py

KNOWLEDGE_BASE = [

    {
        "docId": "POL-001",
        "title": "Hardship Withdrawal – Medical Grounds",
        "category": "Withdrawal",
        "tags": ["medical", "hardship", "withdraw"],
        "content": """
Members may apply for early release of superannuation on medical hardship grounds.

Eligibility:
- Demonstrated inability to pay medical bills
- Certified medical documentation required

Required Documents:
- Doctor certificate
- Medical invoices

Tax Implications:
- Subject to marginal tax rate
- May impact retirement savings

Processing Timeline:
- 7-10 business days

Compliance Requirements:
- Agent must disclose tax implications
- Agent must explain retirement balance impact
- Offer alternative options if available
"""
    },

    {
        "docId": "POL-002",
        "title": "Financial Hardship Withdrawal Policy",
        "category": "Withdrawal",
        "tags": ["financial", "hardship"],
        "content": """
Members may withdraw funds under financial hardship conditions.

Eligibility:
- Receiving government income support
- Unable to meet reasonable living expenses

Limits:
- Maximum withdrawal limits apply

Processing Timeline:
- 5-8 business days
"""
    },

    {
        "docId": "POL-003",
        "title": "Retirement Withdrawal Policy",
        "category": "Retirement",
        "tags": ["retirement", "age", "pension"],
        "content": """
Members aged 60 or above may access retirement benefits.

Tax-free thresholds may apply.
Proof of age and identity required.
"""
    },

    {
        "docId": "POL-004",
        "title": "Tax Implications – Early Release",
        "category": "Tax",
        "tags": ["tax", "withdrawal"],
        "content": """
Early withdrawals may be taxed at marginal rate.

Agents must disclose:
- Tax payable
- Impact on future retirement savings
- Reporting obligations
"""
    },

    {
        "docId": "POL-005",
        "title": "Vulnerable Customer Handling Policy",
        "category": "Compliance",
        "tags": ["vulnerable", "mental health", "hardship"],
        "content": """
Customers identified as vulnerable require additional care.

Agents must:
- Speak clearly and empathetically
- Offer extended processing support
- Escalate if necessary
"""
    },

    {
        "docId": "POL-006",
        "title": "Fraud & Risk Monitoring Policy",
        "category": "Risk",
        "tags": ["fraud", "risk", "suspicious"],
        "content": """
Accounts flagged for fraud require supervisor approval before processing withdrawals.

Escalation mandatory for high-risk profiles.
"""
    }
]


def search_knowledge(query: str):
    results = []
    query_lower = query.lower()

    for doc in KNOWLEDGE_BASE:
        if any(tag in query_lower for tag in doc["tags"]):
            results.append(doc)

    return results
