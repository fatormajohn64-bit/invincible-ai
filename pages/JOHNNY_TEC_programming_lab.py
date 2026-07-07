"""
JOHNNY_TEC_programming_lab.py (Streamlit Production Mainframe)
============================================================
Integrated multi-engine matrix for 4 distinct AI processing cores:
- Google Gemini Engine Core
- Groq High-Speed Compiler
- OpenAI Intelligence Matrix
- Anthropic Claude Reasoning Matrix
"""

import streamlit as st
import os
from groq import Groq
import google.generativeai as genai
from openai import OpenAI
from anthropic import Anthropic

# ---------------------------------------------------------------------------
# 1. CORE CONFIGURATION & PERSISTENT DATA MATRICES
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="JOHNNY TEC Programming Lab",
    page_icon="💻",
    layout="wide"
)

# Color Theme System Constants
INK = "#020408"
SURFACE = "#070C16"
CYAN = "#00F0FF"
VIOLET = "#A855F7"
MATRIX = "#22C55E"
TEXT = "#F8FAFC"
MUTED = "#64748B"
HOT_PINK = "#F43F5E"

# Inject Custom Structural Styles for Dashboard and One-Click Code Extractions
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
    
    /* Clean formatting layout for generated script blocks */
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

# Secure API Key Gathering Protocols via Environment Variables or Streamlit Secrets
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY", ""))
ANTHROPIC_API_KEY = st.secrets.get("ANTHROPIC_API_KEY", os.environ.get("ANTHROPIC_API_KEY", ""))

# ---------------------------------------------------------------------------
# 2. CONTROL INTERFACE & SWITCH NOTIFICATION PROTOCOLS
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛠️ Core Matrix Router")
    
    # 4 Functioning API Options Selection Box
    engine_choice = st.selectbox(
        "Select Active API Core Matrix",
        [
            "Google Gemini Core",
            "Groq High-Speed Core",
            "OpenAI Intelligence Core",
            "Anthropic Claude Core"
        ]
    )
    
    # Track selection changes in storage state to fire an active toggle toast notification
    if "active_engine" not in st.session_state:
        st.session_state.active_engine = engine_choice
        
    if st.session_state.active_engine != engine_choice:
        st.toast(f"Matrix Routing Shift: Successfully connected to {engine_choice}!", icon="🔄")
        st.session_state.active_engine = engine_choice

    st.divider()
    
    # Blueprint context ingestion upload matrix tools
    st.markdown("### 📂 Context Ingestion Matrix")
    uploaded_file = st.file_uploader("Upload script context files", type=["py", "txt", "js", "html", "css", "md", "json"])
    camera_capture = st.camera_input("Scan document blueprint or visual bugs")

# Process uploaded script context files immediately
file_payload_text = ""
if uploaded_file:
    try:
        file_payload_text = uploaded_file.getvalue().decode("utf-8")
        st.sidebar.success(f"Context locked: `{uploaded_file.name}`")
    except Exception as read_err:
        st.sidebar.error(f"Context ingestion block: {read_err}")

# ---------------------------------------------------------------------------
# 3. INTERFACE VISUAL HEADERS & TELEMETRY INDICATORS
# ---------------------------------------------------------------------------
st.markdown('<div class="terminal-title">JOHNNY TEC PROGRAMMING LAB</div>', unsafe_allow_html=True)
st.markdown('<div class="status-ticker">● GLOBAL MATRIX OPERATIONAL // 4-API PIPELINES ENGAGED</div>', unsafe_allow_html=True)

# Precalculate status values to cleanly bypass f-string formatting constraints
gemini_status = "CONNECTED" if GEMINI_API_KEY else "MISSING"
gemini_color = MATRIX if GEMINI_API_KEY else HOT_PINK

groq_status = "CONNECTED" if GROQ_API_KEY else "MISSING"
groq_color = MATRIX if GROQ_API_KEY else HOT_PINK

openai_status = "CONNECTED" if OPENAI_API_KEY else "MISSING"
openai_color = MATRIX if OPENAI_API_KEY else HOT_PINK

anthropic_status = "CONNECTED" if ANTHROPIC_API_KEY else "MISSING"
anthropic_color = MATRIX if ANTHROPIC_API_KEY else HOT_PINK

# Output Clean Telemetry Cards across a unified grid block rows layout
t_col1, t_col2, t_col3, t_col4 = st.columns(4)
with t_col1:
    st.markdown(f'<div class="telemetry-card"><span style="color:{MUTED}; font-size:0.72rem;">GEMINI ENGINE</span><br><span style="color:{gemini_color}; font-size:0.95rem; font-weight:bold;">{gemini_status}</span></div>', unsafe_allow_html=True)
with t_col2:
    st.markdown(f'<div class="telemetry-card"><span style="color:{MUTED}; font-size:0.72rem;">GROQ COMPILER</span><br><span style="color:{groq_color}; font-size:0.95rem; font-weight:bold;">{groq_status}</span></div>', unsafe_allow_html=True)
