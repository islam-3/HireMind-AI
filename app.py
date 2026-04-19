import streamlit as st
import plotly.graph_objects as go
from google import genai
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
    .sidebar-subtitle { font-size: 0.85rem !important; color: #8b949e !important; text-align: center !important; margin-bottom: 20px !important; }
    [data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #30363d !important; }
    .strength-card { background-color: #1c2b1d; border-left: 5px solid #238636; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    .weakness-card { background-color: #2d1a1a; border-left: 5px solid #da3633; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    .stButton>button { background-color: #30363d !important; color: white !important; border: 1px solid #8b949e !important; width: 100%; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if "comparison_list" not in st.session_state: 
    st.session_state.comparison_list = []

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown('<p class="sidebar-logo">🧠 HireMind AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-subtitle">Enterprise Recruitment</p>', unsafe_allow_html=True)
    st.markdown("---")
    current_count = len(st.session_state.comparison_list)
    st.write(f"Candidates Analysed: **{current_count}**")
    if st.button("🗑️ Reset All"):
        st.session_state.comparison_list = []
        if "last_res" in st.session_state: del st.session_state.last_res
        st.rerun()

# --- 4. AI CORE LOGIC ---
# استخدمنا المفتاح الجديد الذي زودتني به
API_KEY = "AIzaSyBf7FTT2C68Fg072TB6iatnxrPHgxDBFWQ"
client = genai.Client(api_key=API_KEY)

def get_detailed_evaluation(cv_text, jd_text):
    # استخدام موديل مستقر جداً لتجنب خطأ 404
    model_id = "gemini-1.5-flash" 
    prompt = f"HR Expert Audit. Return JSON ONLY. Format: {{\"score\": float, \"strengths\": [], \"weaknesses\": [], \"summary\": \"\"}}. CV: {cv_text[:5000]} JD: {jd_text[:2000]}"
    
    try:
        response = client.models.generate_content(model=model_id, contents=prompt)
        text = response.text
        
        # استخراج JSON بذكاء
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            res = json.loads(match.group(0))
            if res.get('score', 0) > 10: res['score'] = res['score'] / 10
            return res
        else:
            raise ValueError("Invalid Response")
    except Exception as e:
        err_str = str(e)
        if "429" in err_str:
            return {"score": 0, "strengths": ["Server Busy"], "weaknesses": ["Please wait 30 seconds"], "summary": "Quota Limit."}
        return {"score": 0, "strengths": ["Audit Error"], "weaknesses": [f"Technical: {err_str[:30]}"], "summary": "System Update required."}

# --- 5. MAIN INTERFACE ---
st.title("Strategic Talent Analysis")
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("💼 Job Description")
    jd_input = st.text_area("Paste Requirements...", height=250, label_visibility="collapsed")

with col2:
    st.subheader("👤 Candidate CV")
    c_name = st.text_input("Name:")
    uploaded_file = st.file_uploader("Upload PDF:", type="pdf")
    
    if uploaded_file and st.button("Run AI Audit"):
        if not c_name or not jd_input:
            st.warning("Fill all info first.")
        else:
            with st.spinner("Processing..."):
                try:
                    reader = PdfReader(uploaded_file)
                    # تنظيف النص المستخرج
                    cv_text = ""
                    for page in reader.pages:
                        text = page.extract_text()
                        if text: cv_text += text + " "
                    
                    if not cv_text.strip():
                        st.error("Could not read text from PDF. Is it an image?")
                    else:
                        result = get_detailed_evaluation(cv_text, jd_input)
                        st.session_state.last_res = result
                        st.session_state.last_name = c_name
                        st.session_state.comparison_list.append({"Name": c_name, "Score": result['score']})
                        st.rerun()
                except Exception as e:
                    st.error(f"File Error: {str(e)[:50]}")

# --- 6. RESULTS ---
if "last_res" in st.session_state:
    res = st.session_state.last_res
    st.markdown("---")
    c_res1, c_res2 = st.columns([1, 2])
    with c_res1:
        fig = go.Figure(go.Indicator(mode="gauge+number", value=res['score'], gauge={'axis': {'range': [0, 10]}}))
        fig.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
        st.plotly_chart(fig, use_container_width=True)
    with c_res2:
        st.markdown(f"### Verdict: {st.session_state.last_name}")
        st.info(res.get('summary', 'Done.'))
    
    r1, r2 = st.columns(2)
    with r1:
        st.markdown("### ✅ Strengths")
        for s in res.get('strengths', []): st.markdown(f'<div class="strength-card">{s}</div>', unsafe_allow_html=True)
    with r2:
        st.markdown("### ⚠️ Gaps")
        for w in res.get('weaknesses', []): st.markdown(f'<div class="weakness-card">{w}</div>', unsafe_allow_html=True)

if st.session_state.comparison_list:
    st.markdown("---")
    st.table(pd.DataFrame(st.session_state.comparison_list))
