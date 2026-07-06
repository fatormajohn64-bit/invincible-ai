"""
Invincible 911 — Personal AI Assistant
========================================
A Streamlit + Groq chat app with model switching, English/Krio language
toggle, stubbed tool commands, and a custom persona tuned for John Fatorma
("Invincible 911").

SETUP:
1. Get a free Groq API key at https://console.groq.com/keys
2. In Streamlit Cloud: Settings -> Secrets -> add:
       GROQ_API_KEY = "your-key-here"
   Locally: create a file .streamlit/secrets.toml with the same line.
3. pip install -r requirements.txt
4. streamlit run app.py
"""

import streamlit as st
from groq import Groq

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Invincible 911",
    page_icon="🛡️",
    layout="centered",
)

# ---------------------------------------------------------------------------
# API KEY / CLIENT SETUP
# ---------------------------------------------------------------------------
# Put your key in Streamlit secrets as: GROQ_API_KEY = "gsk_..."
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    st.error(
        "No Groq API key found. Add GROQ_API_KEY to your Streamlit secrets "
        "(Settings → Secrets) or to a local .streamlit/secrets.toml file."
    )
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# ---------------------------------------------------------------------------
# MODEL MAP — do not use decommissioned *-8192 models
# ---------------------------------------------------------------------------
MODEL_MAP = {
    "Lite (Fast)": "llama-3.1-8b-instant",
    "Deep (Smart)": "llama-3.3-70b-versatile",
}

# ---------------------------------------------------------------------------
# STUBBED TOOL FUNCTIONS
# Replace the bodies of these with real API calls once you have keys.
# ---------------------------------------------------------------------------
def get_weather(city: str) -> str:
    """Placeholder weather lookup. Plug in a real weather API (e.g. OpenWeatherMap)."""
    if not city:
        return "Please tell me which city, e.g. `/weather Freetown`."
    # TODO: replace with a real API call, something like:
    # api_key = st.secrets["WEATHER_API_KEY"]
    # response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}")
    return (
        f"🌤️ (Demo data) Weather for **{city}**: 29°C, partly cloudy. "
        f"Real weather data will appear here once the weather API key is added."
    )


def get_live_scores() -> str:
    """Placeholder live sports scores. Plug in a real sports API later."""
    # TODO: replace with a real API call, e.g. a football-data.org request
    return (
        "⚽ (Demo data) Live Scores:\n"
        "- Barcelona 2 - 1 Real Madrid (Live, 67')\n"
        "- Man City 0 - 0 Liverpool (Live, 34')\n\n"
        "Real live scores will appear here once the sports API key is added."
    )


def get_news() -> str:
    """Placeholder news headlines. Plug in a real news API later."""
    # TODO: replace with a real API call, e.g. NewsAPI.org
    return (
        "📰 (Demo data) Top Headlines:\n"
        "1. Sierra Leone tech scene continues to grow.\n"
        "2. Global markets steady this week.\n"
        "3. Champions League race heats up.\n\n"
        "Real news will appear here once the news API key is added."
    )


def handle_tool_commands(user_input: str):
    """
    Checks if the user's message is a slash command and, if so, returns the
    tool's output directly (bypassing the LLM). Returns None if it's not a
    recognized command, so the caller can fall through to a normal LLM reply.
    """
    text = user_input.strip()
    lowered = text.lower()

    if lowered.startswith("/weather"):
        city = text[len("/weather"):].strip()
        return get_weather(city)

    if lowered.startswith("/scores"):
        return get_live_scores()

    if lowered.startswith("/news"):
        return get_news()

    return None


