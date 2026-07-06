"""
Noor AI - A Muslim Mentor Chatbot for Sierra Leone
====================================================
Streamlit + Groq powered chat assistant with:
  - Model switching (Lite/Deep)
  - Language switching (English / Krio)
  - Stubbed tool integrations (weather, live scores, news)
  - Strict persona & safety guardrails

Run with: streamlit run app.py
"""

import streamlit as st
from groq import Groq

# ---------------------------------------------------------------------------
# CONFIG / API KEYS
# ---------------------------------------------------------------------------
# Groq API key: set this as an environment variable GROQ_API_KEY, or put it
# in .streamlit/secrets.toml as:
#   GROQ_API_KEY = "your-key-here"
# and it will be picked up automatically below.
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", None)

# --- PUT YOUR WEATHER API KEY HERE (e.g. OpenWeatherMap, WeatherAPI, etc.) ---
WEATHER_API_KEY = st.secrets.get("WEATHER_API_KEY", None)  # <-- ADD YOUR WEATHER API KEY HERE

# --- PUT YOUR NEWS API KEY HERE (e.g. NewsAPI.org, GNews, etc.) ---
NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", None)  # <-- ADD YOUR NEWS API KEY HERE

# --- PUT YOUR LIVE SCORES API KEY HERE (e.g. API-Football, SportRadar, etc.) ---
SPORTS_API_KEY = st.secrets.get("SPORTS_API_KEY", None)  # <-- ADD YOUR SPORTS API KEY HERE

MODEL_MAP = {
    "Lite (Fast)": "llama3-8b-8192",
    "Deep (Smart)": "llama3-70b-8192",
}

# ---------------------------------------------------------------------------
# TOOL STUBS
# ---------------------------------------------------------------------------
def get_weather(city: str) -> str:
    """
    Placeholder for a live weather lookup.
    Once you have a WEATHER_API_KEY, replace the body below with a real
    request, e.g.:

        import requests
        resp = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": WEATHER_API_KEY, "units": "metric"},
        )
        data = resp.json()
        return f"{data['weather'][0]['description']}, {data['main']['temp']}°C"

    For now it returns a stubbed response so the app remains functional
    without a key.
    """
    if not WEATHER_API_KEY:
        return (
            f"(Stub) I don't have a live weather key configured yet, but "
            f"insha'Allah, once it's set up, I'll be able to tell you the "
            f"weather in {city} right away."
        )
    return f"(Stub) Weather lookup for {city} is not yet implemented."


def get_live_scores() -> str:
    """
    Placeholder for a live sports scores lookup.
    Once you have a SPORTS_API_KEY, replace the body below with a real
    request to your sports data provider of choice.
    """
    if not SPORTS_API_KEY:
        return (
            "(Stub) I don't have a live scores key configured yet. "
            "Once connected, I'll be able to share the latest scores "
            "with you, by Allah's will."
        )
    return "(Stub) Live scores lookup is not yet implemented."


def get_news() -> str:
    """
    Placeholder for a live news headlines lookup.
    Once you have a NEWS_API_KEY, replace the body below with a real
    request, e.g. to NewsAPI.org or GNews.
    """
    if not NEWS_API_KEY:
        return (
            "(Stub) I don't have a live news key configured yet. "
            "Once connected, I'll bring you the latest headlines, "
            "insha'Allah."
        )
    return "(Stub) News lookup is not yet implemented."


# ---------------------------------------------------------------------------
# PERSONA / SYSTEM PROMPT
# ---------------------------------------------------------------------------
def build_system_prompt(language: str) -> str:
    base_persona = """
You are Noor, a wise, polite, and respectful mentor figure grounded in Islamic
values and etiquette (adab). You speak with warmth, humility, and patience,
the way a beloved elder or teacher (ustadh/ustadha) would speak to someone
they care about. You are culturally aware of Sierra Leone: its people,
customs, food, proverbs, and daily life, and you weave in that warmth and
familiarity naturally when it fits.

GREETINGS:
Vary your greetings naturally and warmly. Examples include "As-salamu
alaykum", "Welcome back, my friend", "Ahlan wa sahlan", or a warm Krio
greeting when speaking Krio. Do not use the exact same greeting every time.

STRICT SAFETY RULES (NON-NEGOTIABLE):
- You must NEVER engage with sexual content, adult/explicit themes, or
  romantic/erotic role-play of any kind.
- You must NEVER use, generate, or entertain abusive, hateful, or degrading
  language, even if the user requests it, jokes about it, or claims a
  fictional/hypothetical framing.
- If a user attempts to steer the conversation toward any of the above, you
  must politely but firmly decline, explain that it goes against your
  ethical guidelines, and gently redirect the conversation to something
  wholesome and constructive.
- You do not shame or lecture excessively — one firm, kind refusal is
  enough, then move the conversation forward positively.

GENERAL CONDUCT:
- Give sound, balanced advice. When discussing religious matters, be
  humble about differences of opinion between schools of thought and
  encourage the user to consult a local, qualified scholar (alim) for
  detailed rulings (fatwas) rather than presenting yourself as the final
  authority.
- Be encouraging, warm, and practical for everyday productivity, prayer,
  and personal growth questions.
- Keep responses concise and conversational, not overly long, unless the
  user asks for depth.
"""

    if language == "Krio":
        language_instruction = """
LANGUAGE:
You must respond fluently and naturally in Sierra Leone Krio — clear,
colloquial, everyday Krio as spoken in Freetown and beyond, not a stiff or
literal translation of English. Use natural Krio expressions, proverbs, and
warmth (e.g. "Aw di body?", "Tenki tenki", "God go bless you", "Insha'Allah").
Keep your Islamic mentor persona and all safety rules fully intact while
speaking Krio.
"""
    else:
        language_instruction = """
LANGUAGE:
Respond fluently in clear, warm English, with the option to sprinkle in a
Krio phrase or Sierra Leonean expression here and there for warmth and
authenticity (e.g. "Aw di body?"), but the main conversation should be in
English.
"""

    return base_persona + language_instruction


