import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json
import pandas as pd

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .sidebar-logo { font-size: 1.8rem; font-weight: 900; color: #f0f6fc; text-align: center; margin-bottom: 0px; }
    .edge-card { background-color: #1c2b1d; border-left: 5px solid #238636; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    .improve-card { background-color: #2d1a1a; border-left: 5px solid #da3633; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    .stButton>button { background-color: #238636 !important; color: white !important; border-radius: 8px; font-weight: bold; width: 100%; }
    .letter-box { background-color: #0d1117; border: 1px dashed #30363d; padding: 25px; border-radius: 10px; color: #c9d1d9; font-family: 'Courier New', Courier, monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALIZE GROQ CLIENT ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("API Key configuration error.")
    st.stop()

# حفظ النصوص في الـ Session لضمان انتقالها بين الصفحات
if "last_cv_text" not in st.session_state: st.session_state.last_cv_text = ""
if "last_jd_text" not in st.session_state: st.session_state.last_jd_text = ""
if "history" not in st.session_state: st.session_state.history = []
if "current_result" not in st.session_state: st.session_state.current_result = None

# --- 3. ANALYZER FUNCTIONS ---
def get_groq_analysis(cv_text, jd_text):
    prompt = f"As a Career Coach, compare CV to JD. Return JSON: {{'score': float, 'strengths': [], 'weaknesses': [], 'summary': ''}}. CV: {cv_text[:6000]} JD: {jd_text[:2000]}"
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(completion.choices[0].message.content)

def generate_cover_letter(cv_text, jd_text, tone):
    prompt = f"Write a {tone} cover letter for a candidate based on their CV and this JD. Highlight skills that match the requirements. Tone should be {tone}. CV: {cv_text[:5000]} JD: {jd_text[:1500]}"
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown('<p class="sidebar-logo">🚀 CareerMind</p>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigation", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep"])
    st.markdown("---")
    if st.session_state.history:
        st.markdown("**Top Matches:**")
        for entry in sorted(st.session_state.history, key=lambda x: x['Score'], reverse=True):
            st.write(f"⭐ {entry['Score']} - {entry['Name']}")

# --- 5. PAGE: CV MATCHER ---
if page == "🔍 CV Matcher":
    st.title("Optimize Your Application")
    c1, c2 = st.columns(2)
    with c1:
        jd_input = st.text_area("Paste JD:", height=200)
    with c2:
        name = st.text_input("Version Name:")
        file = st.file_uploader("Upload CV:", type="pdf")
        
    if file and st.button("Check Match Score"):
        reader = PdfReader(file)
        text = " ".join([p.extract_text() or "" for p in reader.pages])
        st.session_state.last_cv_text = text
        st.session_state.last_jd_text = jd_input
        res = get_groq_analysis(text, jd_input)
        st.session_state.current_result = {"name": name, "data": res}
        st.session_state.history.append({"Name": name, "Score": res['score']})
        st.rerun()

    if st.session_state.current_result:
        # (هنا يوضع كود عرض النتائج والعداد - نفس الكود السابق)
        res = st.session_state.current_result['data']
        st.markdown("---")
        res_c1, res_c2 = st.columns([1, 2])
        with res_c1:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=res['score'], gauge={'axis': {'range': [0, 10]}}))
            fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
            st.plotly_chart(fig, use_container_width=True)
        with res_c2:
            st.info(res['summary'])
            col_a, col_b = st.columns(2)
            with col_a:
                for s in res['strengths']: st.markdown(f'<div class="edge-card">{s}</div>', unsafe_allow_html=True)
            with col_b:
                for w in res['weaknesses']: st.markdown(f'<div class="improve-card">{w}</div>', unsafe_allow_html=True)

# --- 6. PAGE: COVER LETTER ---
elif page == "✉️ Cover Letter":
    st.title("AI Cover Letter Generator")
    if not st.session_state.last_cv_text:
        st.warning("⚠️ Please upload your CV in the 'CV Matcher' page first.")
    else:
        st.success("✅ CV and JD data detected!")
        tone = st.selectbox("Choose Tone:", ["Professional", "Creative", "Enthusiastic", "Short & Direct"])
        if st.button("Generate My Letter"):
            with st.spinner("Writing your letter..."):
                letter = generate_cover_letter(st.session_state.last_cv_text, st.session_state.last_jd_text, tone)
                st.markdown("### Your Customized Cover Letter")
                st.markdown(f'<div class="letter-box">{letter}</div>', unsafe_allow_html=True)
                st.download_button("📥 Download as Text", letter, file_name="cover_letter.txt")

# --- 7. PAGE: INTERVIEW PREP ---
elif page == "🎙️ Interview Prep":
    st.title("Interview Preparation")
    st.info("Next step: Generating custom interview questions based on your CV gaps!")
