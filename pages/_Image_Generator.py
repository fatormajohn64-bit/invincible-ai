"""
pages/1_🎨_Image_Generator.py
============================================================
JOHNNY TEC PROGRAMMING LAB - VISUAL IMAGING MATRIX
Runs completely free using Hugging Face Serverless Inference
"""

import streamlit as st
import os
from huggingface_hub import InferenceClient
from io import BytesIO
from PIL import Image

# ---------------------------------------------------------------------------
# 1. PAGE CONFIG & MATRIX STYLING
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Visual Imaging Matrix", page_icon="🎨", layout="wide")

INK = "#020408"
SURFACE = "#070C16"
CYAN = "#00F0FF"
MATRIX = "#22C55E"
TEXT = "#F8FAFC"
MUTED = "#64748B"
HOT_PINK = "#F43F5E"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=JetBrains+Mono:wght@500&display=swap');
    .stApp {{ background: {INK}; }}
    h1, h2, h3 {{ font-family: 'Orbitron', sans-serif !important; color: {TEXT} !important; }}
    
    .imaging-title {{
        background: linear-gradient(90deg, {CYAN} 0%, {HOT_PINK} 100%);
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
    </style>
    """,
    unsafe_allow_html=True
)

# Authenticate with Hugging Face Serverless Core
HF_TOKEN = st.secrets.get("HF_TOKEN", os.environ.get("HF_TOKEN", ""))

# ---------------------------------------------------------------------------
# 2. SIDEBAR RENDERING CONTROLS
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧬 Imaging Models")
    model_choice = st.selectbox(
        "Select Generative Core",
        [
            "black-forest-labs/FLUX.1-dev",
            "stabilityai/stable-diffusion-xl-base-1.0"
        ]
    )
    st.divider()
    st.markdown("💡 *Tip: FLUX.1 handles high-fidelity graphics and text extremely well, while SDXL is great for broad, artistic concepts.*")

# ---------------------------------------------------------------------------
# 3. INTERFACE HEADERS & IMAGING RUNTIME
# ---------------------------------------------------------------------------
st.markdown('<div class="imaging-title">VISUAL IMAGING MATRIX</div>', unsafe_allow_html=True)
st.markdown('<div class="status-ticker">● QUANTUM RENDER PIPELINE // FREE OPEN-SOURCE HUB ACTIVE</div>', unsafe_allow_html=True)

if not HF_TOKEN:
    st.error("Execution Interrupted: `HF_TOKEN` secret configuration is missing in Streamlit.")
    st.stop()

# Prompt Entry Interface
user_prompt = st.text_area(
    "Inject Visual Prompt Instructions...",
    placeholder="Example: A futuristic gaming setup with neon cyan and hot pink lighting, cybernetic monitors showing terminal code, hyper-realistic, 8k resolution..."
)

if st.button("🚀 IGNITE QUANTUM RENDER"):
    if not user_prompt.strip():
        st.warning("Prompt buffer empty. Please provide descriptive instructions before starting deployment.")
    else:
        with st.spinner("Compiling multi-dimensional data arrays... (This may take a moment on first model initialization)"):
            try:
                # Initialize Serverless Client Routing
                client = InferenceClient(api_key=HF_TOKEN)
                
                # Fetch generated image from open source inference provider
                generated_raw_image = client.text_to_image(
                    prompt=user_prompt,
                    model=model_choice
                )
                
                # Render to Interface layout
                st.success("Visual manifestation completed successfully!")
                st.image(generated_raw_image, caption=f"Manifestation Pipeline: {model_choice}", use_column_width=True)
                
                # Provide an instant download array pipeline
                buffer = BytesIO()
                generated_raw_image.save(buffer, format="PNG")
                byte_data = buffer.getvalue()
                
                st.download_button(
                    label="💾 EXTRACT BLUEPRINT (DOWNLOAD PNG)",
                    data=byte_data,
                    file_name="johnny_tec_manifestation.png",
                    mime="image/png"
                )
                
            except Exception as rendering_anomaly:
                st.error(f"Render engine anomaly detected: {rendering_anomaly}")
                st.info("Note: Free models sometimes fall asleep. If it mentions a 503 error, wait 10 seconds and try again while the engine warms up!")
                
