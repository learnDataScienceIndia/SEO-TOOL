import streamlit as st
import requests
from bs4 import BeautifulSoup
import os

# ---------------------------
# CONFIG
# ---------------------------
GROK_API_KEY = os.getenv("xai-9jYZNeVaafUGsGxdYDg1boTPbBc6c92SWPZEojbu44WS9EzMTKm5yqMvdJQr9pYLUAZUuEleml1BJhah")
GROK_API_URL = "https://api.x.ai/v1/chat/completions"
MODEL = "grok-4-1-fast"

# ---------------------------
# PAGE SETUP
# ---------------------------
st.set_page_config(page_title="AI CRO + SEO Auditor", layout="wide")

st.title("🚀 AI CRO + SEO Growth Auditor")
st.markdown("Analyze landing pages for SEO, messaging, and conversion improvements.")

st.markdown("---")

# ---------------------------
# INPUTS
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    url = st.text_input("🌐 Website URL")

with col2:
    keyword = st.text_input("🔍 Target Keyword")

analyze = st.button("Analyze")

# ---------------------------
# SCRAPER
# ---------------------------
def scrape_website(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.title.string if soup.title else ""
        meta_desc = ""

        meta = soup.find("meta", attrs={"name": "description"})
        if meta:
            meta_desc = meta.get("content", "")

        headings = " ".join([h.get_text() for h in soup.find_all(["h1", "h2", "h3"])])
        paragraphs = " ".join([p.get_text() for p in soup.find_all("p")])

        content = f"""
        TITLE: {title}
        META DESCRIPTION: {meta_desc}
        HEADINGS: {headings[:1000]}
        CONTENT: {paragraphs[:3000]}
        """

        return content

    except Exception as e:
        return f"Error scraping website: {e}"

# ---------------------------
# GROK ANALYSIS
# ---------------------------
def analyze_with_grok(content, keyword):
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are an elite SEO + CRO strategist.

Analyze the landing page and return output in EXACT sections:

1. HEADLINE IMPROVEMENT
2. CTA IMPROVEMENTS
3. SEO ISSUES
4. CRO ISSUES
5. MISSING SECTIONS
6. FUNNEL GAPS
7. QUICK WINS

Target Keyword: {keyword}

Website Data:
{content}
"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(GROK_API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"❌ API Error:\n{response.text}"

    except Exception as e:
        return f"❌ Request Failed: {e}"

# ---------------------------
# DISPLAY FUNCTION
# ---------------------------
def display_sections(result):
    sections = [
        "HEADLINE IMPROVEMENT",
        "CTA IMPROVEMENTS",
        "SEO ISSUES",
        "CRO ISSUES",
        "MISSING SECTIONS",
        "FUNNEL GAPS",
        "QUICK WINS"
    ]

    for sec in sections:
        if sec in result:
            split_text = result.split(sec)
            if len(split_text) > 1:
                content = split_text[1].split("\n\n")[0]
                st.subheader(f"📌 {sec}")
                st.write(content)

# ---------------------------
# MAIN
# ---------------------------
if analyze:

    if not GROK_API_KEY:
        st.error("❌ Missing GROK_API_KEY. Set environment variable first.")
    elif not url or not keyword:
        st.warning("⚠️ Please enter both URL and keyword.")
    else:
        with st.spinner("🔍 Scraping website..."):
            content = scrape_website(url)

        with st.spinner("🧠 Running AI analysis..."):
            result = analyze_with_grok(content, keyword)

        st.markdown("---")

        tab1, tab2 = st.tabs(["📊 Structured Report", "🧾 Raw Output"])

        with tab1:
            display_sections(result)

        with tab2:
            st.write(result)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.markdown("👨‍💻 Developed by 👉 https://www.linkedin.com/in/vikasgoyaleng/")
