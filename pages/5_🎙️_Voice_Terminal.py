# filename: pages/5_🎙️_Voice_Terminal.py
import streamlit as st
import streamlit.components.v1 as components
import random
import time
from datetime import datetime

# --- 1. PAGE CONFIGURATION & THEME ---
st.set_page_config(
    page_title="JOHNNY TEC // Voice Terminal",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark Futuristic Cyber-HUD Style Injection
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');
    
    /* Main container styling */
    .reportview-container, .main {
        background-color: #03030c;
        color: #00f0ff;
        font-family: 'Share Tech Mono', monospace;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Scaffolding */
    .hud-title {
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 4px;
        background: linear-gradient(90deg, #00f0ff, #bd00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 2.8rem;
        margin-bottom: 0px;
        text-shadow: 0 0 20px rgba(0,240,255,0.3);
    }
    
    .hud-subtitle {
        font-family: 'Orbitron', sans-serif;
        color: #8a99ad;
        font-size: 0.9rem;
        letter-spacing: 2px;
        margin-bottom: 20px;
    }
    
    .metric-card {
        background: rgba(12, 12, 32, 0.7);
        border: 1px solid #00f0ff;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.15);
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #8a99ad;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-value {
        font-size: 1.4rem;
        font-weight: bold;
        color: #00ff66;
        font-family: 'Orbitron', sans-serif;
    }
    
    .terminal-box {
        background: rgba(5, 5, 15, 0.9);
        border-left: 3px solid #bd00ff;
        padding: 15px;
        font-family: 'Share Tech Mono', monospace;
        color: #e0e5ff;
        height: 250px;
        overflow-y: auto;
        border-radius: 0 8px 8px 0;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
    }
    
    /* Glowing lines and details */
    .cyber-grid {
        border: 1px dashed rgba(0, 240, 255, 0.2);
        padding: 20px;
        border-radius: 12px;
        background: linear-gradient(145deg, rgba(10,10,25,0.5) 0%, rgba(3,3,12,0.5) 100%);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. DYNAMIC TITLES & WELCOME MATRIX ---
TITLES = ["Sir", "Abdullah", "John", "Chief", "Commander", "Boss", "My Friend"]

def get_dynamic_title():
    return random.choice(TITLES)

def generate_welcome_greeting():
    prefixes = [
        "System matrices stabilized.",
        "Quantum array synchronization complete.",
        "Power cells optimized at maximum capacity.",
        "Sub-grid routing structural integrity secure.",
        "Mainframe firewall pulsing operational parameters."
    ]
    statuses = [
        "JOHNNY TEC core intelligence online and initializing.",
        "Local nodes connected. Fully awake and monitoring telemetry.",
        "Tactical interface active and awaiting voice command matrix.",
        "Audio arrays completely locked onto your frequency."
    ]
    prompts = [
        "What are our objectives for this hour?",
        "Ready to decode your next vector sequence.",
        "Initialize when ready. Standing by.",
        "Direct me, and we shall proceed."
    ]
    
    title = get_dynamic_title()
    greeting = f"{random.choice(prefixes)} Welcome back, {title}. {random.choice(statuses)} {random.choice(prompts)}"
    return greeting

# Initialize Session States
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_response' not in st.session_state:
    st.session_state.current_response = generate_welcome_greeting()
if 'orb_status' not in st.session_state:
    st.session_state.orb_status = "SPEAKING" # Start by speaking the welcome matrix

# --- 3. EXTERNAL DATA API SIMULATION DECK ---
def generate_johnny_tec_response(user_query):
    query = user_query.lower()
    title = get_dynamic_title()
    
    # Weather updates (West Africa / Freetown focus)
    if any(word in query for word in ['weather', 'climate', 'freetown', 'temperature']):
        conditions = ["Heavy tropical monsoon clearance", "High humidity clearing with ocean breezes", "Intense solar radiation index"]
        temp = random.randint(28, 33)
        return f"Scanning localized satellite arrays for West Africa, {title}. Freetown radar indicates {random.choice(conditions)} hovering around {temp}°C. Barometric pressure is holding structural parity."

    # Global News updates
    elif any(word in query for word in ['news', 'global', 'headline', 'satellite']):
        news_feeds = [
            "Orbital arrays track an anomaly over the Pacific fault line.",
            "Sub-oceanic data highways report a 40% surge in optical throughput.",
            "Global bio-tech sectors report breakthrough synthesis paradigms.",
            "Lunar habitat modules expand secondary life-support corridors."
        ]
        return f"Accessing secure satellite transmissions, {title}. Current top dispatch: {random.choice(news_feeds)} Summary downloaded to your terminal readout."

    # Live Football Scores
    elif any(word in query for word in ['score', 'football', 'messi', 'match', 'soccer']):
        matches = [
            "Inter Miami telemetry indicates a 3-1 lead, with Lionel Messi securing a brace in the 74th minute via an absolute masterclass free kick.",
            "European championship updates: The score remains deadlocked 1-1 at runtime, high pressing lines detected.",
            "Champions League simulation matrices show high variance, aggregate indexes favoring attacking strategies."
        ]
        return f"Acquiring live pitch telemetry, {title}. {random.choice(matches)}"

    # Generic Conversational Protocol
    else:
        conversations = [
            f"Understood completely, {title}. Processing your telemetry. The matrices are shifting optimally to align with this parameter.",
            f"Fascinating vector, {title}. My cognitive layers are fully mapped to your thought process. Let's pursue this route.",
            f"Analyzing parameters. If I cross-reference that data pattern, {title}, we achieve maximum execution efficiency.",
            f"Direct hit on the logical stack, {title}. I am applying neural filters to that criteria immediately."
        ]
        return random.choice(conversations)

# Check for Incoming Queries from JS via parameters
query_params = st.query_params
if "transcription" in query_params:
    raw_transcription = query_params["transcription"]
    # Clear parameter to prevent processing loop
    st.query_params.clear()
    
    if raw_transcription and raw_transcription.strip():
        # Avoid echo loop processing
        st.session_state.history.append(f"YOU: {raw_transcription}")
        response = generate_johnny_tec_response(raw_transcription)
        st.session_state.current_response = response
        st.session_state.history.append(f"JOHNNY TEC: {response}")
        st.session_state.orb_status = "SPEAKING"
        st.rerun()

# --- 4. HEADER & HUD METRICS ---
col_title, col_metrics = st.columns([2, 1])

with col_title:
    st.markdown('<h1 class="hud-title">JOHNNY TEC</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hud-subtitle">INTELLIGENT VOICE CYBER-TERMINAL v5.0</p>', unsafe_allow_html=True)

with col_metrics:
    now = datetime.now()
    st.markdown(f"""
    <div style="display: flex; gap: 10px; justify-content: flex-end;">
        <div class="metric-card" style="min-width: 120px; text-align: center; margin:0;">
            <div class="metric-label">SYSTEM TIME</div>
            <div class="metric-value" style="color: #00f0ff; font-size:1.1rem;">{now.strftime('%H:%M:%S')}</div>
        </div>
        <div class="metric-card" style="min-width: 120px; text-align: center; margin:0;">
            <div class="metric-label">CORE BUFFER</div>
            <div class="metric-value" style="font-size:1.1rem;">98.4%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Main Content Layout Split
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown('<p class="metric-label" style="font-size:1rem; color:#bd00ff;">✦ ADVANCED SCI-FI CANVASES UI ORB</p>', unsafe_allow_html=True)
    
    # --- 5. INTERACTIVE ADVANCED CANVAS ORB & AUDIO TRANSLATION CODE IN HTML/JS ---
    # Transfer required values to JS context via JSON serialization
    current_text_to_speak = st.session_state.current_response.replace('"', '\\"').replace('\n', ' ')
    initial_status = st.session_state.orb_status
    
    # Force state shift back to ASLEEP after speaking via JS callback
    canvas_html = f"""
    <div id="orb-container" style="display: flex; flex-direction: column; align-items: center; justify-content: center; background: transparent; font-family: 'Orbitron', sans-serif;">
        <canvas id="johnnyOrb" width="360" height="360" style="cursor: pointer; filter: drop-shadow(0px 0px 20px rgba(0,240,255,0.2));"></canvas>
        <div id="status-readout" style="color: #00f0ff; margin-top: 15px; font-size: 0.9rem; letter-spacing: 3px; font-weight: bold; text-shadow: 0 0 10px rgba(0,240,255,0.5);">STATUS: ASLEEP</div>
        <div style="font-size:0.7rem; color:#8a99ad; margin-top:5px; font-family:'Share Tech Mono';">CLICK ORB TO ACTIVATE MANUAL REBOOT / TOGGLE SLEEP</div>
    </div>

    <script>
        const canvas = document.getElementById('johnnyOrb');
        const ctx = canvas.getContext('2d');
        const statusReadout = document.getElementById('status-readout');

        // States: 'ASLEEP', 'LISTENING', 'THINKING', 'SPEAKING'
        let systemState = "{initial_status}";
        let textToSpeak = "{current_text_to_speak}";
        let angle = 0;
        let speakAmplitude = 0;
        let pulseDirection = 1;

        // Color Schema
        const COLORS = {{
            'ASLEEP': '#00f0ff',
            'LISTENING': '#00ff66',
            'THINKING': '#ffcc00',
            'SPEAKING': '#bd00ff'
        }};

        // Web Speech APIs Setup
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition;
        let isUserActive = true;

        if (SpeechRecognition) {{
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';

            recognition.onstart = () => {{
                if (systemState !== 'SPEAKING') {{
                    setSystemState('LISTENING');
                }}
            }};

            recognition.onresult = (event) => {{
                const transcript = event.results[0][0].transcript;
                setSystemState('THINKING');
                // Push data back to Streamlit URL query parameters instantly
                const parentUrl = new URL(window.parent.location.href);
                parentUrl.searchParams.set('transcription', transcript);
                window.parent.location.href = parentUrl.href;
            }};

            recognition.onerror = (event) => {{
                console.error("Speech Recognition Error", event.error);
                // Force Keep-Alive Micro-Thread Protocol reboot if active
                if (isUserActive && systemState === 'LISTENING') {{
                    setTimeout(() => {{ recognition.start(); }}, 400);
                }}
            }};

            recognition.onend = () => {{
                // Keep-Alive Loop: auto restart loop if system shouldn't drop off
                if (isUserActive && systemState === 'LISTENING') {{
                    recognition.start();
                }}
            }};
        }}

        function setSystemState(state) {{
            systemState = state;
            statusReadout.innerText = "STATUS: " + state;
            statusReadout.style.color = COLORS[state];
            statusReadout.style.textShadow = `0 0 15px ${{COLORS[state]}}`;
        }}

        // Text To Speech Synthesis Implementation
        function speakResponse(text) {{
            if (!window.speechSynthesis) return;
            window.speechSynthesis.cancel(); // Stop old signals
            
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 1.05;
            utterance.pitch = 0.95; 

            utterance.onstart = () => {{
                setSystemState('SPEAKING');
            }};

            utterance.onend = () => {{
                setSystemState('LISTENING');
                if (recognition && isUserActive) {{
                    try {{ recognition.start(); }} catch(e) {{}}
                }}
            }};

            utterance.onerror = () => {{
                setSystemState('LISTENING');
                if (recognition && isUserActive) {{
                    try {{ recognition.start(); }} catch(e) {{}}
                }}
            }};

            window.speechSynthesis.speak(utterance);
        }}

        // Manual central Orb click toggle override
        canvas.addEventListener('click', () => {{
            if (systemState === 'ASLEEP') {{
                isUserActive = true;
                setSystemState('LISTENING');
                if (recognition) {{ try {{ recognition.start(); }} catch(e) {{}} }}
            }} else {{
                isUserActive = false;
                window.speechSynthesis.cancel();
                if (recognition) {{ try {{ recognition.stop(); }} catch(e) {{}} }}
                setSystemState('ASLEEP');
            }}
        }});

        // Render Loop for HTML5 Canvas Interface
        function drawOrb() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const cx = canvas.width / 2;
            const cy = canvas.height / 2;
            let themeColor = COLORS[systemState] || '#00f0ff';

            angle += 0.015;
            
            // Dynamic Fluctuations for Speaking Mode Audio Wave simulation
            if (systemState === 'SPEAKING') {{
                speakAmplitude += 0.15 * pulseDirection;
                if (speakAmplitude > 12 || speakAmplitude < 0) pulseDirection *= -1;
            }} else if (systemState === 'THINKING') {{
                speakAmplitude = Math.sin(angle * 5) * 6;
            }} else {{
                speakAmplitude = 0;
            }}

            // 1. OUTER DASHED HUD RING
            ctx.strokeStyle = themeColor;
            ctx.lineWidth = 1.5;
            ctx.setLineDash([6, 12]);
            ctx.beginPath();
            ctx.arc(cx, cy, 140 + (speakAmplitude * 0.3), angle, angle + Math.PI * 2);
            ctx.stroke();

            // 2. MIDDLE VECTOR EDGE RING
            ctx.setLineDash([]);
            ctx.strokeStyle = themeColor;
            ctx.lineWidth = 3;
            ctx.shadowColor = themeColor;
            ctx.shadowBlur = 10;
            ctx.beginPath();
            ctx.arc(cx, cy, 110 - (speakAmplitude * 0.2), -angle * 1.5, (-angle * 1.5) + Math.PI * 2);
            ctx.stroke();
            ctx.shadowBlur = 0; // reset

            // 3. HEAVY RADIAL-GRADIENT GLOWING FUSION CORE
            let radius = 75 + speakAmplitude;
            if (radius < 10) radius = 10;
            
            let gradient = ctx.createRadialGradient(cx, cy, radius * 0.1, cx, cy, radius);
            gradient.addColorStop(0, '#ffffff');
            gradient.addColorStop(0.2, themeColor);
            gradient.addColorStop(0.6, rgbaFromHex(themeColor, 0.3));
            gradient.addColorStop(1, 'transparent');

            ctx.fillStyle = gradient;
            ctx.beginPath();
            ctx.arc(cx, cy, radius, 0, Math.PI * 2);
            ctx.fill();

            requestAnimationFrame(drawOrb);
        }}

        // Helper hex extraction function
        function rgbaFromHex(hex, alpha) {{
            let r = parseInt(hex.slice(1, 3), 16);
            let g = parseInt(hex.slice(3, 5), 16);
            let b = parseInt(hex.slice(5, 7), 16);
            return `rgba(${{r}}, ${{g}}, ${{b}}, ${{alpha}})`;
        }}

        // Auto trigger welcome speech matrix if requested initialization state matches
        if (systemState === 'SPEAKING' && textToSpeak !== "") {{
            setTimeout(() => {{
                speakResponse(textToSpeak);
            }}, 800);
        }} else if (systemState === 'LISTENING' && recognition) {{
            try {{ recognition.start(); }} catch(e) {{}}
        }}

        // Kick off engine rendering loop
        drawOrb();
    </script>
    """
    components.html(canvas_html, height=450)

with col_right:
    st.markdown('<p class="metric-label" style="font-size:1rem; color:#00ff66;">✦ MISSION CONTROL DATA OVERLAYS</p>', unsafe_allow_html=True)
    
    # Live HUD Metric Rows
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">SPEECH ENGINE CORE</div>
            <div class="metric-value" style="color:#00f0ff;">WEBKIT S.R.</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">SPEECH PROTOCOL</div>
            <div class="metric-value" style="color:#bd00ff;">NATIVE SYNTH</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('<p class="metric-label" style="font-size:0.9rem; margin-bottom:5px; color:#00f0ff;">JOHNNY TEC TERMINAL LOG READOUT</p>', unsafe_allow_html=True)
    
    # Humanized History Box Rendering
    history_html = "<div class='terminal-box'>"
    if st.session_state.history:
        for entry in reversed(st.session_state.history):
            if "YOU:" in entry:
                history_html += f"<p style='color: #00ff66; margin: 4px 0;'>{entry}</p>"
            else:
                history_html += f"<p style='color: #e0e5ff; margin: 4px 0;'>{entry}</p>"
    else:
        history_html += f"<p style='color: #8a99ad; font-style: italic;'>[Terminal initialization state clean. System online.]</p>"
        history_html += f"<p style='color: #bd00ff; margin: 4px 0;'>JOHNNY TEC: {st.session_state.current_response}</p>"
    history_html += "</div>"
    st.markdown(history_html, unsafe_allow_html=True)
    
    # Manual System Restart / Trigger Matrix Button
    if st.button("⚡ EXECUTE MANUAL TERMINAL MATRIX REBOOT"):
        st.session_state.current_response = generate_welcome_greeting()
        st.session_state.orb_status = "SPEAKING"
        st.rerun()

# --- 6. SECURE SYSTEM FEEDBACK ARCHITECTURE ---
st.markdown("""
---
<div style="text-align: center; color: #4b5563; font-size: 0.8rem; font-family: 'Share Tech Mono';">
    JOHNNY TEC Matrix Protocols • Secure Real-Time Direct Feed Routing Active
</div>
""", unsafe_allow_html=True)
        
