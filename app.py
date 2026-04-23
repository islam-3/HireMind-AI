import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. FIXED & STABLE UI CONFIG ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

st.markdown("""
    <style>
    /* Global Styles */
    .stApp { background-color: #0d1117; color: #e6edf3; }
    [data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid #30363d; }
    
    /* Result Cards */
    .result-card {
        background: rgba(22, 27, 34, 0.6);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 25px;
    }
    
    /* Badges for Edges/Improvements */
    .badge { padding: 10px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid; }
    .badge-pos { background: rgba(46, 160, 67, 0.1); border-color: #238636; color: #3fb950; }
    .badge-neg { background: rgba(248, 81, 73, 0.1); border-color: #da3633; color: #f85149; }
    
    /* Professional Green Button */
    div.stButton > button {
        background-color: #238636 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE LOGIC ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
if "history" not in st.session_state: st.session_state.history = []

def read_pdf(file):
    reader = PdfReader(file)
    return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

# --- 3. NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #58a6ff;'>🧠 CareerMind</h2>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("NAVIGATION", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep"])

# --- 4. CV MATCHER (Left: JD | Right: CV) ---
if page == "🔍 CV Matcher":
    st.title("Strategic Application Audit")
    
    # Input Area with fixed layout
    col_left, col_right = st.columns(2, gap="large")
    
    with col_left:
        st.markdown("### 📋 Job Description")
        jd_input = st.text_area("Paste the requirements here", height=250, label_visibility="collapsed", placeholder="Paste Job Description...")
        
    with col_right:
        st.markdown("### 👤 Your Profile")
        v_name = st.text_input("Candidate/Version Name", placeholder="e.g., Islam - Sales Executive")
        pdf_file = st.file_uploader("Upload CV (PDF)", type="pdf")
        if st.button("Analyze Match Score", use_container_width=True):
            if pdf_file and jd_input:
                with st.spinner("Analyzing data..."):
                    cv_txt = read_pdf(pdf_file)
                    p = f"Analyze CV vs JD. Return JSON: {{'score': float, 'strengths': [], 'weaknesses': [], 'summary': ''}}. CV: {cv_txt[:3000]} JD: {jd_input[:1500]}"
                    res = json.loads(client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": p}], response_format={"type": "json_object"}).choices[0].message.content)
                    st.session_state.last_res = res
                    st.session_state.history.append({"name": v_name, "score": res['score']})
                    st.rerun()

    # Organized Results
    if "last_res" in st.session_state:
        st.markdown("---")
        data = st.session_state.last_res
        r1, r2 = st.columns([1, 2])
        with r1:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=data['score'], number={'suffix': "/10", 'font':{'color':'white'}},
                gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "#238636"}, 'bgcolor': "#30363d"}))
            fig.update_layout(height=250, margin=dict(t=30, b=0), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        with r2:
            st.markdown(f'<div class="result-card"><b>AI Verdict:</b><br>{data["summary"]}</div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        l1, l2 = st.columns(2)
        with l1:
            st.markdown("#### 🏆 Competitive Edges")
            for s in data['strengths']: st.markdown(f'<div class="badge badge-pos">✓ {s}</div>', unsafe_allow_html=True)
        with l2:
            st.markdown("#### 🛠️ Areas to Improve")
            for w in data['weaknesses']: st.markdown(f'<div class="badge badge-neg">! {w}</div>', unsafe_allow_html=True)

# --- 5. COVER LETTER (Left: JD | Right: CV) ---
elif page == "✉️ Cover Letter":
    st.title("AI Cover Letter Architect")
    st.markdown("Build a high-impact letter tailored to your specific CV.")
    
    cl_left, cl_right = st.columns(2, gap="large")
    with cl_left:
        cl_jd = st.text_area("Target Job Description", height=250, placeholder="Paste JD here...")
    with cl_right:
        cl_pdf = st.file_uploader("Upload CV for tailored writing", type="pdf")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Generate Tailored Letter", use_container_width=True):
            with st.spinner("Writing masterpiece..."):
                cv_text = read_pdf(cl_pdf) if cl_pdf else "General experience"
                p = f"Write a professional cover letter. JD: {cl_jd[:1000]} CV: {cv_text[:2500]}"
                st.session_state.gen_cl = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": p}]).choices[0].message.content
                st.rerun()

    if "gen_cl" in st.session_state:
        st.markdown("---")
        st.subheader("📄 Generated Draft")
        st.text_area("Final Output", value=st.session_state.gen_cl, height=450, label_visibility="collapsed")
