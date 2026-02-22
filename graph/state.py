# graph/state.py — LangGraph Agent State for Insurance FNOL

from typing import TypedDict, Optional


class AgentState(TypedDict):
    transcript: str
    full_transcript: str
    is_finalized: bool

    # Processing outputs
    intent: Optional[str]
    claim_type: Optional[str]
    entities: Optional[dict]
    member_data: Optional[dict]
    knowledge_docs: Optional[list[dict]]
    compliance_alerts: Optional[list[dict]]

    # Final output
    suggestion: Optional[str]
