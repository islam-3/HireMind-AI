import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. UI CONFIGURATION & HIGH-END STYLING ---
st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 50% 50%, #1a1f29 0%, #050505 100%); color: #e6edf3; }
    
    /* Landing Page Styling */
    .hero-wrapper { text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 90vh; }
    .main-title { font-size: 5rem; font-weight: 900; background: linear-gradient(90deg, #58a6ff, #3fb950); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; }
    .sub-title { font-size: 1.1rem; color: #8b949e; margin-bottom: 40px; letter-spacing: 5px; }
    
    /* Cards */
    .feature-grid { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 40px; }
    .service-card { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 30px 20px; width: 240px; transition: 0.4s; }
    .service-card:hover { border-color: #58a6ff; transform: translateY(-10px); }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid #30363d; }
    .sidebar-logo { display: flex; flex-direction: column; align-items: center; font-size: 2.2rem !important; font-weight: bold; color: #58a6ff; padding-top: 25px; }
    
    /* Buttons */
    div.stButton > button { background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important; color: white !important; border-radius: 50px !important; padding: 12px 50px !important; font-weight: 600 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if "entered" not in st.session_state:
    st.session_state.entered = False

# --- 3. CORE LOGIC ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 4. NAVIGATION RENDERING ---
if not st.session_state.entered:
    # LANDING PAGE (المقدمة الفخمة)
    st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">CareerMind AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">The Future of Career Engineering</p>', unsafe_allow_html=True)
    st.markdown("""
        <div class="feature-grid">
            <div class="service-card"><h3>🔍 Audit</h3><p>Gap analysis between profile and JD.</p></div>
            <div class="service-card"><h3>✉️ Script</h3><p>High impact cover letters.</p></div>
            <div class="service-card"><h3>🎙️ Master</h3><p>2026 Interview simulation.</p></div>
            <div class="service-card"><h3>💰 Value</h3><p>Real-time market valuation.</p></div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("ENTER WORKSPACE"):
        st.session_state.entered = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # DASHBOARD (الموقع الأصلي)
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🧠 CareerMind</div>', unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("NAVIGATION", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        st.markdown("<br>" * 6, unsafe_allow_html=True)
        if st.button("🗑️ Exit Dashboard", use_container_width=True):
            st.session_state.entered = False
            st.rerun()

    if page == "🔍 CV Matcher":
        st.title("Strategic Application Audit")
        col_l, col_r = st.columns(2, gap="large")
        with col_l: st.text_area("Job Requirements", height=300)
        with col_r: 
            st.file_uploader("Upload CV", type="pdf")
            st.button("Analyze Match Score")
    
    elif page == "💰 Salary Insight":
        st.title("Market Value Estimator")
        # العودة لتنسيق الليرة التركية والعملات المحلية
        st.info("Calculating 2026 local market trends...")
