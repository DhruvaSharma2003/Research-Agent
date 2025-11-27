import streamlit as st

from src.graph import build_research_graph


def main():
    st.set_page_config(page_title="Research-Agent", page_icon="🧠", layout="wide")
    st.title("🧠 Research-Agent")
    st.write("AI-powered research assistant using LangGraph, Tavily, and Google Docs.")

    query = st.text_area(
        "Enter your research question",
        placeholder="e.g., What are the latest approaches for time series forecasting in crypto markets?",
        height=120,
    )

    # Build the graph once per session
    if "graph" not in st.session_state:
        st.session_state.graph = build_research_graph()

    if st.button("Run Research", type="primary", disabled=not query.strip()):
        with st.spinner("Running research pipeline..."):
            graph = st.session_state.graph
            result_state = graph(query=query)

        st.success("Research pipeline completed.")

        report_md = result_state.get("report_markdown")
        st.subheader("Report preview")
        st.markdown(report_md or "_No report generated yet._")

        drive_link = result_state.get("drive_file_link")
        if drive_link:
            st.markdown(f"[Open in Google Docs]({drive_link})")


if __name__ == "__main__":
    main()

