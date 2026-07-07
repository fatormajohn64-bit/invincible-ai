"""
JOHNNY_TEC_programming_lab.py
====================================
Elite Cyberpunk Dev Sandbox & Code Architecture Mainframe.
Specialized in Python, Full-Stack Generation, Complex Bug Diagnostics, and Architectural Roadmaps.
"""

import streamlit as st
import base64
import os
from groq import Groq

# ---------------------------------------------------------------------------
# MAIN PAGE ROUTING CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="JOHNNY TEC Programming Lab",
    page_icon="💻",
    layout="wide"
)

# Fetching core infrastructure credentials
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", None))

# ---------------------------------------------------------------------------
# HARDCORE CYBERPUNK CSS DESIGN SYSTEM
# ---------------------------------------------------------------------------
INK = "#030508"
SURFACE = "#0B0F19"
SURFACE_LIGHT = "#121826"
CYAN = "#00F0FF"
VIOLET = "#9D4EDD"
MATRIX = "#39FF14"
TEXT = "#F1F4FA"
MUTED = "#7C879C"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@500&display=swap');
    
    .stApp {{
        background: {INK};
    }}
    
    section[data-testid="stSidebar"] {{
        background: {SURFACE} !important;
        border-right: 1px solid rgba(0, 240, 255, 0.2) !important;
    }}
    
    h1, h2, h3, h4 {{
        font-family: 'Space Grotesk', sans-serif !important;
        color: {TEXT} !important;
    }}
    
    .terminal-title {{
        background: linear-gradient(90deg, {CYAN} 0%, {VIOLET} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem !important;
        font-weight: 700;
        letter-spacing: -1px;
        margin-bottom: 0px;
    }}
    
    .status-ticker {{
        font-family: 'JetBrains Mono', monospace;
        color: {MATRIX};
        font-size: 0.8rem;
        letter-spacing: 2px;
        margin-bottom: 20px;
        text-shadow: 0 0 8px {MATRIX};
    }}
    
    /* Premium Panel Box styling */
    .lab-panel {{
        background: {SURFACE_LIGHT};
        border: 1px solid rgba(157, 78, 221, 0.3);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 0 20px rgba(157, 78, 221, 0.1);
        margin-bottom: 20px;
    }}
    
    /* Code area styling overrides */
    div[data-testid="stMarkdownContainer"] pre {{
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        background-color: {SURFACE} !important;
        border-radius: 8px !important;
        box-shadow: inset 0 0 10px rgba(0, 240, 255, 0.05);
    }}
    
    /* Form input styling overrides */
    div[data-testid="stTextArea"] textarea {{
        background-color: {SURFACE} !important;
        color: {TEXT} !important;
        border: 1px solid rgba(157, 78, 221, 0.3) !important;
        font-family: 'JetBrains Mono', monospace !important;
    }}
    
    .mode-badge {{
        background: rgba(0, 240, 255, 0.1);
        border: 1px solid {CYAN};
        color: {CYAN};
        padding: 4px 12px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------------
# CORE LOGIC UTILITIES
# ---------------------------------------------------------------------------
def encode_image_base64(uploaded_file):
    """Safely converts file uploads or camera frames into Base64 strings for vision tracking."""
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        return base64.b64encode(file_bytes).decode("utf-8")
    return None

# ---------------------------------------------------------------------------
# HEADER BRANDING FRAME
# ---------------------------------------------------------------------------
st.markdown('<div class="terminal-title">JOHNNY TEC PROGRAMMING LAB</div>', unsafe_allow_html=True)
st.markdown('<div class="status-ticker">// MAINFRAME ONLINE // CORE ENGINE: PYTHON FOCUS</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# CONTROL ROOM SIDE PANEL
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛠️ Operation Directives")
    
    # 1. Select the main technical objective
    lab_mode = st.selectbox(
        "Select Operation Target",
        [
            "🚀 Full-Stack Architect (Build Apps & Guides)",
            "🩺 Error Core Analyzer (Debug Stack Traces)",
            "🏗️ Massive Task Compiler (Breakdown Large Codebases)"
        ]
    )
    
    # 2. Select target language platform
    target_lang = st.selectbox(
        "Primary Code Core",
        ["Python (Core Focal Point)", "JavaScript / TypeScript", "HTML & CSS Complete Frontend", "C++ System Programming", "Shell Scripting / Bash"]
    )
    
    st.divider()
    
    # 3. Code Upload Assets
    st.markdown("### 📂 Blueprint Ingestion Matrix")
    uploaded_code_file = st.file_uploader("Upload Payload Script", type=["py", "txt", "js", "html", "css", "cpp", "json"])
    
    # 4. Physical Document Camera Matrix
    st.markdown("### 📸 Document Core Scanner")
    camera_capture = st.camera_input("Scan Code Blueprint / Error Document")

st.divider()

# ---------------------------------------------------------------------------
# MAIN OPERATIONAL INTERFACE
# ---------------------------------------------------------------------------
if not GROQ_API_KEY:
    st.error("🚨 CORE REACTION FAILURE: `GROQ_API_KEY` missing from cluster secrets configuration environment.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# Assemble text inputs based on the target execution mode
st.markdown(f'<div class="lab-panel">', unsafe_allow_html=True)
st.markdown(f"### ⚙️ Operational Core Target Settings")

user_prompt = st.text_area(
    "Define your build requirements, paste buggy scripts, or layout your massive software design parameters below:",
    height=180,
    placeholder="Example: Design a responsive modern landing page for an app using streamlit components or write an automated data scraping engine in python with step-by-step installation instructions..."
)

# Extract content from uploaded text assets if available
file_content = ""
if uploaded_code_file:
    try:
        file_content = uploaded_code_file.getvalue().decode("utf-8")
        st.success(f"Successfully loaded code payload: `{uploaded_code_file.name}` ({len(file_content)} characters extracted)")
    except Exception as e:
        st.error(f"Error reading file structure payload data stream: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# Process visual assets if present (Vision Model Router)
base64_visual_payload = None
if camera_capture:
    base64_visual_payload = encode_image_base64(camera_capture)
    st.image(camera_capture, caption="📷 Document Snapshot Intercepted Successfully", width=300)

# ---------------------------------------------------------------------------
# COMPILING LOGIC ENGINE ON TRIGGER CLICK
# ---------------------------------------------------------------------------
if st.button("⚡ EXECUTE COMPILER RUN", type="primary", use_container_width=True):
    if not user_prompt and not file_content and not base64_visual_payload:
        st.warning("⚠️ Mainframe processing input empty. Please specify code parameters, capture image, or load target script payloads.")
    else:
        # Construct the execution instruction prompt
        system_instructions = (
            "You are the premier AI core of JOHNNY TEC programming lab, an elite master engineer and world class full-stack designer. "
            f"Your current operation objective is: {lab_mode}. The target technology stack is centered on: {target_lang}. "
            "When writing web apps or full websites, provide complete, production-ready, clean, modular code snippets along with an explicit step-by-step technical deployment instruction roadmap showing configuration directories, required packages, and runtime executions. "
            "When analyzing errors, pinpoint exactly why the failure trace occurs and present optimized remediation patches. "
            "For massive assignments, structure structural breakdowns into clean milestone deployment checklists."
        )
        
        # Combine instructions with structural file scripts if provided
        combined_user_text = user_prompt if user_prompt else ""
        if file_content:
            combined_user_text += f"\n\n--- INGESTED PAYLOAD ATTACHMENT TEXT ---\n{file_content}"
            
        messages = []
        
        # Route processing depending on visual payload availability
        if base64_visual_payload:
            # Route to Groq's high speed Llama 3.2 Vision Model engine
            model_target = "llama-3.2-11b-vision-preview"
            messages = [
                {"role": "system", "content": system_instructions},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"Analyze the scanned blueprint attachment along with these directives:\n{combined_user_text}"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_visual_payload}"
                            }
                        }
                    ]
                }
            ]
        else:
            # Route to Groq's flagship intelligence model engine
            model_target = "llama-3.3-70b-versatile"
            messages = [
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": combined_user_text}
            ]
            
        try:
            with st.spinner("⚡ Processing system variables via compiler logic engine cores..."):
                completion = client.chat.completions.create(
                    model=model_target,
                    messages=messages,
                    temperature=0.2,
                    max_tokens=4096,
                    stream=True
                )
                
                # Render results into a beautiful terminal output frame
                st.markdown("### 📡 Mainframe Compilation Transmission Output")
                output_placeholder = st.empty()
                full_stream_response = ""
                
                for chunk in completion:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        full_stream_response += delta
                        output_placeholder.markdown(full_stream_response)
                        
            st.success("🏁 Core iteration operations complete. Scripts successfully organized.")
            
        except Exception as err:
            st.error(f"Execution matrix fault encountered: {err}")
