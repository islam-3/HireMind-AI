import streamlit as st
try:
    from groq import Groq
except ImportError:
    st.error("Missing 'groq' library.")
    st.stop()

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

# --- 2. كود الـ CSS النظيف (العودة للجذور) ---
st.markdown("""
    <style>
    /* تنسيق الخلفية العامة */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a1f29 0%, #050505 100%);
        color: #e6edf3;
    }

    /* تنسيق الصفحة الأولى */
    .hero-section {
        text-align: center;
        padding: 60px 0;
    }
    
    .main-title {
        font-size: 5rem !important;
        font-weight: 900;
        background: linear-gradient(90deg, #58a6ff, #3fb950);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    .tagline {
        color: #8b949e;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-bottom: 40px;
    }

    .feature-grid {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
        margin-bottom: 50px;
    }

    .service-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px 15px;
        width: 220px;
        text-align: center;
    }

    /* تنسيق الأزرار الافتراضي (لضمان عدم التداخل) */
    div.stButton > button {
        border-radius: 10px !important;
        transition: 0.3s;
    }
    
    /* تنسيق خاص لزر الدخول في الصفحة الأولى فقط */
    .landing-button-container {
        display: flex;
        justify-content: center;
        width: 100%;
    }

    /* تنسيق الواجهة الداخلية */
    .internal-header {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        border: 1px solid rgba(88, 166, 255, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

if "entered" not in st.session_state:
    st.session_state.entered = False

# التحقق من مفتاح API
if "GROQ_API_KEY" not in st.secrets:
    st.error("Missing API Key in Secrets.")
    st.stop()

# --- 3. عرض الصفحات ---

if not st.session_state.entered:
    # --- العودة لتصميم الصفحة الأولى الأصلي ---
    st.markdown("""
        <div class="hero-section">
            <h1 class="main-title">CareerMind AI</h1>
            <p class="tagline">Architecting Your Professional Future</p>
        </div>
        <div class="feature-grid">
            <div class="service-card"><h3>🔍 Audit</h3><p>CV & JD Alignment</p></div>
            <div class="service-card"><h3>✉️ Script</h3><p>Cover Letter Builder</p></div>
            <div class="service-card"><h3>🎙️ Master</h3><p>Interview Simulator</p></div>
            <div class="service-card"><h3>💰 Value</h3><p>Salary Estimation</p></div>
        </div>
    """, unsafe_allow_html=True)

    # زر الدخول موسطن وبسيط
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Access Professional Suite", use_container_width=True):
            st.session_state.entered = True
            st.rerun()

else:
    # --- الواجهة الداخلية (نظيفة ومرتبة) ---
    with st.sidebar:
        st.title("🧠 CareerMind")
        page = st.radio("Executive Tools", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        st.markdown("---")
        if st.button("Logout"):
            st.session_state.entered = False
            st.rerun()

    # محتوى صفحة CV Matcher
    if page == "🔍 CV Matcher":
        st.markdown('<div class="internal-header"><h1>CV Matcher</h1><p>Compare your CV with a specific Job Description.</p></div>', unsafe_allow_html=True)
        
        col_jd, col_cv = st.columns(2)
        with col_jd:
            st.subheader("📝 Job Description")
            jd_text = st.text_area("Paste JD here...", height=300)
        with col_cv:
            st.subheader("📄 Your CV")
            cv_text = st.text_area("Paste CV text here...", height=300)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Start Analysis", type="primary", use_container_width=True):
            if jd_text and cv_text:
                st.success("Analysis started! (Logic goes here)")
            else:
                st.warning("Please fill both fields.")
    
    else:
        st.title(page)
        st.info("This tool is coming soon.")
