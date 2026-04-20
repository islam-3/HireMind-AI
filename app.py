import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. الإعدادات والتنسيق (CSS) ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .sidebar-logo { font-size: 1.8rem !important; font-weight: 800; color: #f0f6fc; text-align: center; margin-top: 15px; display: block; }
    .audit-box { background-color: #143224; color: #aff5b4; padding: 18px; border-radius: 8px; border: 1px solid #238636; margin-top: 35px; min-height: 120px; }
    .card-edge { background-color: #162a45; padding: 12px; border-radius: 6px; margin-bottom: 10px; color: #58a6ff; border: 1px solid #30363d; }
    .card-improve { background-color: #2b2d16; padding: 12px; border-radius: 6px; margin-bottom: 10px; color: #d29922; border: 1px solid #30363d; }
    .history-item { padding: 10px; border-radius: 5px; background: #21262d; margin-bottom: 5px; border-left: 4px solid #238636; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة الجلسة (لضمان عدم اختفاء البيانات) ---
if "history" not in st.session_state: st.session_state.history = []
if "analysis_result" not in st.session_state: st.session_state.analysis_result = None

def run_analysis(cv_text, jd_text):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    # برومبت أكثر دقة لضمان تفاوت النتائج بناءً على الخبرات الفعلية
    prompt = f"""
    Compare this CV against the JD with extreme precision. 
    Assign a UNIQUE score based on exact keyword matching, years of experience, and skill relevance.
    Avoid generic scores like 6.5 unless it's a perfect match for that number.
    Return ONLY JSON: 
    {{
      "score": float (0.0-10.0), 
      "strengths": ["list 3 specific strengths"], 
      "weaknesses": ["list 3 specific gaps"], 
      "summary": "1-2 sentences of professional feedback"
    }}
    CV: {cv_text[:5000]} | JD: {jd_text[:2000]}
    """
    chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], response_format={"type": "json_object"})
    return json.loads(chat.choices[0].message.content)

# --- 3. القائمة الجانبية (استعادة سجل النتائج) ---
with st.sidebar:
    st.markdown('<h1 class="sidebar-logo">🧠 CareerMind</h1>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigation", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep"])
    
    # قسم "Top Versions" كما في الصورة (image_67b61d.png)
    if st.session_state.history:
        st.markdown("<br><b>Your Top Versions:</b>", unsafe_allow_html=True)
        for item in reversed(st.session_state.history):
            st.markdown(f'<div class="history-item">⭐ {item["score"]}/10 - {item["name"]}</div>', unsafe_allow_html=True)
        
        if st.button("Reset Sessions"):
            st.session_state.history = []
            st.session_state.analysis_result = None
            st.rerun()

# --- 4. الصفحة الرئيسية ---
if page == "🔍 CV Matcher":
    st.title("Strategic Application Audit")
    
    col_left, col_right = st.columns(2, gap="large")
    with col_left:
        st.markdown('### 📋 Job Description')
        jd_data = st.text_area("JD Content", height=200, label_visibility="collapsed")
    with col_right:
        st.markdown('### 👤 Your CV')
        v_name = st.text_input("Version Name:", placeholder="e.g. Islam - V1")
        pdf_file = st.file_uploader("Upload PDF", type="pdf")
        
        if st.button("Analyze Match Score", use_container_width=True):
            if pdf_file and jd_data:
                with st.spinner("Calculating unique score..."):
                    reader = PdfReader(pdf_file)
                    cv_txt = " ".join([p.extract_text() for p in reader.pages])
                    res = run_analysis(cv_txt, jd_data)
                    
                    # حفظ في السجل الحالي والنتائج
                    st.session_state.analysis_result = {"name": v_name, "data": res}
                    st.session_state.history.append({"name": v_name, "score": res['score']})
                    st.rerun()

    # عرض النتائج
    if st.session_state.analysis_result:
        data = st.session_state.analysis_result['data']
        st.markdown("<br><hr>", unsafe_allow_html=True)
        
        res_top_1, res_top_2 = st.columns([1, 2.5], gap="medium")
        with res_top_1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=data['score'],
                number={'font': {'size': 32}, 'suffix': "/10"}, 
                gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "#238636"}}
            ))
            fig.update_layout(height=180, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, margin=dict(t=0, b=0, l=10, r=10))
            st.plotly_chart(fig, use_container_width=True)
        with res_top_2:
            st.markdown(f'<div class="audit-box"><b>Audit for: {st.session_state.analysis_result["name"]}</b><br><br>{data["summary"]}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        res_bot_1, res_bot_2 = st.columns(2)
        with res_bot_1:
            st.markdown("#### 🏆 Competitive Edges")
            for s in data['strengths']: st.markdown(f'<div class="card-edge">{s}</div>', unsafe_allow_html=True)
        with res_bot_2:
            st.markdown("#### 🛠️ Areas to Improve")
            for w in data['weaknesses']: st.markdown(f'<div class="card-improve">{w}</div>', unsafe_allow_html=True)
