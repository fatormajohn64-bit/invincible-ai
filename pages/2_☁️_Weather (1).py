"""
2_☁️_Weather.py
====================
Premium, glowing dark-themed weather telemetry control room powered by WeatherAPI.com.

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
# COUNTRY DIRECTORY (country -> representative city for lookup)
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
    "🇸🇪 Sweden": "Stockholm",
    "🇳🇴 Norway": "Oslo",
    "🇷🇺 Russia": "Moscow",
    "🇨🇦 Canada": "Toronto",
    "🇧🇷 Brazil": "Rio de Janeiro",
    "🇲🇽 Mexico": "Mexico City",
    "🇦🇷 Argentina": "Buenos Aires",
    "🇦🇺 Australia": "Sydney",
    "🇳🇿 New Zealand": "Auckland",
    "🇲🇦 Morocco": "Marrakesh",
    "🇹🇳 Tunisia": "Tunis",
    "🇶🇦 Qatar": "Doha",
    "🇯🇴 Jordan": "Amman",
    "🇱🇧 Lebanon": "Beirut",
    "🇮🇩 Iraq": "Baghdad",
    "🇮🇷 Iran": "Tehran",
    "🇹🇭 Thailand": "Bangkok",
    "🇵🇭 Philippines": "Manila",
    "🇻🇳 Vietnam": "Hanoi",
    "🇸🇬 Singapore": "Singapore",
}

# ---------------------------------------------------------------------------
# PREMIUM UI STYLE TOKENS (Cyber Glow System)
# ---------------------------------------------------------------------------
INK        = "#05070C"
SURFACE    = "#0E121B"
SURFACE_2  = "#161B27"
LINE       = "#242938"
TEXT       = "#F1F4FA"
MUTED      = "#7C879C"
SIGNAL     = "#28E0C4"

def temp_mood(temp_c: float):
    """Return (label, emoji, glow color, meter position 0-1)"""
    if temp_c < 5:
        return "Freezing", "🥶", "#4FC3F7", 0.02
    elif temp_c < 14:
        return "Cold", "❄️", "#42A5F5", 0.18
    elif temp_c < 20:
        return "Cool", "🌥️", "#5DD5C0", 0.35
    elif temp_c < 26:
        return "Mild", "😌", "#28E0C4", 0.5
    elif temp_c < 31:
        return "Warm", "🌤️", "#FFC94D", 0.68
    elif temp_c < 36:
        return "Hot", "🥵", "#FF8A3D", 0.85
    else:
        return "Scorching", "🔥", "#FF4433", 1.0

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background: radial-gradient(circle at 20% 0%, #0d1a1c 0%, {INK} 55%);
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

    @keyframes pulseGlow {{
        0%   {{ box-shadow: 0 0 18px 0 var(--glow-color); }}
        50%  {{ box-shadow: 0 0 34px 6px var(--glow-color); }}
        100% {{ box-shadow: 0 0 18px 0 var(--glow-color); }}
    }}

    .weather-card {{
        background: linear-gradient(160deg, {SURFACE} 0%, {SURFACE_2} 100%);
        border: 1px solid var(--glow-color);
        border-radius: 20px;
        padding: 26px;
        margin-bottom: 20px;
        animation: pulseGlow 3.2s ease-in-out infinite;
    }}

    .location-sub {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: var(--glow-color);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        text-shadow: 0 0 8px var(--glow-color);
    }}

    .temp-display {{
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 3.6rem;
        color: {TEXT};
        line-height: 1;
        margin: 10px 0;
        text-shadow: 0 0 22px var(--glow-color);
    }}

    .mood-badge {{
        display: inline-block;
        margin-top: 6px;
        padding: 6px 14px;
        border-radius: 999px;
        border: 1px solid var(--glow-color);
        color: {TEXT};
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 0 14px var(--glow-color);
    }}

    .telemetry-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-top: 22px;
    }}

    .telemetry-item {{
        background: {SURFACE_2};
        border: 1px solid {LINE};
        padding: 12px;
        border-radius: 12px;
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

    .meter-track {{
        position: relative;
        height: 10px;
        border-radius: 999px;
        margin-top: 22px;
        background: linear-gradient(90deg, #4FC3F7, #28E0C4, #FFC94D, #FF8A3D, #FF4433);
    }}

    .meter-marker {{
        position: absolute;
        top: -6px;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        background: {TEXT};
        border: 3px solid var(--glow-color);
        box-shadow: 0 0 12px var(--glow-color);
        transform: translateX(-50%);
    }}

    .meter-labels {{
        display: flex;
        justify-content: space-between;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        color: {MUTED};
        margin-top: 8px;
        text-transform: uppercase;
    }}

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
    st.caption("Pick a country node or launch a deep radar search.")

    country_options = list(COUNTRIES.keys()) + ["🔍 Custom Search..."]
    selection = st.selectbox("Country", options=country_options, index=0)

    if selection == "🔍 Custom Search...":
        city = st.text_input("🔍 Input target global city name:", value="Freetown")
    else:
        city = COUNTRIES[selection]

    st.divider()
    unit_toggle = st.radio("Units", ["°C", "°F"], horizontal=True)
    st.divider()
    st.caption("Telemetry feeds refresh dynamically on country swap.")

# ---------------------------------------------------------------------------
# INTERFACE MAIN COMPONENT VIEW
# ---------------------------------------------------------------------------
st.title("☁️ Invincible 911 Weather Station")
st.caption("Real-time high-fidelity atmospheric tracking and global condition analytics.")


def render_card(city_name, country, local_time, temp_c, feelslike_c, humidity,
                wind_kph, uv, condition_text, icon_url, is_live=True):
    if unit_toggle == "°F":
        temp_disp = round(temp_c * 9 / 5 + 32, 1)
        feels_disp = round(feelslike_c * 9 / 5 + 32, 1)
        unit_label = "°F"
    else:
        temp_disp = temp_c
        feels_disp = feelslike_c
        unit_label = "°C"

    mood_label, mood_emoji, glow_color, meter_pos = temp_mood(temp_c)
    feed_label = "LIVE NODE" if is_live else "SIMULATION FEED"

    st.markdown(
        f"""
        <div class="weather-card" style="--glow-color: {glow_color};">
            <div class="location-sub">{feed_label} · LOCAL CLOCK: {local_time}</div>
            <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 10px;">
                <div>
                    <h2 style='margin:0;'>{city_name}</h2>
                    <div style="color: {MUTED}; font-size: 0.9rem; margin-top: 2px;">{country}</div>
                    <div class="temp-display">{temp_disp}{unit_label}</div>
                    <div style="color: {TEXT}; font-weight: 500; font-size: 1.0rem;">
                        Feels Like {feels_disp}{unit_label} · {condition_text}
                    </div>
                    <div class="mood-badge">{mood_emoji} {mood_label}</div>
                </div>
                <div>
                    <img src="{icon_url}" style="width: 100px; height: 100px; filter: drop-shadow(0 0 14px {glow_color});">
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

            <div class="meter-track">
                <div class="meter-marker" style="left: {meter_pos * 100}%;"></div>
            </div>
            <div class="meter-labels">
                <span>🥶 Freezing</span>
                <span>❄️ Cold</span>
                <span>😌 Mild</span>
                <span>🥵 Hot</span>
                <span>🔥 Scorching</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


