import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. التنسيق المستقر (Stable UI) ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    /* تنسيق النتائج */
    .summary-box { background-color: #143224; color: #aff5b4; padding: 15px; border-radius: 8px; border: 1px solid #238636; margin-top: 20px; }
    .edge-card { background-color: #162a45; padding: 10px; border-radius: 6px; margin-bottom: 8px; border: 1px solid #30363d; color: #58a6ff; }
    .improve-card { background-color: #2b2d16; padding: 10px; border-radius: 6px; margin-bottom: 8px; border: 1px solid #30363d; color: #d29922; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المنطق ---
if "history" not in st.session_state: st.session_state.history = []
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def read_pdf(file):
    reader = PdfReader(file)
    return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

# --- 3. القائمة الجانبية ---
with st.sidebar:
    st.markdown("## 🧠 CareerMind")
    st.markdown("---")
    page = st.radio("Navigation", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
    
    if st.session_state.history:
        st.markdown("<br><b>Recent Audits:</b>", unsafe_allow_html=True)
        for item in reversed(st.session_state.history[-3:]):
            st.info(f"⭐ {item['score']}/10 - {item['name']}")
        if st.button("Reset Sessions"):
            st.session_state.history = []; st.rerun()

# --- 4. صفحة CV Matcher (مرتبة أفقياً) ---
if page == "🔍 CV Matcher":
    st.title("Strategic Application Audit")
    
    # قسم المدخلات: جنباً إلى جنب
    col_in1, col_in2 = st.columns(2, gap="medium")
    with col_in1:
        st.subheader("📋 Job Description")
        jd_input = st.text_area("Paste JD here", height=250, label_visibility="collapsed")
    with col_in2:
        st.subheader("👤 Your Profile")
        v_name = st.text_input("Version Name (e.g. Islam V1)")
        pdf_file = st.file_uploader("Upload CV (PDF)", type="pdf")
        if st.button("Analyze Now", use_container_width=True, type="primary"):
            if pdf_file and jd_input:
                with st.spinner("Analyzing..."):
                    cv_txt = read_pdf(pdf_file)
                    p = f"Analyze CV vs JD. Return JSON: {{'score': float, 'strengths': [], 'weaknesses': [], 'summary': ''}}. CV: {cv_txt[:3500]} JD: {jd_input[:1500]}"
                    res = json.loads(client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": p}], response_format={"type": "json_object"}).choices[0].message.content)
                    st.session_state.last_res = res
                    st.session_state.history.append({"name": v_name, "score": res['score']})
                    st.rerun()

    # عرض النتائج: مقسمة بوضوح
    if "last_res" in st.session_state:
        st.markdown("---")
        data = st.session_state.last_res
        res_col1, res_col2 = st.columns([1, 2])
        
        with res_col1:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=data['score'], number={'suffix': "/10"}, gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "#238636"}}))
            fig.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
            st.plotly_chart(fig, use_container_width=True)
            
        with res_col2:
            st.markdown(f'<div class="summary-box"><b>Expert Summary:</b><br>{data["summary"]}</div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        list_col1, list_col2 = st.columns(2)
        with list_col1:
            st.markdown("### 🏆 Strengths")
            for s in data['strengths']: st.markdown(f'<div class="edge-card">✓ {s}</div>', unsafe_allow_html=True)
        with list_col2:
            st.markdown("### 🛠️ Improvements")
            for w in data['weaknesses']: st.markdown(f'<div class="improve-card">! {w}</div>', unsafe_allow_html=True)

# --- 5. صفحة Cover Letter (بسيطة ومنظمة) ---
elif page == "✉️ Cover Letter":
    st.title("AI Cover Letter Architect")
    cl_col1, cl_col2 = st.columns(2, gap="large")
    with cl_col1:
        cl_jd = st.text_area("Job Requirements", height=200)
        cl_pdf = st.file_uploader("Upload CV", type="pdf")
    with cl_col2:
        st.markdown("<br><br>", unsafe_allow_html=True) # موازنة المسافة
        if st.button("Generate Letter", use_container_width=True, type="primary"):
            cv_text = read_pdf(cl_pdf) if cl_pdf else "Professional background"
            p = f"Write a cover letter for this JD: {cl_jd[:1000]} and CV: {cv_text[:2500]}"
            st.session_state.gen_cl = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": p}]).choices[0].message.content
            st.rerun()

    if "gen_cl" in st.session_state:
        st.markdown("---")
        st.text_area("Draft:", value=st.session_state.gen_cl, height=400)

# --- 6. صفحة Interview Prep ---
elif page == "🎙️ Interview Prep":
    st.title("Interview Coach")
    int_jd = st.text_area("Paste Job Description to generate questions")
    if st.button("Get Questions"):
        p = f"Generate 5 interview questions for: {int_jd[:1000]}"
        st.write(client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": p}]).choices[0].message.content)
