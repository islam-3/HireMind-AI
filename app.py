import streamlit as st
import plotly.graph_objects as go
import google.generativeai as pal_genai # المكتبة المستقرة
from PyPDF2 import PdfReader
import json
import pandas as pd
import re

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="HireMind AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117 !important; color: #ffffff !important; }
    .sidebar-logo { font-size: 1.5rem !important; font-weight: 800 !important; color: #f0f6fc !important; text-align: center !important; margin-bottom: 0px !important; }
    [data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #30363d !important; }
    .strength-card { background-color: #1c2b1d; border-left: 5px solid #238636; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    .weakness-card { background-color: #2d1a1a; border-left: 5px solid #da3633; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    .stButton>button { background-color: #30363d !important; color: white !important; border: 1px solid #8b949e !important; width: 100%; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AI CORE LOGIC (المكتبة المستقرة) ---
API_KEY = "AIzaSyBf7FTT2C68Fg072TB6iatnxrPHgxDBFWQ"
pal_genai.configure(api_key=API_KEY)

def get_detailed_evaluation(cv_text, jd_text):
    # استخدام الموديل بنظام المكتبة القديمة المستقرة
    model = pal_genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Audit CV vs JD. Return ONLY JSON: {{\"score\": float, \"strengths\": [], \"weaknesses\": [], \"summary\": \"\"}}. CV: {cv_text[:4000]} JD: {jd_text[:1500]}"
    
    try:
        response = model.generate_content(prompt)
        text = response.text
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise ValueError("Parse Error")
    except Exception as e:
        err = str(e)
        if "429" in err: return {"score": 0, "strengths": ["Busy"], "weaknesses": ["Wait 30s"], "summary": "Quota Limit."}
        return {"score": 0, "strengths": ["Error"], "weaknesses": [f"Tech: {err[:20]}"], "summary": "System Issue."}

# --- 3. SESSION STATE ---
if "comparison_list" not in st.session_state: st.session_state.comparison_list = []

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown('<p class="sidebar-logo">🧠 HireMind AI</p>', unsafe_allow_html=True)
    st.write(f"Processed: **{len(st.session_state.comparison_list)}**")
    if st.button("🗑️ Reset All"):
        st.session_state.comparison_list = []
        if "last_res" in st.session_state: del st.session_state.last_res
        st.rerun()

# --- 5. MAIN INTERFACE ---
st.title("Strategic Talent Analysis")
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("💼 Job Description")
    jd_input = st.text_area("Requirements...", height=250, label_visibility="collapsed")

with col2:
    st.subheader("👤 Candidate CV")
    c_name = st.text_input("Name:")
    uploaded_file = st.file_uploader("Upload PDF:", type="pdf")
    
    if uploaded_file and st.button("Run AI Audit"):
        if not c_name or not jd_input:
            st.warning("Complete fields.")
        else:
            with st.spinner("Analyzing..."):
                try:
                    reader = PdfReader(uploaded_file)
                    cv_text = " ".join([p.extract_text() or "" for p in reader.pages])
                    result = get_detailed_evaluation(cv_text, jd_input)
                    st.session_state.last_res = result
                    st.session_state.last_name = c_name
                    st.session_state.comparison_list.append({"Name": c_name, "Score": result.get('score', 0)})
                    st.rerun()
                except: st.error("PDF Error")

# --- 6. RESULTS ---
if "last_res" in st.session_state:
    res = st.session_state.last_res
    st.markdown("---")
    r_col1, r_col2 = st.columns([1, 2])
    with r_col1:
        fig = go.Figure(go.Indicator(mode="gauge+number", value=res.get('score', 0), gauge={'axis': {'range': [0, 10]}}))
        fig.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
        st.plotly_chart(fig, use_container_width=True)
    with r_col2:
        st.markdown(f"### Verdict: {st.session_state.last_name}")
        st.info(res.get('summary', ''))
    
    s1, s2 = st.columns(2)
    with s1:
        st.markdown("### ✅ Strengths")
        for s in res.get('strengths', []): st.markdown(f'<div class="strength-card">{s}</div>', unsafe_allow_html=True)
    with s2:
        st.markdown("### ⚠️ Gaps")
        for w in res.get('weaknesses', []): st.markdown(f'<div class="weakness-card">{w}</div>', unsafe_allow_html=True)

if st.session_state.comparison_list:
    st.markdown("---")
    st.table(pd.DataFrame(st.session_state.comparison_list))
