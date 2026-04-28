import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. إعدادات الصفحة والتصميم العالي (UI) ---
st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* الخلفية العميقة */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a1f29 0%, #050505 100%);
        color: #e6edf3;
    }

    /* تنسيق صفحة الهبوط */
    .hero-wrapper {
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 90vh;
    }

    .main-title {
        font-size: 5.5rem;
        font-weight: 900;
        margin-bottom: 10px;
        background: linear-gradient(90deg, #58a6ff, #3fb950);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .sub-title {
        font-size: 1.2rem;
        color: #8b949e;
        margin-bottom: 50px;
        text-transform: uppercase;
        letter-spacing: 6px;
    }

    /* بطاقات الخدمات الأربعة الأصلية */
    .feature-grid {
        display: flex;
        justify-content: center;
        gap: 25px;
        flex-wrap: wrap;
        max-width: 1200px;
        margin-bottom: 60px;
    }

    .service-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 40px 25px;
        width: 260px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .service-card:hover {
        border-color: #58a6ff;
        transform: translateY(-15px);
        background: rgba(88, 166, 255, 0.08);
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
    }

    .service-card h3 { color: #58a6ff; font-size: 1.4rem; margin-bottom: 15px; }
    .service-card p { color: #8b949e; font-size: 0.9rem; line-height: 1.6; }

    /* زر الدخول الأخضر الفخم */
    div.stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        border: none !important;
        padding: 15px 60px !important;
        font-size: 1.3rem !important;
        border-radius: 60px !important;
        color: white !important;
        font-weight: 700 !important;
        transition: 0.4s !important;
        box-shadow: 0 10px 25px rgba(35, 134, 54, 0.3) !important;
    }

    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 35px rgba(35, 134, 54, 0.5) !important;
    }

    /* تنسيق السايدبار */
    [data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid #30363d; }
    .sidebar-logo { font-size: 2.2rem; font-weight: bold; color: #58a6ff; text-align: center; padding: 30px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إعداد المفتاح الجديد لـ Groq ---
# سيستخدم هذا الكود المفتاح الذي وضعته في Secrets تلقائياً
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 3. إدارة الجلسة ---
if "entered" not in st.session_state:
    st.session_state.entered = False

# --- 4. عرض الصفحات ---
if not st.session_state.entered:
    # صفحة البداية الفخمة التي كانت موجودة
    st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">CareerMind AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Architecting Your Professional Future</p>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="feature-grid">
            <div class="service-card">
                <h3>🔍 CV Matcher</h3>
                <p>Strategic alignment analysis between your profile and target roles.</p>
            </div>
            <div class="service-card">
                <h3>✉️ Cover Letter</h3>
                <p>Precision-crafted narratives designed to engage recruiters.</p>
            </div>
            <div class="service-card">
                <h3>🎙️ Interview Prep</h3>
                <p>Context-aware simulation to master high-stakes conversations.</p>
            </div>
            <div class="service-card">
                <h3>💰 Salary Insight</h3>
                <p>Dynamic 2026 market valuation based on global benchmarks.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Access Professional Suite", use_container_width=True):
            st.session_state.entered = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # لوحة التحكم الداخلية (Dashboard) الأصلية
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🧠 CareerMind</div>', unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("EXECUTIVE TOOLS", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        
        st.markdown("<br>" * 8, unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.entered = False
            st.rerun()

    # تنفيذ الأدوات الأربعة
    if page == "🔍 CV Matcher":
        st.title("Strategic Application Audit")
        col_l, col_r = st.columns(2, gap="large")
        with col_l: st.text_area("Job Description", height=350, placeholder="Paste JD here...")
        with col_r: 
            st.file_uploader("Upload Professional Resume", type="pdf")
            if st.button("Generate Match Report"):
                st.info("Analyzing alignment...")

    elif page == "🎙️ Interview Prep":
        st.title("Interview Simulation Environment")
        st.write("Ready to simulate a high-pressure interview?")
        st.button("Start AI Simulation")

    elif page == "💰 Salary Insight":
        st.title("Market Value Intelligence")
        # التنسيق الذي كنا نستخدمه للسوق المحلي
        st.write("Real-time data for 2026 career benchmarks.")
        st.selectbox("Industry", ["Software Engineering", "AI & Data Science", "Fintech"])
        st.button("Get Valuation")
