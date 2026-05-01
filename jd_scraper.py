"""
jd_scraper.py
Attempts to scrape plain text from a job posting URL.
Falls back gracefully with a helpful message if the site blocks bots.
"""

import requests
from bs4 import BeautifulSoup


# Common sites known to block scrapers
BLOCKED_DOMAINS = ["linkedin.com", "indeed.com", "glassdoor.com", "ziprecruiter.com"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def is_blocked_domain(url: str) -> bool:
    return any(domain in url.lower() for domain in BLOCKED_DOMAINS)


def scrape_job_description(url: str) -> dict:
    """
    Attempts to fetch and extract the main body text from a job posting URL.

    Returns:
        {
            "success": True/False,
            "text": <extracted text or empty string>,
            "message": <status message for display>
        }
    """
    if is_blocked_domain(url):
        return {
            "success": False,
            "text": "",
            "message": (
                f"⚠️ This site ({url.split('/')[2]}) blocks automated scraping. "
                "Please **copy and paste** the job description text manually into the text area below."
            ),
        }

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style tags
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        # Try to find main content containers common in job boards
        content_tags = ["main", "article", "section", '[class*="job"]', '[class*="description"]']
        text = ""

        for selector in content_tags:
            found = soup.select(selector)
            if found:
                text = " ".join(el.get_text(separator=" ", strip=True) for el in found)
                break

        # Fallback: grab all body text
        if not text:
            text = soup.get_text(separator=" ", strip=True)

        # Trim to a reasonable length
        text = " ".join(text.split())[:8000]

        if len(text) < 100:
            return {
                "success": False,
                "text": "",
                "message": "⚠️ Could not extract meaningful text from this URL. Please paste the JD manually.",
            }

        return {
            "success": True,
            "text": text,
            "message": f"✅ Successfully scraped job description ({len(text)} characters).",
        }

    except requests.exceptions.Timeout:
        return {"success": False, "text": "", "message": "⏱️ Request timed out. Please paste the JD manually."}
    except requests.exceptions.RequestException as e:
        return {"success": False, "text": "", "message": f"❌ Failed to fetch URL: {e}"}
