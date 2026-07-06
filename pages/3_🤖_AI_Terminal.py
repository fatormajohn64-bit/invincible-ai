"""
3_🤖_AI_Terminal.py
====================
Premium Cyber-Dark AI Chat Terminal.
Integrates ultra-fast LLM completion architecture securely using Streamlit Secrets.
"""

import streamlit as st
import requests

# ---------------------------------------------------------------------------
# GLOBAL PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Terminal",
    page_icon="🤖",
    layout="centered"
)

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", None)

# ---------------------------------------------------------------------------
# DESIGN TOKENS & TYPOGRAPHY STYLE (Unified Theme)
# ---------------------------------------------------------------------------
INK        = "#0A0E14"
SURFACE    = "#12161F"
SURFACE_2  = "#191E2A"
LINE       = "#242938"
TEXT       = "#E7EAF0"
MUTED      = "#7C879C"
SIGNAL     = "#28E0C4"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght=500;600;700&family=Inter:wght=400;500;600&family=JetBrains+Mono:wght=500&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background: {INK};
    }}

    section[data-testid="stSidebar"] {{
        background: {SURFACE};
        border-right: 1px solid {LINE};
    }}

    h1, h2, h3, h4 {{
        font-family: 'Space Grotesk', sans-serif !important;
        color: {TEXT} !important;
        letter-spacing: -0.02em;
    }}

    div[data-testid="stChatMessage"] {{
        background-color: {SURFACE} !important;
        border: 1px solid {LINE} !important;
        border-radius: 12px !important;
        padding: 16px !important;
        margin-bottom: 12px !important;
    }}

    div[data-testid="stChatMessage"] p {{
        color: {TEXT} !important;
    }}

    div[data-testid="stChatInput"] textarea {{
        background-color: {SURFACE_2} !important;
        color: {TEXT} !important;
        border: 1px solid {LINE} !important;
        border-radius: 10px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------------
# INTERFACE MAIN COMPONENT VIEW
# ---------------------------------------------------------------------------
st.title("🤖 Invincible AI Command Terminal")
st.caption("Secure neural link interface for script generation, code optimization, and analytical reasoning.")

if not GROQ_API_KEY:
    st.warning("⚠️ AI Core API Key Missing")
    st.markdown(
        "To activate this module stream:\n"
        "1. Generate a free API key at **console.groq.com**.\n"
        "2. Add your key token to your cloud management variables as `GROQ_API_KEY`."
    )
    st.markdown("---")
    st.markdown("### 🖥️ Chat Terminal (Demo Simulation)")
    st.chat_message("assistant", avatar="🤖").write("System Core is ready. Provide API authorization sequence to initiate execution.")
    st.chat_input("Input command string...", disabled=True)

else:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "⚡ Encryption handshake complete. Core Terminal ready for prompt command lines."}
        ]

    for msg in st.session_state.messages:
        avatar_icon = "🤖" if msg["role"] == "assistant" else "👤"
        st.chat_message(msg["role"], avatar=avatar_icon).write(msg["content"])

    if prompt := st.chat_input("Input deep prompt query statement..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user", avatar="👤").write(prompt)
        
        with st.chat_message("assistant", avatar="🤖"):
            response_placeholder = st.empty()
            response_placeholder.markdown("`Connecting to server matrix...`")
            
            try:
                api_url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "llama3-8b-8192",
                    "messages": [
                        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                    ],
                    "temperature": 0.5,
                    "max_tokens": 1024
                }
                
                response = requests.post(api_url, headers=headers, json=payload, timeout=15)
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result["choices"][0]["message"]["content"]
                    response_placeholder.markdown(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                else:
                    response_placeholder.error(f"Matrix connection failure. Code: {response.status_code}")
                    
            except Exception as e:
                response_placeholder.error(f"Failed to resolve secure data link array: {e}")

# ---------------------------------------------------------------------------
# SIDEBAR REFRESH HOOK
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎛️ Terminal Settings")
    st.caption("Active Core Processing Layer")
    st.code("Model: Llama3-8b-8192\nLatency: ~0.18s", language="text")
    
    if st.button("Clear Terminal Log History", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "⚡ Terminal history array flushed. Memory context clear."}]
        st.rerun()
             
