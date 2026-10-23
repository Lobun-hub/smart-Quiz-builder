import streamlit as st

from study_buddy import ask_buddy, buddy_available
from theme_manager import apply_theme

st.set_page_config(page_title="AI Study Buddy", page_icon="🤖", layout="centered")
apply_theme()

st.title("🤖 AI Study Buddy")
st.caption("Ask about AZ-900 concepts and get a simple explanation.")

if not buddy_available():
    st.info(
        "Offline study helper: built-in AZ-900 explanations are available "
        "without an API key. Add an Anthropic key to enable generated answers."
    )

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