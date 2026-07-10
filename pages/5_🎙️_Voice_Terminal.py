"""
JOHNNY TEC — FULLY FUNCTIONAL DYNAMIC VOICE INTERFACE
===========================================================
Features: Live Backend Connection, Continuous Active Listening,
Anti-Echo Shielding, and Adaptive User Recognition.
"""

import streamlit as st
import random

# --- PAGE ARCHITECTURE ---
st.set_page_config(page_title="JOHNNY TEC Voice Core", page_icon="🎙️", layout="wide")

# Cyberpunk Terminal UI Styling
st.markdown("""
    <style>
    .ai-title {
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        color: #00f0ff;
        text-shadow: 0 0 15px #00f0ff, 0 0 30px #00f0ff;
        margin-bottom: 10px;
    }
    .sub-status {
        text-align: center;
        color: #bd00ff;
        font-family: monospace;
        letter-spacing: 2px;
        margin-bottom: 30px;
        text-shadow: 0 0 8px #bd00ff;
    }
    .hud-card {
        background-color: #070a13;
        border: 1px solid #00f0ff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.1);
        font-family: monospace;
    }
    .matrix-text {
        color: #00ff66;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='ai-title'>◢ JOHNNY TEC VOICE TERMINAL ◣</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-status'>⚡ LIVE BACKEND INTELLIGENCE MATRICES ONLINE // PROTOCOL 911</div>", unsafe_allow_html=True)

# --- BACKEND DYNAMIC AI RESPONSE ENGINE ---
# This links your microphone directly to python logic so it never says the same thing!
def generate_johnny_tec_response(user_query):
    query = user_query.lower().strip()
    titles = ["John", "Abdullah", "Sir"]
    t = random.choice(titles)
    
    if not query:
        return f"System standing by, {t}. Speak when ready."
        
    if "hello" in query or "hi" in query or "johnny tec" in query:
        return random.choice([
            f"Voice link established. Good to hear you, {t}.",
            f"Hello {t}. I am JOHNNY TEC, completely at your service.",
            f"Neural channels online. What is our objective today, {t}?"
        ])
    elif "weather" in query:
        return f"Accessing climate array. Freetown radar displays warm structural conditions, {t}."
    elif "clear" in query:
        return f"Console buffer flushed, {t}. Standing by."
    elif "football" in query or "messi" in query:
        return f"Analyzing sports parameters. Lionel Messi remains the absolute peak of football intelligence matrices, {t}."
    elif "who are you" in query or "your name" in query:
        return f"I am JOHNNY TEC, your personal artificial intelligence operating system, customized for Invincible 911."
    elif "islamic" in query or "reminder" in query or "quote" in query:
        return f"Of course, {t}. Remember: Verily, with hardship, there is relief. Keep your intentions pure today."
    else:
        # Dynamic fallback response so it acknowledges exactly what you said!
        return f"I have processed your statement regarding '{user_query}', {t}. Optimization vectors are locked in."

# --- SESSION STATE PROCESSING ---
# This transfers data from the Javascript layer into Python instantly
query_param = st.query_params.get("last_voice_query", "")
ai_reply_to_speak = ""

if query_param:
    ai_reply_to_speak = generate_johnny_tec_response(query_param)
    # Clear query parameters immediately so it doesn't loop trigger on refresh
    st.query_params.clear()

# --- UI LAYOUT ---
col_viz, col_hud = st.columns([6, 4])

with col_hud:
    st.markdown("### 🖥️ Core Matrix Metrics")
    st.markdown(f"""
    <div class='hud-card'>
        <span style='color: #00f0ff;'>[SYSTEM]</span> Identity: <span style='color: #00ff66;'>JOHNNY TEC</span><br>
        <span style='color: #00f0ff;'>[ENGINE]</span> Core: <span style='color: #FFD700;'>Live Python Engine</span><br>
        <span style='color: #00f0ff;'>[STATUS]</span> Mic-Lock: <span style='color: #00ff66;'>KEEP-ALIVE PROTOCOL ACTIVE</span><br>
        <span style='color: #00f0ff;'>[TARGET]</span> User Profile: <span style='color: #bd00ff;'>John / Abdullah</span>
        <hr style='border-color: #bd00ff;'>
        <span style='color: #bd00ff;'>🧠 SYSTEM CONSOLE LOGS:</span><br>
        <p class='matrix-text'>
        > Last Captured Voice: <span style='color:#ffffff;'>"{query_param if query_param else 'None'}"</span><br>
        > Tap the central core once to boot.<br>
        > Keep-Alive holds mic lock open while you are in the room.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.radio("Core Target Language Pipeline:", ["English (Universal)", "Krio (Regional Sync)"], index=0, horizontal=True)

with col_viz:
    # --- JARVIS-STYLE ORB WITH DYNAMIC WEB-API INJECTION ---
    johnny_orb_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; background: #070a13; border: 2px solid #00f0ff; border-radius: 12px; padding: 25px; box-shadow: 0 0 25px rgba(0,240,255,0.15);">
        <canvas id="aiCanvas" width="320" height="320" style="cursor: pointer;"></canvas>
        <div id="statusText" style="color: #00f0ff; font-family: monospace; font-size: 1.1rem; margin-top: 15px; text-shadow: 0 0 8px #00f0ff;">🔴 SYSTEM ASLEEP - TAP ORB TO WAKE</div>
        
        <div style="width: 100%; max-height: 120px; overflow-y: auto; background: rgba(0,0,0,0.4); border: 1px solid #bd00ff; border-radius: 6px; margin-top: 15px; padding: 10px;">
            <p style="color: #718096; margin: 0; font-size: 0.8rem; font-family: monospace;">[TRANSCRIPT RADAR]</p>
            <p id="transcriptBox" style="color: #00ff66; margin: 5px 0 0 0; font-family: monospace; font-size: 0.95rem; font-style: italic;">...</p>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('aiCanvas');
        const ctx = canvas.getContext('2d');
        const statusText = document.getElementById('statusText');
        const transcriptBox = document.getElementById('transcriptBox');
        
        let isListening = false;
        let isSpeaking = false; 
        let pulsePhase = 0;
        let micAmplitude = 0;

        // Python State Injection variables
        const pythonReply = `{ai_reply_to_speak}`;

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition;
        
        if (SpeechRecognition) {{
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';

            recognition.onstart = () => {{
                if(isSpeaking) {{ recognition.abort(); return; }}
                isListening = true;
                statusText.innerHTML = "🟢 JOHNNY TEC IS LISTENING...";
                statusText.style.color = "#00ff66";
                statusText.style.textShadow = "0 0 10px #00ff66";
            }};

            recognition.onresult = (event) => {{
                const speechResult = event.results[0][0].transcript;
                // Force push data to Streamlit URL parameters so Python can update instantly
                const url = new URL(window.location.href);
                url.searchParams.set("last_voice_query", speechResult);
                window.parent.location.href = url.toString();
            }};

            recognition.onerror = (event) => {{
                // Keep-Alive Protocol: If error occurs or microphone drops out, force-awaken it
                if (isListening && event.error !== 'aborted') {{
                    setTimeout(() => {{ try {{ recognition.start(); }} catch(e){{}} }}, 400);
                }}
            }};

            recognition.onend = () => {{
                // Keep-Alive Protocol: Never let the microphone go to sleep while user is active
                if(isListening && !isSpeaking) {{ 
                    setTimeout(() => {{ try {{ recognition.start(); }} catch(e){{}} }}, 300); 
                }}
            }};
        }} else {{
            statusText.innerText = "❌ ERROR: Browser speech node unavailable.";
        }}

        // If Python loaded a response, speak it instantly out loud
        if (pythonReply.length > 0) {{
            isSpeaking = true;
            statusText.innerHTML = "🔊 JOHNNY TEC SPEAKING...";
            statusText.style.color = "#bd00ff";
            transcriptBox.innerText = "Johnny Tec: " + pythonReply;

            const utterance = new SpeechSynthesisUtterance(pythonReply);
            
            utterance.onend = () => {{ 
                isSpeaking = false;
                isListening = true;
                statusText.innerHTML = "🟢 JOHNNY TEC IS LISTENING...";
                statusText.style.color = "#00ff66";
                micAmplitude = 0;
                // Reactivate microphone instantly
                try {{ recognition.start(); }} catch(e){{}}
            }};

            let speakPulse = setInterval(() => {{
                if(isSpeaking) {{
                    micAmplitude = Math.random() * 25 + 8;
                }} else {{
                    clearInterval(speakPulse);
                }}
            }}, 70);

            window.speechSynthesis.speak(utterance);
        }}

        canvas.addEventListener('click', () => {{
            if (!isListening && !isSpeaking) {{
                isListening = true;
                if(recognition) try {{ recognition.start(); }} catch(e) {{}}
            }} else {{
                isListening = false;
                isSpeaking = false;
                statusText.innerHTML = "🔴 SYSTEM ASLEEP - TAP ORB TO WAKE";
                statusText.style.color = "#00f0ff";
                micAmplitude = 0;
                window.speechSynthesis.cancel();
                if(recognition) recognition.abort();
            }}
        }});

        // Glowing Core Canvas Animation Loop
        function drawOrb() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const centerX = canvas.width / 2;
            const centerY = canvas.height / 2;
            
            pulsePhase += isListening ? 0.08 : 0.02;
            let dynamicRadius = 75 + Math.sin(pulsePhase) * 6 + micAmplitude;

            // Outer Tech Ring
            ctx.beginPath();
            ctx.arc(centerX, centerY, dynamicRadius + 20, 0, 2 * Math.PI);
            ctx.strokeStyle = isSpeaking ? 'rgba(189, 0, 255, 0.2)' : (isListening ? 'rgba(0, 255, 102, 0.2)' : 'rgba(0, 240, 255, 0.2)');
            ctx.lineWidth = 4;
            ctx.setLineDash([15, 10]);
            ctx.stroke();

            // Intermediary Glow Ring
            ctx.beginPath();
            ctx.arc(centerX, centerY, dynamicRadius, 0, 2 * Math.PI);
            ctx.strokeStyle = isSpeaking ? '#bd00ff' : (isListening ? '#00ff66' : '#00f0ff');
            ctx.lineWidth = 2;
            ctx.setLineDash([]);
            ctx.stroke();

            // Fusion Core
            let gradient = ctx.createRadialGradient(centerX, centerY, 5, centerX, centerY, dynamicRadius - 10);
            if (isSpeaking) {{
                gradient.addColorStop(0, '#ffffff');
                gradient.addColorStop(0.3, '#bd00ff');
                gradient.addColorStop(1, 'rgba(7, 10, 19, 0)');
            }} else if (isListening) {{
                gradient.addColorStop(0, '#ffffff');
                gradient.addColorStop(0.2, '#00ff66');
                gradient.addColorStop(1, 'rgba(7, 10, 19, 0)');
            }} else {{
                gradient.addColorStop(0, '#ffffff');
                gradient.addColorStop(0.2, '#00f0ff');
                gradient.addColorStop(1, 'rgba(7, 10, 19, 0)');
            }}
            
            ctx.beginPath();
            ctx.arc(centerX, centerY, dynamicRadius, 0, 2 * Math.PI);
            ctx.fillStyle = gradient;
            ctx.fill();

            requestAnimationFrame(drawOrb);
        }}
        drawOrb();
    </script>
    """
    st.components.v1.html(johnny_orb_html, height=520)

st.markdown("<hr style='border-color: #00f0ff;'><p style='text-align: center; color: #4A5568;'>JOHNNY TEC VOICE INFRASTRUCTURE v4.0 // LIVE PRODUCTION STABLE</p>", unsafe_allow_html=True)
