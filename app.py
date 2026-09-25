"""
Streamlit UI for the multi-agent research pipeline defined in pipeline.py

Run with:
    streamlit run streamlit_app.py

Requires pipeline.py (and the agents.py module it imports from) to be in the
same folder, or importable on your PYTHONPATH.
"""

import io
import sys
import contextlib
from datetime import datetime

import streamlit as st

# --- Import the existing pipeline, unmodified ---------------------------
from pipeline import run_research_pipeline


# --- Page setup -----------------------------------------------------------
st.set_page_config(
    page_title="Multi-Agent Research Pipeline",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 Multi-Agent Research Pipeline")
st.caption(
    "Search agent → Reader agent → Writer chain → Critic chain, "
    "all wired together via `pipeline.run_research_pipeline`."
)

# --- Session state ----------------------------------------------------------
if "state" not in st.session_state:
    st.session_state.state = None
if "log" not in st.session_state:
    st.session_state.log = ""
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "error" not in st.session_state:
    st.session_state.error = None

# --- Sidebar ----------------------------------------------------------------
with st.sidebar:
    st.header("About")
    st.write(
        "This app calls your existing 4-step pipeline:\n\n"
        "1. **Search agent** finds sources\n"
        "2. **Reader agent** scrapes the best one\n"
        "3. **Writer chain** drafts a report\n"
        "4. **Critic chain** reviews it\n"
    )
    st.divider()
    if st.button("🗑️ Clear results", use_container_width=True):
        st.session_state.state = None
        st.session_state.log = ""
        st.session_state.error = None
        st.rerun()

# --- Input form ---------------------------------------------------------
with st.form("topic_form"):
    topic = st.text_input(
        "Research topic",
        value=st.session_state.topic,
        placeholder="e.g. Impact of quantum computing on cryptography",
    )
    submitted = st.form_submit_button("Run pipeline 🚀", use_container_width=True)

if submitted:
    if not topic.strip():
        st.warning("Please enter a topic before running the pipeline.")
    else:
        st.session_state.topic = topic
        st.session_state.state = None
        st.session_state.error = None

        buf = io.StringIO()
        with st.spinner(f"Running the pipeline on: **{topic}** — this can take a minute..."):
            try:
                with contextlib.redirect_stdout(buf):
                    result_state = run_research_pipeline(topic)
                st.session_state.state = result_state
            except Exception as e:
                st.session_state.error = f"{type(e).__name__}: {e}"
            finally:
                st.session_state.log = buf.getvalue()

# --- Results --------------------------------------------------------------
if st.session_state.error:
    st.error(f"Pipeline failed: {st.session_state.error}")
    if st.session_state.log:
        with st.expander("Execution log (up to the point of failure)"):
            st.code(st.session_state.log, language="text")

elif st.session_state.state:
    state = st.session_state.state
    st.success(f"Pipeline finished for topic: **{st.session_state.topic}**")

    tab_report, tab_critic, tab_search, tab_scraped, tab_log = st.tabs(
        ["📄 Report", "🧐 Critic Feedback", "🔍 Search Results", "📰 Scraped Content", "🪵 Execution Log"]
    )

    with tab_report:
        report = str(state.get("report", ""))
        st.markdown(report)
        st.download_button(
            "⬇️ Download report (.md)",
            data=report,
            file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with tab_critic:
        st.markdown(str(state.get("feedback", "")))

    with tab_search:
        st.text(state.get("search_results", ""))

    with tab_scraped:
        st.text(state.get("scraped_content", ""))

    with tab_log:
        st.code(st.session_state.log or "(no output captured)", language="text")

else:
    st.info("Enter a topic above and click **Run pipeline** to get started.")