import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from PyPDF2 import PdfReader
import json
import pandas as pd

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="HireMind AI", layout="wide")

# CSS لتعديل الألوان والمظهر الفخم
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .sidebar-logo { font-size: 1.5rem; font-weight: 800; color: #f0f6fc; text-align: center; margin-bottom: 20px; }
    .strength-card { background-color: #1c2b1d; border-left: 5px solid #238636; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    .weakness-card { background-color: #2d1a1a; border-left: 5px solid #da3633; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    .stButton>button { background-color: #30363d !important; color: white !important; width: 100%; border-radius: 8px; border: 1px solid #8b949e; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALIZE GROQ CLIENT ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Missing API Key in Streamlit Secrets!")
    st.stop()

def get_groq_analysis(cv_text, jd_text):
    prompt = f"""
    As an expert HR Auditor, compare this CV with the Job Description.
    Return ONLY a valid JSON object with this structure:
    {{
      "score": float (0-10),
      "strengths": ["list of 3 key strengths"],
      "weaknesses": ["list of 3 gaps/weaknesses"],
      "summary": "one professional sentence overview"
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
        return {"score": 0, "strengths": ["Audit Fail"], "weaknesses": [str(e)[:30]], "summary": "Technical check required."}

# --- 3. SESSION STATE ---
if "history" not in st.session_state: st.session_state.history = []
if "current_result" not in st.session_state: st.session_state.current_result = None

# --- 4. SIDEBAR (التصميم الجديد والفخم) ---
with st.sidebar:
    st.markdown('<p style="font-size: 2.2rem; font-weight: 900; color: #f0f6fc; text-align: center; margin-bottom: 0px;">🧠 HireMind</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 0.9rem; color: #8b949e; text-align: center; margin-bottom: 30px;">Strategic AI Auditing</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    total_candidates = len(st.session_state.history)
    st.markdown(f"""
        <div style="background: linear-gradient(145deg, #161b22, #30363d); padding: 20px; border-radius: 15px; border: 1px solid #484f58; text-align: center;">
            <p style="color: #8b949e; margin: 0; font-size: 0.8rem; text-transform: uppercase;">Total Candidates</p>
            <p style="color: #ffffff; margin: 0; font-size: 2.5rem; font-weight: bold;">{total_candidates}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.history:
        st.markdown('<p style="color: #f0f6fc; font-weight: bold; font-size: 1.1rem;">📝 History</p>', unsafe_allow_html=True)
        for entry in reversed(st.session_state.history[-5:]):
            color = "#238636" if entry['Score'] >= 7 else "#d29922" if entry['Score'] >= 5 else "#da3633"
            st.markdown(f"""
                <div style="padding: 10px; border-bottom: 1px solid #30363d; font-size: 0.9rem;">
                    <span style="color: {color}; font-weight: bold;">{entry['Score']}/10</span> 
                    <span style="color: #c9d1d9; margin-left: 10px;">{entry['Name']}</span>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Reset Sessions"):
        st.session_state.history = []
        st.session_state.current_result = None
        st.rerun()

# --- 5. MAIN INTERFACE ---
st.title("Strategic Talent Analysis")
c1, c2 = st.columns(2, gap="large")

with c1:
    st.subheader("💼 Job Description")
    jd_input = st.text_area("Paste JD here...", height=250, label_visibility="collapsed")

with c2:
    st.subheader("👤 Candidate CV")
    name = st.text_input("Candidate Name:")
    file = st.file_uploader("Upload PDF:", type="pdf")
    
    if file and st.button("Run Strategic Audit"):
        if name and jd_input:
            with st.spinner("AI Analysis in progress..."):
                reader = PdfReader(file)
                text = " ".join([p.extract_text() or "" for p in reader.pages])
                res = get_groq_analysis(text, jd_input)
                st.session_state.current_result = {"name": name, "data": res}
                st.session_state.history.append({"Name": name, "Score": res['score']})
                st.rerun()

# --- 6. DISPLAY RESULTS ---
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
        st.markdown(f"### Verdict: {st.session_state.current_result['name']}")
        st.info(res['summary'])
        
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        st.markdown("### ✅ Strengths")
        for s in res['strengths']: st.markdown(f'<div class="strength-card">{s}</div>', unsafe_allow_html=True)
    with s_col2:
        st.markdown("### ⚠️ Gaps")
        for w in res['weaknesses']: st.markdown(f'<div class="weakness-card">{w}</div>', unsafe_allow_html=True)

if st.session_state.history:
    st.markdown("---")
    st.subheader("📊 Ranking Leaderboard")
    st.table(pd.DataFrame(st.session_state.history).sort_values(by="Score", ascending=False))
