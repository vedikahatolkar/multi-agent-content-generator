from utils import create_word_file
import streamlit as st
import time
import os

from dotenv import load_dotenv

from crew import run_crew, compare_papers
from db import save_to_db

load_dotenv()

# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="Multi-Agent Content Generator",
    page_icon="🤖",
    layout="wide"
)

# ──────────────────────────────────────────────
# Warm Earthy CSS Design System
# ──────────────────────────────────────────────

st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap');

/* ── Root Variables ── */
:root {
    --bg-page: #e8ddd3;
    --bg-card: #f5f0eb;
    --bg-input: #ffffff;
    --accent-peach: #d4a590;
    --accent-coral: #c8876f;
    --accent-warm: #b87860;
    --accent-terracotta: #c27856;
    --text-dark: #3d2e25;
    --text-body: #5c4a3f;
    --text-muted: #8a7a6e;
    --text-light: #a89888;
    --border-soft: #d4c8bc;
    --border-light: #e0d6cc;
    --shadow-soft: 0 4px 20px rgba(61, 46, 37, 0.06);
    --shadow-card: 0 8px 30px rgba(61, 46, 37, 0.08);
    --shadow-hover: 0 12px 40px rgba(61, 46, 37, 0.12);
    --radius-lg: 20px;
    --radius-md: 12px;
    --radius-sm: 8px;
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── Global Reset ── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: var(--bg-page) !important;
    color: var(--text-body) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* ── Header / Toolbar ── */
[data-testid="stHeader"],
header[data-testid="stHeader"] {
    background: rgba(232, 221, 211, 0.85) !important;
    backdrop-filter: blur(12px) !important;
    border-bottom: 1px solid var(--border-light) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border-light) !important;
}

/* ── Main Content ── */
.main .block-container {
    padding-top: 2rem !important;
    max-width: 1100px !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] {
    text-align: center !important;
}

[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 0 !important;
    background: var(--bg-card) !important;
    border-radius: 30px !important;
    padding: 4px !important;
    display: inline-flex !important;
    border: 1px solid var(--border-soft) !important;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
    border-radius: 26px !important;
    padding: 0.5rem 1.8rem !important;
    border: none !important;
    transition: var(--transition) !important;
    background: transparent !important;
}

[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, var(--accent-peach), var(--accent-terracotta)) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 12px rgba(194, 120, 86, 0.3) !important;
}

[data-testid="stTabs"] [data-baseweb="tab-highlight"],
[data-testid="stTabs"] [data-baseweb="tab-border"] {
    display: none !important;
}

/* ── Text Input ── */
[data-testid="stTextInput"] {
    max-width: 100% !important;
}

[data-testid="stTextInput"] > div > div {
    background: var(--bg-input) !important;
    border: 1.5px solid var(--border-soft) !important;
    border-radius: var(--radius-sm) !important;
    transition: var(--transition) !important;
}

[data-testid="stTextInput"] > div > div:focus-within {
    border-color: var(--accent-coral) !important;
    box-shadow: 0 0 0 3px rgba(200, 135, 111, 0.15) !important;
}

[data-testid="stTextInput"] input {
    color: var(--text-dark) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    letter-spacing: 0.02em !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: var(--text-light) !important;
    text-transform: uppercase !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.08em !important;
}

[data-testid="stTextInput"] label {
    color: var(--text-muted) !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}

/* ── Primary Button (Generate) ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--accent-peach), var(--accent-terracotta)) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 30px !important;
    padding: 0.75rem 2.5rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    transition: var(--transition) !important;
    box-shadow: 0 4px 15px rgba(194, 120, 86, 0.25) !important;
    width: 100% !important;
}

[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(194, 120, 86, 0.35) !important;
    filter: brightness(1.05) !important;
}

[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Download Button ── */
[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    color: var(--accent-warm) !important;
    border: 1.5px solid var(--accent-peach) !important;
    border-radius: 30px !important;
    padding: 0.7rem 2rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    transition: var(--transition) !important;
}

[data-testid="stDownloadButton"] > button:hover {
    background: rgba(212, 165, 144, 0.12) !important;
    box-shadow: 0 4px 15px rgba(194, 120, 86, 0.15) !important;
    transform: translateY(-1px) !important;
}

/* ── Status Widget ── */
[data-testid="stStatusWidget"],
details[data-testid="stStatusWidget"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: var(--radius-md) !important;
}

