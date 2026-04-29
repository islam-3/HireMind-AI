import streamlit as st
try:
    from groq import Groq
except ImportError:
    st.error("Missing 'groq' library. Please check requirements.txt")
    st.stop()

# --- 1. إعدادات الصفحة الاحترافية ---
st.set_page_config(
    page_title="CareerMind AI", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. نظام التصميم (CSS) لضغط الواجهة للأعلى ---
st.markdown("""
    <style>
    /* إزالة الفراغات الافتراضية المزعجة في Streamlit */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 95%;
    }
    
    /* الخلفية والخطوط */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a1f29 0%, #050505 100%);
        color: #e6edf3;
        font-family: 'Inter', sans-serif;
    }

    /* حاوية الهيرو (مركزة ومرفوعة) */
    .hero-wrapper {
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        padding-top: 5vh;
    }

    .main-title {
        font-size: 4.5rem !important;
        font-weight: 900;
        margin-bottom: 5px;
        background: linear-gradient(90deg, #58a6ff, #3fb950);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .sub-title {
        font-size: 0.9rem;
        color: #8b949e;
        margin-bottom: 35px;
        text-transform: uppercase;
        letter-spacing: 5px;
    }

    /* شبكة البطاقات (مضغوطة) */
    .feature-grid {
        display: flex;
        justify-content: center;
        gap: 15px;
        flex-wrap: wrap;
        margin-bottom: 40px;
    }

    .service-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 25px 15px;
        width: 210px;
        transition: 0.3s ease;
    }

    .service-card:hover {
        border-color: #58a6ff;
        transform: translateY(-8px);
        background: rgba(88, 166, 255, 0.05);
    }

    .service-card h3 { 
        color: #58a6ff; 
        font-size: 1.2rem; 
        margin-bottom: 10px; 
    }
    
    .service-card p { 
        color: #8b949e; 
        font-size: 0.75rem; 
        line-height: 1.4;
    }

    /* زر الدخول الفخم */
    div.stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        border: none !important;
        padding: 12px 50px !important;
        font-size: 1.1rem !important;
        border-radius: 50px !important;
        color: white !important;
        font-weight: bold !important;
        box-shadow: 0 8px 20px rgba(35, 134, 54, 0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. التحقق من المفتاح (Secrets) ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Please set GROQ_API_KEY in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 4. منطق حالة الجلسة ---
if "entered" not in st.session_state:
    st.session_state.entered = False

# --- 5. عرض الواجهة ---
if not st.session_state.entered:
    # واجهة الدخول ( Landing Page )
    st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">CareerMind AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Architecting Your Professional Future</p>', unsafe_allow_html=True)
    
    # البطاقات الأربعة
    st.markdown("""
        <div class="feature-grid">
            <div class="service-card">
                <h3>🔍 Audit</h3>
                <p>Strategic alignment analysis between CV and JD.</p>
            </div>
            <div class="service-card">
                <h3>✉️ Script</h3>
                <p>Precision-crafted cover letters for recruiters.</p>
            </div>
            <div class="service-card">
                <h3>🎙️ Master</h3>
                <p>AI-driven context-aware interview simulations.</p>
            </div>
            <div class="service-card">
                <h3>💰 Value</h3>
                <p>2026 market valuation for your role.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # زر الدخول الموسطن
    col1, col2, col3 = st.columns([1, 0.8, 1])
    with col2:
        if st.button("Access Professional Suite", use_container_width=True):
            st.session_state.entered = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # لوحة التحكم الداخلية بعد الدخول
    with st.sidebar:
        st.markdown("<h2 style='text-align:center; color:#58a6ff;'>🧠 CareerMind</h2>", unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("Executive Tools", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        
        st.markdown("<br>" * 10, unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True):
            st.session_state.entered = False
            st.rerun()

    st.title(page)
    st.info(f"System Online: Connected to Groq Cloud for {page}.")
    # هنا ستتم إضافة محتوى كل صفحة لاحقاً
