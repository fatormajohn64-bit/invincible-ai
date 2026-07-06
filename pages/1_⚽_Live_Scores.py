"""
1_⚽_Live_Scores.py
====================
Premium, dark-themed live scores dashboard powered by the free tier of
Football-Data.org (v4). Built for a multipage Streamlit app.

SETUP:
    Add to .streamlit/secrets.toml (or Streamlit Cloud secrets):
        FOOTBALL_DATA_API_KEY = "your-key-here"

Free-tier docs: https://www.football-data.org/documentation/quickstart
"""

import hashlib
import time
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
INK        = "#0A0E14"   # page background
SURFACE    = "#12161F"   # card background
SURFACE_2  = "#191E2A"   # inset / hover surface
LINE       = "#242938"   # hairline borders
TEXT       = "#E7EAF0"   # primary text
MUTED      = "#7C879C"   # secondary text
SIGNAL     = "#28E0C4"   # live / active accent (signal-cyan)
GOLD       = "#F2B84B"   # draw / neutral probability
CORAL      = "#FF6B5E"   # away-leaning probability / live dot
EMERALD    = "#3ED598"   # finished / win state

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

    .badge-live {{
        background: rgba(255, 107, 94, 0.14);
        color: {CORAL};
    }}
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

    .badge-scheduled {{
        background: rgba(124, 135, 156, 0.14);
        color: {MUTED};
    }}

    .badge-finished {{
        background: rgba(62, 213, 152, 0.14);
        color: {EMERALD};
    }}

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
        margin-top: 8px;
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
        margin-top: 4px;
    }}

    .empty-state {{
        text-align: center;
        padding: 3rem 1rem;
        color: {MUTED};
        font-family: 'Inter', sans-serif;
    }}

    div[data-testid="stButton"] button {{
        background: {SURFACE_2};
        border: 1px solid {LINE};
        color: {TEXT};
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.15s ease;
    }}
    div[data-testid="stButton"] button:hover {{
        border-color: {SIGNAL};
        color: {SIGNAL};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# COMPETITION CATALOG (free tier codes)
# ---------------------------------------------------------------------------
INTERNATIONAL_COMPS = {
    "WC":  "FIFA World Cup",
    "CL":  "UEFA Champions League",
    "CLI": "Copa Libertadores",
}

DOMESTIC_COMPS = {
    "PL":  "Premier League",
    "PD":  "La Liga",
    "SA":  "Serie A",
    "BL1": "Bundesliga",
    "FL1": "Ligue 1",
    "DED": "Eredivisie",
    "BSA": "Campeonato Brasileiro Série A",
    "ELC": "Championship",
    "PPL": "Primeira Liga",
}

ALL_COMPS = {**INTERNATIONAL_COMPS, **DOMESTIC_COMPS}

STATUS_LIVE = {"LIVE", "IN_PLAY", "PAUSED"}
STATUS_SCHEDULED = {"TIMED", "SCHEDULED"}
STATUS_FINISHED = {"FINISHED", "AWARDED"}


# ---------------------------------------------------------------------------
# WIN PROBABILITY ENGINE (deterministic analytics simulation)
# ---------------------------------------------------------------------------
def get_win_probabilities(home_name: str, away_name: str):
    key = f"{home_name.strip().lower()}::{away_name.strip().lower()}".encode()
    digest = hashlib.sha256(key).hexdigest()

    raw_home = int(digest[0:10], 16)
    raw_draw = int(digest[10:20], 16)
    raw_away = int(digest[20:30], 16)

    total = raw_home + raw_draw + raw_away
    home_share = raw_home / total
    draw_share = raw_draw / total
    away_share = raw_away / total

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

    home_pct = round(home_share * 100)
    draw_pct = round(draw_share * 100)
    away_pct = 100 - home_pct - draw_pct

    return {"home": home_pct, "draw": draw_pct, "away": away_pct}


# ---------------------------------------------------------------------------
# COUNTDOWN FORMATTER
# ---------------------------------------------------------------------------
def format_countdown(utc_date_str: str) -> str:
    try:
        match_time = datetime.fromisoformat(utc_date_str.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return ""

    now = datetime.now(timezone.utc)
    delta = match_time - now
    seconds = delta.total_seconds()

    if seconds <= 0:
        return "Kicking off any moment"

    total_minutes = int(seconds // 60)
    days, rem_minutes = divmod(total_minutes, 1440)
    hours, minutes = divmod(rem_minutes, 60)

    if days > 0:
        return f"Starts in {days}d {hours}h"
    if hours > 0:
        return f"Starts in {hours}h {minutes}m"
    if minutes > 15:
        return f"Starts in {minutes}m"
    if minutes > 0:
        return f"⚡ Kicking off in {minutes}m"
    return "⚡ Kicking off any moment"


# ---------------------------------------------------------------------------
# API DATA CONDUIT
# ---------------------------------------------------------------------------
@st.cache_data(ttl=60, show_spinner=False)
def fetch_matches(competition_codes: tuple, date_from: str, date_to: str):
    if not API_KEY:
        return [], "missing_key"

    headers = {"X-Auth-Token": API_KEY}
    params = {"dateFrom": date_from, "dateTo": date_to}
    if competition_codes:
        params["competitions"] = ",".join(competition_codes)

    try:
        response = requests.get(
            f"{API_BASE}/matches", headers=headers, params=params, timeout=10
        )
    except requests.exceptions.ConnectionError:
        return [], "connection_error"
    except requests.exceptions.Timeout:
        return [], "timeout"
    except requests.exceptions.RequestException as exc:
        return [], f"request_error: {exc}"

    if response.status_code == 429:
        return [], "rate_limited"
    if response.status_code == 403:
        return [], "forbidden"
    if response.status_code != 200:
        return [], f"http_{response.status_code}"

    try:
        payload = response.json()
    except ValueError:
        return [], "bad_json"

    return payload.get("matches", []), None


# ---------------------------------------------------------------------------
# CARD UI COMPONENT: STATUS BADGES
# ---------------------------------------------------------------------------
def render_status_badge(match):
    status = match.get("status")
    comp_code = match.get("competition", {}).get("code", "")
    comp_name = ALL_COMPS.get(comp_code, match.get("competition", {}).get("name", ""))

    if status in STATUS_LIVE:
        minute = match.get("minute")
        minute_txt = f"{minute}'" if minute else "LIVE"
        st.markdown(
            f'<span class="badge badge-live"><span class="dot-live"></span>{minute_txt}</span>',
            unsafe_allow_html=True,
        )
    elif status in STATUS_SCHEDULED:
        st.markdown('<span class="badge badge-scheduled">⏱ Scheduled</span>', unsafe_allow_html=True)
    elif status in STATUS_FINISHED:
        st.markdown('<span class="badge badge-finished">✓ Full-Time</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="badge badge-scheduled">{status}</span>', unsafe_allow_html=True)

    return comp_name


# ---------------------------------------------------------------------------
# CARD UI COMPONENT: LIVE & UPCOMING FIXTURES
# ---------------------------------------------------------------------------
def render_live_or_upcoming_card(match):
    home = match.get("homeTeam", {}).get("name", "TBD")
    away = match.get("awayTeam", {}).get("name", "TBD")
    home_short = match.get("homeTeam", {}).get("shortName") or home
    away_short = match.get("awayTeam", {}).get("shortName") or away
    status = match.get("status")
    score = match.get("score", {}).get("fullTime", {})
    home_score = score.get("home")
    away_score = score.get("away")
    kickoff_time = match.get("utcDate", "")

    try:
        dt = datetime.fromisoformat(kickoff_time.replace("Z", "+00:00"))
        time_txt = dt.strftime("%b %d · %H:%M UTC")
    except (ValueError, AttributeError):
        time_txt = "--:--"

    with st.container(border=True):
        top = st.columns([3, 1])
        with top[0]:
            comp_name = render_status_badge(match)
            st.markdown(f'<div class="comp-eyebrow">{comp_name}</div>', unsafe_allow_html=True)
        with top[1]:
            if status in STATUS_SCHEDULED:
                st.markdown(
                    f'<div style="text-align:right" class="countdown-text">{format_countdown(kickoff_time)}</div>',
                    unsafe_allow_html=True,
                )

        cols = st.columns([4, 2, 4])
        with cols[0]:
            st.markdown(f'<div class="team-name">🏠 {home_short}</div>', unsafe_allow_html=True)
        with cols[1]:
            if status in STATUS_LIVE:
                st.markdown(
                    f'<div class="score-num" style="text-align:center">{home_score if home_score is not None else 0} – {away_score if away_score is not None else 0}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="score-num" style="text-align:center;font-size:0.85rem;color:#7C879C;line-height:1.2;">{time_txt}</div>',
                    unsafe_allow_html=True,
                )
        with cols[2]:
            st.markdown(f'<div class="team-name" style="text-align:right">{away_short} ✈️</div>', unsafe_allow_html=True)

        if status in STATUS_SCHEDULED:
            probs = get_win_probabilities(home, away)
            st.markdown(
                f"""
                <div class="prob-wrap">
                    <div class="prob-seg-home" style="width:{probs['home']}%"></div>
                    <div class="prob-seg-draw" style="width:{probs['draw']}%"></div>
                    <div class="prob-seg-away" style="width:{probs['away']}%"></div>
                </div>
                <div class="prob-labels">
                    <span>{home_short} {probs['home']}%</span>
                    <span>Draw {probs['draw']}%</span>
                    <span>{away_short} {probs['away']}%</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------------------------
# CARD UI COMPONENT: COMPLETED HISTORICAL MATCHES
# ---------------------------------------------------------------------------
def render_finished_card(match):
    home_short = match.get("homeTeam", {}).get("shortName") or match.get("homeTeam", {}).get("name", "TBD")
    away_short = match.get("awayTeam", {}).get("shortName") or match.get("awayTeam", {}).get("name", "TBD")
    score = match.get("score", {}).get("fullTime", {})
    home_score = score.get("home", "-")
    away_score = score.get("away", "-")
    winner = match.get("score", {}).get("winner")
    kickoff_time = match.get("utcDate", "")

    try:
        dt = datetime.fromisoformat(kickoff_time.replace("Z", "+00:00"))
        date_txt = dt.strftime("%b %d")
    except (ValueError, AttributeError):
        date_txt = ""

    with st.container(border=True):
        comp_name = render_status_badge(match)
        st.markdown(f'<div class="comp-eyebrow">{comp_name} <span style="color:#7C879C">· {date_txt}</span></div>', unsafe_allow_html=True)

        cols = st.columns([4, 2, 4])
        with cols[0]:
            home_prefix = "🏆 " if winner == "HOME_TEAM" else ""
            st.markdown(f'<div class="team-name">{home_prefix}{home_short}</div>', unsafe_allow_html=True)
        with cols[1]:
            st.markdown(
                f'<div class="score-num" style="text-align:center">{home_score} – {away_score}</div>',
                unsafe_allow_html=True,
            )
        with cols[2]:
            away_suffix = " 🏆" if winner == "AWAY_TEAM" else ""
            st.markdown(f'<div class="team-name" style="text-align:right">{away_short}{away_suffix}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# SIDEBAR CONTROL INTERFACE
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚽ Filters")

    scope = st.radio(
        "Scope",
        options=["All Competitions", "🌐 International", "🏆 Domestic Leagues"],
        index=0,
    )

    if scope == "🌐 International":
        pool = INTERNATIONAL_COMPS
    elif scope == "🏆 Domestic Leagues":
        pool = DOMESTIC_COMPS
    else:
        pool = ALL_COMPS

    league_choice = st.selectbox(
        "Competition",
        options=["All"] + list(pool.keys()),
        format_func=lambda code: "All in scope" if code == "All" else f"{pool[code]} ({code})",
    )

    if league_choice == "All":
        selected_codes = tuple(pool.keys())
    else:
        selected_codes = (league_choice,)

    st.divider()
    
    st.markdown("### 📅 Timeframe")
    date_mode = st.selectbox(
        "Date Range Selection",
        options=["7-Day Window (Recommended)", "Today Only", "Next 3 Days", "Past 3 Days"],
        index=0
    )
    
    now_utc = datetime.now(timezone.utc)
    if date_mode == "Today Only":
        date_from = now_utc.strftime("%Y-%m-%d")
        date_to = now_utc.strftime("%Y-%m-%d")
    elif date_mode == "Next 3 Days":
        date_from = now_utc.strftime("%Y-%m-%d")
        date_to = (now_utc + timedelta(days=3)).strftime("%Y-%m-%d")
    elif date_mode == "Past 3 Days":
        date_from = (now_utc - timedelta(days=3)).strftime("%Y-%m-%d")
        date_to = now_utc.strftime("%Y-%m-%d")
    else: # Default 7-Day Matrix Window
        date_from = (now_utc - timedelta(days=3)).strftime("%Y-%m-%d")
        date_to = (now_utc + timedelta(days=3)).strftime("%Y-%m-%d")

    st.divider()
    st.caption("Data caches for 60s. Tap refresh below to force update.")

# ---------------------------------------------------------------------------
# CORE VIEW RENDER ENGINE
# ---------------------------------------------------------------------------
st.title("⚽ Live Scores")
st.caption(f"Powered by Football-Data.org · Range: {date_from} to {date_to}")

if not API_KEY:
    st.error("No API key configured. Check your Streamlit Secrets layout settings.")
    st.stop()

# Execution fetch cycle
matches, error = fetch_matches(selected_codes, date_from, date_to)

if error == "rate_limited":
    st.warning("⏳ Rate limit hit for Football-Data.org free tier. Please wait a moment.")
    st.stop()
elif error == "forbidden":
    st.error("🔒 Access denied—this selection might require a paid tier key.")
    st.stop()
elif error in ("connection_error", "timeout"):
    st.error("📡 Data stream connection timeout. Check network latency.")
    st.stop()
elif error is not None:
    st.error(f"⚠️ App encounter state anomaly: {error}")
    st.stop()

# Sorting partitions
live_and_upcoming = [m for m in matches if m.get("status") in STATUS_LIVE | STATUS_SCHEDULED]
previous_results = [m for m in matches if m.get("status") in STATUS_FINISHED]

def _sort_key(match):
    status = match.get("status")
    is_live = 0 if status in STATUS_LIVE else 1
    return (is_live, match.get("utcDate", ""))

live_and_upcoming.sort(key=_sort_key)
previous_results.sort(key=lambda m: m.get("utcDate", ""), reverse=True)

# Tabs management allocation Layout
tab_live, tab_previous = st.tabs(["🔴 Live & Upcoming", "🏁 Previous Results"])

with tab_live:
    if not live_and_upcoming:
        st.markdown(
            f'<div class="empty-state">No live or upcoming matches found from {date_from} to {date_to}.</div>',
            unsafe_allow_html=True,
        )
    else:
        for m in live_and_upcoming:
            render_live_or_upcoming_card(m)

with tab_previous:
    if not previous_results:
        st.markdown(
            f'<div class="empty-state">No completed matches found from {date_from} to {date_to}.</div>',
            unsafe_allow_html=True,
        )
    else:
        for m in previous_results:
            render_finished_card(m)

# Interactivity controller block
st.divider()
if st.button("🔄 Refresh Match Center", type="primary", use_container_width=True):
    st.rerun()