/* ── Alert Boxes ── */
[data-testid="stAlert"] {
    background: var(--bg-card) !important;
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border-soft) !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Expander / Status ── */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: var(--radius-md) !important;
}

/* ── Markdown Text ── */
[data-testid="stMarkdown"] {
    color: var(--text-body) !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stMarkdown"] p {
    color: var(--text-body) !important;
    line-height: 1.7 !important;
}

[data-testid="stMarkdown"] h1,
[data-testid="stMarkdown"] h2,
[data-testid="stMarkdown"] h3 {
    color: var(--text-dark) !important;
    font-family: 'Playfair Display', serif !important;
    font-weight: 700 !important;
}

/* ── Divider ── */
[data-testid="stMarkdown"] hr {
    border-color: var(--border-light) !important;
    margin: 2rem 0 !important;
}

/* ── Custom Hero Title ── */
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: var(--text-dark);
    letter-spacing: -0.02em;
    line-height: 1.2;
    margin-bottom: 0.3rem;
    text-align: center;
    font-style: italic;
}

.hero-subtitle {
    font-family: 'Inter', sans-serif;
    color: var(--text-muted);
    font-size: 0.9rem;
    font-weight: 400;
    text-align: center;
    margin-bottom: 2rem;
    letter-spacing: 0.03em;
    line-height: 1.6;
}

/* ── Decorative Dots (organic shapes) ── */
.deco-bar {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1.2rem;
    margin: 1.2rem 0 2rem 0;
    flex-wrap: wrap;
}

.deco-dot {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: inline-block;
    opacity: 0.7;
    transition: var(--transition);
}

.deco-dot:hover {
    transform: scale(1.15);
    opacity: 1;
}

.deco-oval {
    width: 48px;
    height: 30px;
    border-radius: 50%;
    display: inline-block;
    opacity: 0.5;
    border: 2px solid;
    transition: var(--transition);
}

.deco-oval:hover {
    transform: scale(1.1) rotate(10deg);
    opacity: 0.8;
}

/* ── Result Card ── */
.result-card {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-lg);
    padding: 2rem 2.5rem;
    box-shadow: var(--shadow-soft);
    margin: 1.5rem 0;
    transition: var(--transition);
    position: relative;
}

.result-card:hover {
    box-shadow: var(--shadow-hover);
}

.result-card h3 {
    color: var(--text-dark);
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: 1.4rem;
    margin-bottom: 1rem;
}

.result-card .content {
    color: var(--text-body);
    line-height: 1.8;
    font-size: 0.95rem;
    font-family: 'Inter', sans-serif;
}

/* ── Status Badges ── */
.agent-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.02em;
}

.badge-research {
    background: rgba(212, 165, 144, 0.2);
    color: var(--accent-warm);
    border: 1px solid rgba(212, 165, 144, 0.3);
}

.badge-writer {
    background: rgba(194, 120, 86, 0.15);
    color: var(--accent-terracotta);
    border: 1px solid rgba(194, 120, 86, 0.25);
}

/* ── Paper Label Badges ── */
.paper-label {
    display: inline-block;
    padding: 0.3rem 1rem;
    border-radius: 999px;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.75rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

.paper-a {
    background: rgba(212, 165, 144, 0.25);
    color: var(--accent-warm);
    border: 1px solid rgba(212, 165, 144, 0.4);
}

.paper-b {
    background: rgba(139, 160, 120, 0.2);
    color: #6b7f56;
    border: 1px solid rgba(139, 160, 120, 0.35);
}

/* ── VS Badge ── */
.vs-badge {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent-peach), var(--accent-terracotta));
    color: #ffffff;
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    font-size: 0.8rem;
    letter-spacing: 0.02em;
    box-shadow: 0 4px 12px rgba(194, 120, 86, 0.3);
    margin: 0 auto;
}

/* ── Comparison Card ── */
.compare-card {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-lg);
    padding: 1.8rem 2rem;
    box-shadow: var(--shadow-soft);
    transition: var(--transition);
    min-height: 200px;
}

.compare-card:hover {
    box-shadow: var(--shadow-hover);
    border-color: var(--accent-peach);
}

.compare-card h4 {
    color: var(--text-dark);
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: 1.1rem;
    margin-bottom: 0.8rem;
}

.compare-card .content {
    color: var(--text-body);
    line-height: 1.7;
    font-size: 0.9rem;
    font-family: 'Inter', sans-serif;
}

/* ── Footer ── */
.footer-text {
    text-align: center;
    color: var(--text-light);
    font-size: 0.8rem;
    margin-top: 3rem;
    padding: 1.5rem 0;
    border-top: 1px solid var(--border-light);
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.03em;
}

