import streamlit as st
import os
try:
    from groq import Groq
except ImportError:
    st.error("Please install groq: pip install groq")
    st.stop()

# --- إعدادات الصفحة ---
st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

# --- CSS (ثبات الواجهة الأولى وتنسيق الأدوات الداخلية) ---
st.markdown("""
    <style>
    [data-testid="stAppViewBlockContainer"] {
        padding-top: 2rem !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
    }

    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a1f29 0%, #050505 100%);
        color: #e6edf3;
    }

    /* الواجهة الأولى */
    .hero-container { text-align: center; width: 100%; margin-bottom: 40px; }
    .main-title {
        font-size: 5rem !important;
        font-weight: 900;
        background: linear-gradient(90deg, #58a6ff, #3fb950);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    .tagline { color: #8b949e; letter-spacing: 5px; text-transform: uppercase; text-align: center; }
    
    /* تنسيق الكروت في الواجهة الأولى */
    .feature-grid { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 50px; }
    .service-card { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 30px 15px; width: 220px; text-align: center; }

    /* تنسيق الأزرار الخضراء */
    div.stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        padding: 10px 30px !important;
        font-size: 1.1rem !important;
        border-radius: 50px !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 10px 20px rgba(35, 134, 54, 0.2) !important;
    }

    /* توسيط زر التحليل داخل الصفحات */
    .center-btn { display: flex; justify-content: center; width: 100%; margin-top: 20px; }

    /* تنسيق صناديق الإدخال */
    .stTextArea textarea, .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    .tool-header {
        background: rgba(88, 166, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 25px;
        border-left: 5px solid #58a6ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- إعداد Groq Client ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "entered" not in st.session_state:
    st.session_state.entered = False

# --- الوظائف المساعدة (AI logic) ---
def get_ai_response(prompt):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# --- التنقل بين الصفحات ---
if not st.session_state.entered:
    # الصفحة الرئيسية (ثابتة)
    st.markdown('<div class="hero-container"><h1 class="main-title">CareerMind AI</h1><p class="tagline">Architecting Your Professional Future</p></div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="feature-grid">
            <div class="service-card"><h3>🔍 Audit</h3><p>CV & JD Alignment</p></div>
            <div class="service-card"><h3>✉️ Script</h3><p>Cover Letter Builder</p></div>
            <div class="service-card"><h3>🎙️ Master</h3><p>Interview Simulator</p></div>
            <div class="service-card"><h3>💰 Value</h3><p>Salary Estimation</p></div>
        </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([2, 1, 2])
    with col:
        if st.button("Access Professional Suite", use_container_width=True):
            st.session_state.entered = True
            st.rerun()

else:
    # الواجهة الداخلية
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;'>🧠 CareerMind</h2>", unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("Executive Tools", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        for _ in range(10): st.sidebar.write("") # دفع زر الخروج لأسفل
        if st.button("Logout", use_container_width=True):
            st.session_state.entered = False
            st.rerun()

    # --- صفحة CV Matcher ---
    if page == "🔍 CV Matcher":
        st.markdown('<div class="tool-header"><h2>CV & JD Audit</h2><p>Check how well your profile matches the job requirements.</p></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            jd = st.text_area("📝 Job Description", height=300, placeholder="Paste the full job description here...")
        with col2:
            cv = st.text_area("📄 Your CV (Text Content)", height=300, placeholder="Paste your CV text content here...")
        
        if st.button("Start AI Analysis", use_container_width=True):
            if jd and cv:
                with st.spinner("Analyzing alignment..."):
                    prompt = f"Analyze this CV against this JD. Provide a match score (0-100%), list missing keywords, and suggest 3 specific improvements.\n\nJD: {jd}\n\nCV: {cv}"
                    response = get_ai_response(prompt)
                    st.markdown("### Analysis Results")
                    st.write(response)
            else: st.warning("Please fill both JD and CV fields.")

    # --- صفحة Cover Letter ---
    elif page == "✉️ Cover Letter":
        st.markdown('<div class="tool-header"><h2>Cover Letter Script</h2><p>Generate a tailored cover letter in seconds.</p></div>', unsafe_allow_html=True)
        jd_cl = st.text_area("Paste Job Description", height=200)
        highlights = st.text_input("Key highlights you want to mention (e.g., 5 years experience in Python)")
        
        if st.button("Generate Script", use_container_width=True):
            with st.spinner("Writing..."):
                prompt = f"Write a professional and persuasive cover letter for this job: {jd_cl}. Include these highlights: {highlights}. Keep it concise and impactful."
                st.markdown("### Your Tailored Cover Letter")
                st.write(get_ai_response(prompt))

    # --- صفحة Interview Prep ---
    elif page == "🎙️ Interview Prep":
        st.markdown('<div class="tool-header"><h2>Interview Master</h2><p>Simulate a real interview based on your target role.</p></div>', unsafe_allow_html=True)
        role = st.text_input("Target Role", placeholder="e.g. Senior Data Scientist")
        if st.button("Generate Interview Questions", use_container_width=True):
            with st.spinner("Preparing questions..."):
                prompt = f"Provide 5 challenging interview questions for a {role} position, with a brief tip on how to answer each one perfectly."
                st.markdown(f"### Mock Interview for {role}")
                st.write(get_ai_response(prompt))

    # --- صفحة Salary Insight ---
    elif page == "💰 Salary Insight":
        st.markdown('<div class="tool-header"><h2>Value Estimation</h2><p>Estimate your market value based on role and skills.</p></div>', unsafe_allow_html=True)
        s_role = st.text_input("Job Title")
        s_loc = st.text_input("Location (City/Country)")
        if st.button("Get Salary Insight", use_container_width=True):
            with st.spinner("Fetching market data..."):
                prompt = f"Provide an estimated salary range for a {s_role} in {s_loc} based on current 2026 market trends. Include a breakdown for Junior, Mid, and Senior levels."
                st.markdown(f"### Salary Report: {s_role}")
                st.write(get_ai_response(prompt))
