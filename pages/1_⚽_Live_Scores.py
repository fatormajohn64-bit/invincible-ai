import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Live Football Scores", page_icon="⚽", layout="centered")

st.title("⚽ Invincible 911 Match Center")
st.caption("Real-time global football scores powered by API-Football.")

# Retrieve the API key securely from Streamlit Secrets
SPORTS_API_KEY = st.secrets.get("SPORTS_API_KEY", None)

if not SPORTS_API_KEY:
    st.warning("⚠️ Live API Key Not Configured")
    st.markdown("To view dynamic real-time scores, connect an API key in your Streamlit secrets.")
else:
    try:
        url = "https://v3.football.api-sports.io/fixtures"
        headers = {"x-apisports-key": SPORTS_API_KEY}
        
        # 1. Try to fetch active live matches first
        response = requests.get(url, headers=headers, params={"live": "all"}, timeout=10)
        data = response.json()
        fixtures = data.get("response", [])
        
        is_live_data = True
        
        # 2. Smart Fallback: If no matches are live right now, fetch all of today's fixtures
        if not fixtures:
            is_live_data = False
            today_date = datetime.now().strftime("%Y-%m-%d")
            response = requests.get(url, headers=headers, params={"date": today_date}, timeout=10)
            data = response.json()
            fixtures = data.get("response", [])
            
        if not fixtures:
            st.info("No matches scheduled or playing today. Check back tomorrow!")
        else:
            if is_live_data:
                st.markdown(f"### 🔴 Live Matches In Play ({len(fixtures)})")
            else:
                st.markdown(f"### 📅 Today's Match Schedule ({len(fixtures)})")
                st.caption("No matches are live at this exact moment. Showing today's results and upcoming games:")
            
            for item in fixtures:
                fixture_info = item.get("fixture", {})
                status = fixture_info.get("status", {})
                time_elapsed = status.get("elapsed", 0)
                status_short = status.get("short", "")
                
                # Format status description text cleanly
                if status_short == "NS":
                    status_text = "Not Started Yet"
                elif status_short == "FT":
                    status_text = "Full Time (Finished)"
                else:
                    status_text = f"{time_elapsed}' ({status_short})"
                
                league_info = item.get("league", {})
                league_name = league_info.get("name", "Unknown League")
                country = league_info.get("country", "")
                
                teams = item.get("teams", {})
                home_team = teams.get("home", {}).get("name", "Home")
                away_team = teams.get("away", {}).get("name", "Away")
                
                goals = item.get("goals", {})
                home_goals = goals.get("home") if goals.get("home") is not None else "-"
                away_goals = goals.get("away") if goals.get("away") is not None else "-"
                
                # Build responsive container cards for high scannability
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{home_team}** vs **{away_team}**")
                        st.caption(f"{league_name} ({country}) — {status_text}")
                    with col2:
                        st.markdown(f"### {home_goals} – {away_goals}")
                    
    except Exception as e:
        st.error(f"Error connecting to live score engine: {e}")

if st.button("🔄 Refresh Scores", type="primary", use_container_width=True):
    st.rerun()
    
