import streamlit as st
try:
    from groq import Groq
except ImportError:
    st.error("Missing 'groq' library.")
    st.stop()

st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    [data-testid="stAppViewBlockContainer"] {
        padding-top: 2rem !important;
        max-width: 1100px !important;
        margin: 0 auto !important;
    }

    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a1f29 0%, #050505 100%);
        color: #e6edf3;
    }

    .all-center-container {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .main-title {
        font-size: 5rem !important;
        font-weight: 900;
        background: linear-gradient(90deg, #58a6ff, #3fb950);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        text-align: center;
        width: 100%;
    }

    .tagline {
        color: #8b949e;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-bottom: 40px;
        text-align: center;
        width: 100%;
    }

    .feature-grid {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
        margin-bottom: 50px;
        width: 100%;
    }

    .service-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px 15px;
        width: 220px;
        text-align: center;
    }

    .service-card h3 { color: #58a6ff; margin-bottom: 10px; }
    .service-card p { color: #8b949e; font-size: 0.8rem; }

    /* Center the button column contents */
    [data-testid="stColumn"] {
        display: flex !important;
        justify-content: center !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        padding: 12px 80px !important;
        font-size: 1.2rem !important;
        border-radius: 50px !important;
        color: white !important;
        font-weight: bold !important;
        box-shadow: 0 10px 25px rgba(35, 134, 54, 0.3) !important;
        white-space: nowrap !important;
        width: 320px !important;
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
        <div class="all-center-container">
            <h1 class="main-title">CareerMind AI</h1>
            <p class="tagline">Architecting Your Professional Future</p>
            <div class="feature-grid">
                <div class="service-card"><h3>🔍 Audit</h3><p>CV & JD Alignment</p></div>
                <div class="service-card"><h3>✉️ Script</h3><p>Cover Letter Builder</p></div>
                <div class="service-card"><h3>🎙️ Master</h3><p>Interview Simulator</p></div>
                <div class="service-card"><h3>💰 Value</h3><p>Salary Estimation</p></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([3, 3, 3])
    with col2:
        if st.button("Access Professional Suite"):
            st.session_state.entered = True
            st.rerun()

else:
    with st.sidebar:
        st.markdown("<h2 style='text-align:center; color:#58a6ff;'>🧠 CareerMind</h2>", unsafe_allow_html=True)
        page = st.radio("Tools", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        if st.button("Logout"):
            st.session_state.entered = False
            st.rerun()
    st.title(page)
    st.info(f"Connected to Groq Cloud for {page}.")
