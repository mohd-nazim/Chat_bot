import streamlit as st
import requests
import os
from dotenv import load_dotenv
import re

# Load environment
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

API_URL = os.getenv("GROQ_API_URL")
API_KEY = os.getenv("GROQ_API_KEY")

# Page setup
st.set_page_config(page_title="Groq Dev Copilot", layout="wide", page_icon="🧑‍💻")

# CSS styling
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .chat-box {
        padding: 0.8em;
        border-radius: 10px;
        margin-bottom: 1rem;
        font-family: 'Fira Code', monospace;
        white-space: pre-wrap;
    }
    .user { background-color: #1e1e1e; color: #dcdcdc; }
    .bot { background-color: #22272e; color: #9cdcfe; }
    .stTextArea > div > textarea {
        background-color: #1e1e1e;
        color: white;
        font-family: 'Fira Code', monospace;
    }
    </style>
""", unsafe_allow_html=True)

# App title
st.markdown("## 🤖 Groq Dev Copilot")
st.caption("Your AI coding assistant powered by LLaMA 3")

# Sidebar actions
with st.sidebar:
    st.markdown("### ⚙️ Chat Settings")
    if st.button("🧹 Clear Chat"):
        st.session_state.history = []

# Chat history initialization
if "history" not in st.session_state:
    st.session_state.history = []

# Input area
user_prompt = st.text_area("💬 Enter your question:", height=100, placeholder="e.g., How to use FastAPI with MongoDB?")

if st.button("🚀 Send", use_container_width=True) and user_prompt.strip():
    with st.spinner("Generating response..."):
        try:
            response = requests.post(
                API_URL,
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": user_prompt}]
                }
            )

            if response.status_code == 200:
                reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response.")
                st.session_state.history.append(("user", user_prompt))
                st.session_state.history.append(("bot", reply))
            else:
                st.error(f"Error {response.status_code}: {response.text}")

        except Exception as e:
            st.error(f"Request failed: {str(e)}")

# Message renderer with markdown & code support
def render_message(role, msg):
    style = "user" if role == "user" else "bot"
    st.markdown(f'<div class="chat-box {style}">', unsafe_allow_html=True)
    # Syntax highlighting using st.markdown and st.code
    code_blocks = re.findall(r"```(.*?)```", msg, re.DOTALL)
    if code_blocks:
        parts = re.split(r"```.*?```", msg, flags=re.DOTALL)
        for i, part in enumerate(parts):
            st.markdown(part.strip())
            if i < len(code_blocks):
                st.code(code_blocks[i].strip())
    else:
        st.markdown(msg.strip())
    st.markdown('</div>', unsafe_allow_html=True)

# Render chat history
for role, message in st.session_state.history:
    render_message(role, message)
