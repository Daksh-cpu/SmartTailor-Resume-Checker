# 🎯 SmartTailor — AI Resume × Job Description Matcher

🚀 SmartTailor is an AI-powered web app built with Python and Streamlit. It uses LangChain and Groq's open-source Llama 3 API to analyze your resume against any job description, scoring your fit and rewriting your experience bullets to pass the ATS.

---

## 🌟 Features

- **Upload & Parse:** Upload PDF or TXT resumes, or paste plain text.
- **Job Description Scraper:** Paste a job URL and let the app extract the description automatically (supports fallbacks).
- **Match Scorer:** Get a realistic 0–100% match score with a quick reasoning summary.
- **Gap Finder:** Identifies the top missing technical skills and keywords from your resume.
- **AI Bullet Rewriter:** Transforms generic experience points into STAR-formatted, ATS-optimized achievements tailored to the JD.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit (Custom Glassmorphism UI)
- **AI/LLM Engine:** LangChain + Groq (Llama-3.1-8b-instant)
- **Document Parsing:** PyPDF2
- **Web Scraping:** BeautifulSoup4, Requests

---

## 🚀 Live Demo

**[Click here to view the live app on Streamlit Cloud](https://smarttailor-resume-checker-ob3vrdy4eqyf2ukjye43nc.streamlit.app/)**

---

## 💻 Local Setup

Want to run it locally? Follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/Daksh-cpu/SmartTailor-Resume-Checker.git
cd SmartTailor-Resume-Checker
```

### 2. Install dependencies

Make sure you have Python 3.9+ installed.

```bash
pip install -r requirements.txt
```

### 3. Set up your API Key

This app uses the free Groq API. Get a key at [console.groq.com](https://console.groq.com/).

Create a `.env` file in the root directory and add:

```env
GROQ_API_KEY="gsk_your_api_key_here"
```

### 4. Run the app

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`.

---

## 📜 Project Structure

```
SmartTailor-Resume-Checker/
├── app.py                  # Main Streamlit UI
├── ai_analyzer.py          # LangChain logic & prompts
├── resume_parser.py        # PDF/TXT extraction utility
├── jd_scraper.py           # Job URL scraping tool
├── requirements.txt        # Python dependencies
├── .env                    # API keys (not tracked in git)
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation
```

---

## 🤝 Contributing

Feel free to open issues or submit pull requests. If you're blocked from scraping certain job boards (like LinkedIn or Indeed), pasting the plain text directly into the app will always work.
