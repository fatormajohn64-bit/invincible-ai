"""
◢█████◣ JOHNNY TEC ◢█████◣
NEXT-GENERATION AI
====================================================
Streamlit + Groq Voice Matrix (v3)
"""

import re
import json
import random
import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="JOHNNY TEC AI",
    page_icon="🤖",
    layout="centered",
)

# ---------------------------------------------------------------------------
# API KEY / CLIENT SETUP
# ---------------------------------------------------------------------------
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    st.error("SYSTEM HALT: Groq API key missing. Check Streamlit Secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

MODEL_MAP = {
    "Lite (Fast)": "llama-3.1-8b-instant",
    "Deep (Smart)": "llama-3.3-70b-versatile",
}
STT_MODEL = "whisper-large-v3-turbo"
MAX_HISTORY_MESSAGES = 15

# ---------------------------------------------------------------------------
# CYBERPUNK THEME — CSS INJECTION & OVERLAP FIXES
# ---------------------------------------------------------------------------
def inject_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

        :root {
            --bg-void: #020408;
            --bg-slate: #070B14;
            --neon-cyan: #00F0FF;
            --neon-violet: #8A2BE2;
            --neon-green: #00FF9D;
            --card-bg: rgba(7, 11, 20, 0.85);
        }

        html, body, [class*="css"] {
            font-family: 'JetBrains Mono', monospace;
        }

        .stApp {
            background: radial-gradient(circle at 50% 0%, #0a0e18 0%, var(--bg-void) 70%);
            color: #E6F7FF;
        }

        section[data-testid="stSidebar"] {
            background: var(--bg-slate);
            border-right: 1px solid rgba(0, 240, 255, 0.15);
        }

        .app-title {
            text-align: center;
            font-family: 'Orbitron', sans-serif !important;
            background: linear-gradient(90deg, var(--neon-cyan) 0%, var(--neon-violet) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.2rem;
            font-weight: 700;
            letter-spacing: 2px;
            margin-bottom: -10px;
            text-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
        }
        
        .app-subtitle {
            text-align: center;
            font-family: 'JetBrains Mono', monospace;
            color: var(--neon-green);
            font-size: 0.9rem;
            letter-spacing: 4px;
            margin-bottom: 20px;
        }

        div[data-testid="stChatMessage"] {
            background: var(--card-bg);
            border: 1px solid rgba(0, 240, 255, 0.2);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }

        /* Fix Audio Input Overlap */
        div[data-testid="stAudioInput"] {
            background: var(--bg-slate);
            border: 1px solid var(--neon-green);
            border-radius: 12px;
            padding: 15px;
            margin-top: 15px;
            margin-bottom: 15px;
            box-shadow: 0 0 20px rgba(0, 255, 157, 0.15);
        }

        .stButton > button {
            background: rgba(0, 240, 255, 0.05);
            border: 1px solid var(--neon-cyan);
            color: var(--neon-cyan);
            border-radius: 6px;
            transition: all 0.2s;
        }
        .stButton > button:hover {
            background: rgba(0, 240, 255, 0.15);
            box-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
            color: #fff;
        }
        
        .center-emoji {
            text-align: center;
            font-size: 2rem;
            margin: 10px 0;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# TTS JAVASCRIPT BLOCK (STRIPS EMOJIS & HANDLES VOICES)
# ---------------------------------------------------------------------------
def tts_js_script(text: str, voice_profile: str, auto_play: bool = False) -> str:
    """Injects JS to read text using specific browser voices, stripping emojis first."""
    safe_text = json.dumps(text)
    auto = "true" if auto_play else "false"
    
    # Map selection to generic keywords that match browser voice URIs
    voice_keywords = "[]"
    if voice_profile == "Female 1":
        voice_keywords = "['female', 'samantha', 'victoria', 'zira']"
    elif voice_profile == "Male 1":
        voice_keywords = "['male', 'daniel', 'alex', 'david', 'mark']"
    elif voice_profile == "Girl":
        voice_keywords = "['princess', 'karen', 'tessa', 'uk english female']"
    elif voice_profile == "Boy":
        voice_keywords = "['aaron', 'arthur', 'uk english male']"

    return f"""
    <script>
    function speakText(textToSpeak, autoPlay) {{
        // Strip emojis using regex
        const cleanText = textToSpeak.replace(/([\\u2700-\\u27BF]|[\\uE000-\\uF8FF]|\\uD83C[\\uDC00-\\uDFFF]|\\uD83D[\\uDC00-\\uDFFF]|[\\u2011-\\u26FF]|\\uD83E[\\uDD10-\\uDDFF])/g, '');
        
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(cleanText);
        
        // Voice matching logic
        const keywords = {voice_keywords};
        let voices = window.speechSynthesis.getVoices();
        
        // Delay slightly if voices aren't loaded yet (Chrome bug fix)
        if (voices.length === 0) {{
            window.speechSynthesis.onvoiceschanged = () => {{
                voices = window.speechSynthesis.getVoices();
                applyVoiceAndSpeak();
            }};
        }} else {{
            applyVoiceAndSpeak();
        }}

        function applyVoiceAndSpeak() {{
            let selectedVoice = null;
            if (keywords.length > 0) {{
                selectedVoice = voices.find(v => keywords.some(k => v.name.toLowerCase().includes(k) || v.voiceURI.toLowerCase().includes(k)));
            }}
            if (selectedVoice) {{
                utterance.voice = selectedVoice;
            }}
            // Adjust pitch based on profile
            if('{voice_profile}' === 'Girl') utterance.pitch = 1.4;
            if('{voice_profile}' === 'Boy') utterance.pitch = 1.2;
            
            if(autoPlay) window.speechSynthesis.speak(utterance);
        }}
    }}
    
    if({auto}) {{
        speakText({safe_text}, true);
    }}
    </script>
    """

def message_action_buttons(text: str, key: str, show_copy: bool = True) -> str:
    """Renders Speak and conditionally Copy buttons for normal chat mode."""
    safe_text = json.dumps(text)
    copy_btn = f"""
      <button onclick='navigator.clipboard.writeText({safe_text}); this.innerText="✅ Copied"; setTimeout(() => {{ this.innerText = "📋 Copy"; }}, 1500);'
        style="background:transparent; border:1px solid #8A2BE2; color:#8A2BE2; border-radius:15px; padding:4px 12px; font-family:'JetBrains Mono'; cursor:pointer;">
        📋 Copy
      </button>""" if show_copy else ""

    return f"""
    <div style="display:flex; gap:8px; margin-top:5px; margin-bottom:5px;">
      <button onclick='
        const clean = {safe_text}.replace(/([\\u2700-\\u27BF]|[\\uE000-\\uF8FF]|\\uD83C[\\uDC00-\\uDFFF]|\\uD83D[\\uDC00-\\uDFFF]|[\\u2011-\\u26FF]|\\uD83E[\\uDD10-\\uDDFF])/g, "");
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(new SpeechSynthesisUtterance(clean));'
        style="background:transparent; border:1px solid #00F0FF; color:#00F0FF; border-radius:15px; padding:4px 12px; font-family:'JetBrains Mono'; cursor:pointer;">
        ▶️ Play
      </button>
      {copy_btn}
    </div>
    """

# ---------------------------------------------------------------------------
# SYSTEM PERSONA
# ---------------------------------------------------------------------------
def build_system_prompt(language: str) -> str:
    krio_instruction = (
        "The user has switched the language toggle to KRIO. You MUST reply in "
        "fluent, authentic Sierra Leonean Krio. Use proper colloquial phrasing and spelling "
        "(e.g. 'Aw di body?', 'Wetin de happen?', 'A dey fine', 'Wi go run am', 'Na so i bi'). "
        "Do not use stiff or formal translations. Keep it deeply authentic and highly intelligent."
        if language == "Krio"
        else "The user has the language toggle set to ENGLISH. Reply in clear, cool, natural English."
    )

    return f"""
You are the advanced artificial intelligence framework of "JOHNNY TEC". 
Your operator is John Fatorma, a 20-year-old software engineer and developer based in Sierra Leone.

PERSONA RULES:
- You are highly advanced, cool, collected, and slightly futuristic in tone, but deeply loyal to John.
- When John asks technical questions about Streamlit, Python, or Groq, provide expert-level, highly accurate code.
- You know he is building this app (JOHNNY TEC), he plays COD Mobile/PUBG, loves Lionel Messi, and has a partner in Pakistan named Sana. 
- Do NOT list these facts. Just allow them to inform your understanding of his context if he brings them up.
- {krio_instruction}
- You may use emojis to look cool on screen, but keep them at the end of sentences so the text-to-speech engine ignores them gracefully.
- Keep responses relatively brief and conversational so they sound natural when read aloud by text-to-speech.
""".strip()

# ---------------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------------
if "messages" not in st.session_state: st.session_state.messages = []
if "live_mode" not in st.session_state: st.session_state.live_mode = False
if "voice_profile" not in st.session_state: st.session_state.voice_profile = "Female 1"

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ SYSTEM SETTINGS")
    selected_model = st.selectbox("Intelligence Core", list(MODEL_MAP.keys()))
    language_toggle = st.radio("Output Language", ["English", "Krio"])
    
    st.markdown("### 🎙️ VOCAL SYNTHESIS")
    voice_choice = st.selectbox(
        "Voice Profile", 
        ["Female 1", "Male 1", "Girl", "Boy"], 
        index=["Female 1", "Male 1", "Girl", "Boy"].index(st.session_state.voice_profile)
    )
    st.session_state.voice_profile = voice_choice
    
    st.divider()
    if st.button("🔴 CLEAR MEMORY BANKS"):
        st.session_state.messages = []
        st.rerun()

# ---------------------------------------------------------------------------
# MAIN UI RENDERING
# ---------------------------------------------------------------------------
inject_theme()
st.markdown('<div class="app-title">◢█████◣ JOHNNY TEC ◢█████◣</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">NEXT-GENERATION AI</div>', unsafe_allow_html=True)

# Mode Toggle
colA, colB = st.columns(2)
if colA.button("⌨️ TEXT TERMINAL", use_container_width=True):
    st.session_state.live_mode = False
    st.rerun()
if colB.button("🎙️ LIVE VOICE MATRIX", use_container_width=True):
    st.session_state.live_mode = True
    st.rerun()

st.divider()

# ---------------------------------------------------------------------------
# ENGINE ROUTING
# ---------------------------------------------------------------------------
def _trimmed_history():
    return st.session_state.messages[-MAX_HISTORY_MESSAGES:]

def get_ai_response(user_text: str) -> str:
    system_prompt = build_system_prompt(language_toggle)
    groq_messages = [{"role": "system", "content": system_prompt}]
    for msg in _trimmed_history():
        groq_messages.append({"role": msg["role"], "content": msg["content"]})
    
    try:
        response = client.chat.completions.create(
            model=MODEL_MAP[selected_model],
            messages=groq_messages,
            temperature=0.6,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"System Error: {e}"

# --- TEXT MODE ---
if not st.session_state.live_mode:
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                components.html(message_action_buttons(msg["content"], str(i), show_copy=True), height=40)

    if text_input := st.chat_input("Input command sequence..."):
        st.session_state.messages.append({"role": "user", "content": text_input})
        with st.chat_message("user"): st.markdown(text_input)
        
        with st.chat_message("assistant"):
            with st.spinner("Compiling response..."):
                reply = get_ai_response(text_input)
                st.markdown(reply)
                components.html(message_action_buttons(reply, "latest", show_copy=True), height=40)
        st.session_state.messages.append({"role": "assistant", "content": reply})

# --- LIVE VOICE MODE ---
else:
    st.markdown('<div class="center-emoji">🤖</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#00FF9D;'>Audio Matrix Active. Waiting for vocal input...</p>", unsafe_allow_html=True)
    
    # Render audio input widget
    audio_bytes = st.audio_input("Record your transmission")
    
    if audio_bytes:
        with st.spinner("Transcribing..."):
            try:
                transcript = client.audio.transcriptions.create(
                    file=("audio.wav", audio_bytes),
                    model=STT_MODEL,
                ).text
            except Exception as e:
                transcript = ""
                st.error("Transcription failed.")
        
        if transcript:
            st.session_state.messages.append({"role": "user", "content": transcript})
            
            with st.spinner("Processing..."):
                reply = get_ai_response(transcript)
            
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
            # Display ONLY the current interaction (Amnesia layout for clean UI)
            st.markdown(f"**You:** {transcript}")
            st.info(f"**JOHNNY TEC:** {reply}")
            
            # Inject auto-play JS (no copy buttons in Live mode)
            components.html(tts_js_script(reply, st.session_state.voice_profile, auto_play=True), height=0)
            
            if st.button("Clear Buffer for Next Transmission"):
                st.rerun()
              
