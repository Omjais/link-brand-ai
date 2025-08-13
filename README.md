# Influence OS — Streamlit MVP (No‑Experience Friendly)

A simplified, demo‑ready **LinkedIn Personal Branding AI Agent** built with **Streamlit**.  
It **analyzes a profile**, **generates ideas & posts**, **schedules** them, and **simulates posting + analytics** — no complex OAuth or LinkedIn API required. Perfect for the assignment demo.

## Quick Start (Local)
1) Install Python 3.11
2) `pip install -r requirements.txt`
3) Set your OpenAI key (optional but recommended):
   - mac/linux: `export OPENAI_API_KEY=sk-...`
   - windows (powershell): `$env:OPENAI_API_KEY="sk-..."`
4) Run: `streamlit run app.py`

> No key? The app will run in **offline mode** and produce placeholder content for demo.

## Deploy (Streamlit Cloud)
- Push this folder to a **public GitHub repo**.
- On Streamlit Cloud, select the repo → `app.py` as the entrypoint → add `OPENAI_API_KEY` in Secrets (optional).
- Click **Deploy**.

## What’s Inside
- **Pages**: Profile & Voice, Ideas, Scheduler, Analytics
- **AI**: OpenAI (or fallback offline generation)
- **Storage**: CSV files in `data/`
- **Scheduler**: checks due posts and marks them **posted**
- **Analytics**: simulated impressions/likes/comments
- **Safety**: lightweight content checks

## Notes
- This MVP **simulates** LinkedIn posting to keep setup trivial and focus on AI + automation.
- The code is clean, commented, and easy to extend to a real FastAPI/LinkedIn API later.