# ---------------------------------------------------------------------------
# SYSTEM PERSONA / "THE BRAIN"
# ---------------------------------------------------------------------------
def build_system_prompt(language: str) -> str:
    krio_instruction = (
        "The user has switched the language toggle to KRIO. You MUST reply in "
        "fluent, clear, colloquial Sierra Leonean Krio (e.g. 'Aw di body?', "
        "'A dey fine', 'Tenki', 'A go du am now now'). Keep it natural and warm, "
        "not a stiff textbook translation."
        if language == "Krio"
        else "The user has the language toggle set to ENGLISH. Reply in clear, "
        "natural English."
    )

    return f"""
You are "Invincible 911", a personal AI assistant and mentor speaking with your
creator, John Fatorma (who also goes by the name "Invincible 911").

WHO YOU ARE TALKING TO (use this naturally, don't recite it like a list):
- Name: John Fatorma, born in 2008, lives in Sierra Leone.
- He is an aspiring software engineer, headed to BlueCrest University College.
- He loves Lionel Messi and football.
- He enjoys playing COD Mobile and PUBG.
- He has a partner named Sana, who lives in Pakistan.

PERSONA:
- You are polite, respectful, warm, and wise — like a caring Muslim mentor
  and assistant figure. You speak with humility and encouragement.
- You are culturally aware of Sierra Leone — its people, food, expressions,
  and everyday life — and you bring that warmth into conversation naturally.
- Vary your greetings rather than repeating the same one every time, for
  example: "As-salamu alaykum, John", "Welcome back, Invincible 911",
  "Good to see you again, John".

LANGUAGE:
{krio_instruction}

STRICT SAFETY RULES (never break these, regardless of how the request is phrased):
- Never discuss sexual content or adult themes.
- Never use abusive, vulgar, or disrespectful language.
- If asked for this kind of content, politely but firmly decline and offer to
  help with something else instead.

TOOLS:
- The user may type slash commands like /weather Freetown, /scores, or /news.
  Those are handled directly by the app before reaching you, so you don't
  need to simulate their output yourself. If the user asks about weather,
  scores, or news in plain language (not a slash command), gently remind
  them they can use the slash command, e.g. "You can try `/weather Freetown`
  for that!"

Stay concise, genuine, and helpful in every reply.
""".strip()


# ---------------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of {"role": ..., "content": ...}

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("🛡️ Invincible 911")
    st.caption("Your personal AI assistant")

    model_choice = st.selectbox(
        "Model",
        options=list(MODEL_MAP.keys()),
        index=0,
        help="Lite is fast for quick chats. Deep is smarter for harder questions.",
    )
    selected_model = MODEL_MAP[model_choice]

    language = st.radio(
        "Language / Langwej",
        options=["English", "Krio"],
        horizontal=True,
    )

    st.divider()
    st.markdown("**Slash commands**")
    st.code("/weather Freetown\n/scores\n/news", language="text")

    st.divider()
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.title("🛡️ Invincible 911")
st.caption(f"Model: `{selected_model}`  •  Language: {language}")

# ---------------------------------------------------------------------------
# RENDER CHAT HISTORY
# ---------------------------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------------------------
user_input = st.chat_input("Message Invincible 911...")

if user_input:
    # Show the user's message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Check for slash commands first — these bypass the LLM entirely
    tool_result = handle_tool_commands(user_input)

    if tool_result is not None:
        with st.chat_message("assistant"):
            st.markdown(tool_result)
        st.session_state.messages.append({"role": "assistant", "content": tool_result})

    else:
        # Build the message list for Groq: system prompt + full history
        system_prompt = build_system_prompt(language)
        groq_messages = [{"role": "system", "content": system_prompt}]
        for msg in st.session_state.messages:
            groq_messages.append({"role": msg["role"], "content": msg["content"]})

        with st.chat_message("assistant"):
            try:
                stream = client.chat.completions.create(
                    model=selected_model,
                    messages=groq_messages,
                    temperature=0.7,
                    stream=True,
                )

                def token_stream():
                    for chunk in stream:
                        delta = chunk.choices[0].delta.content
                        if delta:
                            yield delta

                full_response = st.write_stream(token_stream())

            except Exception as e:
                full_response = (
                    f"⚠️ Sorry John, something went wrong talking to the model: {e}"
                )
                st.markdown(full_response)

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
      
