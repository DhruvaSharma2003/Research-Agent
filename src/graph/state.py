from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class Source:
    title: str
    url: str
    content: str
    meta: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentState:
    query: str
    plan: Optional[Dict[str, Any]] = None
    sources: List[Source] = field(default_factory=list)
    notes: List[Dict[str, Any]] = field(default_factory=list)
    report_markdown: Optional[str] = None
    drive_file_link: Optional[str] = None
