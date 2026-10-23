import streamlit as st

from study_buddy import ask_buddy, buddy_available

st.set_page_config(page_title="AI Study Buddy", page_icon="🤖", layout="centered")

st.title("🤖 AI Study Buddy")
st.caption("Ask about any AZ-900 concept and get a simple explanation.")

if not buddy_available():
    st.warning("Add ANTHROPIC_API_KEY to your .env file, restart the app, and this page will come alive.")
    st.stop()

if "chat" not in st.session_state:
    st.session_state.chat = []

# Quick-start topic buttons
st.write("**Try a topic:**")
topics = [
    "IaaS vs PaaS vs SaaS",
    "Availability Zones",
    "Azure Policy vs RBAC",
    "Shared responsibility model",
    "CapEx vs OpEx",
]
cols = st.columns(len(topics))
picked = None
for col, topic in zip(cols, topics):
    if col.button(topic, use_container_width=True):
        picked = f"Explain {topic} simply."

if st.sidebar.button("🧹 Clear chat", use_container_width=True):
    st.session_state.chat = []
    st.rerun()

# Replay history
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask about an Azure concept...") or picked
if prompt:
    st.session_state.chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                # Send only the last 10 messages to keep requests small
                reply = ask_buddy(st.session_state.chat[-10:])
        except Exception as e:
            reply = f"Sorry, I could not reach the AI service: {e}"
        st.markdown(reply)
    st.session_state.chat.append({"role": "assistant", "content": reply})