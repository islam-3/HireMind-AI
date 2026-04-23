import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. UI ENHANCEMENTS (ألوان حيوية مع هيكل ثابت) ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

st.markdown("""
    <style>
    /* تحسين الخلفية العامة */
    .stApp { 
        background: radial-gradient(circle at top right, #1a1f25, #0e1117); 
        color: #e6edf3; 
    }
    
    /* تنسيق العناوين الجانبية والقوائم */
    [data-testid="stSidebar"] { background-color: #0d1117 !important; border-right: 1px solid #30363d; }
    
    /* بطاقات النتائج الملونة (بدون تغيير الترتيب) */
    .result-card {
        background: rgba(22, 27, 34, 0.6);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    
    /* لمسة جمالية لنقاط القوة والضعف */
    .strength-tag {
        background: rgba(46, 160, 67, 0.15);
        color: #3fb950;
        padding: 8px 12px;
        border-radius: 6px;
        border-left: 4px solid #238636;
        margin-bottom: 8px;
        font-weight: 500;
    }
    .weakness-tag {
        background: rgba(248, 81, 73, 0.1);
        color: #f85149;
        padding: 8px 12px;
        border-radius: 6px;
        border-left: 4px solid #da3633;
        margin-bottom: 8px;
        font-weight: 500;
    }
    
    /* صندوق الملخص الاحترافي */
    .summary-text {
        background: linear-gradient(90deg, rgba(35, 134, 54, 0.1), transparent);
        padding: 15px;
        border-radius: 8px;
        border: 1px solid rgba(48, 54, 61, 0.5);
        line-height: 1.6;
    }
    
    /* أزرار مفعمة بالحيوية */
    div.stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
        color: white;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(46, 160, 67, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC ---
if "history" not in st.session_state: st.session_state.history = []
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def read_pdf(file):
    reader = PdfReader(file)
    return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #58a6ff;'>🧠 CareerMind</h2>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigation", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
    
    if st.session_state.history:
        st.markdown("<br><b>Activity Trace:</b>", unsafe_allow_html=True)
        for item in reversed(st.session_state.history[-3:]):
            st.caption(f"📍 {item['name']} - Score: {item['score']}")
        if st.button("Reset Sessions", use_container_width=True):
            st.session_state.history = []; st.rerun()

# --- 4. PAGE: CV MATCHER (ترتيب ثابت مع لمسات ألوان) ---
if page == "🔍 CV Matcher":
    st.title("Strategic Application Audit")
    
    # قسم المدخلات (أعمدة متوازنة)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("#### 📋 Job Description")
        jd_input = st.text_area("Input JD", height=250, label_visibility="collapsed", placeholder="Paste the job requirements here...")
    with col2:
        st.markdown("#### 👤 Candidate File")
        v_name = st.text_input("Version Name:", placeholder="e.g. Islam - Senior Role")
        pdf_file = st.file_uploader("Upload CV (PDF)", type="pdf")
        if st.button("Launch Analysis", use_container_width=True):
            if pdf_file and jd_input:
                with st.spinner("Processing Data..."):
                    cv_txt = read_pdf(pdf_file)
                    p = f"Analyze CV vs JD. Return JSON: {{'score': float, 'strengths': [], 'weaknesses': [], 'summary': ''}}. CV: {cv_txt[:3500]} JD: {jd_input[:1500]}"
                    res = json.loads(client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": p}], response_format={"type": "json_object"}).choices[0].message.content)
                    st.session_state.last_res = res
                    st.session_state.history.append({"name": v_name, "score": res['score']})
                    st.rerun()

    # عرض النتائج (بنظام البطاقات الشفافة دون تغيير الترتيب)
    if "last_res" in st.session_state:
        data = st.session_state.last_res
        st.markdown("---")
        
        # الصف الأول: العداد والملخص
        res_col1, res_col2 = st.columns([1, 2], gap="medium")
        with res_col1:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=data['score'], number={'suffix': "/10", 'font':{'color':'#ffffff'}},
                gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "#238636"}, 'bgcolor': "#30363d"}))
            fig.update_layout(height=230, margin=dict(t=30, b=0, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        with res_col2:
            st.markdown(f'<div class="summary-text"><b>AI Analysis Verdict:</b><br>{data["summary"]}</div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # الصف الثاني: النقاط جنباً إلى جنب
        list_col1, list_col2 = st.columns(2, gap="medium")
        with list_col1:
            st.markdown("<p style='color:#3fb950; font-weight:bold;'>🏆 Competitive Edges</p>", unsafe_allow_html=True)
            for s in data['strengths']: st.markdown(f'<div class="strength-tag">✓ {s}</div>', unsafe_allow_html=True)
        with list_col2:
            st.markdown("<p style='color:#f85149; font-weight:bold;'>🛠️ Areas to Improve</p>", unsafe_allow_html=True)
            for w in data['weaknesses']: st.markdown(f'<div class="weakness-tag">⚠ {w}</div>', unsafe_allow_html=True)

# --- 5. PAGE: COVER LETTER (تصميم متوازن) ---
elif page == "✉️ Cover Letter":
    st.title("AI Cover Letter Architect")
    st.info("Upload your CV and provide the Job Description to generate a tailored letter.")
    
    cl_col1, cl_col2 = st.columns(2, gap="large")
    with cl_col1:
        cl_jd = st.text_area("Target Job Description", height=200)
        cl_pdf = st.file_uploader("Use CV Context (Optional)", type="pdf")
    with cl_col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Generate Tailored Letter", use_container_width=True):
            with st.spinner("Architecting your letter..."):
                cv_text = read_pdf(cl_pdf) if cl_pdf else "Generic Professional Background"
                p = f"Write a high-impact cover letter. JD: {cl_jd[:1000]} CV: {cv_text[:2000]}"
                st.session_state.gen_cl = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": p}]).choices[0].message.content
                st.rerun()

    if "gen_cl" in st.session_state:
        st.markdown("---")
        st.markdown("#### ✨ Generated Draft")
        st.text_area("Final Output", value=st.session_state.gen_cl, height=450, label_visibility="collapsed")
