from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict


class AgentState(TypedDict, total=False):
    """
    Shared state for the research graph.
    LangGraph will pass this between nodes.
    """
    # User query
    query: str

    # Research plan (subquestions, focus, etc.)
    plan: Dict[str, Any]

    # Raw web sources from Tavily
    sources: List[Dict[str, Any]]

    # (Optional) intermediate notes if we add them later
    notes: List[Dict[str, Any]]

    # Final report in markdown
    report_markdown: str

    # Google Docs link (we'll fill this in Step 4)
    drive_file_link: Optional[str]
