"""
2_☁️_Weather.py
====================
Premium, glowing dark-themed weather telemetry control room powered by WeatherAPI.com.
Upgraded with global temperature tracking extremes and automated weather news streams.
"""

import requests
import streamlit as st
from datetime import datetime

# ---------------------------------------------------------------------------
# PAGE SYSTEM CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Weather Station",
    page_icon="☁️",
    layout="wide"
)

WEATHER_API_KEY = st.secrets.get("WEATHER_API_KEY", None)
NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", None)

# ---------------------------------------------------------------------------
# COUNTRY NODE DIRECTORY
# ---------------------------------------------------------------------------
COUNTRIES = {
    "🇸🇱 Sierra Leone": "Freetown",
    "🇬🇧 United Kingdom": "London",
    "🇺🇸 United States": "New York",
    "🇫🇷 France": "Paris",
    "🇯🇵 Japan": "Tokyo",
    "🇪🇬 Egypt": "Cairo",
    "🇳🇬 Nigeria": "Lagos",
    "🇬🇭 Ghana": "Accra",
    "🇿🇦 South Africa": "Cape Town",
    "🇰🇪 Kenya": "Nairobi",
    "🇸🇦 Saudi Arabia": "Riyadh",
    "🇦🇪 UAE": "Dubai",
    "🇹🇷 Turkey": "Istanbul",
    "🇮🇳 India": "New Delhi",
    "🇵🇰 Pakistan": "Islamabad",
    "🇧🇩 Bangladesh": "Dhaka",
    "🇮🇩 Indonesia": "Jakarta",
    "🇲🇾 Malaysia": "Kuala Lumpur",
    "🇨🇳 China": "Beijing",
    "🇰🇷 South Korea": "Seoul",
    "🇩🇪 Germany": "Berlin",
    "🇪🇸 Spain": "Madrid",
    "🇮🇹 Italy": "Rome",
    "🇳🇱 Netherlands": "Amsterdam",
    "🇨🇦 Canada": "Toronto",
    "🇧🇷 Brazil": "Rio de Janeiro",
    "🇲🇽 Mexico": "Mexico City",
    "🇦🇷 Argentina": "Buenos Aires",
    "🇦🇺 Australia": "Sydney",
    "🇷🇺 Russia": "Yakutsk",
}

# ---------------------------------------------------------------------------
# PREMIUM CYBERPUNK COLOR SYSTEM
# ---------------------------------------------------------------------------
INK = "#030508"
SURFACE = "#0B0F19"
SURFACE_2 = "#121826"
LINE = "rgba(0, 240, 255, 0.2)"
TEXT = "#F1F4FA"
MUTED = "#7C879C"

def temp_mood(temp_c: float):
    if temp_c < 5: return "Freezing", "🥶", "#00F0FF", 0.05
    elif temp_c < 15: return "Cold", "❄️", "#3A86FF", 0.25
    elif temp_c < 25: return "Mild", "😌", "#39FF14", 0.50
    elif temp_c < 35: return "Hot", "🌤️", "#FFB703", 0.75
    else: return "Scorching", "🔥", "#FF0055", 0.95

