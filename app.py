import streamlit as st
import requests
from bs4 import BeautifulSoup
import os

# ---------------------------
# CONFIG (WORKS EVERYWHERE)
# ---------------------------
def get_api_key():
    try:
        return st.secrets["GROK_API_KEY"]  # Streamlit Cloud
    except:
        return os.getenv("GROK_API_KEY")   # Local env

GROK_API_KEY = get_api_key()

# 👉 TEMP fallback (for testing only)
if not GROK_API_KEY:
    GROK_API_KEY = "xai-9jYZNeVaafUGsGxdYDg1boTPbBc6c92SWPZEojbu44WS9EzMTKm5yqMvdJQr9pYLUAZUuEleml1BJhah"

GROK_API_URL = "https://api.x.ai/v1/chat/completions"
MODEL = "grok-4-1-fast"

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="AI CRO + SEO Auditor", layout="wide")

st.title("🚀 AI CRO + SEO Growth Auditor")
st.markdown("Analyze landing pages for SEO, messaging, and conversion improvements.")

st.markdown("---")

# ---------------------------
# INPUT UI
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    url = st.text_input("🌐 Website URL", placeholder="https://example.com")

with col2:
    keyword = st.text_input("🔍 Target Keyword", placeholder="hotel renovation services")

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

        return f"""
TITLE: {title}
META: {meta_desc}
HEADINGS: {headings[:1000]}
CONTENT: {paragraphs[:3000]}
"""
    except Exception as e:
        return f"Error: {e}"

# ---------------------------
# GROK CALL
# ---------------------------
def analyze_with_grok(content, keyword):

    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are an elite SEO + CRO strategist.

Analyze this page and return clearly separated sections:

HEADLINE IMPROVEMENT:
CTA IMPROVEMENTS:
SEO ISSUES:
CRO ISSUES:
MISSING SECTIONS:
FUNNEL GAPS:
QUICK WINS:

Target Keyword: {keyword}

Website Data:
{content}
"""

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        res = requests.post(GROK_API_URL, headers=headers, json=payload)

        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"]
        else:
            return f"API Error:\n{res.text}"

    except Exception as e:
        return f"Request Failed: {e}"

# ---------------------------
# SECTION PARSER
# ---------------------------
def parse_section(text, section):
    try:
        part = text.split(section)[1]
        return part.split("\n\n")[0]
    except:
        return "Not found"

# ---------------------------
# MAIN
# ---------------------------
if analyze:

    if not url or not keyword:
        st.warning("⚠️ Enter URL and keyword")
    else:
        with st.spinner("🔍 Scraping..."):
            content = scrape_website(url)

        with st.spinner("🧠 Analyzing..."):
            result = analyze_with_grok(content, keyword)

        st.markdown("---")

        tab1, tab2 = st.tabs(["📊 Report", "🧾 Raw"])

        # ---------------------------
        # REPORT UI
        # ---------------------------
        with tab1:
            st.subheader("✨ Headline Improvement")
            st.success(parse_section(result, "HEADLINE IMPROVEMENT"))

            st.subheader("🔥 CTA Improvements")
            st.info(parse_section(result, "CTA IMPROVEMENTS"))

            st.subheader("📈 SEO Issues")
            st.warning(parse_section(result, "SEO ISSUES"))

            st.subheader("⚡ CRO Issues")
            st.warning(parse_section(result, "CRO ISSUES"))

            st.subheader("❌ Missing Sections")
            st.error(parse_section(result, "MISSING SECTIONS"))

            st.subheader("🧠 Funnel Gaps")
            st.info(parse_section(result, "FUNNEL GAPS"))

            st.subheader("🚀 Quick Wins")
            st.success(parse_section(result, "QUICK WINS"))

        # ---------------------------
        # RAW OUTPUT
        # ---------------------------
        with tab2:
            st.write(result)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.markdown("👨‍💻 Developed by 👉 https://www.linkedin.com/in/vikasgoyaleng/")
