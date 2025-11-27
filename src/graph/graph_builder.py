from .state import AgentState
from .nodes import plan_research, web_search, write_report, upload_to_drive

def build_research_graph():
    """
    For now, returns a simple callable that mimics a graph.

    Later we will replace this with a real LangGraph graph object.
    """
    def run_graph(query: str) -> AgentState:
        state = AgentState(query=query)

        # Simple linear flow (stubbed for now)
        state = plan_research(state)
        state = web_search(state)
        state = write_report(state)
        state = upload_to_drive(state)

        return state

    return run_graph
