"""
pages/2_🎬_Video_Generator.py
============================================================
JOHNNY TEC PROGRAMMING LAB - VIDEO MATRIX
Generates short video clips using Hugging Face Free Inference
"""

import streamlit as st
import os
import requests
import time

# ---------------------------------------------------------------------------
# 1. PAGE CONFIG & MATRIX STYLING
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Video Render Matrix", page_icon="🎬", layout="wide")

INK = "#020408"
SURFACE = "#070C16"
CYAN = "#00F0FF"
MATRIX = "#22C55E"
TEXT = "#F8FAFC"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=JetBrains+Mono:wght@500&display=swap');
    
    .stApp {{ background: {INK}; }}
    h1, h2, h3 {{ font-family: 'Orbitron', sans-serif !important; color: {TEXT} !important; }}
    
    .video-title {{
        background: linear-gradient(90deg, {CYAN} 0%, {MATRIX} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem !important;
        font-weight: 700;
        font-family: 'Orbitron', sans-serif;
        filter: drop-shadow(0 0 12px rgba(0, 240, 255, 0.25));
    }}
    .status-ticker {{
        font-family: 'JetBrains Mono', monospace; color: {MATRIX};
        font-size: 0.85rem; letter-spacing: 2px; margin-bottom: 25px;
        text-shadow: 0 0 8px {MATRIX};
    }}
    div[data-testid="stSidebar"] {{
        background: {SURFACE} !important;
        border-right: 1px solid rgba(0, 240, 255, 0.2) !important;
    }}
    
    /* Glowing Text Area */
    div[data-testid="stTextArea"] textarea {{
        background-color: {SURFACE} !important;
        color: {TEXT} !important;
        border: 1px solid rgba(0, 240, 255, 0.4) !important;
        border-radius: 8px !important;
        font-family: 'JetBrains Mono', monospace !important;
    }}
    
    /* Custom button aesthetics - Enhanced for High Contrast Readability */
    div.stButton > button:first-child {{
        background: linear-gradient(90deg, #00F0FF 0%, #22C55E 100%) !important;
        color: #020408 !important; /* Dark text for sharp readability */
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        border: none !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.4) !important;
        transition: all 0.3s ease !important;
    }}
    div.stButton > button:first-child:hover {{
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.6) !important;
        transform: translateY(-1px);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Pull Free Hugging Face Token 
HF_TOKEN = st.secrets.get("HF_TOKEN", os.environ.get("HF_TOKEN", ""))

# ---------------------------------------------------------------------------
# 2. SIDEBAR RENDERING CONTROLS (FREE TIER VIDEO ENDPOINTS)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎬 Video Cores")
    model_choice = st.selectbox(
        "Select Generative Core",
        [
            "damo-vilab/text-to-video-ms-1.7b",  # Core ModelScope video engine
            "cerspense/zeroscope_v2_576w"        # Core Zeroscope video engine
        ]
    )
    st.divider()
    st.markdown("💡 *Note: Video rendering requires massive computational power. Generating on a 100% free server may take 1-3 minutes.*")

# ---------------------------------------------------------------------------
# 3. INTERFACE HEADERS & VIDEO RUNTIME via direct API Requests
# ---------------------------------------------------------------------------
st.markdown('<div class="video-title">CINEMATIC VIDEO MATRIX</div>', unsafe_allow_html=True)
st.markdown('<div class="status-ticker">● VIDEO RENDERING PIPELINE // FREE OPEN-SOURCE HUB ACTIVE</div>', unsafe_allow_html=True)

if not HF_TOKEN:
    st.error("Execution Interrupted: `HF_TOKEN` secret configuration is missing in Streamlit.")
    st.stop()

# Scene Instructions
st.markdown("### 🕌 Scene Instructions")
user_prompt = st.text_area(
    "Describe the video you want to generate:",
    value="A cinematic 3D animation of a glowing Ramadan lantern sitting on a prayer mat inside a beautiful mosque, dust particles floating in the warm light, hyper-realistic, 4k resolution.",
    height=120
)

if st.button("🎬 IGNITE VIDEO RENDER"):
    if not user_prompt.strip():
        st.warning("⚠️ Prompt buffer empty. Please provide descriptive instructions.")
    else:
        with st.spinner("⏳ Compiling cinematic arrays... (Free servers take 1-3 minutes to render. Hang tight!)"):
            try:
                # Set up standard HTTP endpoint routing to completely avoid the 400 Client error
                API_URL = f"https://api-inference.huggingface.co/models/{model_choice}"
                headers = {"Authorization": f"Bearer {HF_TOKEN}"}
                payload = {"inputs": user_prompt}
                
                # Request generation
                response = requests.post(API_URL, headers=headers, json=payload)
                
                # Check if the model is sleeping (503 Error). If so, wait for it to heat up.
                if response.status_code == 503:
                    st.info("🔄 Server is booting up from sleep mode. Retrying connection in 15 seconds...")
                    time.sleep(15)
                    response = requests.post(API_URL, headers=headers, json=payload)
                
                if response.status_code == 200:
                    video_bytes = response.content
                    
                    st.success("✨ Cinematic rendering completed successfully!")
                    
                    # Display video player layout
                    st.video(video_bytes)
                    
                    # Provide immediate download button
                    st.download_button(
                        label="💾 DOWNLOAD MP4 BLUEPRINT",
                        data=video_bytes,
                        file_name="johnny_tec_cinematic.mp4",
                        mime="video/mp4"
                    )
                else:
                    st.error(f"Render engine returned status code: {response.status_code}")
                    st.text(response.text)
                    
            except Exception as rendering_anomaly:
                st.error(f"Render engine anomaly detected: {rendering_anomaly}")
                st.info("⚠️ Free video servers are often busy. If it fails, wait 30 seconds and click Ignite again!")
