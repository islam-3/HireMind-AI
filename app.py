import streamlit as st
try:
    from groq import Groq
except ImportError:
    st.error("Missing 'groq' library.")
    st.stop()

st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Bebas+Neue&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background: #0F0F0F;
    font-family: 'Space Grotesk', sans-serif;
    color: #F0EDE8;
    min-height: 100vh;
}

[data-testid="stAppViewBlockContainer"] { padding: 0 !important; max-width: 100% !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }

.page {
    min-height: 100vh;
    display: grid;
    grid-template-rows: auto 1fr auto;
}

/* ── TOP BAR ── */
.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 22px 48px;
    border-bottom: 1px solid #1E1E1E;
}
.topbar-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 22px;
    letter-spacing: 3px;
    color: #F0EDE8;
}
.topbar-pill {
    background: #1A1A1A;
    border: 1px solid #2A2A2A;
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #888;
}

/* ── HERO ── */
.hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 48px;
    gap: 0;
}

.hero-label {
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #FF5C00;
    margin-bottom: 16px;
}

.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(72px, 11vw, 140px);
    line-height: 0.92;
    text-align: center;
    letter-spacing: 2px;
    margin-bottom: 32px;
}

.hero-title .line1 { color: #F0EDE8; display: block; }
.hero-title .line2 {
    display: block;
    -webkit-text-fill-color: transparent;
    -webkit-text-stroke: 2px #F0EDE8;
    opacity: 0.25;
}
.hero-title .line3 {
    display: block;
    background: linear-gradient(90deg, #FF5C00, #FFB800);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── CARDS ROW ── */
.cards-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0;
    width: 100%;
    max-width: 1000px;
    margin-bottom: 48px;
    border: 1px solid #222;
    border-radius: 4px;
    overflow: hidden;
}

.card {
    padding: 28px 24px 24px;
    border-right: 1px solid #222;
    position: relative;
    transition: background 0.2s;
}
.card:last-child { border-right: none; }
.card:hover { background: #161616; }

.card-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 20px;
}
.card-num {
    font-size: 10px;
    font-weight: 500;
    color: #444;
    letter-spacing: 1px;
}
.card-tag {
    font-size: 9px;
    font-weight: 500;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 3px 8px;
    border-radius: 100px;
}
.tag-orange { background: rgba(255,92,0,0.12); color: #FF5C00; }
.tag-yellow { background: rgba(255,184,0,0.12); color: #FFB800; }
.tag-blue   { background: rgba(88,166,255,0.12); color: #58A6FF; }
.tag-green  { background: rgba(63,185,80,0.12);  color: #3FB950; }

.card-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 32px;
    letter-spacing: 2px;
    color: #F0EDE8;
    margin-bottom: 6px;
    line-height: 1;
}
.card-desc {
    font-size: 11px;
    color: #555;
    font-weight: 400;
    line-height: 1.5;
}

.card-bar {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.bar-orange { background: #FF5C00; }
.bar-yellow { background: #FFB800; }
.bar-blue   { background: #58A6FF; }
.bar-green  { background: #3FB950; }

/* ── BOTTOM BAR ── */
.bottombar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 18px 48px;
    border-top: 1px solid #1E1E1E;
}
.bottombar-copy {
    font-size: 10px;
    color: #333;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.bottombar-stats {
    display: flex;
    gap: 32px;
}
.bstat { text-align: center; }
.bstat-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 20px;
    color: #444;
    letter-spacing: 1px;
}
.bstat-lbl {
    font-size: 8px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #333;
}

/* ── STREAMLIT BUTTON ── */
div.stButton { display: flex; justify-content: center; }
div.stButton > button {
    background: linear-gradient(90deg, #FF5C00, #FFB800) !important;
    border: none !important;
    border-radius: 4px !important;
    color: #0F0F0F !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 18px !important;
    letter-spacing: 3px !important;
    padding: 14px 64px !important;
    box-shadow: 0 0 40px rgba(255,92,0,0.25) !important;
    transition: all 0.2s !important;
}
div.stButton > button:hover {
    box-shadow: 0 0 60px rgba(255,92,0,0.4) !important;
    transform: translateY(-1px) !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #0A0A0A !important;
    border-right: 1px solid #1E1E1E !important;
}
</style>
""", unsafe_allow_html=True)

if "entered" not in st.session_state:
    st.session_state.entered = False

if "GROQ_API_KEY" not in st.secrets:
    st.error("Missing API Key in Secrets.")
    st.stop()

if not st.session_state.entered:
    st.markdown("""
    <div class="page">

        <div class="topbar">
            <div class="topbar-logo">CareerMind</div>
            <div class="topbar-pill">AI Platform — v2.0</div>
        </div>

        <div class="hero">
            <div class="hero-label">● Your Career Intelligence Suite</div>
            <div class="hero-title">
                <span class="line1">Career</span>
                <span class="line2">Mind</span>
                <span class="line3">AI</span>
            </div>

            <div class="cards-row">
                <div class="card">
                    <div class="card-bar bar-orange"></div>
                    <div class="card-top">
                        <span class="card-num">01</span>
                        <span class="card-tag tag-orange">Audit</span>
                    </div>
                    <div class="card-title">CV<br>Match</div>
                    <div class="card-desc">Deep CV & JD alignment analysis</div>
                </div>
                <div class="card">
                    <div class="card-bar bar-yellow"></div>
                    <div class="card-top">
                        <span class="card-num">02</span>
                        <span class="card-tag tag-yellow">Script</span>
                    </div>
                    <div class="card-title">Cover<br>Letter</div>
                    <div class="card-desc">Bespoke cover letter generation</div>
                </div>
                <div class="card">
                    <div class="card-bar bar-blue"></div>
                    <div class="card-top">
                        <span class="card-num">03</span>
                        <span class="card-tag tag-blue">Master</span>
                    </div>
                    <div class="card-title">Interview<br>Prep</div>
                    <div class="card-desc">Live interview simulation</div>
                </div>
                <div class="card">
                    <div class="card-bar bar-green"></div>
                    <div class="card-top">
                        <span class="card-num">04</span>
                        <span class="card-tag tag-green">Value</span>
                    </div>
                    <div class="card-title">Salary<br>Intel</div>
                    <div class="card-desc">Salary intelligence & benchmarks</div>
                </div>
            </div>

        </div>

        <div class="bottombar">
            <div class="bottombar-copy">© 2025 CareerMind AI</div>
            <div class="bottombar-stats">
                <div class="bstat"><div class="bstat-num">4</div><div class="bstat-lbl">Tools</div></div>
                <div class="bstat"><div class="bstat-num">AI</div><div class="bstat-lbl">Powered</div></div>
                <div class="bstat"><div class="bstat-num">∞</div><div class="bstat-lbl">Sessions</div></div>
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([2, 1, 2])
    with col:
        if st.button("ACCESS SUITE", use_container_width=True):
            st.session_state.entered = True
            st.rerun()

else:
    with st.sidebar:
        st.markdown("""
        <div style='padding:24px 0 16px; text-align:center;'>
            <div style='font-family:Bebas Neue,sans-serif; font-size:26px; letter-spacing:3px; color:#F0EDE8;'>CareerMind</div>
            <div style='font-size:9px; letter-spacing:3px; text-transform:uppercase; color:#444; margin-top:4px;'>AI Suite</div>
        </div>
        """, unsafe_allow_html=True)
        page = st.radio("", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        if st.button("← Exit"):
            st.session_state.entered = False
            st.rerun()

    st.markdown(f"""
    <div style='padding:48px 48px 0;'>
        <div style='font-size:10px; letter-spacing:3px; text-transform:uppercase; color:#FF5C00; margin-bottom:8px;'>Active Tool</div>
        <div style='font-family:Bebas Neue,sans-serif; font-size:56px; letter-spacing:2px; color:#F0EDE8; line-height:1; margin-bottom:12px;'>{page}</div>
        <div style='width:48px; height:3px; background:linear-gradient(90deg,#FF5C00,#FFB800); margin-bottom:32px;'></div>
    </div>
    """, unsafe_allow_html=True)
    st.info(f"Workspace for {page} is ready.")
