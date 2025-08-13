# Deployment Guide

## Option A — Streamlit Cloud (Recommended)
1. Create a **public GitHub repo** and push this folder.
2. Go to Streamlit Cloud → **New app** → connect your repo.
3. App file: `app.py`
4. (Optional) Add **Secrets**: `OPENAI_API_KEY: sk-...`
5. Click **Deploy**.

## Option B — Local
```
python -m venv .venv
source .venv/bin/activate   # windows: .venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...  # optional
streamlit run app.py
```

## Data & Logs
- CSV files stored in `data/` (created automatically on first run).
- If you redeploy, copy `data/` to retain history.
