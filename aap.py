import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Get API values
GROQ_API_URL = os.getenv("GROQ_API_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Page config
st.set_page_config(page_title="Groq CoPilot", page_icon="🤖", layout="wide")

# Custom style
st.markdown("""
    <style>
    .message-container {
        padding: 0.8em;
        border-radius: 8px;
        margin-bottom: 1em;
    }
    .user-message {
        background-color: #1e1e1e;
        color: #ffffff;
        font-family: Consolas, monospace;
    }
    .bot-message {
        background-color: #2c2c2c;
        color: #9cdcfe;
        font-family: Consolas, monospace;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Groq CoPilot")
st.caption("AI-powered coding assistant (LLaMA 3.3 70B)")

# Initialize history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_area("💬 Enter your prompt:", height=100, placeholder="Ask anything related to code, bugs, or tools...")

# On click send
if st.button("🚀 Send"):
    if not GROQ_API_URL or not GROQ_API_KEY:
        st.error("Missing API key or URL. Please set them in your .env file.")
    elif user_input.strip() == "":
        st.warning("Enter a message before sending.")
    else:
        with st.spinner("Thinking..."):
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
                    reply = response.json()["choices"][0]["message"]["content"]
                    st.session_state.chat_history.append(("user", user_input))
                    st.session_state.chat_history.append(("bot", reply))
                else:
                    st.error(f"API Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Request failed: {str(e)}")

# Display chat history
for role, message in reversed(st.session_state.chat_history):
    css_class = "user-message" if role == "user" else "bot-message"
    st.markdown(f'<div class="message-container {css_class}">{message}</div>', unsafe_allow_html=True)
