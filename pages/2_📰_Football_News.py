"""
3_📰_News.py
====================
Premium Cyberpunk Football News Room powered by NewsData.io.
Features live tracking, glowing UI, league filters, and deep-read expanders.
"""

import streamlit as st
import requests

# ---------------------------------------------------------------------------
# PAGE SYSTEM CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Invincible 911 Football News", 
    page_icon="⚽", 
    layout="wide"
)

NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", None)

# ---------------------------------------------------------------------------
# PREMIUM CYBERPUNK UI & GLOW INJECTIONS
# ---------------------------------------------------------------------------
# Color Palette
INK = "#030508"
SURFACE = "#0B0F19"
SURFACE_2 = "#121826"
CYAN = "#00F0FF"
VIOLET = "#9D4EDD"
LIVE_RED = "#FF0055"
TEXT = "#F1F4FA"
MUTED = "#7C879C"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@500&display=swap');
    
    .stApp {{
        background: {INK};
    }}
    
    h1, h2, h3 {{
        font-family: 'Space Grotesk', sans-serif !important;
        color: {TEXT} !important;
    }}
    
    .glow-title {{
        background: linear-gradient(90deg, {CYAN} 0%, {VIOLET} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 700;
        margin-bottom: 0;
    }}
    
    /* Pulsating Live Badge */
    @keyframes pulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(255, 0, 85, 0.7); }}
        70% {{ box-shadow: 0 0 0 10px rgba(255, 0, 85, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(255, 0, 85, 0); }}
    }}
    
    .live-badge {{
        background-color: {LIVE_RED};
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        font-weight: bold;
        letter-spacing: 1px;
        animation: pulse 2s infinite;
        display: inline-block;
        margin-bottom: 20px;
    }}

    .news-card {{
        background: {SURFACE_2};
        border: 1px solid {VIOLET};
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(157, 78, 221, 0.2);
        margin-bottom: 20px;
        transition: transform 0.2s, box-shadow 0.2s;
    }}
    
    .news-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.4);
        border-color: {CYAN};
    }}
    
    .source-tag {{
        font-family: 'JetBrains Mono', monospace;
        color: {CYAN};
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    /* Expander override for seamless integration */
    div[data-testid="stExpander"] {{
        background-color: {SURFACE} !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        border-radius: 8px !important;
    }}
    div[data-testid="stExpander"] p {{
        color: {TEXT} !important;
        font-size: 1rem !important;
        line-height: 1.6;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------------
# HEADER & BRANDING
# ---------------------------------------------------------------------------
# Using columns to place the Barcelona Logo next to the Title
head_col1, head_col2 = st.columns([1, 8])

with head_col1:
    # High-quality transparent FC Barcelona logo
    st.markdown(
        """<img src="https://upload.wikimedia.org/wikipedia/en/thumb/4/47/FC_Barcelona_%28crest%29.svg/1200px-FC_Barcelona_%28crest%29.svg.png" width="100" style="filter: drop-shadow(0 0 15px rgba(157, 78, 221, 0.5));">""",
        unsafe_allow_html=True
    )

with head_col2:
    st.markdown('<div class="glow-title">Invincible 911 News Room</div>', unsafe_allow_html=True)
    st.markdown('<div class="live-badge">🔴 LIVE BROADCAST</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# GLOBAL RADAR & LEAGUE FILTER
# ---------------------------------------------------------------------------
st.markdown("### 📡 Select Intel Channel")

# Dictionary mapping friendly names to API search queries
LEAGUES = {
    "🌍 Global Football": "football",
    "🇪🇸 La Liga & Barça": "barcelona OR la liga",
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League": "premier league",
    "🏆 Champions League": "champions league",
    "🐐 Messi Watch": "lionel messi"
}

# Render filters horizontally
selected_category = st.radio(
    "Filter by League / Topic:",
    options=list(LEAGUES.keys()),
    horizontal=True,
    label_visibility="collapsed"
)

st.divider()

# ---------------------------------------------------------------------------
# CORE NEWS ENGINE
# ---------------------------------------------------------------------------
if not NEWS_API_KEY:
    st.warning("⚠️ Atmospheric Core API Key Missing")
    st.markdown("Enter your NewsData.io API key in Streamlit secrets to activate the live feed.")
    
    st.markdown("### 🏆 Top Headlines (Simulation Feed)")
    st.markdown(
        f"""
        <div class="news-card">
            <div class="source-tag">GLOBAL SPORTS NETWORK • RECENTLY</div>
            <h3 style="margin-top: 5px; color: {TEXT};">Messi Secures Another Magical Victory</h3>
            <p style="color: {MUTED};">An incredible performance tonight kept fans on their feet as the football legend secured a brilliant brace...</p>
        </div>
        """, unsafe_allow_html=True
    )
else:
    try:
        url = "https://newsdata.io/api/1/latest"
        search_query = LEAGUES[selected_category]
        
        params = {
            "apikey": NEWS_API_KEY,
            "q": search_query,
            "category": "sports",
            "language": "en",
            "image": 1 # Request articles with images where possible
        }
        
        # Displaying a loading spinner with a custom message
        with st.spinner(f"Intercepting live data for {selected_category}..."):
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            articles = data.get("results", [])
        
        if not articles:
            st.info(f"No recent transmissions found for {selected_category}. Try another channel.")
        else:
            # Render articles using Streamlit columns for a grid layout
            cols = st.columns(2)
            
            for index, article in enumerate(articles):
                title = article.get("title", "Encrypted Title")
                description = article.get("description", "No detailed transmission available.")
                content = article.get("content", description) # Use full content if available, fallback to description
                source = article.get("source_id", "Unknown Source")
                pub_date = article.get("pubDate", "")
                link = article.get("link", "#")
                image_url = article.get("image_url", None)
                
                # Distribute cards evenly across the two columns
                with cols[index % 2]:
                    # Create the glowing card container using pure HTML/CSS injection
                    st.markdown(f'<div class="news-card">', unsafe_allow_html=True)
                    
                    if image_url:
                        st.image(image_url, use_container_width=True)
                    
                    st.markdown(f'<div class="source-tag">{source} • {pub_date}</div>', unsafe_allow_html=True)
                    st.markdown(f'<h3 style="margin-top: 8px;">{title}</h3>', unsafe_allow_html=True)
                    
                    # Provide a short snippet for scannability
                    short_desc = description[:150] + "..." if description and len(description) > 150 else description
                    st.write(f"<span style='color:{MUTED};'>{short_desc}</span>", unsafe_allow_html=True)
                    
                    # The Deep-Dive Expander (Requirement #1: Read more and understand)
                    with st.expander("📖 Read Full Intel Report"):
                        if content and content != "None":
                            st.write(content)
                        else:
                            st.write("Detailed text not provided by the publisher API.")
                        
                        st.link_button("Access Original Database ➡️", link)
                        
                    st.markdown('</div>', unsafe_allow_html=True)
                    
    except Exception as e:
        st.error(f"Signal disruption in the news matrix: {e}")

st.divider()
if st.button("🔄 Sync Latest Transmissions", type="primary", use_container_width=True):
    st.rerun()
             
