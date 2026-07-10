import streamlit as st, random, json, urllib.parse
from datetime import datetime

st.set_page_config(page_title="JOHNNY TEC", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.stApp{background:#050510;color:#e0e0ff;}
.main>div{padding:0 !important;}
.hud-box{background:linear-gradient(135deg,#0a0a1a,#151530);border:1px solid #00f0ff33;border-radius:12px;padding:14px;margin:6px 0;text-align:center;}
.hud-title{color:#00f0ff;font-size:10px;text-transform:uppercase;letter-spacing:2px;margin-bottom:4px;}
.hud-val{color:#bd00ff;font-size:24px;font-weight:800;text-shadow:0 0 12px #bd00ff44;}
#hud-status{color:#00f0ff;}
.orb-wrap{display:flex;justify-content:center;align-items:center;height:380px;position:relative;}
#orbCanvas{cursor:pointer;transition:transform 0.3s ease;}
#orbCanvas:hover{transform:scale(1.05);}
.log-box{max-height:110px;overflow-y:auto;padding:8px;margin-top:6px;font-family:'Courier New',monospace;font-size:11px;color:#00f0ffaa;border-left:2px solid #00f0ff33;}
.welcome-banner{text-align:center;color:#00f0ff;font-size:16px;margin:14px 0;text-shadow:0 0 12px #00f0ff33;font-weight:500;}
.integrity-bar{width:100%;height:4px;background:#00f0ff22;border-radius:2px;margin-top:6px;overflow:hidden;}
.integrity-fill{height:100%;background:linear-gradient(90deg,#00f0ff,#bd00ff);width:94%;border-radius:2px;}
</style>
""", unsafe_allow_html=True)

TITLES = ["Sir","Abdullah","John","Chief","Commander","Boss","My Friend"]
PREFIXES = ["System matrices stabilized","Power cells at maximum capacity","Neural pathways synchronized","Mainframe online","All sectors nominal","Quantum core aligned","Operational threshold reached"]
MIDPHRASES = ["JOHNNY TEC is fully operational","awaiting your voice command","ready to execute","standing by for directives","systems green across the board","what are our objectives for this hour","how can I assist the mission"]

def gt(): return random.choice(TITLES)
def greet(): return f"{random.choice(PREFIXES)}. Welcome back, {gt()}. {random.choice(MIDPHRASES)}."

WEATHER = {"Freetown":"32°C scattered clouds humidity 78%","West Africa":"Regional monsoon active temps 28-35°C","Lagos":"30°C thunderstorm warning","Accra":"31°C clear skies"}
NEWS = ["Satellite-X7 confirms Atlantic trade corridor expansion","ECOWAS summit concludes with new infrastructure pact","Regional power grid stabilization at 94% capacity","Freetown port throughput up 12% this quarter"]
FOOTBALL = {"Messi":"Inter Miami 2-1 Orlando City — Messi 1 goal 1 assist","Barcelona":"Barcelona 3-0 Sevilla — Lewandowski brace","Real Madrid":"Real Madrid 1-1 Atletico — Bellingham goal"}

def respond(q):
    q = q.lower(); t = gt()
    if any(w in q for w in ["weather","temperature","rain","humid","forecast"]):
        loc = "Freetown" if "freetown" in q else "West Africa" if "africa" in q else "Freetown"
        return f"Atmospheric telemetry for {loc}, {t}: {WEATHER.get(loc, WEATHER['Freetown'])}. Shall I pull extended forecasts?"
    if any(w in q for w in ["news","headline","report","update"]):
        return f"Live satellite uplink confirmed, {t}. Top regional bulletins: {' • '.join(NEWS)}. Do you want sector-specific analysis?"
    if any(w in q for w in ["score","football","soccer","messi","goal","match","game","player"]):
        ply = "Messi" if "messi" in q else "Barcelona" if "barcelona" in q else "Messi"
        return f"Match telemetry locked, {t}. {FOOTBALL.get(ply, FOOTBALL['Messi'])}. Want live substitution data?"
    return f"Acknowledged, {t}. I have routed your request through my core inference matrix. What is the next directive?"

def get_qp(key, default=""):
    v = st.query_params.get(key, default)
    if isinstance(v, list): return v[0] if v else default
    return v if v else default

ui = get_qp("user_input")
response_text = ""

if ui and st.session_state.get("last_ui") != ui:
    st.session_state.last_ui = ui
    response_text = respond(ui)
    try:
        if "user_input" in st.query_params: del st.query_params["user_input"]
    except Exception:
        pass

if "welcome" not in st.session_state:
    st.session_state.welcome = greet()
    st.session_state.boot = datetime.now().strftime("%H:%M:%S")

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="hud-box"><div class="hud-title">System Status</div><div class="hud-val" id="hud-status">ASLEEP</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="hud-box"><div class="hud-title">Uptime</div><div class="hud-val">{st.session_state.boot}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="hud-box"><div class="hud-title">Core Temp</div><div class="hud-val">42.7°C</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="hud-box"><div class="hud-title">Neural Load</div><div class="hud-val">{random.randint(8,18)}%</div><div class="integrity-bar"><div class="integrity-fill"></div></div></div>', unsafe_allow_html=True)

st.markdown("---")

if not ui and not response_text:
    st.markdown(f'<div class="welcome-banner">🗣️ {st.session_state.welcome}</div>', unsafe_allow_html=True)

html = f"""
<div class="orb-wrap"><canvas id="orbCanvas" width="400" height="400"></canvas></div>
<div id="stxt" style="text-align:center;color:#00f0ff;font-size:13px;margin-top:10px;font-family:monospace;letter-spacing:1px;">CLICK ORB TO ACTIVATE</div>
<div class="log-box" id="logBox"></div>
<script>
(function(){{
const C=document.getElementById('orbCanvas'),X=C.getContext('2d'),S=document.getElementById('stxt'),L=document.getElementById('logBox'),H=document.getElementById('hud-status');
let state='ASLEEP',ang=0,pulse=0,cr=40,tcr=40,rec=null,synth=window.speechSynthesis,speaking=false,initResp={json.dumps(response_text)},spoken=false;
const COL={{ASLEEP:{{r:'#00f0ff',g:'rgba(0,240,255,0.3)'}},LISTENING:{{r:'#00ff66',g:'rgba(0,255,102,0.3)'}},THINKING:{{r:'#ffcc00',g:'rgba(255,204,0,0.3)'}},SPEAKING:{{r:'#bd00ff',g:'rgba(189,0,255,0.3)'}}}};
function log(t){{const d=document.createElement('div');d.textContent='» '+t;L.prepend(d);if(L.children.length>20)L.lastChild.remove();}}
function set(s){{state=s;S.textContent='JOHNNY TEC // '+s;if(H)H.textContent=s;log('State: '+s);}}
function draw(){{const w=C.width,h=C.height,cx=w/2,cy=h/2,o=COL[state];X.clearRect(0,0,w,h);X.save();X.translate(cx,cy);X.rotate(ang);X.beginPath();X.arc(0,0,165,0,Math.PI*2);X.setLineDash([22,14]);X.strokeStyle=o.r;X.lineWidth=2;X.stroke();X.restore();X.beginPath();X.arc(cx,cy,125,0,Math.PI*2);X.strokeStyle=o.r;X.lineWidth=1;X.globalAlpha=0.5;X.stroke();X.globalAlpha=1;X.beginPath();X.arc(cx,cy,95,0,Math.PI*2);X.strokeStyle=o.r;X.lineWidth=3;X.stroke();const g=X.createRadialGradient(cx,cy,8,cx,cy,cr*2.6);g.addColorStop(0,o.g);g.addColorStop(1,'transparent');X.fillStyle=g;X.beginPath();X.arc(cx,cy,cr*2.6,0,Math.PI*2);X.fill();const cg=X.createRadialGradient(cx,cy,4,cx,cy,cr);cg.addColorStop(0,'#ffffff');cg.addColorStop(0.25,o.r);cg.addColorStop(1,'transparent');X.fillStyle=cg;X.beginPath();X.arc(cx,cy,cr,0,Math.PI*2);X.fill();X.beginPath();X.arc(cx,cy,cr+pulse,0,Math.PI*2);X.strokeStyle=o.r;X.globalAlpha=0.35-(pulse/55);X.lineWidth=2;X.stroke();X.globalAlpha=1;}}
function anim(){{ang+=0.012;if(state==='SPEAKING')cr=tcr*(0.75+Math.random()*0.5);else cr+=(tcr-cr)*0.08;pulse+=0.6;if(pulse>38)pulse=0;draw();requestAnimationFrame(anim);}}
function speak(t){{if(!t||speaking)return;speaking=true;set('SPEAKING');tcr=58;const u=new SpeechSynthesisUtterance(t);u.rate=0.95;u.pitch=0.92;u.volume=1;u.onend=()=>{{speaking=false;set('ASLEEP');tcr=40;}};u.onerror=()=>{{speaking=false;set('ASLEEP');tcr=40;}};synth.cancel();synth.speak(u);}}
function listen(){{if(!('webkitSpeechRecognition' in window)){{S.textContent='SPEECH API UNAVAILABLE';return;}}if(rec)rec.stop();rec=new webkitSpeechRecognition();rec.continuous=true;rec.interimResults=false;rec.lang='en-US';rec.onstart=()=>{{set('LISTENING');tcr=52;}};rec.onresult=(e)=>{{const txt=e.results[e.results.length-1][0].transcript;log('Heard: '+txt);set('THINKING');tcr=46;rec.stop();const url=new URL(window.location.href);url.searchParams.set('user_input',encodeURIComponent(txt));window.location.href=url.toString();}};rec.onerror=(e)=>{{log('Mic error: '+e.error);if(state!=='SPEAKING')setTimeout(listen,400);}};rec.onend=()=>{{if(state==='LISTENING')setTimeout(listen,150);}};rec.start();}}
function stop(){{if(rec)rec.stop();synth.cancel();set('ASLEEP');tcr=40;speaking=false;}}
C.addEventListener('click',()=>{{if(state==='ASLEEP'){{listen();}}else{{stop();}}}});
setInterval(()=>{{if(state==='LISTENING'&&rec){{try{{rec.start();}}catch(e){{}}}},2500);
if(initResp&&!spoken){{spoken=true;setTimeout(()=>speak(initResp),600);}}
if(initResp){{setTimeout(()=>{{set('SPEAKING');tcr=58;}},80);}}
anim();
}})();
</script>
"""

st.components.v1.html(html, height=500)

st.markdown("---")
st.markdown(f'<div style="text-align:center;color:#00f0ff55;font-size:10px;font-family:monospace;letter-spacing:2px;">JOHNNY TEC v2.0.7 // SECURE CHANNEL // ENCRYPTED // {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
    
