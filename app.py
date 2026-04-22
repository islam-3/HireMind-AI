import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. SETTINGS & CSS (STABLE & FINAL) ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .audit-box { background-color: #143224; color: #aff5b4; padding: 15px; border-radius: 8px; border: 1px solid #238636; margin-top: 35px; min-height: 110px; font-size: 0.9rem; }
    .card-edge { background-color: #162a45; padding: 12px; border-radius: 6px; margin-bottom: 10px; color: #58a6ff; border: 1px solid #30363d; min-height: 50px; font-size: 0.9rem; }
    .card-improve { background-color: #2b2d16; padding: 12px; border-radius: 6px; margin-bottom: 10px; color: #d29922; border: 1px solid #30363d; min-height: 50px; font-size: 0.9rem; }
    .salary-card { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 20px; border-radius: 10px; border: 1px solid #334155; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GLOBAL LOGIC ---
if "history" not in st.session_state: st.session_state.history = []
if "analysis_result" not in st.session_state: st.session_state.analysis_result = None
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def get_ai_response(prompt, is_json=True):
    response_format = {"type": "json_object"} if is_json else None
    chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], response_format=response_format)
    return chat.choices[0].message.content

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown('<h1 style="text-align:center;">🧠 CareerMind</h1>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigation", ["🔍 CV Matcher", "✉️ Cover Letter", "💰 Salary Insight"])
    
    if st.session_state.history:
        st.markdown("<br><b>Top Versions:</b>", unsafe_allow_html=True)
        for item in reversed(st.session_state.history):
            st.markdown(f'<div style="padding:8px; background:#21262d; border-left:3px solid #238636; margin-bottom:5px; font-size:0.85rem;">⭐ {item["score"]}/10 - {item["name"]}</div>', unsafe_allow_html=True)
        if st.button("Reset Sessions", use_container_width=True):
            st.session_state.history = []; st.session_state.analysis_result = None; st.rerun()

# --- 4. PAGE: CV MATCHER (STABLE) ---
if page == "🔍 CV Matcher":
    st.title("Strategic Application Audit")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("### 📋 Job Description")
        jd_input = st.text_area("JD", height=200, label_visibility="collapsed")
    with c2:
        st.markdown("### 👤 Your CV")
        v_name = st.text_input("Version Name:", placeholder="e.g. Sales Role")
        pdf_file = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")
        if st.button("Analyze Match Score", use_container_width=True):
            if pdf_file and jd_input:
                reader = PdfReader(pdf_file)
                cv_txt = " ".join([p.extract_text() for p in reader.pages])
                # برومبت التقييم العادل والمستقر
                prompt = f"Analyze CV vs JD. Be fair and professional. Return JSON: {{'score': float, 'strengths': [], 'weaknesses': [], 'summary': ''}}. CV: {cv_txt[:4000]} JD: {jd_input[:1500]}"
                res = json.loads(get_ai_response(prompt))
                st.session_state.analysis_result = {"name": v_name, "data": res}
                st.session_state.history.append({"name": v_name, "score": res['score']})
                st.rerun()

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

# --- 5. PAGE: COVER LETTER (NEW) ---
elif page == "✉️ Cover Letter":
    st.title("AI Cover Letter Architect")
    col_cl1, col_cl2 = st.columns(2)
    with col_cl1:
        cl_jd = st.text_area("Target Job Description:", height=150)
        tone = st.selectbox("Writing Tone:", ["Professional & Bold", "Academic", "Short & Direct"])
    with col_cl2:
        cl_bio = st.text_area("Your Key Experience (or paste CV text):", height=150)
        if st.button("Generate Letter", use_container_width=True):
            with st.spinner("Drafting..."):
                prompt = f"Write a {tone} cover letter based on this JD: {cl_jd} and this background: {cl_bio}. Focus on impact."
                st.session_state.last_cl = get_ai_response(prompt, is_json=False)

    if "last_cl" in st.session_state:
        st.markdown("---")
        st.text_area("Result:", value=st.session_state.last_cl, height=400)
        st.download_button("Download as TXT", st.session_state.last_cl)

# --- 6. PAGE: SALARY INSIGHT (NEW) ---
elif page == "💰 Salary Insight":
    st.title("Market Value Estimator")
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        job_t = st.text_input("Job Title:", placeholder="Software Engineer")
        loc = st.text_input("Location:", placeholder="Riyadh, SA")
    with s_col2:
        years = st.slider("Years of Experience:", 0, 20, 2)
        if st.button("Get Estimate", use_container_width=True):
            prompt = f"Provide salary data for {job_t} in {loc} with {years} years exp. Return JSON: {{'min': str, 'max': str, 'avg': str, 'currency': str}}"
            st.session_state.sal_res = json.loads(get_ai_response(prompt))

    if "sal_res" in st.session_state:
        s = st.session_state.sal_res
        st.markdown("---")
        res_col1, res_col2, res_col3 = st.columns(3)
        with res_col1: st.markdown(f'<div class="salary-card"><small>Min</small><h2>{s["min"]} {s["currency"]}</h2></div>', unsafe_allow_html=True)
        with res_col2: st.markdown(f'<div class="salary-card" style="border-color:#238636;"><small>Average</small><h2>{s["avg"]} {s["currency"]}</h2></div>', unsafe_allow_html=True)
        with res_col3: st.markdown(f'<div class="salary-card"><small>Max</small><h2>{s["max"]} {s["currency"]}</h2></div>', unsafe_allow_html=True)
