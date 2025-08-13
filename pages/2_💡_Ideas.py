import streamlit as st
from utils import storage
from utils.ai import generate_ideas

st.header("💡 Ideas")
profiles = storage.read("profiles")
if profiles.empty:
    st.info("Create a profile first on the previous page.")
else:
    latest = profiles.iloc[-1]
    industry = st.text_input("Your industry", "AI / Software")
    persona = st.text_input("Target persona", "Founders & Engineers")
    if st.button("Generate Ideas", type="primary"):
        ideas = generate_ideas(industry, persona)
        storage.add_ideas(latest["id"], ideas)
        st.success("Ideas generated and saved.")
    st.subheader("Saved Ideas")
    st.dataframe(storage.read("ideas"), use_container_width=True)
