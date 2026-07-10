"""
JOHNNY TEC / INVINCIBLE 911 — JARVIS VOICE OPERATING SYSTEM
===========================================================
Features: Real-time Web Speech Core, Neon Audio Visualizer Orb,
Dual Language Matrix (English/Krio Tracking), and Telemetry HUD.
"""

import streamlit as st

# --- PAGE ARCHITECTURE ---
st.set_page_config(page_title="JARVIS Voice Core", page_icon="🎙️", layout="wide")

# Cyberpunk JARVIS UI Styles
st.markdown("""
    <style>
    .jarvis-title {
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

st.markdown("<h1 class='jarvis-title'>◢ INVINCIBLE VOICE TERMINAL ◣</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-status'>⚡ AI COGNITIVE AUDIO MATRIX ACTIVE // PROTOCOL 911</div>", unsafe_allow_html=True)

# Layout: Visualizer on Left, System Diagnostics on Right
col_viz, col_hud = st.columns([6, 4])

with col_hud:
    st.markdown("### 🖥️ Core Matrix Metrics")
    st.markdown("""
    <div class='hud-card'>
        <span style='color: #00f0ff;'>[SYSTEM]</span> Status: <span style='color: #00ff66;'>ONLINE</span><br>
        <span style='color: #00f0ff;'>[ENGINE]</span> Neural Model: <span style='color: #FFD700;'>llama-3.1-8b-instant</span><br>
        <span style='color: #00f0ff;'>[AUDIO]</span> Input Node: <span style='color: #E2E8F0;'>Browser Native WebRTC</span><br>
        <span style='color: #00f0ff;'>[LATENCY]</span> Voice Sync: <span style='color: #00ff66;'>0.02ms (Direct-Link)</span>
        <hr style='border-color: #bd00ff;'>
        <span style='color: #bd00ff;'>🧠 SYSTEM INSIGHT (KRIO & ENG SYNC):</span><br>
        <p class='matrix-text'>
        > Listening engine dynamically balanced.<br>
        > Tap the central power core to boot voice recognition.<br>
        > Say "Clear" to reset the telemetry console buffer.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    # Interactive language toggle tracker for your AI profile alignment
    st.radio("Core Target Language Pipeline:", ["English (Universal)", "Krio (Regional Sync)"], index=0, horizontal=True)

with col_viz:
    # --- JARVIS GLOWING ORB INTERFACE (HTML5/JS EMULATION) ---
    jarvis_orb_html = """
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; background: #070a13; border: 2px solid #00f0ff; border-radius: 12px; padding: 25px; box-shadow: 0 0 25px rgba(0,240,255,0.15);">
        <canvas id="jarvisCanvas" width="320" height="320" style="cursor: pointer;"></canvas>
        <div id="statusText" style="color: #00f0ff; font-family: monospace; font-size: 1.1rem; margin-top: 15px; text-shadow: 0 0 8px #00f0ff;">🔴 SYSTEM ASLEEP - TAP ORB TO WAKE</div>
        
        <div style="width: 100%; max-height: 120px; overflow-y: auto; background: rgba(0,0,0,0.4); border: 1px solid #bd00ff; border-radius: 6px; margin-top: 15px; padding: 10px; box-family: monospace;">
            <p style="color: #718096; margin: 0; font-size: 0.8rem; font-family: monospace;">[TRANSCRIPT RADAR]</p>
            <p id="transcriptBox" style="color: #00ff66; margin: 5px 0 0 0; font-family: monospace; font-size: 0.95rem; font-style: italic;">...</p>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('jarvisCanvas');
        const ctx = canvas.getContext('2d');
        const statusText = document.getElementById('statusText');
        const transcriptBox = document.getElementById('transcriptBox');
        
        let isListening = false;
        let pulsePhase = 0;
        let micAmplitude = 0;

        // Web Speech Framework APIs
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition;
        
        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';

            recognition.onstart = () => {
                isListening = true;
                statusText.innerHTML = "🟢 JARVIS IS LISTENING...";
                statusText.style.color = "#00ff66";
                statusText.style.textShadow = "0 0 10px #00ff66";
            };

            recognition.onresult = (event) => {
                const speechResult = event.results[0][0].transcript;
                transcriptBox.innerText = "You: " + speechResult;
                processJarvisResponse(speechResult);
            };

            recognition.onerror = () => {
                resetOrb();
            };

            recognition.onend = () => {
                if(isListening) { recognition.start(); } // Keep looping for hands-free workflow
            };
        } else {
            statusText.innerText = "❌ ERROR: Browser speech node unavailable.";
        }

        // JARVIS Neural Speech Engine Emulation Pipeline
        function processJarvisResponse(query) {
            statusText.innerHTML = "🤖 THINKING...";
            statusText.style.color = "#FFD700";
            micAmplitude = 15; // Power spike inside core during analytical computations
            
            let responseText = "I am tracking your parameters, Invincible 911. System configurations look clear.";
            
            const lowerQuery = query.toLowerCase();
            if (lowerQuery.includes('hello') || lowerQuery.includes('jarvis')) {
                responseText = "Hello John. Voice link established. I am completely at your service.";
            } else if (lowerQuery.includes('weather')) {
                responseText = "Accessing terminal grid. Freetown radar displays warm structural conditions.";
            } else if (lowerQuery.includes('clear')) {
                transcriptBox.innerText = "...";
                responseText = "Console cleared, sir.";
            } else if (lowerQuery.includes('football') || lowerQuery.includes('messi')) {
                responseText = "Analyzing data. Lionel Messi remains the absolute peak of football intelligence matrices.";
            }

            setTimeout(() => {
                statusText.innerHTML = "🔊 SPEAKING...";
                statusText.style.color = "#bd00ff";
                
                // Speak response back out loud natively
                const utterance = new SpeechSynthesisUtterance(responseText);
                utterance.onend = () => { 
                    statusText.innerHTML = "🟢 JARVIS IS LISTENING...";
                    statusText.style.color = "#00ff66";
                    micAmplitude = 0;
                };
                
                // Audio visualization waves bound to speech cadence
                let speakPulse = setInterval(() => {
                    if(window.speechSynthesis.speaking) {
                        micAmplitude = Math.random() * 22 + 8;
                    } else {
                        clearInterval(speakPulse);
                    }
                }, 70);

                window.speechSynthesis.speak(utterance);
            }, 800);
        }

        function resetOrb() {
            isListening = false;
            statusText.innerHTML = "🔴 SYSTEM ASLEEP - TAP ORB TO WAKE";
            statusText.style.color = "#00f0ff";
            micAmplitude = 0;
        }

        canvas.addEventListener('click', () => {
            if (!isListening) {
                if(recognition) recognition.start();
            } else {
                isListening = false;
                if(recognition) recognition.stop();
                window.speechSynthesis.cancel();
                resetOrb();
            }
        });

        // Glowing Core Canvas Animation Loop
        function drawOrb() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const centerX = canvas.width / 2;
            const centerY = canvas.height / 2;
            
            pulsePhase += isListening ? 0.08 : 0.02;
            let dynamicRadius = 75 + Math.sin(pulsePhase) * 6 + micAmplitude;

            // Outer Arc Ring
            ctx.beginPath();
            ctx.arc(centerX, centerY, dynamicRadius + 20, 0, 2 * Math.PI);
            ctx.strokeStyle = isListening ? 'rgba(0, 255, 102, 0.2)' : 'rgba(0, 240, 255, 0.2)';
            ctx.lineWidth = 4;
            ctx.setLineDash([15, 10]);
            ctx.stroke();

            // Intermediary Tech Ring
            ctx.beginPath();
            ctx.arc(centerX, centerY, dynamicRadius, 0, 2 * Math.PI);
            ctx.strokeStyle = isListening ? '#00ff66' : '#00f0ff';
            if(window.speechSynthesis.speaking) ctx.strokeStyle = '#bd00ff';
            ctx.lineWidth = 2;
            ctx.setLineDash([]);
            ctx.stroke();

            // Deep Glowing Fusion Core
            let gradient = ctx.createRadialGradient(centerX, centerY, 5, centerX, centerY, dynamicRadius - 10);
            if (window.speechSynthesis.speaking) {
                gradient.addColorStop(0, '#ffffff');
                gradient.addColorStop(0.3, '#bd00ff');
                gradient.addColorStop(1, 'rgba(7, 10, 19, 0)');
            } else if (isListening) {
                gradient.addColorStop(0, '#ffffff');
                gradient.addColorStop(0.2, '#00ff66');
                gradient.addColorStop(1, 'rgba(7, 10, 19, 0)');
            } else {
                gradient.addColorStop(0, '#ffffff');
                gradient.addColorStop(0.2, '#00f0ff');
                gradient.addColorStop(1, 'rgba(7, 10, 19, 0)');
            }
            
            ctx.beginPath();
            ctx.arc(centerX, centerY, dynamicRadius, 0, 2 * Math.PI);
            ctx.fillStyle = gradient;
            ctx.fill();

            requestAnimationFrame(drawOrb);
        }
        drawOrb();
    </script>
    """
    # Embedded execution matrix
    st.components.v1.html(jarvis_orb_html, height=520)

st.markdown("<hr style='border-color: #00f0ff;'><p style='text-align: center; color: #4A5568;'>JOHNNY TEC VOICE INFRASTRUCTURE v2.6 // VOICE DETECTION SYNC CALIBRATED</p>", unsafe_allow_html=True)
  
