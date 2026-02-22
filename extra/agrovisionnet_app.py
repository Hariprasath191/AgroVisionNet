import streamlit as st
from PIL import Image
import tempfile, os

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="AgroVisionNet", layout="wide", page_icon="🌾")

# ─── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,800;1,600&family=Lato:wght@300;400;700&display=swap');

/* ── Root Variables ── */
:root {
  --soil:   #3e2005;
  --bark:   #5c3317;
  --leaf:   #2d6a4f;
  --sprout: #52b788;
  --sun:    #f4a261;
  --sky:    #d8f3dc;
  --wheat:  #e9c46a;
  --cream:  #fefae0;
  --mist:   rgba(255,255,255,0.55);
}

/* ── Body / App Background ── */
.stApp {
  background:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100%25' height='100%25'%3E%3Cdefs%3E%3CradialGradient id='sun' cx='80%25' cy='5%25' r='40%25'%3E%3Cstop offset='0%25' stop-color='%23ffe8b0' stop-opacity='0.7'/%3E%3Cstop offset='100%25' stop-color='transparent'/%3E%3C/radialGradient%3E%3C/defs%3E%3Crect fill='url(%23sun)' width='100%25' height='100%25'/%3E%3C/svg%3E"),
    linear-gradient(170deg, #d8f3dc 0%, #b7e4c7 30%, #fefae0 70%, #f4d47a22 100%);
  font-family: 'Lato', sans-serif;
}

/* ── Animated pollen dots ── */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    radial-gradient(1.5px 1.5px at 10% 20%, #52b78855 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 30% 60%, #f4a26144 0%, transparent 100%),
    radial-gradient(1px 1px at 55% 15%, #2d6a4f33 0%, transparent 100%),
    radial-gradient(2px 2px at 75% 40%, #e9c46a44 0%, transparent 100%),
    radial-gradient(1px 1px at 90% 80%, #52b78833 0%, transparent 100%);
  pointer-events: none;
  animation: floatPollen 18s ease-in-out infinite alternate;
}
@keyframes floatPollen {
  from { transform: translateY(0px) rotate(0deg); opacity: 0.6; }
  to   { transform: translateY(-20px) rotate(8deg); opacity: 1; }
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 3rem 3rem; max-width: 1280px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #1b4332 0%, #2d6a4f 60%, #40916c 100%) !important;
  border-right: none !important;
}
[data-testid="stSidebar"] * { color: #d8f3dc !important; }
[data-testid="stSidebar"] .stRadio label {
  font-family: 'Lato', sans-serif !important;
  font-size: 1rem !important;
  padding: 0.4rem 0 !important;
}
[data-testid="stSidebar"] hr { border-color: rgba(82,183,136,0.3) !important; }

/* ── Hero Banner ── */
.hero {
  background:
    linear-gradient(135deg, rgba(45,106,79,0.92) 0%, rgba(62,32,5,0.85) 100%),
    url("data:image/svg+xml,%3Csvg width='60' height='60' xmlns='http://www.w3.org/2000/svg'%3E%3Cellipse cx='30' cy='55' rx='4' ry='8' fill='%232d6a4f22'/%3E%3Cellipse cx='10' cy='50' rx='3' ry='6' fill='%232d6a4f22'/%3E%3Cellipse cx='50' cy='52' rx='3' ry='7' fill='%232d6a4f22'/%3E%3C/svg%3E");
  border-radius: 24px;
  padding: 2.8rem 3rem 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 20px 60px rgba(45,106,79,0.3);
  position: relative;
  overflow: hidden;
  animation: riseUp 0.8s cubic-bezier(0.22,1,0.36,1) both;
}
.hero::after {
  content: '🌾🌿🌻🌾🌿';
  position: absolute;
  bottom: -6px; right: 2rem;
  font-size: 2.4rem;
  opacity: 0.25;
  letter-spacing: 8px;
  animation: swayLeaf 6s ease-in-out infinite alternate;
}
@keyframes swayLeaf {
  from { transform: rotate(-3deg) translateX(0); }
  to   { transform: rotate(3deg) translateX(10px); }
}
@keyframes riseUp {
  from { opacity:0; transform: translateY(30px); }
  to   { opacity:1; transform: translateY(0); }
}
.hero h1 {
  font-family: 'Playfair Display', serif;
  font-size: 3.2rem !important;
  color: #fefae0 !important;
  margin: 0 0 0.3rem !important;
  text-shadow: 0 4px 20px rgba(0,0,0,0.4);
  letter-spacing: 1px;
}
.hero p {
  color: #b7e4c7;
  font-size: 1.1rem;
  margin: 0;
  font-weight: 300;
  letter-spacing: 0.5px;
}

/* ── Section Cards ── */
.farm-card {
  background: rgba(254,250,224,0.85);
  backdrop-filter: blur(12px);
  border: 1.5px solid rgba(82,183,136,0.3);
  border-radius: 20px;
  padding: 1.8rem 2rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 8px 32px rgba(45,106,79,0.10);
  transition: transform 0.3s, box-shadow 0.3s;
  animation: fadeSlide 0.6s ease both;
}
.farm-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 48px rgba(45,106,79,0.18);
}
@keyframes fadeSlide {
  from { opacity:0; transform: translateY(20px); }
  to   { opacity:1; transform: translateY(0); }
}
.farm-card h3 {
  font-family: 'Playfair Display', serif !important;
  color: #2d6a4f !important;
  font-size: 1.3rem;
  margin-bottom: 0.8rem;
}

/* ── Feature grid for Home ── */
.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin: 1rem 0;
}
.feature-item {
  background: rgba(82,183,136,0.1);
  border: 1.5px solid rgba(82,183,136,0.25);
  border-radius: 16px;
  padding: 1.2rem;
  text-align: center;
  font-family: 'Lato', sans-serif;
  color: #3e2005;
  transition: all 0.3s;
}
.feature-item:hover {
  background: rgba(82,183,136,0.2);
  transform: translateY(-3px);
}
.feature-item .icon { font-size: 2rem; margin-bottom: 0.5rem; }
.feature-item .label { font-weight: 700; font-size: 0.9rem; color: #2d6a4f; }

/* ── Selectbox ── */
.stSelectbox > div > div {
  background: rgba(45,106,79,0.12) !important;
  border: 1.5px solid #52b788 !important;
  border-radius: 12px !important;
  color: #2d6a4f !important;
}

/* ── File Uploader ── */
.stFileUploader > div {
  border: 2.5px dashed #52b788 !important;
  border-radius: 16px !important;
  background: rgba(82,183,136,0.06) !important;
  transition: background 0.3s;
}
.stFileUploader > div:hover { background: rgba(82,183,136,0.12) !important; }

/* ── Text Input ── */
.stTextInput > div > div > input {
  border: 1.5px solid #52b788 !important;
  border-radius: 12px !important;
  background: rgba(254,250,224,0.7) !important;
  color: #3e2005;
  padding: 0.6rem 1rem !important;
  box-shadow: inset 0 2px 6px rgba(0,0,0,0.04);
}
.stTextInput > div > div > input:focus {
  box-shadow: 0 0 0 3px rgba(82,183,136,0.3) !important;
}

/* ── Buttons ── */
.stButton > button {
  background: linear-gradient(135deg, #2d6a4f, #52b788) !important;
  color: #fefae0 !important;
  border: none !important;
  border-radius: 14px !important;
  padding: 0.7rem 2rem !important;
  font-family: 'Playfair Display', serif !important;
  font-size: 1.05rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.5px;
  box-shadow: 0 6px 20px rgba(45,106,79,0.35) !important;
  transition: all 0.25s ease !important;
  position: relative;
  overflow: hidden;
}
.stButton > button::before {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.18) 0%, transparent 60%);
  pointer-events: none;
}
.stButton > button:hover {
  transform: translateY(-2px) scale(1.02) !important;
  box-shadow: 0 10px 30px rgba(45,106,79,0.45) !important;
}
.stButton > button:active { transform: translateY(0) scale(0.98) !important; }

/* ── Metrics ── */
[data-testid="metric-container"] {
  background: linear-gradient(135deg, rgba(255,255,255,0.7), rgba(216,243,220,0.5)) !important;
  border: 1.5px solid rgba(82,183,136,0.4) !important;
  border-radius: 16px !important;
  padding: 1.2rem 1.5rem !important;
  text-align: center;
  box-shadow: 0 4px 16px rgba(45,106,79,0.08);
  transition: transform 0.25s;
}
[data-testid="metric-container"]:hover { transform: scale(1.03); }
[data-testid="metric-container"] label {
  color: #5c3317 !important;
  font-weight: 700 !important;
  font-size: 0.85rem !important;
}
[data-testid="metric-container"] [data-testid="metric-value"] {
  color: #2d6a4f !important;
  font-family: 'Playfair Display', serif !important;
  font-size: 1.6rem !important;
}

/* ── Alerts ── */
.stAlert {
  border-radius: 14px !important;
  border-left: 5px solid #52b788 !important;
}

/* ── Divider ── */
hr { border-color: rgba(82,183,136,0.25) !important; margin: 1.5rem 0 !important; }

/* ── Spinner ── */
.stSpinner > div { border-color: #52b788 !important; }

/* ── Weather strip ── */
.weather-strip {
  display: flex;
  gap: 1.2rem;
  flex-wrap: wrap;
  background: linear-gradient(90deg, rgba(45,106,79,0.12), rgba(82,183,136,0.08));
  border-radius: 14px;
  padding: 1rem 1.5rem;
  border: 1px solid rgba(82,183,136,0.3);
  font-size: 1.05rem;
  color: #3e2005;
  font-weight: 600;
}
.weather-strip span { display: flex; align-items: center; gap: 0.4rem; }

/* ── Tip item ── */
.tip-item {
  display: flex;
  align-items: flex-start;
  gap: 0.8rem;
  padding: 0.75rem 1rem;
  background: rgba(82,183,136,0.10);
  border-radius: 12px;
  margin-bottom: 0.6rem;
  border-left: 4px solid #52b788;
  color: #3e2005;
  animation: fadeSlide 0.4s ease both;
}

/* ── Chatbot ── */
.chat-bubble-user {
  background: linear-gradient(135deg, #2d6a4f, #40916c);
  color: #fefae0;
  border-radius: 20px 20px 4px 20px;
  padding: 0.9rem 1.3rem;
  max-width: 75%;
  margin-left: auto;
  margin-bottom: 0.8rem;
  font-size: 0.97rem;
  box-shadow: 0 4px 14px rgba(45,106,79,0.25);
  animation: popIn 0.3s cubic-bezier(0.22,1,0.36,1) both;
}
.chat-bubble-bot {
  background: rgba(254,250,224,0.92);
  color: #3e2005;
  border: 1.5px solid rgba(82,183,136,0.35);
  border-radius: 20px 20px 20px 4px;
  padding: 0.9rem 1.3rem;
  max-width: 80%;
  margin-bottom: 0.8rem;
  font-size: 0.97rem;
  box-shadow: 0 4px 14px rgba(0,0,0,0.07);
  animation: popIn 0.3s cubic-bezier(0.22,1,0.36,1) both;
}
.chat-label {
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 0.25rem;
  opacity: 0.65;
}
@keyframes popIn {
  from { opacity:0; transform: scale(0.92); }
  to   { opacity:1; transform: scale(1); }
}
.chat-container {
  background: linear-gradient(180deg, rgba(216,243,220,0.5), rgba(254,250,224,0.5));
  border: 1.5px solid rgba(82,183,136,0.3);
  border-radius: 20px;
  padding: 1.5rem;
  min-height: 200px;
  max-height: 420px;
  overflow-y: auto;
}

/* ── Section headers ── */
.section-header {
  font-family: 'Playfair Display', serif;
  color: #2d6a4f;
  font-size: 1.5rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding-bottom: 0.4rem;
  border-bottom: 2px solid rgba(82,183,136,0.3);
}

/* ── Ground decoration ── */
.ground-deco {
  text-align: center;
  font-size: 2rem;
  letter-spacing: 6px;
  opacity: 0.18;
  margin-top: 2rem;
  animation: swayLeaf 8s ease-in-out infinite alternate;
}

/* ── Severity badges ── */
.badge {
  display: inline-block;
  padding: 0.3rem 1rem;
  border-radius: 999px;
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}
.badge-low    { background:#b7e4c7; color:#1b4332; }
.badge-medium { background:#f4d47a; color:#7c4d00; }
.badge-high   { background:#ffb4b4; color:#7c0000; }

/* ── Profile avatar ── */
.profile-avatar {
  width: 70px; height: 70px;
  border-radius: 50%;
  background: linear-gradient(135deg, #52b788, #2d6a4f);
  display: flex; align-items: center; justify-content: center;
  font-size: 2rem;
  margin: 0 auto 0.5rem;
  border: 3px solid rgba(82,183,136,0.5);
  box-shadow: 0 4px 16px rgba(45,106,79,0.3);
}
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ──────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"
if "result" not in st.session_state:
    st.session_state.result = None
if "username" not in st.session_state:
    st.session_state.username = "Farmer"
if "language" not in st.session_state:
    st.session_state.language = "English"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "profile_emoji" not in st.session_state:
    st.session_state.profile_emoji = "👨‍🌾"

# ─── TRANSLATIONS ───────────────────────────────────────────────────────────────
translations = {
    "English": {
        "title":           "Smart Crop Disease Detection & Advisory",
        "upload":          "📷 Upload Crop / Leaf Image",
        "city":            "📍 Your City",
        "analyze":         "Analyze Now",
        "report":          "Analysis Report",
        "recommendations": "Recommendations",
        "chat":            "Ask your farming question…",
        "weather":         "Weather Conditions",
        "settings_saved":  "✅ Settings saved!",
        "no_result":       "No analysis yet. Please go to Analyze first.",
        "no_image":        "🌱 Please upload a crop or leaf image first.",
    },
    "தமிழ்": {
        "title":           "ஸ்மார்ட் பயிர் நோய் கண்டறிதல் & ஆலோசனை",
        "upload":          "📷 பயிர் / இலை படம் பதிவேற்றவும்",
        "city":            "📍 உங்கள் நகரம்",
        "analyze":         "இப்போது பகுப்பாய்வு செய்",
        "report":          "பகுப்பாய்வு அறிக்கை",
        "recommendations": "பரிந்துரைகள்",
        "chat":            "உங்கள் விவசாய கேள்வியை கேளுங்கள்…",
        "weather":         "வானிலை நிலைகள்",
        "settings_saved":  "✅ அமைப்புகள் சேமிக்கப்பட்டன!",
        "no_result":       "பகுப்பாய்வு இல்லை. முதலில் பகுப்பாய்வுக்கு செல்லவும்.",
        "no_image":        "🌱 முதலில் ஒரு படத்தை பதிவேற்றவும்.",
    },
}

# ─── MOCK AI FUNCTIONS ──────────────────────────────────────────────────────────
def predict_image(path):
    return "Leaf Blight", 0.87

def get_weather(city):
    return 32, 78, 12, 0.42

def get_climate_risk(temp, hum, rain, soil):
    return 0.63

def fusion_decision(disease, conf, risk):
    return "Medium", "⚠️ Moderate risk detected. Immediate action advised to prevent spread."

def get_recommendations(disease, severity, risk):
    return [
        "Apply copper-based fungicide every 7 days.",
        "Ensure proper drainage around the crop bed.",
        "Remove and destroy infected leaves promptly.",
        "Maintain plant spacing for good air circulation.",
        "Monitor soil moisture — avoid overwatering.",
    ]

def ask_farmer_bot(question, disease="unknown", weather_ctx=""):
    return (
        f"Based on the detected {disease} and current weather ({weather_ctx}), "
        "I recommend increasing fungicide frequency and checking for waterlogging near roots. "
        "Also consider applying neem oil as an organic alternative. "
        "Would you like more details on dosage or application timing?"
    )

# ─── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:1rem 0 0.5rem;">
      <div class="profile-avatar">{st.session_state.profile_emoji}</div>
      <div style="font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:#d8f3dc;">
        {st.session_state.username}
      </div>
      <div style="font-size:0.75rem;color:#95d5b2;margin-top:0.2rem;">AgroVisionNet Member</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    menu = st.radio(
        "Navigation",
        ["🏠 Home", "🔬 Analyze", "📊 Results", "🤖 Chatbot", "⚙️ Settings"],
        index=["🏠 Home", "🔬 Analyze", "📊 Results", "🤖 Chatbot", "⚙️ Settings"].index(
            st.session_state.page
        ) if st.session_state.page in ["🏠 Home", "🔬 Analyze", "📊 Results", "🤖 Chatbot", "⚙️ Settings"] else 0,
        label_visibility="collapsed",
    )
    st.session_state.page = menu

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;font-size:0.72rem;color:#95d5b2;opacity:0.7;padding-bottom:1rem;">
      AgroVisionNet v1.0<br>Empowering Farmers with AI
    </div>
    """, unsafe_allow_html=True)

# ─── Get current language translations ─────────────────────────────────────────
t = translations[st.session_state.language]

# ─── HERO (shown on all pages) ──────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <h1>🌾 AgroVisionNet</h1>
  <p>{t["title"]} · from field to forecast</p>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# 🏠 HOME PAGE
# ════════════════════════════════════════════════════════════════
if menu == "🏠 Home":

    st.markdown('<div class="farm-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">🌱 About AgroVisionNet</p>', unsafe_allow_html=True)
    st.markdown("""
    <p style="font-family:'Lato',sans-serif;font-size:1.05rem;color:#3e2005;line-height:1.8;">
      <b>AgroVisionNet</b> is an AI-powered crop health monitoring platform designed to help farmers
      detect plant diseases early, understand climate risks, and get actionable treatment advice —
      all from a single photo of their crop.
    </p>
    <p style="font-family:'Lato',sans-serif;font-size:1.05rem;color:#3e2005;line-height:1.8;">
      By combining <b>computer vision</b>, <b>weather intelligence</b>, and a <b>farming AI chatbot</b>,
      AgroVisionNet gives every farmer access to expert-level crop care recommendations in seconds.
    </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="farm-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">⚡ Key Features</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="feature-grid">
      <div class="feature-item"><div class="icon">🦠</div><div class="label">Disease Detection</div><div style="font-size:0.82rem;margin-top:0.3rem;color:#5c3317;">AI-powered image analysis identifies 50+ crop diseases</div></div>
      <div class="feature-item"><div class="icon">🌦️</div><div class="label">Climate Risk</div><div style="font-size:0.82rem;margin-top:0.3rem;color:#5c3317;">Real-time weather data fused with disease risk scoring</div></div>
      <div class="feature-item"><div class="icon">💡</div><div class="label">Smart Advice</div><div style="font-size:0.82rem;margin-top:0.3rem;color:#5c3317;">Personalized treatment recommendations instantly</div></div>
      <div class="feature-item"><div class="icon">🤖</div><div class="label">AI Chatbot</div><div style="font-size:0.82rem;margin-top:0.3rem;color:#5c3317;">Ask any farming question in natural language</div></div>
      <div class="feature-item"><div class="icon">🌍</div><div class="label">Multi-Language</div><div style="font-size:0.82rem;margin-top:0.3rem;color:#5c3317;">Available in English and Tamil</div></div>
      <div class="feature-item"><div class="icon">📊</div><div class="label">Detailed Reports</div><div style="font-size:0.82rem;margin-top:0.3rem;color:#5c3317;">Comprehensive crop health dashboard</div></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="farm-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">🌍 Benefits for Farmers</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="tip-item">🌾 Prevent crop loss before it happens</div>
        <div class="tip-item">🧪 Reduce unnecessary pesticide misuse</div>
        <div class="tip-item">📈 Improve seasonal yield significantly</div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="tip-item">🌱 Support sustainable smart farming</div>
        <div class="tip-item">⚡ Get instant expert-level guidance</div>
        <div class="tip-item">🌦️ Plan based on climate forecasts</div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;padding:1.5rem;">
      <p style="font-family:'Playfair Display',serif;font-size:1.2rem;color:#2d6a4f;font-style:italic;">
        👉 Navigate to <b>Analyze</b> in the sidebar to get started!
      </p>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# 🔬 ANALYZE PAGE
# ════════════════════════════════════════════════════════════════
elif menu == "🔬 Analyze":

    st.markdown('<p class="section-header">🔬 Analyze Crop Health</p>', unsafe_allow_html=True)

    st.markdown('<div class="farm-card">', unsafe_allow_html=True)
    upload_col, city_col = st.columns([3, 1])
    with upload_col:
        uploaded = st.file_uploader(t["upload"], type=["jpg", "jpeg", "png"])
    with city_col:
        city = st.text_input("City", "Chennai", placeholder=t["city"])
    st.markdown('</div>', unsafe_allow_html=True)

    _, btn_col, _ = st.columns([2, 1, 2])
    with btn_col:
        analyze = st.button("🌿 " + t["analyze"], use_container_width=True)

    if analyze:
        if not uploaded:
            st.warning(t["no_image"])
        else:
            image = Image.open(uploaded)

            with st.spinner("🔬 Scanning crop health patterns…"):
                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                    tmp_path = tmp.name
                    image.save(tmp_path)

                disease, conf      = predict_image(tmp_path)
                temp, hum, rain, soil = get_weather(city)
                risk               = get_climate_risk(temp, hum, rain, soil)
                severity, decision = fusion_decision(disease, conf, risk)
                tips               = get_recommendations(disease, severity, risk)

                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

            # Store in session state
            st.session_state.result = {
                "image":      image,
                "disease":    disease,
                "confidence": conf,
                "temp":       temp,
                "humidity":   hum,
                "rain":       rain,
                "soil":       soil,
                "risk":       risk,
                "severity":   severity,
                "decision":   decision,
                "tips":       tips,
                "city":       city,
            }

            # Reset chatbot for new analysis
            st.session_state.chat_history = []

            st.balloons()
            st.success("✅ Analysis completed! Navigate to **Results** to view the full report.")

# ════════════════════════════════════════════════════════════════
# 📊 RESULTS PAGE
# ════════════════════════════════════════════════════════════════
elif menu == "📊 Results":

    st.markdown('<p class="section-header">📊 Crop Health Report</p>', unsafe_allow_html=True)

    result = st.session_state.result

    if not result:
        st.warning(t["no_result"])
    else:
        # ── Image + Summary ──
        st.markdown('<div class="farm-card">', unsafe_allow_html=True)
        prev_c, info_c = st.columns([1, 2])
        with prev_c:
            st.image(result["image"], use_container_width=True, caption="Analyzed Crop Image")
        with info_c:
            st.markdown(f'<p class="section-header">🌿 {t["report"]}</p>', unsafe_allow_html=True)
            badge_cls = (
                "badge-low"    if result["severity"] == "Low"  else
                "badge-high"   if result["severity"] == "High" else
                "badge-medium"
            )
            st.markdown(
                f'<span class="badge {badge_cls}">Severity: {result["severity"]}</span>',
                unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)
            m1, m2, m3 = st.columns(3)
            m1.metric("🦠 Disease",      result["disease"])
            m2.metric("🎯 Confidence",   f"{result['confidence']*100:.1f}%")
            m3.metric("⚠️ Climate Risk", f"{result['risk']*100:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Decision banner ──
        st.info(result["decision"])

        # ── Weather ──
        st.markdown('<div class="farm-card">', unsafe_allow_html=True)
        st.markdown(f'<p class="section-header">🌦 {t["weather"]}</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="weather-strip">
          <span>🌡️ <span>{result['temp']}°C</span></span>
          <span>💧 <span>Humidity {result['humidity']}%</span></span>
          <span>🌧️ <span>Rainfall {result['rain']} mm</span></span>
          <span>🌱 <span>Soil Moisture {result['soil']*100:.0f}%</span></span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Recommendations ──
        st.markdown('<div class="farm-card">', unsafe_allow_html=True)
        st.markdown(f'<p class="section-header">🌱 {t["recommendations"]}</p>', unsafe_allow_html=True)
        for tip in result["tips"]:
            st.markdown(f'<div class="tip-item">✅ {tip}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# 🤖 CHATBOT PAGE
# ════════════════════════════════════════════════════════════════
elif menu == "🤖 Chatbot":

    st.markdown('<p class="section-header">🤖 AI Farmer Assistant</p>', unsafe_allow_html=True)

    # Welcome message if empty
    if not st.session_state.chat_history:
        result = st.session_state.result
        if result:
            welcome = (
                f"🌾 Namaste! I've analyzed your crop. "
                f"I detected <b>{result['disease']}</b> with {result['confidence']*100:.0f}% confidence. "
                "Feel free to ask me anything about treatment, prevention, or farming tips!"
            )
        else:
            welcome = (
                "🌾 Namaste! I'm AgroBot, your AI farming assistant. "
                "You can ask me anything about crop diseases, treatments, soil care, or farming best practices!"
            )
        st.session_state.chat_history.append({"role": "bot", "text": welcome})

    # ── Render chat ──
    st.markdown('<div class="farm-card">', unsafe_allow_html=True)
    chat_html = '<div class="chat-container">'
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            chat_html += f"""
            <div style="display:flex;justify-content:flex-end">
              <div>
                <div class="chat-label" style="text-align:right;color:#2d6a4f">You</div>
                <div class="chat-bubble-user">{msg["text"]}</div>
              </div>
            </div>"""
        else:
            chat_html += f"""
            <div>
              <div class="chat-label" style="color:#5c3317">🌾 AgroBot</div>
              <div class="chat-bubble-bot">{msg["text"]}</div>
            </div>"""
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # ── Input ──
    q_col, ask_col = st.columns([4, 1])
    with q_col:
        question = st.text_input(
            "Ask",
            placeholder=t["chat"],
            key="chat_input",
            label_visibility="collapsed",
        )
    with ask_col:
        send = st.button("🌿 Ask", use_container_width=True, key="send_btn")

    if send and question.strip():
        st.session_state.chat_history.append({"role": "user", "text": question})
        result = st.session_state.result
        disease     = result["disease"] if result else "unknown"
        weather_ctx = f"{result['temp']}°C & humidity {result['humidity']}%" if result else "unknown"
        with st.spinner("🌱 Thinking…"):
            reply = ask_farmer_bot(question, disease, weather_ctx)
        st.session_state.chat_history.append({"role": "bot", "text": reply})
        st.rerun()

    if st.button("🗑️ Clear Chat", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# ⚙️ SETTINGS PAGE
# ════════════════════════════════════════════════════════════════
elif menu == "⚙️ Settings":

    st.markdown('<p class="section-header">⚙️ Settings</p>', unsafe_allow_html=True)

    # ── Profile ──
    st.markdown('<div class="farm-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">👤 Profile</p>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center;margin-bottom:1rem;">
      <div class="profile-avatar" style="margin:0 auto 0.5rem;">{st.session_state.profile_emoji}</div>
      <div style="font-family:'Playfair Display',serif;color:#2d6a4f;font-size:1.2rem;">{st.session_state.username}</div>
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input("Display Name", st.session_state.username)

    st.markdown("**Choose Profile Avatar**")
    avatars = ["👨‍🌾", "👩‍🌾", "🧑‍🌾", "🌾", "🌱", "🌻"]
    avatar_cols = st.columns(len(avatars))
    for i, emoji in enumerate(avatars):
        with avatar_cols[i]:
            if st.button(emoji, key=f"avatar_{i}"):
                st.session_state.profile_emoji = emoji
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Language ──
    st.markdown('<div class="farm-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">🌐 Language</p>', unsafe_allow_html=True)
    language = st.selectbox(
        "Language",
        ["English", "தமிழ்"],
        index=["English", "தமிழ்"].index(st.session_state.language),
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── App Info ──
    st.markdown('<div class="farm-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">ℹ️ App Information</p>', unsafe_allow_html=True)
    st.markdown("""
    <table style="width:100%;font-family:'Lato',sans-serif;color:#3e2005;font-size:0.95rem;">
      <tr><td style="padding:0.4rem 0;font-weight:700;">Version</td><td>AgroVisionNet v1.0</td></tr>
      <tr><td style="padding:0.4rem 0;font-weight:700;">Model</td><td>CNN + Fusion Decision Engine</td></tr>
      <tr><td style="padding:0.4rem 0;font-weight:700;">Weather API</td><td>OpenWeatherMap (mocked)</td></tr>
      <tr><td style="padding:0.4rem 0;font-weight:700;">Languages</td><td>English, Tamil</td></tr>
    </table>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Save ──
    _, save_col, _ = st.columns([2, 1, 2])
    with save_col:
        if st.button("💾 Save Settings", use_container_width=True):
            st.session_state.username = name
            st.session_state.language = language
            st.success(t["settings_saved"])
            st.rerun()

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ground-deco">🌾 🌿 🌻 🌱 🪴 🌻 🌿 🌾</div>
<p style="text-align:center;color:#5c3317;opacity:0.4;font-size:0.78rem;margin-top:0.5rem;font-family:'Lato',sans-serif;">
  AgroVisionNet · Empowering Farmers with AI
</p>
""", unsafe_allow_html=True)
