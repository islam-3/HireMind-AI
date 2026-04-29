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

# --- 2. نظام التصميم (CSS) - فرض التوسيط المطلق ---
st.markdown("""
    <style>
    /* 1. رفع كل شيء للأعلى وإلغاء القيود الجانبية */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
        display: flex !important;
        justify-content: center !important;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a1f29 0%, #050505 100%);
        color: #e6edf3;
    }

    /* 2. حاوية المحتوى الرئيسية - العرض ثابت والتوسيط تلقائي */
    .main-wrapper {
        width: 100%;
        max-width: 1100px;
        margin: 0 auto !important;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    /* 3. تنسيق العنوان الفخم موسطن */
    .hero-title {
        font-size: 5.5rem !important;
        font-weight: 900;
        margin: 0 auto 5px auto !important;
        display: block;
        background: linear-gradient(90deg, #58a6ff, #3fb950);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #8b949e;
        margin: 0 auto 40px auto !important;
        text-transform: uppercase;
        letter-spacing: 10px;
        font-weight: 300;
    }

    /* 4. شبكة البطاقات موسطنة */
    .cards-box {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
        margin-bottom: 50px;
        width: 100%;
    }

    .feature-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px 15px;
        width: 220px;
        transition: 0.4s;
    }

    .feature-card h3 { color: #58a6ff; font-size: 1.3rem; margin-bottom: 10px; }
    .feature-card p { color: #8b949e; font-size: 0.8rem; line-height: 1.5; }

    /* 5. تنسيق الزرار الموسطن */
    .stButton {
        display: flex;
        justify-content: center;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        border: none !important;
        padding: 15px 80px !important;
        font-size: 1.2rem !important;
        border-radius: 60px !important;
        color: white !important;
        font-weight: bold !important;
        box-shadow: 0 10px 30px rgba(35, 134, 54, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة الجلسة والمفاتيح ---
if "entered" not in st.session_state:
    st.session_state.entered = False

# --- 4. العرض الرئيسي ---
if not st.session_state.entered:
    # استخدام Wrapper لفرض التوسيط
    st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)
    
    st.markdown('<h1 class="hero-title">CareerMind AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Architecting Your Professional Future</p>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="cards-box">
            <div class="feature-card"><h3>🔍 Audit</h3><p>Strategic CV analysis and JD alignment mapping.</p></div>
            <div class="feature-card"><h3>✉️ Script</h3><p>High-conversion cover letters crafted by AI.</p></div>
            <div class="feature-card"><h3>🎙️ Master</h3><p>Advanced real-time interview roleplay simulations.</p></div>
            <div class="feature-card"><h3>💰 Value</h3><p>Global salary benchmarks for 2026 trends.</p></div>
        </div>
    """, unsafe_allow_html=True)
    
    # الزر موسطن تماماً
    if st.button("Access Professional Suite"):
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
