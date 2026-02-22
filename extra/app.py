import streamlit as st
from PIL import Image
import tempfile, os

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="AgroVisionNet", layout="wide", page_icon="🌾")

# ─── Session State Defaults ───────────────────────────────────────────────────
if "page"           not in st.session_state: st.session_state.page          = "main"
if "chat_history"   not in st.session_state: st.session_state.chat_history  = []
if "analysis_done"  not in st.session_state: st.session_state.analysis_done = False

# ─── Inject ALL CSS once at the very top ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,800;1,600&family=Lato:wght@300;400;700&display=swap');

/* ── Reset & Layout ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 3rem 3rem !important; max-width: 1280px !important; }

/* ── Keyframes ── */
@keyframes floatPollen {
  from { transform: translateY(0)   rotate(0deg);  opacity: 0.6; }
  to   { transform: translateY(-20px) rotate(8deg);  opacity: 1;   }
}
@keyframes riseUp {
  from { opacity:0; transform: translateY(30px); }
  to   { opacity:1; transform: translateY(0);    }
}
@keyframes swayLeaf {
  from { transform: rotate(-3deg) translateX(0);    }
  to   { transform: rotate( 3deg) translateX(10px); }
}
@keyframes fadeSlide {
  from { opacity:0; transform: translateY(16px); }
  to   { opacity:1; transform: translateY(0);    }
}
@keyframes popIn {
  from { opacity:0; transform: scale(0.9); }
  to   { opacity:1; transform: scale(1);   }
}
@keyframes fabFloat {
  0%,100% { transform: translateY(0)   scale(1);    }
  50%     { transform: translateY(-7px) scale(1.05); }
}
@keyframes tooltipFloat {
  0%,100% { transform: translateY(0);   opacity: 0.85; }
  50%     { transform: translateY(-4px); opacity: 1;    }
}
@keyframes rippleAnim {
  0%   { transform: scale(1);   opacity: 0.7; }
  100% { transform: scale(1.9); opacity: 0;   }
}
@keyframes botBounce {
  0%,100% { transform: translateY(0)    rotate(0deg);  }
  40%     { transform: translateY(-12px) rotate(-5deg); }
  60%     { transform: translateY(-7px)  rotate( 3deg); }
}
@keyframes tdBounce {
  0%,80%,100% { transform: translateY(0);   }
  40%         { transform: translateY(-7px); }
}

