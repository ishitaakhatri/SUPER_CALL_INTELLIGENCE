# graph/graph.py

from langgraph.graph import StateGraph
from graph.state import AgentState
from graph.nodes import (
    intent_node,
    entity_node,
    member_node,
    knowledge_node,
    suggestion_node
)


def build_graph():

    builder = StateGraph(AgentState)

    builder.add_node("intent", intent_node)
    builder.add_node("entity", entity_node)
    builder.add_node("knowledge", knowledge_node)
    builder.add_node("member", member_node)
    builder.add_node("suggestion", suggestion_node)

    # Entry
    builder.set_entry_point("intent")

    # Parallel branches
    builder.add_edge("intent", "entity")
    builder.add_edge("intent", "knowledge")

    builder.add_edge("entity", "member")

    # Merge before suggestion
    builder.add_edge("member", "suggestion")
    builder.add_edge("knowledge", "suggestion")

    builder.set_finish_point("suggestion")

    return builder.compile()