if not WEATHER_API_KEY:
    st.warning("⚠️ Atmospheric Core API Key Missing")
    st.markdown(
        "To switch out of demo simulation mode and tap into live monitoring assets:\n"
        "1. Create a key at **WeatherAPI.com**.\n"
        "2. Save it as `WEATHER_API_KEY` in your Streamlit secrets."
    )
    st.markdown("---")
    st.markdown("### 🌆 Telemetry Station Frame (Simulation Mode)")

    render_card(
        city_name="Freetown",
        country="Sierra Leone",
        local_time="15:36",
        temp_c=28,
        feelslike_c=31,
        humidity=82,
        wind_kph=14,
        uv=5.0,
        condition_text="Partly Cloudy",
        icon_url="https://cdn.weatherapi.com/weather/64x64/day/116.png",
        is_live=False
    )

else:
    if city:
        try:
            url = "https://api.weatherapi.com/v1/current.json"
            params = {"key": WEATHER_API_KEY, "q": city, "aqi": "no"}
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 400:
                st.error("❌ Specified location not found. Check the city name.")
            elif response.status_code != 200:
                st.error(f"⚠️ Telemetry fault — status code: {response.status_code}")
            else:
                data = response.json()

                loc = data.get("location", {})
                city_name = loc.get("name", "Unknown Node")
                country = loc.get("country", "")
                local_time = loc.get("localtime", "")

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

                render_card(
                    city_name, country, local_time, temp_c, feelslike_c,
                    humidity, wind_kph, uv, condition_text, icon_url, is_live=True
                )

                # ---------------------------------------------------------------
                # 💡 EXTRA IDEA: Quick multi-country comparison strip
                # ---------------------------------------------------------------
                st.markdown("### 🌍 Global Snapshot")
                st.caption("Quick glance at a few other stations around the world.")

                compare_cities = ["London", "New York", "Dubai", "Tokyo"]
                compare_cities = [c for c in compare_cities if c != city][:3]

                cols = st.columns(len(compare_cities))
                for col, c_city in zip(cols, compare_cities):
                    try:
                        r = requests.get(url, params={"key": WEATHER_API_KEY, "q": c_city, "aqi": "no"}, timeout=6)
                        if r.status_code == 200:
                            d = r.json()
                            t = d["current"]["temp_c"]
                            mood_label, mood_emoji, glow_color, _ = temp_mood(t)
                            with col:
                                st.markdown(
                                    f"""
                                    <div style="background:{SURFACE_2}; border:1px solid {glow_color};
                                                border-radius:12px; padding:10px; text-align:center;
                                                box-shadow: 0 0 10px {glow_color};">
                                        <div style="font-size:0.75rem; color:{MUTED};">{c_city}</div>
                                        <div style="font-size:1.3rem; font-weight:700; color:{TEXT};">{t}°C</div>
                                        <div style="font-size:0.8rem;">{mood_emoji} {mood_label}</div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                    except Exception:
                        pass

        except Exception as e:
            st.error(f"Unable to safely decode remote atmospheric telemetry stream: {e}")
