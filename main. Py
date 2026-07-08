"""
Invincible 911 — Cyberpunk Terminal Dashboard (v2)
====================================================
A Streamlit + Groq chat app with:
  - Neon cyberpunk dashboard theme (custom CSS injection)
  - Per-message 🔊 Speak + 📋 Copy buttons
  - A ▶️ Play Full Conversation button (queues every AI reply through TTS)
  - A fullscreen "Live Conversation Mode": tap the native mic recorder, speak,
    and Invincible 911 transcribes, replies, and speaks back automatically —
    with a glowing orb that reacts in real time to actual speech-synthesis
    events (not a fake timer).
  - Randomized greetings (Salam variations + Krio + English) fire the moment
    you switch into Live Mode.
  - Original features preserved: model switcher, English/Krio toggle,
    slash commands (/weather, /scores, /news), and the John Fatorma persona.

WHY THIS VERSION CHANGES THE VOICE ENGINE:
The previous build used `webkitSpeechRecognition` inside a
`components.html` iframe, bridged into Streamlit via a hidden-widget DOM
hack. That mic path is fundamentally blocked by browsers: `srcdoc` iframes
(which is what components.html renders) have no origin, and getUserMedia()
is disabled by Permissions Policy in cross-origin/no-origin iframes unless
explicitly allow-listed — which Streamlit doesn't do. That's the
"Script execution error" / dead orb you hit.

This version instead uses Streamlit's own native `st.audio_input` widget
(a first-party mic recorder that is NOT sandboxed the same way) to capture
audio, then sends the recording to Groq's Whisper endpoint for
transcription. This is far more reliable across phones/browsers, and it's
the same approach Streamlit itself recommends for anything mic-related.
Text-to-speech (playback) has no such restriction, so the orb's glow is
still driven by real browser `SpeechSynthesisUtterance` events.

SETUP:
1. Get a free Groq API key at https://console.groq.com/keys
2. In Streamlit Cloud: Settings -> Secrets -> add:
       GROQ_API_KEY = "your-key-here"
   Locally: create a file .streamlit/secrets.toml with the same line.
3. pip install -r requirements.txt   (streamlit, groq)
4. streamlit run app.py
"""

import hashlib
import json
import random
import streamlit as st
import streamlit.components.v1 as components
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

# Whisper model used for Live Mode transcription. If your Groq account
# doesn't have this exact id enabled, swap for "whisper-large-v3".
STT_MODEL = "whisper-large-v3-turbo"

# How many past messages (user+assistant) to actually send to the model.
# Keeps replies fast and focused instead of dragging the whole history
# through every request — this is most of what "make it smarter" means in
# practice: relevant recent context, not everything since the app opened.
MAX_HISTORY_MESSAGES = 20