/* ══════════════════════════════════════
   MAIN PAGE STYLES
══════════════════════════════════════ */
.main-bg .stApp,
.stApp {
  background:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100%25' height='100%25'%3E%3Cdefs%3E%3CradialGradient id='sun' cx='80%25' cy='5%25' r='40%25'%3E%3Cstop offset='0%25' stop-color='%23ffe8b0' stop-opacity='0.7'/%3E%3Cstop offset='100%25' stop-color='transparent'/%3E%3C/radialGradient%3E%3C/defs%3E%3Crect fill='url(%23sun)' width='100%25' height='100%25'/%3E%3C/svg%3E"),
    linear-gradient(170deg, #d8f3dc 0%, #b7e4c7 30%, #fefae0 70%, #f4d47a22 100%);
  font-family: 'Lato', sans-serif;
}
.stApp::before {
  content: '';
  position: fixed; inset: 0; pointer-events: none;
  background-image:
    radial-gradient(1.5px 1.5px at 10% 20%, #52b78855 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 30% 60%, #f4a26144 0%, transparent 100%),
    radial-gradient(1px   1px   at 55% 15%, #2d6a4f33 0%, transparent 100%),
    radial-gradient(2px   2px   at 75% 40%, #e9c46a44 0%, transparent 100%),
    radial-gradient(1px   1px   at 90% 80%, #52b78833 0%, transparent 100%);
  animation: floatPollen 18s ease-in-out infinite alternate;
}

/* Hero */
.hero {
  background: linear-gradient(135deg, rgba(45,106,79,0.92) 0%, rgba(62,32,5,0.85) 100%);
  border-radius: 24px; padding: 2.8rem 3rem 2rem; margin-bottom: 2rem;
  box-shadow: 0 20px 60px rgba(45,106,79,0.3);
  position: relative; overflow: hidden;
  animation: riseUp 0.8s cubic-bezier(0.22,1,0.36,1) both;
}
.hero::after {
  content: '🌾🌿🌻🌾🌿';
  position: absolute; bottom: -6px; right: 2rem;
  font-size: 2.4rem; opacity: 0.25; letter-spacing: 8px;
  animation: swayLeaf 6s ease-in-out infinite alternate;
}
.hero h1 {
  font-family: 'Playfair Display', serif !important;
  font-size: 3.2rem !important; color: #fefae0 !important;
  margin: 0 0 0.3rem !important; text-shadow: 0 4px 20px rgba(0,0,0,0.4);
}
.hero p { color: #b7e4c7; font-size: 1.1rem; margin: 0; font-weight: 300; }

/* Cards */
.farm-card {
  background: rgba(254,250,224,0.85); backdrop-filter: blur(12px);
  border: 1.5px solid rgba(82,183,136,0.3); border-radius: 20px;
  padding: 1.8rem 2rem; margin-bottom: 1.5rem;
  box-shadow: 0 8px 32px rgba(45,106,79,0.10);
  transition: transform 0.3s, box-shadow 0.3s;
  animation: fadeSlide 0.6s ease both;
}
.farm-card:hover { transform: translateY(-4px); box-shadow: 0 16px 48px rgba(45,106,79,0.18); }

/* Section header */
.section-header {
  font-family: 'Playfair Display', serif; color: #2d6a4f;
  font-size: 1.5rem; font-weight: 700;
  margin-bottom: 1rem; padding-bottom: 0.4rem;
  border-bottom: 2px solid rgba(82,183,136,0.3);
}

/* Selectbox */
.stSelectbox > div > div {
  background: rgba(45,106,79,0.12) !important;
  border: 1.5px solid #52b788 !important;
  border-radius: 12px !important; color: #2d6a4f !important;
}

/* File uploader */
.stFileUploader > div {
  border: 2.5px dashed #52b788 !important;
  border-radius: 16px !important; background: rgba(82,183,136,0.06) !important;
  transition: background 0.3s;
}
.stFileUploader > div:hover { background: rgba(82,183,136,0.12) !important; }

/* Text input */
.stTextInput > div > div > input {
  border: 1.5px solid #52b788 !important;
  border-radius: 12px !important; background: rgba(254,250,224,0.7) !important;
  color: #3e2005 !important; padding: 0.6rem 1rem !important;
}
.stTextInput > div > div > input:focus { box-shadow: 0 0 0 3px rgba(82,183,136,0.3) !important; }

/* Buttons */
.stButton > button {
  background: linear-gradient(135deg, #2d6a4f, #52b788) !important;
  color: #fefae0 !important; border: none !important;
  border-radius: 14px !important; padding: 0.7rem 2rem !important;
  font-family: 'Playfair Display', serif !important;
  font-size: 1.05rem !important; font-weight: 600 !important;
  box-shadow: 0 6px 20px rgba(45,106,79,0.35) !important;
  transition: all 0.25s ease !important;
}
.stButton > button:hover {
  transform: translateY(-2px) scale(1.02) !important;
  box-shadow: 0 10px 30px rgba(45,106,79,0.45) !important;
}
.stButton > button:active { transform: scale(0.98) !important; }

/* Metrics */
[data-testid="metric-container"] {
  background: linear-gradient(135deg, rgba(255,255,255,0.7), rgba(216,243,220,0.5)) !important;
  border: 1.5px solid rgba(82,183,136,0.4) !important;
  border-radius: 16px !important; padding: 1.2rem 1.5rem !important;
  box-shadow: 0 4px 16px rgba(45,106,79,0.08); transition: transform 0.25s;
}
[data-testid="metric-container"]:hover { transform: scale(1.03); }
[data-testid="metric-container"] label {
  color: #5c3317 !important; font-weight: 700 !important; font-size: 0.85rem !important;
}
[data-testid="metric-container"] [data-testid="metric-value"] {
  color: #2d6a4f !important; font-family: 'Playfair Display', serif !important; font-size: 1.6rem !important;
}

/* Alerts / HR */
.stAlert { border-radius: 14px !important; border-left: 5px solid #52b788 !important; }
hr { border-color: rgba(82,183,136,0.25) !important; margin: 1.5rem 0 !important; }

/* Weather strip */
.weather-strip {
  display: flex; gap: 1.2rem; flex-wrap: wrap;
  background: linear-gradient(90deg, rgba(45,106,79,0.12), rgba(82,183,136,0.08));
  border-radius: 14px; padding: 1rem 1.5rem;
  border: 1px solid rgba(82,183,136,0.3);
  font-size: 1.05rem; color: #3e2005; font-weight: 600;
}

/* Tip items */
.tip-item {
  display: flex; align-items: flex-start; gap: 0.8rem;
  padding: 0.75rem 1rem; background: rgba(82,183,136,0.10);
  border-radius: 12px; margin-bottom: 0.6rem;
  border-left: 4px solid #52b788; color: #3e2005;
  animation: fadeSlide 0.4s ease both;
}

/* Badges */
.badge { display: inline-block; padding: 0.3rem 1rem; border-radius: 999px; font-size: 0.82rem; font-weight: 700; text-transform: uppercase; }
.badge-low    { background: #b7e4c7; color: #1b4332; }
.badge-medium { background: #f4d47a; color: #7c4d00; }
.badge-high   { background: #ffb4b4; color: #7c0000; }

/* Ground deco */
.ground-deco {
  text-align: center; font-size: 2rem; letter-spacing: 6px;
  opacity: 0.18; margin-top: 2rem;
  animation: swayLeaf 8s ease-in-out infinite alternate;
}

/* FAB button */
.chat-fab-outer {
  position: fixed; bottom: 2.2rem; right: 2.2rem; z-index: 9999;
  display: flex; flex-direction: column; align-items: flex-end; gap: 0.5rem;
  pointer-events: none;
}
.chat-fab-tooltip {
  background: #2d6a4f; color: #fefae0;
  font-family: 'Lato', sans-serif; font-size: 0.8rem; font-weight: 700;
  padding: 0.35rem 1rem; border-radius: 20px;
  box-shadow: 0 4px 14px rgba(45,106,79,0.4);
  animation: tooltipFloat 2.5s ease-in-out infinite;
  pointer-events: none;
}
.ripple-ring {
  position: absolute; width: 62px; height: 62px; border-radius: 50%;
  border: 2.5px solid #52b788; pointer-events: none;
  animation: rippleAnim 2s ease-out infinite;
}
.ripple-ring2 { animation-delay: 0.9s; }

/* ══════════════════════════════════════
   CHATBOT PAGE STYLES
══════════════════════════════════════ */
.chat-bg {
  background: linear-gradient(160deg, #1b4332 0%, #2d6a4f 35%, #081c15 100%) !important;
}

.chat-hero {
  text-align: center; padding: 1.2rem 1rem 0.8rem;
  animation: riseUp 0.7s cubic-bezier(0.22,1,0.36,1) both;
}
.bot-avatar {
  font-size: 4.5rem; display: block; margin-bottom: 0.4rem;
  animation: botBounce 3s ease-in-out infinite;
}
.chat-hero h2 {
  font-family: 'Playfair Display', serif !important;
  color: #fefae0 !important; font-size: 2.2rem !important;
  margin: 0 0 0.3rem !important; text-shadow: 0 4px 16px rgba(0,0,0,0.5);
}
.chat-hero p { color: #95d5b2; font-size: 0.95rem; margin: 0; font-weight: 300; }

/* Context pills */
.ctx-bar { text-align: center; margin-bottom: 1rem; }
.ctx-pill {
  display: inline-flex; align-items: center; gap: 0.4rem;
  background: rgba(82,183,136,0.2); border: 1px solid rgba(82,183,136,0.45);
  border-radius: 999px; padding: 0.3rem 0.9rem;
  font-size: 0.78rem; color: #d8f3dc; font-weight: 600;
  margin: 0 0.2rem 0.4rem; backdrop-filter: blur(4px);
}

/* Chips */
.chip-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem; }
.chip {
  background: rgba(82,183,136,0.15); border: 1px solid rgba(82,183,136,0.4);
  color: #b7e4c7; border-radius: 999px; padding: 0.3rem 0.85rem;
  font-size: 0.78rem; font-weight: 600; font-family: 'Lato', sans-serif;
}

/* Chat window */
.chat-window {
  background: rgba(8,28,21,0.55); backdrop-filter: blur(20px);
  border: 1.5px solid rgba(82,183,136,0.2); border-radius: 22px;
  padding: 1.3rem; min-height: 300px; max-height: 420px;
  overflow-y: auto; margin-bottom: 0.8rem;
  box-shadow: inset 0 2px 20px rgba(0,0,0,0.3), 0 8px 32px rgba(0,0,0,0.3);
}
.chat-window::-webkit-scrollbar { width: 4px; }
.chat-window::-webkit-scrollbar-thumb { background: rgba(82,183,136,0.35); border-radius: 4px; }

/* Chat bubble rows */
.brow-user {
  display: flex; justify-content: flex-end;
  margin-bottom: 1rem; animation: popIn 0.3s ease both;
}
.brow-bot {
  display: flex; justify-content: flex-start; align-items: flex-end; gap: 0.5rem;
  margin-bottom: 1rem; animation: popIn 0.3s ease both;
}
.bubble-u {
  background: linear-gradient(135deg, #2d6a4f, #40916c);
  color: #fefae0; border-radius: 22px 22px 5px 22px;
  padding: 0.8rem 1.1rem; max-width: 72%;
  font-size: 0.93rem; line-height: 1.55;
  box-shadow: 0 6px 20px rgba(45,106,79,0.5);
}
.bubble-b {
  background: rgba(254,250,224,0.93); color: #3e2005;
  border: 1.5px solid rgba(82,183,136,0.25); border-radius: 22px 22px 22px 5px;
  padding: 0.8rem 1.1rem; max-width: 78%;
  font-size: 0.93rem; line-height: 1.55;
  box-shadow: 0 6px 20px rgba(0,0,0,0.2);
}
.blabel {
  font-size: 0.65rem; font-weight: 700; letter-spacing: 1px;
  text-transform: uppercase; margin-bottom: 0.2rem; opacity: 0.55;
}
.blabel-u { text-align: right; color: #95d5b2; }
.blabel-b { color: #5c3317; }
.bot-ico {
  width: 32px; height: 32px; border-radius: 50%;
  background: linear-gradient(135deg, #2d6a4f, #52b788);
  display: flex; align-items: center; justify-content: center;
  font-size: 1rem; flex-shrink: 0;
  box-shadow: 0 3px 10px rgba(45,106,79,0.5);
}

/* Typing dots */
.typing { display: inline-flex; gap: 4px; align-items: center; padding: 2px 4px; }
.td { width: 7px; height: 7px; border-radius: 50%; background: #52b788; animation: tdBounce 1.1s ease-in-out infinite; }
.td:nth-child(2) { animation-delay: 0.18s; }
.td:nth-child(3) { animation-delay: 0.36s; }

/* Chat input area */
.input-wrap {
  background: rgba(8,28,21,0.45); backdrop-filter: blur(14px);
  border: 1.5px solid rgba(82,183,136,0.25); border-radius: 18px;
  padding: 0.9rem 1rem; margin-bottom: 0.6rem;
}

/* Chat footer */
.chat-footer {
  text-align: center; color: rgba(149,213,178,0.3);
  font-size: 0.7rem; margin-top: 1rem; font-family: 'Lato', sans-serif;
}

/* Back button override for dark chatbot page */
.back-btn .stButton > button {
  background: rgba(254,250,224,0.12) !important;
  color: #fefae0 !important;
  border: 1.5px solid rgba(254,250,224,0.3) !important;
  font-family: 'Lato', sans-serif !important; font-size: 0.9rem !important;
  padding: 0.5rem 1.4rem !important;
}
.back-btn .stButton > button:hover {
  background: rgba(254,250,224,0.22) !important;
  transform: translateX(-4px) !important;
}
</style>
""", unsafe_allow_html=True)


# ─── MOCK functions (replace with your real imports) ─────────────────────────
def predict_image(path):
    return "Leaf Blight", 0.87

def get_weather(city):
    return 32, 78, 12, 0.42

def get_climate_risk_from_values(temp, hum, rain, soil):
    return 0.63

def fusion_decision(disease, conf, risk):
    return "Medium", "⚠️ Moderate risk detected. Immediate action advised to prevent spread."

def get_recommendation(disease, severity, risk):
    return [
        "Apply copper-based fungicide every 7 days.",
        "Ensure proper drainage around the crop bed.",
        "Remove and destroy infected leaves promptly.",
        "Maintain plant spacing for good air circulation.",
        "Monitor soil moisture — avoid overwatering.",
    ]

def ask_farmer_bot(question, disease, weather_ctx):
    return (
        f"Based on the detected {disease} and current weather ({weather_ctx}), "
        "I recommend increasing fungicide frequency and checking for waterlogging near roots. "
        "Also consider applying neem oil as an organic alternative. "
        "Would you like more details on dosage or application timing?"
    )


# ═════════════════════════════════════════════════════════════════════════════
#  MAIN PAGE
# ═════════════════════════════════════════════════════════════════════════════
def render_main():
    translations = {
        "en": {
            "upload": "📷 Upload Crop / Leaf Image",
            "city": "📍 Your City",
            "analyze": "Analyze Now",
            "report": "Analysis Report",
            "recommendations": "Recommendations",
        },
        "ta": {
            "upload": "📷 பயிர் / இலை படம் பதிவேற்றவும்",
            "city": "📍 உங்கள் நகரம்",
            "analyze": "இப்போது பகுப்பாய்வு செய்",
            "report": "பகுப்பாய்வு அறிக்கை",
            "recommendations": "பரிந்துரைகள்",
        }
    }

    # ── Hero ──
    st.markdown("""
    <div class="hero">
      <h1>🌾 AgroVisionNet</h1>
      <p>AI-powered crop intelligence for every farmer · from field to forecast</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Language + City ──
    col_lang, col_city = st.columns([1, 2])
    with col_lang:
        lang = st.selectbox("Language", ["English", "தமிழ்"], label_visibility="collapsed")
    t = translations["ta"] if lang == "தமிழ்" else translations["en"]
    with col_city:
        city = st.text_input("City", "Chennai", placeholder=t["city"], label_visibility="collapsed")

    st.markdown("---")

    # ── Upload + Analyze ──
    up_col, btn_col = st.columns([3, 1])
    with up_col:
        uploaded = st.file_uploader(t["upload"], type=["jpg", "png", "jpeg"])
    with btn_col:
        st.markdown("<div style='margin-top:1.9rem'></div>", unsafe_allow_html=True)
        analyze = st.button("🌿 " + t["analyze"], use_container_width=True)

    # ── Analysis ──
    if analyze:
        if not uploaded:
            st.warning("🌱 Please upload a crop or leaf image first.")
        else:
            image = Image.open(uploaded)
            with st.spinner("🔬 Scanning crop health patterns…"):
                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                    tmp_path = tmp.name
                image.save(tmp_path)
                disease, conf = predict_image(tmp_path)
                try: os.remove(tmp_path)
                except: pass
                temp, hum, rain, soil = get_weather(city)
                risk     = get_climate_risk_from_values(temp, hum, rain, soil)
                severity, decision = fusion_decision(disease, conf, risk)
                tips     = get_recommendation(disease, severity, risk)

            # Save context for chatbot
            st.session_state.update({
                "last_disease": disease, "last_conf": conf,
                "last_temp": temp,       "last_hum": hum,
                "last_rain": rain,       "last_soil": soil,
                "last_risk": risk,       "last_severity": severity,
                "analysis_done": True,   "chat_history": []
            })

            st.balloons()

            # Report card
            st.markdown('<div class="farm-card">', unsafe_allow_html=True)
            pc, ic = st.columns([1, 2])
            with pc:
                st.image(image, use_container_width=True, caption="Uploaded Image")
            with ic:
                st.markdown(f'<div class="section-header">🌿 {t["report"]}</div>', unsafe_allow_html=True)
                badge_cls = "badge-low" if severity == "Low" else ("badge-high" if severity == "High" else "badge-medium")
                st.markdown(f'<span class="badge {badge_cls}">Severity: {severity}</span>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                m1, m2, m3 = st.columns(3)
                m1.metric("🦠 Disease",      disease)
                m2.metric("🎯 Confidence",   f"{conf*100:.1f}%")
                m3.metric("⚠️ Climate Risk", f"{risk*100:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)

            st.info(decision)

            # Weather
            st.markdown('<div class="farm-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">🌦 Weather Conditions</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="weather-strip">
              <span>🌡️ {temp}°C</span>
              <span>💧 Humidity {hum}%</span>
              <span>🌧️ Rainfall {rain} mm</span>
              <span>🌱 Soil {soil*100:.0f}%</span>
            </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Tips
            st.markdown('<div class="farm-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="section-header">🌱 {t["recommendations"]}</div>', unsafe_allow_html=True)
            for tip in tips:
                st.markdown(f'<div class="tip-item">✅ {tip}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ── Floating Chat Button ──
    st.markdown("""
    <div class="chat-fab-outer">
      <div class="chat-fab-tooltip">🤖 Ask AgroBot</div>
      <div style="position:relative;display:inline-block;width:62px;height:62px;">
        <div class="ripple-ring"></div>
        <div class="ripple-ring ripple-ring2"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Real Streamlit button positioned at bottom-right via columns
    spacer, fab_col = st.columns([20, 1])
    with fab_col:
        if st.button("🤖", key="open_chat", help="Open AI Farmer Assistant"):
            st.session_state.page = "chatbot"
            st.rerun()

    # Footer
    st.markdown("""
    <div class="ground-deco">🌾 🌿 🌻 🌱 🪴 🌻 🌿 🌾</div>
    <p style="text-align:center;color:#5c3317;opacity:0.35;font-size:0.78rem;
       margin-top:0.5rem;font-family:'Lato',sans-serif;">
      AgroVisionNet · Empowering Farmers with AI
    </p>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
#  CHATBOT PAGE
# ═════════════════════════════════════════════════════════════════════════════
def render_chatbot():
    disease  = st.session_state.get("last_disease",  "Unknown")
    conf     = st.session_state.get("last_conf",     0.0)
    temp     = st.session_state.get("last_temp",     "--")
    hum      = st.session_state.get("last_hum",      "--")
    severity = st.session_state.get("last_severity", "--")
    has_ctx  = st.session_state.get("analysis_done", False)

    # Dark background for chatbot page
    st.markdown("""
    <style>
    .stApp {
      background: linear-gradient(160deg, #1b4332 0%, #2d6a4f 35%, #081c15 100%) !important;
    }
    .stApp::before { display: none; }
    </style>
    """, unsafe_allow_html=True)

    # ── Back button ──
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Back to Analysis", key="back_btn"):
        st.session_state.page = "main"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Hero ──
    st.markdown("""
    <div class="chat-hero">
      <span class="bot-avatar">🤖</span>
      <h2>AI Farmer Assistant</h2>
      <p>Your personal agronomist · Powered by AgroVisionNet AI</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Context pills ──
    if has_ctx:
        st.markdown(f"""
        <div class="ctx-bar">
          <span class="ctx-pill">🦠 {disease}</span>
          <span class="ctx-pill">🎯 {conf*100:.0f}% confidence</span>
          <span class="ctx-pill">🌡️ {temp}°C · 💧 {hum}%</span>
          <span class="ctx-pill">⚠️ Severity: {severity}</span>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="ctx-bar">
          <span class="ctx-pill">💡 Run an analysis first for crop-specific advice</span>
        </div>""", unsafe_allow_html=True)

    # ── Suggestion chips ──
    st.markdown("""
    <div class="chip-row">
      <span class="chip">💊 Best treatment?</span>
      <span class="chip">🌾 Safe to harvest?</span>
      <span class="chip">🍃 Organic alternatives?</span>
      <span class="chip">🚫 How to prevent spread?</span>
      <span class="chip">🌿 Fertilizer tips?</span>
    </div>""", unsafe_allow_html=True)

    # ── Welcome message ──
    if not st.session_state.chat_history:
        if has_ctx:
            welcome = (f"🌾 Namaste! I've reviewed your crop analysis — detected <b>{disease}</b> "
                       f"with <b>{conf*100:.0f}% confidence</b>. Weather shows {temp}°C with {hum}% humidity. "
                       "Ask me anything about treatment, prevention, or organic alternatives!")
        else:
            welcome = ("🌾 Namaste! I'm AgroBot, your AI farming assistant. "
                       "Go back and run a crop analysis first for personalised advice, "
                       "or ask me any general farming question!")
        st.session_state.chat_history.append({"role": "bot", "text": welcome})

    # ── Render chat bubbles ──
    chat_html = '<div class="chat-window" id="cw">'
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            chat_html += f"""
            <div class="brow-user">
              <div>
                <div class="blabel blabel-u">You</div>
                <div class="bubble-u">{msg['text']}</div>
              </div>
            </div>"""
        else:
            chat_html += f"""
            <div class="brow-bot">
              <div class="bot-ico">🌾</div>
              <div>
                <div class="blabel blabel-b">AgroBot</div>
                <div class="bubble-b">{msg['text']}</div>
              </div>
            </div>"""
    chat_html += """</div>
    <script>
      var cw = document.getElementById('cw');
      if (cw) cw.scrollTop = cw.scrollHeight;
    </script>"""
    st.markdown(chat_html, unsafe_allow_html=True)

    # ── Input bar ──
    st.markdown('<div class="input-wrap">', unsafe_allow_html=True)
    q_col, s_col = st.columns([5, 1])
    with q_col:
        question = st.text_input(
            "question", key="chat_q",
            placeholder="🌱 Ask about crops, disease, fertilizer…",
            label_visibility="collapsed"
        )
    with s_col:
        send = st.button("Send 🌿", use_container_width=True, key="send_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Handle message ──
    if send and question.strip():
        st.session_state.chat_history.append({"role": "user", "text": question})
        weather_ctx = f"{temp}°C & humidity {hum}%" if has_ctx else "unknown weather"
        with st.spinner("🌱 AgroBot is thinking…"):
            reply = ask_farmer_bot(question, disease, weather_ctx)
        st.session_state.chat_history.append({"role": "bot", "text": reply})
        st.rerun()

    # ── Clear chat ──
    if len(st.session_state.chat_history) > 1:
        if st.button("🗑️ Clear Chat", key="clear_btn"):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown('<div class="chat-footer">🌾 AgroVisionNet · AI Farmer Assistant</div>', unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
#  ROUTER — must be at the very bottom
# ═════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "chatbot":
    render_chatbot()
else:
    render_main()