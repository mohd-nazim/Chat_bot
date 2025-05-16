# app.py
# app.py

import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Groq API URL and Key
GROQ_API_URL = os.getenv('GROQ_API_URL')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Streamlit UI
st.title('LLM-based Chatbot using Groq API')
st.markdown('Ask anything to the chatbot:')

# User input
user_input = st.text_input('You: ', '')

if user_input:
    st.markdown('**Bot is thinking...**')
    
    # API call to Groq
    response = requests.post(
        GROQ_API_URL,
        headers={'Authorization': f'Bearer {GROQ_API_KEY}'},
        json={'prompt': user_input}
    )
    
    if response.status_code == 200:
        reply = response.json().get('response', 'No response from the API.')
        st.markdown(f'**Bot:** {reply}')
    else:
        st.error('Failed to connect to the Groq API. Please check your credentials.')

#new code


print("GROQ_API_URL:", GROQ_API_URL)
print("GROQ_API_KEY:", GROQ_API_KEY)
