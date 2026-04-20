import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. SETTINGS & REFINED CSS ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    
    .sidebar-logo { font-size: 1.8rem !important; font-weight: 800; color: #f0f6fc; text-align: center; margin-top: 15px; display: block; }
    .main-header { font-size: 1.3rem; font-weight: 700; margin-bottom: 10px; color: #f0f6fc; }

    /* صندوق الملخص الأخضر - تم تصغير الحجم وتحسين التناسق */
    .audit-box {
        background-color: #143224; 
        color: #aff5b4;
        padding: 15px;
        border-radius: 6px;
        border: 1px solid #238636;
        font-size: 0.95rem;
        line-height: 1.4;
        margin-top: 10px;
    }

    /* بطاقات النتائج */
    .card-edge { background-color: #162a45; padding: 10px; border-radius: 5px; margin-bottom: 8px; color: #58a6ff; border: 1px solid #30363d; font-size: 0.9rem; }
    .card-improve { background-color: #2b2d16; padding: 10px; border-radius: 5px; margin-bottom: 8px; color: #d29922; border: 1px solid #30363d; font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC ---
if "analysis_result" not in st.session_state: st.session_state.analysis_result = None

def run_analysis(cv_text, jd_text):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    prompt = f"Critically analyze CV vs JD. Provide a REALISTIC match score (0-10). Return ONLY JSON: {{'score': float, 'strengths': [], 'weaknesses': [], 'summary': ''}}. CV: {cv_text[:5000]} JD: {jd_text[:2000]}"
    chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], response_format={"type": "json_object"})
    return json.loads(chat.choices[0].message.content)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown('<h1 class="sidebar-logo">🧠 CareerMind</h1>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigation", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep"])

# --- 4. MAIN PAGE ---
if page == "🔍 CV Matcher":
    st.title("Strategic Application Audit")
    
    with st.container():
        col_left, col_right = st.columns(2, gap="large")
        with col_left:
            st.markdown('<div class="main-header">📋 Job Description</div>', unsafe_allow_html=True)
            jd_data = st.text_area("JD Content", height=200, label_visibility="collapsed")
        with col_right:
            st.markdown('<div class="main-header">👤 Your CV</div>', unsafe_allow_html=True)
            v_name = st.text_input("Version Name:")
            pdf_file = st.file_uploader("Upload PDF", type="pdf")
            
            if st.button("Analyze Match Score", use_container_width=True):
                if pdf_file and jd_data:
                    with st.spinner("Processing..."):
                        reader = PdfReader(pdf_file)
                        cv_txt = " ".join([p.extract_text() for p in reader.pages])
                        res = run_analysis(cv_txt, jd_data)
                        st.session_state.analysis_result = {"name": v_name, "data": res}
                        st.rerun()

    if st.session_state.analysis_result:
        data = st.session_state.analysis_result['data']
        st.markdown("<br><hr>", unsafe_allow_html=True)
        
        # ضبط التناسب بين العداد والملخص
        res_top_1, res_top_2 = st.columns([1, 2.2], gap="small")
        
        with res_top_1:
            # تصغير حجم العداد والنتيجة (number font size)
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=data['score'],
                number={'font': {'size': 40}}, # تصغير رقم النتيجة
                gauge={'axis': {'range': [0, 10], 'tickwidth': 1}, 'bar': {'color': "#238636"}}
            ))
            fig.update_layout(height=180, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, margin=dict(t=0, b=0, l=10, r=10))
            st.plotly_chart(fig, use_container_width=True)
            
        with res_top_2:
            st.markdown(f"""
                <div class="audit-box">
                    <b style='font-size:1.1rem; color:#ffffff;'>Audit for: {st.session_state.analysis_result['name']}</b><br>
                    {data['summary']}
                </div>
            """, unsafe_allow_html=True)

        # البطاقات في الأسفل
        st.markdown("<br>", unsafe_allow_html=True)
        res_bot_1, res_bot_2 = st.columns(2, gap="medium")
        with res_bot_1:
            st.markdown("### 🏆 Competitive Edges")
            for s in data['strengths']: st.markdown(f'<div class="card-edge">{s}</div>', unsafe_allow_html=True)
        with res_bot_2:
            st.markdown("### 🛠️ Areas to Improve")
            for w in data['weaknesses']: st.markdown(f'<div class="card-improve">{w}</div>', unsafe_allow_html=True)
