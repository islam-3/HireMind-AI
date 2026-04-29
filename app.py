import streamlit as st
try:
    from groq import Groq
except ImportError:
    st.error("Missing 'groq' library.")
    st.stop()

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

# --- 2. كود الـ CSS الجبري للتوسيط المطلق (العنوان + البطاقات + الزر) ---
st.markdown("""
    <style>
    /* تصفير الحاويات الأساسية وتوسيطها */
    [data-testid="stAppViewBlockContainer"] {
        padding-top: 2rem !important;
        max-width: 1100px !important;
        margin: 0 auto !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }

    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a1f29 0%, #050505 100%);
        color: #e6edf3;
    }

    /* تنسيق العنوان والتاجلاين في الوسط */
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
        width: 100%;
    }

    .tagline {
        color: #8b949e;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-bottom: 40px;
        width: 100%;
    }

    /* شبكة البطاقات موسطنة */
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

    /* --- سر توسيط الزر المطلق --- */
    [data-testid="stColumn"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
    }

    div.stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        padding: 12px 0px !important;
        font-size: 1.2rem !important;
        border-radius: 50px !important;
        color: white !important;
        font-weight: bold !important;
        box-shadow: 0 10px 25px rgba(35, 134, 54, 0.3) !important;
        width: 350px !important; /* عرض ثابت لضمان التوازن */
        margin: 0 auto !important;
        white-space: nowrap !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة الجلسة والمفاتيح ---
if "entered" not in st.session_state:
    st.session_state.entered = False

if "GROQ_API_KEY" not in st.secrets:
    st.error("Missing API Key in Secrets.")
    st.stop()

# --- 4. العرض ---
if not st.session_state.entered:
    # حاوية العنوان والبطاقات
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

    # توسيط الزر باستخدام أعمدة متوازنة تماماً
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Access Professional Suite"):
            st.session_state.entered = True
            st.rerun()

else:
    # لوحة التحكم الداخلية (بعد تسجيل الدخول)
    with st.sidebar:
        st.markdown("<h2 style='text-align:center; color:#58a6ff;'>🧠 CareerMind</h2>", unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("Executive tools", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        if st.button("Logout"):
            st.session_state.entered = False
            st.rerun()
            
    st.title(page)
    st.info(f"Workspace ready for {page}. Connected to Groq Intelligence.")
