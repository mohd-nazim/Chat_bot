# app.py

import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

GROQ_API_URL = os.getenv("GROQ_API_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Page settings
st.set_page_config(page_title="Groq CoPilot", page_icon="🤖", layout="wide")

st.markdown(
    """
    <style>
    .message-container {
        padding: 0.8em;
        border-radius: 8px;
        margin-bottom: 1em;
    }
    .user-message {
        background-color: #1e1e1e;
        color: #dcdcdc;
        font-family: Consolas, monospace;
    }
    .bot-message {
        background-color: #2c2c2c;
        color: #9cdcfe;
        font-family: Consolas, monospace;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Show title
st.title("🤖 Groq CoPilot")
st.caption("AI-powered coding assistant")

# Initialize session history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
user_input = st.text_area("Enter your prompt:", height=100, placeholder="Ask about code, debug help, or tech questions...")

# On send
if st.button("🚀 Send"):
    if not GROQ_API_URL or not GROQ_API_KEY:
        st.error("API URL or API Key is missing. Check your .env file.")
    elif user_input.strip() == "":
        st.warning("Please type something.")
    else:
        with st.spinner("Generating response..."):
            try:
                response = requests.post(
                    GROQ_API_URL,
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [{"role": "user", "content": user_input}]
                    }
                )

                if response.status_code == 200:
                    reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response.")
                    st.session_state.chat_history.append(("user", user_input))
                    st.session_state.chat_history.append(("bot", reply))
                else:
                    st.error(f"Error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"API request failed: {str(e)}")

# Show chat history
for role, message in reversed(st.session_state.chat_history):
    css_class = "user-message" if role == "user" else "bot-message"
    st.markdown(f'<div class="message-container {css_class}">{message}</div>', unsafe_allow_html=True)
