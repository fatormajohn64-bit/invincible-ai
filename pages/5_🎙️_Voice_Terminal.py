"""
JOHNNY TEC — ADVANCED VOICE OPERATING SYSTEM
===========================================================
Features: Real-time Web Speech Core, Neon Audio Visualizer Orb,
Anti-Echo Chamber Tech, and Dynamic Identity Recognition.
"""

import streamlit as st

# --- PAGE ARCHITECTURE ---
st.set_page_config(page_title="JOHNNY TEC Voice Core", page_icon="🎙️", layout="wide")

# Cyberpunk UI Styles
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
st.markdown("<div class='sub-status'>⚡ COGNITIVE AUDIO MATRIX ACTIVE // PROTOCOL 911</div>", unsafe_allow_html=True)

# Layout: Visualizer on Left, System Diagnostics on Right
col_viz, col_hud = st.columns([6, 4])

with col_hud:
    st.markdown("### 🖥️ Core Matrix Metrics")
    st.markdown("""
    <div class='hud-card'>
        <span style='color: #00f0ff;'>[SYSTEM]</span> Identity: <span style='color: #00ff66;'>JOHNNY TEC</span><br>
        <span style='color: #00f0ff;'>[ENGINE]</span> Neural Model: <span style='color: #FFD700;'>llama-3.1-8b-instant</span><br>
        <span style='color: #00f0ff;'>[AUDIO]</span> Feedback Loop: <span style='color: #ff0055;'>ANTI-ECHO ENGAGED</span><br>
        <span style='color: #00f0ff;'>[LATENCY]</span> Voice Sync: <span style='color: #00ff66;'>0.02ms (Direct-Link)</span>
        <hr style='border-color: #bd00ff;'>
        <span style='color: #bd00ff;'>🧠 SYSTEM INSIGHT:</span><br>
        <p class='matrix-text'>
        > Anti-echo protocol prevents infinite talking loops.<br>
        > Tap the central power core to boot voice recognition.<br>
        > Say "Clear" to reset the telemetry console buffer.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.radio("Core Target Language Pipeline:", ["English (Universal)", "Krio (Regional Sync)"], index=0, horizontal=True)

with col_viz:
    # --- JOHNNY TEC GLOWING ORB INTERFACE (UPGRADED LOGIC) ---
    johnny_orb_html = """
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
        
        // High-Level State Engine
        let isListening = false;
        let isSpeaking = false; 
        let pulsePhase = 0;
        let micAmplitude = 0;

        // Dynamic Identity Array
        const userTitles = ["John", "Abdullah", "Sir"];
        const getRandomTitle = () => userTitles[Math.floor(Math.random() * userTitles.length)];

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition;
        
        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';

            recognition.onstart = () => {
                if(isSpeaking) { recognition.abort(); return; } // Anti-Echo Shield
                isListening = true;
                statusText.innerHTML = "🟢 JOHNNY TEC IS LISTENING...";
                statusText.style.color = "#00ff66";
                statusText.style.textShadow = "0 0 10px #00ff66";
            };

            recognition.onresult = (event) => {
                const speechResult = event.results[0][0].transcript;
                transcriptBox.innerText = "You: " + speechResult;
                processVoiceCommand(speechResult);
            };

            recognition.onerror = (event) => {
                if (event.error !== 'aborted') resetOrb();
            };

            recognition.onend = () => {
                // Auto-restart ONLY if we are not speaking to prevent loops
                if(isListening && !isSpeaking) { 
                    try { recognition.start(); } catch(e){} 
                }
            };
        } else {
            statusText.innerText = "❌ ERROR: Browser speech node unavailable.";
        }

        function processVoiceCommand(query) {
            isListening = false; // Stop listening while processing
            if(recognition) recognition.abort(); 

            statusText.innerHTML = "🤖 THINKING...";
            statusText.style.color = "#FFD700";
            micAmplitude = 15;
            
            const lowerQuery = query.toLowerCase();
            const title = getRandomTitle();
            let responseText = `I am tracking your parameters, ${title}. Systems are nominal.`;
            
            // Dynamic Response Matrix
            if (lowerQuery.includes('hello') || lowerQuery.includes('hi')) {
                const greetings = [
                    `Voice link established. Good to hear you, ${title}.`,
                    `Hello ${title}. I am JOHNNY TEC, completely at your service.`,
                    `Systems online. What is our objective today, ${title}?`
                ];
                responseText = greetings[Math.floor(Math.random() * greetings.length)];
            } else if (lowerQuery.includes('weather')) {
                responseText = `Accessing grid. Freetown radar displays warm structural conditions, ${title}.`;
            } else if (lowerQuery.includes('clear')) {
                transcriptBox.innerText = "...";
                responseText = `Console cleared, ${title}. Ready for next command.`;
            } else if (lowerQuery.includes('football') || lowerQuery.includes('messi')) {
                responseText = `Analyzing data. Lionel Messi remains the absolute peak of football matrices, ${title}.`;
            } else if (lowerQuery.includes('who are you') || lowerQuery.includes('your name')) {
                responseText = `I am JOHNNY TEC, your personal artificial intelligence, designed for Invincible 911.`;
            }

            setTimeout(() => {
                statusText.innerHTML = "🔊 JOHNNY TEC SPEAKING...";
                statusText.style.color = "#bd00ff";
                isSpeaking = true; 
                
                const utterance = new SpeechSynthesisUtterance(responseText);
                
                utterance.onend = () => { 
                    isSpeaking = false; 
                    statusText.innerHTML = "🔄 RECALIBRATING MIC...";
                    statusText.style.color = "#FFD700";
                    micAmplitude = 0;
                    
                    // Anti-Echo Timeout: Wait 1.5 seconds before listening again
                    setTimeout(() => {
                        resetOrb();
                    }, 1500);
                };
                
                utterance.onerror = () => {
                    isSpeaking = false;
                    resetOrb();
                };
                
                let speakPulse = setInterval(() => {
                    if(isSpeaking) {
                        micAmplitude = Math.random() * 22 + 8;
                    } else {
                        clearInterval(speakPulse);
                    }
                }, 70);

                window.speechSynthesis.speak(utterance);
            }, 600);
        }

        function resetOrb() {
            isListening = false;
            isSpeaking = false;
            statusText.innerHTML = "🔴 SYSTEM ASLEEP - TAP ORB TO WAKE";
            statusText.style.color = "#00f0ff";
            micAmplitude = 0;
            window.speechSynthesis.cancel();
            if(recognition) recognition.abort();
        }

        canvas.addEventListener('click', () => {
            if (!isListening && !isSpeaking) {
                if(recognition) recognition.start();
            } else {
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
            if (isSpeaking) {
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
    st.components.v1.html(johnny_orb_html, height=520)

st.markdown("<hr style='border-color: #00f0ff;'><p style='text-align: center; color: #4A5568;'>JOHNNY TEC VOICE INFRASTRUCTURE v3.0 // ANTI-ECHO SECURED</p>", unsafe_allow_html=True)
