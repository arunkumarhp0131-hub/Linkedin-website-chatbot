import os

import httpx
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(
    page_title="LeadMind AI Copilot",
    page_icon="🤖",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main {padding-top: 1rem;}
    .card {
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 16px;
        background: #FFFFFF;
        box-shadow: 0 4px 14px rgba(0,0,0,0.04);
    }
    .hero {
        background: linear-gradient(120deg, #0A66C2, #6A7BFF);
        color: white;
        padding: 18px 20px;
        border-radius: 16px;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero">
<h2 style="margin:0;">🤖 LeadMind AI Copilot</h2>
<p style="margin:8px 0 0 0;">Analyze LinkedIn profiles or websites and auto-generate outreach + follow-ups.</p>
</div>
""",
    unsafe_allow_html=True,
)

left, right = st.columns([1, 1.2], gap="large")

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Input")
    source_type = st.selectbox("Source", ["linkedin", "website", "mixed"], index=2)
    tone = st.selectbox("Tone", ["professional", "friendly", "bold"], index=0)
    content = st.text_area(
        "Paste LinkedIn profile text, About section, company website content, or notes",
        height=300,
        placeholder="Example: John Doe, CTO at ABC Logistics, company focuses on fleet visibility...",
    )
    analyze = st.button("🚀 Analyze Lead", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("AI Output")
    if "last_output" not in st.session_state:
        st.session_state.last_output = "Run analysis to see lead summary, outreach message, follow-up, and meeting prep."
    st.markdown(st.session_state.last_output)
    st.markdown("</div>", unsafe_allow_html=True)

if analyze:
    if len(content.strip()) < 10:
        st.error("Please paste more details so AI can produce useful insights.")
    else:
        with st.spinner("Thinking like a sales strategist..."):
            try:
                response = httpx.post(
                    f"{API_BASE}/analyze",
                    json={"content": content, "source_type": source_type, "tone": tone},
                    timeout=60,
                )
                response.raise_for_status()
                st.session_state.last_output = response.json()["result"]
                st.rerun()
            except Exception as exc:  # noqa: BLE001
                st.error(f"Could not analyze lead: {exc}")
