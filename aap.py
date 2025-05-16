# app.py

import streamlit as st
import requests
from dotenv import load_dotenv
import os

# ✅ Explicitly load the .env file with full path
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# ✅ Environment variables
GROQ_API_URL = os.getenv("GROQ_API_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ✅ Debugging information
print("Loaded API URL:", GROQ_API_URL)
print("Loaded API Key:", GROQ_API_KEY)

if not GROQ_API_URL or not GROQ_API_KEY:
    st.error("API URL or API Key is missing. Please check your .env file.")
else:
    # Streamlit UI
    st.title("Groq Chatbot")
    st.markdown("Ask anything to the chatbot:")

    # User input
    user_input = st.text_input("You: ", "")

    if st.button("Send"):
        if user_input:
            with st.spinner("Connecting to Groq API..."):
                try:
                    # ✅ API call to Groq
                    response = requests.post(
                        GROQ_API_URL,
                        headers={
                            "Authorization": f"Bearer {GROQ_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "llama-3.3-70b-versatile",
                            "messages": [
                                {"role": "user", "content": user_input}
                            ]
                        }
                    )

                    # ✅ Debugging response
                    print("Response Status Code:", response.status_code)
                    print("Response Text:", response.text)

                    if response.status_code == 200:
                        reply = response.json().get('choices', [{}])[0].get('message', {}).get('content', 'No response from the API.')
                        st.markdown(f"**Bot:** {reply}")
                    else:
                        st.error(f"Failed to connect: {response.status_code} - {response.text}")

                except Exception as e:
                    st.error(f"Request failed: {str(e)}")
        else:
            st.warning("Please type a message before sending.")
