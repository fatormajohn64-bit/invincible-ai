"""
🏠_Home.py
====================
The central command console for the Invincible 911 Web Ecosystem.
Acts as the root entry point for a premium, multipage Streamlit environment.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# GLOBAL PAGE INITIALIZATION
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Command Center",
    page_icon="🏠",
    layout="centered",
)

# ---------------------------------------------------------------------------
# DESIGN TOKENS & TYPOGRAPHY STYLE (Unified Theme)
# ---------------------------------------------------------------------------
INK        = "#0A0E14"   # Page background
SURFACE    = "#12161F"   # Container layout background
SURFACE_2  = "#191E2A"   # Interactive surfaces
LINE       = "#242938"   # High-definition borders
TEXT       = "#E7EAF0"   # Primary text color
MUTED      = "#7C879C"   # Sub-labels / descriptions
SIGNAL     = "#28E0C4"   # Glowing accent cyan

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

    /* Main Welcome Panel */
    .hero-panel {{
        background: {SURFACE};
        border: 1px solid {LINE};
        border-radius: 16px;
        padding: 32px;
        margin-bottom: 24px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }}

    .hero-title {{
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 8px;
    }}

    .hero-subtitle {{
        color: {MUTED};
        font-size: 1rem;
        max-width: 500px;
        margin: 0 auto 16px auto;
        line-height: 1.5;
    }}

    /* Grid Module Blocks */
    .module-card {{
        background: {SURFACE_2};
        border: 1px solid {LINE};
        border-radius: 12px;
        padding: 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }}
    .module-card:hover {{
        border-color: {SIGNAL};
        transform: translateY(-2px);
    }}

    .module-header {{
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 6px;
    }}

    .module-desc {{
        color: {MUTED};
        font-size: 0.85rem;
        line-height: 1.4;
        margin-bottom: 12px;
    }}

    .status-indicator {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: {SIGNAL};
        text-transform: uppercase;
        letter-spacing: 0.05em;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }}

    .status-dot {{
        width: 6px;
        height: 6px;
        background-color: {SIGNAL};
        border-radius: 50%;
        box-shadow: 0 0 8px {SIGNAL};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# MAIN HERO INTERFACE VIEW
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="hero-panel">
        <div class="hero-title">⚡ Invincible 911 Engine</div>
        <div class="hero-subtitle">
            Welcome to your master workspace layout. Access your live tracking systems and data telemetry nodes from the control options below.
        </div>
        <div class="status-indicator">
            <span class="status-dot"></span> Core Systems Nominal
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("### 🎛️ Quick Navigation Core")
st.caption("Select a control element array or jump directly into tracking operations:")

# ---------------------------------------------------------------------------
# RE-ROUTING COLUMNS MATRIX
# ---------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="module-card">
            <div class="module-header">⚽ Live Scores</div>
            <div class="module-desc">
                High-fidelity global football tracking engine displaying live matches, results, and tactical win probability models.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Native Streamlit navigation component action
    if st.button("Launch Sports Radar →", use_container_width=True):
        st.switch_page("pages/1_⚽_Live_Scores.py")

with col2:
    st.markdown(
        """
        <div class="module-card">
            <div class="module-header">☁️ Weather Station</div>
            <div class="module-desc">
                Real-time atmospheric control deck providing hyper-local telemetry, UV indicators, and live environmental radar overlays.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Native Streamlit navigation component action
    if st.button("Launch Climate Monitor →", use_container_width=True):
        st.switch_page("pages/2_☁️_Weather.py")

# ---------------------------------------------------------------------------
# CONTROL FOOTER FRAME
# ---------------------------------------------------------------------------
st.divider()
with st.sidebar:
    st.markdown("### 🎚️ Main Console")
    st.caption("Active Session Context Node")
    st.info("💡 **Pro-Tip:** Use the workspace sidebar links to seamlessly shift views between modules without losing internal application operational cache.")
