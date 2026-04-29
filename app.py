import streamlit as st
try:
    from groq import Groq
except ImportError:
    st.error("Missing 'groq' library.")
    st.stop()

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

# --- 2. كود الـ CSS (التوسيط المطلق للأزرار) ---
st.markdown("""
    <style>
    [data-testid="stAppViewBlockContainer"] {
        padding-top: 1.5rem !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
    }

    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a1f29 0%, #050505 100%);
        color: #e6edf3;
    }

    /* الواجهة الأولى */
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
    
    /* ضمان توسيط أي زر داخل Streamlit */
    .stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        padding: 8px 30px !important;
        font-size: 1rem !important;
        border-radius: 50px !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        min-width: 250px !important;
    }

    /* تنسيقات الأدوات الداخلية */
    .tool-header {
        background: rgba(255, 255, 255, 0.03);
        padding: 15px 25px;
        border-radius: 12px;
        border: 1px solid rgba(88, 166, 255, 0.2);
        margin-bottom: 30px;
    }
    .tool-header h2 { color: #58a6ff; margin: 0; font-size: 1.5rem !important; }
    
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
    # الواجهة الأولى
    st.markdown('<div class="hero-container"><h1 class="main-title">CareerMind AI</h1><p class="tagline">Architecting Your Professional Future</p></div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 50px;">
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 30px 15px; width: 220px; text-align: center;"><h3>🔍 Audit</h3><p style="color: #8b949e; font-size: 0.8rem;">CV & JD Alignment</p></div>
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 30px 15px; width: 220px; text-align: center;"><h3>✉️ Script</h3><p style="color: #8b949e; font-size: 0.8rem;">Cover Letter Builder</p></div>
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 30px 15px; width: 220px; text-align: center;"><h3>🎙️ Master</h3><p style="color: #8b949e; font-size: 0.8rem;">Interview Simulator</p></div>
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 30px 15px; width: 220px; text-align: center;"><h3>💰 Value</h3><p style="color: #8b949e; font-size: 0.8rem;">Salary Estimation</p></div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Access Professional Suite"):
        st.session_state.entered = True
        st.rerun()

else:
    # الواجهة الداخلية
    with st.sidebar:
        st.markdown("<h3 style='text-align:center; color:#58a6ff;'>🧠 CareerMind</h3>", unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("Executive Tools", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        
        for _ in range(15): st.sidebar.write("") # دفع الزر للأسفل أكثر
        if st.button("Logout"):
            st.session_state.entered = False
            st.rerun()

    if page == "🔍 CV Matcher":
        st.markdown(f'<div class="tool-header"><h2>{page}</h2><p style="color: #8b949e; font-size: 0.9rem;">Optimize your application by matching your CV with the Job Description.</p></div>', unsafe_allow_html=True)
        
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("### 📝 Job Description")
            jd_text = st.text_area("Paste the job details here...", height=250)
        with col_right:
            st.markdown("### 📄 Your CV")
            cv_file = st.file_uploader("Upload Resume (PDF/TXT)", type=["pdf", "txt"])
            st.markdown("<div style='height: 95px;'></div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        # الزر الآن في حاوية موسطنة تلقائياً بسبب CSS
        if st.button("Start Analysis"):
            if cv_file and jd_text:
                st.info("🚀 AI Analysis in progress...")
            else:
                st.warning("⚠️ Please provide both CV and JD.")
