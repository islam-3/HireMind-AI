import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json
import pandas as pd

# --- 1. SETTINGS & BRANDING (التصميم الفخم مع لوجو أكبر) ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    
    /* تكبير اللوجو بشكل ملحوظ */
    .sidebar-logo { 
        font-size: 3.5rem; /* تم تكبير الخط هنا */
        font-weight: 900; 
        color: #f0f6fc; 
        text-align: center; 
        margin-top: 30px;
        margin-bottom: 0px;
        letter-spacing: -2px;
        line-height: 1;
    }
    .sidebar-subtitle {
        font-size: 1rem;
        color: #8b949e;
        text-align: center;
        margin-bottom: 40px;
    }
    
    /* بطاقات النتائج */
    .edge-card { background-color: #1c2b1d; border-left: 5px solid #238636; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    .improve-card { background-color: #2d1a1a; border-left: 5px solid #da3633; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    
    /* الأزرار */
    .stButton>button { 
        background-color: #30363d !important; 
        color: white !important; 
        border-radius: 8px; 
        border: 1px solid #484f58; 
        font-weight: bold; 
        width: 100%; 
    }
    
    /* صندوق الرسالة */
    .letter-box { 
        background-color: #0d1117; 
        border: 1px solid #30363d; 
        padding: 25px; 
        border-radius: 10px; 
        color: #c9d1d9; 
        line-height: 1.6;
        white-space: pre-wrap;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALIZE GROQ ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key in Secrets.")
    st.stop()

# حفظ البيانات للتنقل
if "last_cv_text" not in st.session_state: st.session_state.last_cv_text = ""
if "last_jd_text" not in st.session_state: st.session_state.last_jd_text = ""
if "history" not in st.session_state: st.session_state.history = []
if "current_result" not in st.session_state: st.session_state.current_result = None

# --- 3. FUNCTIONS ---
def get_groq_analysis(cv_text, jd_text):
    prompt = f"As a Career Coach, compare CV to JD. Return ONLY JSON: {{'score': float, 'strengths': [], 'weaknesses': [], 'summary': ''}}. CV: {cv_text[:6000]} JD: {jd_text[:2000]}"
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(completion.choices[0].message.content)

def generate_cover_letter(cv_text, jd_text, tone):
    prompt = f"Write a {tone} cover letter for a candidate based on this CV and JD. CV: {cv_text[:5000]} JD: {jd_text[:1500]}"
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

# --- 4. SIDEBAR (اللوجو الضخم) ---
with st.sidebar:
    st.markdown('<p class="sidebar-logo">🧠 CareerMind</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-subtitle">Master Your Job Application</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    page = st.radio("Navigation", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep"])
    
    st.markdown("---")
    if st.session_state.history:
        st.markdown("**Top Versions:**")
        for entry in sorted(st.session_state.history, key=lambda x: x['Score'], reverse=True):
            st.write(f"⭐ {entry['Score']} - {entry['Name']}")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🗑️ Reset Sessions"):
        st.session_state.history = []
        st.session_state.current_result = None
        st.rerun()

# --- 5. PAGE: CV MATCHER ---
if page == "🔍 CV Matcher":
    st.title("Strategic Application Audit")
    c1, c2 = st.columns(2, gap="large")
    
    with c1:
        st.subheader("📋 Job Description")
        jd_input = st.text_area("Paste JD requirements...", height=250, label_visibility="collapsed")
        
    with c2:
        st.subheader("👤 Your CV")
        v_name = st.text_input("Version Name:")
        file = st.file_uploader("Upload PDF:", type="pdf")
        
        if file and st.button("Analyze Match Score"):
            if jd_input and v_name:
                with st.spinner("Analyzing..."):
                    reader = PdfReader(file)
                    text = " ".join([p.extract_text() or "" for p in reader.pages])
                    st.session_state.last_cv_text = text
                    st.session_state.last_jd_text = jd_input
                    res = get_groq_analysis(text, jd_input)
                    st.session_state.current_result = {"name": v_name, "data": res}
                    st.session_state.history.append({"Name": v_name, "Score": res['score']})
                    st.rerun()

    if st.session_state.current_result:
        res = st.session_state.current_result['data']
        st.markdown("---")
        res_c1, res_c2 = st.columns([1, 2])
        with res_c1:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=res['score'], gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "#8b949e"}}))
            fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
            st.plotly_chart(fig, use_container_width=True)
        with res_c2:
            st.markdown(f"### Results for: {st.session_state.current_result['name']}")
            st.info(res['summary'])
            sc1, sc2 = st.columns(2)
            with sc1:
                st.markdown("#### ✅ Competitive Edges")
                for s in res['strengths']: st.markdown(f'<div class="edge-card">{s}</div>', unsafe_allow_html=True)
            with sc2:
                st.markdown("#### ⚠️ Areas to Improve")
                for w in res['weaknesses']: st.markdown(f'<div class="improve-card">{w}</div>', unsafe_allow_html=True)

# --- 6. PAGE: COVER LETTER ---
elif page == "✉️ Cover Letter":
    st.title("AI Cover Letter Generator")
    if not st.session_state.last_cv_text:
        st.warning("Please upload your CV in the 'CV Matcher' page first.")
    else:
        tone = st.selectbox("Select Tone:", ["Professional", "Creative", "Short & Precise"])
        if st.button("Generate Letter"):
            with st.spinner("Writing..."):
                letter = generate_cover_letter(st.session_state.last_cv_text, st.session_state.last_jd_text, tone)
                st.markdown("---")
                st.markdown(f'<div class="letter-box">{letter}</div>', unsafe_allow_html=True)
                st.download_button("📥 Download Letter", letter, file_name="cover_letter.txt")

# --- 7. PAGE: INTERVIEW PREP ---
elif page == "🎙️ Interview Prep":
    st.title("Interview Preparation")
    st.info("Coming Next: Custom Questions based on your profile!")
