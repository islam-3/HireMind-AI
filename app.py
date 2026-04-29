import streamlit as st
import plotly.graph_objects as go
try:
    from groq import Groq
except ImportError:
    st.error("مكتبة Groq غير مثبتة. تأكد من وجودها في ملف requirements.txt")
    st.stop()
from PyPDF2 import PdfReader
import pandas as pd
import json

# --- 1. إعدادات الصفحة والتصميم الفخم ---
st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 50% 50%, #1a1f29 0%, #050505 100%); color: #e6edf3; }
    .hero-wrapper { text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 85vh; }
    .main-title { font-size: 5.5rem; font-weight: 900; background: linear-gradient(90deg, #58a6ff, #3fb950); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .sub-title { font-size: 1.2rem; color: #8b949e; letter-spacing: 6px; margin-bottom: 40px; }
    .feature-grid { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 50px; }
    .service-card { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 30px 20px; width: 250px; transition: 0.4s; }
    .service-card:hover { border-color: #58a6ff; transform: translateY(-10px); background: rgba(88, 166, 255, 0.05); }
    div.stButton > button { background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important; color: white !important; border-radius: 50px !important; padding: 12px 50px !important; font-weight: 700 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. التحقق من مفتاح الـ API (حماية من السواد) ---
if "GROQ_API_KEY" not in st.secrets:
    st.warning("⚠️ مفتاح GROQ_API_KEY مفقود من الأسرار (Secrets).")
    st.info("يرجى إضافته من Manage app -> Settings -> Secrets")
    st.stop()

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"فشل الاتصال بـ Groq: {e}")
    st.stop()

# --- 3. حالة الجلسة ---
if "entered" not in st.session_state:
    st.session_state.entered = False

# --- 4. واجهة المستخدم ---
if not st.session_state.entered:
    # الصفحة التي تحبها
    st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">CareerMind AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Architecting Your Professional Future</p>', unsafe_allow_html=True)
    st.markdown("""
        <div class="feature-grid">
            <div class="service-card"><h3>🔍 Audit</h3><p>CV & JD Alignment</p></div>
            <div class="service-card"><h3>✉️ Script</h3><p>Cover Letter Builder</p></div>
            <div class="service-card"><h3>🎙️ Master</h3><p>Interview Simulator</p></div>
            <div class="service-card"><h3>💰 Value</h3><p>Salary Estimation</p></div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Access Professional Suite"):
        st.session_state.entered = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # لوحة التحكم الأصلية
    with st.sidebar:
        st.markdown("<h2 style='color:#58a6ff; text-align:center;'>🧠 CareerMind</h2>", unsafe_allow_html=True)
        page = st.radio("Navigation", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        if st.button("Logout"):
            st.session_state.entered = False
            st.rerun()

    st.title(page)
    st.write(f"Welcome to the {page} section. System is Online.")
