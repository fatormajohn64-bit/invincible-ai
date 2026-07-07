"""
2_🌍_World_News.py
====================
Premium, dark-themed global news dashboard powered by the free tier of
GNews.io. Strict country filtering + fallback search for countries not
covered by GNews's top-headlines endpoint + in-app "Read More" expansion.
"""

from datetime import datetime, timezone

import requests
import streamlit as st

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="World News",
    page_icon="🌍",
    layout="wide",
)

API_BASE = "https://gnews.io/api/v4"
API_KEY = st.secrets.get("GNEWS_API_KEY", "")

# ---------------------------------------------------------------------------
# DESIGN TOKENS (matches Live Scores theme)
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

    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
    .stApp {{ background: {INK}; }}

    section[data-testid="stSidebar"] {{
        background: {SURFACE};
        border-right: 1px solid {LINE};
    }}

    h1, h2, h3 {{
        font-family: 'Space Grotesk', sans-serif !important;
        color: {TEXT} !important;
        letter-spacing: -0.02em;
    }}

    /* Breaking ticker */
    .ticker-wrap {{
        background: linear-gradient(90deg, rgba(255,107,94,0.14), rgba(155,140,255,0.10));
        border: 1px solid {LINE};
        border-radius: 10px;
        padding: 8px 14px;
        margin-bottom: 18px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: {TEXT};
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .ticker-dot {{
        width: 8px; height: 8px; border-radius: 50%;
        background: {CORAL};
        animation: pulse 1.4s ease-in-out infinite;
        flex-shrink: 0;
    }}
    @keyframes pulse {{
        0%   {{ box-shadow: 0 0 0 0 rgba(255,107,94,0.55); }}
        70%  {{ box-shadow: 0 0 0 7px rgba(255,107,94,0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(255,107,94,0); }}
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: {SURFACE};
        border: 1px solid {LINE} !important;
        border-radius: 16px;
        transition: border-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease;
        overflow: hidden;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
        border-color: {SIGNAL} !important;
        box-shadow: 0 8px 28px rgba(40, 224, 196, 0.10);
        transform: translateY(-2px);
    }}

    .news-eyebrow {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.66rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: {MUTED};
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    .badge {{
        display: inline-flex;
        align-items: center;
        gap: 5px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.64rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        padding: 3px 9px;
        border-radius: 999px;
        background: rgba(40, 224, 196, 0.14);
        color: {SIGNAL};
    }}

    .news-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.05rem;
        color: {TEXT};
        line-height: 1.3;
        margin: 8px 0 6px 0;
    }}

    .news-desc {{
        font-size: 0.85rem;
        color: {MUTED};
        line-height: 1.45;
        margin-bottom: 10px;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
    }}

    .news-meta {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: {MUTED};
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 8px;
        border-top: 1px solid {LINE};
    }}

    .no-image-fallback {{
        width: 100%;
        height: 160px;
        background: {SURFACE_2};
        display: flex;
        align-items: center;
        justify-content: center;
        color: {MUTED};
        font-size: 2rem;
    }}

    a.news-link {{ text-decoration: none !important; font-weight: 600; }}

    .fallback-note {{
        background: rgba(242, 184, 75, 0.08);
        border: 1px dashed rgba(242, 184, 75, 0.4);
        border-radius: 10px;
        padding: 10px 14px;
        font-size: 0.8rem;
        color: {GOLD};
        margin-bottom: 14px;
    }}

    .full-content-box {{
        background: {SURFACE_2};
        border: 1px solid {LINE};
        border-radius: 10px;
        padding: 12px 14px;
        font-size: 0.85rem;
        color: {TEXT};
        line-height: 1.55;
        margin-top: 4px;
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

    .empty-state {{
        text-align: center;
        padding: 3rem 1rem;
        color: {MUTED};
        font-family: 'Inter', sans-serif;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# CATEGORY CATALOG
# ---------------------------------------------------------------------------
CATEGORIES = {
    "general": "🌎 Top Stories",
    "world": "🗺️ World",
    "nation": "🏛️ Politics",
    "business": "💼 Business",
    "technology": "💻 Technology",
    "entertainment": "🎬 Entertainment",
    "sports": "⚽ Sports",
    "science": "🔬 Science",
    "health": "🩺 Health",
}

# Countries GNews's top-headlines endpoint actually supports on the free tier.
TOPHEADLINE_SUPPORTED = {
    "au", "br", "ca", "cn", "eg", "fr", "de", "gr", "hk", "in", "ie", "il",
    "it", "jp", "nl", "no", "pk", "pe", "ph", "pt", "ro", "ru", "sg", "es",
    "se", "ch", "tw", "ua", "gb", "us",
}

# Large practical country list (name -> ISO code). Any code NOT in
# TOPHEADLINE_SUPPORTED automatically falls back to keyword search.
COUNTRIES = {
    "🌐 All Countries": "",
    "🇺🇸 United States": "us", "🇬🇧 United Kingdom": "gb", "🇮🇳 India": "in",
    "🇦🇺 Australia": "au", "🇨🇦 Canada": "ca", "🇩🇪 Germany": "de",
    "🇫🇷 France": "fr", "🇪🇬 Egypt": "eg", "🇨🇳 China": "cn",
    "🇬🇷 Greece": "gr", "🇭🇰 Hong Kong": "hk", "🇮🇪 Ireland": "ie",
    "🇮🇱 Israel": "il", "🇮🇹 Italy": "it", "🇯🇵 Japan": "jp",
    "🇳🇱 Netherlands": "nl", "🇳🇴 Norway": "no", "🇵🇰 Pakistan": "pk",
    "🇵🇪 Peru": "pe", "🇵🇭 Philippines": "ph", "🇵🇹 Portugal": "pt",
    "🇷🇴 Romania": "ro", "🇷🇺 Russia": "ru", "🇸🇬 Singapore": "sg",
    "🇪🇸 Spain": "es", "🇸🇪 Sweden": "se", "🇨🇭 Switzerland": "ch",
    "🇹🇼 Taiwan": "tw", "🇺🇦 Ukraine": "ua", "🇧🇷 Brazil": "br",
    # --- Not natively supported by GNews top-headlines: auto-fallback to search ---
    "🇸🇱 Sierra Leone": "sl", "🇳🇬 Nigeria": "ng", "🇰🇪 Kenya": "ke",
    "🇬🇭 Ghana": "gh", "🇿🇦 South Africa": "za", "🇸🇦 Saudi Arabia": "sa",
    "🇦🇪 UAE": "ae", "🇹🇷 Turkey": "tr", "🇲🇽 Mexico": "mx",
    "🇦🇷 Argentina": "ar", "🇮🇩 Indonesia": "id", "🇲🇾 Malaysia": "my",
    "🇻🇳 Vietnam": "vn", "🇧🇩 Bangladesh": "bd", "🇪🇹 Ethiopia": "et",
    "🇺🇬 Uganda": "ug", "🇹🇿 Tanzania": "tz", "🇿🇼 Zimbabwe": "zw",
    "🇱🇷 Liberia": "lr", "🇬🇲 Gambia": "gm", "🇸🇳 Senegal": "sn",
    "🇨🇮 Ivory Coast": "ci", "🇨🇲 Cameroon": "cm", "🇲🇦 Morocco": "ma",
    "🇩🇿 Algeria": "dz", "🇹🇳 Tunisia": "tn", "🇶🇦 Qatar": "qa",
    "🇰🇼 Kuwait": "kw", "🇱🇧 Lebanon": "lb", "🇯🇴 Jordan": "jo",
    "🇮🇶 Iraq": "iq", "🇮🇷 Iran": "ir", "🇰🇷 South Korea": "kr",
    "🇹🇭 Thailand": "th", "🇳🇿 New Zealand": "nz", "🇨🇱 Chile": "cl",
    "🇨🇴 Colombia": "co", "🇻🇪 Venezuela": "ve",
}

COUNTRY_DISPLAY_NAME = {v: k.split(" ", 1)[1] if v else "the World" for k, v in COUNTRIES.items()}


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
def time_ago(published_at: str) -> str:
    try:
        pub = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        diff = datetime.now(timezone.utc) - pub
        secs = diff.total_seconds()
        if secs < 3600:
            return f"{int(secs // 60)}m ago"
        if secs < 86400:
            return f"{int(secs // 3600)}h ago"
        return f"{int(secs // 86400)}d ago"
    except Exception:
        return ""


def dedupe_articles(articles: list) -> list:
    seen_urls, seen_titles, out = set(), set(), []
    for a in articles:
        url = a.get("url", "")
        title = (a.get("title") or "").strip().lower()
        if url in seen_urls or title in seen_titles:
            continue
        seen_urls.add(url)
        seen_titles.add(title)
        out.append(a)
    return out


# ---------------------------------------------------------------------------
# API CONDUIT
# ---------------------------------------------------------------------------
@st.cache_data(ttl=300, show_spinner=False)
def fetch_news(category: str, country_code: str, query: str, max_results: int = 24):
    """
    Strict country filtering:
    - If a country is selected AND supported by top-headlines -> use it directly.
    - If a country is selected but NOT supported -> fall back to the search
      endpoint, forcing the country name into the query so results stay
      relevant to that country instead of silently blending in everything.
    - If no country selected -> normal top-headlines by category (or search
      if the user typed a keyword).
    """
    if not API_KEY:
        return [], "missing_key", None

    fallback_used = False

    if country_code and country_code not in TOPHEADLINE_SUPPORTED:
        # Fallback: search endpoint, keyword = country name (+ optional user query/category)
        fallback_used = True
        country_name = COUNTRY_DISPLAY_NAME.get(country_code, country_code)
        search_terms = country_name
        if query:
            search_terms += f" {query}"
        elif category != "general":
            search_terms += f" {category}"

        params = {"token": API_KEY, "lang": "en", "max": max_results, "q": search_terms}
        endpoint = "search"
    elif query:
        params = {"token": API_KEY, "lang": "en", "max": max_results, "q": query}
        if country_code:
            params["country"] = country_code
        endpoint = "search"
    else:
        params = {"token": API_KEY, "lang": "en", "max": max_results, "category": category}
        if country_code:
            params["country"] = country_code
        endpoint = "top-headlines"

    try:
        res = requests.get(f"{API_BASE}/{endpoint}", params=params, timeout=10)
    except Exception as e:
        return [], str(e), fallback_used

    if res.status_code != 200:
        return [], f"Error {res.status_code}: {res.text[:150]}", fallback_used

    try:
        articles = res.json().get("articles", [])
        return dedupe_articles(articles), None, fallback_used
    except ValueError:
        return [], "bad_json", fallback_used


# ---------------------------------------------------------------------------
# UI COMPONENTS
# ---------------------------------------------------------------------------
def render_article_card(article: dict, idx: int):
    title = article.get("title", "Untitled")
    desc = article.get("description") or ""
    content = article.get("content") or ""
    url = article.get("url", "#")
    image = article.get("image")
    source = article.get("source", {}).get("name", "Unknown")
    published = article.get("publishedAt", "")

    with st.container(border=True):
        if image:
            st.image(image, use_container_width=True)
        else:
            st.markdown('<div class="no-image-fallback">📰</div>', unsafe_allow_html=True)

        st.markdown(
            f'''
            <div style="padding: 12px 14px 4px 14px;">
                <div class="news-eyebrow">
                    <span class="badge">🔥 {source}</span>
                    <span>{time_ago(published)}</span>
                </div>
                <div class="news-title">{title}</div>
                <div class="news-desc">{desc}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

        with st.container():
            col1, col2 = st.columns([1, 1])
            with col1:
                with st.expander("📖 Read More"):
                    full_text = content if len(content) > len(desc) else desc
                    st.markdown(f'<div class="full-content-box">{full_text}</div>', unsafe_allow_html=True)
                    st.caption("GNews free tier truncates full article bodies — tap the link below for the complete story.")
            with col2:
                st.markdown(
                    f'<div style="padding-top:8px;"><a class="news-link" href="{url}" target="_blank" style="color:{SIGNAL};">Open source →</a></div>',
                    unsafe_allow_html=True,
                )
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# MAIN APP LOOP
# ---------------------------------------------------------------------------
def main():
    st.markdown(
        '''
        <div class="ticker-wrap">
            <span class="ticker-dot"></span>
            <span>LIVE &nbsp;•&nbsp; Global headlines refresh every 5 minutes &nbsp;•&nbsp; Pick a country for strictly local news</span>
        </div>
        ''',
        unsafe_allow_html=True,
    )
    st.title("🌍 Global News Feed")

    if not API_KEY:
        st.error("Missing GNEWS_API_KEY in Streamlit Secrets. Add it to `.streamlit/secrets.toml`.")
        return

    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ News Filters")

    selected_category_label = st.sidebar.selectbox("📂 Category", options=list(CATEGORIES.values()), index=0)
    selected_category = [k for k, v in CATEGORIES.items() if v == selected_category_label][0]

    selected_country_label = st.sidebar.selectbox("🌐 Country", options=list(COUNTRIES.keys()), index=0)
    selected_country = COUNTRIES[selected_country_label]

    search_query = st.sidebar.text_input("🔍 Search keyword (optional)", value="")

    if st.sidebar.button("🔄 Refresh Feed"):
        st.cache_data.clear()

    articles, err, fallback_used = fetch_news(selected_category, selected_country, search_query.strip())

    if err == "missing_key":
        st.error("Missing GNEWS_API_KEY in Streamlit Secrets.")
        return
    if err:
        st.error(f"Error fetching news: {err}")
        return

    if fallback_used:
        st.markdown(
            f'<div class="fallback-note">⚠️ GNews\'s free plan doesn\'t index top-headlines directly for '
            f'{COUNTRY_DISPLAY_NAME.get(selected_country, selected_country)}, so results below are pulled via '
            f'keyword search for that country instead.</div>',
            unsafe_allow_html=True,
        )

    if not articles:
        st.markdown(
            f'<div class="empty-state">No news found for {COUNTRY_DISPLAY_NAME.get(selected_country, "the world")}. '
            f'Try a different category or clear the search keyword.</div>',
            unsafe_allow_html=True,
        )
        return

    st.caption(f"Showing {len(articles)} hot stories • {selected_category_label} • {selected_country_label}")

    cols = st.columns(3)
    for i, article in enumerate(articles):
        with cols[i % 3]:
            render_article_card(article, i)


if __name__ == "__main__":
    main()
