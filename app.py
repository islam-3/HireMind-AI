import streamlit as st
try:
    from groq import Groq
except ImportError:
    st.error("Missing 'groq' library.")
    st.stop()

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

# --- 2. كود الـ CSS (النسخة الأصلية للزر الصغير على اليسار) ---
st.markdown("""
    <style>
    [data-testid="stAppViewBlockContainer"] {
        padding-top: 2rem !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
    }

    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a1f29 0%, #050505 100%);
        color: #e6edf3;
    }

    .hero-container {
        text-align: center;
        width: 100%;
        margin-bottom: 40px;
    }

    .main-title {
        font-size: 5rem !important;
        font-weight: 900;
        background: linear-gradient(90deg, #58a6ff, #3fb950);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        display: inline-block;
    }

    .tagline {
        color: #8b949e;
        letter-spacing: 5px;
        text-transform: uppercase;
        width: 100%;
        text-align: center;
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

    /* تنسيق الزر الأصلي كما في الصورة (بدون توسيط جبري) */
    div.stButton > button {
        background: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
        color: white !important;
        transition: 0.3s;
    }

    div.stButton > button:hover {
        border-color: #3fb950 !important;
        background: rgba(63, 185, 80, 0.1) !important;
    }

    /* تنسيق خاص لزر اللوج أوت والأنالايز فقط لتمميزهم عن الواجهة */
    .internal-tools [data-testid="stSidebar"] { background-color: #0d1117 !important; }
    </style>
    """, unsafe_allow_html=True)

if "entered" not in st.session_state:
    st.session_state.entered = False

if "GROQ_API_KEY" not in st.secrets:
    st.error("Missing API Key in Secrets.")
    st.stop()

# --- 4. العرض ---
if not st.session_state.entered:
    # الصفحة الأولى (image_38029a.jpg)
    st.markdown("""
        <div class="hero-container">
            <h1 class="main-title">CareerMind AI</h1>
            <p class="tagline">Architecting Your Professional Future</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="feature-grid">
            <div class="service-card"><h3>🔍 Audit</h3><p style="color: #8b949e; font-size: 0.8rem;">CV & JD Alignment</p></div>
            <div class="service-card"><h3>✉️ Script</h3><p style="color: #8b949e; font-size: 0.8rem;">Cover Letter Builder</p></div>
            <div class="service-card"><h3>🎙️ Master</h3><p style="color: #8b949e; font-size: 0.8rem;">Interview Simulator</p></div>
            <div class="service-card"><h3>💰 Value</h3><p style="color: #8b949e; font-size: 0.8rem;">Salary Estimation</p></div>
        </div>
    """, unsafe_allow_html=True)

    # الزر الصغير على اليسار كما في الصورة
    col1, col2, col3 = st.columns([1.2, 4, 1])
    with col1:
        if st.button("Access Professional Suite"):
            st.session_state.entered = True
            st.rerun()

else:
    # الصفحة الداخلية
    with st.sidebar:
        st.markdown("<h3 style='text-align:center;'>🧠 CareerMind</h3>", unsafe_allow_html=True)
        page = st.radio("Tools", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        
        for _ in range(15): st.sidebar.write("")
        if st.button("Logout"):
            st.session_state.entered = False
            st.rerun()
            
    st.title(page)
    if page == "🔍 CV Matcher":
        col_jd, col_cv = st.columns(2)
        with col_jd:
            st.subheader("📝 Job Description")
            st.text_area("Paste JD here...", height=250)
        with col_cv:
            st.subheader("📄 Your CV")
            st.file_uploader("Upload CV")
            
        st.write("")
        if st.button("Start Analysis"):
            st.info("Analyzing...")
