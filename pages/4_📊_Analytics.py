import streamlit as st, altair as alt, pandas as pd
from utils import storage
from utils.scheduler import run_due_jobs

st.header("📊 Analytics")
if st.button("Refresh & Run Scheduler"):
    count = run_due_jobs()
    st.success(f"Scheduler posted {count} job(s).")

analytics = storage.read("analytics")
posts = storage.read("posts")
if analytics.empty:
    st.info("No analytics yet — schedule and run the scheduler.")
else:
    df = analytics.copy()
    df["collected_at"] = pd.to_datetime(df["collected_at"])
    st.dataframe(df.sort_values("collected_at", ascending=False), use_container_width=True)

    chart = alt.Chart(df).mark_line(point=True).encode(
        x="collected_at:T",
        y="impressions:Q",
        tooltip=["post_id","impressions","reactions","comments","collected_at"]
    )
    st.altair_chart(chart, use_container_width=True)
