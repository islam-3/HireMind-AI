import streamlit as st
import plotly.graph_objects as go
import requests
import json
from PyPDF2 import PdfReader
import pandas as pd
import re

# --- 1. إعدادات الصفحة والتصميم الفاخر ---
st.set_page_config(page_title="HireMind AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; min-width: 250px; }
    .sidebar-logo { font-size: 1.5rem; font-weight: 800; color: #f0f6fc; text-align: center; margin-bottom: 5px; }
    .strength-card { background-color: #1c2b1d; border-left: 5px solid #238636; padding: 12px; border-radius: 5px; margin-bottom: 10px; }
    .weakness-card { background-color: #2d1a1a; border-left: 5px solid #da3633; padding: 12px; border-radius: 5px; margin-bottom: 10px; }
    .stButton>button { background-color: #30363d !important; color: white !important; width: 100%; border-radius: 8px; border: 1px solid #8b949e; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة الجلسة (لإصلاح القائمة الجانبية) ---
if "comparison_list" not in st.session_state:
    st.session_state.comparison_list = []
if "last_res" not in st.session_state:
    st.session_state.last_res = None

# --- 3. وظيفة الاتصال المباشر بجوجل (لتجنب خطأ 404) ---
def get_ai_analysis(cv_text, jd_text):
    api_key = "AIzaSyBf7FTT2C68Fg072TB6iatnxrPHgxDBFWQ"
    # هذا الرابط هو الرابط الرسمي المباشر
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Analyze CV vs Job Description. Return ONLY JSON. Format: {{\"score\": 7.5, \"strengths\": [\"point\"], \"weaknesses\": [\"point\"], \"summary\": \"text\"}}. CV: {cv_text[:5000]} JD: {jd_text[:2000]}"
            }]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if response.status_code == 200:
            raw_text = data['candidates'][0]['content']['parts'][0]['text']
            # استخراج الـ JSON من النص
            match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            return json.loads(match.group(0))
        else:
            return {"score": 0, "strengths": ["API Error"], "weaknesses": [f"Status: {response.status_code}"], "summary": "Connection Issue."}
    except Exception as e:
        return {"score": 0, "strengths": ["Error"], "weaknesses": [str(e)[:30]], "summary": "System Issue."}

# --- 4. القائمة الجانبية ثابتة ---
with st.sidebar:
    st.markdown('<p class="sidebar-logo">🧠 HireMind AI</p>', unsafe_allow_html=True)
    st.markdown("---")
    st.write(f"Candidates Analysed: **{len(st.session_state.comparison_list)}**")
    if st.button("🗑️ Reset Sessions"):
        st.session_state.comparison_list = []
        st.session_state.last_res = None
        st.rerun()

# --- 5. الواجهة الرئيسية ---
st.title("Strategic Talent Analysis")
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.subheader("💼 Job Description")
    jd_input = st.text_area("Paste here...", height=250, label_visibility="collapsed")

with col2:
    st.subheader("👤 Candidate CV")
    c_name = st.text_input("Name:")
    uploaded_file = st.file_uploader("Upload PDF:", type="pdf")
    
    if uploaded_file and st.button("Run Strategic Audit"):
        if c_name and jd_input:
            with st.spinner("Processing..."):
                reader = PdfReader(uploaded_file)
                text = " ".join([p.extract_text() or "" for p in reader.pages])
                result = get_ai_analysis(text, jd_input)
                st.session_state.last_res = result
                st.session_state.last_name = c_name
                st.session_state.comparison_list.append({"Name": c_name, "Score": result.get('score', 0)})
                st.rerun()

# --- 6. عرض النتائج ---
if st.session_state.last_res:
    res = st.session_state.last_res
    st.markdown("---")
    r1, r2 = st.columns([1, 2])
    with r1:
        fig = go.Figure(go.Indicator(mode="gauge+number", value=res.get('score', 0), gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "#8b949e"}}))
        fig.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
        st.plotly_chart(fig, use_container_width=True)
    with r2:
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
    st.subheader("📊 Ranking")
    st.table(pd.DataFrame(st.session_state.comparison_list))
