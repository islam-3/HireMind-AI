import streamlit as st
try:
    from groq import Groq
except ImportError:
    st.error("Missing 'groq' library. Please check requirements.txt")
    st.stop()

# --- 1. إعدادات الصفحة ---
st.set_page_config(
    page_title="CareerMind AI", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. نظام التصميم (CSS) - التوسيط المطلق ---
st.markdown("""
    <style>
    /* تصفير الهوامش لرفع المحتوى للأعلى */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a1f29 0%, #050505 100%);
        color: #e6edf3;
    }

    /* حاوية الهيرو الرئيسية موسطنة إجبارياً */
    .hero-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        width: 100%;
        margin-top: 2vh;
    }

    /* تصميم العنوان الاحترافي */
    .main-brand-title {
        font-size: 5.5rem !important;
        font-weight: 900;
        margin-bottom: 0px !important;
        background: linear-gradient(90deg, #58a6ff, #3fb950);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }

    .brand-subtitle {
        font-size: 1rem;
        color: #8b949e;
        margin-top: -10px;
        margin-bottom: 40px;
        text-transform: uppercase;
        letter-spacing: 10px;
        font-weight: 300;
    }

    /* شبكة البطاقات الموسطنة */
    .features-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
        width: 100%;
        max-width: 1200px;
        margin-bottom: 45px;
    }

    .card-item {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 35px 20px;
        width: 230px;
        transition: 0.4s;
    }

    .card-item:hover {
        border-color: #58a6ff;
        transform: translateY(-10px);
        background: rgba(88, 166, 255, 0.05);
    }

    .card-item h3 { color: #58a6ff; font-size: 1.4rem; margin-bottom: 10px; }
    .card-item p { color: #8b949e; font-size: 0.85rem; line-height: 1.5; }

    /* موسطنة الزرار */
    div.stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        border: none !important;
        padding: 15px 80px !important;
        font-size: 1.2rem !important;
        border-radius: 60px !important;
        color: white !important;
        font-weight: 800 !important;
        box-shadow: 0 10px 30px rgba(35, 134, 54, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. الجلسة والمفاتيح ---
if "entered" not in st.session_state:
    st.session_state.entered = False

# --- 4. العرض ---
if not st.session_state.entered:
    # استخدام حاوية CSS الموسطنة
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-brand-title">CareerMind AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="brand-subtitle">Architecting Your Professional Future</p>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="features-container">
            <div class="card-item">
                <h3>🔍 Audit</h3>
                <p>Strategic CV analysis and JD alignment mapping.</p>
            </div>
            <div class="card-item">
                <h3>✉️ Script</h3>
                <p>High-conversion cover letters crafted by AI.</p>
            </div>
            <div class="card-item">
                <h3>🎙️ Master</h3>
                <p>Advanced real-time interview roleplay simulations.</p>
            </div>
            <div class="card-item">
                <h3>💰 Value</h3>
                <p>Global salary benchmarks for 2026 market trends.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # وضع الزر في منتصف الأعمدة
    c1, c2, c3 = st.columns([1, 0.8, 1])
    with c2:
        if st.button("Access Professional Suite", use_container_width=True):
            st.session_state.entered = True
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

else:
    with st.sidebar:
        st.markdown("<h2 style='text-align:center; color:#58a6ff;'>🧠 CareerMind</h2>", unsafe_allow_html=True)
        page = st.radio("Executive Suite", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.entered = False
            st.rerun()

    st.title(page)
    st.success(f"Workspace Synchronized: {page} is ready.")
