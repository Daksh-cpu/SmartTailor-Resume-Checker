# <div align="center">🎯 SmartTailor</div>

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=chainlink&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq_Cloud-f25022?style=for-the-badge&logo=fastapi&logoColor=white" />
</div>

<br />

<div align="center">
  <img src="smarttailor_banner.png" alt="SmartTailor Banner" width="100%" />
</div>

<div align="center">
  <h3>AI-Powered Resume × Job Description Matcher</h3>
  <p><i>Stop guessing. Start tailoring. Pass the ATS with a high-fidelity AI analyzer.</i></p>
  
  **[🚀 View Live Demo](https://smarttailor-resume-checker-ob3vrdy4eqyf2ukjye43nc.streamlit.app/)**
</div>

---

## 💎 The SmartTailor Advantage

SmartTailor isn't just a checker; it's your personal career strategist. Built with **LangChain** and powered by **Groq's Llama 3 API**, it provides deep semantic analysis that goes far beyond simple keyword matching.

### ✨ Core Capabilities

| Feature | Description |
| :--- | :--- |
| **🔍 Intelligent Scoring** | A realistic 0–100% match score based on semantic alignment, not just word count. |
| **🛠️ Gap Analysis** | Pinpoints exact technical skills and keywords missing from your profile. |
| **✍️ STAR Rewriter** | Automatically transforms generic bullets into high-impact, STAR-formatted achievements. |
| **🌐 URL Scraping** | Direct job posting analysis from URLs (Indeed, LinkedIn, and more). |
| **🎭 Premium UI** | A stunning glassmorphism interface with custom 3D CSS animations. |

---

## 🎨 Design Philosophy: 3D High-Fidelity

We believe that professional tools should be beautiful. SmartTailor features a **custom-built 3D Hero section** using pure CSS.

*   **Rotating 3D Cube:** A symbol of multi-faceted career data.
*   **Halo Orbitals:** Representing the screening layers of the ATS.
*   **Atmospheric Starfield:** A dynamic, performance-optimized background effect that brings the interface to life.

---

## 🛠️ Tech Stack & Architecture

*   **Engine:** [LangChain](https://www.langchain.com/) for complex LLM orchestration.
*   **LLM:** [Groq Llama-3.1-8b](https://groq.com/) for lightning-fast, open-source intelligence.
*   **Interface:** [Streamlit](https://streamlit.io/) with custom CSS injection for the glassmorphism aesthetic.
*   **Processing:** PyPDF2 & BeautifulSoup4 for robust data extraction.

---

## 💻 Local Development

### 1️⃣ Clone & Navigate
```bash
git clone https://github.com/Daksh-cpu/SmartTailor-Resume-Checker.git
cd SmartTailor-Resume-Checker
```

### 2️⃣ Environment Setup
```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3️⃣ Configuration
Create a `.env` file in the root directory:
```env
GROQ_API_KEY="your_groq_api_key_here"
```

### 4️⃣ Launch
```bash
streamlit run app.py
```

---

## 📂 Project Structure

```bash
SmartTailor/
├── app.py              # Main Entry Point (Streamlit UI)
├── ai_analyzer.py      # LangChain & Prompt Engineering
├── resume_parser.py    # PDF/TXT Extraction Logic
├── jd_scraper.py       # Job Board Scraping Utility
├── static/
│   └── style.css       # Custom Glassmorphism & 3D Styles
└── requirements.txt    # Project Dependencies
```

---

## 🤝 Contributing & Support

We welcome contributions! Whether it's adding new scraping fallbacks or enhancing the UI, feel free to fork and PR.

**Note:** If certain job boards block automated scraping, the "Manual Paste" feature ensures you can always analyze any role instantly.

---

<div align="center">
  <p>Built with ❤️ by <a href="https://github.com/Daksh-cpu">Daksh</a></p>
  <img src="https://view-counter.api.fnkr.net/v1/counter/github/Daksh-cpu/SmartTailor-Resume-Checker" alt="Views" />
</div>
