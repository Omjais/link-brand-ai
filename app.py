import os, streamlit as st
from utils.scheduler import run_due_jobs

st.set_page_config(page_title="Influence OS — LinkedIn Agent (MVP)", layout="wide")

st.title("Influence OS — LinkedIn Personal Branding Agent (MVP)")
st.caption("Streamlit demo — AI-generated ideas & posts, simple scheduler, simulated posting & analytics.")

with st.sidebar:
    st.header("Admin")
    if st.button("Run Scheduler Now"):
        count = run_due_jobs()
        st.success(f"Scheduler executed. {count} job(s) posted.")
    st.divider()
    st.write("OpenAI Model:", os.getenv("OPENAI_MODEL","gpt-4o-mini"))
    st.write("API Key:", "set" if os.getenv("OPENAI_API_KEY") else "not set (offline mode)")

st.markdown("""
Use the **pages** on the left:
1) Profile & Voice — paste your LinkedIn profile; infer voice/pillars
2) Ideas — generate post ideas
3) Scheduler — compose A/B variants and schedule
4) Analytics — track simulated performance
""")
