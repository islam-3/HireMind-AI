import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json
import pandas as pd

# --- 1. SETTINGS & BRANDING (التصميم الفخم مع لوجو متوازن) ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    
    /* اللوجو بحجم وسط منطقي وفخم */
    .sidebar-logo { 
        font-size: 2.5rem !important; 
        font-weight: 800 !important; 
        color: #f0f6fc !important; 
        text-align: center !important; 
        margin-top: 20px !important;
        margin-bottom: 5px !important;
        letter-spacing: -1px !important;
        display: block !important;
    }
    
    .sidebar-subtitle {
        font-size: 0.9rem !important;
        color: #8b949e !important;
        text-align: center !important;
        margin-bottom: 30px !important;
        opacity: 0.8;
    }
    
    /* بطاقات النتائج */
    .edge-card { background-color: #1c2b1d; border-left: 5px solid #238636; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    .improve-card { background-color: #2d1a1a; border-left: 5px solid #da3633; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    
    /* تنسيق الأزرار */
    .stButton>button { 
        background-color: #30363d !important; 
        color: white !important; 
        border-radius: 8px; 
        border: 1px solid #484f58; 
        font-weight: bold; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALIZE GROQ ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key in Secrets.")
    st.stop()

# حفظ البيانات
if "history" not in st.session_state: st.session_state.history = []
if "current_result" not in st.session_state: st.session_state.current_result = None

# --- 3. FUNCTIONS ---
def get_groq_analysis(cv_text, jd_text):
    prompt = f"As a Career Coach, compare CV to JD. Return JSON: {{'score': float, 'strengths': [], 'weaknesses': [], 'summary': ''}}. CV: {cv_text[:6000]} JD: {jd_text[:2000]}"
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(completion.choices[0].message.content)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown('<h1 class="sidebar-logo">🧠 CareerMind</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-subtitle">Master Your Job Application</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    page = st.radio("Navigation", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep"])
    st.markdown("---")
    
    if st.session_state.history:
        st.markdown("**Top Versions:**")
        for entry in sorted(st.session_state.history, key=lambda x: x['Score'], reverse=True):
            st.write(f"⭐ {entry['Score']} - {entry['Name']}")
    
    if st.button("🗑️ Reset Sessions"):
        st.session_state.history = []
        st.session_state.current_result = None
        st.rerun()

# --- 5. PAGE: CV MATCHER ---
if page == "🔍 CV Matcher":
    st.title("Strategic Application Audit")
    c1, c2 = st.columns(2, gap="large")
    
    with c1:
        st.subheader("📋 Job Description")
        jd_input = st.text_area("Paste JD requirements...", height=250)
        
    with c2:
        st.subheader("👤 Your CV")
        v_name = st.text_input("Version Name:")
        file = st.file_uploader("Upload PDF:", type="pdf")
        
        if file and st.button("Analyze Match Score"):
            if jd_input and v_name:
                with st.spinner("Analyzing..."):
                    reader = PdfReader(file)
                    text = " ".join([p.extract_text() or "" for p in reader.pages])
                    res = get_groq_analysis(text, jd_input)
                    st.session_state.current_result = {"name": v_name, "data": res}
                    st.session_state.history.append({"Name": v_name, "Score": res['score']})
                    st.rerun()

    if st.session_state.current_result:
        res = st.session_state.current_result['data']
        st.markdown("---")
        r1, r2 = st.columns([1, 2])
        with r1:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=res['score'], gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "#8b949e"}}))
            fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
            st.plotly_chart(fig, use_container_width=True)
        with r2:
            st.info(res['summary'])
            sc1, sc2 = st.columns(2)
            with sc1:
                st.markdown("#### ✅ Competitive Edges")
                for s in res['strengths']: st.markdown(f'<div class="edge-card">{s}</div>', unsafe_allow_html=True)
            with sc2:
                st.markdown("#### ⚠️ Areas to Improve")
                for w in res['weaknesses']: st.markdown(f'<div class="improve-card">{w}</div>', unsafe_allow_html=True)

# أماكن الصفحات الأخرى
elif page == "✉️ Cover Letter":
    st.title("AI Cover Letter Generator")
    st.info("Feature integration in progress...")

elif page == "🎙️ Interview Prep":
    st.title("Interview Preparation")
    st.info("Preparing questions based on your profile...")
