"""
app.py
SmartTailor — AI Resume × Job Description Matcher
Run with: streamlit run app.py
"""

import streamlit as st
import time
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

# ── Custom CSS ────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main background */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* Hide Streamlit default header */
#MainMenu, footer, header { visibility: hidden; }

/* Hero section */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1rem;
}
.hero h1 {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.4rem;
}
.hero p {
    color: #94a3b8;
    font-size: 1.1rem;
    max-width: 600px;
    margin: 0 auto;
}

/* Glass cards */
.glass-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.5rem;
    backdrop-filter: blur(10px);
    margin-bottom: 1.2rem;
}

/* Score ring */
.score-ring-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1.5rem 0;
}
.score-number {
    font-size: 5rem;
    font-weight: 800;
    line-height: 1;
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.score-label {
    font-size: 0.95rem;
    color: #94a3b8;
    margin-top: 0.3rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.score-reason {
    color: #cbd5e1;
    font-size: 0.95rem;
    text-align: center;
    margin-top: 1rem;
    font-style: italic;
    max-width: 400px;
}

/* Importance badges */
.badge-high   { background:#ef444420; color:#f87171; border:1px solid #f8717140; padding:2px 10px; border-radius:20px; font-size:0.78rem; font-weight:600; }
.badge-medium { background:#f59e0b20; color:#fbbf24; border:1px solid #fbbf2440; padding:2px 10px; border-radius:20px; font-size:0.78rem; font-weight:600; }
.badge-low    { background:#10b98120; color:#34d399; border:1px solid #34d39940; padding:2px 10px; border-radius:20px; font-size:0.78rem; font-weight:600; }

/* Section headers */
.section-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Strength/weakness pills */
.pill-green { background:#10b98118; color:#34d399; border:1px solid #34d39930; border-radius:8px; padding:6px 12px; margin:4px; display:inline-block; font-size:0.88rem; }
.pill-red   { background:#ef444418; color:#f87171; border:1px solid #f8717130; border-radius:8px; padding:6px 12px; margin:4px; display:inline-block; font-size:0.88rem; }

/* Analyze button */
div.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 2.5rem;
    font-size: 1.05rem;
    font-weight: 700;
    width: 100%;
    cursor: pointer;
    transition: all 0.3s ease;
    letter-spacing: 0.03em;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #6d28d9, #1d4ed8);
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(124,58,237,0.4);
}

/* Rewritten bullets box */
.bullets-box {
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    color: #e2e8f0;
    line-height: 1.85;
    font-size: 0.96rem;
}

/* Input labels */
label { color: #cbd5e1 !important; font-weight: 500 !important; }
.stTextArea textarea, .stTextInput input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
}
.stFileUploader {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 12px !important;
}

/* Progress bar color */
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #7c3aed, #2563eb) !important;
}

/* Divider */
hr { border-color: rgba(255,255,255,0.08) !important; }

/* Step badges */
.step-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px; height: 28px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    color: white;
    font-weight: 700;
    font-size: 0.85rem;
    margin-right: 8px;
    flex-shrink: 0;
}
</style>
""", unsafe_allow_html=True)

# ── Hero Header ───────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero">
    <h1>🎯 SmartTailor</h1>
    <p>AI-powered resume × job description matcher. Score your fit, find the gaps, and rewrite your bullets — in seconds.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Input Section ─────────────────────────────────────────────────────────────

col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.markdown('<div class="section-title"><span class="step-badge">1</span> Upload Your Resume</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drag & drop or browse",
        type=["pdf", "txt"],
        label_visibility="collapsed",
        key="resume_upload",
    )
    if uploaded_file:
        st.success(f"✅ **{uploaded_file.name}** loaded ({uploaded_file.size // 1024} KB)")

with col_right:
    st.markdown('<div class="section-title"><span class="step-badge">2</span> Job Description</div>', unsafe_allow_html=True)

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
                # Show manual fallback text area
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

    # ── Results ──────────────────────────────────────────────────────────────

    score_data   = results.get("score_data", {})
    gaps         = results.get("gaps", [])
    bullets      = results.get("rewritten_bullets", "")

    score = score_data.get("score", 0)
    reason = score_data.get("reason", "")
    strengths = score_data.get("strengths", [])
    weaknesses = score_data.get("weaknesses", [])

    # Score color thresholds
    if score >= 75:
        score_color = "#34d399"
        score_label = "Strong Match 🟢"
    elif score >= 50:
        score_color = "#fbbf24"
        score_label = "Partial Match 🟡"
    else:
        score_color = "#f87171"
        score_label = "Weak Match 🔴"

    # ── Row 1: Score + Quick Verdict ─────────────────────────────────────────

    r1_col1, r1_col2 = st.columns([1, 2], gap="large")

    with r1_col1:
        st.markdown(f"""
        <div class="glass-card score-ring-wrap">
            <div class="score-number" style="color:{score_color};">{score}%</div>
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
            st.markdown('<span style="color:#94a3b8;">No strong matches found.</span>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">❌ Key Weaknesses</div>', unsafe_allow_html=True)
        if weaknesses:
            pills_html = "".join(f'<span class="pill-red">✗ {w}</span>' for w in weaknesses)
            st.markdown(pills_html, unsafe_allow_html=True)
        else:
            st.markdown('<span style="color:#94a3b8;">No major weaknesses detected.</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Row 2: Missing Keywords Table ────────────────────────────────────────

    st.markdown('<div class="section-title">🔍 Missing Keywords & Skills</div>', unsafe_allow_html=True)

    if gaps:
        badge_map = {"High": "badge-high", "Medium": "badge-medium", "Low": "badge-low"}

        # Build table rows
        table_rows = ""
        for g in gaps:
            badge_class = badge_map.get(g.get("importance", "Medium"), "badge-medium")
            table_rows += f"""
            <tr>
                <td style="padding:10px 14px; color:#e2e8f0; font-weight:600;">{g.get('keyword','')}</td>
                <td style="padding:10px 14px;"><span class="{badge_class}">{g.get('importance','')}</span></td>
                <td style="padding:10px 14px; color:#94a3b8; font-size:0.9rem;">{g.get('context','')}</td>
            </tr>"""

        st.markdown(f"""
        <div class="glass-card" style="padding:0; overflow:hidden;">
            <table style="width:100%; border-collapse:collapse;">
                <thead>
                    <tr style="background:rgba(255,255,255,0.05);">
                        <th style="padding:12px 14px; color:#a78bfa; text-align:left; font-size:0.85rem; letter-spacing:0.08em; text-transform:uppercase;">Keyword</th>
                        <th style="padding:12px 14px; color:#a78bfa; text-align:left; font-size:0.85rem; letter-spacing:0.08em; text-transform:uppercase;">Priority</th>
                        <th style="padding:12px 14px; color:#a78bfa; text-align:left; font-size:0.85rem; letter-spacing:0.08em; text-transform:uppercase;">Why It Matters</th>
                    </tr>
                </thead>
                <tbody>{table_rows}</tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No significant gaps found — great match! 🎉")

    st.markdown("---")

    # ── Row 3: Rewritten Bullets ─────────────────────────────────────────────

    st.markdown('<div class="section-title">✍️ AI-Rewritten Experience Bullets</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="glass-card bullets-box">{bullets.replace(chr(10), "<br>")}</div>',
        unsafe_allow_html=True,
    )

    # Copy to clipboard button (download as text)
    st.download_button(
        label="📋 Download Rewritten Bullets",
        data=bullets,
        file_name="rewritten_bullets.txt",
        mime="text/plain",
    )

    st.markdown("---")
    st.markdown(
        '<p style="text-align:center; color:#475569; font-size:0.85rem;">SmartTailor — Powered by GPT-4o-mini & LangChain 🤖</p>',
        unsafe_allow_html=True,
    )
