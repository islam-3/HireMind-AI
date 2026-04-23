import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. UI CONFIGURATION & THEME ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

st.markdown("""
    <style>
    /* Main Theme */
    .stApp { background-color: #0d1117; color: #e6edf3; }
    [data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid #30363d; }
    
    /* Result Cards */
    .result-card { background: rgba(22, 27, 34, 0.6); border: 1px solid #30363d; border-radius: 12px; padding: 25px; margin-bottom: 20px; }
    .badge { padding: 10px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid; font-size: 0.9rem; }
    .badge-pos { background: rgba(46, 160, 67, 0.1); border-color: #238636; color: #3fb950; }
    .badge-neg { background: rgba(248, 81, 73, 0.1); border-color: #da3633; color: #f85149; }
    
    /* Buttons */
    div.stButton > button {
        background-color: #238636 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold;
        border: none !important;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE LOGIC ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Initialize session state
for key in ["history", "last_res", "gen_cl", "salary_data", "interview_q"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key in ["history", "interview_q"] else None

def read_pdf(file):
    try:
        reader = PdfReader(file)
        return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
    except: return ""

# --- 3. SIDEBAR (Navigation & Reset) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #58a6ff;'>🧠 CareerMind</h2>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("NAVIGATION", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
    
    st.markdown("<br><br>", unsafe_allow_html=True)
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
        if st.button("Generate Letter", use_container_width=True):
            with st.spinner("Writing..."):
                cv_txt = read_pdf(cl_pdf) if cl_pdf else "General Profile"
                p = f"Write a professional cover letter. JD: {cl_jd[:1000]} CV: {cv_txt[:2500]}"
                st.session_state.gen_cl = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": p}]).choices[0].message.content
                st.rerun()
    if st.session_state.gen_cl:
        st.text_area("Result", value=st.session_state.gen_cl, height=450)

# --- 6. SALARY INSIGHT (USD Conversion & Stability) ---
elif page == "💰 Salary Insight":
    st.title("Market Value Estimator")
    s_l, s_r = st.columns(2, gap="large")
    with s_l:
        role = st.text_input("Job Title", placeholder="e.g. Sales Executive")
        loc = st.text_input("Location", placeholder="e.g. Istanbul, Turkey")
    with s_r:
        s_pdf = st.file_uploader("Upload CV for skill-based audit", type="pdf", key="s_cv")
        if st.button("Estimate Stable Range", use_container_width=True):
            if role and loc:
                with st.spinner("Calculating market value and USD conversion..."):
                    cv_txt = read_pdf(s_pdf)
                    prompt = f"""
                    Estimate salary for {role} in {loc}. Skills: {cv_txt[:1000]}.
                    Return JSON: {{
                        "min": int, "max": int, "avg": int, "currency": str, 
                        "min_usd": int, "max_usd": int, "notes": str
                    }}
                    Base the USD conversion on April 2026 rates.
                    """
                    res = json.loads(client.chat.completions.create(
                        model="llama-3.3-70b-versatile", 
                        messages=[{"role": "user", "content": prompt}], 
                        response_format={"type": "json_object"}, 
                        temperature=0 # Stability fix
                    ).choices[0].message.content)
                    st.session_state.salary_data = res
                    st.rerun()

    if st.session_state.salary_data:
        sd = st.session_state.salary_data
        st.markdown("---")
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Local Currency Range", f"{sd['min']:,} - {sd['max']:,} {sd['currency']}")
        with m2:
            st.metric("USD Equivalent", f"${sd['min_usd']:,} - ${sd['max_usd']:,}")
        
        st.markdown(f"**Average:** {sd['avg']:,} {sd['currency']}")
        st.progress(0.65)
        st.info(f"📌 {sd['notes']}")
