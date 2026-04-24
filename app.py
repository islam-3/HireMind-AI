import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. UI CONFIGURATION & STYLING ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

st.markdown("""
    <style>
    /* Main Theme */
    .stApp { background-color: #0d1117; color: #e6edf3; }
    [data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid #30363d; }
    
    /* Logo Styling - Centered & Balanced */
    .sidebar-logo {
        display: flex;
        flex-direction: column;
        align-items: center; /* سنتر اللوغو */
        justify-content: center;
        width: 100%;
        text-align: center; 
        font-size: 2.2rem !important;
        font-weight: bold;
        color: #58a6ff;
        padding-top: 20px;
    }
    
    .sidebar-subtext {
        text-align: center;
        width: 100%;
        color: #8b949e;
        font-size: 0.9rem;
        margin-bottom: 20px;
    }
    
    /* Result Cards */
    .result-card { background: rgba(22, 27, 34, 0.6); border: 1px solid #30363d; border-radius: 12px; padding: 25px; margin-bottom: 20px; }
    .badge { padding: 10px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid; font-size: 0.9rem; }
    .badge-pos { background: rgba(46, 160, 67, 0.1); border-color: #238636; color: #3fb950; }
    .badge-neg { background: rgba(248, 81, 73, 0.1); border-color: #da3633; color: #f85149; }
    
    /* Buttons Styling */
    div.stButton > button {
        background-color: #238636 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE LOGIC ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

for key in ["history", "last_res", "gen_cl", "salary_data", "interview_q"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key in ["history", "interview_q"] else None

def read_pdf(file):
    try:
        reader = PdfReader(file)
        return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
    except: return ""

# --- 3. SIDEBAR (Logo, Nav, & Balanced Reset) ---
with st.sidebar:
    # اللوغو الموحد والموسطن
    st.markdown('<div class="sidebar-logo">🧠 CareerMind</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtext">Master Your Job Application</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    page = st.radio("NAVIGATION", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
    
    # مباعدة الزر ليكون في المنتصف تحت خيارات التنقل
    st.markdown("<br>" * 4, unsafe_allow_html=True) 
    if st.button("🗑️ Reset All Progress", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- 4. CV MATCHER ---
if page == "🔍 CV Matcher":
    st.title("Strategic Application Audit")
    col_l, col_r = st.columns(2, gap="large")
    with col_l:
        st.subheader("📋 Job Requirements")
        jd_input = st.text_area("JD Content", height=250, label_visibility="collapsed", placeholder="Paste JD here...")
    with col_r:
        st.subheader("👤 Profile Upload")
        v_name = st.text_input("Analysis Label")
        pdf_file = st.file_uploader("Upload CV", type="pdf", key="m_cv")
        if st.button("Analyze Match Score", use_container_width=True):
            if pdf_file and jd_input:
                with st.spinner("Analyzing..."):
                    cv_txt = read_pdf(pdf_file)
                    p = f"Analyze CV vs JD. Return JSON: {{'score': float, 'strengths': [], 'weaknesses': [], 'summary': ''}}. CV: {cv_txt[:3000]} JD: {jd_input[:1500]}"
                    res = json.loads(client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": p}], response_format={"type": "json_object"}).choices[0].message.content)
                    st.session_state.last_res = res
                    st.session_state.history.append({"name": v_name or "Audit", "score": res['score']})
                    st.rerun()

    if st.session_state.last_res:
        data = st.session_state.last_res
        st.markdown("---")
        r1, r2 = st.columns([1, 2])
        with r1:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=data['score'], number={'suffix': "/10", 'font':{'color':'white'}}, gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "#238636"}}))
            fig.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
        with r2:
            st.markdown(f'<div class="result-card"><b>AI Verdict:</b><br>{data["summary"]}</div>', unsafe_allow_html=True)
        l1, l2 = st.columns(2)
        with l1:
            for s in data['strengths']: st.markdown(f'<div class="badge badge-pos">✓ {s}</div>', unsafe_allow_html=True)
        with l2:
            for w in data['weaknesses']: st.markdown(f'<div class="badge badge-neg">! {w}</div>', unsafe_allow_html=True)

# --- 5. COVER LETTER ---
elif page == "✉️ Cover Letter":
    st.title("AI Cover Letter Architect")
    cl_l, cl_r = st.columns(2, gap="large")
    with cl_l:
        cl_jd = st.text_area("Job Description", height=250)
    with cl_r:
        cl_pdf = st.file_uploader("Upload CV", type="pdf", key="cl_cv")
        if st.button("Generate Tailored Letter", use_container_width=True):
            with st.spinner("Writing..."):
                cv_txt = read_pdf(cl_pdf) if cl_pdf else "General Profile"
                p = f"Write a professional cover letter. JD: {cl_jd[:1000]} CV: {cv_txt[:2500]}"
                st.session_state.gen_cl = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": p}]).choices[0].message.content
                st.rerun()
    if st.session_state.gen_cl:
        st.text_area("Resulting Draft", value=st.session_state.gen_cl, height=450)

# --- 6. INTERVIEW PREP ---
elif page == "🎙️ Interview Prep":
    st.title("AI Interview Simulator")
    i_l, i_r = st.columns(2, gap="large")
    with i_l:
        int_jd = st.text_area("Target JD", height=200)
    with i_r:
        int_pdf = st.file_uploader("Context CV", type="pdf", key="int_cv")
        if st.button("Generate Questions", use_container_width=True):
            with st.spinner("Generating..."):
                cv_txt = read_pdf(int_pdf)
                p = f"Generate 5 interview questions for this JD: {int_jd[:800]} and CV: {cv_txt[:1500]}. Return JSON: {{'questions': []}}"
                st.session_state.interview_q = json.loads(client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": p}], response_format={"type": "json_object"}).choices[0].message.content)['questions']
                st.rerun()
    if st.session_state.interview_q:
        for q in st.session_state.interview_q:
            st.markdown(f'<div class="result-card">{q}</div>', unsafe_allow_html=True)

# --- 7. SALARY INSIGHT ---
elif page == "💰 Salary Insight":
    st.title("Market Value Estimator")
    s_l, s_r = st.columns(2, gap="large")
    with s_l:
        role = st.text_input("Job Title")
        loc = st.text_input("Location")
    with s_r:
        s_pdf = st.file_uploader("Upload CV", type="pdf", key="s_cv")
        if st.button("Estimate Realistic Range", use_container_width=True):
            with st.spinner("Analyzing 2026 rates..."):
                cv_txt = read_pdf(s_pdf)
                prompt = f"Estimate 2026 salary for {role} in {loc}. Context: {cv_txt[:1000]}. Return JSON: {{'min': int, 'max': int, 'avg': int, 'currency': str, 'notes': str}}"
                res = json.loads(client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], response_format={"type": "json_object"}, temperature=0).choices[0].message.content)
                st.session_state.salary_data = res
                st.rerun()

    if st.session_state.salary_data:
        sd = st.session_state.salary_data
        st.markdown("---")
        st.header(f"{sd['min']:,} - {sd['max']:,} {sd['currency']}")
        st.info(f"📌 {sd['notes']}")
