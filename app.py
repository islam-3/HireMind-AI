import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. CLEAN & MODERN UI CONFIG ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

st.markdown("""
    <style>
    /* Global Styles */
    .stApp { background-color: #0d1117; color: #e6edf3; }
    [data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid #30363d; }
    
    /* Result Cards - Soft Glow */
    .result-card {
        background: rgba(22, 27, 34, 0.5);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 25px;
        margin-top: 20px;
    }
    
    /* Status Badges */
    .badge {
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-size: 0.9rem;
        border-left: 5px solid;
    }
    .badge-pos { background: rgba(46, 160, 67, 0.1); border-color: #238636; color: #3fb950; }
    .badge-neg { background: rgba(248, 81, 73, 0.1); border-color: #da3633; color: #f85149; }
    
    /* Buttons */
    div.stButton > button {
        background: #238636;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 24px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE LOGIC ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
if "history" not in st.session_state: st.session_state.history = []

def read_pdf(file):
    reader = PdfReader(file)
    return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #58a6ff;'>🧠 CareerMind</h2>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("MAIN MENU", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
    
    if st.session_state.history:
        st.markdown("<br><b>Activity Log:</b>", unsafe_allow_html=True)
        for item in reversed(st.session_state.history[-3:]):
            st.caption(f"✔ {item['name']} - {item['score']}/10")

# --- 4. CV MATCHER PAGE ---
if page == "🔍 CV Matcher":
    st.title("Strategic Application Audit")
    
    # Inputs Section - Using balanced columns to prevent overlap
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.subheader("📋 Job Description")
        jd_input = st.text_area("Paste JD here", height=280, label_visibility="collapsed", placeholder="Enter the job requirements...")
    with col2:
        st.subheader("👤 Candidate Info")
        v_name = st.text_input("Analysis Name (e.g. Islam V2)")
        pdf_file = st.file_uploader("Upload CV (PDF)", type="pdf")
        if st.button("Launch Analysis", use_container_width=True):
            if pdf_file and jd_input:
                with st.spinner("Calculating Match Score..."):
                    cv_txt = read_pdf(pdf_file)
                    p = f"Analyze CV vs JD. Return JSON: {{'score': float, 'strengths': [], 'weaknesses': [], 'summary': ''}}. CV: {cv_txt[:3500]} JD: {jd_input[:1500]}"
                    res = json.loads(client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": p}], response_format={"type": "json_object"}).choices[0].message.content)
                    st.session_state.last_res = res
                    st.session_state.history.append({"name": v_name, "score": res['score']})
                    st.rerun()

    # Results Section - Vertical stack for clarity
    if "last_res" in st.session_state:
        st.markdown("---")
        data = st.session_state.last_res
        
        # Row 1: Gauge & Summary
        res_col1, res_col2 = st.columns([1, 2], gap="medium")
        with res_col1:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=data['score'], number={'suffix': "/10", 'font':{'color':'white'}},
                gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "#238636"}, 'bgcolor': "#30363d"}))
            fig.update_layout(height=250, margin=dict(t=30, b=0), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        with res_col2:
            st.markdown(f'<div class="result-card"><b>AI Verdict:</b><br><p style="color:#8b949e; margin-top:10px;">{data["summary"]}</p></div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Row 2: Strengths & Weaknesses
        list_col1, list_col2 = st.columns(2, gap="large")
        with list_col1:
            st.markdown("#### 🏆 Competitive Edges")
            for s in data['strengths']: st.markdown(f'<div class="badge badge-pos">✓ {s}</div>', unsafe_allow_html=True)
        with list_col2:
            st.markdown("#### 🛠️ Areas to Improve")
            for w in data['weaknesses']: st.markdown(f'<div class="badge badge-neg">! {w}</div>', unsafe_allow_html=True)

# --- 5. COVER LETTER PAGE ---
elif page == "✉️ Cover Letter":
    st.title("AI Cover Letter Architect")
    st.markdown("Build a high-impact letter based on your specific CV.")
    
    cl_col1, cl_col2 = st.columns(2, gap="large")
    with cl_col1:
        cl_jd = st.text_area("Target Job Description", height=250)
        cl_pdf = st.file_uploader("Upload CV for Context", type="pdf")
    with cl_col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Generate Tailored Letter", use_container_width=True):
            with st.spinner("Writing..."):
                cv_text = read_pdf(cl_pdf) if cl_pdf else "Professional Profile"
                p = f"Write a professional cover letter. JD: {cl_jd[:1000]} CV: {cv_text[:2500]}"
                st.session_state.gen_cl = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": p}]).choices[0].message.content
                st.rerun()

    if "gen_cl" in st.session_state:
        st.markdown("---")
        st.subheader("📄 Generated Masterpiece")
        st.text_area("Result", value=st.session_state.gen_cl, height=450, label_visibility="collapsed")
