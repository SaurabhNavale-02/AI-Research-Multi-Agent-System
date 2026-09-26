import io
import contextlib
from datetime import datetime

import streamlit as st

from pipeline import run_research_pipeline


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Research Studio",
    page_icon="🔬",
    layout="wide",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    #MainMenu, footer, header { visibility: hidden; }

    .stApp { background: #f8fafc; }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    html, body, [class*="css"] {
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    /* HERO */
    .hero { padding: 1rem 0 2rem 0; }
    .hero-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 999px;
        background: #eef2ff;
        color: #4f46e5;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-size: 3rem;
        line-height: 1.1;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: #0f172a;
        margin: 0;
    }
    .hero-title span { color: #6366f1; }
    .hero-subtitle {
        max-width: 700px;
        margin-top: 0.9rem;
        color: #64748b;
        font-size: 1rem;
        line-height: 1.7;
    }

    /* INPUT CARD — styled directly on the real form container so it
       actually wraps the widgets inside it (no hand-rolled open/close divs) */
    div[data-testid="stForm"] {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.4rem;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.05);
        margin-bottom: 0.5rem;
    }
    .input-title {
        font-size: 0.9rem;
        font-weight: 700;
        color: #334155;
        margin-bottom: 0.5rem;
    }
    .input-description {
        font-size: 0.78rem;
        color: #94a3b8;
        margin: 0.6rem 0 2rem 0;
    }

    .stTextInput input {
        height: 3.1rem;
        border-radius: 10px;
        border: 1px solid #cbd5e1;
        background: white;
        font-size: 0.95rem;
        padding-left: 1rem;
    }
    .stTextInput input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.12);
    }

    div[data-testid="stFormSubmitButton"] button {
        height: 3.1rem;
        border-radius: 10px;
        background: #4f46e5;
        color: white;
        border: none;
        font-weight: 700;
        transition: all 0.2s ease;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        background: #4338ca;
        color: white;
        transform: translateY(-1px);
    }

    /* SECTION TITLE */
    .section-title {
        font-size: 1rem;
        font-weight: 750;
        color: #0f172a;
        margin-bottom: 0.8rem;
    }

    /* AGENT WORKFLOW */
    .workflow {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.8rem;
        margin-bottom: 2rem;
    }
    .agent-card {
        position: relative;
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1rem;
        min-height: 115px;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.035);
        transition: all 0.2s ease;
    }
    .agent-card.done {
        border-color: #bbf7d0;
        background: #f0fdf4;
    }
    .agent-icon {
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        background: #eef2ff;
        font-size: 1rem;
        margin-bottom: 0.65rem;
    }
    .agent-card.done .agent-icon { background: #dcfce7; }
    .agent-name { font-size: 0.88rem; font-weight: 750; color: #1e293b; }
    .agent-description { font-size: 0.72rem; color: #94a3b8; margin-top: 0.25rem; }
    .agent-arrow {
        position: absolute;
        right: -0.65rem;
        top: 43%;
        color: #94a3b8;
        font-size: 1rem;
        z-index: 2;
    }
    .agent-check {
        position: absolute;
        top: 0.7rem;
        right: 0.8rem;
        color: #10b981;
        font-weight: 800;
        font-size: 0.85rem;
    }

    /* EMPTY STATE */
    .empty-state { text-align: center; padding: 3rem 1rem; color: #64748b; }
    .empty-icon { font-size: 2.5rem; margin-bottom: 0.7rem; }
    .empty-title { font-size: 1.05rem; font-weight: 700; color: #334155; }
    .empty-description { font-size: 0.85rem; margin-top: 0.35rem; }

    /* STATUS */
    .success-status {
        padding: 0.8rem 1rem;
        border-radius: 10px;
        background: #ecfdf5;
        border: 1px solid #bbf7d0;
        color: #047857;
        font-size: 0.85rem;
        font-weight: 650;
        margin-bottom: 1rem;
    }

    /* RESULT HEADER */
    .result-title { font-size: 1.3rem; font-weight: 800; color: #0f172a; margin-top: 1.5rem; }
    .result-topic { color: #94a3b8; font-size: 0.8rem; margin-top: 0.2rem; margin-bottom: 1rem; }

    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.25rem;
        background: #f1f5f9;
        padding: 0.25rem;
        border-radius: 11px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.55rem 0.9rem;
        font-size: 0.8rem;
        font-weight: 650;
        color: #64748b;
    }
    .stTabs [aria-selected="true"] {
        background: white;
        color: #4f46e5;
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.08);
    }

    /* DOWNLOAD BUTTON */
    .stDownloadButton button {
        border-radius: 9px;
        border: 1px solid #cbd5e1;
        background: white;
        color: #334155;
        font-weight: 650;
    }
    .stDownloadButton button:hover { border-color: #6366f1; color: #4f46e5; }

    /* FOOTER */
    .app-footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.2rem;
        border-top: 1px solid #e2e8f0;
        color: #94a3b8;
        font-size: 0.75rem;
    }

    @media (max-width: 800px) {
        .hero-title { font-size: 2.2rem; }
        .workflow { grid-template-columns: repeat(2, 1fr); }
        .agent-arrow { display: none; }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def to_text(value) -> str:
    """Safely turn a chain/agent result into plain text.

    Handles plain strings as well as LangChain message objects
    (e.g. AIMessage) that expose a `.content` attribute, so the UI
    never shows a raw object repr like `content='...' additional_kwargs=...`.
    """
    if value is None:
        return ""
    if hasattr(value, "content"):
        return str(value.content)
    return str(value)


STEP_MARKERS = [
    "step 1 - search agent",
    "step 2 - reader agent",
    "step 3 - writer",
    "step 4 - critic",
]


def parse_completed_steps(log: str) -> list[int]:
    log_lower = log.lower()
    return [i for i, marker in enumerate(STEP_MARKERS) if marker in log_lower]


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "state": None,
    "log": "",
    "topic": "",
    "error": None,
    "steps_done": [],
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">✦ GENERATIVE AI RESEARCH SYSTEM</div>
        <div class="hero-title">AI Research <span>Studio</span></div>
        <div class="hero-subtitle">
            Research any topic using a coordinated team of AI agents.
            Search the web, read relevant sources, generate a structured
            report, and review the result automatically.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# INPUT (single self-contained form — CSS styles it as a card,
# no manual div open/close spanning multiple markdown calls)
# ============================================================

with st.form("research_form"):
    st.markdown('<div class="input-title">What would you like to research?</div>', unsafe_allow_html=True)

    topic = st.text_input(
        "Research topic",
        value=st.session_state.topic,
        placeholder="e.g. Impact of Generative AI on software development",
        label_visibility="collapsed",
    )

    submitted = st.form_submit_button("🚀 Start Research", use_container_width=True)

    st.markdown(
        '<div class="input-description">The AI agents will search, read, write and review your research.</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# WORKFLOW (highlights steps that actually completed, once available)
# ============================================================

st.markdown('<div class="section-title">Agent Workflow</div>', unsafe_allow_html=True)

AGENTS = [
    ("🔎", "Search Agent", "Find relevant information"),
    ("📖", "Reader Agent", "Extract source content"),
    ("✍️", "Writer Agent", "Generate research report"),
    ("🔍", "Critic Agent", "Review the generated report"),
]

done_steps = st.session_state.steps_done
cards_html = '<div class="workflow">'
for i, (icon, name, desc) in enumerate(AGENTS):
    done_class = "done" if i in done_steps else ""
    check = '<div class="agent-check">✓</div>' if i in done_steps else ""
    arrow = '<div class="agent-arrow">→</div>' if i < len(AGENTS) - 1 else ""
    cards_html += (
        f'<div class="agent-card {done_class}">'
        f'{check}'
        f'<div class="agent-icon">{icon}</div>'
        f'<div class="agent-name">{name}</div>'
        f'<div class="agent-description">{desc}</div>'
        f'{arrow}'
        f'</div>'
    )
cards_html += "</div>"
st.markdown(cards_html, unsafe_allow_html=True)


# ============================================================
# RUN RESEARCH
# ============================================================

if submitted:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.topic = topic
        st.session_state.state = None
        st.session_state.error = None
        st.session_state.log = ""
        st.session_state.steps_done = []

        buffer = io.StringIO()
        with st.spinner("AI agents are researching your topic..."):
            try:
                with contextlib.redirect_stdout(buffer):
                    result_state = run_research_pipeline(topic)
                st.session_state.state = result_state
            except Exception as e:
                st.session_state.error = f"{type(e).__name__}: {e}"
            finally:
                st.session_state.log = buffer.getvalue()
                st.session_state.steps_done = parse_completed_steps(st.session_state.log)

        st.rerun()  # refresh so the workflow cards above reflect steps_done


# ============================================================
# ERROR
# ============================================================

if st.session_state.error:
    st.error(f"Research pipeline failed: {st.session_state.error}")
    if st.session_state.log:
        with st.expander("View execution log"):
            st.code(st.session_state.log, language="text")


# ============================================================
# RESULTS
# ============================================================

elif st.session_state.state:
    state = st.session_state.state

    st.markdown('<div class="success-status">✓ Research completed successfully</div>', unsafe_allow_html=True)
    st.markdown('<div class="result-title">Research Results</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-topic">{st.session_state.topic}</div>', unsafe_allow_html=True)

    report_tab, review_tab, search_tab, source_tab, log_tab = st.tabs(
        ["📄 Report", "🔍 AI Review", "🌐 Search Results", "📖 Source", "⚙️ Execution Log"]
    )

    with report_tab:
        report = to_text(state.get("report", ""))
        st.markdown(report)
        st.divider()
        st.download_button(
            "⬇ Download Report",
            data=report,
            file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
        )

    with review_tab:
        st.markdown(to_text(state.get("feedback", "")))

    with search_tab:
        st.code(to_text(state.get("search_results", "")), language="text")

    with source_tab:
        st.markdown("### Extracted Source Content")
        st.text_area(
            "Source content",
            value=to_text(state.get("scraped_content", "")),
            height=500,
            label_visibility="collapsed",
        )

    with log_tab:
        st.code(st.session_state.log or "(no output captured)", language="text")


# ============================================================
# EMPTY STATE
# ============================================================

else:
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-icon">🔬</div>
            <div class="empty-title">Ready to research</div>
            <div class="empty-description">
                Enter a topic above and let your AI research team get to work.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="app-footer">
        AI Research Studio · Multi-Agent Generative AI System
        <br>
        Built with Python · LangChain · Groq · Tavily · Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)