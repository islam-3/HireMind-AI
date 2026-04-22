import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. نظام التنسيق الحديث (Modern Dashboard UI) ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

st.markdown("""
    <style>
    /* تحسين الخلفية والخطوط */
    .stApp { background-color: #0d1117; color: #e6edf3; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* تنسيق الحاويات (Cards) */
    .section-card {
        background-color: #161b22;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* الصندوق الأخضر للملخص */
    .summary-box {
        background-color: #143224;
        color: #aff5b4;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #238636;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* عناوين الأقسام */
    .header-text { color: #58a6ff; font-weight: 600; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
    
    /* بطاقات النقاط الجمالية */
    .badge-positive { background: #1f2d23; color: #3fb950; padding: 10px; border-radius: 6px; margin-bottom: 8px; border: 1px solid #238636; }
    .badge-negative { background: #2d2323; color: #f85149; padding: 10px; border-radius: 6px; margin-bottom: 8px; border: 1px solid #da3633; }
    
    /* تحسين القائمة الجانبية */
    [data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المنطق البرمجي الأساسي ---
if "history" not in st.session_state: st.session_state.history = []
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def read_pdf(file):
    reader = PdfReader(file)
    return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

def get_ai_json(prompt):
    chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], response_format={"type": "json_object"})
    return json.loads(chat.choices[0].message.content)

# --- 3. القائمة الجانبية ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🧠 CareerMind</h2>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("MAIN MENU", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
    
    if st.session_state.history:
        st.markdown("<br>📅 <b>Recent Audits</b>", unsafe_allow_html=True)
        for item in reversed(st.session_state.history[-5:]):
            st.markdown(f"<div style='font-size:0.8rem; padding:5px; color:#8b949e'>• {item['name']} ({item['score']}/10)</div>", unsafe_allow_html=True)
        if st.button("Clear History"):
            st.session_state.history = []; st.rerun()

# --- 4. صفحة CV Matcher (منظمة في بطاقات) ---
if page == "🔍 CV Matcher":
    st.markdown("<h2 style='margin-bottom:25px;'>Strategic Application Audit</h2>", unsafe_allow_html=True)
    
    # بطاقة المدخلات
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1.5, 1])
        with c1:
            st.markdown('<div class="header-text">📋 Job Description</div>', unsafe_allow_html=True)
            jd_input = st.text_area("Paste JD here", height=200, label_visibility="collapsed")
        with c2:
            st.markdown('<div class="header-text">👤 Candidate Profile</div>', unsafe_allow_html=True)
            v_name = st.text_input("Candidate/Version Name")
            pdf_file = st.file_uploader("Upload CV (PDF)", type="pdf")
            if st.button("Launch Analysis", use_container_width=True, type="primary"):
                if pdf_file and jd_input:
                    with st.spinner("Decoding DNA..."):
                        cv_txt = read_pdf(pdf_file)
                        prompt = f"Analyze CV vs JD. Return JSON: {{'score': float, 'strengths': [], 'weaknesses': [], 'summary': ''}}. CV: {cv_txt[:3500]} JD: {jd_input[:1500]}"
                        res = get_ai_json(prompt)
                        st.session_state.last_audit = res
                        st.session_state.history.append({"name": v_name, "score": res['score']})
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # عرض النتائج في بطاقة منفصلة
    if "last_audit" in st.session_state:
        data = st.session_state.last_audit
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="header-text">📊 Analysis Results</div>', unsafe_allow_html=True)
        
        r1, r2 = st.columns([1, 2])
        with r1:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=data['score'], number={'suffix': "/10", 'font':{'size':40}},
                gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "#238636"}, 'bgcolor': "#30363d"}))
            fig.update_layout(height=250, margin=dict(t=0, b=0, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
            st.plotly_chart(fig, use_container_width=True)
        with r2:
            st.markdown(f'<div class="summary-box"><b>Expert Verdict:</b><br>{data["summary"]}</div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1:
            st.markdown("<b>🏆 Competitive Edges</b>", unsafe_allow_html=True)
            for s in data['strengths']: st.markdown(f'<div class="badge-positive">✓ {s}</div>', unsafe_allow_html=True)
        with b2:
            st.markdown("<b>⚠️ Areas to Improve</b>", unsafe_allow_html=True)
            for w in data['weaknesses']: st.markdown(f'<div class="badge-negative">! {w}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. صفحة Cover Letter (منظمة ومنسقة) ---
elif page == "✉️ Cover Letter":
    st.markdown("<h2>AI Cover Letter Architect</h2>", unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    cl_col1, cl_col2 = st.columns(2)
    with cl_col1:
        st.markdown('<div class="header-text">📝 Context</div>', unsafe_allow_html=True)
        cl_jd = st.text_area("Target Job Description", height=150)
        cl_pdf = st.file_uploader("Upload CV for tailored writing", type="pdf")
    with cl_col2:
        st.markdown('<div class="header-text">🎭 Personalization</div>', unsafe_allow_html=True)
        tone = st.select_slider("Select Tone", options=["Direct", "Balanced", "Enthusiastic"])
        if st.button("Generate Masterpiece", use_container_width=True, type="primary"):
            with st.spinner("Writing..."):
                cv_info = read_pdf(cl_pdf) if cl_pdf else "Use generic professional background"
                p = f"Write a {tone} cover letter. JD: {cl_jd[:1000]}. Background: {cv_info[:2500]}. Format clearly."
                st.session_state.generated_cl = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": p}]).choices[0].message.content
    st.markdown('</div>', unsafe_allow_html=True)

    if "generated_cl" in st.session_state:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="header-text">📄 Draft</div>', unsafe_allow_html=True)
        st.text_area("Final Text", value=st.session_state.generated_cl, height=400, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

# --- صفحات Interview و Salary تتبع نفس هيكل "section-card" ---
