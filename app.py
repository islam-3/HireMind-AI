import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. SETTINGS & CSS (STABLE VERSION) ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .sidebar-logo { font-size: 1.8rem !important; font-weight: 800; color: #f0f6fc; text-align: center; margin-top: 15px; display: block; }
    .audit-box { background-color: #143224; color: #aff5b4; padding: 18px; border-radius: 8px; border: 1px solid #238636; margin-top: 35px; min-height: 120px; }
    .card-edge { background-color: #162a45; padding: 12px; border-radius: 6px; margin-bottom: 10px; color: #58a6ff; border: 1px solid #30363d; }
    .card-improve { background-color: #2b2d16; padding: 12px; border-radius: 6px; margin-bottom: 10px; color: #d29922; border: 1px solid #30363d; }
    .history-item { padding: 10px; border-radius: 5px; background: #21262d; margin-bottom: 5px; border-left: 4px solid #238636; font-size: 0.85rem; }
    .salary-card { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 20px; border-radius: 10px; border: 1px solid #334155; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SHARED LOGIC ---
if "history" not in st.session_state: st.session_state.history = []
if "analysis_result" not in st.session_state: st.session_state.analysis_result = None
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def get_ai_response(prompt, is_json=True):
    response_format = {"type": "json_object"} if is_json else None
    chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], response_format=response_format)
    return chat.choices[0].message.content

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown('<h1 class="sidebar-logo">🧠 CareerMind</h1>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigation", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
    
    if st.session_state.history:
        st.markdown("<br><b>Top Versions:</b>", unsafe_allow_html=True)
        for item in reversed(st.session_state.history):
            st.markdown(f'<div class="history-item">⭐ {item["score"]}/10 - {item["name"]}</div>', unsafe_allow_html=True)
        if st.button("Reset Sessions"):
            st.session_state.history = []; st.session_state.analysis_result = None; st.rerun()

# --- 4. CV MATCHER (STAYING STABLE) ---
if page == "🔍 CV Matcher":
    st.title("Strategic Application Audit")
    col_left, col_right = st.columns(2, gap="large")
    with col_left:
        st.markdown('### 📋 Job Description')
        jd_data = st.text_area("JD Content", height=200, label_visibility="collapsed")
    with col_right:
        st.markdown('### 👤 Your CV')
        v_name = st.text_input("Version Name:", placeholder="e.g. Sales Role")
        pdf_file = st.file_uploader("Upload PDF", type="pdf")
        if st.button("Analyze Match Score", use_container_width=True):
            if pdf_file and jd_data:
                with st.spinner("Analyzing..."):
                    reader = PdfReader(pdf_file)
                    cv_txt = " ".join([p.extract_text() for p in reader.pages])
                    prompt = f"Analyze CV vs JD. Return JSON: {{'score': float, 'strengths': [], 'weaknesses': [], 'summary': ''}}. CV: {cv_txt[:4000]} JD: {jd_data[:1500]}"
                    res = json.loads(get_ai_response(prompt))
                    st.session_state.analysis_result = {"name": v_name, "data": res}
                    st.session_state.history.append({"name": v_name, "score": res['score']})
                    st.rerun()

    if st.session_state.analysis_result:
        data = st.session_state.analysis_result['data']
        st.markdown("<br><hr>", unsafe_allow_html=True)
        r_top1, r_top2 = st.columns([1, 2.5], gap="medium")
        with r_top1:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=data['score'], number={'font': {'size': 32}, 'suffix': "/10"}, gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "#238636"}}))
            fig.update_layout(height=180, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, margin=dict(t=0, b=0, l=10, r=10))
            st.plotly_chart(fig, use_container_width=True)
        with r_top2:
            st.markdown(f'<div class="audit-box"><b>Audit for: {st.session_state.analysis_result["name"]}</b><br><br>{data["summary"]}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        r_bot1, r_bot2 = st.columns(2)
        with r_bot1:
            st.markdown("#### 🏆 Competitive Edges")
            for s in data['strengths']: st.markdown(f'<div class="card-edge">{s}</div>', unsafe_allow_html=True)
        with r_bot2:
            st.markdown("#### 🛠️ Areas to Improve")
            for w in data['weaknesses']: st.markdown(f'<div class="card-improve">{w}</div>', unsafe_allow_html=True)

# --- 5. COVER LETTER PAGE ---
elif page == "✉️ Cover Letter":
    st.title("Strategic Cover Letter Generator")
    st.markdown("Generate a high-impact cover letter tailored to the job description.")
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        cl_jd = st.text_area("Job Requirements:", height=150)
        cl_tone = st.selectbox("Tone:", ["Professional", "Bold & Creative", "Direct & Short"])
    with c_col2:
        cl_cv = st.text_area("Key Skills/Background:", height=150)
        if st.button("Generate Letter", use_container_width=True):
            with st.spinner("Writing..."):
                prompt = f"Write a {cl_tone} cover letter for this JD: {cl_jd} using this background: {cl_cv}. Make it short and powerful."
                st.session_state.generated_cl = get_ai_response(prompt, is_json=False)
    
    if "generated_cl" in st.session_state:
        st.markdown("---")
        st.text_area("Your Cover Letter:", value=st.session_state.generated_cl, height=400)

# --- 6. SALARY INSIGHT PAGE ---
elif page == "💰 Salary Insight":
    st.title("Salary Expectations Tool")
    st.markdown("Estimate the market rate for this role.")
    s_col1, s_col2 = st.columns([1, 1])
    with s_col1:
        job_title = st.text_input("Job Title:", placeholder="e.g. Sales Manager")
        location = st.text_input("Location:", placeholder="e.g. Dubai, UAE")
    with s_col2:
        exp = st.slider("Years of Experience:", 0, 20, 3)
        if st.button("Estimate Salary", use_container_width=True):
            with st.spinner("Fetching Market Data..."):
                prompt = f"Estimate monthly salary for {job_title} in {location} with {exp} years experience. Return JSON: {{'min': str, 'max': str, 'avg': str, 'currency': str, 'tips': []}}"
                st.session_state.salary_data = json.loads(get_ai_response(prompt))
    
    if "salary_data" in st.session_state:
        sd = st.session_state.salary_data
        st.markdown("---")
        s_res1, s_res2, s_res3 = st.columns(3)
        with s_res1: st.markdown(f'<div class="salary-card"><small>Minimum</small><h3>{sd["min"]} {sd["currency"]}</h3></div>', unsafe_allow_html=True)
        with s_res2: st.markdown(f'<div class="salary-card" style="border-color: #238636;"><small>Average</small><h3>{sd["avg"]} {sd["currency"]}</h3></div>', unsafe_allow_html=True)
        with r_res3: st.markdown(f'<div class="salary-card"><small>Maximum</small><h3>{sd["max"]} {sd["currency"]}</h3></div>', unsafe_allow_html=True)
        
        st.info("💡 **Negotiation Tip:** " + sd['tips'][0] if sd['tips'] else "Know your value!")
