import streamlit as st
import PyPDF2
import io

try:
    from groq import Groq
except ImportError:
    st.error("Missing 'groq' library. Please install it using: pip install groq")
    st.stop()

# --- 1. إعدادات الصفحة والتنسيق (CSS) ---
st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* الحاوية الرئيسية */
    [data-testid="stAppViewBlockContainer"] {
        padding-top: 2rem !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
    }
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a1f29 0%, #050505 100%);
        color: #e6edf3;
    }

    /* إصلاح الأزرار لتكون بعرض كامل وتنسيق فخم (مثل image_a468ba.jpg) */
    div.stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        color: white !important;
        padding: 12px 20px !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        width: 100% !important; /* هذا يجعل الزر يمتد بعرض الحقل */
        border: none !important;
        box-shadow: 0 4px 15px rgba(35,134,54,0.3) !important;
        transition: all 0.2s ease;
        margin-top: 10px;
    }

    /* تخصيص زر الـ Reset حصرياً بنفس الحجم ولكن بلون محايد */
    div.stButton > button[key*="reset"] {
        background: rgba(255,255,255,0.05) !important;
        color: #8b949e !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        box-shadow: none !important;
    }
    div.stButton > button[key*="reset"]:hover {
        border-color: rgba(255,100,100,0.4) !important;
        color: #ff6b6b !important;
    }

    /* حذف ومنع ظهور أي أزرار حمراء افتراضية (الزر الغبي) */
    button[style*="background-color: rgb(255, 75, 75)"], 
    button[style*="background-color: #ff4b4b"] {
        display: none !important;
    }

    /* العناوين والصناديق */
    .main-title {
        font-size: 5rem !important; font-weight: 900;
        background: linear-gradient(90deg, #58a6ff, #3fb950);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center;
    }
    .tagline { color: #8b949e; letter-spacing: 5px; text-transform: uppercase; text-align: center; margin-bottom: 40px;}
    .result-box { background: rgba(88,166,255,0.05); border: 1px solid rgba(88,166,255,0.15); border-radius: 12px; padding: 25px; margin-top: 20px; color: #e6edf3; line-height: 1.6; }
    .col-label { font-size: 0.75rem; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: #58a6ff; margin-bottom: 8px; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background: #0d1117 !important; border-right: 1px solid rgba(255,255,255,0.06) !important; }
    .sidebar-logo { font-size: 1.8rem; font-weight: 900; color: #e6edf3; padding: 20px 10px; }
    .sidebar-logo span { color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المنطق البرمجي (Helper Functions) ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def call_groq(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        temperature=0.7, max_tokens=2000,
    )
    return response.choices[0].message.content

def extract_pdf_text(uploaded_file):
    reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
    text = "".join([page.extract_text() or "" for page in reader.pages])
    return text.strip()

def render_dual_buttons(label, action_key, session_keys):
    """ترسم أزرار متناسقة بعرض كامل تحت الخانات"""
    col_main, col_reset = st.columns([2.5, 1])
    with col_main:
        main_btn = st.button(label, key=f"btn_{action_key}")
    with col_reset:
        if st.button("↺ Reset", key=f"reset_{action_key}"):
            for k in session_keys:
                st.session_state.pop(k, None)
            st.rerun()
    return main_btn

# --- 3. إدارة الجلسة (Session State) ---
if "entered" not in st.session_state:
    st.session_state.entered = False

# --- 4. واجهة المستخدم (UI) ---

# الصفحة الافتتاحية
if not st.session_state.entered:
    st.markdown('<div style="padding-top:100px;"><h1 class="main-title">CareerMind AI</h1><p class="tagline">Architecting Your Professional Future</p></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([2, 1, 2])
    with col:
        if st.button("Access Professional Suite", key="access_app"):
            st.session_state.entered = True
            st.rerun()

# التطبيق الداخلي
else:
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🧠 Career<span>Mind</span></div>', unsafe_allow_html=True)
        page = st.radio("Navigation", ["🔍 CV Matcher", "✉️ Cover Letter", "🎙️ Interview Prep", "💰 Salary Insight", "🎓 Skills Finder"])
        st.write("---")
        if st.button("🚪 Logout", key="logout"):
            st.session_state.entered = False
            st.rerun()

    # --- 1. CV Matcher ---
    if page == "🔍 CV Matcher":
        st.markdown(f"<h1>{page}</h1>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="col-label">📋 Job Description</div>', unsafe_allow_html=True)
            jd_input = st.text_area("JD", placeholder="Paste Job Description here...", height=300, label_visibility="collapsed", key="jd_cv")
        with c2:
            st.markdown('<div class="col-label">📄 Your CV</div>', unsafe_allow_html=True)
            uploaded_cv = st.file_uploader("Upload PDF CV", type="pdf", label_visibility="collapsed", key="pdf_cv")
            cv_text = extract_pdf_text(uploaded_cv) if uploaded_cv else st.text_area("CV", placeholder="Or paste CV text...", height=210, label_visibility="collapsed", key="txt_cv")

        if render_dual_buttons("Analyse Match ⚡", "cv_match", ["jd_cv", "txt_cv", "cv_res"]):
            if (jd_input and (uploaded_cv or cv_text)):
                with st.spinner("Calculating ATS Score..."):
                    st.session_state.cv_res = call_groq("You are an ATS Expert.", f"Match CV: {cv_text or uploaded_cv} with JD: {jd_input}")
            else: st.warning("Please provide both CV and JD.")
        
        if "cv_res" in st.session_state:
            st.markdown(f'<div class="result-box">{st.session_state.cv_res}</div>', unsafe_allow_html=True)

    # --- 2. Cover Letter ---
    elif page == "✉️ Cover Letter":
        st.markdown(f"<h1>{page}</h1>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="col-label">📋 Job Details</div>', unsafe_allow_html=True)
            jd_cl = st.text_area("JD", height=250, label_visibility="collapsed", key="jd_cl")
        with c2:
            st.markdown('<div class="col-label">📄 Your Experience</div>', unsafe_allow_html=True)
            cv_cl = st.text_area("CV", height=250, label_visibility="collapsed", key="cv_cl")

        if render_dual_buttons("Generate Letter ✉️", "cl_gen", ["jd_cl", "cv_cl", "cl_res"]):
            with st.spinner("Writing..."):
                st.session_state.cl_res = call_groq("Expert Writer", f"Write cover letter for JD: {jd_cl} and CV: {cv_cl}")
        
        if "cl_res" in st.session_state:
            st.markdown(f'<div class="result-box">{st.session_state.cl_res}</div>', unsafe_allow_html=True)

    # --- 3. Interview Prep ---
    elif page == "🎙️ Interview Prep":
        st.markdown(f"<h1>{page}</h1>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="col-label">📋 Job Description</div>', unsafe_allow_html=True)
            jd_iv = st.text_area("JD", height=200, label_visibility="collapsed", key="jd_iv")
        with c2:
            st.markdown('<div class="col-label">📄 CV Context</div>', unsafe_allow_html=True)
            cv_iv = st.text_area("CV", height=200, label_visibility="collapsed", key="cv_iv")

        if render_dual_buttons("Generate Questions 🎙️", "iv_gen", ["jd_iv", "cv_iv", "iv_res"]):
            with st.spinner("Preparing questions..."):
                st.session_state.iv_res = call_groq("Interviewer", f"Questions for JD: {jd_iv} and CV: {cv_iv}")
        
        if "iv_res" in st.session_state:
            st.markdown(f'<div class="result-box">{st.session_state.iv_res}</div>', unsafe_allow_html=True)

    # --- 4. Salary Insight ---
    elif page == "💰 Salary Insight":
        st.markdown(f"<h1>{page}</h1>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="col-label">💼 Role & Location</div>', unsafe_allow_html=True)
            role = st.text_input("Role", key="sal_role")
            loc = st.text_input("Location", key="sal_loc")
        with c2:
            st.markdown('<div class="col-label">⚙️ Seniority</div>', unsafe_allow_html=True)
            exp = st.selectbox("Years", ["0-2", "3-5", "5-10", "10+"], key="sal_exp")

        if render_dual_buttons("Get Salary Insight 💰", "sal_gen", ["sal_role", "sal_loc", "sal_exp", "sal_res"]):
            with st.spinner("Fetching market data..."):
                st.session_state.sal_res = call_groq("Salary Expert", f"Salary for {role} in {loc} with {exp} years exp.")
        
        if "sal_res" in st.session_state:
            st.markdown(f'<div class="result-box">{st.session_state.sal_res}</div>', unsafe_allow_html=True)

    # --- 5. Skills Finder (الصفحة التي طلبت تعديلها) ---
    elif page == "🎓 Skills Finder":
        st.markdown(f"<h1>{page}</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#8b949e;'>Enter a job title and get the essential skills, tools, and recommended courses.</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="col-label">💼 Job Title</div>', unsafe_allow_html=True)
            sk_title = st.text_input("Job Title", placeholder="e.g. Data Scientist...", label_visibility="collapsed", key="sk_t_in")
            st.markdown('<div class="col-label">Level</div>', unsafe_allow_html=True)
            sk_level = st.selectbox("Level", ["Beginner", "Junior", "Mid-level", "Senior"], label_visibility="collapsed", key="sk_l_in")
        
        with col2:
            st.markdown('<div class="col-label">🌍 Industry (Optional)</div>', unsafe_allow_html=True)
            sk_ind = st.text_input("Industry", placeholder="e.g. Tech, Finance...", label_visibility="collapsed", key="sk_i_in")
            st.markdown('<div class="col-label">Any specific focus?</div>', unsafe_allow_html=True)
            sk_focus = st.text_area("Focus", placeholder="e.g. Cloud, Mobile...", height=68, label_visibility="collapsed", key="sk_f_in")

        # استخدام الدالة المصلحة للأزرار (كاملة العرض ولا يوجد أحمر)
        if render_dual_buttons("Find Skills & Courses 🎓", "sk_finder", ["sk_t_in", "sk_l_in", "sk_i_in", "sk_f_in", "sk_res"]):
            if sk_title:
                with st.spinner("Curating your learning path..."):
                    st.session_state.sk_res = call_groq(
                        "You are a Career Advisor.", 
                        f"Job Title: {sk_title}, Level: {sk_level}, Industry: {sk_ind}, Focus: {sk_focus}. Provide skills and top 5 courses."
                    )
            else:
                st.warning("Please enter a Job Title.")

        if "sk_res" in st.session_state:
            st.markdown(f'<div class="result-box">{st.session_state.sk_res}</div>', unsafe_allow_html=True)
