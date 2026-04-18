import sys
import os

# 🔥 FIX IMPORT PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from backend.retrieval.qa_system import generate_answer

st.set_page_config(page_title="Campus Chatbot", layout="wide")

st.title("🎓 Campus Knowledge Chatbot")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
user_input = st.chat_input("Ask your question...")

if user_input:
    # User message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_answer(user_input)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})