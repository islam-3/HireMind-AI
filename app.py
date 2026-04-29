import streamlit as st
try:
    from groq import Groq
except ImportError:
    st.error("Missing 'groq' library. Please check requirements.txt")
    st.stop()

# --- 1. إعدادات الصفحة والتصميم الفخم (CSS) ---
st.set_page_config(
    page_title="CareerMind AI", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* تصفير الفراغات العلوية الافتراضية لـ Streamlit */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 0rem !important;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a1f29 0%, #050505 100%);
        color: #e6edf3;
    }

    /* تنسيق العنوان الرئيسي (توهج خفيف + موسطن) */
    .hero-wrapper {
        text-align: center;
        margin-bottom: 0px;
    }

    .main-title {
        font-size: 5rem !important;
        font-weight: 900;
        background: linear-gradient(90deg, #58a6ff, #3fb950);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    .sub-title {
        color: #8b949e;
        letter-spacing: 5px;
        font-size: 1rem;
        margin-top: -10px;
        margin-bottom: 40px;
        text-transform: uppercase;
    }

    /* تنسيق شبكة البطاقات موسطنة */
    .feature-grid {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
        margin-bottom: 50px;
    }

    .service-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px 15px;
        width: 220px;
        transition: 0.3s;
        text-align: center;
    }

    .service-card:hover {
        border-color: #58a6ff;
        transform: translateY(-8px);
    }

    .service-card h3 { color: #58a6ff; font-size: 1.3rem; margin-bottom: 10px; }
    .service-card p { color: #8b949e; font-size: 0.8rem; line-height: 1.5; }

    /* موسطنة الزر الأخضر الفخم */
    div.stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        border: none !important;
        padding: 12px 60px !important;
        font-size: 1.1rem !important;
        border-radius: 50px !important;
        color: white !important;
        font-weight: bold !important;
        box-shadow: 0 10px 25px rgba(35, 134, 54, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. التحقق من المفتاح في Secrets ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ مفتاح الـ API مفقود! يرجى إضافته في إعدادات Secrets باسم GROQ_API_KEY.")
    st.stop()

# --- 3. حالة الجلسة ودفع الصفحة للأعلى ---
if "entered" not in st.session_state:
    st.session_state.entered = False

# --- 4. عرض الواجهة ---
if not st.session_state.entered:
    # استخدام حاوية CSS الموسطنة للعنوان
    st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">CareerMind AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Architecting Your Professional Future</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # البطاقات الموسطنة
    st.markdown("""
        <div class="feature-grid">
            <div class="service-card">
                <h3>🔍 Audit</h3>
                <p>Strategic alignment analysis between CV and JD.</p>
            </div>
            <div class="service-card">
                <h3>✉️ Script</h3>
                <p>High-conversion cover letters crafted by AI.</p>
            </div>
            <div class="service-card">
                <h3>🎙️ Master</h3>
                <p>Context-aware interview simulation masterclass.</p>
            </div>
            <div class="service-card">
                <h3>💰 Value</h3>
                <p>Dynamic 2026 market valuation benchmarks.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # توسيط الزرار باستخدام columns (آمن ومضمون)
    col1, col2, col3 = st.columns([1, 0.8, 1])
    with col2:
        if st.button("Access Professional Suite", use_container_width=True):
            st.session_state.entered = True
            st.rerun()
else:
    # لوحة التحكم الداخلية
    with st.sidebar:
        st.markdown("<h2 style='text-align:center; color:#58a6ff;'>🧠 CareerMind</h2>", unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("Executive tools", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        if st.button("Logout"):
            st.session_state.entered = False
            st.rerun()
            
    st.title(page)
    st.info(f"Welcome to the {page} workspace.")
