import datetime as dt, streamlit as st, json
from utils import storage
from utils.ai import compose_post
from utils.safety import check

st.header("🗓️ Scheduler & Composer")

profiles = storage.read("profiles")
ideas = storage.read("ideas")
if profiles.empty or ideas.empty:
    st.info("You need at least 1 profile and 1 idea.")
else:
    profile = profiles.iloc[-1]
    idea_titles = ideas["title"].unique().tolist()
    idea = st.selectbox("Pick an idea", idea_titles)
    if st.button("Compose A/B Variants", type="primary"):
        variants = compose_post(idea, {"voice": eval(profile["voice"])})
        st.session_state["variants"] = variants
        st.success("Generated A/B variants.")
    variants = st.session_state.get("variants")
    if variants:
        tabA, tabB = st.tabs(["Variant A", "Variant B"])
        with tabA:
            textA = st.text_area("Text A", variants["A"]["text"], height=260)
            issues = check(textA)
            if issues: st.warning(f"Safety flags: {issues}")
        with tabB:
            textB = st.text_area("Text B", variants["B"]["text"], height=260)
            issues = check(textB)
            if issues: st.warning(f"Safety flags: {issues}")
        choice = st.selectbox("Choose variant to schedule", ["A","B"])
        date = st.date_input("Schedule date (UTC)", dt.datetime.utcnow().date())
        time = st.time_input("Schedule time (UTC)", (dt.datetime.utcnow() + dt.timedelta(minutes=2)).time())
        when = dt.datetime.combine(date, time)

        if st.button("Schedule Post"):
            chosen = textA if choice=="A" else textB
            hashtags = variants[choice].get("hashtags", [])
            post_id = storage.add_post(profile["id"], idea, choice, chosen, hashtags)
            storage.schedule_post(post_id, when.isoformat()+"Z", tz="UTC")
            st.success("Scheduled. Use 'Run Scheduler Now' in the sidebar for demo.")
    st.divider()
    st.subheader("Drafts & Posted")
    st.dataframe(storage.read("posts"), use_container_width=True)
    st.subheader("Schedules")
    st.dataframe(storage.read("schedules"), use_container_width=True)
