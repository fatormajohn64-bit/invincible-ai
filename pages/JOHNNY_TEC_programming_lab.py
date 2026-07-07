"""
JOHNNY_TEC_programming_lab.py
====================================
Elite Cyberpunk Dev Sandbox & Code Architecture Mainframe.
Specialized in Python, Full-Stack Generation, Complex Bug Diagnostics, and Architectural Roadmaps.
"""

import streamlit as st
import base64
import os
import time
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
# NEXT-GEN CYBERPUNK CSS DESIGN SYSTEM
# ---------------------------------------------------------------------------
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
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=JetBrains+Mono:wght@500&family=Space+Grotesk:wght@500;700&display=swap');
    
    .stApp {{
        background: {INK};
    }}
    
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
        font-size: 3rem !important;
        font-weight: 700;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: -1px;
        margin-bottom: 0px;
        filter: drop-shadow(0 0 15px rgba(0, 240, 255, 0.3));
    }}
    
    /* Animated Ticker Status */
    @keyframes pulse-glow {{
        0% {{ text-shadow: 0 0 4px {MATRIX}; opacity: 0.8; }}
        50% {{ text-shadow: 0 0 12px {MATRIX}, 0 0 20px {MATRIX}; opacity: 1; }}
        100% {{ text-shadow: 0 0 4px {MATRIX}; opacity: 0.8; }}
    }}
    
    .status-ticker {{
        font-family: 'JetBrains Mono', monospace;
        color: {MATRIX};
        font-size: 0.85rem;
        letter-spacing: 2px;
        margin-bottom: 25px;
        animation: pulse-glow 2.5s infinite;
    }}
    
    /* Premium Telemetry Grid Cards */
    .telemetry-card {{
        background: {SURFACE};
        border-left: 3px solid {CYAN};
        border-radius: 6px;
        padding: 12px 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
        font-family: 'JetBrains Mono', monospace;
    }}
    
    /* Premium Control Input Frame */
    .lab-panel {{
        background: linear-gradient(145deg, {SURFACE_LIGHT}, {SURFACE});
        border: 1px solid rgba(168, 85, 247, 0.4);
        border-radius: 14px;
        padding: 28px;
        box-shadow: 0 0 30px rgba(168, 85, 247, 0.15);
        margin-bottom: 25px;
    }}
    
    /* Code block syntax container override */
    div[data-testid="stMarkdownContainer"] pre {{
        border: 1px solid rgba(0, 240, 255, 0.25) !important;
        background-color: #030712 !important;
        border-radius: 10px !important;
        padding: 15px !important;
        box-shadow: inset 0 0 15px rgba(0, 240, 255, 0.08) !important;
    }}
    
    /* Input textarea glowing focus */
    div[data-testid="stTextArea"] textarea {{
        background-color: {SURFACE} !important;
        color: {TEXT} !important;
        border: 1px solid rgba(168, 85, 247, 0.4) !important;
        border-radius: 8px !important;
        font-family: 'JetBrains Mono', monospace !important;
        transition: all 0.3s ease;
    }}
    div[data-testid="stTextArea"] textarea:focus {{
        border-color: {CYAN} !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.2) !important;
    }}
    
    /* Custom button aesthetics */
    div.stButton > button:first-child {{
        background: linear-gradient(90deg, #7C3AED 0%, #C084FC 100%) !important;
        color: white !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        border: none !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4) !important;
        transition: all 0.3s ease !important;
    }}
    div.stButton > button:first-child:hover {{
        background: linear-gradient(90deg, #C084FC 0%, #00F0FF 100%) !important;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.6) !important;
        transform: translateY(-1px);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------------
# CORE IMAGE ENCODING UTILITIES
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
st.markdown('<div class="status-ticker">● CORE COMPILER STATUS: ULTRA-READY // SYSTEM STACK LINKED</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# MAINFRAME TELEMETRY GRID
# ---------------------------------------------------------------------------
t_col1, t_col2, t_col3, t_col4 = st.columns(4)
with t_col1:
    st.markdown(f'<div class="telemetry-card"><span style="color:{MUTED}; font-size:0.75rem;">PRIMARY MODULE</span><br><span style="color:{CYAN}; font-size:1.05rem; font-weight:bold;">FULL-STACK QUANTUM</span></div>', unsafe_allow_html=True)
with t_col2:
    st.markdown(f'<div class="telemetry-card"><span style="color:{MUTED}; font-size:0.75rem;">VISION TRANSLATOR</span><br><span style="color:{VIOLET}; font-size:1.05rem; font-weight:bold;">QWEN 3.6 MULTIMODAL</span></div>', unsafe_allow_html=True)
with t_col3:
    st.markdown(f'<div class="telemetry-card"><span style="color:{MUTED}; font-size:0.75rem;">REASONING DEPTH</span><br><span style="color:{MATRIX}; font-size:1.05rem; font-weight:bold;">GPT-OSS 120B ENGINE</span></div>', unsafe_allow_html=True)
with t_col4:
    st.markdown(f'<div class="telemetry-card"><span style="color:{MUTED}; font-size:0.75rem;">COMPILATION SPEED</span><br><span style="color:{HOT_PINK}; font-size:1.05rem; font-weight:bold;">~660 TOKENS / SEC</span></div>', unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------------------------------
# CONTROL ROOM SIDE PANEL (OPERATION OPTIONS & IMAGE CAPTURE)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛠️ Operation Directives")
    
    # 1. Target Objectives
    lab_mode = st.selectbox(
        "Select Operation Target",
        [
            "🚀 Full-Stack Architect (Build Apps & Complete Guides)",
            "🩺 Error Core Analyzer (Debug Stack Traces & Instant Fixes)",
            "🏗️ Massive Task Compiler (Breakdown Large Codebases & Files)"
        ]
    )
    
    # 2. Target Languages
    target_lang = st.selectbox(
        "Primary Code Core Stack",
        ["Python (Core Focal Point)", "JavaScript / TypeScript", "HTML, CSS & JS Complete Site", "C++ System Programming", "Shell / Termux Bash Automation"]
    )
    
    st.divider()
    
    # 3. Payload File Ingestor
    st.markdown("### 📂 Structural Script Payload")
    uploaded_code_file = st.file_uploader("Drop project code files or errors", type=["py", "txt", "js", "html", "css", "cpp", "json"])
    
    # 4. Premium Live Camera Scanner
    st.markdown("### 📸 Blueprint Document Scanner")
    camera_capture = st.camera_input("Capture handwritten wireframes, screen errors, or specs")

st.write("")

# ---------------------------------------------------------------------------
# MAIN PROGRAMMING INTERFACE CANVAS
# ---------------------------------------------------------------------------
if not GROQ_API_KEY:
    st.error("🚨 SYSTEM CONSOLE ALERT: `GROQ_API_KEY` missing from your Streamlit configuration vault secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# Command Specification Box
st.markdown(f'<div class="lab-panel">', unsafe_allow_html=True)
st.markdown(f"### ⚙️ Mainframe Command Input")

user_prompt = st.text_area(
    "Enter detailed construction maps, requirements, code blocks, or tell the mainframe what app you want to build:",
    height=200,
    placeholder="Example: Act as a master full-stack engineer. Build a beautiful complete web app with a gorgeous interface, and supply a detailed guide explaining the structure, files, and deployment layout..."
)

# Parse content from text scripts uploaded
file_content = ""
if uploaded_code_file:
    try:
        file_content = uploaded_code_file.getvalue().decode("utf-8")
        st.success(f"📂 Extracted script stream: `{uploaded_code_file.name}` ({len(file_content)} characters ready)")
    except Exception as e:
        st.error(f"Error reading file structure block: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# Parse base64 string from camera scanner frame
base64_visual_payload = None
if camera_capture:
    base64_visual_payload = encode_image_base64(camera_capture)
    st.markdown("#### 👁️ Captured Snapshot Metadata")
    st.image(camera_capture, caption="Intercepted Frame Buffer Matrix Ready for Processing", width=340)

# ---------------------------------------------------------------------------
# CORE SYSTEM LOGIC ENGINE ENFORCEMENT
# ---------------------------------------------------------------------------
if st.button("⚡ EXECUTE SYSTEM COMPILER RUN", use_container_width=True):
    if not user_prompt and not file_content and not base64_visual_payload:
        st.warning("⚠️ Action blocked. Provide instructions, scan blueprints, or load code payloads before compiling.")
    else:
        # High level system agent identity instructions
        system_instructions = (
            "You are the master terminal artificial intelligence core of the JOHNNY TEC Programming Lab. "
            "You are an elite, world-class full-stack engineer specialized completely in Python, web architecture, mobile applications, and rigorous optimization. "
            f"Current Operation Target Mode: {lab_mode}. Target Engine Language Core: {target_lang}.\n\n"
            "CRITICAL PROTOCOLS:\n"
            "1. When generating web apps or full websites, write production-ready, clean, modular code snippets without placeholder summaries.\n"
            "2. Always follow up your code with a comprehensive, step-by-step technical deployment instruction map covering folder directories, package installations, and execution terminal commands.\n"
            "3. When analyzing error screenshots or code text blocks, pinpoint the exact structural root cause and display the fully fixed, drop-in replacement code script.\n"
            "4. For massive assignments, parse requirements into a clean check-list milestone roadmap."
        )
        
        # Merge input data variables seamlessly
        combined_user_text = user_prompt if user_prompt else ""
        if file_content:
            combined_user_text += f"\n\n--- INGESTED PAYLOAD ATTACHMENT TEXT ---\n{file_content}"
            
        messages = []
        
        # Route processing depending on visual payload status
        if base64_visual_payload:
            # UPGRADED 2026 ROUTE: Harness Groq's high-speed Qwen 3.6 Multimodal Vision engine
            model_target = "qwen/qwen3.[span_1](start_span)6-27b"[span_1](end_span)
            messages = [
                {"role": "system", "content": system_instructions},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"Analyze the scanned blueprint capture along with these directives:\n{combined_user_text}"},
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
            # UPGRADED 2026 ROUTE: Harness Groq's flagship ultra-reasoning model for pure text processing
            model_target = "openai/gpt-oss-120b"
            messages = [
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": combined_user_text}
            ]
            
        try:
            start_time = time.time()
            
            with st.spinner("⚡ Matrix loop routing activated... Compiling data structure assets..."):
                completion = client.chat.completions.create(
                    model=model_target,
                    messages=messages,
                    temperature=0.15,
                    max_tokens=4096,
                    stream=True
                )
                
                st.markdown("### 📡 Mainframe Transmission Output")
                output_placeholder = st.empty()
                full_stream_response = ""
                
                # Stream responses in real-time
                for chunk in completion:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        full_stream_response += delta
                        output_placeholder.markdown(full_stream_response)
                        
            elapsed_time = round(time.time() - start_time, 2)
            st.success(f"🏁 System Core Execution Success! Pipeline finalized in {elapsed_time} seconds.")
            
        except Exception as err:
            st.error(f"Execution matrix fault encountered: {err}")
