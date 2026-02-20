# graph/state.py

from typing import TypedDict, Optional, Dict, List


class AgentState(TypedDict):
    transcript: str

    intent: Optional[str]
    entities: Optional[Dict]
    member_data: Optional[Dict]
    knowledge_docs: Optional[List[Dict]]

    suggestion: Optional[str]
