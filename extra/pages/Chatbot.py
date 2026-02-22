import streamlit as st

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="AgroBot · AgroVisionNet", layout="wide", page_icon="🤖")

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,800;1,600&family=Lato:wght@300;400;700&display=swap');

.stApp {
  background:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100%25' height='100%25'%3E%3Cdefs%3E%3CradialGradient id='g' cx='20%25' cy='10%25' r='50%25'%3E%3Cstop offset='0%25' stop-color='%23d8f3dc' stop-opacity='0.9'/%3E%3Cstop offset='100%25' stop-color='transparent'/%3E%3C/radialGradient%3E%3C/defs%3E%3Crect fill='url(%23g)' width='100%25' height='100%25'/%3E%3C/svg%3E"),
    linear-gradient(160deg, #1b4332 0%, #2d6a4f 30%, #fefae0 100%);
  font-family: 'Lato', sans-serif;
}

/* Pollen animation */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    radial-gradient(1.5px 1.5px at 15% 25%, #b7e4c755 0%, transparent 100%),
    radial-gradient(1px 1px at 45% 70%, #e9c46a44 0%, transparent 100%),
    radial-gradient(2px 2px at 70% 30%, #52b78833 0%, transparent 100%),
    radial-gradient(1px 1px at 85% 65%, #b7e4c733 0%, transparent 100%);
  pointer-events: none;
  animation: floatPollen 20s ease-in-out infinite alternate;
}
@keyframes floatPollen {
  from { transform: translateY(0); opacity: 0.5; }
  to   { transform: translateY(-25px) rotate(6deg); opacity: 0.9; }
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1rem 2rem 3rem; max-width: 900px; margin: 0 auto; }

/* ── Back button ── */
.back-btn-wrap { margin-bottom: 1.2rem; }
.stButton > button {
  background: rgba(254,250,224,0.2) !important;
  color: #fefae0 !important;
  border: 1.5px solid rgba(254,250,224,0.4) !important;
  border-radius: 12px !important;
  padding: 0.5rem 1.4rem !important;
  font-family: 'Lato', sans-serif !important;
  font-size: 0.9rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.3px;
  transition: all 0.2s ease !important;
  backdrop-filter: blur(8px);
}
.stButton > button:hover {
  background: rgba(254,250,224,0.35) !important;
  transform: translateX(-3px) !important;
}

/* ── Chat hero ── */
.chat-hero {
  text-align: center;
  padding: 2.2rem 1rem 1.5rem;
  animation: riseUp 0.7s cubic-bezier(0.22,1,0.36,1) both;
}
@keyframes riseUp {
  from { opacity:0; transform: translateY(24px); }
  to   { opacity:1; transform: translateY(0); }
}
.chat-hero .bot-avatar {
  font-size: 4.5rem;
  display: block;
  margin-bottom: 0.5rem;
  animation: botBounce 3s ease-in-out infinite;
}
@keyframes botBounce {
  0%,100% { transform: translateY(0) rotate(0deg); }
  40%     { transform: translateY(-10px) rotate(-5deg); }
  60%     { transform: translateY(-6px) rotate(3deg); }
}
.chat-hero h1 {
  font-family: 'Playfair Display', serif;
  color: #fefae0 !important;
  font-size: 2.4rem !important;
  margin: 0 0 0.4rem !important;
  text-shadow: 0 4px 16px rgba(0,0,0,0.4);
}
.chat-hero p {
  color: #b7e4c7;
  font-size: 1rem;
  margin: 0;
  font-weight: 300;
}

/* ── Context pill ── */
.context-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(82,183,136,0.22);
  border: 1px solid rgba(82,183,136,0.5);
  border-radius: 999px;
  padding: 0.35rem 1rem;
  font-size: 0.82rem;
  color: #d8f3dc;
  font-weight: 600;
  letter-spacing: 0.3px;
  margin: 0 0.3rem 0.6rem;
  backdrop-filter: blur(6px);
}
.context-bar {
  text-align: center;
  margin-bottom: 1.5rem;
  animation: riseUp 0.9s ease both;
}

/* ── Chat window ── */
.chat-window {
  background: rgba(254,250,224,0.12);
  backdrop-filter: blur(18px);
  border: 1.5px solid rgba(254,250,224,0.2);
  border-radius: 24px;
  padding: 1.5rem 1.5rem 1rem;
  min-height: 340px;
  max-height: 480px;
  overflow-y: auto;
  margin-bottom: 1rem;
  scroll-behavior: smooth;
  box-shadow: inset 0 2px 20px rgba(0,0,0,0.1), 0 8px 32px rgba(0,0,0,0.2);
}
.chat-window::-webkit-scrollbar { width: 4px; }
.chat-window::-webkit-scrollbar-track { background: transparent; }
.chat-window::-webkit-scrollbar-thumb { background: rgba(82,183,136,0.4); border-radius: 4px; }

/* ── Chat bubbles ── */
.bubble-row-user {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
  animation: slideRight 0.35s cubic-bezier(0.22,1,0.36,1) both;
}
.bubble-row-bot {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 1rem;
  animation: slideLeft 0.35s cubic-bezier(0.22,1,0.36,1) both;
}
@keyframes slideRight {
  from { opacity:0; transform: translateX(20px); }
  to   { opacity:1; transform: translateX(0); }
}
@keyframes slideLeft {
  from { opacity:0; transform: translateX(-20px); }
  to   { opacity:1; transform: translateX(0); }
}

.bubble-user {
  background: linear-gradient(135deg, #2d6a4f, #40916c);
  color: #fefae0;
  border-radius: 22px 22px 5px 22px;
  padding: 0.85rem 1.2rem;
  max-width: 72%;
  font-size: 0.95rem;
  line-height: 1.5;
  box-shadow: 0 6px 20px rgba(45,106,79,0.4);
}
.bubble-bot {
  background: rgba(254,250,224,0.9);
  color: #3e2005;
  border: 1.5px solid rgba(82,183,136,0.3);
  border-radius: 22px 22px 22px 5px;
  padding: 0.85rem 1.2rem;
  max-width: 78%;
  font-size: 0.95rem;
  line-height: 1.5;
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}
.bubble-label {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 0.3rem;
  opacity: 0.6;
}
.bubble-label-user { text-align: right; color: #b7e4c7; }
.bubble-label-bot  { color: #5c3317; }

.bot-icon {
  width: 36px; height: 36px;
  background: linear-gradient(135deg, #2d6a4f, #52b788);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem;
  margin-right: 0.6rem;
  flex-shrink: 0;
  box-shadow: 0 3px 10px rgba(45,106,79,0.4);
}

/* ── Input bar ── */
.input-bar {
  background: rgba(254,250,224,0.15);
  backdrop-filter: blur(16px);
  border: 1.5px solid rgba(254,250,224,0.25);
  border-radius: 20px;
  padding: 1rem 1.2rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}
.stTextInput > div > div > input {
  background: rgba(254,250,224,0.85) !important;
  border: 1.5px solid rgba(82,183,136,0.5) !important;
  border-radius: 14px !important;
  color: #3e2005 !important;
  font-family: 'Lato', sans-serif;
  font-size: 0.97rem;
  padding: 0.75rem 1.1rem !important;
}
.stTextInput > div > div > input:focus {
  box-shadow: 0 0 0 3px rgba(82,183,136,0.35) !important;
  border-color: #52b788 !important;
}
.stTextInput > div > div > input::placeholder { color: #5c3317; opacity: 0.5; }

/* Send button — override to wheat/sun color for contrast */
.stButton > button[kind="primary"],
div[data-testid="stHorizontalBlock"] .stButton > button {
  background: linear-gradient(135deg, #e9c46a, #f4a261) !important;
  color: #3e2005 !important;
  border: none !important;
  border-radius: 14px !important;
  font-family: 'Playfair Display', serif !important;
  font-weight: 700 !important;
  font-size: 1rem !important;
  padding: 0.75rem 1.5rem !important;
  box-shadow: 0 6px 20px rgba(244,162,97,0.45) !important;
}
div[data-testid="stHorizontalBlock"] .stButton > button:hover {
  transform: scale(1.05) !important;
  box-shadow: 0 10px 28px rgba(244,162,97,0.55) !important;
}

/* ── Typing indicator ── */
.typing-dot {
  display: inline-block;
  width: 8px; height: 8px;
  border-radius: 50%;
  background: #52b788;
  margin: 0 2px;
  animation: typingBounce 1.2s ease-in-out infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes typingBounce {
  0%,80%,100% { transform: translateY(0); }
  40%         { transform: translateY(-8px); }
}

/* ── Suggestion chips ── */
.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
.chip {
  background: rgba(82,183,136,0.18);
  border: 1px solid rgba(82,183,136,0.45);
  color: #d8f3dc;
  border-radius: 999px;
  padding: 0.35rem 0.9rem;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'Lato', sans-serif;
}
.chip:hover {
  background: rgba(82,183,136,0.35);
  transform: scale(1.04);
}

/* ── Footer ── */
.chat-footer {
  text-align: center;
  color: rgba(254,250,224,0.3);
  font-size: 0.72rem;
  margin-top: 1.5rem;
  font-family: 'Lato', sans-serif;
  letter-spacing: 0.5px;
}
</style>
""", unsafe_allow_html=True)

# ─── Mock bot function (replace with your real ask_farmer_bot) ───────────────
def ask_farmer_bot(question, disease, weather_ctx):
    return (
        f"Based on the detected {disease} and current weather ({weather_ctx}), "
        "I recommend increasing fungicide frequency and checking for waterlogging near roots. "
        "Also consider applying neem oil as an organic alternative. "
        "Would you like more details on dosage or application timing?"
    )

# ─── Pull context from session state (set by main app after analysis) ─────────
disease  = st.session_state.get("last_disease",  "Unknown")
conf     = st.session_state.get("last_conf",     0.0)
temp     = st.session_state.get("last_temp",     "--")
hum      = st.session_state.get("last_hum",      "--")
rain     = st.session_state.get("last_rain",     "--")
severity = st.session_state.get("last_severity", "--")
has_ctx  = st.session_state.get("analysis_done", False)

# ─── Back button ─────────────────────────────────────────────────────────────
st.markdown('<div class="back-btn-wrap">', unsafe_allow_html=True)
if st.button("← Back to Analysis"):
    st.switch_page("app.py")
st.markdown('</div>', unsafe_allow_html=True)

# ─── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="chat-hero">
  <span class="bot-avatar">🤖</span>
  <h1>AI Farmer Assistant</h1>
  <p>Your personal agronomist · Powered by AgroVisionNet AI</p>
</div>
""", unsafe_allow_html=True)

# ─── Context pills ───────────────────────────────────────────────────────────
if has_ctx:
    st.markdown(f"""
    <div class="context-bar">
      <span class="context-pill">🦠 {disease}</span>
      <span class="context-pill">🎯 {conf*100:.0f}% conf</span>
      <span class="context-pill">🌡️ {temp}°C · 💧 {hum}%</span>
      <span class="context-pill">⚠️ Severity: {severity}</span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="context-bar">
      <span class="context-pill">💡 Run an analysis first for crop-specific advice</span>
    </div>
    """, unsafe_allow_html=True)

# ─── Chat history init ───────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Auto-welcome message
if not st.session_state.chat_history:
    if has_ctx:
        welcome = (
            f"🌾 Namaste! I've reviewed your crop analysis — I detected <b>{disease}</b> "
            f"with <b>{conf*100:.0f}% confidence</b>. Current weather shows {temp}°C with {hum}% humidity. "
            f"Ask me anything about treatment, prevention schedules, or organic alternatives!"
        )
    else:
        welcome = (
            "🌾 Namaste! I'm AgroBot, your AI farming assistant. "
            "I can help with crop diseases, fertilizers, weather impacts, and more. "
            "For crop-specific advice, go back and run an analysis first!"
        )
    st.session_state.chat_history.append({"role": "bot", "text": welcome})

# ─── Suggestion chips ────────────────────────────────────────────────────────
suggestions = [
    "What is the best treatment?",
    "Is it safe to harvest?",
    "Organic alternatives?",
    "How to prevent spread?",
    "Fertilizer recommendation",
]
st.markdown('<div class="chip-row">' +
    "".join(f'<span class="chip">{s}</span>' for s in suggestions) +
    '</div>', unsafe_allow_html=True)

# ─── Render chat window ───────────────────────────────────────────────────────
chat_html = '<div class="chat-window" id="chatWin">'
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        chat_html += f"""
        <div class="bubble-row-user">
          <div>
            <div class="bubble-label bubble-label-user">You</div>
            <div class="bubble-user">{msg["text"]}</div>
          </div>
        </div>"""
    else:
        chat_html += f"""
        <div class="bubble-row-bot">
          <div class="bot-icon">🌾</div>
          <div>
            <div class="bubble-label bubble-label-bot">AgroBot</div>
            <div class="bubble-bot">{msg["text"]}</div>
          </div>
        </div>"""
chat_html += '</div>'

# Auto-scroll JS
chat_html += """
<script>
  var win = document.getElementById("chatWin");
  if(win) win.scrollTop = win.scrollHeight;
</script>
"""
st.markdown(chat_html, unsafe_allow_html=True)

# ─── Input bar ────────────────────────────────────────────────────────────────
st.markdown('<div class="input-bar">', unsafe_allow_html=True)
q_col, send_col = st.columns([5, 1])
with q_col:
    question = st.text_input(
        "question",
        placeholder="🌱 Ask about your crop, disease, fertilizer…",
        key="chat_q",
        label_visibility="collapsed"
    )
with send_col:
    send = st.button("Send 🌿", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── Handle send ─────────────────────────────────────────────────────────────
if send and question.strip():
    st.session_state.chat_history.append({"role": "user", "text": question})
    weather_ctx = f"{temp}°C & humidity {hum}%" if has_ctx else "unknown weather"
    with st.spinner(""):
        st.markdown("""
        <div class="bubble-row-bot">
          <div class="bot-icon">🌾</div>
          <div class="bubble-bot">
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
          </div>
        </div>""", unsafe_allow_html=True)
        reply = ask_farmer_bot(question, disease, weather_ctx)
    st.session_state.chat_history.append({"role": "bot", "text": reply})
    st.rerun()

# ─── Clear chat ───────────────────────────────────────────────────────────────
if st.session_state.chat_history and len(st.session_state.chat_history) > 1:
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="chat-footer">
  🌾 AgroVisionNet · AI Farmer Assistant · Powered by machine learning & agronomy
</div>
""", unsafe_allow_html=True)