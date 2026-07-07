"""
Invincible 911 — Cyberpunk Terminal Dashboard
================================================
A Streamlit + Groq chat app with:
  - Neon cyberpunk dashboard theme (custom CSS injection)
  - Per-message text-to-speech playback (Web Speech Synthesis)
  - A fullscreen "Live Conversation Mode" with an animated audio orb and
    hands-free mic capture (Web Speech Recognition), bridged back into
    Streamlit's Python state.
  - Original features preserved: model switcher, English/Krio toggle,
    slash commands (/weather, /scores, /news), and the John Fatorma persona.

SETUP:
1. Get a free Groq API key at https://console.groq.com/keys
2. In Streamlit Cloud: Settings -> Secrets -> add:
       GROQ_API_KEY = "your-key-here"
   Locally: create a file .streamlit/secrets.toml with the same line.
3. pip install -r requirements.txt   (streamlit, groq)
4. streamlit run app.py

NOTE ON VOICE LOOP (read this before you rely on it):
Streamlit does not natively support a JS component pushing values straight
into Python without a rerun. "Live Conversation Mode" below uses a common,
documented workaround: a hidden Streamlit text_input + button pair that a
JS snippet (running inside the components.html iframe) locates in the
parent document and triggers programmatically. This works reliably on
current Streamlit versions but is inherently a DOM hack — if Anthropic/
Streamlit changes internal markup, the selectors in `VOICE_BRIDGE_JS` may
need small tweaks. It is NOT a fully continuous phone-call style loop;
each turn is "press orb -> speak -> release -> AI replies + speaks back".
"""

