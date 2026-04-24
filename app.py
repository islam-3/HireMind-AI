import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. UI CONFIGURATION ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    [data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid #30363d; }
    .result-card { background: rgba(22, 27, 34, 0.6); border: 1px solid #30363d; border-radius: 12px; padding: 25px; margin-bottom: 20px; }
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

for key in ["history", "last_res", "gen_cl", "salary_data", "interview_q", "current_feedback"]:
    if key not in st.session_state:
        st.session_state[key] = [] if "history" in key or "interview_q" in key else None

def read_pdf(file):
    try:
        reader = PdfReader(file)
        return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
    except: return ""

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #58a6ff;'>🧠 CareerMind</h2>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("NAVIGATION", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
    if st.button("🗑️ Reset All Progress", use_container_width=True):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- 4. INTERVIEW PREP (NEWLY ACTIVATED) ---
if page == "🎙️ Interview Prep":
    st.title("AI Interview Simulator")
    i_l, i_r = st.columns(2, gap="large")
    
    with i_l:
        st.subheader("🎯 Target Role Context")
        int_jd = st.text_area("Paste Job Description", height=200, placeholder="What role are you interviewing for?")
    
    with i_r:
        st.subheader("👤 Your Profile")
        int_pdf = st.file_uploader("Upload CV for context", type="pdf", key="int_cv")
        if st.button("Generate Interview Questions", use_container_width=True):
            if int_jd:
                with st.spinner("Generating targeted questions..."):
                    cv_context = read_pdf(int_pdf) if int_pdf else "General candidate"
                    prompt = f"Based on JD: {int_jd[:1000]} and CV: {cv_context[:1000]}, generate 5 difficult interview questions. Return as a JSON list of strings: {{\"questions\": []}}"
                    res = json.loads(client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], response_format={"type": "json_object"}).choices[0].message.content)
                    st.session_state.interview_q = res['questions']
                    st.rerun()

    if st.session_state.interview_q:
        st.markdown("---")
        st.subheader("📋 Mock Interview Session")
        for i, q in enumerate(st.session_state.interview_q):
            with st.expander(f"Question {i+1}: {q}"):
                ans = st.text_area("Your Answer:", key=f"ans_{i}")
                if st.button(f"Analyze Answer {i+1}", key=f"btn_{i}"):
                    with st.spinner("Analyzing..."):
                        p = f"Question: {q}\nAnswer: {ans}\nProvide feedback and a better sample answer. Return JSON: {{'feedback': '', 'sample': ''}}"
                        feedback = json.loads(client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": p}], response_format={"type": "json_object"}).choices[0].message.content)
                        st.info(f"💡 **Feedback:** {feedback['feedback']}")
                        st.success(f"🌟 **Better Way to Say It:** {feedback['sample']}")

# --- 5. CV MATCHER & COVER LETTER & SALARY (Same logic as before) ---
elif page == "🔍 CV Matcher":
    # ... (كود الـ CV Matcher السابق)
    st.title("Strategic Application Audit")
    col_l, col_r = st.columns(2, gap="large")
    with col_l:
        jd_input = st.text_area("JD Content", height=250)
    with col_r:
        v_name = st.text_input("Label")
        pdf_file = st.file_uploader("Upload CV", type="pdf")
        if st.button("Analyze"):
            # logic here...
            pass

elif page == "✉️ Cover Letter":
    # ... (كود الـ Cover Letter السابق)
    st.title("AI Cover Letter Architect")
    cl_l, cl_r = st.columns(2, gap="large")
    with cl_l: cl_jd = st.text_area("JD")
    with cl_r:
        cl_pdf = st.file_uploader("CV", type="pdf")
        if st.button("Generate"):
            # logic here...
            pass

elif page == "💰 Salary Insight":
    # ... (كود الـ Salary Insight الواقعي لعام 2026 السابق)
    st.title("Market Value Estimator")
    s_l, s_r = st.columns(2, gap="large")
    # logic here...
    pass
