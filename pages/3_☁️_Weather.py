"""
2_☁️_Weather.py
====================
Premium, dark-themed weather telemetry control room powered by WeatherAPI.com.
Designed to integrate seamlessly into an elite multipage application ecosystem.

SETUP:
    Add to .streamlit/secrets.toml (or Streamlit Cloud secrets):
        WEATHER_API_KEY = "your-key-here"
"""

import requests
import streamlit as st

# ---------------------------------------------------------------------------
# PAGE SYSTEM CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Weather Station",
    page_icon="☁️",
    layout="centered"
)

WEATHER_API_KEY = st.secrets.get("WEATHER_API_KEY", None)

# ---------------------------------------------------------------------------
# PREMIUM UI STYLE TOKENS (Cyber Dark System)
# ---------------------------------------------------------------------------
INK        = "#0A0E14"   # Core background
SURFACE    = "#12161F"   # Container components
SURFACE_2  = "#191E2A"   # Inputs and panels
LINE       = "#242938"   # High-definition borders
TEXT       = "#E7EAF0"   # High-contrast typography
MUTED      = "#7C879C"   # Lower priority telemetry labels
SIGNAL     = "#28E0C4"   # Active accent cyan

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

    /* Card Wrapper Architecture */
    .weather-card {{
        background: {SURFACE};
        border: 1px solid {LINE};
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }}

    .location-sub {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: {SIGNAL};
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }}

    .temp-display {{
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 3.5rem;
        color: {TEXT};
        line-height: 1;
        margin: 10px 0;
    }}

    /* Custom Metric Matrix grid */
    .telemetry-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-top: 20px;
    }}

    .telemetry-item {{
        background: {SURFACE_2};
        border: 1px solid {LINE};
        padding: 12px;
        border-radius: 10px;
        text-align: center;
    }}

    .telemetry-label {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: {MUTED};
        text-transform: uppercase;
        margin-bottom: 4px;
    }}

    .telemetry-value {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: {TEXT};
    }}

    /* Form Inputs Overrides */
    div[data-testid="stTextInput"] input {{
        background-color: {SURFACE_2} !important;
        color: {TEXT} !important;
        border: 1px solid {LINE} !important;
        border-radius: 10px !important;
    }}
    
    div[data-testid="stSelectbox"] div[data-testid="stMarkdownContainer"] p {{
        color: {TEXT} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------------
# SIDEBAR CONTROL ROOM
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🗺️ Navigation Hub")
    st.caption("Select a telemetry node or launch deep radar search.")
    
    # Predefined quick-access locations layout
    quick_cities = [
        "Freetown", 
        "London", 
        "New York", 
        "Paris", 
        "Tokyo", 
        "Cairo",
        "🔍 Custom Search..."
    ]
    
    selection = st.selectbox(
        "Monitor Station Location",
        options=quick_cities,
        index=0
    )
    
    st.divider()
    st.caption("Telemetry feeds refresh dynamically on user location swapping.")

# Process final input query logic
if selection == "🔍 Custom Search...":
    city = st.text_input("🔍 Input target global city name:", value="Freetown")
else:
    city = selection

# ---------------------------------------------------------------------------
# INTERFACE MAIN COMPONENT VIEW
# ---------------------------------------------------------------------------
st.title("☁️ Invincible 911 Weather Station")
st.caption("Real-time high-fidelity atmospheric tracking and global condition analytics.")

if not WEATHER_API_KEY:
    st.warning("⚠️ Atmospheric Core API Key Missing")
    st.markdown(
        "To switch out of demo simulation mode and tap into live monitoring assets:\n"
        "1. Create a key layer index at **WeatherAPI.com**.\n"
        "2. Save inside your local deployment environment context settings as `WEATHER_API_KEY`."
    )
    
    st.markdown("---")
    st.markdown("### 🌆 Telemetry Station Frame (Simulation Mode)")
    
    # Mirror premium dashboard frame using hardcoded demo matrix points
    st.markdown(
        f"""
        <div class="weather-card">
            <div class="location-sub">SIMULATION FEED · LOCAL TIME: 15:36</div>
            <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 10px;">
                <div>
                    <h3 style='margin:0;'>Freetown, Sierra Leone</h3>
                    <div class="temp-display">28°C</div>
                    <div style="color: {SIGNAL}; font-weight: 500;">⛅ Partly Cloudy</div>
                </div>
                <img src="https://cdn.weatherapi.com/weather/64x64/day/116.png" style="width: 90px; height: 90px; filter: drop-shadow(0 0 8px rgba(40,224,196,0.2));">
            </div>
            <div class="telemetry-grid">
                <div class="telemetry-item">
                    <div class="telemetry-label">💧 Moisture</div>
                    <div class="telemetry-value">82%</div>
                </div>
                <div class="telemetry-item">
                    <div class="telemetry-label">💨 Air Velocity</div>
                    <div class="telemetry-value">14 kph</div>
                </div>
                <div class="telemetry-item">
                    <div class="telemetry-label">☀️ UV Index</div>
                    <div class="telemetry-value">5.0</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    if city:
        try:
            url = "https://api.weatherapi.com/v1/current.json"
            params = {"key": WEATHER_API_KEY, "q": city, "aqi": "no"}
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 400:
                st.error("❌ Specified location coordinates not found. Correct string syntax input.")
            elif response.status_code != 200:
                st.error(f"⚠️ Telemetry Data Fault System Code: {response.status_code}")
            else:
                data = response.json()
                
                # Metadata payload extraction
                loc = data.get("location", {})
                city_name = loc.get("name", "Unknown Node")
                country = loc.get("country", "")
                local_time = loc.get("localtime", "")
                
                # Metrics engine data parse
                current = data.get("current", {})
                temp_c = current.get("temp_c", 0)
                feelslike_c = current.get("feelslike_c", 0)
                humidity = current.get("humidity", 0)
                wind_kph = current.get("wind_kph", 0)
                uv = current.get("uv", 0)
                
                condition = current.get("condition", {})
                condition_text = condition.get("text", "Unknown State")
                icon_url = condition.get("icon", "")
                
                if icon_url.startswith("//"):
                    icon_url = "https:" + icon_url

                # Inject dynamic live payload array into HTML component template
                st.markdown(
                    f"""
                    <div class="weather-card">
                        <div class="location-sub">LIVE NODE · LOCAL CLOCK: {local_time}</div>
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 10px;">
                            <div>
                                <h2 style='margin:0;'>{city_name}</h2>
                                <div style="color: {MUTED}; font-size: 0.9rem; margin-top: 2px;">{country}</div>
                                <div class="temp-display">{temp_c}°C</div>
                                <div style="color: {SIGNAL}; font-weight: 600; font-size: 1.05rem;">
                                    Feels Like {feelslike_c}°C · {condition_text}
                                </div>
                            </div>
                            <div>
                                <img src="{icon_url}" style="width: 100px; height: 100px; filter: drop-shadow(0 0 12px rgba(40,224,196,0.25));">
                            </div>
                        </div>
                        
                        <div class="telemetry-grid">
                            <div class="telemetry-item">
                                <div class="telemetry-label">💧 Humidity</div>
                                <div class="telemetry-value">{humidity}%</div>
                            </div>
                            <div class="telemetry-item">
                                <div class="telemetry-label">💨 Wind Flow</div>
                                <div class="telemetry-value">{wind_kph} kph</div>
                            </div>
                            <div class="telemetry-item">
                                <div class="telemetry-label">☀️ Ultraviolet</div>
                                <div class="telemetry-value">{uv}</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                    
        except Exception as e:
            st.error(f"Unable to safely decode remote atmospheric telemetry stream: {e}")
    
