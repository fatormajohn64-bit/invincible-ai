"""
JOHNNY_TEC_programming_lab.py (Streamlit Production Mainframe)
============================================================
Integrated multi-engine terminal for Groq & Google Gemini APIs.
"""

import streamlit as st
import os
import base64
from groq import Groq
import google.generativeai as genai

# ---------------------------------------------------------------------------
# MAIN PAGE CONFIG & CYBERPUNK INTERFACE DESIGN
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="JOHNNY TEC Programming Lab",
    page_icon="💻",
    layout="wide"
)

# Color System
INK = "#020408"
SURFACE = "#070C16"
SURFACE_LIGHT = "#0F172A"
CYAN = "#00F0FF"
VIOLET = "#A855F7"
MATRIX = "#22C55E"
TEXT = "#F8FAFC"
MUTED = "#64748B"
HOT_PINK = "#F43F5E"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=JetBrains+Mono:wght@500&display=swap');
    
    .stApp {{ background: {INK}; }}
    
    section[data-testid="stSidebar"] {{
        background: {SURFACE} !important;
        border-right: 1px solid rgba(0, 240, 255, 0.2) !important;
    }}
    
    h1, h2, h3, h4 {{
        font-family: 'Orbitron', sans-serif !important;
        color: {TEXT} !important;
        letter-spacing: 1px;
    }}
    
    .terminal-title {{
        background: linear-gradient(90deg, {CYAN} 0%, {VIOLET} 50%, {HOT_PINK} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem !important;
        font-weight: 700;
        font-family: 'Orbitron', sans-serif;
        filter: drop-shadow(0 0 15px rgba(0, 240, 255, 0.3));
        margin-bottom: 5px;
    }}
    
    .status-ticker {{
        font-family: 'JetBrains Mono', monospace;
        color: {MATRIX};
        font-size: 0.85rem;
        letter-spacing: 2px;
        margin-bottom: 25px;
        text-shadow: 0 0 8px {MATRIX};
    }}
    
    .telemetry-card {{
        background: {SURFACE};
        border-left: 3px solid {CYAN};
        border-radius: 6px;
        padding: 12px 18px;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 15px;
    }}
    
    /* Perfect One-Click Code Box Layout */
    div[data-testid="stMarkdownContainer"] pre {{
        border: 1px solid rgba(0, 240, 255, 0.25) !important;
        background-color: #030712 !important;
        border-radius: 10px !important;
        padding: 15px !important;
        box-shadow: inset 0 0 15px rgba(0, 240, 255, 0.08) !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------------
# CREDENTIALS INGESTION
# ---------------------------------------------------------------------------
# Pull keys automatically from environment or Streamlit secrets
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))

# ---------------------------------------------------------------------------
# APP HEADER & TELEMETRY INDICATORS
# ---------------------------------------------------------------------------
st.markdown('<div class="terminal-title">JOHNNY TEC PROGRAMMING LAB</div>', unsafe_allow_html=True)
st.markdown('<div class="status-ticker">● MAINFRAME OPERATIONAL // DUAL-ROUTED ENGINE READY</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# SIDEBAR CONTROL ROOM
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛠️ Core Configuration")
    
    # Engine Router (Distributes loads completely to separate model architectures)
    engine_choice = st.selectbox(
        "Select Active API Core Matrix",
        [
            "Gemini 1.5 Flash (Ultra-Fast Core)",
            "Gemini 1.5 Pro (Deep Reasoning)",
            "Groq Llama 3.3 (High-Speed Compiler)"
        ]
    )
    
    st.divider()
    
    # File & Blueprint Upload Section
    st.markdown("### 📂 Blueprint Ingestion Matrix")
    uploaded_file = st.file_uploader("Upload script context / documentation", type=["py", "txt", "js", "html", "css", "md", "json"])
    camera_capture = st.camera_input("Scan document blueprint or visual errors")

# Inform the layout about current file payloads instantly
file_payload_text = ""
if uploaded_file:
    try:
        file_payload_text = uploaded_file.getvalue().decode("utf-8")
        st.sidebar.success(f"Locked context file: `{uploaded_file.name}`")
    except Exception as e:
        st.sidebar.error(f"Context error: {e}")

# Display active pipeline stats on screen
t_col1, t_col2, t_col3 = st.columns(3)
with t_col1:
    st.markdown(f'<div class="telemetry-card"><span style="color:{MUTED}; font-size:0.75rem;">ROUTED CORE</span><br><span style="color:{CYAN}; font-size:1.0rem; font-weight:bold;">{engine_choice.split(" ")[0]} Matrix</span></div>', unsafe_allow_html=True)
with t_col2:
    st.markdown(f'<div class="telemetry-card"><span style="color:{MUTED}; font-size:0.75rem;">GEMINI ENGINE</span><br><span style="color:{MATRIX} if GEMINI_API_KEY else HOT_PINK}; font-size:1.0rem; font-weight:bold;">{"CONNECTED" if GEMINI_API_KEY else "MISSING"}</span></div>', unsafe_allow_html=True)
with t_col3:
    st.markdown(f'<div class="telemetry-card"><span style="color:{MUTED}; font-size:0.75rem;">GROQ ENGINE</span><br><span style="color:{MATRIX} if GROQ_API_KEY else HOT_PINK}; font-size:1.0rem; font-weight:bold;">{"CONNECTED" if GROQ_API_KEY else "MISSING"}</span></div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# LIVE CHAT INTERACTIVE PERSISTENCE ENGINE
# ---------------------------------------------------------------------------
# Prevent message memory loss when pages refresh
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Print persistent history on screen inside styled elements
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# System Instruction Blueprint to ensure full file output without shortcuts
SYSTEM_PROMPT = (
    "You are the supreme master artificial intelligence core of the JOHNNY TEC Programming Lab. "
    "When requested to build code or apps, ALWAYS generate comprehensive, clean, functional scripts without summaries or missing lines. "
    "Put your main logical codebase clearly inside a unified markdown block so the user can easily duplicate it with a single click."
)

# ---------------------------------------------------------------------------
# CHAT EXECUTION LOGIC ENVELOPE
# ---------------------------------------------------------------------------
if user_message := st.chat_input("Inject instruction script into active engine core..."):
    
    # Immediately render human user prompt
    st.chat_message("user").markdown(user_message)
    st.session_state.chat_history.append({"role": "user", "content": user_message})
    
    # Append loaded document attachments if present to the prompt automatically
    final_prompt = user_message
    if file_payload_text:
        final_prompt += f"\n\n[CONTEXT ATTACHMENT PROVIDE]:\n```\n{file_payload_text}\n```"
        
    # Render assistant placeholder to safely stream incoming data matrices
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response_text = ""
        
        try:
            # INTERFACE ROUTE A: GOOGLE GEMINI ENGINES
            if "Gemini" in engine_choice:
                if not GEMINI_API_KEY:
                    st.error("Missing GEMINI_API_KEY variable.")
                    st.stop()
                    
                genai.configure(api_key=GEMINI_API_KEY)
                model_id = "gemini-1.5-flash" if "Flash" in engine_choice else "gemini-1.5-pro"
                
                # Combine System Instructions with Context
                model = genai.GenerativeModel(
                    model_name=model_id,
                    system_instruction=SYSTEM_PROMPT
                )
                
                # Process text or images
                if camera_capture:
                    bytes_data = camera_capture.getvalue()
                    image_parts = [{"mime_type": "image/jpeg", "data": bytes_data}]
                    response = model.generate_content([final_prompt, image_parts[0]], stream=True)
                else:
                    response = model.generate_content(final_prompt, stream=True)
                
                for chunk in response:
                    if chunk.text:
                        full_response_text += chunk.text
                        response_placeholder.markdown(full_response_text)

            # INTERFACE ROUTE B: GROQ COMPILER ENGINE
            elif "Groq" in engine_choice:
                if not GROQ_API_KEY:
                    st.error("Missing GROQ_API_KEY variable.")
                    st.stop()
                    
                groq_client = Groq(api_key=GROQ_API_KEY)
                
                # Build context messages array
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": final_prompt}
                ]
                
                completion = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    temperature=0.15,
                    stream=True
                )
                
                for chunk in completion:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        full_response_text += delta
                        response_placeholder.markdown(full_response_text)
                        
            # Save streaming output inside state memory safely so it doesn't get lost
            st.session_state.chat_history.append({"role": "assistant", "content": full_response_text})
            
        except Exception as crash_error:
            st.error(f"Mainframe routing anomaly detected: {crash_error}")
    
