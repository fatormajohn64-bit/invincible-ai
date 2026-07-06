import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Page Config
st.set_page_config(page_title="Invincible 911", page_icon="🤖")
st.title("🤖 Invincible 911")

# Load API key
load_dotenv()
# If running on Streamlit Cloud, it will use st.secrets; otherwise uses local .env
api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask Invincible 911..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
