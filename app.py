import streamlit as st
from groq import Groq
import plotly.graph_objects as go
from PyPDF2 import PdfReader

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

# 2. التأكد من وجود مفتاح API في Secrets
if "GROQ_API_KEY" not in st.secrets:
    st.error("الرجاء إضافة GROQ_API_KEY في إعدادات Secrets")
    st.stop()

# 3. تهيئة حالة الجلسة
if "entered" not in st.session_state:
    st.session_state.entered = False

# 4. التصميم (CSS)
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 50% 50%, #1a1f29 0%, #050505 100%); color: #e6edf3; }
    .hero-wrapper { text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 80vh; }
    .main-title { font-size: 5rem; font-weight: 900; background: linear-gradient(90deg, #58a6ff, #3fb950); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .feature-grid { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin: 40px 0; }
    .service-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 25px; width: 230px; text-align: center; }
    div.stButton > button { background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important; color: white !important; border-radius: 50px !important; padding: 10px 40px !important; }
    </style>
    """, unsafe_allow_html=True)

# 5. منطق العرض
if not st.session_state.entered:
    st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">CareerMind AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#8b949e; letter-spacing:4px;">THE FUTURE OF CAREER ENGINEERING</p>', unsafe_allow_html=True)
    st.markdown("""
        <div class="feature-grid">
            <div class="service-card"><h3 style="color:#58a6ff;">Audit</h3><p style="font-size:0.8rem; color:#8b949e;">CV analysis.</p></div>
            <div class="service-card"><h3 style="color:#58a6ff;">Script</h3><p style="font-size:0.8rem; color:#8b949e;">Cover letters.</p></div>
            <div class="service-card"><h3 style="color:#58a6ff;">Master</h3><p style="font-size:0.8rem; color:#8b949e;">Interviews.</p></div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("ENTER WORKSPACE", use_container_width=True):
            st.session_state.entered = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # محتوى لوحة التحكم الفعلي
    st.sidebar.markdown("<h2 style='text-align:center; color:#58a6ff;'>🧠 CareerMind</h2>", unsafe_allow_html=True)
    page = st.sidebar.radio("Navigation", ["🔍 Audit", "🎙️ Interview"])
    
    if st.sidebar.button("Log Out"):
        st.session_state.entered = False
        st.rerun()
    
    st.title(f"Professional {page}")
    st.info("System is ready and connected to Groq Cloud.")
