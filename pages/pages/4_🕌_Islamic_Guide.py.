"""
JOHNNY TEC — ISLAMIC GUIDANCE HUB
====================================================
Features: Interactive Tasbih Counter, Daily Reminders, 
Prayer Time Tracker, and Spiritual Knowledge Base.
"""

import streamlit as st
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Islamic Guide Hub", page_icon="🕌", layout="wide")

# --- CUSTOM CYBER-ISLAMIC CSS ---
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        color: #00FFCC;
        text-shadow: 0 0 10px #00FFCC, 0 0 20px #00FFCC;
        margin-bottom: 30px;
    }
    .crypto-card {
        background-color: #111525;
        border: 1px solid #00FFCC;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0px 0px 15px rgba(0, 255, 204, 0.1);
    }
    .hadith-text {
        font-style: italic;
        color: #E0E0E0;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    .hadith-ref {
        color: #00FFCC;
        text-align: right;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE FOR TASBIH ---
if "tasbih_count" not in st.session_state:
    st.session_state.tasbih_count = 0
if "current_dhikr" not in st.session_state:
    st.session_state.current_dhikr = "SubhanAllah (Glory be to Allah)"

# --- MAIN HEADER ---
st.markdown("<h1 class='main-title'>◢ 🕌 ISLAMIC SPIRITUAL MATRIX ◣</h1>", unsafe_allow_html=True)

# --- TOP ROW: DAILY REMINDER & TASBIH COUNTER ---
col1, col2 = st.columns([5, 4])

with col1:
    st.markdown("""
    <div class='crypto-card'>
        <h3 style='color: #00FFCC; margin-top:0;'>📖 SPIRITUAL REMINDER</h3>
        <p class='hadith-text'>"The best remembrance is 'La ilaha illa Allah' (There is no god but Allah), and the best supplication is 'Alhamdulillah' (All praise is due to Allah)."</p>
        <div class='hadith-ref'>— Sunan al-Tirmidhi</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<div class='crypto-card'>", unsafe_allow_html=True)
    st.subheader("📿 Digital Tasbih Counter")
    
    # Dhikr Selection
    dhikr_options = [
        "SubhanAllah (Glory be to Allah)",
        "Alhamdulillah (Praise be to Allah)",
        "Allahu Akbar (Allah is the Greatest)",
        "Astaghfirullah (I seek forgiveness from Allah)"
    ]
    st.session_state.current_dhikr = st.selectbox("Choose Dhikr Focus:", dhikr_options)
    
    # Display & Increment Button
    st.metric(label=f"Current Focus Count", value=st.session_state.tasbih_count)
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("✨ TAP TO DHIKR", use_container_width=True):
            st.session_state.tasbih_count += 1
            st.rerun()
    with btn_col2:
        if st.button("🔄 RESET", use_container_width=True):
            st.session_state.tasbih_count = 0
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- MIDDLE ROW: PRAYER METRICS (SIERRA LEONE ZONE) ---
st.markdown("### ⏰ SOLAT TIME ENGINE (Freetown Zone)")
p_col1, p_col2, p_col3, p_col4, p_col5 = st.columns(5)

# Beautiful modular metrics for prayer tracking
p_col1.metric("FAJR", "05:14 AM", "Next", delta_color="inverse")
p_col2.metric("DHUHR", "12:45 PM", "Active")
p_col3.metric("ASR", "04:10 PM", "Pending")
p_col4.metric("MAGHRIB", "07:12 PM", "Pending")
p_col5.metric("ISHA", "08:30 PM", "Pending")

st.divider()

# --- BOTTOM ROW: THE 5 PILLARS EXPLORER ---
st.markdown("### 🛡️ Core Infrastructure: The 5 Pillars of Islam")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "☝️ 1. Shahada", 
    "🧎 2. Salah", 
    "🌾 3. Zakat", 
    "🌙 4. Sawm", 
    "🕋 5. Hajj"
])

with tab1:
    st.markdown("#### **The Declaration of Faith**")
    st.info("*\"La ilaha illa Allah, Muhammadun rasul Allah\"* — Believing and declaring that there is no god worthy of worship except Allah, and Muhammad is His final messenger.")

with tab2:
    st.markdown("#### **The Five Daily Prayers**")
    st.success("Establishing the continuous connection with the Creator 5 times a day: Fajr, Dhuhr, Asr, Maghrib, and Isha.")

with tab3:
    st.markdown("#### **Almsgiving / Charity**")
    st.warning("The obligation to give 2.5% of one's accumulated wealth annually to help the poor, purifying your earnings.")

with tab4:
    st.markdown("#### **Fasting in Ramadan**")
    st.error("Abstaining from food, drink, and bad habits from dawn until sunset during the holy month to build self-restraint (Taqwa).")

with tab5:
    st.markdown("#### **The Pilgrimage**")
    st.info("The sacred journey to the Holy Kaaba in Makkah once in a lifetime, for those who are physically and financially capable.")

# --- FOOTER ---
st.markdown("<br><p style='text-align: center; color: #555;'>JOHNNY TEC OS v2.6 // Dedicated to Spiritual Growth</p>", unsafe_allow_html=True)
