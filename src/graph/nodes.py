import json
from typing import Dict, Any, List

from langchain_openai import ChatOpenAI
from tavily import TavilyClient

from src.config import TAVILY_API_KEY
from .state import AgentState

# ---------- LLMs ----------

# Small / cheap model for planning
planner_llm = ChatOpenAI(
    model="gpt-4o-mini",  # adjust if you prefer another model
    temperature=0.0,
)

# Slightly larger / richer model for writing the report
writer_llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.3,
)

# ---------- Tavily client ----------

if TAVILY_API_KEY:
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
else:
    # Tavily can also read TAVILY_API_KEY directly from environment
    tavily_client = TavilyClient()


# ---------- Nodes ----------

def plan_research(state: AgentState) -> Dict[str, Any]:
    """
    Use LLM to turn the main query into a small research plan:
    - subquestions
    - what to focus on
    - what sources to prefer
    """
    query = state["query"]

    prompt = (
        "You are a research planning assistant.\n\n"
        f"User question:\n{query}\n\n"
        "Break this into 3–6 concrete research subquestions.\n"
        "Respond with **ONLY valid JSON** in this schema:\n"
        "{\n"
        '  "subquestions": [string, ...],\n'
        '  "focus": "1–2 sentence description of what to prioritize",\n'
        '  "source_preferences": "what kinds of sources to prefer (papers, docs, news, etc.)"\n'
        "}\n"
    )

    msg = planner_llm.invoke(prompt)
    raw_content = msg.content if isinstance(msg.content, str) else str(msg.content)

    try:
        plan = json.loads(raw_content)
    except Exception:
        # Fallback if model doesn't return perfect JSON
        plan = {
            "subquestions": [query],
            "focus": "General overview of the topic.",
            "source_preferences": "Mixed high-quality web sources.",
        }

    return {"plan": plan}


def web_search(state: AgentState) -> Dict[str, Any]:
    """
    Use Tavily to search the web for each subquestion (or the main query if no plan).
    Returns a list of source dicts: title, url, content, etc.
    """
    plan = state.get("plan") or {}
    subquestions: List[str] = plan.get("subquestions") or [state["query"]]

    all_results: List[Dict[str, Any]] = []

    for sq in subquestions:
        try:
            resp = tavily_client.search(sq, max_results=4)
        except Exception as e:
            # In case Tavily errors for a subquestion, skip it instead of crashing
            print(f"Tavily error for subquestion '{sq}': {e}")
            continue

        for r in resp.get("results", []):
            all_results.append(
                {
                    "subquestion": sq,
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "content": r.get("content", ""),
                    "score": r.get("score"),
                }
            )

    # Simple dedupe by URL
    seen_urls = set()
    deduped_results: List[Dict[str, Any]] = []
    for r in all_results:
        url = r.get("url")
        if not url:
            deduped_results.append(r)
            continue
        if url in seen_urls:
            continue
        seen_urls.add(url)
        deduped_results.append(r)

    return {"sources": deduped_results}


def write_report(state: AgentState) -> Dict[str, Any]:
    """
    Use LLM to synthesize a structured markdown report from the plan + sources.
    """
    query = state["query"]
    plan = state.get("plan") or {}
    sources = state.get("sources") or []

    # Build compact sources summary for the prompt
    source_snippets = []
    for i, s in enumerate(sources[:10], start=1):  # cap at 10 for context size
        snippet = s.get("content", "") or ""
        if len(snippet) > 800:
            snippet = snippet[:800] + "..."

        source_snippets.append(
            f"[{i}] {s.get('title', '(no title)')} — {s.get('url', '')}\n"
            f"Subquestion: {s.get('subquestion', '')}\n"
            f"Snippet: {snippet}\n"
        )

    sources_block = "\n\n".join(source_snippets) if source_snippets else "No web sources were found."

    system_prompt = (
        "You are an expert research assistant. "
        "Your job is to synthesize web sources into a **clear, structured markdown report**.\n"
        "Be precise, grounded in the provided sources, and cite them with indices like [1], [2], etc.\n"
        "If something is not supported by the sources, say that explicitly instead of hallucinating."
    )

    user_prompt = (
        f"Main research question:\n{query}\n\n"
        f"Plan (may be partial):\n{json.dumps(plan, indent=2)}\n\n"
        "Here are web sources you can use (indexed as [1], [2], ...):\n"
        f"{sources_block}\n\n"
        "Write a markdown report with the following structure:\n"
        "# Title\n"
        "## Abstract\n"
        "## Introduction\n"
        "## Background / Key Concepts\n"
        "## Main Discussion (sections per subquestion if possible)\n"
        "## Limitations of this report\n"
        "## Future research directions\n"
        "## References\n"
        "In References, list [index] Title — URL.\n"
    )

    msg = writer_llm.invoke(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )

    report = msg.content if isinstance(msg.content, str) else str(msg.content)

    return {"report_markdown": report}


def upload_to_drive(state: AgentState) -> Dict[str, Any]:
    """
    Placeholder for now – later we'll create a Google Doc and return a link.
    """
    # In Step 4 we'll implement Google Docs + Drive here.
    return {}
