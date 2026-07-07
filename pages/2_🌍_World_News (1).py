"""
2_🌍_World_News.py
====================
Premium, dark-themed global news dashboard powered by the free tier of
GNews.io. Built for a multipage Streamlit app (matches Live Scores theme).
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
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
        overflow: hidden;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
        border-color: #323952 !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }}

    .news-eyebrow {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
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
        font-size: 0.65rem;
        font-weight: 500;
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
        border-radius: 10px 10px 0 0;
    }}

    a.news-link {{
        text-decoration: none !important;
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
# CATEGORY / COUNTRY CATALOG
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

COUNTRIES = {
    "": "🌐 All Countries",
    "us": "🇺🇸 United States",
    "gb": "🇬🇧 United Kingdom",
    "in": "🇮🇳 India",
    "au": "🇦🇺 Australia",
    "ca": "🇨🇦 Canada",
    "de": "🇩🇪 Germany",
    "fr": "🇫🇷 France",
    "eg": "🇪🇬 Egypt",
    "sa": "🇸🇦 Saudi Arabia",
    "ae": "🇦🇪 UAE",
    "pk": "🇵🇰 Pakistan",
    "ng": "🇳🇬 Nigeria",
    "za": "🇿🇦 South Africa",
    "br": "🇧🇷 Brazil",
    "jp": "🇯🇵 Japan",
}


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


# ---------------------------------------------------------------------------
# API CONDUIT
# ---------------------------------------------------------------------------
@st.cache_data(ttl=300, show_spinner=False)
def fetch_news(category: str, country: str, query: str, max_results: int = 24):
    if not API_KEY:
        return [], "missing_key"

    endpoint = "search" if query else "top-headlines"
    params = {
        "token": API_KEY,
        "lang": "en",
        "max": max_results,
    }
    if query:
        params["q"] = query
    else:
        params["category"] = category
    if country:
        params["country"] = country

    try:
        res = requests.get(f"{API_BASE}/{endpoint}", params=params, timeout=10)
    except Exception as e:
        return [], str(e)

    if res.status_code != 200:
        return [], f"Error {res.status_code}: {res.text[:150]}"

    try:
        return res.json().get("articles", []), None
    except ValueError:
        return [], "bad_json"


# ---------------------------------------------------------------------------
# UI COMPONENTS
# ---------------------------------------------------------------------------
def render_article_card(article: dict):
    title = article.get("title", "Untitled")
    desc = article.get("description") or ""
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
            <div style="padding: 12px 14px 14px 14px;">
                <div class="news-eyebrow">
                    <span class="badge">🔥 {source}</span>
                    <span>{time_ago(published)}</span>
                </div>
                <div class="news-title">{title}</div>
                <div class="news-desc">{desc}</div>
                <div class="news-meta">
                    <a class="news-link" href="{url}" target="_blank" style="color:{SIGNAL};">Read full article →</a>
                </div>
            </div>
            ''',
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# MAIN APP LOOP
# ---------------------------------------------------------------------------
def main():
    st.title("🌍 Global News Feed")

    if not API_KEY:
        st.error("Missing GNEWS_API_KEY in Streamlit Secrets. Add it to `.streamlit/secrets.toml`.")
        return

    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ News Filters")

    selected_category_label = st.sidebar.selectbox(
        "📂 Category",
        options=list(CATEGORIES.values()),
        index=0,
    )
    selected_category = [k for k, v in CATEGORIES.items() if v == selected_category_label][0]

    selected_country_label = st.sidebar.selectbox(
        "🌐 Country",
        options=list(COUNTRIES.values()),
        index=0,
    )
    selected_country = [k for k, v in COUNTRIES.items() if v == selected_country_label][0]

    search_query = st.sidebar.text_input("🔍 Search keyword (optional)", value="")

    if st.sidebar.button("🔄 Refresh Feed"):
        st.cache_data.clear()

    articles, err = fetch_news(selected_category, selected_country, search_query.strip())

    if err == "missing_key":
        st.error("Missing GNEWS_API_KEY in Streamlit Secrets.")
        return
    if err:
        st.error(f"Error fetching news: {err}")
        return

    if not articles:
        st.markdown(
            '<div class="empty-state">No news found. Try a different search term or country.</div>',
            unsafe_allow_html=True,
        )
        return

    st.caption(f"Showing {len(articles)} hot stories • {selected_category_label} • {selected_country_label}")

    # 3-column responsive grid
    cols = st.columns(3)
    for i, article in enumerate(articles):
        with cols[i % 3]:
            render_article_card(article)


if __name__ == "__main__":
    main()
