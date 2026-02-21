# graph/graph.py — LangGraph state machine for FNOL processing

from langgraph.graph import StateGraph
from graph.state import AgentState
from graph.nodes import (
    intent_node,
    entity_node,
    member_node,
    knowledge_node,
    compliance_node,
    suggestion_node,
)


def build_graph():
    """
    Build the LangGraph processing pipeline.

    Flow:
        intent ──┬──> entity ──> member ──┐
                 ├──> knowledge ──────────┤
                 └──> compliance ─────────┘
                                          └──> suggestion
    """
    builder = StateGraph(AgentState)

    # Register all nodes
    builder.add_node("intent", intent_node)
    builder.add_node("entity", entity_node)
    builder.add_node("knowledge", knowledge_node)
    builder.add_node("compliance", compliance_node)
    builder.add_node("member", member_node)
    builder.add_node("suggestion", suggestion_node)

    # Entry point
    builder.set_entry_point("intent")

    # After intent → fan out to three parallel branches
    builder.add_edge("intent", "entity")
    builder.add_edge("intent", "knowledge")
    builder.add_edge("intent", "compliance")

    # Entity → member lookup
    builder.add_edge("entity", "member")

    # All branches merge into suggestion
    builder.add_edge("member", "suggestion")
    builder.add_edge("knowledge", "suggestion")
    builder.add_edge("compliance", "suggestion")

    # Finish
    builder.set_finish_point("suggestion")

    return builder.compile()