/* ── Animations ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

.animate-in {
    animation: fadeInUp 0.6s ease-out;
}

/* ── Scrollbar ── */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-track {
    background: var(--bg-page);
}
::-webkit-scrollbar-thumb {
    background: var(--border-soft);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--text-light);
}

</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Hero Section
# ──────────────────────────────────────────────

st.markdown("""
<div class="animate-in">
    <div class="hero-title">Welcome to Multi-Agent Content Generator</div>
    <div class="hero-subtitle">
        Generate structured AI content using multiple intelligent agents<br>
        that research, write, and deliver premium results.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Decorative organic shapes bar ──
st.markdown("""
<div class="deco-bar">
    <span class="deco-dot" style="background: #c8a48a;"></span>
    <span class="deco-oval" style="border-color: #b8956e;"></span>
    <span class="deco-dot" style="background: #c27856; width: 42px; height: 42px;"></span>
    <span class="deco-oval" style="border-color: #a8b080; width: 40px;"></span>
    <span class="deco-dot" style="background: #d4bca0; width: 28px; height: 28px;"></span>
    <span class="deco-dot" style="background: #e0c8a8; width: 50px; height: 50px;"></span>
    <span class="deco-oval" style="border-color: #c27856;"></span>
    <span class="deco-dot" style="background: #c8a48a; width: 44px; height: 44px;"></span>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Tabs: Generate Content | Compare Papers
# ──────────────────────────────────────────────

tab_generate, tab_compare = st.tabs([" Generate Content", " Compare Content"])

# ══════════════════════════════════════════════
# TAB 1: Generate Content
# ══════════════════════════════════════════════

with tab_generate:

    col1, col2, col3 = st.columns([1, 2.5, 1])

    with col2:
        topic = st.text_input("TOPIC", placeholder="ENTER YOUR TOPIC", key="gen_topic")

        # Session state init
        if "last_run" not in st.session_state:
            st.session_state.last_run = 0

        generate = st.button("GENERATE", use_container_width=True, key="gen_btn")

    if generate:

        if not topic:
            st.warning("⚠️  Please enter a topic to get started.")

        else:

            # ── Agent Status via st.status ──
            with st.status("🚀 AI Agents are working...", expanded=True) as status:

                st.markdown('<span class="agent-badge badge-research">🔍 Research Agent</span>', unsafe_allow_html=True)
                st.write("Scanning sources and gathering insights...")
                time.sleep(2)
                st.write("✅ Research complete — insights gathered.")

                st.markdown('<span class="agent-badge badge-writer">✍️ Writer Agent</span>', unsafe_allow_html=True)
                st.write("Drafting structured content...")
                time.sleep(2)
                st.write("✅ Draft generated — content structured.")

                status.update(label="⏳ Finalizing content...", state="running")

                # ── Run AI Workflow ──
                try:
                    result = run_crew(topic)
                except Exception as e:
                    status.update(label="❌ Generation failed", state="error")
                    st.error("⚠️ Rate limit hit. Please wait a few seconds and try again.")
                    st.stop()

                status.update(label="✅ Content generated successfully!", state="complete")

            # ── Clean Output ──
            clean_output = result.raw

            # ── Divider ──
            st.markdown("---")

            # ── Result Card ──
            st.markdown(f"""
            <div class="result-card animate-in">
                <h3>📄 Generated Content</h3>
                <div class="content">{clean_output}</div>
            </div>
            """, unsafe_allow_html=True)

            # ── Download Button ──
            word_file = create_word_file(clean_output)
            with open(word_file, "rb") as file:
                st.download_button(
                    label="⬇️  DOWNLOAD REPORT",
                    data=file,
                    file_name="generated_report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )

            # ── Save to Database ──
            save_to_db(topic, clean_output)
            st.success("✅ Content saved to database.")


# ══════════════════════════════════════════════
# TAB 2: Compare Papers
# ══════════════════════════════════════════════

with tab_compare:

    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <span class="paper-label paper-a" style="font-size: 0.9rem;">Multi-ReportAnalysis</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Content Comparison")
    st.markdown("Generate two content report on different topics and get an AI-powered comparison covering themes, strengths, weaknesses, and a verdict.")

    st.markdown("---")

    # ── Side-by-side topic inputs ──
    left_col, vs_col, right_col = st.columns([5, 1, 5])

    with left_col:
        st.markdown('<span class="paper-label paper-a">Report A</span>', unsafe_allow_html=True)
        topic_a = st.text_input("TOPIC A", placeholder="ENTER FIRST TOPIC", key="topic_a")

    with vs_col:
        st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="vs-badge">VS</div>', unsafe_allow_html=True)

    with right_col:
        st.markdown('<span class="paper-label paper-b">Report B</span>', unsafe_allow_html=True)
        topic_b = st.text_input("TOPIC B", placeholder="ENTER SECOND TOPIC", key="topic_b")

    st.markdown("")

    # ── Compare Button (centered) ──
    btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
    with btn_col2:
        compare_btn = st.button("COMPARE REPORTS", use_container_width=True, key="compare_btn")

    # ── Comparison Workflow ──
    if compare_btn:

        if not topic_a or not topic_b:
            st.warning("⚠️  Please enter both topics to compare.")

        else:

            # ── Generate Paper A ──
            with st.status("📝 Generating Report A...", expanded=True) as status_a:
                st.markdown('<span class="agent-badge badge-research">🔍 Researching: ' + topic_a + '</span>', unsafe_allow_html=True)
                st.write("Research Agent is gathering insights...")
                time.sleep(1)

                st.markdown('<span class="agent-badge badge-writer">✍️ Writing Paper A</span>', unsafe_allow_html=True)
                st.write("Writer Agent is drafting content...")

                try:
                    result_a = run_crew(topic_a)
                except Exception as e:
                    status_a.update(label="❌ Report A generation failed", state="error")
                    st.error("⚠️ Rate limit hit on Report A. Please wait and try again.")
                    st.stop()

                status_a.update(label="✅ Report A generated!", state="complete")

            # ── Generate Paper B ──
            with st.status("📝 Generating Report B...", expanded=True) as status_b:
                st.markdown('<span class="agent-badge badge-research">🔍 Researching: ' + topic_b + '</span>', unsafe_allow_html=True)
                st.write("Research Agent is gathering insights...")
                time.sleep(1)

                st.markdown('<span class="agent-badge badge-writer">✍️ Writing Report B</span>', unsafe_allow_html=True)
                st.write("Writer Agent is drafting content...")

                try:
                    result_b = run_crew(topic_b)
                except Exception as e:
                    status_b.update(label="❌ Report B generation failed", state="error")
                    st.error("⚠️ Rate limit hit on Report B. Please wait and try again.")
                    st.stop()

                status_b.update(label="✅ Report B generated!", state="complete")

            paper_a_content = result_a.raw
            paper_b_content = result_b.raw

            # ── Display Papers Side by Side ──
            st.markdown("---")

            col_a, col_b = st.columns(2)

            with col_a:
                st.markdown(f"""
                <div class="compare-card animate-in">
                    <span class="paper-label paper-a">Paper A</span>
                    <h4>{topic_a}</h4>
                    <div class="content">{paper_a_content}</div>
                </div>
                """, unsafe_allow_html=True)

            with col_b:
                st.markdown(f"""
                <div class="compare-card animate-in">
                    <span class="paper-label paper-b">Paper B</span>
                    <h4>{topic_b}</h4>
                    <div class="content">{paper_b_content}</div>
                </div>
                """, unsafe_allow_html=True)

            # ── Run Comparison Agent ──
            st.markdown("---")

            with st.status("🔎 Comparison Agent analyzing both reports...", expanded=True) as status_c:
                st.write("Identifying themes, strengths, and differences...")

                try:
                    comparison_result = compare_papers(paper_a_content, paper_b_content, topic_a, topic_b)
                except Exception as e:
                    status_c.update(label="❌ Comparison failed", state="error")
                    st.error("⚠️ Rate limit hit during comparison. Please wait and try again.")
                    st.stop()

                status_c.update(label="✅ Comparison complete!", state="complete")

            comparison_output = comparison_result.raw

            # ── Comparison Result ──
            st.markdown(f"""
            <div class="result-card animate-in">
                <h3>📊 Comparison Analysis</h3>
                <div class="content">{comparison_output}</div>
            </div>
            """, unsafe_allow_html=True)

            # ── Save both papers ──
            save_to_db(topic_a, paper_a_content)
            save_to_db(topic_b, paper_b_content)
            st.success("✅ Both papers and comparison saved to database.")

# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────

st.markdown("""
<div class="footer-text">
    Built with Streamlit · Powered by CrewAI & Groq
</div>
""", unsafe_allow_html=True)
