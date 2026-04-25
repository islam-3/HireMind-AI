import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. UI CONFIGURATION & FULL SCREEN STYLING ---
st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Main Theme */
    .stApp { background-color: #0d1117; color: #e6edf3; }
    
    /* Full Screen Landing Page Container */
    .landing-container {
        height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        background: radial-gradient(circle at center, #161b22 0%, #0d1117 100%);
        margin: -75px -50px; /* لإلغاء هوامش ستريم ليت الافتراضية */
        padding: 50px;
    }
    
    .hero-title { font-size: 4rem; font-weight: 800; color: #58a6ff; margin-bottom: 10px; }
    .hero-subtitle { font-size: 1.5rem; color: #8b949e; margin-bottom: 40px; max-width: 800px; }
    
    /* Feature Cards Grid */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        width: 100%;
        max-width: 1100px;
        margin-bottom: 50px;
    }
    
    .feature-card {
        background: rgba(22, 27, 34, 0.7);
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 20px;
        transition: 0.3s;
    }
    .feature-card:hover { border-color: #58a6ff; transform: translateY(-5px); }
    .feature-card h3 { color: #58a6ff; margin-bottom: 10px; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid #30363d; }
    .sidebar-logo { display: flex; flex-direction: column; align-items: center; text-align: center; font-size: 2.2rem !important; font-weight: bold; color: #58a6ff; padding-top: 20px; }
    
    /* Buttons */
    div.stButton > button {
        background-color: #238636 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.5rem 2rem !important;
        font-size: 1.2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE LOGIC & SESSION STATE ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# التحقق مما إذا كان المستخدم قد دخل للموقع أم لا يزال في صفحة الترحيب
if "entered" not in st.session_state:
    st.session_state.entered = False

for key in ["history", "last_res", "gen_cl", "salary_data", "interview_q"]:
    if key not in st.session_state:
        st.session_state[key] = [] if "history" in key or "interview_q" in key else None

def read_pdf(file):
    try:
        reader = PdfReader(file)
        return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
    except: return ""

# --- 3. CONDITION: SHOW LANDING OR MAIN APP ---

if not st.session_state.entered:
    # --- صفحة الترحيب كاملة الشاشة ---
    st.markdown("""
        <div class="landing-container">
            <div class="hero-title">🧠 CareerMind AI</div>
            <div class="hero-subtitle">The ultimate intelligence suite for modern job seekers. Audit your CV, generate letters, and master your interview in one place.</div>
            <div class="grid-container">
                <div class="feature-card"><h3>🔍 CV Matcher</h3><p>Precision gap analysis against any JD.</p></div>
                <div class="feature-card"><h3>✉️ Cover Letter</h3><p>AI-crafted letters that sell your skills.</p></div>
                <div class="feature-card"><h3>🎙️ Interview Prep</h3><p>Personalized mock interview simulator.</p></div>
                <div class="feature-card"><h3>💰 Salary Insight</h3><p>Real-time 2026 market value tracking.</p></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # وضع الزر في المنتصف
    col_c1, col_c2, col_c3 = st.columns([1, 1, 1])
    with col_c2:
        if st.button("🚀 Enter Dashboard", use_container_width=True):
            st.session_state.entered = True
            st.rerun()

else:
    # --- الموقع الأصلي والخدمات ---
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🧠 CareerMind</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #8b949e;'>2026 Professional Suite</p>", unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("NAVIGATION", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        
        st.markdown("<br>" * 5, unsafe_allow_html=True)
        if st.button("🗑️ Reset All", use_container_width=True):
            st.session_state.entered = False # للعودة لصفحة البداية
            for key in ["history", "last_res", "gen_cl", "salary_data", "interview_q"]:
                st.session_state[key] = [] if "history" in key or "interview_q" in key else None
            st.rerun()

    # محتوى الصفحات
    if page == "🔍 CV Matcher":
        st.title("Strategic Application Audit")
        # ... (نفس كود الماتشر السابق)
        col_l, col_r = st.columns(2, gap="large")
        with col_l:
            jd_input = st.text_area("JD Content", height=250, placeholder="Paste JD here...")
        with col_r:
            v_name = st.text_input("Label")
            pdf_file = st.file_uploader("Upload CV", type="pdf")
            if st.button("Analyze Match Score", use_container_width=True):
                # logic here
                pass

    elif page == "✉️ Cover Letter":
        st.title("AI Cover Letter Architect")
        # ... (كود الكوفر ليتر)
        pass

    elif page == "🎙️ Interview Prep":
        st.title("AI Interview Simulator")
        # ... (كود المقابلة)
        pass

    elif page == "💰 Salary Insight":
        st.title("Market Value Estimator")
        # ... (كود الرواتب الواقعي 2026)
        pass
