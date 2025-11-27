from .state import AgentState

def plan_research(state: AgentState) -> AgentState:
    # TODO: implement using LLM
    return state

def web_search(state: AgentState) -> AgentState:
    # TODO: implement using Tavily
    return state

def write_report(state: AgentState) -> AgentState:
    # TODO: implement using LLM
    state.report_markdown = "# Demo report\n\nThis is a placeholder report."
    return state

def upload_to_drive(state: AgentState) -> AgentState:
    # TODO: implement using Google Docs + Drive
    state.drive_file_link = None
    return state
