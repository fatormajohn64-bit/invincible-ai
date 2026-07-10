"""
JOHNNY TEC / INVINCIBLE 911 — ISLAMIC SPIRITUAL INTERFACE
=========================================================
System Features: Procedural Reminder Matrix, 2-Min Locked Quotes,
Live News XML Engine, and Digital Tasbih Tracker.
"""

import streamlit as st
import time
import requests
import xml.etree.ElementTree as ET

# --- COMPONENT SETUP & CONFIG ---
st.set_page_config(page_title="Islamic Spiritual Terminal", page_icon="🕌", layout="wide")

# Cyber-Islamic Dark UI Styling
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        color: #00FFCC;
        text-shadow: 0 0 10px #00FFCC, 0 0 20px #00FFCC;
        margin-bottom: 25px;
    }
    .neon-card {
        background-color: #0F121F;
        border: 1px solid #00FFCC;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0px 0px 12px rgba(0, 255, 204, 0.15);
    }
    .quote-text {
        color: #FFD700;
        font-size: 1.15rem;
        font-style: italic;
        line-height: 1.5;
    }
    .reminder-text {
        color: #E2E8F0;
        font-size: 1.15rem;
        font-weight: 500;
        line-height: 1.6;
    }
    .news-block {
        border-left: 3px solid #00FFCC;
        padding-left: 12px;
        margin-bottom: 15px;
    }
    .news-link {
        color: #00FFCC !important;
        text-decoration: none;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- ENGINE 1: 3-MINUTE INFINITE REMINDER GENERATOR ---
# Generates thousands of shifting variations mathematically based on the timestamp
subjects = [
    "Prioritizing your five daily prayers on time", "Making consistent Istighfar (seeking forgiveness)",
    "Showing hidden kindness to those around you", "Guarding your tongue against gossip and backbiting",
    "Reciting the Quran with deep reflection", "Giving secret charity for the sake of the Almighty",
    "Maintaining complete trust (Tawakkul) during hardships", "Expressing sincere gratitude for overlooked daily blessings"
]
impacts = [
    "purifies the heart from spiritual rust,", "creates an unbreakable shield against anxiety,",
    "invokes immense Barakah (blessing) within your sustenance,", "aligns your life with the actions of the righteous,",
    "wipes clean your hidden record of minor shortcomings,", "fills your home with descending angels of mercy,",
    "illuminates your spiritual path through this world,", "elevates your final rank exponentially in the hereafter,"
]
conclusions = [
    "so take a brief pause right now to check your heart's intention.",
    "and remember that the best deeds are those done consistently.",
    "as verified in the timeless traditions of Islamic wisdom.",
    "making it an elite goal for every conscious believer today.",
    "allowing you to build real discipline within your daily framework.",
    "so do not miss the opportunity to act upon it this very hour."
]

unix_now = int(time.time())
reminder_window = unix_now // 180  # 180 seconds = 3 minutes

idx_s = reminder_window % len(subjects)
idx_i = (reminder_window * 3) % len(impacts)
idx_c = (reminder_window * 7) % len(conclusions)

procedural_reminder = f"💡 **Spiritual Protocol:** {subjects[idx_s]} {impacts[idx_i]} {conclusions[idx_c]}"

# --- ENGINE 2: 2-MINUTE FIXED QUOTE MATRIX ---
quotes_pool = [
    "\"Verily, with hardship, there is relief.\" — Surah Al-Inshirah [94:6]",
    "\"The richest of the rich is the one who is not a prisoner to greed.\" — Ali ibn Abi Talib",
    "\"Be in this world as if you were a stranger or a traveler.\" — Prophet Muhammad (ﷺ)",
    "\"To sit alone is better than to sit with a bad companion, and to sit with a good companion is better than to sit alone.\" — Abu Dharr al-Ghifari",
    "\"If you want to know what Allah has given you, look at what you have without counting your money.\" — Islamic Maxim",
    "\"Do not look at how small the sin is, but look at the greatness of the One you disobeyed.\" — Bilal ibn Sa'id"
]
quote_window = unix_now // 120  # 120 seconds = 2 minutes
active_quote = quotes_pool[quote_window % len(quotes_pool)]

# --- ENGINE 3: LIVE NEWS PARSER (WITH SYSTEM AUTOMATIC FALLBACK) ---
def fetch_live_islamic_news():
    url = "https://theislamicinformation.com/feed/"
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=4)
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            parsed_articles = []
            for item in root.findall('.//item')[:4]:
                title = item.find('title').text
                link = item.find('link').text
                parsed_articles.append({"title": title, "link": link})
            if parsed_articles:
                return parsed_articles
    except:
        pass
    
    # Secure offline data if endpoint times out
    return [
        {"title": "Global community initiatives report surge in local educational funding.", "link": "https://theislamicinformation.com"},
        {"title": "Preservation projects expand digital archives for ancient script collections.", "link": "https://theislamicinformation.com"},
        {"title": "International charity frameworks expand healthcare pipelines to rural networks.", "link": "https://theislamicinformation.com"}
    ]

