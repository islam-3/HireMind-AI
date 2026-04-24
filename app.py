import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. UI CONFIGURATION ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    [data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid #30363d; }
    
    /* Logo & Sidebar Centering */
    .sidebar-logo { display: flex; flex-direction: column; align-items: center; text-align: center; font-size: 2.2rem !important; font-weight: bold; color: #58a6ff; padding-top: 20px; }
    .sidebar-subtext { text-align: center; color: #8b949e; font-size: 0.9rem; margin-bottom: 20px; }
    
    /* Landing Page Cards */
    .feature-card {
        background: rgba(22, 27, 34, 0.7);
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        transition: 0.3s;
        height: 100%;
    }
    .feature-card:hover { border-color: #58a6ff; transform: translateY(-5px); }
    
    /* Buttons */
    div.stButton > button { background-color: #238636 !important; color: white !important; border-radius: 8px !important; font-weight: bold; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE LOGIC ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

for key in ["history", "last_res", "gen_cl", "salary_data", "interview_q"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key in ["history", "interview_q"] else None

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🧠 CareerMind</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtext">Master Your Job Application</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # أضفنا خيار "🏠 Home" ليكون الواجهة الأولى
    page = st.radio("NAVIGATION", ["🏠 Home", "🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
    
    st.markdown("<br>" * 4, unsafe_allow_html=True) 
    if st.button("🗑️ Reset All Progress", use_container_width=True):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- 4. HOME / LANDING PAGE ---
if page == "🏠 Home":
    st.markdown("<h1 style='text-align: center; color: #58a6ff;'>Elevate Your Professional Journey</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #8b949e;'>Precision AI tools designed to help you land your dream job in 2026.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    with col1:
        st.markdown("""<div class="feature-card"><h3>🔍 CV Matcher</h3><p>Audit your resume against any job description with real-time scoring.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="feature-card"><h3>✉️ Cover Letter</h3><p>Generate high-impact, tailored letters that capture recruiter attention.</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="feature-card"><h3>🎙️ Interview Prep</h3><p>Practice with AI-generated questions based on your specific profile.</p></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="feature-card"><h3>💰 Salary Insight</h3><p>Get realistic 2026 market value estimates for any role worldwide.</p></div>""", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚀 Start Your Application Audit", use_container_width=True):
        # توجيه المستخدم لأول أداة عند الضغط على الزر
        st.info("Select a tool from the sidebar to begin!")

# --- باقي الصفحات (نفس الكود السابق بدون تغيير) ---
elif page == "🔍 CV Matcher":
    st.title("Strategic Application Audit")
    # ... بقية كود الـ Matcher ...

elif page == "✉️ Cover Letter":
    st.title("AI Cover Letter Architect")
    # ... بقية كود الـ Letter ...

elif page == "🎙️ Interview Prep":
    st.title("AI Interview Simulator")
    # ... بقية كود الـ Prep ...

elif page == "💰 Salary Insight":
    st.title("Market Value Estimator")
    # ... بقية كود الـ Salary ...
