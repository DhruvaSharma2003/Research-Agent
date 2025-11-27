from langgraph.graph import StateGraph, START, END

from .state import AgentState
from .nodes import plan_research, web_search, write_report, upload_to_drive


def build_research_graph():
    """
    Build and compile the LangGraph StateGraph for the research workflow.
    Returns a callable that takes `query: str` and returns the final AgentState dict.
    """
    builder = StateGraph(AgentState)

    # Register nodes
    builder.add_node("plan_research", plan_research)
    builder.add_node("web_search", web_search)
    builder.add_node("write_report", write_report)
    builder.add_node("upload_to_drive", upload_to_drive)

    # Linear flow for MVP:
    # START -> plan_research -> web_search -> write_report -> upload_to_drive -> END
    builder.add_edge(START, "plan_research")
    builder.add_edge("plan_research", "web_search")
    builder.add_edge("web_search", "write_report")
    builder.add_edge("write_report", "upload_to_drive")
    builder.add_edge("upload_to_drive", END)

    graph = builder.compile()

    # Wrap into a simple callable so `app.py` doesn't need to know LangGraph internals
    def run_graph(query: str) -> AgentState:
        # We only provide the initial "query" field; other keys are optional
        final_state: AgentState = graph.invoke({"query": query})
        return final_state

    return run_graph

