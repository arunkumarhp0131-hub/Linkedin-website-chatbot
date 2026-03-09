# LeadMind AI Copilot (LinkedIn + Website + ChatGPT-style)

A complete hackathon-ready project that combines:
- **FastAPI backend** for AI reasoning
- **Streamlit web app** with polished UI
- **Embeddable website widget**
- **Chrome extension for LinkedIn pages**

## What it does
Paste LinkedIn/website content and get:
1. Lead Summary
2. Company Insights
3. Potential Needs
4. Personalized LinkedIn Message
5. Follow-up Message
6. Meeting Prep Questions

---

## 1) Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set `OPENAI_API_KEY`.

---

## 2) Run backend API

```bash
uvicorn backend.main:app --reload --port 8000
```

Health check:

```bash
curl http://localhost:8000/health
```

---

## 3) Run web app (better UI)

```bash
streamlit run frontend/app.py --server.port 8501
```

Open `http://localhost:8501`.

---

## 4) Embed in any website

Use the widget script:

```html
<script src="/path/to/embed.js"></script>
```

For local demo, open `widget/example.html` in a browser.

---

## 5) LinkedIn integration (Chrome extension)

1. Open `chrome://extensions`
2. Enable **Developer mode**
3. Click **Load unpacked**
4. Select the `extension/` folder
5. Open a LinkedIn profile page and click **Analyze with LeadMind AI**

---

## 6) Demo script (2 minutes)

1. Paste a lead profile in web app
2. Click **Analyze Lead**
3. Show generated outreach + follow-up
4. Open LinkedIn and click extension button
5. Show same AI output pattern

---

## Notes
- LinkedIn does not allow direct third-party widget embedding in its product UI.
- The extension overlay is the recommended approach.
- For production use, add authentication, logging, and rate-limits.
