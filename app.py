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
    .status-card { background: linear-gradient(145deg, #161b22, #30363d); padding: 15px; border-radius: 12px; border: 1px solid #484f58; text-align: center; }
    .stButton>button { background-color: #238636 !important; color: white !important; border-radius: 8px; border: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALIZE GROQ ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("API Key configuration error.")
    st.stop()

# --- 3. SESSION STATE ---
if "history" not in st.session_state: st.session_state.history = []
if "current_result" not in st.session_state: st.session_state.current_result = None

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown('<p class="sidebar-logo">🚀 CareerMind</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#8b949e; font-size:0.8rem;">Master Your Job Application</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # اختيار الصفحة
    page = st.radio("Navigation", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep"])
    
    st.markdown("---")
    if st.session_state.history:
        st.markdown("**Your Top Versions:**")
        hist_df = pd.DataFrame(st.session_state.history).sort_values(by="Score", ascending=False)
        for _, row in hist_df.iterrows():
            st.write(f"⭐ {row['Score']}/10 - {row['Name']}")

# --- 5. PAGE: CV MATCHER ---
if page == "🔍 CV Matcher":
    st.title("Optimize Your Application")
    st.write("Compare your CV against the Job Description to find gaps and improve your score.")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.subheader("📋 Targeted Job Description")
        jd_input = st.text_area("Paste the job requirements here...", height=200)
        
    with col2:
        st.subheader("📄 Your CV (PDF)")
        version_name = st.text_input("Version Name (e.g., CV with Python focus):")
        file = st.file_uploader("Upload your resume:", type="pdf")
        
        if file and st.button("Analyze My Match Score"):
            if jd_input and version_name:
                with st.spinner("AI is auditing your profile..."):
                    reader = PdfReader(file)
                    text = " ".join([p.extract_text() or "" for p in reader.pages])
                    
                    # نستخدم نفس وظيفة الـ Groq السابقة
                    prompt = f"Compare this CV to JD. Return JSON: {{'score':.., 'strengths':[], 'weaknesses':[], 'summary':''}}. CV: {text[:5000]} JD: {jd_input[:2000]}"
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        response_format={"type": "json_object"}
                    )
                    res = json.loads(completion.choices[0].message.content)
                    st.session_state.current_result = {"name": version_name, "data": res}
                    st.session_state.history.append({"Name": version_name, "Score": res['score']})
                    st.rerun()

    if st.session_state.current_result:
        res = st.session_state.current_result['data']
        st.markdown("---")
        # عرض النتائج بنفس التنسيق الفخم السابق مع تعديل المسميات
        r1, r2 = st.columns([1, 2])
        with r1:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=res['score'], gauge={'axis': {'range': [0, 10]}}))
            fig.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
            st.plotly_chart(fig, use_container_width=True)
        with r2:
            st.success(f"Audit for: {st.session_state.current_result['name']}")
            st.write(res['summary'])
            
        c_a, c_b = st.columns(2)
        with c_a:
            st.markdown("### 🏆 Your Competitive Edges")
            for s in res['strengths']: st.info(s)
        with c_b:
            st.markdown("### 🛠️ Areas to Improve")
            for w in res['weaknesses']: st.warning(w)

# --- 6. PLACEHOLDERS FOR NEW PAGES ---
elif page == "✉️ Cover Letter":
    st.title("AI Cover Letter Generator")
    st.info("This feature will use your uploaded CV and JD to write a perfect letter. (Coming in the next step)")

elif page == "🎙️ Interview Prep":
    st.title("Interview Preparation")
    st.info("Prepare for questions based on your specific profile. (Coming in the next step)")
