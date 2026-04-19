import streamlit as st
import plotly.graph_objects as go
from google import genai
from PyPDF2 import PdfReader
import json
import pandas as pd

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="HireMind AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117 !important; color: #ffffff !important; }
    .block-container { padding-top: 1rem !important; }

    /* ضبط حجم اللوغو بدقة وإجباره على التغيير */
    .sidebar-logo {
        font-size: 1.5rem !important; /* حجم أصغر واحترافي جداً */
        font-weight: 800 !important;
        color: #f0f6fc !important;
        text-align: center !important;
        margin-bottom: 0px !important;
        text-shadow: 2px 2px 4px #000000;
    }
    .sidebar-subtitle {
        font-size: 0.85rem !important;
        color: #8b949e !important;
        text-align: center !important;
        margin-bottom: 20px !important;
        letter-spacing: 1px;
    }

    /* تحسين شكل القائمة الجانبية */
    [data-testid="stSidebar"] { 
        background-color: #161b22 !important; 
        border-right: 1px solid #30363d !important; 
        min-width: 250px !important;
    }

    .stTextArea textarea { background-color: #161b22 !important; color: #ffffff !important; border: 1px solid #30363d !important; height: 300px !important; }
    
    .strength-card { background-color: #1c2b1d; border-left: 5px solid #238636; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    .weakness-card { background-color: #2d1a1a; border-left: 5px solid #da3633; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    
    .clear-btn button { background-color: #da363310 !important; color: #da3633 !important; border: 1px solid #da363333 !important; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if "comparison_list" not in st.session_state: 
    st.session_state.comparison_list = []

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown('<p class="sidebar-logo">🧠 HireMind AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-subtitle">Enterprise Recruitment</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("📊 Session Stats")
    # التأكد من حساب العدد مباشرة من القائمة
    current_count = len(st.session_state.comparison_list)
    st.write(f"Processed Candidates: **{current_count}**")
    
    if current_count > 0:
        avg = sum(c['Score'] for c in st.session_state.comparison_list) / current_count
        st.write(f"Global Match Avg: **{avg:.1f}/10**")
    
    st.markdown("<br>" * 12, unsafe_allow_html=True)
    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    if st.button("🗑️ Clear All Sessions"):
        st.session_state.comparison_list = []
        if "last_res" in st.session_state: del st.session_state.last_res
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. AI CORE LOGIC ---
API_KEY = "AIzaSyBWxCNTFI_XlhE_i7lFtvJQgwNPfCQxhqE"
client = genai.Client(api_key=API_KEY)

def get_detailed_evaluation(cv_text, jd_text):
    prompt = f"Expert HR. Compare CV & JD. Score 0-10 only. JSON: {{'score': float, 'strengths': [], 'weaknesses': [], 'summary': ''}} CV: {cv_text} JD: {jd_text}"
    try:
        response = client.models.generate_content(model="gemini-flash-latest", contents=prompt)
        res = json.loads(response.text.replace("```json", "").replace("```", "").strip())
        if res['score'] > 10: res['score'] = res['score'] / 10
        return res
    except: return {"score": 0, "strengths": ["Analysis Error"], "weaknesses": [], "summary": "N/A"}

# --- 5. MAIN INTERFACE ---
st.title("Strategic Talent Analysis")
st.markdown("---")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("💼 Job Description")
    jd_input = st.text_area("Requirements", height=300, label_visibility="collapsed", placeholder="Paste the Job Description here...")

with col2:
    st.subheader("👤 Candidate CV")
    c_name = st.text_input("Candidate Name:", placeholder="e.g. John Doe")
    uploaded_file = st.file_uploader("Upload PDF:", type="pdf")
    
    if uploaded_file and st.button("Execute Strategic Audit"):
        if not c_name:
            st.warning("Please enter candidate name before starting.")
        else:
            with st.spinner("Analyzing Professional Background..."):
                reader = PdfReader(uploaded_file)
                cv_text = "".join([p.extract_text() or "" for p in reader.pages])
                result = get_detailed_evaluation(cv_text, jd_input)
                
                # تخزين النتيجة في الـ Session
                st.session_state.last_res = result
                st.session_state.last_name = c_name
                st.session_state.comparison_list.append({"Name": c_name, "Score": result['score']})
                st.rerun() # لإجبار القائمة الجانبية على التحديث فوراً

# عرض النتائج
if "last_res" in st.session_state:
    res = st.session_state.last_res
    st.markdown("---")
    
    c_res1, c_res2 = st.columns([1, 2])
    with c_res1:
        fig = go.Figure(go.Indicator(mode="gauge+number", value=res['score'],
                        gauge={'axis': {'range': [0, 10], 'tickmode': "linear", 'dtick': 1}, 
                               'bar': {'color': "#58a6ff"}, 'bgcolor': "#0d1117"}))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=250)
        st.plotly_chart(fig, use_container_width=True)
    
    with c_res2:
        st.markdown(f"### 📋 Audit Verdict: {st.session_state.last_name}")
        st.write(res['summary'])

    r1, r2 = st.columns(2)
    with r1:
        st.markdown("### ✅ Strengths")
        for s in res['strengths']: st.markdown(f'<div class="strength-card">{s}</div>', unsafe_allow_html=True)
    with r2:
        st.markdown("### ⚠️ Gaps")
        for w in res['weaknesses']: st.markdown(f'<div class="weakness-card">{w}</div>', unsafe_allow_html=True)

if st.session_state.comparison_list:
    st.markdown("---")
    st.subheader("📊 Ranking Leaderboard")
    df = pd.DataFrame(st.session_state.comparison_list).sort_values(by="Score", ascending=False)
    st.table(df)