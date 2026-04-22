import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. SETTINGS & CSS (STABLE) ---
st.set_page_config(page_title="CareerMind AI", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .audit-box { background-color: #143224; color: #aff5b4; padding: 15px; border-radius: 8px; border: 1px solid #238636; margin-top: 35px; min-height: 110px; font-size: 0.9rem; }
    .card-edge { background-color: #162a45; padding: 12px; border-radius: 6px; margin-bottom: 10px; color: #58a6ff; border: 1px solid #30363d; font-size: 0.9rem; }
    .card-improve { background-color: #2b2d16; padding: 12px; border-radius: 6px; margin-bottom: 10px; color: #d29922; border: 1px solid #30363d; font-size: 0.9rem; }
    .salary-card { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 20px; border-radius: 10px; border: 1px solid #334155; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC ---
if "history" not in st.session_state: st.session_state.history = []
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def get_ai_response(prompt, is_json=True):
    response_format = {"type": "json_object"} if is_json else None
    chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], response_format=response_format)
    return chat.choices[0].message.content

def read_pdf(file):
    reader = PdfReader(file)
    return " ".join([p.extract_text() for p in reader.pages])

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown('<h1 style="text-align:center;">🧠 CareerMind</h1>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigation", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
    
    if st.session_state.history:
        st.markdown("<br><b>Top Versions:</b>", unsafe_allow_html=True)
        for item in reversed(st.session_state.history):
            st.markdown(f'<div style="background:#21262d; padding:8px; border-left:3px solid #238636; margin-bottom:5px;">⭐ {item["score"]}/10 - {item["name"]}</div>', unsafe_allow_html=True)
        if st.button("Reset Sessions", use_container_width=True):
            st.session_state.history = []; st.rerun()

# --- 4. CV MATCHER ---
if page == "🔍 CV Matcher":
    st.title("Strategic Application Audit")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        jd_input = st.text_area("Job Description", height=200)
    with c2:
        v_name = st.text_input("Version Name:", placeholder="Islam V1")
        pdf_file = st.file_uploader("Upload PDF", type="pdf")
        if st.button("Analyze Match Score", use_container_width=True):
            if pdf_file and jd_input:
                cv_txt = read_pdf(pdf_file)
                prompt = f"Analyze CV vs JD. Return JSON: {{'score': float, 'strengths': [], 'weaknesses': [], 'summary': ''}}. CV: {cv_txt[:4000]} JD: {jd_input[:1500]}"
                res = json.loads(get_ai_response(prompt))
                st.session_state.history.append({"name": v_name, "score": res['score']})
                st.session_state.last_res = res
                st.rerun()

    if "last_res" in st.session_state:
        data = st.session_state.last_res
        st.markdown("<br><hr>", unsafe_allow_html=True)
        r1, r2 = st.columns([1, 2.5], gap="medium")
        with r1:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=data['score'], gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "#238636"}}))
            st.plotly_chart(fig, use_container_width=True)
        with r2:
            st.markdown(f'<div class="audit-box">{data["summary"]}</div>', unsafe_allow_html=True)

# --- 5. COVER LETTER (مع دعم الـ PDF) ---
elif page == "✉️ Cover Letter":
    st.title("AI Cover Letter Architect")
    c1, c2 = st.columns(2)
    with c1:
        cl_jd = st.text_area("Job Requirements:", height=150)
        pdf_file = st.file_uploader("Upload CV for context:", type="pdf")
    with c2:
        cl_skills = st.text_area("Or paste extra skills/experience:", height=150)
        if st.button("Generate Letter", use_container_width=True):
            cv_text = read_pdf(pdf_file) if pdf_file else cl_skills
            prompt = f"Write a professional cover letter based on this CV: {cv_text[:3000]} and this JD: {cl_jd}."
            st.session_state.cl_text = get_ai_response(prompt, is_json=False)
    
    if "cl_text" in st.session_state:
        st.text_area("Your Cover Letter:", value=st.session_state.cl_text, height=400)

# --- 6. INTERVIEW PREP (عاد للعمل) ---
elif page == "🎙️ Interview Prep":
    st.title("Mock Interview Simulator")
    jd_mock = st.text_area("Paste the Job Description to prepare for:", height=150)
    if st.button("Generate Questions"):
        prompt = f"Generate 5 tough interview questions and how to answer them for this JD: {jd_mock}"
        st.session_state.int_res = get_ai_response(prompt, is_json=False)
    
    if "int_res" in st.session_state:
        st.markdown(st.session_state.int_res)

# --- 7. SALARY INSIGHT ---
elif page == "💰 Salary Insight":
    st.title("Market Value Estimator")
    j_title = st.text_input("Job Title:")
    if st.button("Get Estimate"):
        prompt = f"Provide salary range (min, max, avg) for {j_title}. Return JSON: {{'min': '', 'max': '', 'avg': ''}}"
        res = json.loads(get_ai_response(prompt))
        st.success(f"Average: {res['avg']} | Range: {res['min']} - {res['max']}")
