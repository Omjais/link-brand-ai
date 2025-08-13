import json, streamlit as st
from utils import storage
from utils.ai import infer_voice

st.header("🔑 Profile & Voice")
profile_text = st.text_area("Paste your LinkedIn profile text (headline, About, roles)...", height=220)

if st.button("Analyze Voice & Pillars", type="primary"):
    with st.spinner("Analyzing..."):
        voice = infer_voice(profile_text)
        pid = storage.add_profile(profile_text, {"voice": voice.voice, "pillars": voice.pillars, "pitch": voice.pitch})
    st.success("Profile analyzed and saved.")
    st.json({"voice": voice.voice, "pillars": voice.pillars, "pitch": voice.pitch})

st.subheader("Saved Profiles")
df = storage.read("profiles")
st.dataframe(df, use_container_width=True)