# Injecting Global Cyberpunk Layout
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@500&display=swap');
    
    .stApp {{ background: {INK}; }}
    section[data-testid="stSidebar"] {{
        background: {SURFACE} !important;
        border-right: 1px solid {LINE} !important;
    }}
    h1, h2, h3 {{
        font-family: 'Space Grotesk', sans-serif !important;
        background: linear-gradient(90deg, #00F0FF 0%, #9D4EDD 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .weather-card {{
        background: {SURFACE_2};
        border: 1px solid var(--glow-color);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.1);
        margin-bottom: 25px;
    }}
    .extreme-box {{
        background: rgba(18, 24, 38, 0.8);
        border-radius: 12px;
        padding: 15px;
        border: 1px solid {LINE};
        text-align: center;
    }}
    .telemetry-item {{
        background: {SURFACE};
        border: 1px solid {LINE};
        padding: 12px;
        border-radius: 10px;
        text-align: center;
    }}
    .meter-track {{
        position: relative; height: 8px; border-radius: 4px; margin-top: 20px;
        background: linear-gradient(90deg, #00F0FF, #39FF14, #FFB703, #FF0055);
    }}
    .meter-marker {{
        position: absolute; top: -5px; width: 18px; height: 18px; border-radius: 50%;
        background: {TEXT}; border: 3px solid var(--glow-color); transform: translateX(-50%);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------------
# GLOBAL RADAR EXTREMES LOCATOR
# ---------------------------------------------------------------------------
@st.cache_data(ttl=1800)
def fetch_global_extremes():
    if not WEATHER_API_KEY:
        return {"hottest": ("Dubai", 41.2), "coldest": ("Yakutsk", -32.5)}
    
    highest_temp = -999.0
    lowest_temp = 999.0
    hottest_city = "Unknown"
    coldest_city = "Unknown"
    
    # Sample a rapid strategic subnet checklist of extreme key nodes
    check_nodes = ["Yakutsk", "London", "Cairo", "Dubai", "Freetown", "Toronto", "Riyadh", "Sydney"]
    for node in check_nodes:
        try:
            r = requests.get(f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={node}", timeout=4)
            if r.status_code == 200:
                val = r.json().get("current", {}).get("temp_c", 0.0)
                if val > highest_temp:
                    highest_temp = val
                    hottest_city = node
                if val < lowest_temp:
                    lowest_temp = val
                    coldest_city = node
        except:
            continue
    return {"hottest": (hottest_city, highest_temp), "coldest": (coldest_city, lowest_temp)}

# ---------------------------------------------------------------------------
# INTERACTIVE DATA CONTROLLERS
# ---------------------------------------------------------------------------
st.title("⚡ Telemetry Weather Core")
st.caption("High-fidelity environmental monitoring data feeds.")

# Fetch extremes data early for main panel assembly layout
extremes = fetch_global_extremes()

# Sidebar Setup
with st.sidebar:
    st.markdown("### 🗺️ Navigation Hub")
    selection = st.selectbox("Select Station Node", options=list(COUNTRIES.keys()) + ["🔍 Custom Search..."])
    city = st.text_input("Target Input", "Freetown") if selection == "🔍 Custom Search..." else COUNTRIES[selection]
    unit_toggle = st.radio("Display Metric System", ["°C", "°F"], horizontal=True)

# Main Grid Layout split into Data Engine Frame & Real-Time Weather News
col_main, col_news = st.columns([2, 1])

with col_main:
    if not WEATHER_API_KEY:
        st.info("🔌 Core API running in simulation framework mode.")
        temp_c, feelslike_c, humidity, wind_kph, uv, cond_text, icon = 28.0, 32.0, 80, 12, 6.0, "Partly Cloudy", "https://cdn.weatherapi.com/weather/64x64/day/116.png"
        city_name, country, local_time = "Freetown", "Sierra Leone", "12:00 PM"
    else:
        try:
            res = requests.get(f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}", timeout=10)
            data = res.json()
            loc = data["location"]
            cur = data["current"]
            city_name, country, local_time = loc["name"], loc["country"], loc["localtime"]
            temp_c, feelslike_c, humidity, wind_kph, uv = cur["temp_c"], cur["feelslike_c"], cur["humidity"], cur["wind_kph"], cur["uv"]
            cond_text = cur["condition"]["text"]
            icon = "https:" + cur["condition"]["icon"] if cur["condition"]["icon"].startswith("//") else cur["condition"]["icon"]
        except Exception as e:
            st.error(f"Fault parsing tracking metrics data stream: {e}")
            st.stop()

    # Apply Conversion Logic if Requested
    t_val = round(temp_c * 9/5 + 32, 1) if unit_toggle == "°F" else temp_c
    f_val = round(feelslike_c * 9/5 + 32, 1) if unit_toggle == "°F" else feelslike_c
    lbl = "°F" if unit_toggle == "°F" else "°C"
    
    mood_lbl, mood_emoji, color, position = temp_mood(temp_c)

    # Core Telemetry Visual Card Output
    st.markdown(
        f"""
        <div class="weather-card" style="--glow-color: {color};">
            <div style="font-family:'JetBrains Mono'; font-size:0.75rem; color:{color}; letter-spacing:2px;">SYS_NODE_ACTIVE // TIME: {local_time}</div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top:15px;">
                <div>
                    <h2 style="margin:0; font-size:2.2rem;">{city_name}, {country}</h2>
                    <div style="font-size:3.5rem; font-weight:700; margin:10px 0; text-shadow: 0 0 15px {color};">{t_val}{lbl}</div>
                    <div style="color:{TEXT}; font-size:1.1rem; font-weight:500;">Feels like {f_val}{lbl} &bull; {cond_text}</div>
                    <span class="mood-badge" style="border: 1px solid {color}; padding:4px 12px; border-radius:20px; font-size:0.85rem; color:{TEXT}; box-shadow: 0 0 10px {color};">{mood_emoji} {mood_lbl}</span>
                </div>
                <img src="{icon}" style="width:110px; height:110px; filter: drop-shadow(0 0 12px {color});">
            </div>
            <div class="telemetry-grid" style="display:grid; grid-template-columns: repeat(3, 1fr); gap:15px; margin-top:25px;">
                <div class="telemetry-item"><div style="font-size:0.7rem; color:{MUTED}; font-family:'JetBrains Mono';">💧 HUMIDITY</div><div style="font-size:1.2rem; font-weight:700; color:{TEXT};">{humidity}%</div></div>
                <div class="telemetry-item"><div style="font-size:0.7rem; color:{MUTED}; font-family:'JetBrains Mono';">💨 WIND FLOW</div><div style="font-size:1.2rem; font-weight:700; color:{TEXT};">{wind_kph} kph</div></div>
                <div class="telemetry-item"><div style="font-size:0.7rem; color:{MUTED}; font-family:'JetBrains Mono';">☀️ ULTRAVIOLET</div><div style="font-size:1.2rem; font-weight:700; color:{TEXT};">{uv}</div></div>
            </div>
            <div class="meter-track"><div class="meter-marker" style="left:{position*100}%; --glow-color:{color};"></div></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Global Extreme Nodes Render Section
    st.write("### 🌋 Planetary Thermal Extremes")
    c_hot, c_cold = st.columns(2)
    with c_hot:
        st.markdown(
            f'<div class="extreme-box" style="border-color:#FF0055;"><div style="color:#FF0055; font-size:0.8rem; font-weight:700;">🔥 HOTTEST STATION RECORDED</div>'
            f'<div style="font-size:1.4rem; font-weight:700; margin:5px 0;">{extremes["hottest"][0]}</div>'
            f'<div style="color:{MUTED}; font-size:1.1rem;">{extremes["hottest"][1]}°C</div></div>', 
            unsafe_allow_html=True
        )
    with c_cold:
        st.markdown(
            f'<div class="extreme-box" style="border-color:#00F0FF;"><div style="color:#00F0FF; font-size:0.8rem; font-weight:700;">🥶 COLDEST STATION RECORDED</div>'
            f'<div style="font-size:1.4rem; font-weight:700; margin:5px 0;">{extremes["coldest"][0]}</div>'
            f'<div style="color:{MUTED}; font-size:1.1rem;">{extremes["coldest"][1]}°C</div></div>', 
            unsafe_allow_html=True
        )

# ---------------------------------------------------------------------------
# REAL-TIME METEOROLOGICAL NEWS ENGINE
# ---------------------------------------------------------------------------
with col_news:
    st.write("### 📰 Climate News Feed")
    
    if not NEWS_API_KEY:
        st.info("Missing `NEWS_API_KEY` token secret. Displaying simulated data updates.")
        mock_stories = [
            ("Severe heat wave warning issued across parts of regional global centers.", "Meteorologists track shifting high pressure zones."),
            ("Global weather satellites track unusual atmospheric system development.", "Low pressure anomalies bring storms inland.")
        ]
        for title, desc in mock_stories:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.caption(desc)
    else:
        try:
            # Query News API specifically targeting weather & environmental dynamics
            news_url = f"https://newsapi.org/v2/everything?q=weather+climate&pageSize=4&apiKey={NEWS_API_KEY}"
            news_res = requests.get(news_url, timeout=5).json()
            articles = news_res.get("articles", [])
            
            if not articles:
                st.caption("No recent telemetry broadcast bulletins discovered.")
            for art in articles:
                with st.container(border=True):
                    st.markdown(f"**[{art['title']}]({art['url']})**")
                    st.write(f"<span style='color:{MUTED}; font-size:0.85rem;'>{art.get('description','')[:120]}...</span>", unsafe_allow_html=True)
        except Exception as e:
            st.caption("News data feed processing currently unavailable.")
    
