import streamlit as st
try:
    from groq import Groq
except ImportError:
    st.error("Missing libraries. Check requirements.txt")
    st.stop()

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

# --- 2. التصميم الاحترافي (مبني على النسخة الناجحة) ---
st.markdown("""
    <style>
    /* تقليل الفراغ العلوي لرفع المحتوى */
    .block-container { padding-top: 2rem !important; }
    
    .stApp { background: radial-gradient(circle at 50% 50%, #1a1f29 0%, #050505 100%); color: #e6edf3; }
    
    /* حاوية موسطة وبسيطة */
    .main-container {
        text-align: center;
        margin: 0 auto;
        max-width: 1000px;
    }
    
    .title-text {
        font-size: 5rem !important;
        font-weight: 900;
        background: linear-gradient(90deg, #58a6ff, #3fb950);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    
    .tagline {
        font-size: 1rem;
        color: #8b949e;
        letter-spacing: 5px;
        margin-bottom: 40px;
        text-transform: uppercase;
    }
    
    /* شبكة الخدمات موسطنة تماماً */
    .services-grid {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
        margin-bottom: 50px;
    }
    
    .card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px 20px;
        width: 220px;
    }
    
    .card h3 { color: #58a6ff; font-size: 1.3rem; margin-bottom: 10px; }
    .card p { color: #8b949e; font-size: 0.8rem; }

    /* موسطنة الزر */
    .stButton { display: flex; justify-content: center; }
    div.stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        border: none !important;
        padding: 12px 60px !important;
        font-size: 1.1rem !important;
        border-radius: 50px !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. حالة الجلسة والمفاتيح ---
if "entered" not in st.session_state:
    st.session_state.entered = False

if "GROQ_API_KEY" not in st.secrets:
    st.error("API Key missing in Secrets")
    st.stop()

# --- 4. عرض الواجهة ---
if not st.session_state.entered:
    # استخدام حاوية بسيطة تضمن التوسيط
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="title-text">CareerMind AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">Architecting Your Professional Future</p>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="services-grid">
            <div class="card"><h3>🔍 Audit</h3><p>CV & JD Alignment</p></div>
            <div class="card"><h3>✉️ Script</h3><p>Cover Letter Builder</p></div>
            <div class="card"><h3>🎙️ Master</h3><p>Interview Simulator</p></div>
            <div class="card"><h3>💰 Value</h3><p>Salary Estimation</p></div>
        </div>
    """, unsafe_allow_html=True)
    
    # الزر موسطن طبيعياً داخل الـ Flexbox
    if st.button("Access Professional Suite"):
        st.session_state.entered = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    with st.sidebar:
        st.markdown("<h2 style='text-align:center; color:#58a6ff;'>🧠 CareerMind</h2>", unsafe_allow_html=True)
        page = st.radio("Tools", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        if st.button("Logout"):
            st.session_state.entered = False
            st.rerun()
    st.title(page)
    st.info(f"System synchronized for {page}.")
