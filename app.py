import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. التنسيق الحديدي (Fixed CSS) لضمان ثبات التصميم ---
st.set_page_config(page_title="CareerMind AI", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .audit-box { background-color: #143224; color: #aff5b4; padding: 15px; border-radius: 8px; border: 1px solid #238636; margin-top: 35px; min-height: 110px; max-height: 110px; overflow-y: auto; font-size: 0.9rem; }
    .card-edge { background-color: #162a45; padding: 12px; border-radius: 6px; margin-bottom: 10px; color: #58a6ff; border: 1px solid #30363d; min-height: 50px; display: flex; align-items: center; font-size: 0.9rem; }
    .card-improve { background-color: #2b2d16; padding: 12px; border-radius: 6px; margin-bottom: 10px; color: #d29922; border: 1px solid #30363d; min-height: 50px; display: flex; align-items: center; font-size: 0.9rem; }
    .history-item { padding: 10px; border-radius: 5px; background: #21262d; margin-bottom: 5px; border-left: 4px solid #238636; font-size: 0.85rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة الجلسة والمنطق ---
if "history" not in st.session_state: st.session_state.history = []
if "analysis_result" not in st.session_state: st.session_state.analysis_result = None
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def run_analysis(cv_text, jd_text):
    # برومبت عادل لضمان نتائج منطقية غير محطمة
    prompt = f"""
    You are a FAIR and Professional Recruiter. Evaluate the CV against the JD.
    CRITICAL: Avoid extremely low scores (like 0.8) if basic skills are present. Use a realistic 10-point scale.
    Return ONLY JSON: {{ "score": float, "strengths": [], "weaknesses": [], "summary": "" }}
    CV: {cv_text[:5000]} | JD: {jd_text[:1500]}
    """
    chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], response_format={"type": "json_object"})
    return json.loads(chat.choices[0].message.content)

# --- 3. القائمة الجانبية (Sidebar) مع زر الريسيت ---
with st.sidebar:
    st.markdown('<h1 style="text-align:center;">🧠 CareerMind</h1>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigation", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
    
    # قسم سجل النسخ وزر الريسيت
    if st.session_state.history:
        st.markdown("<br><b>Top Versions:</b>", unsafe_allow_html=True)
        for item in reversed(st.session_state.history):
            st.markdown(f'<div class="history-item">⭐ {item["score"]}/10 - {item["name"]}</div>', unsafe_allow_html=True)
        
        # زر الريسيت لمسح كافة البيانات والجلسات
        if st.button("Reset Sessions", use_container_width=True):
            st.session_state.history = []
            st.session_state.analysis_result = None
            if "generated_cl" in st.session_state: del st.session_state.generated_cl
            if "salary_data" in st.session_state: del st.session_state.salary_data
            st.rerun()

# --- 4. الصفحة الرئيسية ---
if page == "🔍 CV Matcher":
    st.title("Strategic Application Audit")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("### 📋 Job Description")
        jd_input = st.text_area("JD", height=200, label_visibility="collapsed")
    with col2:
        st.markdown("### 👤 Your CV")
        v_name = st.text_input("Version Name:", placeholder="e.g. Sales Role")
        pdf_file = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")
        if st.button("Analyze Match Score", use_container_width=True):
            if pdf_file and jd_input:
                with st.spinner("Analyzing..."):
                    reader = PdfReader(pdf_file)
                    cv_txt = " ".join([p.extract_text() for p in reader.pages])
                    res = run_analysis(cv_txt, jd_input)
                    st.session_state.analysis_result = {"name": v_name, "data": res}
                    st.session_state.history.append({"name": v_name, "score": res['score']})
                    st.rerun()

    # عرض النتائج الثابتة
    if st.session_state.analysis_result:
        data = st.session_state.analysis_result['data']
        st.markdown("<br><hr>", unsafe_allow_html=True)
        r1, r2 = st.columns([1, 2.5], gap="medium")
        with r1:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=data['score'], number={'font': {'size': 32}, 'suffix': "/10"}, gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "#238636"}}))
            fig.update_layout(height=180, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, margin=dict(t=0, b=0, l=10, r=10))
            st.plotly_chart(fig, use_container_width=True)
        with r2:
            st.markdown(f'<div class="audit-box"><b>Audit for: {st.session_state.analysis_result["name"]}</b><br>{data["summary"]}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        b1, b2 = st.columns(2, gap="medium")
        with b1:
            st.markdown("#### 🏆 Competitive Edges")
            for s in data['strengths']: st.markdown(f'<div class="card-edge">{s}</div>', unsafe_allow_html=True)
        with b2:
            st.markdown("#### 🛠️ Areas to Improve")
            for w in data['weaknesses']: st.markdown(f'<div class="card-improve">{w}</div>', unsafe_allow_html=True)

# الصفحات الأخرى (Cover Letter / Salary) تضاف هنا بنفس النمط...
