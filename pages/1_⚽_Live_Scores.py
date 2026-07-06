"""
1_⚽_Live_Scores.py
====================
Premium, dark-themed live scores dashboard powered by the free tier of
Football-Data.org (v4). Built for a multipage Streamlit app.

SETUP:
    Add to .streamlit/secrets.toml (or Streamlit Cloud secrets):
        FOOTBALL_DATA_API_KEY = "your-key-here"

Free-tier docs: https://www.football-data.org/documentation/quickstart

NOTE ON MATCH DETAIL DATA:
    The free tier of Football-Data.org does NOT include player-level data
    (lineups, substitutions, cards, player ratings) — that requires a paid
    "deep data" add-on. Real fields available on the free tier (venue,
    attendance, referee, half/full-time score, matchday, etc.) are fetched
    live from the API. Lineups and player ratings shown in the match detail
    view are clearly labeled SIMULATED — deterministically generated (same
    technique as the existing win-probability engine) so the app still
    looks and feels complete, without pretending to have real player data.
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
VIOLET     = "#9B8CFF"   # simulated-data accent

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

    .badge-sim {{
        background: rgba(155, 140, 255, 0.14);
        color: {VIOLET};
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

    .detail-stat-label {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: {MUTED};
        margin-bottom: 2px;
    }}
    .detail-stat-value {{
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        color: {TEXT};
    }}

    .sim-banner {{
        background: rgba(155, 140, 255, 0.08);
        border: 1px dashed rgba(155, 140, 255, 0.4);
        border-radius: 10px;
        padding: 10px 14px;
        font-size: 0.8rem;
        color: {VIOLET};
        margin-bottom: 14px;
    }}

    .formation-tag {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: {MUTED};
        margin-bottom: 10px;
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
    .player-left {{
        display: flex;
        align-items: center;
        gap: 9px;
    }}
    .player-num {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: {MUTED};
        width: 20px;
        text-align: center;
    }}
    .player-pos {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.62rem;
        letter-spacing: 0.05em;
        color: {MUTED};
        background: rgba(124,135,156,0.14);
        padding: 2px 6px;
        border-radius: 5px;
    }}
    .player-name {{
        font-size: 0.85rem;
        color: {TEXT};
        font-weight: 500;
    }}
    .rating-chip {{
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 0.78rem;
        padding: 2px 9px;
        border-radius: 999px;
        color: {INK};
    }}
    .team-avg-rating {{
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
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
# SIMULATED LINEUP & PLAYER RATING ENGINE
# ---------------------------------------------------------------------------
# The free API tier has no real squad/lineup/player-rating data. This engine
# deterministically derives a plausible formation + shirt numbers + ratings
# from the team name and match id, so refreshing the page always shows the
# same "simulated" lineup for a given match rather than random noise.
FORMATIONS = ["4-3-3", "4-4-2", "3-5-2", "4-2-3-1", "3-4-3", "5-3-2"]


def get_rating_color(rating: float) -> str:
    if rating >= 8.3:
        return EMERALD
    if rating >= 7.0:
        return SIGNAL
    if rating >= 6.0:
        return GOLD
    return CORAL


def generate_simulated_lineup(team_name: str, match_id, side: str):
    seed = f"{match_id}::{side}::{team_name.strip().lower()}".encode()
    digest = hashlib.sha256(seed).hexdigest()

    formation = FORMATIONS[int(digest[0:4], 16) % len(FORMATIONS)]
    line_counts = [int(x) for x in formation.split("-")]

    slots = [("GK", 1)]
    line_labels = ["DF", "MF", "FW"]
    for i, count in enumerate(line_counts):
        slots.append((line_labels[i], count))

    used_numbers = set()
    players = []
    slot_idx = 0
    for pos, count in slots:
        for _ in range(count):
            chunk = digest[(slot_idx * 6) % 58: (slot_idx * 6) % 58 + 6]
            val = int(chunk, 16) if chunk else slot_idx * 7 + 1

            number = (val % 27) + 1
            while number in used_numbers:
                number = (number % 27) + 1
            used_numbers.add(number)

            rating = round(5.6 + (val % 401) / 100, 1)  # ~5.6 - 9.6
            players.append({"number": number, "position": pos, "rating": rating})
            slot_idx += 1

    avg_rating = round(sum(p["rating"] for p in players) / len(players), 2)
    return formation, players, avg_rating


def render_lineup_column(team_short: str, team_name: str, match_id, side: str):
    formation, players, avg_rating = generate_simulated_lineup(team_name, match_id, side)

    top = st.columns([2, 1])
    with top[0]:
        st.markdown(f'<div class="team-name">{team_short}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="formation-tag">Formation {formation} · Simulated</div>', unsafe_allow_html=True)
    with top[1]:
        st.markdown(
            f'<div style="text-align:right" class="team-avg-rating" style="color:{get_rating_color(avg_rating)}">{avg_rating}</div>',
            unsafe_allow_html=True,
        )

    for p in players:
        color = get_rating_color(p["rating"])
        st.markdown(
            f"""
            <div class="player-row">
                <div class="player-left">
                    <span class="player-num">#{p['number']}</span>
                    <span class="player-pos">{p['position']}</span>
                    <span class="player-name">{team_short} Player {p['number']}</span>
                </div>
                <span class="rating-chip" style="background:{color}">{p['rating']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


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


@st.cache_data(ttl=30, show_spinner=False)
def fetch_match_detail(match_id):
    """Fetch a single match's real data from the free-tier API.
    Note: lineups/player ratings are NOT part of the free-tier response."""
    if not API_KEY:
        return None, "missing_key"

    headers = {"X-Auth-Token": API_KEY}
    try:
        response = requests.get(
            f"{API_BASE}/matches/{match_id}", headers=headers, timeout=10
        )
    except requests.exceptions.ConnectionError:
        return None, "connection_error"
    except requests.exceptions.Timeout:
        return None, "timeout"
    except requests.exceptions.RequestException as exc:
        return None, f"request_error: {exc}"

    if response.status_code == 429:
        return None, "rate_limited"
    if response.status_code == 403:
        return None, "forbidden"
    if response.status_code != 200:
        return None, f"http_{response.status_code}"

    try:
        return response.json(), None
    except ValueError:
        return None, "bad_json"


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
# NAVIGATION HELPER
# ---------------------------------------------------------------------------
def go_to_match(match_id):
    st.session_state["selected_match_id"] = match_id
    st.session_state["selected_match_status"] = None


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
    match_id = match.get("id")

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
                    u
