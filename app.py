import streamlit as st
try:
    from groq import Groq
except ImportError:
    st.error("Missing 'groq' library.")
    st.stop()

st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    [data-testid="stAppViewBlockContainer"] {
        padding-top: 2rem !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a1f29 0%, #050505 100%);
        color: #e6edf3;
    }
    .hero-container { text-align: center; width: 100%; margin-bottom: 40px; }
    .main-title {
        font-size: 5rem !important;
        font-weight: 900;
        background: linear-gradient(90deg, #58a6ff, #3fb950);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        display: inline-block;
    }
    .tagline { color: #8b949e; letter-spacing: 5px; text-transform: uppercase; width: 100%; text-align: center; }
    .feature-grid { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 50px; width: 100%; }
    .service-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 30px 15px; width: 220px; text-align: center; }
    .service-card h3 { color: #58a6ff; margin-bottom: 10px; }
    .service-card p { color: #8b949e; font-size: 0.8rem; }
    div.stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        padding: 12px 0px !important;
        font-size: 1.2rem !important;
        border-radius: 50px !important;
        color: white !important;
        font-weight: bold !important;
        box-shadow: 0 10px 25px rgba(35,134,54,0.3) !important;
        border: none !important;
    }
    .page-title { font-size: 2rem; font-weight: 700; color: #58a6ff; margin-bottom: 8px; }
    .page-sub   { color: #8b949e; font-size: 0.9rem; margin-bottom: 28px; }
    .result-box {
        background: rgba(88,166,255,0.05);
        border: 1px solid rgba(88,166,255,0.15);
        border-radius: 12px;
        padding: 20px 24px;
        margin-top: 20px;
        white-space: pre-wrap;
        font-size: 0.92rem;
        line-height: 1.7;
        color: #e6edf3;
    }
    </style>
    """, unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def call_groq(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=1500,
    )
    return response.choices[0].message.content

if "entered" not in st.session_state:
    st.session_state.entered = False

# ─── LANDING PAGE ───────────────────────────────────────────────
if not st.session_state.entered:
    st.markdown("""
        <div class="hero-container">
            <h1 class="main-title">CareerMind AI</h1>
            <p class="tagline">Architecting Your Professional Future</p>
        </div>
    """, unsafe_allow_html=True)
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

# ─── INNER APP ──────────────────────────────────────────────────
else:
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;'>🧠 CareerMind</h2>", unsafe_allow_html=True)
        page = st.radio("Tools", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight"])
        if st.button("Logout"):
            st.session_state.entered = False
            st.rerun()

    # ── 1. CV MATCHER ────────────────────────────────────────────
    if page == "🔍 CV Matcher":
        st.markdown('<div class="page-title">🔍 CV Matcher</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-sub">Paste your CV and the Job Description — get a full alignment report.</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            cv_text = st.text_area("📄 Your CV", height=280, placeholder="Paste your CV here...")
        with col2:
            jd_text = st.text_area("📋 Job Description", height=280, placeholder="Paste the job description here...")

        if st.button("Analyse Match ⚡"):
            if cv_text.strip() and jd_text.strip():
                with st.spinner("Analysing alignment..."):
                    result = call_groq(
                        "You are an expert career coach and ATS specialist. Analyse the match between the CV and the job description. Provide: 1) Match score out of 100, 2) Key strengths, 3) Missing keywords/skills, 4) Recommendations to improve the CV.",
                        f"CV:\n{cv_text}\n\nJob Description:\n{jd_text}"
                    )
                st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please paste both your CV and the Job Description.")

    # ── 2. COVER LETTER ──────────────────────────────────────────
    elif page == "✉️ Cover Letter":
        st.markdown('<div class="page-title">✉️ Cover Letter Builder</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-sub">Generate a tailored, professional cover letter in seconds.</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            cv_cl = st.text_area("📄 Your CV / Experience", height=220, placeholder="Paste your CV or key experience...")
            name  = st.text_input("Your Name", placeholder="e.g. Ahmed Al-Rashidi")
        with col2:
            jd_cl  = st.text_area("📋 Job Description", height=220, placeholder="Paste the job description...")
            tone   = st.selectbox("Tone", ["Professional", "Confident", "Enthusiastic", "Concise"])

        if st.button("Generate Cover Letter ✉️"):
            if cv_cl.strip() and jd_cl.strip():
                with st.spinner("Writing your cover letter..."):
                    result = call_groq(
                        f"You are an expert cover letter writer. Write a compelling, tailored cover letter in a {tone} tone. Do not add placeholders — use the actual info provided. Sign off with the candidate's name.",
                        f"Candidate Name: {name}\n\nCV/Experience:\n{cv_cl}\n\nJob Description:\n{jd_cl}"
                    )
                st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please fill in your CV and the Job Description.")

    # ── 3. INTERVIEW PREP ────────────────────────────────────────
    elif page == "🎙️ Interview Prep":
        st.markdown('<div class="page-title">🎙️ Interview Simulator</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-sub">Practice real interview questions and get expert feedback on your answers.</div>', unsafe_allow_html=True)

        jd_iv   = st.text_area("📋 Job Description", height=160, placeholder="Paste the job description...")
        q_type  = st.selectbox("Question Type", ["Behavioural", "Technical", "Situational", "Mixed"])

        if "iv_question" not in st.session_state:
            st.session_state.iv_question = ""

        if st.button("Generate Interview Question 🎯"):
            if jd_iv.strip():
                with st.spinner("Generating question..."):
                    st.session_state.iv_question = call_groq(
                        f"You are a senior hiring manager. Generate one realistic {q_type} interview question based on this job description. Just the question, nothing else.",
                        f"Job Description:\n{jd_iv}"
                    )
            else:
                st.warning("Please paste the Job Description first.")

        if st.session_state.iv_question:
            st.markdown(f'<div class="result-box"><b>❓ Question:</b><br>{st.session_state.iv_question}</div>', unsafe_allow_html=True)
            user_answer = st.text_area("✍️ Your Answer", height=180, placeholder="Type your answer here...")

            if st.button("Get Feedback 💬"):
                if user_answer.strip():
                    with st.spinner("Evaluating your answer..."):
                        feedback = call_groq(
                            "You are an expert interview coach. Evaluate the candidate's answer to the interview question. Give: 1) Score out of 10, 2) What was strong, 3) What was weak, 4) A suggested improved answer.",
                            f"Question:\n{st.session_state.iv_question}\n\nCandidate's Answer:\n{user_answer}"
                        )
                    st.markdown(f'<div class="result-box">{feedback}</div>', unsafe_allow_html=True)
                else:
                    st.warning("Please type your answer first.")

    # ── 4. SALARY INSIGHT ────────────────────────────────────────
    elif page == "💰 Salary Insight":
        st.markdown('<div class="page-title">💰 Salary Intelligence</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-sub">Get a data-driven salary estimate and negotiation strategy.</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            job_title   = st.text_input("Job Title", placeholder="e.g. Senior Data Scientist")
            location    = st.text_input("Location / Market", placeholder="e.g. Dubai, UAE")
            experience  = st.slider("Years of Experience", 0, 25, 3)
        with col2:
            industry    = st.text_input("Industry", placeholder="e.g. FinTech, Healthcare")
            skills      = st.text_area("Key Skills", height=120, placeholder="e.g. Python, ML, SQL, AWS...")

        if st.button("Estimate Salary 💰"):
            if job_title.strip() and location.strip():
                with st.spinner("Calculating market value..."):
                    result = call_groq(
                        "You are a compensation specialist with deep knowledge of global salary benchmarks. Provide: 1) Salary range (low / mid / high) in local currency, 2) Factors affecting the range, 3) Negotiation tips, 4) Benefits to negotiate beyond salary.",
                        f"Job Title: {job_title}\nLocation: {location}\nIndustry: {industry}\nYears of Experience: {experience}\nKey Skills: {skills}"
                    )
                st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please enter at least a Job Title and Location.")
