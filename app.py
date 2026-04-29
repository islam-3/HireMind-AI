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

# --- 2. نظام التصميم (CSS) للتوسيط الكامل والجمالية ---
st.markdown("""
    <style>
    /* تنظيف المساحات */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 0rem !important;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a1f29 0%, #050505 100%);
        color: #e6edf3;
    }

    /* حاوية التوسيط الكامل */
    .hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        width: 100%;
        padding-top: 2vh;
    }

    /* تصميم العنوان (موسطن مع توهج) */
    .main-brand {
        font-size: 5rem !important;
        font-weight: 900;
        margin-bottom: 0px;
        background: linear-gradient(90deg, #58a6ff, #3fb950);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 15px rgba(88, 166, 255, 0.2)); /* توهج خفيف */
    }

    .brand-tagline {
        font-size: 1rem;
        color: #8b949e;
        margin-bottom: 40px;
        text-transform: uppercase;
        letter-spacing: 8px; /* تباعد حروف احترافي */
        font-weight: 300;
    }

    /* شبكة البطاقات (موسطنة) */
    .cards-grid {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
        width: 100%;
        max-width: 1100px;
        margin-bottom: 50px;
    }

    .feature-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 30px 20px;
        width: 220px;
        transition: all 0.4s ease;
        text-align: center;
    }

    .feature-card:hover {
        border-color: #3fb950;
        transform: translateY(-10px);
        background: rgba(63, 185, 80, 0.05);
        box-shadow: 0 15px 30px rgba(0,0,0,0.4);
    }

    .feature-card h3 { 
        color: #58a6ff; 
        font-size: 1.3rem; 
        margin-bottom: 12px; 
    }
    
    .feature-card p { 
        color: #8b949e; 
        font-size: 0.8rem; 
        line-height: 1.5;
    }

    /* زر الدخول الموسطن */
    div.stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        border: none !important;
        padding: 14px 70px !important;
        font-size: 1.2rem !important;
        border-radius: 50px !important;
        color: white !important;
        font-weight: bold !important;
        box-shadow: 0 10px 25px rgba(35, 134, 54, 0.3) !important;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 35px rgba(35, 134, 54, 0.5) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة المفاتيح والجلسة ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("API Key not found in Secrets.")
    st.stop()

if "entered" not in st.session_state:
    st.session_state.entered = False

# --- 4. عرض الواجهة ---
if not st.session_state.entered:
    # حاوية الهيرو الموسطنة بالكامل
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    
    # اسم الموقع بالوسط
    st.markdown('<h1 class="main-brand">CareerMind AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="brand-tagline">Architecting Your Professional Future</p>', unsafe_allow_html=True)
    
    # البطاقات بالوسط
    st.markdown("""
        <div class="cards-grid">
            <div class="feature-card">
                <h3>🔍 Audit</h3>
                <p>Strategic CV analysis and JD alignment mapping.</p>
            </div>
            <div class="feature-card">
                <h3>✉️ Script</h3>
                <p>High-conversion cover letters crafted by AI.</p>
            </div>
            <div class="feature-card">
                <h3>🎙️ Master</h3>
                <p>Advanced real-time interview roleplay simulations.</p>
            </div>
            <div class="feature-card">
                <h3>💰 Value</h3>
                <p>Global salary benchmarks for 2026 market trends.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # زر الدخول الموسطن
    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        if st.button("Access Professional Suite", use_container_width=True):
            st.session_state.entered = True
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # محتوى لوحة التحكم الداخلية
    with st.sidebar:
        st.markdown("<h2 style='text-align:center; color:#58a6ff;'>🧠 CareerMind</h2>", unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("Executive Suite", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        
        st.markdown("<br>" * 10, unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.entered = False
            st.rerun()

    st.title(f"Active Workspace: {page}")
    st.success(f"System synchronized with Groq Cloud. Ready for {page} tasks.")
