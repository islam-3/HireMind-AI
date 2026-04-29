import streamlit as st
try:
    from groq import Groq
except ImportError:
    st.error("Missing 'groq' library.")
    st.stop()

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

# --- 2. كود الـ CSS (القالب المعتمد + تنسيق الأدوات الداخلية) ---
st.markdown("""
    <style>
    /* القالب المقدس للواجهة الأولى */
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

    /* زر الدخول الرئيسي */
    div.stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        padding: 12px 0px !important;
        font-size: 1.2rem !important;
        border-radius: 50px !important;
        color: white !important;
        font-weight: bold !important;
        box-shadow: 0 10px 25px rgba(35, 134, 54, 0.3) !important;
        border: none !important;
    }

    /* --- تنسيقات الأدوات الداخلية --- */
    .tool-header {
        background: rgba(88, 166, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #58a6ff;
        margin-bottom: 30px;
    }
    
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    [data-testid="stSidebar"] {
        background-color: #0d1117 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. حالة الجلسة ---
if "entered" not in st.session_state:
    st.session_state.entered = False

if "GROQ_API_KEY" not in st.secrets:
    st.error("Missing API Key in Secrets.")
    st.stop()

# --- 4. عرض الواجهة ---
if not st.session_state.entered:
    # الواجهة الأولى (المعتمدة)
    st.markdown("""
        <div class="hero-container">
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

    _, col, _ = st.columns([2, 1, 2])
    with col:
        if st.button("Access Professional Suite", use_container_width=True):
            st.session_state.entered = True
            st.rerun()

else:
    # الواجهة الداخلية (المطورة)
    with st.sidebar:
        st.markdown("<h2 style='text-align:center; color:#58a6ff;'>🧠 CareerMind</h2>", unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("Executive Tools", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        
        st.write("") # مساحة
        if st.button("Logout", use_container_width=True):
            st.session_state.entered = False
            st.rerun()

    # محتوى الأداة المختارة
    if page == "🔍 CV Matcher":
        st.markdown(f'<div class="tool-header"><h1>{page}</h1><p>Analyze how well your CV aligns with a specific Job Description.</p></div>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Your CV")
            cv_file = st.file_uploader("Upload Resume (PDF/TXT)", type=["pdf", "txt"])
        
        with col_b:
            st.subheader("Job Description")
            jd_text = st.text_area("Paste the target JD here...", height=200)
            
        if st.button("Start Analysis", use_container_width=True):
            if cv_file and jd_text:
                with st.spinner("AI is analyzing alignment..."):
                    # هنا سنضع لاحقاً كود الاتصال بـ Groq
                    st.success("Analysis Complete! (Logic to be added)")
            else:
                st.warning("Please upload a CV and paste a Job Description first.")

    else:
        st.markdown(f'<div class="tool-header"><h1>{page}</h1><p>Workspace for {page} is ready.</p></div>', unsafe_allow_html=True)
        st.info("Feature under development...")
