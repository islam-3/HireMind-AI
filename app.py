import streamlit as st
try:
    from groq import Groq
except ImportError:
    st.error("Missing 'groq' library.")
    st.stop()

st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600;700&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background-color: #080A0F;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(99,179,237,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 40% 30% at 80% 80%, rgba(56,189,128,0.05) 0%, transparent 50%);
    font-family: 'DM Sans', sans-serif;
    color: #E8E2D9;
}

[data-testid="stAppViewBlockContainer"] {
    padding: 0 !important;
    max-width: 100% !important;
}

[data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

.hero-wrap {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 40px;
    position: relative;
}

.top-bar {
    position: absolute;
    top: 0; left: 0; right: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 28px 48px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}

.top-bar-logo {
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: rgba(232,226,217,0.5);
}

.top-bar-tag {
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(232,226,217,0.3);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 6px 16px;
    border-radius: 20px;
}

.divider-line {
    width: 1px;
    height: 60px;
    background: linear-gradient(to bottom, transparent, rgba(255,255,255,0.15), transparent);
    margin: 0 auto 32px;
}

.eyebrow {
    font-size: 10px;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: rgba(99,179,237,0.7);
    margin-bottom: 20px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
}

.main-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(56px, 8vw, 96px);
    font-weight: 300;
    line-height: 1.0;
    letter-spacing: -1px;
    text-align: center;
    margin-bottom: 8px;
    color: #F5F0E8;
}

.main-title span {
    font-weight: 600;
    font-style: italic;
    background: linear-gradient(135deg, #63B3ED 0%, #68D391 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.tagline {
    font-size: 13px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(232,226,217,0.35);
    text-align: center;
    margin-bottom: 64px;
    font-weight: 300;
}

.cards-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 2px;
    overflow: hidden;
    width: 100%;
    max-width: 920px;
    margin-bottom: 56px;
}

.card {
    background: #0D1018;
    padding: 36px 28px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    transition: background 0.3s;
    position: relative;
    overflow: hidden;
}

.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,179,237,0.4), transparent);
    opacity: 0;
    transition: opacity 0.3s;
}

.card:hover { background: #111520; }
.card:hover::before { opacity: 1; }

.card-num {
    font-size: 10px;
    letter-spacing: 3px;
    color: rgba(99,179,237,0.4);
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
}

.card-icon {
    font-size: 22px;
    line-height: 1;
    margin: 4px 0;
}

.card-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 22px;
    font-weight: 600;
    color: #F5F0E8;
    line-height: 1.1;
}

.card-desc {
    font-size: 12px;
    color: rgba(232,226,217,0.35);
    line-height: 1.6;
    font-weight: 300;
}

.btn-wrap {
    display: flex;
    align-items: center;
    gap: 20px;
}

