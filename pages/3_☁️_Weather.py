import streamlit as st
import requests

st.set_page_config(page_title="Real-Time Weather", page_icon="☁️", layout="centered")

st.title("☁️ Invincible 911 Weather Station")
st.caption("Real-time global weather conditions and live icon tracking.")

# Securely grab the key from your Streamlit secrets
WEATHER_API_KEY = st.secrets.get("WEATHER_API_KEY", None)

if not WEATHER_API_KEY:
    st.warning("⚠️ Weather API Key Not Configured")
    st.markdown(
        "To fetch real-time weather and official condition icons:\n"
        "1. Register for a free account at **WeatherAPI.com** (100% free, no credit card needed).\n"
        "2. Add your key to your Streamlit secrets as `WEATHER_API_KEY`."
    )
    
    # Elegant design preview for app testing
    st.markdown("### 🌆 Weather Station (Demo Mode)")
    st.info("Showing mock layout. Connect your API key to view real-time data anywhere!")
    
    with st.container(border=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            # High-quality open-source placeholder weather icon
            st.image("https://cdn.weatherapi.com/weather/64x64/day/116.png", width=100)
        with col2:
            st.subheader("Freetown, Sierra Leone")
            st.markdown("### 28°C")
            st.write("**Condition:** Partly Cloudy ⛅")
            st.caption("Wind: 14 km/h | Humidity: 82% | UV Index: 5.0")
else:
    # User input for City Search
    city = st.text_input("🔍 Search for any city in the world:", value="Freetown")
    
    if city:
        try:
            url = "https://api.weatherapi.com/v1/current.json"
            params = {
                "key": WEATHER_API_KEY,
                "q": city,
                "aqi": "no"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 400:
                st.error("❌ City not found. Please check the spelling and try again.")
            elif response.status_code != 200:
                st.error(f"⚠️ Error code: {response.status_code}")
            else:
                data = response.json()
                
                # Extract location metadata
                loc = data.get("location", {})
                city_name = loc.get("name", "Unknown")
                country = loc.get("country", "")
                local_time = loc.get("localtime", "")
                
                # Extract core metrics
                current = data.get("current", {})
                temp_c = current.get("temp_c", 0)
                feelslike_c = current.get("feelslike_c", 0)
                humidity = current.get("humidity", 0)
                wind_kph = current.get("wind_kph", 0)
                uv = current.get("uv", 0)
                
                # Extract dynamic image condition parameters
                condition = current.get("condition", {})
                condition_text = condition.get("text", "Unknown")
                icon_url = condition.get("icon", "")
                
                # Fix partial URL schema if missing
                if icon_url.startswith("//"):
                    icon_url = "https:" + icon_url
                
                # Build responsive grid container
                with st.container(border=True):
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        if icon_url:
                            st.image(icon_url, caption=condition_text, use_container_width=True)
                        else:
                            st.write("🌡️")
                            
                    with col2:
                        st.subheader(f"{city_name}, {country}")
                        st.caption(f"Local Date & Time: {local_time}")
                        st.markdown(f"## {temp_c}°C")
                        st.write(f"**Feels Like:** {feelslike_c}°C")
                        
                    st.divider()
                    
                    # Highlight extra metadata parameters using Streamlit metrics
                    m_col1, m_col2, m_col3 = st.columns(3)
                    m_col1.metric("💧 Humidity", f"{humidity}%")
                    m_col2.metric("💨 Wind Speed", f"{wind_kph} kph")
                    m_col3.metric("☀️ UV Index", f"{uv}")
                    
        except Exception as e:
            st.error(f"Could not connect to weather servers: {e}")
          