import json
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

        /* App background */
        .stApp {
            background: radial-gradient(circle at 20% 0%, #0a0e18 0%, var(--bg-void) 55%);
            color: #E6F7FF;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: var(--bg-slate);
            border-right: 1px solid rgba(0, 240, 255, 0.25);
        }
        section[data-testid="stSidebar"] * {
            font-family: 'JetBrains Mono', monospace;
        }

        /* Gradient titles */
        h1, h2, h3 {
            font-family: 'Space Grotesk', sans-serif !important;
            background: linear-gradient(90deg, var(--neon-cyan) 0%, var(--neon-violet) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: 0.5px;
        }

        /* Bordered containers / cards */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--card-bg);
            border: 1px solid var(--neon-cyan);
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
        }

        /* Chat bubbles */
        div[data-testid="stChatMessage"] {
            background: var(--card-bg);
            border: 1px solid rgba(0, 240, 255, 0.35);
            border-radius: 12px;
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.12);
            padding: 0.6rem 0.9rem;
            margin-bottom: 0.6rem;
        }

        /* Buttons */
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

        /* Chat input */
        div[data-testid="stChatInput"] {
            background: var(--card-bg);
            border: 1px solid var(--neon-cyan);
            border-radius: 10px;
            box-shadow: 0 0 12px rgba(0, 240, 255, 0.18);
        }

        /* Radio / selectbox labels */
        .stRadio label, .stSelectbox label, .stCheckbox label {
            color: var(--neon-cyan) !important;
        }

        /* Divider */
        hr {
            border-color: rgba(0, 240, 255, 0.25);
        }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-void); }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(var(--neon-cyan), var(--neon-violet));
            border-radius: 4px;
        }

        /* Hide the voice-bridge widgets used by Live Conversation Mode */
        .voice-bridge-hidden {
            position: absolute;
            width: 1px;
            height: 1px;
            overflow: hidden;
            opacity: 0.01;
            pointer-events: none;
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

if "live_mode" not in st.session_state:
    st.session_state.live_mode = False

if "last_ai_reply" not in st.session_state:
    st.session_state.last_ai_reply = ""

if "voice_bridge" not in st.session_state:
    st.session_state.voice_bridge = ""


# ---------------------------------------------------------------------------
# CORE REPLY LOGIC (shared by text chat and voice mode)
# ---------------------------------------------------------------------------
def generate_reply(user_input: str, model: str, language: str) -> str:
    """
    Runs a user message through the slash-command router first, then falls
    back to a streamed Groq completion. Appends both turns to session state
    and returns the assistant's final text (used for on-screen text and for
    text-to-speech playback).
    """
    st.session_state.messages.append({"role": "user", "content": user_input})

    tool_result = handle_tool_commands(user_input)
    if tool_result is not None:
        st.session_state.messages.append({"role": "assistant", "content": tool_result})
        return tool_result

    system_prompt = build_system_prompt(language)
    groq_messages = [{"role": "system", "content": system_prompt}]
    for msg in st.session_state.messages:
        groq_messages.append({"role": msg["role"], "content": msg["content"]})

    try:
        response = client.chat.completions.create(
            model=model,
            messages=groq_messages,
            temperature=0.7,
            stream=False,
        )
        full_response = response.choices[0].message.content
    except Exception as e:
        full_response = f"⚠️ Sorry John, something went wrong talking to the model: {e}"

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    return full_response


def generate_reply_streamed(user_input: str, model: str, language: str):
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
    for msg in st.session_state.messages:
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


# ---------------------------------------------------------------------------
# TEXT-TO-SPEECH BUTTON (inline HTML/JS)
# ---------------------------------------------------------------------------
def tts_button(text: str, key: str) -> str:
    """
    Returns an HTML snippet with a neon 'speak' button that calls the
    browser's native Web Speech Synthesis API. json.dumps safely escapes
    quotes/newlines so the string can't break out of the JS literal.
    """
    safe_text = json.dumps(text)
    return f"""
    <div style="margin-top:-6px; margin-bottom:10px;">
      <button onclick='window.speechSynthesis.cancel(); window.speechSynthesis.speak(new SpeechSynthesisUtterance({safe_text}));'
        style="
          background: linear-gradient(90deg, rgba(0,240,255,0.15), rgba(160,32,240,0.15));
          border: 1px solid #00F0FF;
          color: #00F0FF;
          border-radius: 20px;
          padding: 4px 12px;
          font-family: 'JetBrains Mono', monospace;
          font-size: 12px;
          cursor: pointer;
          box-shadow: 0 0 8px rgba(0,240,255,0.25);
        "
        id="tts-btn-{key}">
        🔘 Speak
      </button>
    </div>
    """


def autoplay_tts(text: str):
    """Fires speech synthesis automatically (no click needed) — used in Live Mode."""
    safe_text = json.dumps(text)
    components.html(
        f"""
        <script>
          window.speechSynthesis.cancel();
          window.speechSynthesis.speak(new SpeechSynthesisUtterance({safe_text}));
        </script>
        """,
        height=0,
    )


# ---------------------------------------------------------------------------
# LIVE CONVERSATION MODE — ORB COMPONENT + VOICE BRIDGE
# ---------------------------------------------------------------------------
ORB_HTML = """
<div id="orb-wrap" style="
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    height:560px; background:#030508; font-family:'JetBrains Mono', monospace;">

  <style>
    #orb {
      width: 220px; height: 220px; border-radius: 50%;
      background: radial-gradient(circle at 35% 30%, #0B0F19, #030508 70%);
      border: 2px solid #00F0FF;
      box-shadow: 0 0 40px rgba(0,240,255,0.35), inset 0 0 30px rgba(0,240,255,0.15);
      transition: all 0.4s ease;
    }
    @keyframes pulseGreen {
      0%   { box-shadow: 0 0 25px rgba(57,255,20,0.4), inset 0 0 20px rgba(57,255,20,0.2); transform: scale(1); border-color:#39FF14; }
      50%  { box-shadow: 0 0 70px rgba(57,255,20,0.9), inset 0 0 45px rgba(57,255,20,0.4); transform: scale(1.12); border-color:#00F0FF; }
      100% { box-shadow: 0 0 25px rgba(57,255,20,0.4), inset 0 0 20px rgba(57,255,20,0.2); transform: scale(1); border-color:#39FF14; }
    }
    @keyframes breatheViolet {
      0%   { box-shadow: 0 0 30px rgba(160,32,240,0.4); transform: scale(1) rotate(0deg); }
      50%  { box-shadow: 0 0 65px rgba(160,32,240,0.85); transform: scale(1.06) rotate(180deg); }
      100% { box-shadow: 0 0 30px rgba(160,32,240,0.4); transform: scale(1) rotate(360deg); }
    }
    .listening { animation: pulseGreen 0.9s ease-in-out infinite; }
    .processing { animation: breatheViolet 2.4s linear infinite; border-color:#A020F0 !important; }

    #orb-status {
      margin-top: 26px; color: #00F0FF; font-size: 14px; letter-spacing: 1px;
      text-shadow: 0 0 8px rgba(0,240,255,0.6);
    }
    #orb-caption {
      margin-top: 14px; color: #9be8ff; font-size: 12px; max-width: 480px;
      text-align: center; opacity: 0.85; min-height: 18px;
    }
    #mic-btn {
      margin-top: 30px; background: linear-gradient(90deg, rgba(0,240,255,0.15), rgba(160,32,240,0.15));
      border: 1px solid #00F0FF; color: #00F0FF; border-radius: 24px;
      padding: 10px 26px; font-family:'JetBrains Mono', monospace; font-size: 13px;
      cursor: pointer; box-shadow: 0 0 12px rgba(0,240,255,0.3);
    }
    #mic-btn:hover { border-color:#A020F0; color:#fff; box-shadow: 0 0 18px rgba(160,32,240,0.6); }
  </style>

  <div id="orb"></div>
  <div id="orb-status">TAP TO SPEAK</div>
  <div id="orb-caption"></div>
  <button id="mic-btn" onclick="startListening()">🎙️ Start Listening</button>

  <script>
    const orb = document.getElementById('orb');
    const status = document.getElementById('orb-status');
    const caption = document.getElementById('orb-caption');

    function setNativeValue(element, value) {
      const proto = Object.getPrototypeOf(element);
      const descriptor = Object.getOwnPropertyDescriptor(proto, 'value');
      descriptor.set.call(element, value);
    }

    function sendTranscriptToStreamlit(text) {
      try {
        const doc = window.parent.document;
        const input = doc.querySelector('input[placeholder="__voice_bridge_field__"]');
        if (!input) {
          caption.innerText = "Bridge input not found — reload the page.";
          return;
        }
        setNativeValue(input, text);
        input.dispatchEvent(new Event('input', { bubbles: true }));

        setTimeout(() => {
          const buttons = doc.querySelectorAll('button');
          for (const b of buttons) {
            if (b.innerText && b.innerText.includes('VOICE_SUBMIT')) {
              b.click();
              break;
            }
          }
        }, 150);
      } catch (err) {
        caption.innerText = "Bridge error: " + err;
      }
    }

    function startListening() {
      if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        status.innerText = "Speech recognition not supported in this browser.";
        return;
      }
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      recognition.lang = 'en-US';
      recognition.interimResults = false;
      recognition.continuous = false;

      recognition.onstart = () => {
        orb.className = 'listening';
        status.innerText = "LISTENING...";
        caption.innerText = "";
      };

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        orb.className = 'processing';
        status.innerText = "PROCESSING...";
        caption.innerText = '"' + transcript + '"';
        sendTranscriptToStreamlit(transcript);
      };

      recognition.onerror = (event) => {
        orb.className = '';
        status.innerText = "ERROR: " + event.error + " — tap to try again.";
      };

      recognition.onend = () => {
        if (orb.className === 'listening') {
          orb.className = '';
          status.innerText = "TAP TO SPEAK";
        }
      };

      recognition.start();
    }
  </script>
</div>
"""


def render_live_mode(model: str, language: str):
    st.markdown(
        "<h2 style='text-align:center;'>🛰️ LIVE CONVERSATION MODE</h2>",
        unsafe_allow_html=True,
    )
    components.html(ORB_HTML, height=600)

    # Hidden bridge widgets — JS above locates these by placeholder text /
    # button label and drives them programmatically.
    st.markdown('<div class="voice-bridge-hidden">', unsafe_allow_html=True)
    bridge_text = st.text_input(
        "voice bridge",
        key="voice_bridge",
        placeholder="__voice_bridge_field__",
        label_visibility="collapsed",
    )
    submit_clicked = st.button("VOICE_SUBMIT", key="voice_submit_btn")
    st.markdown("</div>", unsafe_allow_html=True)

    if submit_clicked and bridge_text.strip():
        reply = generate_reply(bridge_text.strip(), model, language)
        st.session_state.last_ai_reply = reply
        # Clear the bridge field so the same transcript isn't resubmitted.
        st.session_state.voice_bridge = ""
        autoplay_tts(reply)

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


# ---------------------------------------------------------------------------
# APP LAYOUT
# ---------------------------------------------------------------------------
inject_theme()

with st.sidebar:
    st.title("🛡️ Invincible 911")
    st.caption("Cyberpunk terminal dashboard")

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
    st.session_state.live_mode = st.toggle(
        "Voice-to-voice loop",
        value=st.session_state.live_mode,
        help="Hides the text log and switches to a fullscreen audio orb interface.",
    )

    st.divider()
    st.markdown("**Slash commands**")
    st.code("/weather Freetown\n/scores\n/news", language="text")

    st.divider()
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.session_state.last_ai_reply = ""
        st.rerun()

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.title("🛡️ Invincible 911")
st.caption(f"Model: `{selected_model}`  •  Language: {language}")

# ---------------------------------------------------------------------------
# MAIN VIEW: LIVE MODE vs. TEXT CHAT
# ---------------------------------------------------------------------------
if st.session_state.live_mode:
    render_live_mode(selected_model, language)

else:
    # Render chat history with a TTS button under each assistant message
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                st.markdown(tts_button(msg["content"], key=f"hist-{i}"), unsafe_allow_html=True)

    user_input = st.chat_input("Message Invincible 911...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        full_response = generate_reply_streamed(user_input, selected_model, language)
        st.markdown(
            tts_button(full_response, key=f"live-{len(st.session_state.messages)}"),
            unsafe_allow_html=True,
        )