.cta-btn {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: linear-gradient(135deg, #1a4a2e 0%, #1d5c38 100%);
    border: 1px solid rgba(104,211,145,0.25);
    color: #68D391;
    font-family: 'DM Sans', sans-serif;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 16px 44px;
    border-radius: 1px;
    cursor: pointer;
    transition: all 0.3s;
}

.cta-btn:hover {
    background: linear-gradient(135deg, #1d5c38 0%, #21703f 100%);
    border-color: rgba(104,211,145,0.45);
    box-shadow: 0 0 30px rgba(104,211,145,0.12);
}

.cta-arrow {
    font-size: 14px;
    transition: transform 0.3s;
}

.cta-btn:hover .cta-arrow { transform: translateX(4px); }

.sub-note {
    font-size: 11px;
    letter-spacing: 1.5px;
    color: rgba(232,226,217,0.2);
    text-transform: uppercase;
}

.bottom-bar {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 48px;
    border-top: 1px solid rgba(255,255,255,0.04);
}

.bottom-stat {
    text-align: center;
}

.bottom-stat-num {
    font-family: 'Cormorant Garamond', serif;
    font-size: 22px;
    font-weight: 600;
    color: rgba(232,226,217,0.6);
}

.bottom-stat-label {
    font-size: 9px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(232,226,217,0.2);
    margin-top: 2px;
}

/* Streamlit button override */
div.stButton { display: flex; justify-content: center; }
div.stButton > button {
    background: linear-gradient(135deg, #1a4a2e 0%, #1d5c38 100%) !important;
    border: 1px solid rgba(104,211,145,0.25) !important;
    color: #68D391 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    padding: 16px 56px !important;
    border-radius: 2px !important;
    box-shadow: none !important;
    transition: all 0.3s !important;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #1d5c38 0%, #21703f 100%) !important;
    border-color: rgba(104,211,145,0.45) !important;
    box-shadow: 0 0 30px rgba(104,211,145,0.1) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0A0C12 !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}
[data-testid="stSidebar"] * { color: #E8E2D9 !important; }

.stRadio label { font-size: 13px !important; letter-spacing: 1px !important; }
</style>
""", unsafe_allow_html=True)

if "entered" not in st.session_state:
    st.session_state.entered = False

if not st.session_state.entered:
    st.markdown("""
    <div class="hero-wrap">

        <div class="top-bar">
            <div class="top-bar-logo">CareerMind</div>
            <div class="top-bar-tag">AI-Powered Suite</div>
        </div>

        <div class="divider-line"></div>
        <div class="eyebrow">Professional Intelligence Platform</div>

        <h1 class="main-title">Architect Your<br><span>Career Future</span></h1>
        <p class="tagline">Precision tools for the modern professional</p>

        <div class="cards-row">
            <div class="card">
                <div class="card-num">01</div>
                <div class="card-icon">⬡</div>
                <div class="card-title">Audit</div>
                <div class="card-desc">CV & JD deep alignment analysis</div>
            </div>
            <div class="card">
                <div class="card-num">02</div>
                <div class="card-icon">◈</div>
                <div class="card-title">Script</div>
                <div class="card-desc">Bespoke cover letter generation</div>
            </div>
            <div class="card">
                <div class="card-num">03</div>
                <div class="card-icon">◎</div>
                <div class="card-title">Master</div>
                <div class="card-desc">Live interview simulation</div>
            </div>
            <div class="card">
                <div class="card-num">04</div>
                <div class="card-icon">◆</div>
                <div class="card-title">Value</div>
                <div class="card-desc">Salary intelligence & benchmarks</div>
            </div>
        </div>

        <div style="height:0"></div>

        <div class="bottom-bar">
            <div class="bottom-stat"><div class="bottom-stat-num">4</div><div class="bottom-stat-label">Core Tools</div></div>
            <div class="bottom-stat"><div class="bottom-stat-num">AI</div><div class="bottom-stat-label">Powered</div></div>
            <div class="bottom-stat"><div class="bottom-stat-num">∞</div><div class="bottom-stat-label">Sessions</div></div>
        </div>

    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([2, 1, 2])
    with col:
        if st.button("Enter Suite →", use_container_width=True):
            st.session_state.entered = True
            st.rerun()

else:
    with st.sidebar:
        st.markdown("""
        <div style='padding: 20px 0 10px; text-align:center;'>
            <div style='font-family: Cormorant Garamond, serif; font-size: 22px; font-weight: 600; color: #F5F0E8;'>CareerMind</div>
            <div style='font-size: 9px; letter-spacing: 3px; text-transform: uppercase; color: rgba(232,226,217,0.3); margin-top:4px;'>AI Suite</div>
        </div>
        """, unsafe_allow_html=True)
        page = st.radio("", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if st.button("← Exit"):
            st.session_state.entered = False
            st.rerun()

    st.markdown(f"""
    <div style='padding: 48px 40px;'>
        <div style='font-size:10px; letter-spacing:4px; text-transform:uppercase; color:rgba(99,179,237,0.6); margin-bottom:12px; font-family: DM Sans, sans-serif;'>Active Tool</div>
        <h2 style='font-family: Cormorant Garamond, serif; font-size: 48px; font-weight: 300; color: #F5F0E8; margin-bottom: 8px;'>{page}</h2>
        <div style='width:40px; height:1px; background: linear-gradient(90deg, rgba(99,179,237,0.5), transparent); margin-bottom:32px;'></div>
    </div>
    """, unsafe_allow_html=True)
    st.info(f"Workspace for {page} is ready.")