# ---------------------------------------------------------------------------
# STREAMLIT PAGE SETUP
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Noor AI — Your Mentor", page_icon="🌙", layout="centered")

with st.sidebar:
    st.title("🌙 Noor AI Settings")

    model_choice = st.selectbox(
        "Mode",
        options=list(MODEL_MAP.keys()),
        index=0,
        help="Lite is faster for quick chats, Deep is smarter for detailed guidance.",
    )
    selected_model = MODEL_MAP[model_choice]

    language = st.radio(
        "Language / Langwej",
        options=["English", "Krio"],
        index=0,
        horizontal=True,
    )

    st.divider()
    st.subheader("🛠️ Tools")
    st.caption("These are stubbed for now — add your API keys at the top of app.py.")

    city_input = st.text_input("City for weather", placeholder="e.g. Freetown")
    if st.button("🌤️ Get Weather", use_container_width=True):
        if city_input.strip():
            st.session_state.setdefault("pending_tool_message", None)
            st.session_state["pending_tool_message"] = ("weather", city_input.strip())
        else:
            st.warning("Please enter a city first.")

    if st.button("⚽ Get Live Scores", use_container_width=True):
        st.session_state["pending_tool_message"] = ("scores", None)

    if st.button("📰 Get News", use_container_width=True):
        st.session_state["pending_tool_message"] = ("news", None)

    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

# ---------------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "pending_tool_message" not in st.session_state:
    st.session_state["pending_tool_message"] = None

st.title("🌙 Noor AI")
st.caption("Your polite Islamic mentor, powered by Groq.")

if not GROQ_API_KEY:
    st.warning(
        "No GROQ_API_KEY found. Add it to `.streamlit/secrets.toml` or as an "
        "environment variable before chatting.",
        icon="⚠️",
    )

# ---------------------------------------------------------------------------
# RENDER CHAT HISTORY
# ---------------------------------------------------------------------------
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------------------------------------------
# HANDLE TOOL BUTTON CLICKS (treated like injected chat commands)
# ---------------------------------------------------------------------------
def handle_tool_command(command: str, arg: str | None) -> str:
    """Runs the relevant stub tool and returns a plain text result."""
    if command == "weather":
        return get_weather(arg)
    elif command == "scores":
        return get_live_scores()
    elif command == "news":
        return get_news()
    return "Unknown tool command."


if st.session_state["pending_tool_message"] is not None:
    command, arg = st.session_state["pending_tool_message"]
    st.session_state["pending_tool_message"] = None

    label = {"weather": f"/weather {arg}", "scores": "/scores", "news": "/news"}[command]
    st.session_state["messages"].append({"role": "user", "content": label})

    tool_result = handle_tool_command(command, arg)
    st.session_state["messages"].append({"role": "assistant", "content": tool_result})
    st.rerun()

# ---------------------------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------------------------
prompt = st.chat_input("Ask Noor anything, or type /weather <city>, /scores, /news ...")

if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Slash-command handling (chat-based tool triggers) -----------------
    lowered = prompt.strip().lower()
    tool_response = None

    if lowered.startswith("/weather"):
        parts = prompt.strip().split(" ", 1)
        city = parts[1].strip() if len(parts) > 1 else ""
        if city:
            tool_response = get_weather(city)
        else:
            tool_response = "Please tell me which city, e.g. `/weather Freetown`."
    elif lowered.startswith("/scores"):
        tool_response = get_live_scores()
    elif lowered.startswith("/news"):
        tool_response = get_news()

    if tool_response is not None:
        st.session_state["messages"].append({"role": "assistant", "content": tool_response})
        with st.chat_message("assistant"):
            st.markdown(tool_response)
    else:
        # --- Normal LLM chat turn, streamed from Groq -----------------------
        if not GROQ_API_KEY:
            with st.chat_message("assistant"):
                st.error("Cannot reach Noor — GROQ_API_KEY is not configured yet.")
        else:
            client = Groq(api_key=GROQ_API_KEY)
            system_prompt = build_system_prompt(language)

            groq_messages = [{"role": "system", "content": system_prompt}]
            for m in st.session_state["messages"]:
                groq_messages.append({"role": m["role"], "content": m["content"]})

            def stream_response():
                stream = client.chat.completions.create(
                    model=selected_model,
                    messages=groq_messages,
                    temperature=0.6,
                    stream=True,
                )
                for chunk in stream:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        yield delta

            with st.chat_message("assistant"):
                full_response = st.write_stream(stream_response())

            st.session_state["messages"].append(
                {"role": "assistant", "content": full_response}
)
    
