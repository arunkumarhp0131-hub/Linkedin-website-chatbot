import os
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import OpenAI

load_dotenv()

app = FastAPI(title="LinkedIn + Website Sales Copilot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    content: str = Field(..., min_length=10, description="Raw lead/profile/website content")
    source_type: Literal["linkedin", "website", "mixed"] = "mixed"
    tone: Literal["professional", "friendly", "bold"] = "professional"


class AnalyzeResponse(BaseModel):
    result: str


def build_prompt(content: str, source_type: str, tone: str) -> str:
    return f"""
You are an elite B2B sales intelligence assistant.

Input source: {source_type}
Preferred tone: {tone}

Analyze the user-provided data and respond in clean markdown with these exact sections:

## Lead Summary
- Name
- Role
- Company
- Industry
- Buying Signals

## Company Insights
- One paragraph summary of what the company likely does.
- 3 concrete observations from input (no hallucination).

## Potential Needs
- List 3-5 practical technology/business needs this lead/company may have.

## Personalized LinkedIn Message
- Write a concise first-connect message tailored to this lead.

## Follow-up Message
- Write one short follow-up message for 2-4 days later.

## Meeting Prep
- 5 questions the sales rep should ask in discovery.

Rules:
- If some data is missing, state assumptions clearly.
- Keep it actionable and business-focused.
- Avoid generic fluff.

DATA:
{content}
""".strip()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured")

    client = OpenAI(api_key=api_key)

    try:
        completion = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {
                    "role": "system",
                    "content": "You generate practical sales intelligence outputs for outreach teams.",
                },
                {
                    "role": "user",
                    "content": build_prompt(payload.content, payload.source_type, payload.tone),
                },
            ],
            temperature=0.4,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"OpenAI request failed: {exc}") from exc

    content = completion.choices[0].message.content
    if not content:
        raise HTTPException(status_code=500, detail="Empty response from model")

    return AnalyzeResponse(result=content)
