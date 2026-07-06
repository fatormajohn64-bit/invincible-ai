"""
1_⚽_Live_Scores.py
====================
Premium, dark-themed live scores dashboard powered by the free tier of
Football-Data.org (v4). Built for a multipage Streamlit app.
"""

import hashlib
from datetime import datetime, timezone, timedelta

import requests
import streamlit as st

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Live Scores",
    page_icon="⚽",
    layout="wide",
)

API_BASE = "https://api.football-data.org/v4"
API_KEY = st.secrets.get("FOOTBALL_DATA_API_KEY", "")

# ---------------------------------------------------------------------------
# DESIGN TOKENS (Custom Dark Theme Styles)
# ---------------------------------------------------------------------------
INK        = "#0A0E14"   
SURFACE    = "#12161F"   
SURFACE_2  = "#191E2A"   
LINE       = "#242938"   
TEXT       = "#E7EAF0"   
MUTED      = "#7C879C"   
SIGNAL     = "#28E0C4"   
GOLD       = "#F2B84B"   
CORAL      = "#FF6B5E"   
EMERALD    = "#3ED598"   
VIOLET     = "#9B8CFF"   

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

    h1, h2, h3 {{
        font-family: 'Space Grotesk', sans-serif !important;
        color: {TEXT} !important;
        letter-spacing: -0.02em;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: {SURFACE};
        border: 1px solid {LINE} !important;
        border-radius: 14px;
        transition: border-color 0.15s ease;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
        border-color: #323952 !important;
    }}

    .comp-eyebrow {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: {MUTED};
        margin-bottom: 8px;
    }}

    .score-num {{
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.65rem;
        color: {TEXT};
        line-height: 1;
    }}

    .team-name {{
        font-weight: 600;
        font-size: 0.95rem;
        color: {TEXT};
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    .badge {{
        display: inline-flex;
        align-items: center;
        gap: 5px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        font-weight: 500;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        padding: 3px 9px;
        border-radius: 999px;
    }}

    .badge-live {{ background: rgba(255, 107, 94, 0.14); color: {CORAL}; }}
    .dot-live {{
        width: 7px; height: 7px; border-radius: 50%;
        background: {CORAL};
        display: inline-block;
        animation: pulse 1.4s ease-in-out infinite;
    }}
    @keyframes pulse {{
        0%   {{ box-shadow: 0 0 0 0 rgba(255,107,94,0.55); }}
        70%  {{ box-shadow: 0 0 0 7px rgba(255,107,94,0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(255,107,94,0); }}
    }}

    .badge-scheduled {{ background: rgba(124, 135, 156, 0.14); color: {MUTED}; }}
    .badge-finished {{ background: rgba(62, 213, 152, 0.14); color: {EMERALD}; }}
    .badge-sim {{ background: rgba(155, 140, 255, 0.14); color: {VIOLET}; }}

    .countdown-text {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: {MUTED};
    }}

    .prob-wrap {{
        display: flex;
        width: 100%;
        height: 8px;
        border-radius: 999px;
        overflow: hidden;
        background: {SURFACE_2};
        margin-top: 12px;
    }}
    .prob-seg-home  {{ background: {SIGNAL}; height: 100%; }}
    .prob-seg-draw  {{ background: {GOLD};   height: 100%; }}
    .prob-seg-away  {{ background: {CORAL};  height: 100%; }}

    .prob-labels {{
        display: flex;
        justify-content: space-between;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: {MUTED};
        margin-top: 6px;
        margin-bottom: 8px;
    }}

    div[data-testid="stButton"] button {{
        background: {SURFACE_2};
        border: 1px solid {LINE};
        color: {TEXT};
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.15s ease;
        width: 100%;
    }}
    div[data-testid="stButton"] button:hover {{
        border-color: {SIGNAL};
        color: {SIGNAL};
    }}

    .sim-banner {{
        background: rgba(155, 140, 255, 0.08);
        border: 1px dashed rgba(155, 140, 255, 0.4);
        border-radius: 10px;
        padding: 10px 14px;
        font-size: 0.8rem;
        color: {VIOLET};
        margin-bottom: 14px;
        text-align: center;
    }}

    .player-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 7px 10px;
        border-radius: 8px;
        background: {SURFACE_2};
        margin-bottom: 6px;
    }}
    .player-left {{ display: flex; align-items: center; gap: 9px; }}
    .player-num {{ font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: {MUTED}; width: 20px; text-align: center; }}
    .player-pos {{ font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: {MUTED}; background: rgba(124,135,156,0.14); padding: 2px 6px; border-radius: 5px; }}
    .player-name {{ font-size: 0.85rem; color: {TEXT}; font-weight: 500; }}
    .rating-chip {{ font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 0.78rem; padding: 2px 9px; border-radius: 999px; color: {INK}; }}
    .team-avg-rating {{ font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1.1rem; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# COMPETITION CATALOG (All Available International & National Tiers)
# ---------------------------------------------------------------------------
ALL_COMPS = {
    # International Tournaments
    "WC": "🏆 FIFA World Cup",
    "CL": "🇪🇺 UEFA Champions League",
    "EC": "🇪🇺 UEFA European Championship",
    "CLI": "🌎 Copa Libertadores",
    # National Domestic Leagues
    "PL": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League (England)",
    "ELC": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 EFL Championship (England)",
    "PD": "🇪🇸 La Liga (Spain)",
    "SA": "🇮🇹 Serie A (Italy)",
    "BL1": "🇩🇪 Bundesliga (Germany)",
    "FL1": "🇫🇷 Ligue 1 (France)",
    "DED": "🇳🇱 Eredivisie (Netherlands)",
    "PPL": "🇵🇹 Primeira Liga (Portugal)",
    "BSA": "🇧🇷 Campeonato Brasileiro Série A"
}

STATUS_LIVE = {"LIVE", "IN_PLAY", "PAUSED"}
STATUS_SCHEDULED = {"TIMED", "SCHEDULED"}
STATUS_FINISHED = {"FINISHED", "AWARDED"}

# ---------------------------------------------------------------------------
# WIN PROBABILITY ENGINE
# ---------------------------------------------------------------------------
def get_win_probabilities(home_name: str, away_name: str):
    key = f"{home_name.strip().lower()}::{away_name.strip().lower()}".encode()
    digest = hashlib.sha256(key).hexdigest()

    raw_home, raw_draw, raw_away = int(digest[0:10], 16), int(digest[10:20], 16), int(digest[20:30], 16)
    total = raw_home + raw_draw + raw_away
    
    home_share, draw_share, away_share = raw_home/total, raw_draw/total, raw_away/total

    HOME_ADVANTAGE = 0.07
    home_share += HOME_ADVANTAGE
    away_share -= HOME_ADVANTAGE * 0.6
    draw_share -= HOME_ADVANTAGE * 0.4

    draw_share = max(0.18, min(0.32, draw_share))
    remaining = 1.0 - draw_share
    hw_aw_total = home_share + away_share
    
    if hw_aw_total <= 0:
        home_share = away_share = remaining / 2
    else:
        home_share = remaining * (home_share / hw_aw_total)
        away_share = remaining * (away_share / hw_aw_total)

    return {"home": round(home_share * 100), "draw": round(draw_share * 100), "away": 100 - round(home_share * 100) - round(draw_share * 100)}

# ---------------------------------------------------------------------------
# LINEUP ENGINE (Simulated for free tier)
# ---------------------------------------------------------------------------
FORMATIONS = ["4-3-3", "4-4-2", "3-5-2", "4-2-3-1", "3-4-3", "5-3-2"]

def get_rating_color(rating: float) -> str:
    if rating >= 8.3: return EMERALD
    if rating >= 7.0: return SIGNAL
    if rating >= 6.0: return GOLD
    return CORAL

def generate_simulated_lineup(team_name: str, match_id, side: str):
    seed = f"{match_id}::{side}::{team_name.strip().lower()}".encode()
    digest = hashlib.sha256(seed).hexdigest()

    formation = FORMATIONS[int(digest[0:4], 16) % len(FORMATIONS)]
    slots = [("GK", 1)]
    for i, count in enumerate([int(x) for x in formation.split("-")]):
        slots.append((["DF", "MF", "FW"][i], count))

    used_numbers, players, slot_idx = set(), [], 0
    for pos, count in slots:
        for _ in range(count):
            chunk = digest[(slot_idx * 6) % 58: (slot_idx * 6) % 58 + 6]
            val = int(chunk, 16) if chunk else slot_idx * 7 + 1
            number = (val % 27) + 1
            while number in used_numbers: number = (number % 27) + 1
            used_numbers.add(number)
            players.append({"number": number, "position": pos, "rating": round(5.6 + (val % 401) / 100, 1)})
            slot_idx += 1

    return formation, players, round(sum(p["rating"] for p in players) / len(players), 2)

def render_lineup_column(team_short: str, team_name: str, match_id, side: str):
    formation, players, avg_rating = generate_simulated_lineup(team_name, match_id, side)

    st.markdown(
        f'''
        <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
            <div><strong class="team-name">{team_short}</strong><br><span style="font-size:12px; color:{MUTED};">{formation}</span></div>
            <div class="team-avg-rating" style="color:{get_rating_color(avg_rating)}">{avg_rating}</div>
        </div>
        ''', unsafe_allow_html=True
    )

    for p in players:
        st.markdown(
            f'''
            <div class="player-row">
                <div class="player-left">
                    <span class="player-num">#{p['number']}</span>
                    <span class="player-pos">{p['position']}</span>
                    <span class="player-name">{team_short} Player</span>
                </div>
                <span class="rating-chip" style="background:{get_rating_color(p['rating'])}">{p['rating']}</span>
            </div>
            ''', unsafe_allow_html=True
        )

# ---------------------------------------------------------------------------
# API CONDUIT
# ---------------------------------------------------------------------------
@st.cache_data(ttl=60, show_spinner=False)
def fetch_matches(date_from: str, date_to: str):
    if not API_KEY: return [], "missing_key"
    try:
        res = requests.get(f"{API_BASE}/matches", headers={"X-Auth-Token": API_KEY}, params={"dateFrom": date_from, "dateTo": date_to}, timeout=10)
        return res.json().get("matches", []), None if res.status_code == 200 else f"Error {res.status_code}"
    except Exception as e:
        return [], str(e)

# ---------------------------------------------------------------------------
# UI COMPONENTS
# ---------------------------------------------------------------------------
def go_to_match(match_id):
    st.session_state["selected_match_id"] = match_id

def render_status_badge(match):
    status = match.get("status")
    if status in STATUS_LIVE:
        return f'<span class="badge badge-live"><span class="dot-live"></span>{match.get("minute", "LIVE")}\'</span>'
    elif status in STATUS_SCHEDULED:
        return '<span class="badge badge-scheduled">⏱ Scheduled</span>'
    return '<span class="badge badge-finished">✓ Full-Time</span>'

def render_match_card(match):
    home = match.get("homeTeam", {}).get("name", "TBD")
    away = match.get("awayTeam", {}).get("name", "TBD")
    home_short = match.get("homeTeam", {}).get("shortName") or home
    away_short = match.get("awayTeam", {}).get("shortName") or away
    
    score = match.get("score", {}).get("fullTime", {})
    home_score = score.get("home", 0) if score.get("home") is not None else "0"
    away_score = score.get("away", 0) if score.get("away") is not None else "0"
    
    status = match.get("status")
    match_id = match.get("id")

    # Resolve Clean Competition Display Name
    comp_code = match.get("competition", {}).get("code")
    comp_display = ALL_COMPS.get(comp_code, f"🏆 {match.get('competition', {}).get('name', 'Football')}")

    with st.container(border=True):
        st.markdown(f'<div class="comp-eyebrow">{render_status_badge(match)} - {comp_display}</div>', unsafe_allow_html=True)
        
        cols = st.columns([3, 2, 3])
        with cols[0]:
            st.markdown(f'<div class="team-name">🏠 {home_short}</div>', unsafe_allow_html=True)
        
        with cols[1]:
            if status in STATUS_SCHEDULED:
                st.markdown('<div class="score-num" style="text-align:center">V</div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="score-num" style="text-align:center">{home_score} – {away_score}</div>',
                    unsafe_allow_html=True,
                )
                
        with cols[2]:
            st.markdown(f'<div class="team-name" style="text-align:right">{away_short} ✈️</div>', unsafe_allow_html=True)

        if status not in STATUS_FINISHED:
            probs = get_win_probabilities(home, away)
            st.markdown(
                f'''
                <div class="prob-wrap">
                    <div class="prob-seg-home" style="width: {probs["home"]}%"></div>
                    <div class="prob-seg-draw" style="width: {probs["draw"]}%"></div>
                    <div class="prob-seg-away" style="width: {probs["away"]}%"></div>
                </div>
                <div class="prob-labels">
                    <span>{probs["home"]}% H</span>
                    <span>{probs["draw"]}% D</span>
                    <span>{probs["away"]}% A</span>
                </div>
                ''', unsafe_allow_html=True
            )
        else:
            st.markdown("<br>", unsafe_allow_html=True)

        st.button("Match Center", key=f"btn_{match_id}", on_click=go_to_match, args=(match_id,))

# ---------------------------------------------------------------------------
# MAIN APP LOOP
# ---------------------------------------------------------------------------
def main():
    if "selected_match_id" not in st.session_state:
        st.session_state["selected_match_id"] = None

    if st.session_state["selected_match_id"]:
        match_id = st.session_state["selected_match_id"]
        if st.button("← Back to Scores"):
            st.session_state["selected_match_id"] = None
            st.rerun()
            
        st.markdown("### Match Center Analytics")
        st.markdown('<div class="sim-banner">Lineups and ratings are deterministically generated (Free API limitations)</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: render_lineup_column("Home", "Home Team", match_id, "home")
        with c2: render_lineup_column("Away", "Away Team", match_id, "away")
        return

    st.title("⚽ Global Match Feed")
    
    if not API_KEY:
        st.error("Missing FOOTBALL_DATA_API_KEY in Streamlit Secrets.")
        return

    # -----------------------------------------------------------------------
    # NEW SIDEBAR CONTROLS (League Filter & Time Travel)
    # -----------------------------------------------------------------------
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Match Feed Filters")
    
    # NEW: 7-Day Window Toggle Control
    use_7_day = st.sidebar.toggle(
        "📅 Show 7-Day Window", 
        value=False, 
        help="View past (finished), current (live), and upcoming scheduled matches within a 7-day span."
    )

    # 1. Date Picker Control (Grays out when 7-Day Window is active)
    selected_date = st.sidebar.date_input("Select Match Date", datetime.now(timezone.utc).date(), disabled=use_7_day)
    
    # Logic to switch between Single Day and 7-Day Range
    if use_7_day:
        today = datetime.now(timezone.utc).date()
        # API fetches from 3 days ago up to 3 days in the future (7 days total)
        date_from_str = (today - timedelta(days=3)).strftime("%Y-%m-%d")
        date_to_str = (today + timedelta(days=3)).strftime("%Y-%m-%d")
        display_date_text = f"{date_from_str} to {date_to_str}"
    else:
        # FIX: Ensure we only process a single date, even if Streamlit returns a tuple
        if isinstance(selected_date, tuple):
            if len(selected_date) > 0:
                selected_date = selected_date[0]
            else:
                selected_date = datetime.now(timezone.utc).date()
                
        date_from_str = selected_date.strftime("%Y-%m-%d")
        date_to_str = selected_date.strftime("%Y-%m-%d")
        display_date_text = date_from_str
    
    # 2. League Selection Dropdown
    all_league_names = list(ALL_COMPS.values())
    selected_leagues = st.sidebar.multiselect(
        "Filter Competitions",
        options=all_league_names,
        default=all_league_names,
        help="Add or remove leagues to filter the live dashboard view."
    )

    # Convert selected visible names back to API short codes
    selected_codes = {code for code, name in ALL_COMPS.items() if name in selected_leagues}

    # Fetch live match list data from chosen date(s)
    matches, err = fetch_matches(date_from_str, date_to_str)
    
    if err:
        st.error(f"Error fetching data: {err}")
        return
        
    if not matches:
        st.info(f"No match events recorded for {display_date_text}.")
        return

    # Local filtration pass based on sidebar settings
    filtered_matches = [
        m for m in matches 
        if m.get("competition", {}).get("code") in selected_codes
    ]

    if not filtered_matches:
        st.info("No matches match your active sidebar league filters.")
        return

    # Grouping matching data models
    live = [m for m in filtered_matches if m["status"] in STATUS_LIVE]
    upcoming = [m for m in filtered_matches if m["status"] in STATUS_SCHEDULED]
    finished = [m for m in filtered_matches if m["status"] in STATUS_FINISHED]

    if live:
        st.subheader("🔴 Live Now")
        for m in live: render_match_card(m)
        
    if upcoming:
        st.subheader("⏱ Upcoming")
        for m in upcoming: render_match_card(m)
        
    if finished:
        st.subheader("✓ Finished")
        for m in finished: render_match_card(m)

if __name__ == "__main__":
    main()
    
