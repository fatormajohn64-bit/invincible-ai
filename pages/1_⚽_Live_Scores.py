import streamlit as st
import requests

st.set_page_config(page_title="Live Football Scores", page_icon="⚽", layout="centered")

st.title("⚽ Invincible 911 Match Center")
st.caption("Real-time global football scores powered by API-Football.")

# Retrieve the API key securely from Streamlit Secrets
SPORTS_API_KEY = st.secrets.get("SPORTS_API_KEY", None)

if not SPORTS_API_KEY:
    st.warning("⚠️ Live API Key Not Configured")
    st.markdown(
        "To view dynamic real-time scores, connect an API key. "
        "Showing layout preview below:"
    )
    
    # Visual fallback container for application layout testing
    st.markdown("### 🏆 Live Match Center (Demo Mode)")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Real Madrid** 🇪🇸 vs **Barcelona** 🇪🇸")
        st.caption("La Liga — 72' In Play")
    with col2:
        st.markdown("### 2 – 1")
    st.divider()
else:
    try:
        # Configuration for the API-Sports Football endpoint
        url = "https://v3.football.api-sports.io/fixtures"
        headers = {
            "x-apisports-key": SPORTS_API_KEY
        }
        # Parameter to target only active, live matches globally
        params = {"live": "all"}
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()
        
        fixtures = data.get("response", [])
        
        if not fixtures:
            st.info("No live matches are currently in play right now. Check back during match kick-offs!")
        else:
            st.markdown(f"### ⚡ Current Live Matches ({len(fixtures)})")
            
            for item in fixtures:
                fixture_info = item.get("fixture", {})
                status = fixture_info.get("status", {})
                time_elapsed = status.get("elapsed", 0)
                status_short = status.get("short", "")
                
                league_info = item.get("league", {})
                league_name = league_info.get("name", "Unknown League")
                country = league_info.get("country", "")
                
                teams = item.get("teams", {})
                home_team = teams.get("home", {}).get("name", "Home")
                away_team = teams.get("away", {}).get("name", "Away")
                
                goals = item.get("goals", {})
                home_goals = goals.get("home", 0)
                away_goals = goals.get("away", 0)
                
                # Build responsive columns for the match banner
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{home_team}** vs **{away_team}**")
                        st.caption(f"{league_name} ({country}) — {time_elapsed}' ({status_short})")
                    with col2:
                        st.markdown(f"### {home_goals} – {away_goals}")
                    st.divider()
                    
    except Exception as e:
        st.error(f"Error connecting to live score engine: {e}")

# Manual sync action
if st.button("🔄 Refresh Scores", type="primary", use_container_width=True):
    st.rerun()
                