# ---------------------------------------------------------------------------
# CYBERPUNK THEME — CSS INJECTION
# ---------------------------------------------------------------------------
def inject_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

        :root {
            --bg-void: #030508;
            --bg-slate: #0B0F19;
            --neon-cyan: #00F0FF;
            --neon-violet: #A020F0;
            --neon-green: #39FF14;
            --card-bg: rgba(11, 15, 25, 0.7);
        }

        html, body, [class*="css"] {
            font-family: 'JetBrains Mono', monospace;
        }

        .stApp {
            background: radial-gradient(circle at 20% 0%, #0a0e18 0%, var(--bg-void) 55%);
            color: #E6F7FF;
        }

        section[data-testid="stSidebar"] {
            background: var(--bg-slate);
            border-right: 1px solid rgba(0, 240, 255, 0.25);
        }
        section[data-testid="stSidebar"] * {
            font-family: 'JetBrains Mono', monospace;
        }

        h1, h2, h3 {
            font-family: 'Space Grotesk', sans-serif !important;
            background: linear-gradient(90deg, var(--neon-cyan) 0%, var(--neon-violet) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: 0.5px;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--card-bg);
            border: 1px solid var(--neon-cyan);
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
        }

        div[data-testid="stChatMessage"] {
            background: var(--card-bg);
            border: 1px solid rgba(0, 240, 255, 0.35);
            border-radius: 12px;
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.12);
            padding: 0.6rem 0.9rem;
            margin-bottom: 0.6rem;
        }

        .stButton > button, .stDownloadButton > button {
            background: linear-gradient(90deg, rgba(0,240,255,0.12), rgba(160,32,240,0.12));
            border: 1px solid var(--neon-cyan);
            color: var(--neon-cyan);
            border-radius: 8px;
            font-family: 'JetBrains Mono', monospace;
            transition: all 0.15s ease-in-out;
        }
        .stButton > button:hover, .stDownloadButton > button:hover {
            border-color: var(--neon-violet);
            color: #ffffff;
            box-shadow: 0 0 12px rgba(160, 32, 240, 0.6);
        }

        div[data-testid="stChatInput"] {
            background: var(--card-bg);
            border: 1px solid var(--neon-cyan);
            border-radius: 10px;
            box-shadow: 0 0 12px rgba(0, 240, 255, 0.18);
        }

        div[data-testid="stAudioInput"] {
            background: var(--card-bg);
            border: 1px solid var(--neon-green);
            border-radius: 14px;
            box-shadow: 0 0 18px rgba(57, 255, 20, 0.25);
            padding: 6px;
        }

        .stRadio label, .stSelectbox label, .stCheckbox label {
            color: var(--neon-cyan) !important;
        }

        hr {
            border-color: rgba(0, 240, 255, 0.25);
        }

        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-void); }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(var(--neon-cyan), var(--neon-violet));
            border-radius: 4px;
        }

        .sl-flag-strip {
            text-align: center;
            letter-spacing: 6px;
            font-size: 20px;
            margin: 4px 0 14px 0;
            opacity: 0.9;
            text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# STUBBED TOOL FUNCTIONS
# Replace the bodies of these with real API calls once you have keys.
# ---------------------------------------------------------------------------
def get_weather(city: str) -> str:
    """Placeholder weather lookup. Plug in a real weather API (e.g. WeatherAPI.com)."""
    if not city:
        return "Please tell me which city, e.g. `/weather Freetown`."
    return (
        f"🌤️ (Demo data) Weather for **{city}**: 29°C, partly cloudy. "
        f"Real weather data will appear here once the weather API key is added."
    )


def get_live_scores() -> str:
    """Placeholder live sports scores. Plug in a real sports API later."""
    return (
        "⚽ (Demo data) Live Scores:\n"
        "- Barcelona 2 - 1 Real Madrid (Live, 67')\n"
        "- Man City 0 - 0 Liverpool (Live, 34')\n\n"
        "Real live scores will appear here once the sports API key is added."
    )


def get_news() -> str:
    """Placeholder news headlines. Plug in a real news API later."""
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
- Be genuinely sharp, not just warm: when John asks something technical,
  give a real, specific, correct answer first — mentorship tone comes
  second to actually being useful. Ask one focused follow-up question only
  when it would meaningfully change your answer, not out of habit.
- Keep track of what's already been said in this conversation so you don't
  repeat yourself or ask something John already answered.

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

Stay concise, genuine, and helpful in every reply — this may be read aloud
by text-to-speech, so avoid heavy markdown, tables, or long bullet lists;
write in natural spoken sentences.
""".strip()


# ---------------------------------------------------------------------------
# RANDOMIZED LIVE-MODE GREETINGS
# ---------------------------------------------------------------------------
GREETINGS = [
    "As-salamu alaykum, John! 🕌 Invincible 911 is online — I'm listening.",
    "Salaam, Invincible 911! 🇸🇱 Welcome back to live mode. Speak whenever you're ready.",
    "Wa alaykumu salam, my brother — let's talk. 🎙️",
    "Aw di body, John? 🇸🇱 A dey here for you, live mode don activate now now!",
    "Welcome back, Invincible 911 — live conversation mode is active. ⚡",
    "Salamu alaykum wa rahmatullah, John! Ready when you are. 🕌",
    "Good to hear you again, John! 🎙️ Tap the mic and speak.",
    "Ahlan wa sahlan, John! 🇸🇱 Let's build something great today.",
    "Bo John, aw tin dem de go? 🇸🇱 Live mode don ready, tok to me now.",
]


def random_greeting() -> str:
    return random.choice(GREETINGS)


# ---------------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------------
defaults = {
    "messages": [],
    "live_mode": False,
    "live_greeted": False,
    "last_ai_reply": "",
    "spoken_hash": "",
    "last_audio_hash": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ---------------------------------------------------------------------------
# CORE REPLY LOGIC (shared by text chat and voice mode)
# ---------------------------------------------------------------------------
def _trimmed_history():
    return st.session_state.messages[-MAX_HISTORY_MESSAGES:]


def generate_reply(user_input: str, model: str, language: str) -> str:
    """
    Runs a user message through the slash-command router first, then falls
    back to a non-streamed Groq completion (used by Live Mode, where we need
    the full text at once to hand to TTS). Appends both turns to session
    state and returns the assistant's final text.
    """
    st.session_state.messages.append({"role": "user", "content": user_input})

    tool_result = handle_tool_commands(user_input)
    if tool_result is not None:
        st.session_state.messages.append({"role": "assistant", "content": tool_result})
        return tool_result

    system_prompt = build_system_prompt(language)
    groq_messages = [{"role": "system", "content": system_prompt}]
    for msg in _trimmed_history():
        groq_messages.append({"role": msg["role"], "content": msg["content"]})

    try:
        response = client.chat.completions.create(
            model=model,
            messages=groq_messages,
            temperature=0.7,
        )
        full_response = response.choices[0].message.content
    except Exception as e:
        full_response = f"⚠️ Sorry John, something went wrong talking to the model: {e}"

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    return full_response


def generate_reply_streamed(user_input: str, model: str, language: str) -> str:
    """
    Same as generate_reply, but streams the response into the current
    st.chat_message block (used by the normal text-chat view).
    """
    st.session_state.messages.append({"role": "user", "content": user_input})

    tool_result = handle_tool_commands(user_input)
    if tool_result is not None:
        with st.chat_message("assistant"):
            st.markdown(tool_result)
        st.session_state.messages.append({"role": "assistant", "content": tool_result})
        return tool_result

    system_prompt = build_system_prompt(language)
    groq_messages = [{"role": "system", "content": system_prompt}]
    for msg in _trimmed_history():
        groq_messages.append({"role": msg["role"], "content": msg["content"]})

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=model,
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
            full_response = f"⚠️ Sorry John, something went wrong talking to the model: {e}"
            st.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    return full_response


def transcribe_audio(audio_bytes: bytes) -> str:
    """Sends a recorded clip to Groq's Whisper endpoint and returns the text."""
    try:
        result = client.audio.transcriptions.create(
            file=("live_input.wav", audio_bytes),
            model=STT_MODEL,
        )
        return (result.text or "").strip()
    except Exception as e:
        st.warning(f"⚠️ Couldn't transcribe that clip: {e}")
        return ""


# ---------------------------------------------------------------------------
# INLINE HTML/JS ACTION BUTTONS (speak / copy / play-all)
# ---------------------------------------------------------------------------
def message_action_buttons(text: str, key: str) -> str:
    """Renders a small 🔊 Speak + 📋 Copy row under a message. Safely escaped."""
    safe_text = json.dumps(text)
    return f"""
    <div style="display:flex; gap:8px; margin-top:-6px; margin-bottom:10px;">
      <button onclick='window.speechSynthesis.cancel(); window.speechSynthesis.speak(new SpeechSynthesisUtterance({safe_text}));'
        style="background:linear-gradient(90deg, rgba(0,240,255,0.15), rgba(160,32,240,0.15));
               border:1px solid #00F0FF; color:#00F0FF; border-radius:20px; padding:4px 12px;
               font-family:'JetBrains Mono', monospace; font-size:12px; cursor:pointer;
               box-shadow:0 0 8px rgba(0,240,255,0.25);" id="speak-{key}">
        🔊 Speak
      </button>
      <button onclick='navigator.clipboard.writeText({safe_text}); this.innerText="✅ Copied";
               setTimeout(() => {{ this.innerText = "📋 Copy"; }}, 1500);'
        style="background:linear-gradient(90deg, rgba(160,32,240,0.15), rgba(0,240,255,0.15));
               border:1px solid #A020F0; color:#A020F0; border-radius:20px; padding:4px 12px;
               font-family:'JetBrains Mono', monospace; font-size:12px; cursor:pointer;
               box-shadow:0 0 8px rgba(160,32,240,0.25);" id="copy-{key}">
        📋 Copy
      </button>
    </div>
    """


def play_conversation_button(messages) -> str:
    """A button that queues every assistant reply through TTS, in order."""
    texts = [m["content"] for m in messages if m["role"] == "assistant"]
    if not texts:
        return ""
    safe_array = json.dumps(texts)
    return f"""
    <div style="display:flex; gap:10px; margin-bottom:14px;">
      <button onclick='
          const texts = {safe_array};
          window.speechSynthesis.cancel();
          let i = 0;
          function speakNext() {{
            if (i >= texts.length) return;
            const u = new SpeechSynthesisUtterance(texts[i]);
            u.onend = () => {{ i += 1; speakNext(); }};
            window.speechSynthesis.speak(u);
          }}
          speakNext();
        '
        style="background:linear-gradient(90deg, rgba(57,255,20,0.15), rgba(0,240,255,0.15));
               border:1px solid #39FF14; color:#39FF14; border-radius:20px; padding:6px 16px;
               font-family:'JetBrains Mono', monospace; font-size:13px; cursor:pointer;
               box-shadow:0 0 10px rgba(57,255,20,0.3);">
        ▶️ Play Full Conversation
      </button>
      <button onclick='window.speechSynthesis.cancel();'
        style="background:linear-gradient(90deg, rgba(160,32,240,0.15), rgba(0,240,255,0.15));
               border:1px solid #A020F0; color:#A020F0; border-radius:20px; padding:6px 16px;
               font-family:'JetBrains Mono', monospace; font-size:13px; cursor:pointer;
               box-shadow:0 0 10px rgba(160,32,240,0.3);">
        ⏹️ Stop
      </button>
    </div>
    """


# ---------------------------------------------------------------------------
# LIVE CONVERSATION MODE — ORB SYNCED TO REAL TTS EVENTS
# ---------------------------------------------------------------------------
def speaking_orb_html(text: str, autoplay: bool) -> str:
    """
    Renders the audio orb. If autoplay is True, it speaks `text` immediately
    on load and the orb's glow is driven by the *actual* SpeechSynthesis
    onstart/onend events — not a guessed timer — so the visual state always
    matches what's really playing.
    """
    safe_text = json.dumps(text or "")
    autoplay_js = "speakNow();" if autoplay else ""
    return f"""
    <div id="orb-wrap" style="
        position:relative; display:flex; flex-direction:column; align-items:center;
        justify-content:center; height:480px; background:#030508;
        font-family:'JetBrains Mono', monospace;">

      <style>
        #orb-ring {{ position:relative; width:240px; height:240px; }}
        #orb {{
          width: 220px; height: 220px; border-radius: 50%; margin:10px;
          background: radial-gradient(circle at 35% 30%, #0B0F19, #030508 70%);
          border: 2px solid #00F0FF;
          box-shadow: 0 0 30px rgba(0,240,255,0.3), inset 0 0 24px rgba(0,240,255,0.12);
          transition: box-shadow 0.4s ease, border-color 0.4s ease;
        }}
        @keyframes breatheViolet {{
          0%   {{ box-shadow: 0 0 25px rgba(160,32,240,0.4); transform: scale(1) rotate(0deg); }}
          50%  {{ box-shadow: 0 0 60px rgba(160,32,240,0.85); transform: scale(1.07) rotate(180deg); }}
          100% {{ box-shadow: 0 0 25px rgba(160,32,240,0.4); transform: scale(1) rotate(360deg); }}
        }}
        @keyframes pulseGreen {{
          0%   {{ box-shadow: 0 0 20px rgba(57,255,20,0.35); }}
          50%  {{ box-shadow: 0 0 45px rgba(57,255,20,0.8); }}
          100% {{ box-shadow: 0 0 20px rgba(57,255,20,0.35); }}
        }}
        .speaking {{ animation: breatheViolet 2.2s linear infinite; border-color:#A020F0 !important; }}
        .idle {{ animation: pulseGreen 2.6s ease-in-out infinite; }}

        .flag-corner {{ position:absolute; font-size:22px; text-shadow:0 0 8px rgba(0,240,255,0.6); }}
        .flag-tl {{ top:-6px; left:-6px; }}
        .flag-tr {{ top:-6px; right:-6px; }}
        .flag-bl {{ bottom:-6px; left:-6px; }}
        .flag-br {{ bottom:-6px; right:-6px; }}

        #orb-status {{
          margin-top: 22px; color: #00F0FF; font-size: 14px; letter-spacing: 1px;
          text-shadow: 0 0 8px rgba(0,240,255,0.6);
        }}
        #orb-caption {{
          margin-top: 12px; color: #9be8ff; font-size: 12px; max-width: 480px;
          text-align: center; opacity: 0.85; min-height: 18px; padding: 0 16px;
        }}
      </style>

      <div id="orb-ring">
        <span class="flag-corner flag-tl">🇸🇱</span>
        <span class="flag-corner flag-tr">🇸🇱</span>
        <span class="flag-corner flag-bl">🇸🇱</span>
        <span class="flag-corner flag-br">🇸🇱</span>
        <div id="orb" class="idle"></div>
      </div>
      <div id="orb-status">READY — TAP THE MIC BELOW</div>
      <div id="orb-caption"></div>

      <script>
        const orb = document.getElementById('orb');
        const status = document.getElementById('orb-status');
        const caption = document.getElementById('orb-caption');
        const replyText = {safe_text};
        caption.innerText = replyText;

        function speakNow() {{
          if (!replyText) return;
          window.speechSynthesis.cancel();
          const utter = new SpeechSynthesisUtterance(replyText);
          utter.rate = 1.0;
          utter.onstart = () => {{
            orb.className = 'speaking';
            status.innerText = 'INVINCIBLE 911 IS SPEAKING...';
          }};
          utter.onend = () => {{
            orb.className = 'idle';
            status.innerText = 'READY — TAP THE MIC BELOW';
          }};
          utter.onerror = () => {{
            orb.className = 'idle';
            status.innerText = 'READY — TAP THE MIC BELOW';
          }};
          window.speechSynthesis.speak(utter);
        }}
        {autoplay_js}
      </script>
    </div>
    """


def render_live_mode(model: str, language: str):
    st.markdown(
        "<h2 style='text-align:center;'>🛰️ LIVE CONVERSATION MODE</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='sl-flag-strip'>🇸🇱 ⚡ 🎙️ ⚡ 🇸🇱</div>",
        unsafe_allow_html=True,
    )

    # Fire a randomized welcome the moment Live Mode switches on.
    if not st.session_state.live_greeted:
        greeting = random_greeting()
        st.session_state.messages.append({"role": "assistant", "content": greeting})
        st.session_state.last_ai_reply = greeting
        st.session_state.live_greeted = True

    current_hash = hashlib.md5((st.session_state.last_ai_reply or "").encode()).hexdigest()
    should_speak = bool(st.session_state.last_ai_reply) and current_hash != st.session_state.spoken_hash
    components.html(speaking_orb_html(st.session_state.last_ai_reply, autoplay=should_speak), height=520)
    if should_speak:
        st.session_state.spoken_hash = current_hash

    audio_file = st.audio_input("🎙️ Tap to record, speak, tap again to send")

    if audio_file is not None:
        audio_bytes = audio_file.getvalue()
        audio_hash = hashlib.md5(audio_bytes).hexdigest()
        if audio_hash != st.session_state.last_audio_hash:
            st.session_state.last_audio_hash = audio_hash
            with st.spinner("🎧 Transcribing and thinking..."):
                transcript = transcribe_audio(audio_bytes)
            if transcript:
                reply = generate_reply(transcript, model, language)
                st.session_state.last_ai_reply = reply
                st.rerun()

    if st.session_state.last_ai_reply:
        st.markdown(
            f"""
            <div style="
                background: rgba(11,15,25,0.7); border:1px solid #A020F0; border-radius:10px;
                box-shadow: 0 0 15px rgba(160,32,240,0.25); padding: 14px 18px; margin-top: 18px;
                color: #E6F7FF; font-size: 14px; line-height:1.5;">
                <div style="color:#A020F0; font-size:11px; letter-spacing:1px; margin-bottom:6px;">
                    INVINCIBLE 911 · LAST REPLY
                </div>
                {st.session_state.last_ai_reply}
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            message_action_buttons(st.session_state.last_ai_reply, key="live-last"),
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# APP LAYOUT
# ---------------------------------------------------------------------------
inject_theme()

with st.sidebar:
    st.title("🛡️ Invincible 911")
    st.caption("🇸🇱 Cyberpunk terminal dashboard")

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
    st.markdown("**🛰️ Live Conversation Mode**")
    new_live_mode = st.toggle(
        "Voice-to-voice loop",
        value=st.session_state.live_mode,
        help="Switches to a fullscreen mic + orb interface that talks back.",
    )
    if new_live_mode and not st.session_state.live_mode:
        # Just switched ON — reset the greeting flag so a fresh one fires.
        st.session_state.live_greeted = False
    st.session_state.live_mode = new_live_mode

    st.divider()
    st.markdown("**Slash commands**")
    st.code("/weather Freetown\n/scores\n/news", language="text")

    st.divider()
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.session_state.last_ai_reply = ""
        st.session_state.live_greeted = False
        st.session_state.spoken_hash = ""
        st.rerun()

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.title("🛡️ Invincible 911")
st.caption(f"🇸🇱 Model: `{selected_model}`  •  Language: {language}")

# ---------------------------------------------------------------------------
# MAIN VIEW: LIVE MODE vs. TEXT CHAT
# ---------------------------------------------------------------------------
if st.session_state.live_mode:
    render_live_mode(selected_model, language)

else:
    if st.session_state.messages:
        st.markdown(play_conversation_button(st.session_state.messages), unsafe_allow_html=True)

    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                st.markdown(message_action_buttons(msg["content"], key=f"hist-{i}"), unsafe_allow_html=True)

    user_input = st.chat_input("Message Invincible 911...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        full_response = generate_reply_streamed(user_input, selected_model, language)
        st.markdown(
            message_action_buttons(full_response, key=f"live-{len(st.session_state.messages)}"),
            unsafe_allow_html=True,
        )
