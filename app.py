import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json

# --- 1. التنسيق الأنيق والهادئ (Minimalist Design) ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

st.markdown("""
    <style>
    /* خلفية متدرجة خفيفة جداً لإعطاء حياة */
    .stApp { 
        background: linear-gradient(180deg, #0e1117 0%, #161b22 100%); 
        color: #e6edf3; 
    }
    
    /* تنسيق القائمة الجانبية */
    [data-testid="stSidebar"] { background-color: #0d1117 !important; border-right: 1px solid #30363d; }
    
    /* العناوين الملونة بنعومة */
    h1, h2, h3 { color: #58a6ff; font-family: 'Segoe UI', sans-serif; }
    
    /* بطاقات النتائج: شفافة ومنظمة */
    .result-box {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(240, 246, 252, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
    }
    
    /* نقاط القوة والضعف (تصميم احترافي) */
    .tag { padding: 10px 15px; border-radius: 8px; margin-bottom: 10px; font-size: 14px; display: flex; align-items: center; }
    .tag-plus { background: rgba(63, 185, 80, 0.1); border-left: 4px solid #238636; color: #56d364; }
    .tag-minus { background: rgba(248, 81, 73, 0.1); border-left: 4px solid #da3633; color: #ffa198; }
    
    /* تحسين شكل الأزرار */
    div.stButton > button {
        border-radius: 8px;
        background-color: #238636;
        color: white;
        border: none;
        font-weight: bold;
        padding: 0.5rem 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الوظائف الأساسية ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
if "history" not in st.session_state: st.session_state.history = []

def read_pdf(file):
    reader = PdfReader(file)
    return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

# --- 3. القائمة الجانبية (Navigation) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🧠 CareerMind</h2>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("القائمة الرئيسية", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
    
    if st.session_state.history:
        st.markdown("<br><b>آخر العمليات:</b>", unsafe_allow_html=True)
        for item in reversed(st.session_state.history[-3:]):
            st.caption(f"✅ {item['name']} ({item['score']}/10)")

# --- 4. صفحة CV Matcher (ترتيب عمودي سليم) ---
if page == "🔍 CV Matcher":
    st.title("Strategic Application Audit")
    
    # قسم المدخلات: جنباً إلى جنب بوضوح
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.subheader("📋 وصف الوظيفة")
        jd_input = st.text_area("انسخ متطلبات الوظيفة هنا", height=250, label_visibility="collapsed")
    with col2:
        st.subheader("👤 ملف المتقدم")
        v_name = st.text_input("اسم النسخة (مثال: سيرة ذاتية - مبرمج)")
        pdf_file = st.file_uploader("ارفع السيرة الذاتية (PDF)", type="pdf")
        if st.button("بدء التحليل الذكي", use_container_width=True):
            if pdf_file and jd_input:
                with st.spinner("جاري التحليل..."):
                    cv_txt = read_pdf(pdf_file)
                    p = f"Analyze CV vs JD. Return JSON: {{'score': float, 'strengths': [], 'weaknesses': [], 'summary': ''}}. CV: {cv_txt[:3000]} JD: {jd_input[:1500]}"
                    res = json.loads(client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": p}], response_format={"type": "json_object"}).choices[0].message.content)
                    st.session_state.last_res = res
                    st.session_state.history.append({"name": v_name, "score": res['score']})
                    st.rerun()

    # قسم النتائج: يظهر فقط بعد التحليل وبشكل مرتب
    if "last_res" in st.session_state:
        st.markdown("---")
        data = st.session_state.last_res
        
        # توزيع النتائج: العداد يسار والملخص يمين
        res_col1, res_col2 = st.columns([1, 2], gap="medium")
        with res_col1:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=data['score'], number={'suffix': "/10", 'font':{'color':'white'}},
                gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "#238636"}, 'bgcolor': "#30363d"}))
            fig.update_layout(height=250, margin=dict(t=30, b=0), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        with res_col2:
            st.markdown(f'<div class="result-box"><b>📝 ملخص الذكاء الاصطناعي:</b><br><p style="color:#8b949e; margin-top:10px;">{data["summary"]}</p></div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # نقاط القوة والتحسين جنباً إلى جنب
        list_col1, list_col2 = st.columns(2)
        with list_col1:
            st.markdown("### 🏆 نقاط القوة")
            for s in data['strengths']: st.markdown(f'<div class="tag tag-plus">● {s}</div>', unsafe_allow_html=True)
        with list_col2:
            st.markdown("### 🛠️ فرص التحسين")
            for w in data['weaknesses']: st.markdown(f'<div class="tag tag-minus">● {w}</div>', unsafe_allow_html=True)

# --- 5. صفحة Cover Letter (بسيطة ومباشرة) ---
elif page == "✉️ Cover Letter":
    st.title("AI Cover Letter Architect")
    st.markdown('<div class="result-box">ارفع ملفك وضع وصف الوظيفة لنقوم بصياغة رسالة احترافية مخصصة لك.</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2, gap="large")
    with c1:
        cl_jd = st.text_area("وصف الوظيفة المستهدفة", height=200)
        cl_pdf = st.file_uploader("السيرة الذاتية (اختياري)", type="pdf")
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("توليد الرسالة الآن", use_container_width=True):
            with st.spinner("جاري الكتابة..."):
                cv_text = read_pdf(cl_pdf) if cl_pdf else "Generic background"
                p = f"Write a professional cover letter for this JD: {cl_jd[:1000]} based on: {cv_text[:2000]}"
                st.session_state.gen_cl = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": p}]).choices[0].message.content
                st.rerun()

    if "gen_cl" in st.session_state:
        st.markdown("---")
        st.subheader("📄 المسودة المقترحة")
        st.text_area("", value=st.session_state.gen_cl, height=400)
