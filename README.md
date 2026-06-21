# 🎙️ English Buddy

A web app that helps you improve your spoken English. Record yourself speaking and get instant feedback on grammar, pace, filler words, and clarity.

## Features

- 🎤 **Browser Recording** — Record directly from your mic, no installs
- 📝 **Auto Transcription** — Powered by OpenAI Whisper
- 🔁 **Filler Word Detection** — Tracks "um", "uh", "like", "basically" etc.
- ⏱️ **Speaking Pace** — Words per minute with feedback
- ✏️ **Grammar Corrections** — Specific issues with explanations
- ⭐ **Improved Version** — AI-rewritten polished version of your speech
- 💡 **Personalized Tips** — Actionable suggestions to improve

## Tech Stack

- **UI:** Streamlit (Python)
- **Transcription:** OpenAI Whisper (base model)
- **AI Feedback:** Claude API (Anthropic)

## Local Setup

```bash
git clone https://github.com/yourusername/english-buddy.git
cd english-buddy

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Add your API key to `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "your-key-here"
```

Run the app:
```bash
streamlit run app.py
```

## Deploy on Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub → select this repo → set `app.py` as entry point
4. Go to **Settings → Secrets** and add:
   ```
   ANTHROPIC_API_KEY = "your-key-here"
   ```
5. Deploy — your app gets a public URL instantly

## Project Structure

```
english-buddy/
├── app.py                  # Streamlit UI
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── secrets.toml        # Local only, never committed
└── core/
    ├── transcriber.py      # Whisper integration
    └── analyzer.py         # Filler words, WPM, LLM feedback
```

## Roadmap

- [x] Phase 1 — Browser recording, transcription & analysis
- [ ] Phase 2 — Audio file upload support
- [ ] Phase 3 — Session history & progress tracking
- [ ] Phase 4 — User accounts & improvement charts
