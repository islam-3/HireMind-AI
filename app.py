import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json
import pandas as pd

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="CareerMind AI", layout="wide")

# CSS لتحسين المظهر الفخم وتنسيق البطاقات
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .sidebar-logo { font-size: 1.8rem; font-weight: 900; color: #f0f6fc; text-align: center; margin-bottom: 0px; }
    .edge-card { background-color: #1c2b1d; border-left: 5px solid #238636; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    .improve-card { background-color: #2d1a1a; border-left: 5px solid #da3633; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    .stButton>button { background-color: #238636 !important; color: white !important; border-radius: 8px; border: none; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALIZE GROQ CLIENT ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("API Key configuration error. Please check your Secrets.")
    st.stop()

def get_groq_analysis(cv_text, jd_text):
    # تم تعديل البرومبت هنا ليعطي درجات منطقية (7-10) بدلاً من 0.8
    prompt = f"""
    As a Senior Career Coach, evaluate this CV against the Job Description.
    
    SCORING RULES:
    - 8.5-10: Perfect match, has almost all required skills.
    - 6.5-8.4: Good match, has core skills but lacks some secondary ones.
    - 4.0-6.4: Partial match, has basics but significant gaps.
    - 0-3.9: Poor match, different field or missing core requirements.

    Return ONLY a valid JSON object with this exact structure:
    {{
      "score": float,
      "strengths": ["list 3 key competitive edges"],
      "weaknesses": ["list 3 specific areas to improve"],
      "summary": "one encouraging and professional sentence"
    }}

    CV Text: {cv_text[:6000]}
    JD Text: {jd_text[:2000]}
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        return {"score": 0.0, "strengths": ["Analysis Error"], "weaknesses": [str(e)[:30]], "summary": "Technical connection issue."}

# --- 3. SESSION STATE ---
if "history" not in st.session_state: st.session_state.history = []
if "current_result" not in st.session_state: st.session_state.current_result = None

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown('<p class="sidebar-logo">🚀 CareerMind</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#8b949e; font-size:0.8rem;">Master Your Job Application</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    page = st.radio("Navigation", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep"])
    
    st.markdown("---")
    if st.session_state.history:
        st.markdown("**Your Top CV Versions:**")
        # ترتيب الجدول من الأعلى للأقل درجة
        hist_df = pd.DataFrame(st.session_state.history).sort_values(by="Score", ascending=False)
        for _, row in hist_df.iterrows():
            color = "#238636" if row['Score'] >= 7 else "#d29922"
            st.markdown(f"<span style='color:{color}; font-weight:bold;'>{row['Score']}</span> - {row['Name']}", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🗑️ Reset All Sessions"):
        st.session_state.history = []
        st.session_state.current_result = None
        st.rerun()

# --- 5. PAGE: CV MATCHER ---
if page == "🔍 CV Matcher":
    st.title("Optimize Your Application")
    st.write("Compare your resume with any job description to find missing keywords and boost your score.")
    
    c1, c2 = st.columns(2, gap="large")
    
    with c1:
        st.subheader("📋 Targeted Job Description")
        jd_input = st.text_area("Paste the job requirements here...", height=250, label_visibility="collapsed")
        
    with c2:
        st.subheader("📄 Your CV (PDF)")
        version_name = st.text_input("Name this version (e.g. Frontend Focus):")
        file = st.file_uploader("Upload PDF:", type="pdf")
        
        if file and st.button("Check My Match Score"):
            if jd_input and version_name:
                with st.spinner("AI is analyzing your match..."):
                    reader = PdfReader(file)
                    text = " ".join([p.extract_text() or "" for p in reader.pages])
                    res = get_groq_analysis(text, jd_input)
                    st.session_state.current_result = {"name": version_name, "data": res}
                    st.session_state.history.append({"Name": version_name, "Score": res['score']})
                    st.rerun()

    # عرض النتائج
    if st.session_state.current_result:
        res = st.session_state.current_result['data']
        st.markdown("---")
        res_c1, res_c2 = st.columns([1, 2])
        
        with res_c1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number", 
                value=res['score'],
                gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "#8b949e"}}
            ))
            fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
            st.plotly_chart(fig, use_container_width=True)
            
        with res_c2:
            st.markdown(f"### Verdict for: {st.session_state.current_result['name']}")
            st.info(res['summary'])
            
        s_col1, s_col2 = st.columns(2)
        with s_col1:
            st.markdown("### 🏆 Your Competitive Edges")
            for s in res['strengths']: st.markdown(f'<div class="edge-card">{s}</div>', unsafe_allow_html=True)
        with s_col2:
            st.markdown("### 🛠️ Areas to Improve")
            for w in res['weaknesses']: st.markdown(f'<div class="improve-card">{w}</div>', unsafe_allow_html=True)

# --- 6. PAGE: COVER LETTER ---
elif page == "✉️ Cover Letter":
    st.title("AI Cover Letter Generator")
    st.write("We will use your CV data and the JD to write a compelling letter.")
    st.warning("Feature Coming Up: We are building the AI prompt for this page next!")

# --- 7. PAGE: INTERVIEW PREP ---
elif page == "🎙️ Interview Prep":
    st.title("Interview Preparation")
    st.write("Prepare for questions that target your specific gaps.")
    st.warning("Feature Coming Up: This will generate custom questions based on your CV audit!")
