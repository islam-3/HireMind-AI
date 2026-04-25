import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. UI CONFIGURATION & HIGH-END STYLING ---
st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* تطبيق الخلفية الداكنة العميقة */
    .stApp {
        background: radial-gradient(circle at 20% 20%, #1a1f29 0%, #050505 100%);
        color: #e6edf3;
    }

    /* حاوية صفحة الهبوط */
    .hero-wrapper {
        text-align: center;
        padding: 100px 20px;
        min-height: 100vh;
    }

    .main-title {
        font-size: 5.5rem;
        font-weight: 900;
        letter-spacing: -3px;
        margin-bottom: 0px;
        background: linear-gradient(90deg, #58a6ff, #3fb950);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .sub-title {
        font-size: 1.3rem;
        color: #8b949e;
        margin-bottom: 60px;
        font-weight: 300;
        text-transform: uppercase;
        letter-spacing: 4px;
    }

    /* بطاقات الخدمات الاحترافية */
    .feature-grid {
        display: flex;
        justify-content: center;
        gap: 25px;
        flex-wrap: wrap;
        max-width: 1200px;
        margin: 0 auto;
    }

    .service-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 40px 30px;
        width: 260px;
        transition: all 0.5s ease;
        position: relative;
        overflow: hidden;
    }

    .service-card:hover {
        background: rgba(88, 166, 255, 0.08);
        border-color: #58a6ff;
        transform: translateY(-15px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.6), 0 0 20px rgba(88, 166, 255, 0.2);
    }

    .service-card h3 {
        font-size: 1.4rem;
        color: #58a6ff;
        margin-bottom: 15px;
    }

    .service-card p {
        font-size: 0.9rem;
        color: #8b949e;
        line-height: 1.6;
    }

    /* زر الدخول الفخم */
    .stButton > button {
        background: #238636 !important;
        border: none !important;
        padding: 18px 60px !important;
        font-size: 1.4rem !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 700 !important;
        margin-top: 80px !important;
        transition: 0.4s !important;
        box-shadow: 0 10px 30px rgba(35, 134, 54, 0.3) !important;
    }

    .stButton > button:hover {
        transform: scale(1.08);
        box-shadow: 0 15px 40px rgba(35, 134, 54, 0.5) !important;
        background: #2ea043 !important;
    }

    /* السايدبار */
    [data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid #30363d; }
    .sidebar-logo { display: flex; flex-direction: column; align-items: center; font-size: 2.2rem !important; font-weight: bold; color: #58a6ff; padding-top: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC ---
if "entered" not in st.session_state:
    st.session_state.entered = False

# --- 3. PAGE CONTENT ---
if not st.session_state.entered:
    # واجهة الدخول الاحترافية
    st.markdown("""
        <div class="hero-wrapper">
            <h1 class="main-title">CareerMind AI</h1>
            <p class="sub-title">The Future of Career Engineering</p>
            <div class="feature-grid">
                <div class="service-card">
                    <h3>🔍 Audit</h3>
                    <p>Advanced gap analysis between your CV and global JD standards.</p>
                </div>
                <div class="service-card">
                    <h3>✉️ Script</h3>
                    <p>AI-architected cover letters with psychological impact.</p>
                </div>
                <div class="service-card">
                    <h3>🎙️ Master</h3>
                    <p>High-stakes interview simulation based on real 2026 data.</p>
                </div>
                <div class="service-card">
                    <h3>💰 Value</h3>
                    <p>Precise market valuation using real-time global benchmarks.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("ENTER WORKSPACE"):
            st.session_state.entered = True
            st.rerun()

else:
    # المحتوى الداخلي للموقع (كما في الصور الناجحة السابقة)
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🧠 CareerMind</div>', unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("NAVIGATION", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        
        st.markdown("<br>" * 8, unsafe_allow_html=True)
        if st.button("🗑️ Exit Dashboard", use_container_width=True):
            st.session_state.entered = False
            st.rerun()

    # صفحات الخدمات (تحافظ على ترتيبها من اليمين لليسار كما طلبت سابقاً)
    if page == "🔍 CV Matcher":
        st.title("Strategic Application Audit")
        col_l, col_r = st.columns(2, gap="large")
        with col_l:
            st.text_area("JD Content", height=300, placeholder="Drop requirements...")
        with col_r: # السيرة الذاتية دائماً على اليمين
            st.file_uploader("Upload CV", type="pdf")
            st.button("Analyze Match")

    elif page == "💰 Salary Insight":
        st.title("Market Value Estimator")
        # العودة لتنسيق 2026 الواقعي مع إلغاء الدولار
        st.info("Estimating realistic 2026 local currency rates...")
