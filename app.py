import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. التنسيق الحديدي (Fixed CSS) لمنع التخريب ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

st.markdown("""
    <style>
    /* ثبات الخلفية والقائمة الجانبية */
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; min-width: 250px !important; }
    
    /* منع تمدد أو تقلص العناصر */
    .main-header { font-size: 1.3rem; font-weight: 700; margin-bottom: 10px; height: 35px; }

    /* تثبيت الصندوق الأخضر مكانه ومنع تمدده */
    .audit-box {
        background-color: #143224; 
        color: #aff5b4;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #238636;
        margin-top: 35px;
        min-height: 110px;
        max-height: 110px; /* قفل الارتفاع لمنع تخريب الترتيب */
        overflow-y: auto;  /* إضافة سكرول داخلي لو النص طويل */
        font-size: 0.9rem;
    }

    /* تثبيت أحجام كروت النقاط (Competitive Edges) */
    .card-edge { 
        background-color: #162a45; padding: 12px; border-radius: 6px; 
        margin-bottom: 10px; color: #58a6ff; border: 1px solid #30363d; 
        min-height: 50px; display: flex; align-items: center; font-size: 0.9rem;
    }
    .card-improve { 
        background-color: #2b2d16; padding: 12px; border-radius: 6px; 
        margin-bottom: 10px; color: #d29922; border: 1px solid #30363d; 
        min-height: 50px; display: flex; align-items: center; font-size: 0.9rem;
    }

    /* سجل النتائج في الجنب */
    .history-item { padding: 8px; border-radius: 5px; background: #21262d; margin-bottom: 5px; border-left: 3px solid #238636; font-size: 0.85rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المنطق البرمجي (دون تغيير) ---
if "history" not in st.session_state: st.session_state.history = []
if "analysis_result" not in st.session_state: st.session_state.analysis_result = None
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def run_analysis(cv_text, jd_text):
    prompt = f"Analyze CV vs JD. Return ONLY JSON: {{'score': float, 'strengths': [], 'weaknesses': [], 'summary': ''}}. CV: {cv_text[:4000]} JD: {jd_text[:1500]}"
    chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], response_format={"type": "json_object"})
    return json.loads(chat.choices[0].message.content)

# --- 3. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown('<h1 style="text-align:center;">🧠 CareerMind</h1>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigation", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
    
    if st.session_state.history:
        st.markdown("<br><b>Top Versions:</b>", unsafe_allow_html=True)
        for item in reversed(st.session_state.history):
            st.markdown(f'<div class="history-item">⭐ {item["score"]}/10 - {item["name"]}</div>', unsafe_allow_html=True)
        if st.button("Reset Sessions"):
            st.session_state.history = []; st.session_state.analysis_result = None; st.rerun()

# --- 4. الصفحة الرئيسية (الهدف: ثبات التصميم) ---
if page == "🔍 CV Matcher":
    st.title("Strategic Application Audit")
    
    # شبكة المدخلات
    col_in1, col_in2 = st.columns(2, gap="large")
    with col_in1:
        st.markdown('<p class="main-header">📋 Job Description</p>', unsafe_allow_html=True)
        jd_data = st.text_area("JD", height=180, label_visibility="collapsed")
    with col_in2:
        st.markdown('<p class="main-header">👤 Your CV</p>', unsafe_allow_html=True)
        v_name = st.text_input("Version Name:", placeholder="e.g. Sales V1")
        pdf_file = st.file_uploader("Upload", type="pdf", label_visibility="collapsed")
        if st.button("Analyze Match Score", use_container_width=True):
            if pdf_file and jd_data:
                reader = PdfReader(pdf_file)
                cv_txt = " ".join([p.extract_text() for p in reader.pages])
                res = run_analysis(cv_txt, jd_data)
                st.session_state.analysis_result = {"name": v_name, "data": res}
                st.session_state.history.append({"name": v_name, "score": res['score']})
                st.rerun()

    # قسم النتائج (محمي ضد التخريب)
    if st.session_state.analysis_result:
        data = st.session_state.analysis_result['data']
        st.markdown("<br><hr>", unsafe_allow_html=True)
        
        # العداد والملخص الأخضر
        res_top1, res_top2 = st.columns([1, 2.5], gap="medium")
        with res_top1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=data['score'],
                number={'font': {'size': 32}, 'suffix': "/10"}, 
                gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "#238636"}}
            ))
            fig.update_layout(height=180, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, margin=dict(t=0, b=0, l=10, r=10))
            st.plotly_chart(fig, use_container_width=True)
        with res_top2:
            st.markdown(f'<div class="audit-box"><b>Audit for: {st.session_state.analysis_result["name"]}</b><br>{data["summary"]}</div>', unsafe_allow_html=True)

        # نقاط القوة والضعف ( Competitive Edges)
        st.markdown("<br>", unsafe_allow_html=True)
        res_bot1, res_bot2 = st.columns(2, gap="medium")
        with res_bot1:
            st.markdown("#### 🏆 Competitive Edges")
            for s in data['strengths']: 
                st.markdown(f'<div class="card-edge">{s}</div>', unsafe_allow_html=True)
        with res_bot2:
            st.markdown("#### 🛠️ Areas to Improve")
            for w in data['weaknesses']: 
                st.markdown(f'<div class="card-improve">{w}</div>', unsafe_allow_html=True)
