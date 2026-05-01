"""
ai_analyzer.py
Runs three LangChain + GPT-4o-mini chains:
  1. Match Scorer   → 0-100% score + reason
  2. Gap Finder     → Missing keywords/skills table
  3. Rewriter       → Improved experience bullet points
"""

import json
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# ── Model setup ──────────────────────────────────────────────────────────────

def get_llm():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("sk-your"):
        raise ValueError("Missing OpenAI API key. Please set it in your .env file.")
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,
        openai_api_key=api_key,
    )


# ── Prompt Templates ─────────────────────────────────────────────────────────

SCORER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an expert ATS (Applicant Tracking System) and senior hiring manager with 15+ years of experience. "
        "Your job is to objectively score how well a resume matches a job description. "
        "Be critical and realistic — most resumes score between 30-75%."
    )),
    ("human", (
        "Compare the resume and job description below.\n\n"
        "Score the match on a scale of 0 to 100 based on:\n"
        "- Matching technical skills and tools\n"
        "- Relevant experience and domain knowledge\n"
        "- Education and certifications\n"
        "- Soft skills and keywords alignment\n\n"
        "Return ONLY a valid JSON object, nothing else:\n"
        "{{\"score\": <integer 0-100>, \"reason\": \"<one sentence explanation>\", "
        "\"strengths\": [\"<strength 1>\", \"<strength 2>\", \"<strength 3>\"], "
        "\"weaknesses\": [\"<weakness 1>\", \"<weakness 2>\"]}}\n\n"
        "RESUME:\n{resume_text}\n\n"
        "JOB DESCRIPTION:\n{jd_text}"
    )),
])

GAP_FINDER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an expert technical recruiter who specializes in identifying skill gaps "
        "between candidates and job requirements. Be specific and actionable."
    )),
    ("human", (
        "Analyze the resume and job description. Identify the TOP 8 missing technical keywords, "
        "tools, or skills that appear in the JD but are absent or weak in the resume.\n\n"
        "Return ONLY a valid JSON array, nothing else:\n"
        "[{{\"keyword\": \"<skill/tool>\", \"importance\": \"High|Medium|Low\", "
        "\"context\": \"<why this matters for the role in 1 sentence>\"}}]\n\n"
        "RESUME:\n{resume_text}\n\n"
        "JOB DESCRIPTION:\n{jd_text}"
    )),
])

REWRITER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an elite professional resume writer and career coach. "
        "You specialize in transforming generic resume bullets into powerful, "
        "ATS-optimized, metrics-driven achievement statements."
    )),
    ("human", (
        "Rewrite 4-5 experience bullet points from the resume to better align with "
        "the job description's tone, keywords, and requirements.\n\n"
        "Rules:\n"
        "- Start each bullet with a strong action verb\n"
        "- Include quantifiable metrics where possible (%, $, time saved, team size)\n"
        "- Naturally weave in JD keywords without keyword-stuffing\n"
        "- Use the STAR format implicitly (what you did + result)\n"
        "- Keep each bullet under 2 lines\n\n"
        "Return the bullets as a markdown list (each starting with '• ').\n"
        "Also add a short note at the end under '**💡 Pro Tip:**' explaining the key change strategy.\n\n"
        "RESUME:\n{resume_text}\n\n"
        "JOB DESCRIPTION:\n{jd_text}"
    )),
])


# ── Chain runners ─────────────────────────────────────────────────────────────

def run_scorer(resume_text: str, jd_text: str) -> dict:
    """Returns score dict: {score, reason, strengths, weaknesses}"""
    llm = get_llm()
    chain = SCORER_PROMPT | llm
    result = chain.invoke({"resume_text": resume_text[:6000], "jd_text": jd_text[:4000]})
    raw = result.content.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def run_gap_finder(resume_text: str, jd_text: str) -> list:
    """Returns list of gap dicts: [{keyword, importance, context}]"""
    llm = get_llm()
    chain = GAP_FINDER_PROMPT | llm
    result = chain.invoke({"resume_text": resume_text[:6000], "jd_text": jd_text[:4000]})
    raw = result.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def run_rewriter(resume_text: str, jd_text: str) -> str:
    """Returns rewritten bullets as a markdown string."""
    llm = get_llm()
    chain = REWRITER_PROMPT | llm
    result = chain.invoke({"resume_text": resume_text[:6000], "jd_text": jd_text[:4000]})
    return result.content.strip()


def run_full_analysis(resume_text: str, jd_text: str) -> dict:
    """
    Runs all three chains and returns a combined results dict.
    Raises on any failure with a descriptive error message.
    """
    errors = []
    results = {}

    try:
        results["score_data"] = run_scorer(resume_text, jd_text)
    except Exception as e:
        errors.append(f"Scorer failed: {e}")
        results["score_data"] = {"score": 0, "reason": "Analysis failed.", "strengths": [], "weaknesses": []}

    try:
        results["gaps"] = run_gap_finder(resume_text, jd_text)
    except Exception as e:
        errors.append(f"Gap Finder failed: {e}")
        results["gaps"] = []

    try:
        results["rewritten_bullets"] = run_rewriter(resume_text, jd_text)
    except Exception as e:
        errors.append(f"Rewriter failed: {e}")
        results["rewritten_bullets"] = "Rewriter could not complete. Please try again."

    results["errors"] = errors
    return results
