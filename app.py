import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. UI CONFIGURATION & HIGH-END STYLING ---
st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Global Deep Background */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a1f29 0%, #050505 100%);
        color: #e6edf3;
    }

    /* Landing Container Adjustment */
    .hero-wrapper {
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 95vh; /* استغلال مساحة الشاشة بشكل أفضل */
        padding-top: 0px;
    }

    .main-title {
        font-size: 5rem;
        font-weight: 900;
        letter-spacing: -2px;
        margin-bottom: 0px;
        background: linear-gradient(90deg, #58a6ff, #3fb950);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .sub-title {
        font-size: 1.1rem;
        color: #8b949e;
        margin-bottom: 40px; /* تقليل المسافة تحت العنوان */
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 5px;
    }

    /* Feature Cards Grid */
    .feature-grid {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
        max-width: 1200px;
        margin-bottom: 40px; /* تقليل المسافة تحت البطاقات لرفع الزر */
    }

    .service-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px 20px;
        width: 240px;
        transition: all 0.4s ease;
    }

    .service-card:hover {
        border-color: #58a6ff;
        transform: translateY(-10px);
        background: rgba(88, 166, 255, 0.05);
        box-shadow: 0 15px 30px rgba(0,0,0,0.5);
    }

    .service-card h3 { color: #58a6ff; font-size: 1.3rem; margin-bottom: 10px; }
    .service-card p { color: #8b949e; font-size: 0.85rem; line-height: 1.5; }

    /* The "Access" Button - Positioned Higher */
    div.stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        border: none !important;
        padding: 12px 50px !important;
        font-size: 1.2rem !important;
        border-radius: 50px !important;
        color: white !important;
        font-weight: 600 !important;
        transition: 0.3s !important;
        box-shadow: 0 8px 20px rgba(35, 134, 54, 0.2) !important;
    }

    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 25px rgba(35, 134, 54, 0.4) !important;
    }

    /* Sidebar Logo */
    .sidebar-logo { display: flex; flex-direction: column; align-items: center; font-size: 2.2rem !important; font-weight: bold; color: #58a6ff; padding-top: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC ---
if "entered" not in st.session_state:
    st.session_state.entered = False

# --- 3. PAGE CONTENT ---
if not st.session_state.entered:
    # Landing Page
    st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">CareerMind AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">The Future of Career Engineering</p>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="feature-grid">
            <div class="service-card">
                <h3>🔍 Audit</h3>
                <p>Gap analysis between your profile and JD standards.</p>
            </div>
            <div class="service-card">
                <h3>✉️ Script</h3>
                <p>Architected cover letters with maximum impact.</p>
            </div>
            <div class="service-card">
                <h3>🎙️ Master</h3>
                <p>High-stakes interview simulation based on 2026 data.</p>
            </div>
            <div class="service-card">
                <h3>💰 Value</h3>
                <p>Market valuation using real-time benchmarks.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # الزر الآن أقرب للبطاقات
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("ENTER WORKSPACE", use_container_width=True):
            st.session_state.entered = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Dashboard Mode (المحتوى الداخلي)
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🧠 CareerMind</div>', unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("NAVIGATION", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        
        st.markdown("<br>" * 6, unsafe_allow_html=True)
        if st.button("🗑️ Exit Dashboard", use_container_width=True):
            st.session_state.entered = False
            st.rerun()

    # صفحات الخدمات الأصلية
    if page == "🔍 CV Matcher":
        st.title("Strategic Application Audit")
        col_l, col_r = st.columns(2, gap="large")
        with col_l: st.text_area("JD Content", height=300)
        with col_r: 
            st.file_uploader("Upload CV", type="pdf")
            st.button("Analyze")
