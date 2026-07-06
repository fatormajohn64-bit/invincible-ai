"""
3_🤖_AI_Terminal.py
====================
Updated AI Terminal with correct API key reference and current model configuration.
"""

import streamlit as st
import requests

# ---------------------------------------------------------------------------
# GLOBAL CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(page_title="AI Terminal", page_icon="🤖", layout="centered")

# Retrieve Secret key from 1000023794.jpg
GROQ_API_KEY = st.secrets.get("NEW_SERVICE_API_KEY", None)

# Styling (Unified Theme)
INK, SURFACE, SURFACE_2, LINE, TEXT = "#0A0E14", "#12161F", "#191E2A", "#242938", "#E7EAF0"
st.markdown(f"""
    <style>
    .stApp {{background: {INK};}}
    div[data-testid="stChatMessage"] {{background-color: {SURFACE} !important; border: 1px solid {LINE} !important; border-radius: 12px !important; padding: 16px !important;}}
    div[data-testid="stChatMessage"] p {{color: {TEXT} !important;}}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# MAIN INTERFACE
# ---------------------------------------------------------------------------
st.title("🤖 Invincible AI Command Terminal")

if not GROQ_API_KEY:
    st.error("API Key missing. Ensure 'NEW_SERVICE_API_KEY' is set in your Streamlit secrets.")
else:
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "⚡ System Ready."}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Input command..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            
            # --- Payload Construction with Current Model ---
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                ]
            }

            try:
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                    json=payload,
                    timeout=20
                )

                if response.status_code == 200:
                    ai_response = response.json()["choices"][0]["message"]["content"]
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    response_placeholder.markdown(ai_response)
                else:
                    # Detailed Error Reporting
                    error_data = response.json()
                    error_msg = error_data.get("error", {}).get("message", "Unknown Error")
                    response_placeholder.error(f"Error {response.status_code}: {error_msg}")

            except Exception as e:
                response_placeholder.error(f"Connection failed: {str(e)}")
                
