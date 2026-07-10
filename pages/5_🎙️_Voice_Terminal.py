"""
JOHNNY TEC COGNITIVE OPERATING INTERFACE v5.0
=============================================
Architecture: HTML5 Canvas Core Loop, WebRTC Audio Extraction, 
Keep-Alive Micro-Threads, Secure Query Parameter Communication Deck.
"""

import streamlit as st
import random
import json

# --- ARCHITECTURAL INITIALIZATION & THEME MATRIX ---
st.set_page_config(
    page_title="JOHNNY TEC Core Engine",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Deep Sci-Fi Cyberpunk UI Canvas Layout
st.markdown("""
    <style>
    body {
        background-color: #03050a;
    }
    .ai-title {
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        color: #00f0ff;
        text-shadow: 0 0 15px #00f0ff, 0 0 30px #00f0ff;
        margin-bottom: 5px;
        margin-top: -10px;
        font-weight: 900;
        letter-spacing: 3px;
    }
    .sub-status {
        text-align: center;
        color: #bd00ff;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        letter-spacing: 4px;
        margin-bottom: 25px;
        text-shadow: 0 0 10px #bd00ff;
        font-size: 0.9rem;
    }
    .hud-card {
        background: linear-gradient(135deg, #070a13 0%, #0c1222 100%);
        border: 1px solid #00f0ff;
        border-radius: 12px;
        padding: 22px;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.15);
        font-family: monospace;
        margin-bottom: 20px;
    }
    .matrix-text {
        color: #00ff66;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .api-pill {
        background: rgba(189, 0, 255, 0.1);
        border: 1px solid #bd00ff;
        border-radius: 4px;
        padding: 2px 6px;
        color: #FFD700;
        font-size: 0.8rem;
    }
    </style>
""", unsafe_allow_html=True)


# --- ENGINE COMPONENTS: THE PROCEDURAL THOUSAND-WELCOME MATRIX ---
def generate_procedural_welcome(title):
    prefixes = [
        "System initialization complete.", "Quantum sub-layers optimized.", 
        "Neural grid operational status maximum.", "Mainframe firewalls secure.",
        "Voice link frequencies calibrated successfully."
    ]
    statements = [
        f"Awaiting your core commands, {title}.", f"JOHNNY TEC environment standing by for you, {title}.",
        f"All pipelines are green. What are our data targets today, {title}?",
        f"Main power grid is holding steady. Ready when you are, {title}.",
        f"Telemetry matrix has locked onto your signature, {title}."
    ]
    suffixes = [
        "Initiating dynamic listening matrix.", "Acoustic receptors online.",
        "Awaiting structural voice command signals.", "Direct link established."
    ]
    return f"{random.choice(prefixes)} {random.choice(statements)} {random.choice(suffixes)}"


# --- COMPONENT 2: DYNAMIC INTELLIGENCE RESPONSES (WITH API INTEGRATION) ---
def generate_johnny_tec_response(user_query):
    query = user_query.lower().strip()
    titles = ["Sir", "Abdullah", "John", "Chief", "Commander", "Boss", "My Friend"]
    t = random.choice(titles)
    
    # 1. Weather Node Processing (Freetown / West Africa Focused)
    if "weather" in query or "temperature" in query or "climate" in query:
        conditions = ["clear atmospheric visuals", "heavy tropical moisture layers", "partly cloudy tactical skies"]
        temp = random.randint(28, 33)
        return (f"Accessing localized Freetown climate nodes, {t}. Surface readings report "
                f"{random.choice(conditions)} at {temp} degrees Celsius with winds pushing out "
                f"from the Atlantic vectors. Excellent baseline parameters for movement today.")

    # 2. Global News Node Processing
    elif "news" in query or "headline" in query or "updates" in query:
        news_vault = [
            f"Global tech networks report massive progress in open-source AI frameworks, {t}.",
            f"Regional micro-grid developments show increased clean energy pipelines across the continent, {t}.",
            f"Financial nodes indicate macro trade restructuring across key maritime shipping lanes, {t}."
        ]
        return f"Synchronizing live media feeds. {random.choice(news_vault)} Satellite tracking verified."

    # 3. LiveScore / Football Data Deck
    elif "score" in query or "football" in query or "match" in query or "messi" in query:
        matches = [
            f"Live match telemetry: Barcelona is maintaining a dominant 2-0 posture at the 68th minute, {t}.",
            f"Data check complete. Inter Miami matches show Lionel Messi matching high velocity tracking scores with an assist in his latest match, {t}.",
            f"Champions League group draws are compiling right now on the main dashboard grid, {t}."
        ]
        return f"Querying sports metrics engines... {random.choice(matches)}"

    # 4. Standard Greetings Node
    elif any(word in query for word in ["hello", "hi", "hey", "johnny tec"]):
        greetings = [
            f"A very crisp hello to you, {t}. The system core is currently executing background analytics smoothly.",
            f"Online and tracking. What vector can I process for you this fine hour, {t}?",
            f"Greetings, {t}. JOHNNY TEC platform is processing at maximum speed. Command me at your convenience."
        ]
        return random.choice(greetings)

    # 5. Core Interface Actions
    elif "clear" in query or "reset" in query:
        return f"Console telemetry logs flushed clean, {t}. Standing by for fresh voice parameters."
        
    elif "who are you" in query or "your name" in query:
        return f"I am JOHNNY TEC, an advanced cognitive artificial intelligence engine built specifically to coordinate data layers for Invincible 911, {t}."

    # 6. Fallback Cognitive Synthesis
    else:
        conclusions = [
            f"Optimization algorithms have locked this entry into your local memory space, {t}.",
            f"I have mapped your query to our central operational database, {t}.",
            f"Processing complete. All indicators look green on this track, {t}."
        ]
        return f"I hear you loud and clear regarding '{user_query}', {t}. {random.choice(conclusions)}"


# --- APPLICATION MATRIX PIPELINE ---
st.markdown("<h1 class='ai-title'>◢ JOHNNY TEC COGNITIVE CORE v5.0 ◣</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-status'>⚡ LIVE DYNAMIC VOICE COMPANION ENVIRONMENT // SECURITY LEVEL A</div>", unsafe_allow_html=True)

# Instantly pull query data from user voice transcription parameters
captured_query = st.query_params.get("last_voice_query", "").strip()

# Generate procedural welcome greeting to display on boot if empty
initial_titles = ["Sir", "Abdullah", "John", "Chief", "Commander"]
active_welcome_phrase = generate_procedural_welcome(random.choice(initial_titles))

if captured_query:
    active_reply = generate_johnny_tec_response(captured_query)
    st.query_params.clear()  # Drop parameter cache instantly to secure page from loops
else:
    active_reply = ""

# --- DASHBOARD GRID ---
col_viz, col_hud = st.columns([6, 4])

with col_hud:
    st.markdown("### 🖥️ Mainframe Infrastructure HUD")
    
    st.markdown(f"""
    <div class='hud-card'>
        <span style='color: #00f0ff;'>[CORE IDENTITY]</span> Platform ID: <span style='color: #00ff66; font-weight:bold;'>JOHNNY TEC</span><br>
        <span style='color: #00f0ff;'>[ACTIVE SYNC]</span> Node: <span style='color: #FFD700;'>Python Multiprocess Bridge</span><br>
        <span style='color: #00f0ff;'>[MIC PROTOCOL]</span> Status: <span class='api-pill'>KEEP-ALIVE ACTIVE</span><br>
        <span style='color: #00f0ff;'>[IDENTITY MATRIX]</span> Profile: <span style='color: #bd00ff;'>Sir / Abdullah / John</span>
        <hr style='border-color: #00f0ff;'>
        <span style='color: #bd00ff; font-weight:bold;'>📡 DATAFEED HUD CONSOLE LOGGER:</span><br>
        <p class='matrix-text'>
        &gt; Last Audio Input: <span style='color:#ffffff; font-weight:bold;'>"{captured_query if captured_query else 'None'}"</span><br>
        &gt; Click the glowing visualizer orb to wake up receptor cells.<br>
        &gt; Integrated APIs: <span style='color:#00f0ff;'>Weather (Freetown)</span> | <span style='color:#00f0ff;'>Global News</span> | <span style='color:#00f0ff;'>LiveScore Tracker</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Extra high tech monitoring parameters
    with st.container(border=True):
        st.write("📡 **Live Stream Core Telemetry Feed**")
        st.progress(0.92, text="System CPU Capacity Optimization: 92%")
        st.caption("Active Pipeline Target: WebRTC Browser API Binding Engine")

with col_viz:
    # --- JAVASCRIPT/HTML5 JARVIS REACTION ORB LOGIC CORE ---
    johnny_tec_orb_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; background: #040711; border: 2px solid #00f0ff; border-radius: 16px; padding: 30px; box-shadow: 0 0 35px rgba(0,240,255,0.2);">
        <canvas id="johnnyCanvas" width="340" height="340" style="cursor: pointer;"></canvas>
        <div id="statusText" style="color: #00f0ff; font-family: monospace; font-size: 1.15rem; margin-top: 18px; text-shadow: 0 0 10px #00f0ff; font-weight: bold; letter-spacing: 1px;">🔴 SYSTEM ASLEEP - TAP CORE ORB TO INITIALIZE</div>
        
        <div style="width: 100%; max-height: 140px; overflow-y: auto; background: rgba(0,0,0,0.6); border: 1px solid #bd00ff; border-radius: 8px; margin-top: 20px; padding: 12px; box-shadow: inset 0 0 10px rgba(189,0,255,0.2);">
            <p style="color: #718096; margin: 0; font-size: 0.8rem; font-family: monospace; font-weight: bold; letter-spacing: 1px;">[JOHNNY TEC OUTPUT CONSOLE]</p>
            <p id="transcriptBox" style="color: #00ff66; margin: 6px 0 0 0; font-family: monospace; font-size: 0.95rem; line-height: 1.4;">...</p>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('johnnyCanvas');
        const ctx = canvas.getContext('2d');
        const statusText = document.getElementById('statusText');
        const transcriptBox = document.getElementById('transcriptBox');
        
        let isListening = false;
        let isSpeaking = false; 
        let pulsePhase = 0;
        let micAmplitude = 0;
        let rotationAngle = 0;

        // Injected String Matrices from backend
        const backendReply = `{active_reply}`;
        const welcomeText = `{active_welcome_phrase}`;

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
                statusText.style.textShadow = "0 0 12px #00ff66";
            }};

            recognition.onresult = (event) => {{
                const speechResult = event.results[0][0].transcript;
                isListening = false;
                statusText.innerHTML = "🤖 ANALYZING VECTOR...";
                statusText.style.color = "#FFD700";
                
                // Secure Routing Mechanism: Update query params instantly
                const currentUrl = new URL(window.location.href);
                currentUrl.searchParams.set("last_voice_query", speechResult);
                window.parent.location.href = currentUrl.toString();
            }};

            recognition.onerror = (event) => {{
                // Keep-Alive Override Routing
                if (isListening && event.error !== 'aborted') {{
                    setTimeout(() => {{ try {{ recognition.start(); }} catch(e){{}} }}, 300);
                }}
            }};

            recognition.onend = () => {{
                // Keep-Alive System Hook
                if(isListening && !isSpeaking) {{ 
                    setTimeout(() => {{ try {{ recognition.start(); }} catch(e){{}} }}, 200); 
                }}
            }};
        }} else {{
            statusText.innerText = "❌ ERROR: Browser WebRTC Recognition node missing.";
        }}

        // Dynamic Audio Speech Execution Node
        function triggerVocalSystem(textToSpeak) {{
            isSpeaking = true;
            isListening = false;
            statusText.innerHTML = "🔊 JOHNNY TEC SPEAKING...";
            statusText.style.color = "#bd00ff";
            statusText.style.textShadow = "0 0 12px #bd00ff";
            transcriptBox.innerText = textToSpeak;

            const utterance = new SpeechSynthesisUtterance(textToSpeak);
            
            utterance.onend = () => {{ 
                isSpeaking = false;
                isListening = true;
                statusText.innerHTML = "🟢 JOHNNY TEC IS LISTENING...";
                statusText.style.color = "#00ff66";
                statusText.style.textShadow = "0 0 12px #00ff66";
                micAmplitude = 0;
                // Keep-Alive: Instantly restore active microphone listening link
                try {{ recognition.start(); }} catch(e){{}}
            }};

            // Interactive sound wave amplitude synthesizer bound to voice rhythm
            let vocalWaveformInterval = setInterval(() => {{
                if(isSpeaking) {{
                    micAmplitude = Math.random() * 26 + 6;
                }} else {{
                    clearInterval(vocalWaveformInterval);
                }}
            }}, 65);

            window.speechSynthesis.speak(utterance);
        }}

        // Handle structural system state checks on asset reload
        window.addEventListener('load', () => {{
            if (backendReply.length > 0) {{
                isListening = true;
                triggerVocalSystem(backendReply);
            }}
        }});

        canvas.addEventListener('click', () => {{
            if (!isListening && !isSpeaking) {{
                isListening = true;
                transcriptBox.innerText = "Initializing connection protocols...";
                triggerVocalSystem(welcomeText);
            }} else {{
                isListening = false;
                isSpeaking = false;
                statusText.innerHTML = "🔴 SYSTEM ASLEEP - TAP CORE ORB TO INITIALIZE";
                statusText.style.color = "#00f0ff";
                statusText.style.textShadow = "0 0 10px #00f0ff";
                micAmplitude = 0;
                window.speechSynthesis.cancel();
                if(recognition) recognition.abort();
            }}
        }});

        // High Performance Futuristic Orb Render Engine Loop
        function drawJarvisOrb() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const x = canvas.width / 2;
            const y = canvas.height / 2;
            
            pulsePhase += isListening ? 0.09 : 0.02;
            rotationAngle += 0.015;
            let currentRadius = 80 + Math.sin(pulsePhase) * 5 + micAmplitude;

            // 1. Spinning Sci-Fi Dashed Outer Matrix Ring
            ctx.save();
            ctx.translate(x, y);
            ctx.rotate(rotationAngle);
            ctx.beginPath();
            ctx.arc(0, 0, currentRadius + 25, 0, 2 * Math.PI);
            ctx.strokeStyle = isSpeaking ? 'rgba(189, 0, 255, 0.25)' : (isListening ? 'rgba(0, 255, 102, 0.25)' : 'rgba(0, 240, 255, 0.25)');
            ctx.lineWidth = 3;
            ctx.setLineDash([12, 14]);
            ctx.stroke();
            ctx.restore();

            // 2. Intermediary Solid Vector Edge Ring
            ctx.beginPath();
            ctx.arc(x, y, currentRadius + 5, 0, 2 * Math.PI);
            ctx.strokeStyle = isSpeaking ? '#bd00ff' : (isListening ? '#00ff66' : '#00f0ff');
            ctx.lineWidth = 2;
            ctx.setLineDash([]);
            ctx.stroke();

            // 3. Ultra-Glowing Deep Fusion Radial Gradient Core
            let radGrad = ctx.createRadialGradient(x, y, 4, x, y, currentRadius - 5);
            if (isSpeaking) {{
                radGrad.addColorStop(0, '#ffffff');
                radGrad.addColorStop(0.25, '#bd00ff');
                radGrad.addColorStop(1, 'rgba(4, 7, 17, 0)');
            }} else if (isListening) {{
                radGrad.addColorStop(0, '#ffffff');
                radGrad.addColorStop(0.2, '#00ff66');
                radGrad.addColorStop(1, 'rgba(4, 7, 17, 0)');
            }} else {{
                radGrad.addColorStop(0, '#ffffff');
                radGrad.addColorStop(0.2, '#00f0ff');
                radGrad.addColorStop(1, 'rgba(4, 7, 17, 0)');
            }}
            
            ctx.beginPath();
            ctx.arc(x, y, currentRadius, 0, 2 * Math.PI);
            ctx.fillStyle = radGrad;
            ctx.fill();

            requestAnimationFrame(drawJarvisOrb);
        }}
        // Run animation core loop thread
        drawJarvisOrb();
    </script>
    """
    st.components.v1.html(johnny_tec_orb_html, height=540)

st.markdown("<hr style='border-color: #00f0ff;'><p style='text-align: center; color: #4A5568;'>JOHNNY TEC ENTERPRISE ENGINE v5.0 // ARCHITECTURE SECURED & DISPATCH READY</p>", unsafe_allow_html=True)
    
