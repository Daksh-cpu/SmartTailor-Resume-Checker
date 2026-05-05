"""
app.py
SmartTailor — AI Resume × Job Description Matcher
Run with: streamlit run app.py
"""

import streamlit as st
import time
from pathlib import Path
from resume_parser import parse_resume
from jd_scraper import scrape_job_description
from ai_analyzer import run_full_analysis

# ── Page Config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="SmartTailor — AI Resume Matcher",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Load & inject external CSS ────────────────────────────────────────────────

_css_path = Path(__file__).parent / "static" / "style.css"
_css = _css_path.read_text(encoding="utf-8")
st.markdown(f"<style>{_css}</style>", unsafe_allow_html=True)

# ── Inject CSS-animated background orbs (pure CSS, no JS needed) ─────────────

st.markdown("""
<div class="st-orb orb-1"></div>
<div class="st-orb orb-2"></div>
<div class="st-orb orb-3"></div>
""", unsafe_allow_html=True)


# ── Hero Header ───────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero">
  <div class="scene-wrap">
    <div class="halo"></div>
    <div class="halo halo-2"></div>
    <div class="scene">
      <div class="face front">🎯</div>
      <div class="face back">🤖</div>
      <div class="face left">📄</div>
      <div class="face right">✨</div>
      <div class="face top">💡</div>
      <div class="face bottom">🚀</div>
    </div>
  </div>
  <div class="hero-badge">AI-Powered Career Tool</div>
  <h1>SmartTailor</h1>
  <p>AI-powered resume × job description matcher. Score your fit, find the gaps,
     and rewrite your bullets — in seconds.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Input Section ─────────────────────────────────────────────────────────────