with t_col3:
    st.markdown(f'<div class="telemetry-card"><span style="color:{MUTED}; font-size:0.72rem;">OPENAI MATRIX</span><br><span style="color:{openai_color}; font-size:0.95rem; font-weight:bold;">{openai_status}</span></div>', unsafe_allow_html=True)
with t_col4:
    st.markdown(f'<div class="telemetry-card"><span style="color:{MUTED}; font-size:0.72rem;">CLAUDE REASONER</span><br><span style="color:{anthropic_color}; font-size:0.95rem; font-weight:bold;">{anthropic_status}</span></div>', unsafe_allow_html=True)

# Initialize deep session storage context memories so records don't disappear on state reloads
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Permanently output active historical chat elements down the primary screen viewport
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# System Instruction Framework to force comprehensive script outputs
SYSTEM_PROMPT = (
    "You are the master artificial intelligence framework of the JOHNNY TEC Programming Lab. "
    "When requested to write programs, apps, or configurations, ALWAYS provide completely written, "
    "fully functional scripts inside a standard code block markdown syntax wrapper. Never include shortcuts, "
    "placeholders, or truncated segments."
)

# ---------------------------------------------------------------------------
# 4. MULTI-ENGINE DISPATCH LOGIC WRAPPERS
# ---------------------------------------------------------------------------
if user_message := st.chat_input("Inject script instructions into core mainframe matrix..."):
    
    # Display user input elements on-screen immediately and save into state memories
    st.chat_message("user").markdown(user_message)
    st.session_state.chat_history.append({"role": "user", "content": user_message})
    
    # Append external uploaded code document contexts dynamically to processing inputs
    final_prompt = user_message
    if file_payload_text:
        final_prompt += f"\n\n[CONTEXT ATTACHMENT PROVIDE]:\n```\n{file_payload_text}\n```"
        
    # Open streaming layout placeholder targets
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response_text = ""
        
        try:
            # MATRIX ROUTE A: GOOGLE GEMINI ENGINE PIPELINES
            if engine_choice == "Google Gemini Core":
                if not GEMINI_API_KEY:
                    st.error("Execution Interrupted: `GEMINI_API_KEY` configuration is missing.")
                    st.stop()
                    
                genai.configure(api_key=GEMINI_API_KEY)
                model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=SYSTEM_PROMPT)
                
                if camera_capture:
                    img_bytes = camera_capture.getvalue()
                    img_components = [{"mime_type": "image/jpeg", "data": img_bytes}]
                    response = model.generate_content([final_prompt, img_components[0]], stream=True)
                else:
                    response = model.generate_content(final_prompt, stream=True)
                    
                for chunk in response:
                    if chunk.text:
                        full_response_text += chunk.text
                        response_placeholder.markdown(full_response_text)

            # MATRIX ROUTE B: GROQ HIGH-SPEED API CHANNELS
            elif engine_choice == "Groq High-Speed Core":
                if not GROQ_API_KEY:
                    st.error("Execution Interrupted: `GROQ_API_KEY` configuration is missing.")
                    st.stop()
                    
                groq_client = Groq(api_key=GROQ_API_KEY)
                completion = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": final_prompt}
                    ],
                    temperature=0.2,
                    stream=True
                )
                for chunk in completion:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        full_response_text += delta
                        response_placeholder.markdown(full_response_text)

            # MATRIX ROUTE C: OPENAI INTELLIGENCE API INTERFACES
            elif engine_choice == "OpenAI Intelligence Core":
                if not OPENAI_API_KEY:
                    st.error("Execution Interrupted: `OPENAI_API_KEY` configuration is missing.")
                    st.stop()
                    
                openai_client = OpenAI(api_key=OPENAI_API_KEY)
                completion = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": final_prompt}
                    ],
                    temperature=0.2,
                    stream=True
                )
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_response_text += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_response_text)

            # MATRIX ROUTE D: ANTHROPIC CLAUDE RUNTIME MATRIX
            elif engine_choice == "Anthropic Claude Core":
                if not ANTHROPIC_API_KEY:
                    st.error("Execution Interrupted: `ANTHROPIC_API_KEY` configuration is missing.")
                    st.stop()
                    
                anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)
                with anthropic_client.messages.stream(
                    model="claude-3-5-sonnet-latest",
                    max_tokens=4096,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": final_prompt}]
                ) as stream_channel:
                    for text_segment in stream_channel.text_stream:
                        full_response_text += text_segment
                        response_placeholder.markdown(full_response_text)

            # Finalize stream generation actions and permanently store results into state memory caches
            st.session_state.chat_history.append({"role": "assistant", "content": full_response_text})
            
        except Exception as system_crash_anomaly:
            st.error(f"Mainframe core data transfer anomaly detected: {system_crash_anomaly}")
