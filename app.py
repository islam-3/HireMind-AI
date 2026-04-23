import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. FIXED UI & THEME ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    [data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid #30363d; }
    
    /* Global Reset/Action Buttons */
    .reset-btn { border: 1px solid #f85149 !important; color: #f85149 !important; }
    
    /* Result Styling */
    .result-card { background: rgba(22, 27, 34, 0.6); border: 1px solid #30363d; border-radius: 12px; padding: 25px; }
    .badge { padding: 10px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid; }
    .badge-pos { background: rgba(46, 160, 67, 0.1); border-color: #238636; color: #3fb950; }
    .badge-neg { background: rgba(248, 81, 73, 0.1); border-color: #da3633; color: #f85149; }
    
    /* Standard Green Button */
    div.stButton > button { background-color: #238636 !important; color: white !important; border-radius: 8px !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE LOGIC ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# تهيئة الجلسة لجميع الصفحات
for key in ["history", "last_res", "gen_cl", "salary_data"]:
    if key not in st.session_state: st.session_state[key] = None if key != "history" else []

def read_pdf(file):
    reader = PdfReader(file)
    return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

# --- 3. SIDEBAR (With Global Reset) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #58a6ff;'>🧠 CareerMind</h2>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("NAVIGATION", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🗑️ Reset All Progress", use_container_width=True):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()

# --- 4. CV MATCHER ---
if page == "🔍 CV Matcher":
    st.title("Strategic Application Audit")
    col_left, col_right = st.columns(2, gap="large")
    with col_left:
        st.subheader("📋 Job Description")
        jd_input = st.text_area("Requirements", height=250, label_visibility="collapsed", placeholder="Paste JD...")
    with col_right:
        st.subheader("👤 Profile Upload")
        v_name = st.text_input("Version Name")
        pdf_file = st.file_uploader("Upload CV", type="pdf", key="cv_m")
        if st.button("Launch Analysis", use_container_width=True):
            if pdf_file and jd_input:
                with st.spinner("Analyzing..."):
                    cv_txt = read_pdf(pdf_file)
                    p = f"Analyze CV vs JD. Return JSON: {{'score': float, 'strengths': [], 'weaknesses': [], 'summary': ''}}. CV: {cv_txt[:3000]} JD: {jd_input[:1500]}"
                    res = json.loads(client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": p}], response_format={"type": "json_object"}).choices[0].message.content)
                    st.session_state.last_res = res
                    st.session_state.history.append({"name": v_name, "score": res['score']})
                    st.rerun()

    if st.session_state.last_res:
        data = st.session_state.last_res
        st.markdown("---")
        r1, r2 = st.columns([1, 2])
        with r1:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=data['score'], number={'suffix': "/10", 'font':{'color':'white'}}, gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "#238636"}}))
            fig.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)')
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
    col_left, col_right = st.columns(2, gap="large")
    with col_left:
        cl_jd = st.text_area("Job Description", height=250)
    with col_right:
        cl_pdf = st.file_uploader("Upload CV", type="pdf", key="cl_u")
        if st.button("Generate Letter", use_container_width=True):
            with st.spinner("Writing..."):
                cv_txt = read_pdf(cl_pdf) if cl_pdf else ""
                p = f"Write a professional cover letter for: {cl_jd[:1000]} based on: {cv_txt[:2000]}"
                st.session_state.gen_cl = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": p}]).choices[0].message.content
                st.rerun()
    if st.session_state.gen_cl:
        st.text_area("Result", value=st.session_state.gen_cl, height=400)

# --- 6. SALARY INSIGHT (أعيدت بترتيب سليم) ---
elif page == "💰 Salary Insight":
    st.title("Market Value Estimator")
    col_left, col_right = st.columns(2, gap="large")
    with col_left:
        role = st.text_input("Job Title", placeholder="e.g. Software Engineer")
        loc = st.text_input("Location", placeholder="e.g. Dubai, Remote, etc.")
    with col_right:
        sal_pdf = st.file_uploader("Upload CV for skill-based pricing", type="pdf", key="sal_u")
        if st.button("Estimate Salary Range", use_container_width=True):
            with st.spinner("Fetching market data..."):
                cv_txt = read_pdf(sal_pdf) if sal_pdf else ""
                p = f"Estimate salary for {role} in {loc} based on these skills: {cv_txt[:1500]}. Return JSON: {{'min': int, 'max': int, 'avg': int, 'currency': str, 'notes': ''}}"
                st.session_state.salary_data = json.loads(client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": p}], response_format={"type": "json_object"}).choices[0].message.content)
                st.rerun()
    
    if st.session_state.salary_data:
        sd = st.session_state.salary_data
        st.markdown(f"### Estimated Range: {sd['min']:,} - {sd['max']:,} {sd['currency']}")
        st.progress(0.7) # visual indicator
        st.info(sd['notes'])
