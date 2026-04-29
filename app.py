import streamlit as st
try:
    from groq import Groq
except ImportError:
    st.error("Missing 'groq' library.")
    st.stop()

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

# --- 2. كود الـ CSS (فصل كامل بين الواجهتين) ---
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

    /* --- تنسيق الواجهة الأولى (ممنوع اللمس) --- */
    .hero-container { text-align: center; width: 100%; margin-bottom: 40px; }
    .main-title {
        font-size: 5rem !important;
        font-weight: 900;
        background: linear-gradient(90deg, #58a6ff, #3fb950);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    .tagline { color: #8b949e; letter-spacing: 5px; text-transform: uppercase; text-align: center; }
    .feature-grid { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 50px; }
    .service-card { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 30px 15px; width: 220px; text-align: center; }

    /* تنسيق زر الدخول (يبقى يسار كما في الصورة) */
    .landing-btn button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        padding: 12px 40px !important;
        font-size: 1.1rem !important;
        border-radius: 50px !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
    }

    /* --- تنسيق الواجهة الداخلية (التعديلات الجديدة) --- */
    .internal-btn div[data-testid="stButton"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }
    
    .internal-btn button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        padding: 8px 30px !important;
        border-radius: 50px !important;
        color: white !important;
        min-width: 250px !important;
        border: none !important;
    }

    .tool-header {
        background: rgba(255, 255, 255, 0.03);
        padding: 15px 25px;
        border-radius: 12px;
        border: 1px solid rgba(88, 166, 255, 0.2);
        margin-bottom: 30px;
    }
    
    .stTextArea textarea { background-color: rgba(255, 255, 255, 0.05) !important; color: white !important; }
    [data-testid="stSidebar"] { background-color: #0d1117 !important; }
    </style>
    """, unsafe_allow_html=True)

if "entered" not in st.session_state:
    st.session_state.entered = False

if "GROQ_API_KEY" not in st.secrets:
    st.error("Missing API Key in Secrets.")
    st.stop()

# --- 4. العرض ---
if not st.session_state.entered:
    # الصفحة الأولى (كما في image_38e6bd.jpg تماماً)
    st.markdown('<div class="hero-container"><h1 class="main-title">CareerMind AI</h1><p class="tagline">Architecting Your Professional Future</p></div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="feature-grid">
            <div class="service-card"><h3>🔍 Audit</h3><p style="color:#8b949e; font-size:0.8rem;">CV & JD Alignment</p></div>
            <div class="service-card"><h3>✉️ Script</h3><p style="color:#8b949e; font-size:0.8rem;">Cover Letter Builder</p></div>
            <div class="service-card"><h3>🎙️ Master</h3><p style="color:#8b949e; font-size:0.8rem;">Interview Simulator</p></div>
            <div class="service-card"><h3>💰 Value</h3><p style="color:#8b949e; font-size:0.8rem;">Salary Estimation</p></div>
        </div>
    """, unsafe_allow_html=True)
    
    # الزر يسار كما طلبت بالأصل
    st.markdown('<div class="landing-btn">', unsafe_allow_html=True)
    _, col_btn, _ = st.columns([1, 4, 1])
    with col_btn:
        if st.button("Access Professional Suite"):
            st.session_state.entered = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # الصفحة الداخلية (التعديلات الجديدة)
    with st.sidebar:
        st.markdown("<h3 style='text-align:center; color:#58a6ff;'>🧠 CareerMind</h3>", unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("Executive Tools", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        for _ in range(15): st.sidebar.write("") 
        if st.button("Logout"):
            st.session_state.entered = False
            st.rerun()

    if page == "🔍 CV Matcher":
        st.markdown(f'<div class="tool-header"><h2>{page}</h2><p style="color:#8b949e;">Optimize your application by matching your CV with the Job Description.</p></div>', unsafe_allow_html=True)
        
        # JD يسار و CV يمين
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("### 📝 Job Description")
            jd_text = st.text_area("Paste the job details here...", height=250)
        with col_right:
            st.markdown("### 📄 Your CV")
            cv_file = st.file_uploader("Upload Resume (PDF/TXT)", type=["pdf", "txt"])
            st.markdown("<div style='height: 95px;'></div>", unsafe_allow_html=True)
        
        # زر الأنالايز في الوسط تماماً
        st.markdown('<div class="internal-btn">', unsafe_allow_html=True)
        if st.button("Start Analysis"):
            if cv_file and jd_text:
                st.info("🚀 AI Analysis in progress...")
            else:
                st.warning("⚠️ Please provide both CV and JD.")
        st.markdown('</div>', unsafe_allow_html=True)
