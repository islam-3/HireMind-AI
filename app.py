import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. UI CONFIGURATION & PROFESSIONAL STYLING ---
st.set_page_config(page_title="CareerMind AI | Premium Suite", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Global Theme & Deep Background */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a1f29 0%, #0d1117 100%);
        color: #e6edf3;
    }

    /* Full Screen Landing Container */
    .landing-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 90vh;
        padding: 20px;
    }

    .hero-title {
        font-size: 5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #58a6ff 0%, #3fb950 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        letter-spacing: -2px;
    }

    .hero-tagline {
        font-size: 1.4rem;
        color: #8b949e;
        margin-bottom: 50px;
        font-weight: 300;
        letter-spacing: 1px;
    }

    /* Premium Glassmorphism Cards */
    .glass-card {
        background: rgba(22, 27, 34, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 100%;
    }

    .glass-card:hover {
        border-color: #58a6ff;
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        background: rgba(22, 27, 34, 0.6);
    }

    .glass-card h3 { color: #58a6ff; font-size: 1.5rem; margin-bottom: 15px; }
    .glass-card p { color: #8b949e; font-size: 0.95rem; line-height: 1.6; }

    /* Centered Dashboard Button */
    .enter-btn-container { margin-top: 60px; width: 100%; display: flex; justify-content: center; }
    
    div.stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        color: white !important;
        border: none !important;
        padding: 15px 50px !important;
        font-size: 1.3rem !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        box-shadow: 0 10px 20px rgba(35, 134, 54, 0.2) !important;
        transition: 0.3s !important;
    }
    
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 30px rgba(35, 134, 54, 0.4) !important;
    }

    /* Sidebar Fixes */
    [data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid #30363d; }
    .sidebar-logo { display: flex; flex-direction: column; align-items: center; text-align: center; font-size: 2.2rem !important; font-weight: bold; color: #58a6ff; padding-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE LOGIC & NAVIGATION STATE ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "entered" not in st.session_state:
    st.session_state.entered = False

def read_pdf(file):
    try:
        reader = PdfReader(file)
        return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
    except: return ""

# --- 3. PAGE RENDERING ---

if not st.session_state.entered:
    # --- PREMIER LANDING PAGE ---
    st.markdown('<div class="landing-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">CareerMind AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-tagline">Architecting Your Professional Future with Intelligence</div>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4, gap="medium")
    with c1: st.markdown('<div class="glass-card"><h3>🔍 CV Matcher</h3><p>Strategic alignment analysis between your profile and target roles.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="glass-card"><h3>✉️ Cover Letter</h3><p>Precision-crafted narratives designed to engage recruiters.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="glass-card"><h3>🎙️ Interview Prep</h3><p>Context-aware simulation to master high-stakes conversations.</p></div>', unsafe_allow_html=True)
    with c4: st.markdown('<div class="glass-card"><h3>💰 Salary Insight</h3><p>Dynamic 2026 market valuation based on global benchmarks.</p></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="enter-btn-container">', unsafe_allow_html=True)
    if st.button("Access Professional Suite"):
        st.session_state.entered = True
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

else:
    # --- DASHBOARD MODE ---
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🧠 CareerMind</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #8b949e;'>Master Your Career Path</p>", unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("NAVIGATION", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        
        st.markdown("<br>" * 5, unsafe_allow_html=True)
        if st.button("🗑️ Exit to Main", use_container_width=True):
            st.session_state.entered = False
            st.rerun()

    # محتوى الصفحات الأصلي (كما في النسخ المستقرة السابقة)
    if page == "🔍 CV Matcher":
        st.title("Strategic Application Audit")
        col_l, col_r = st.columns(2, gap="large")
        with col_l:
            jd_input = st.text_area("Job Requirements", height=300, placeholder="Paste target JD...")
        with col_r:
            v_label = st.text_input("Analysis Label (e.g. Google - SE)")
            pdf_f = st.file_uploader("Upload CV (PDF)", type="pdf")
            if st.button("Run Audit", use_container_width=True):
                # التكملة هنا...
                pass
    
    # ... بقية الصفحات بنفس المنطق ...
