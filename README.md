# Research-Agent 🧠🔍

An AI-powered research assistant built with **LangGraph**, **Tavily**, and **Streamlit**.

## What it does

- Takes a natural language research query from the user.
- Plans sub-questions and a research strategy using an LLM.
- Searches the web using **Tavily** and selects high-quality sources.
- Synthesizes the information into a structured research report.
- Saves the final report as a **Google Docs document** in the user's Google Drive (coming soon).

## Tech stack

- **Frontend / UI**: Streamlit
- **Agent Orchestration**: LangGraph
- **Web Search & Browsing**: Tavily API
- **LLM**: OpenAI (via `langchain-openai`)
- **Storage**: Google Drive + Google Docs APIs
