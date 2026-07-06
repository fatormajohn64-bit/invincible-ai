import streamlit as st
import requests

st.set_page_config(page_title="Live Football Scores", page_icon="⚽", layout="centered")

st.title("⚽ Invincible 911 Match Center")
st.caption("Real-time football scores powered by Football-Data.org (100% Free).")

# Retrieve the free token securely from your secrets setup
FOOTBALL_DATA_API_KEY = st.secrets.get("FOOTBALL_DATA_API_KEY", None)

if not FOOTBALL_DATA_API_KEY:
    st.warning("⚠️ Free Football-Data API Key Not Configured")
    st.markdown(
        "To link your free token:\n"
        "1. Register at **football-data.org** (no card required).\n"
        "2. Save the key in your Streamlit Advanced Settings under the name `FOOTBALL_DATA_API_KEY`."
    )
    
    # Clean UI presentation sample for layout checking
    st.markdown("### 🏆 Match Board (Demo Mode)")
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Real Madrid** vs **Barcelona**")
            st.caption("🕒 SCHEDULED | La Liga")
        with col2:
            st.markdown("### - – -")
else:
    try:
        # Request path to pull all active global matches for today
        url = "https://api.football-data.org/v4/matches"
        headers = {"X-Auth-Token": FOOTBALL_DATA_API_KEY}
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 429:
            st.error("⚠️ Free limit hit! This tier allows 10 updates per minute. Take a short pause and click refresh again.")
        elif response.status_code != 200:
            st.error(f"⚠️ Server returned error code: {response.status_code}")
        else:
            data = response.json()
            matches = data.get("matches", [])
            
            if not matches:
                st.info("No fixtures playing today inside the core 12 free leagues. Check back during match days!")
            else:
                st.markdown(f"### 📅 Today's Match Board ({len(matches)})")
                
                for match in matches:
                    competition = match.get("competition", {}).get("name", "League")
                    status = match.get("status", "SCHEDULED")
                    
                    home_team = match.get("homeTeam", {}).get("name", "Home")
                    away_team = match.get("awayTeam", {}).get("name", "Away")
                    
                    # Dig out score parameters safely
                    score_details = match.get("score", {})
                    home_goals = score_details.get("fullTime", {}).get("home")
                    away_goals = score_details.get("fullTime", {}).get("away")
                    
                    # Convert blank upcoming match metrics cleanly
                    if home_goals is None: home_goals = "-"
                    if away_goals is None: away_goals = "-"
                    
                    # Set alert dots depending on match status values
                    status_indicator = "🔴" if status in ["IN_PLAY", "PAUSED"] else "🕒"
                    if status == "FINISHED": 
                        status_indicator = "🏁"
                    
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**{home_team}** vs **{away_team}**")
                            st.caption(f"{status_indicator} {status.replace('_', ' ')} | {competition}")
                        with col2:
                            st.markdown(f"### {home_goals} – {away_goals}")
                            
    except Exception as e:
        st.error(f"Could not reach data server: {e}")

# Explicit refresh configuration
if st.button("🔄 Refresh Match Center", type="primary", use_container_width=True):
    st.rerun()
                    
