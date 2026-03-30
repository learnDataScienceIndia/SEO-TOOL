import streamlit as st
import requests
from bs4 import BeautifulSoup

# ---------------------------
# CONFIG
# ---------------------------
GROK_API_KEY = "xai-9jYZNeVaafUGsGxdYDg1boTPbBc6c92SWPZEojbu44WS9EzMTKm5yqMvdJQr9pYLUAZUuEleml1BJhah"
GROK_API_URL = "https://api.x.ai/v1/chat/completions"

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
url = st.text_input("Enter Website URL")
keyword = st.text_input("Target Keyword")

analyze = st.button("Analyze")

# ---------------------------
# SCRAPE WEBSITE
# ---------------------------
def scrape_website(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.title.string if soup.title else ""
        meta_desc = ""

        meta = soup.find("meta", attrs={"name": "description"})
        if meta:
            meta_desc = meta.get("content", "")

        text = " ".join([p.get_text() for p in soup.find_all("p")])

        return f"""
        TITLE: {title}
        META DESCRIPTION: {meta_desc}
        CONTENT: {text[:3000]}
        """
    except Exception as e:
        return f"Error scraping site: {e}"

# ---------------------------
# GROK API CALL
# ---------------------------
def analyze_with_grok(content, keyword):
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    You are an elite SEO + CRO expert.

    Analyze this landing page for:
    1. Messaging clarity
    2. Conversion rate optimization issues
    3. SEO gaps
    4. Funnel gaps

    Provide:
    - Improved headline
    - Better CTA suggestions
    - SEO recommendations
    - Conversion improvements
    - Missing sections

    Target Keyword: {keyword}

    Website Content:
    {content}
    """

    payload = {
        "model": "grok-1",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(GROK_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.text}"

# ---------------------------
# MAIN LOGIC
# ---------------------------
if analyze:
    if not url or not keyword:
        st.warning("Please enter both URL and keyword.")
    else:
        with st.spinner("Scraping website..."):
            content = scrape_website(url)

        with st.spinner("Analyzing with AI..."):
            result = analyze_with_grok(content, keyword)

        st.markdown("---")
        st.subheader("📊 Analysis Result")
        st.write(result)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.markdown(
    "Developed by 👉 https://www.linkedin.com/in/vikasgoyaleng/"
)