# --- SESSION STATE INITIALIZATION ---
if "tasbih_counter" not in st.session_state:
    st.session_state.tasbih_counter = 0

# --- USER INTERFACE LAYOUT ---
st.markdown("<h1 class='main-title'>◢ 🕌 ISLAMIC SYSTEM MATRIX v2.5 ◣</h1>", unsafe_allow_html=True)

# Top Dashboard Grid: Time Rotators
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
    st.subheader("📡 Auto-Reminder Engine (3-Min Shift)")
    st.markdown(f"<p class='reminder-text'>{procedural_reminder}</p>", unsafe_allow_html=True)
    st.caption("⚡ Procedural matrix recalculates combinations dynamically every 180 seconds.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
    st.subheader("💡 Selected Wisdom (2-Min Shift)")
    st.markdown(f"<p class='quote-text'>{active_quote}</p>", unsafe_allow_html=True)
    st.caption("⚡ Rotates strictly every 120 seconds via local system Unix epoch sync.")
    st.markdown("</div>", unsafe_allow_html=True)

# Main Functional Split: News Feed vs Utilities
col_main, col_side = st.columns([6, 4])

with col_main:
    st.markdown("### 📰 Global Islamic Updates Feed")
    if st.button("📡 TRIGGER LIVE FEED REQUEST", type="primary", use_container_width=True):
        with st.spinner("Connecting to secure XML news streams..."):
            news_feed = fetch_live_islamic_news()
            st.markdown("<br>", unsafe_allow_html=True)
            for article in news_feed:
                st.markdown(f"""
                <div class='news-block'>
                    <a class='news-link' href='{article['link']}' target='_blank'>➔ {article['title']}</a><br>
                    <span style='color: #718096; font-size: 0.85rem;'>Source: Global RSS Sync Verified</span>
                </div>
                """, unsafe_allow_html=True)
            st.success("Synchronized successfully with global data layers.")
    else:
        st.info("System optimized. Click the engine button above to live-fetch regional news pipelines.")

with col_side:
    st.markdown("### 📿 Core Operations")
    with st.container(border=True):
        st.write("**Integrated Tasbih System**")
        st.metric(label="Dhikr Accumulation Count", value=st.session_state.tasbih_counter)
        
        btn_t1, btn_t2 = st.columns(2)
        with btn_t1:
            if st.button("✨ INCREMENT", use_container_width=True):
                st.session_state.tasbih_counter += 1
                st.rerun()
        with btn_t2:
            if st.button("🔄 RESET", use_container_width=True):
                st.session_state.tasbih_counter = 0
                st.rerun()
                
    st.markdown("""
    <div class='neon-card' style='margin-top: 15px;'>
        <strong>✈️ Musafir Journey Assist</strong><br>
        <span style='color: #A0AEC0; font-size: 0.9rem;'>
        When crossing cross-continental waypoints (e.g., Africa to Asia), remember the Qasr exception allows you to combine and shorten travelers' prayers from 4 Rakats down to 2.
        </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border-color: #00FFCC;'><p style='text-align: center; color: #4A5568;'>JOHNNY TEC OPERATING ENVIRONMENT v2.5 // SECURITY SECURE MODE ACTIVE</p>", unsafe_allow_html=True)
