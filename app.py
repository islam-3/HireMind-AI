import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. الإعدادات والتصميم الثابت (CSS) ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    
    /* اللوجو الأنيق */
    .sidebar-logo { font-size: 1.8rem !important; font-weight: 800; color: #f0f6fc !important; text-align: center; margin-top: 15px; display: block; }
    
    /* العناوين الفرعية */
    .section-header { font-size: 1.5rem; font-weight: 700; margin-bottom: 10px; }

    /* صندوق الملخص الأخضر (Audit Box) */
    .audit-summary-box {
        background-color: #143224; 
        color: #aff5b4;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #238636;
        height: 100%;
    }

    /* بطاقات النتائج */
    .edge-card { background-color: #162a45; padding: 12px; border-radius: 5px; margin-bottom: 10px; color: #58a6ff; border: 1px solid #30363d; }
    .improve-card { background-color: #2b2d16; padding: 12px; border-radius: 5px; margin-bottom: 10px; color: #d29922; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المنطق البرمجي ---
if "current_result" not in st.session_state: st.session_state.current_result = None

def get_groq_analysis(cv_text, jd_text):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    prompt = f"Analyze CV vs JD. Return ONLY JSON: {{'score': float, 'strengths': [], 'weaknesses': [], 'summary': ''}}. CV: {cv_text[:5000]} JD: {jd_text[:2000]}"
    completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], response_format={"type": "json_object"})
    return json.loads(completion.choices[0].message.content)

# --- 3. القائمة الجانبية ---
with st.sidebar:
    st.markdown('<h1 class="sidebar-logo">🧠 CareerMind</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#8b949e; font-size:0.8rem;">Master Your Job Application</p>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigation", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep"])

# --- 4. الصفحة الرئيسية (القسم العلوي) ---
if page == "🔍 CV Matcher":
    st.title("Strategic Application Audit")
    
    # حاوية المدخلات (لضمان ثبات شكل الصفحة)
    input_container = st.container()
    with input_container:
        col_jd, col_cv = st.columns([1, 1], gap="large")
        with col_jd:
            st.markdown('<div class="section-header">📋 Job Description</div>', unsafe_allow_html=True)
            jd_input = st.text_area("Paste JD here...", height=230, label_visibility="collapsed")
        with col_cv:
            st.markdown('<div class="section-header">👤 Your CV</div>', unsafe_allow_html=True)
            v_name = st.text_input("Version Name:")
            file = st.file_uploader("Upload PDF:", type="pdf")
            
            if st.button("Analyze Match Score", use_container_width=True):
                if file and jd_input:
                    with st.spinner("Analyzing..."):
                        reader = PdfReader(file)
                        text = " ".join([p.extract_text() for p in reader.pages])
                        res = get_groq_analysis(text, jd_input)
                        st.session_state.current_result = {"name": v_name, "data": res}
                        st.rerun()

    # --- 5. قسم النتائج (منفصل تماماً لضمان عدم خربطة الصفحة) ---
    if st.session_state.current_result:
        res = st.session_state.current_result['data']
        st.markdown("<br><hr>", unsafe_allow_html=True)
        
        # توزيع النتائج: العداد والملخص بجانب بعضهما (مثل صورة image_68a1c3.png)
        result_top_row = st.container()
        with result_top_row:
            res_col1, res_col2 = st.columns([1, 2], gap="medium")
            with res_col1:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number", value=res['score'],
                    gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "#238636"}}
                ))
                fig.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, margin=dict(t=0, b=0))
                st.plotly_chart(fig, use_container_width=True)
            with res_col2:
                st.markdown(f"""
                    <div class="audit-summary-box">
                        <b>Audit for: {st.session_state.current_result['name']}</b><br><br>
                        {res['summary']}
                    </div>
                """, unsafe_allow_html=True)

        # توزيع البطاقات: عمودين متساويين في الأسفل
        st.markdown("<br>", unsafe_allow_html=True)
        cards_row = st.container()
        with cards_row:
            bot_col1, bot_col2 = st.columns(2, gap="medium")
            with bot_col1:
                st.markdown("### 🏆 Your Competitive Edges")
                for s in res['strengths']: st.markdown(f'<div class="edge-card">{s}</div>', unsafe_allow_html=True)
            with bot_col2:
                st.markdown("### 🛠️ Areas to Improve")
                for w in res['weaknesses']: st.markdown(f'<div class="improve-card">{w}</div>', unsafe_allow_html=True)