col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.markdown(
        '<div class="section-title"><span class="step-badge">1</span> Upload Your Resume</div>',
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader(
        "Drag & drop or browse",
        type=["pdf", "txt"],
        label_visibility="collapsed",
        key="resume_upload",
    )
    if uploaded_file:
        st.success(f"✅ **{uploaded_file.name}** loaded ({uploaded_file.size // 1024} KB)")

with col_right:
    st.markdown(
        '<div class="section-title"><span class="step-badge">2</span> Job Description</div>',
        unsafe_allow_html=True,
    )

    jd_input_mode = st.radio(
        "Input method",
        ["Paste JD Text", "Paste Job URL"],
        horizontal=True,
        label_visibility="collapsed",
    )

    jd_text_final = ""

    if jd_input_mode == "Paste JD Text":
        jd_text_final = st.text_area(
            "Job Description",
            height=200,
            placeholder="Paste the full job description here...",
            label_visibility="collapsed",
        )
    else:
        job_url = st.text_input(
            "Job URL",
            placeholder="https://careers.example.com/job/12345",
            label_visibility="collapsed",
        )
        if job_url:
            with st.spinner("Fetching job description from URL..."):
                scrape_result = scrape_job_description(job_url)
            st.info(scrape_result["message"])
            if scrape_result["success"]:
                jd_text_final = scrape_result["text"]
                with st.expander("Preview fetched JD text"):
                    st.text(jd_text_final[:800] + "...")
            else:
                jd_text_final = st.text_area(
                    "Paste JD manually instead:",
                    height=150,
                    label_visibility="collapsed",
                )

st.markdown("---")

# ── Analyze Button ────────────────────────────────────────────────────────────

_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    analyze_clicked = st.button("⚡ Analyze My Resume", use_container_width=True)

# ── Run Analysis ──────────────────────────────────────────────────────────────

if analyze_clicked:

    # Validation
    if not uploaded_file:
        st.error("⚠️ Please upload your resume (PDF or TXT).")
        st.stop()
    if not jd_text_final or len(jd_text_final.strip()) < 50:
        st.error("⚠️ Please provide a job description (at least 50 characters).")
        st.stop()

    # Extract resume text
    try:
        resume_text = parse_resume(uploaded_file)
    except Exception as e:
        st.error(f"❌ Failed to read resume: {e}")
        st.stop()

    if len(resume_text.strip()) < 100:
        st.error("❌ Could not extract enough text from your resume. Try a text-based PDF or TXT file.")
        st.stop()

    # Run AI analysis
    with st.spinner("🤖 AI is analyzing your resume... (this takes ~15-20 seconds)"):
        progress_bar = st.progress(0, text="Running match scorer...")
        time.sleep(0.5)
        progress_bar.progress(20, text="Scoring match...")

        try:
            results = run_full_analysis(resume_text, jd_text_final)
        except ValueError as e:
            st.error(f"🔑 API Key Error: {e}")
            st.info("Add your OpenAI key to the `.env` file: `OPENAI_API_KEY=sk-...`")
            st.stop()
        except Exception as e:
            st.error(f"❌ Analysis failed: {e}")
            st.stop()

        progress_bar.progress(100, text="Done!")
        time.sleep(0.3)
        progress_bar.empty()

    # Show any partial errors
    if results.get("errors"):
        for err in results["errors"]:
            st.warning(f"⚠️ {err}")

    st.markdown("---")

    # ── Results ───────────────────────────────────────────────────────────────

    score_data = results.get("score_data", {})
    gaps       = results.get("gaps", [])
    bullets    = results.get("rewritten_bullets", "")

    score      = score_data.get("score", 0)
    reason     = score_data.get("reason", "")
    strengths  = score_data.get("strengths", [])
    weaknesses = score_data.get("weaknesses", [])

    # Score CSS modifier class (no inline colour)
    if score >= 75:
        score_class = "score-high"
        score_label = "Strong Match 🟢"
    elif score >= 50:
        score_class = "score-medium"
        score_label = "Partial Match 🟡"
    else:
        score_class = "score-low"
        score_label = "Weak Match 🔴"

    # ── Row 1: Score + Quick Verdict ──────────────────────────────────────────

    r1_col1, r1_col2 = st.columns([1, 2], gap="large")

    with r1_col1:
        st.markdown(f"""
        <div class="glass-card score-ring-wrap {score_class}">
            <div class="score-number">{score}%</div>
            <div class="score-label">{score_label}</div>
            <div class="score-reason">"{reason}"</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(score / 100)

    with r1_col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">✅ What\'s Working</div>', unsafe_allow_html=True)
        if strengths:
            pills_html = "".join(f'<span class="pill-green">✓ {s}</span>' for s in strengths)
            st.markdown(pills_html, unsafe_allow_html=True)
        else:
            st.markdown('<span class="score-reason">No strong matches found.</span>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">❌ Key Weaknesses</div>', unsafe_allow_html=True)
        if weaknesses:
            pills_html = "".join(f'<span class="pill-red">✗ {w}</span>' for w in weaknesses)
            st.markdown(pills_html, unsafe_allow_html=True)
        else:
            st.markdown('<span class="score-reason">No major weaknesses detected.</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Row 2: Missing Keywords Table ─────────────────────────────────────────

    st.markdown('<div class="section-title">🔍 Missing Keywords &amp; Skills</div>', unsafe_allow_html=True)

    if gaps:
        badge_map = {"High": "badge-high", "Medium": "badge-medium", "Low": "badge-low"}

        table_rows = ""
        for g in gaps:
            badge_class = badge_map.get(g.get("importance", "Medium"), "badge-medium")
            table_rows += f"""
            <tr>
                <td class="kw-td">{g.get('keyword', '')}</td>
                <td class="kw-td-badge"><span class="{badge_class}">{g.get('importance', '')}</span></td>
                <td class="kw-td-ctx">{g.get('context', '')}</td>
            </tr>"""

        st.markdown(f"""
        <div class="glass-card no-pad">
            <table class="kw-table">
                <thead>
                    <tr>
                        <th class="kw-th">Keyword</th>
                        <th class="kw-th">Priority</th>
                        <th class="kw-th">Why It Matters</th>
                    </tr>
                </thead>
                <tbody>{table_rows}</tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No significant gaps found — great match! 🎉")

    st.markdown("---")

    # ── Row 3: Rewritten Bullets ──────────────────────────────────────────────

    st.markdown('<div class="section-title">✍️ AI-Rewritten Experience Bullets</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="glass-card bullets-box">{bullets.replace(chr(10), "<br>")}</div>',
        unsafe_allow_html=True,
    )

    st.download_button(
        label="📋 Download Rewritten Bullets",
        data=bullets,
        file_name="rewritten_bullets.txt",
        mime="text/plain",
    )

    st.markdown("---")
    st.markdown(
        '<p class="st-footer">SmartTailor — Powered by <span>GPT-4o-mini</span> &amp; <span>LangChain</span> 🤖</p>',
        unsafe_allow_html=True,
    )
