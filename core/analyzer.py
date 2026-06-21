import re
import requests
import json
import os
import streamlit as st

FILLER_WORDS = [    
    "um", "uh", "er", "ah", "hmm",
    "like", "basically", "literally", "actually",
    "so", "well", "right", "okay",
    "you know", "i mean", "you see", "mind you",
    "honestly", "seriously", "totally", "obviously",
    "just", "sort of", "kind of", "anyway", "anyhow",
    "look", "listen", "believe me", "tell you what"
    ]

def get_api_key() -> str:
    """Read Groq API key from Streamlit secrets or environment variable."""
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return os.environ.get("GROQ_API_KEY", "")

def count_filler_words(text: str) -> dict:
    text_lower = text.lower()
    counts = {}
    total = 0
    for word in FILLER_WORDS:
        pattern = r'\b' + re.escape(word) + r'\b'
        count = len(re.findall(pattern, text_lower))
        if count > 0:
            counts[word] = count
            total += count
    return {"breakdown": counts, "total": total}

def calculate_wpm(text: str, duration_seconds: float = 60) -> int:
    words = len(text.split())
    minutes = duration_seconds / 60
    return round(words / minutes) if minutes > 0 else 0

def get_llm_feedback(transcript: str) -> dict:
    api_key = get_api_key()
    if not api_key:
        return {
            "grammar_issues": [],
            "improved_version": transcript,
            "clarity_score": 0,
            "confidence_tips": ["API key not configured. Please add GROQ_API_KEY to Streamlit secrets."]
        }

    prompt = f"""Analyze this spoken English transcript and return ONLY a JSON object with these exact keys:
- "grammar_issues": list of objects with "original" and "correction" and "explanation"
- "improved_version": a rewritten, polished version of the transcript
- "clarity_score": integer from 1 to 10
- "confidence_tips": list of 2-3 short actionable tips

Transcript:
\"\"\"{transcript}\"\"\"

Return only valid JSON, no markdown, no extra text."""

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        data = response.json()
        raw = data["choices"][0]["message"]["content"].strip()
        raw = re.sub(r"```json|```", "", raw).strip()
        return json.loads(raw)
    except Exception as e:
        print(f"LLM feedback error: {e}")
        return {
            "grammar_issues": [],
            "improved_version": transcript,
            "clarity_score": 0,
            "confidence_tips": ["Could not fetch AI feedback. Please try again."]
        }

def analyze_speech(transcript: str, duration_seconds: float = 60) -> dict:
    fillers = count_filler_words(transcript)
    wpm = calculate_wpm(transcript, duration_seconds)
    llm = get_llm_feedback(transcript)

    if wpm < 100:
        pace_feedback = "Too slow — try to speak a bit faster."
    elif wpm > 160:
        pace_feedback = "Too fast — slow down for clarity."
    else:
        pace_feedback = "Good pace — easy to follow."

    return {
        "filler_words": fillers,
        "wpm": wpm,
        "pace_feedback": pace_feedback,
        "grammar_issues": llm.get("grammar_issues", []),
        "improved_version": llm.get("improved_version", ""),
        "clarity_score": llm.get("clarity_score", 0),
        "confidence_tips": llm.get("confidence_tips", [])
    }