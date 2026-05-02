import streamlit as st
import PyPDF2
import io
import hashlib
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

try:
    from groq import Groq
except ImportError:
    st.error("Missing 'groq' library.")
    st.stop()

st.set_page_config(page_title="CareerMind AI", layout="wide", initial_sidebar_state="collapsed")

# ── GOOGLE SHEETS SETUP ──────────────────────────────────────────
SHEET_ID = "1Dt4GOPOThY3c1jDJZ1QCCmD96HiM3IdmmQhQazBl5Ds"

@st.cache_resource
def get_sheet():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    )
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).sheet1

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password):
    sheet = get_sheet()
    records = sheet.get_all_records()
    for r in records:
        if r["email"] == email:
            return False, "البريد الإلكتروني مسجل مسبقاً"
        if r["username"] == username:
            return False, "اسم المستخدم محجوز، جرب اسماً آخر"
    sheet.append_row([username, hash_password(password), email, datetime.now().strftime("%Y-%m-%d %H:%M")])
    return True, "تم التسجيل بنجاح!"

def login_user(email, password):
    sheet = get_sheet()
    records = sheet.get_all_records()
    for r in records:
        if r["email"] == email and r["password"] == hash_password(password):
            return True, r["username"]
    return False, "البريد أو كلمة المرور غلط"

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
    font-size: 5rem !important; font-weight: 900;
    background: linear-gradient(90deg, #58a6ff, #3fb950);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0px; display: inline-block;
}
.tagline { color: #8b949e; letter-spacing: 5px; text-transform: uppercase; width: 100%; text-align: center; }
.feature-grid { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 50px; width: 100%; }
.service-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 30px 15px; width: 200px; text-align: center; }
.service-card h3 { color: #58a6ff; margin-bottom: 10px; }
.service-card p { color: #8b949e; font-size: 0.8rem; }

/* AUTH PAGE */
.auth-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 40px 36px;
    width: 100%;
    max-width: 420px;
    margin: 0 auto;
}
.auth-title { font-size: 1.5rem; font-weight: 700; color: #e6edf3; margin-bottom: 6px; text-align: center; }
.auth-sub { font-size: 0.82rem; color: #8b949e; text-align: center; margin-bottom: 28px; }

/* SIDEBAR */
[data-testid="stSidebar"] { background: #0d1117 !important; border-right: 1px solid rgba(255,255,255,0.06) !important; }
.sidebar-logo { font-size: 1.9rem; font-weight: 900; color: #e6edf3; padding: 24px 0 4px 4px; }
.sidebar-logo span { color: #58a6ff; }
.sidebar-tagline { font-size: 0.7rem; letter-spacing: 3px; text-transform: uppercase; color: #3fb950; padding-left: 4px; margin-bottom: 20px; }
.sidebar-divider { height: 1px; background: rgba(255,255,255,0.07); margin: 14px 0; }
.sidebar-section-title { font-size: 0.65rem; letter-spacing: 2.5px; text-transform: uppercase; color: #484f58; padding-left: 4px; margin-bottom: 8px; }
.sidebar-stat-row { display: flex; justify-content: space-between; gap: 8px; margin-bottom: 14px; }
.sidebar-stat { flex: 1; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 10px; padding: 10px 6px; text-align: center; }
.sidebar-stat-num { font-size: 1.2rem; font-weight: 700; color: #58a6ff; }
.sidebar-stat-lbl { font-size: 0.6rem; letter-spacing: 1px; text-transform: uppercase; color: #484f58; margin-top: 2px; }
.sidebar-tip { background: rgba(63,185,80,0.06); border: 1px solid rgba(63,185,80,0.15); border-radius: 10px; padding: 12px 14px; font-size: 0.78rem; color: #8b949e; line-height: 1.5; margin-bottom: 14px; }
.sidebar-tip b { color: #3fb950; }
.sidebar-steps { display: flex; flex-direction: column; gap: 8px; margin-bottom: 14px; }
.sidebar-step { display: flex; align-items: center; gap: 10px; font-size: 0.78rem; color: #8b949e; }
.sidebar-step-num { width: 22px; height: 22px; border-radius: 50%; background: rgba(88,166,255,0.1); border: 1px solid rgba(88,166,255,0.2); color: #58a6ff; font-size: 0.65rem; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.user-card { display: flex; align-items: center; gap: 12px; padding: 12px 4px; margin-bottom: 4px; }
.user-avatar { width: 38px; height: 38px; border-radius: 50%; background: linear-gradient(135deg, #238636, #58a6ff); display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 700; color: white; flex-shrink: 0; }
.user-name { font-size: 0.88rem; font-weight: 600; color: #e6edf3; }
.user-tag  { font-size: 0.68rem; color: #3fb950; letter-spacing: 1px; margin-top: 2px; }

/* LOGOUT */
[data-testid="stSidebar"] div.stButton > button {
    background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important; color: #8b949e !important; font-size: 0.88rem !important;
    font-weight: 500 !important; padding: 10px 0 !important; width: 100% !important; box-shadow: none !important;
}
[data-testid="stSidebar"] div.stButton > button:hover {
    border-color: rgba(255,100,100,0.35) !important; color: #ff6b6b !important; background: rgba(255,100,100,0.05) !important;
}

/* MAIN BUTTONS */
[data-testid="stAppViewBlockContainer"] div.stButton > button {
    padding: 14px 0 !important; font-size: 1rem !important; font-weight: 600 !important;
    border-radius: 50px !important; width: 100% !important; transition: all 0.2s !important; min-height: 52px !important;
}
.green-btn div.stButton > button {
    background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
    color: white !important; border: none !important; box-shadow: 0 8px 24px rgba(35,134,54,0.35) !important;
}
.green-btn div.stButton > button:hover { box-shadow: 0 12px 32px rgba(35,134,54,0.5) !important; transform: translateY(-1px) !important; }
.reset-col div.stButton > button { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.12) !important; color: #8b949e !important; box-shadow: none !important; }
.reset-col div.stButton > button:hover { border-color: rgba(255,100,100,0.4) !important; color: #ff6b6b !important; background: rgba(255,100,100,0.05) !important; transform: none !important; box-shadow: none !important; }

.page-title { font-size: 2rem; font-weight: 700; color: #58a6ff; margin-bottom: 6px; }
.page-sub   { color: #8b949e; font-size: 0.9rem; margin-bottom: 24px; }
.result-box { background: rgba(88,166,255,0.05); border: 1px solid rgba(88,166,255,0.15); border-radius: 12px; padding: 20px 24px; margin-top: 20px; white-space: pre-wrap; font-size: 0.92rem; line-height: 1.7; color: #e6edf3; }
.col-label { font-size: 0.75rem; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: #58a6ff; margin-bottom: 6px; }
.pdf-badge { display: inline-flex; align-items: center; gap: 8px; background: rgba(63,185,80,0.1); border: 1px solid rgba(63,185,80,0.25); border-radius: 8px; padding: 8px 14px; font-size: 0.82rem; color: #3fb950; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def call_groq(system_prompt, user_prompt):
    user_prompt = user_prompt[:4000]
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        temperature=0.7, max_tokens=2048,
    )
    return response.choices[0].message.content

def extract_pdf_text(uploaded_file):
    reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()

def btn_row(action_label, action_key, reset_keys):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="green-btn">', unsafe_allow_html=True)
        clicked = st.button(action_label, key=f"act_{action_key}", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="reset-col">', unsafe_allow_html=True)
        reset = st.button("↺ Reset", key=f"rst_{action_key}", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    if reset:
        for k in reset_keys:
            st.session_state.pop(k, None)
        st.rerun()
    return clicked

# ── SESSION STATE ────────────────────────────────────────────────
if "entered"   not in st.session_state: st.session_state.entered   = False
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username"  not in st.session_state: st.session_state.username  = ""
if "auth_page" not in st.session_state: st.session_state.auth_page = "login"

# ── LANDING ──────────────────────────────────────────────────────
if not st.session_state.entered:
    st.markdown("""
        <div class="hero-container">
            <h1 class="main-title">CareerMind AI</h1>
            <p class="tagline">Architecting Your Professional Future</p>
        </div>
        <div class="feature-grid">
            <div class="service-card"><h3>🔍 Audit</h3><p>CV & JD Alignment</p></div>
            <div class="service-card"><h3>✉️ Script</h3><p>Cover Letter Builder</p></div>
            <div class="service-card"><h3>🎙️ Master</h3><p>Interview Simulator</p></div>
            <div class="service-card"><h3>💰 Value</h3><p>Salary Estimation</p></div>
            <div class="service-card"><h3>🎓 Skills</h3><p>Skills & Course Finder</p></div>
        </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1.2, 1, 1, 1.2]) if False else st.columns([1, 1.2, 1.2, 1])
    with c2:
        st.markdown('<div class="green-btn">', unsafe_allow_html=True)
        if st.button("🚀 Get Started", use_container_width=True):
            st.session_state.entered = True
            st.session_state.auth_page = "login"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="green-btn">', unsafe_allow_html=True)
        if st.button("📝 Create Account", use_container_width=True):
            st.session_state.entered = True
            st.session_state.auth_page = "register"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ── AUTH PAGE ────────────────────────────────────────────────────
elif not st.session_state.logged_in:
    st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)

    if st.session_state.auth_page == "login":
        st.markdown('<div class="auth-box">', unsafe_allow_html=True)
        st.markdown('<div class="auth-title">👋 مرحباً بعودتك</div>', unsafe_allow_html=True)
        st.markdown('<div class="auth-sub">سجّل دخولك للوصول لأدواتك</div>', unsafe_allow_html=True)
        email    = st.text_input("البريد الإلكتروني", placeholder="you@example.com", key="li_email")
        password = st.text_input("كلمة المرور", type="password", key="li_pass")
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        st.markdown('<div class="green-btn">', unsafe_allow_html=True)
        if st.button("تسجيل الدخول", use_container_width=True, key="do_login"):
            if email and password:
                with st.spinner("جارٍ التحقق..."):
                    ok, result = login_user(email, password)
                if ok:
                    st.session_state.logged_in = True
                    st.session_state.username  = result
                    st.rerun()
                else:
                    st.error(result)
            else:
                st.warning("يرجى تعبئة جميع الحقول")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;font-size:0.82rem;color:#8b949e;">ما عندك حساب؟</div>', unsafe_allow_html=True)
        if st.button("أنشئ حساباً جديداً →", key="go_register", use_container_width=True):
            st.session_state.auth_page = "register"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="auth-box">', unsafe_allow_html=True)
        st.markdown('<div class="auth-title">✨ حساب جديد</div>', unsafe_allow_html=True)
        st.markdown('<div class="auth-sub">انضم لـ CareerMind AI مجاناً</div>', unsafe_allow_html=True)
        username = st.text_input("الاسم", placeholder="Ahmed Al-Rashidi", key="rg_name")
        email    = st.text_input("البريد الإلكتروني", placeholder="you@example.com", key="rg_email")
        password = st.text_input("كلمة المرور", type="password", key="rg_pass")
        password2= st.text_input("تأكيد كلمة المرور", type="password", key="rg_pass2")
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        st.markdown('<div class="green-btn">', unsafe_allow_html=True)
        if st.button("إنشاء الحساب", use_container_width=True, key="do_register"):
            if username and email and password and password2:
                if password != password2:
                    st.error("كلمتا المرور غير متطابقتين")
                elif len(password) < 6:
                    st.error("كلمة المرور يجب أن تكون 6 أحرف على الأقل")
                else:
                    with st.spinner("جارٍ إنشاء الحساب..."):
                        ok, msg = register_user(username, email, password)
                    if ok:
                        st.success(msg)
                        st.session_state.logged_in = True
                        st.session_state.username  = username
                        st.rerun()
                    else:
                        st.error(msg)
            else:
                st.warning("يرجى تعبئة جميع الحقول")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;font-size:0.82rem;color:#8b949e;">عندك حساب؟</div>', unsafe_allow_html=True)
        if st.button("سجّل دخولك →", key="go_login", use_container_width=True):
            st.session_state.auth_page = "login"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ── INNER APP ────────────────────────────────────────────────────
else:
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-logo">🧠 Career<span>Mind</span></div>
            <div class="sidebar-tagline">AI Career Suite</div>
            <div class="sidebar-divider"></div>
        """, unsafe_allow_html=True)

        # User card
        initials = "".join([w[0].upper() for w in st.session_state.username.split()[:2]])
        st.markdown(f"""
            <div class="user-card">
                <div class="user-avatar">{initials}</div>
                <div>
                    <div class="user-name">{st.session_state.username}</div>
                    <div class="user-tag">✦ Free Plan</div>
                </div>
            </div>
            <div class="sidebar-divider"></div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section-title">Navigation</div>', unsafe_allow_html=True)
        default_page = st.session_state.get("page", "🔍 CV Matcher")
        page_options = ["🔍 CV Matcher","✉️ Cover Letter","🎙️ Interview Prep","💰 Salary Insight","🎓 Skills Finder"]
        default_idx  = page_options.index(default_page) if default_page in page_options else 0
        page = st.radio("", page_options, index=default_idx, label_visibility="collapsed")
        st.session_state.page = page

        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-section-title">Platform Stats</div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="sidebar-stat-row">
                <div class="sidebar-stat"><div class="sidebar-stat-num">5</div><div class="sidebar-stat-lbl">Tools</div></div>
                <div class="sidebar-stat"><div class="sidebar-stat-num">AI</div><div class="sidebar-stat-lbl">Powered</div></div>
                <div class="sidebar-stat"><div class="sidebar-stat-num">∞</div><div class="sidebar-stat-lbl">Sessions</div></div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

        tips = {
            "🔍 CV Matcher":     ("<b>Tip:</b> Upload your PDF CV for the most accurate ATS match score.", ["Upload or paste your CV","Paste the job description","Click Analyse Match"]),
            "✉️ Cover Letter":   ("<b>Tip:</b> Match the tone to the company culture for best results.", ["Paste the job description","Upload or paste your CV","Generate your letter"]),
            "🎙️ Interview Prep": ("<b>Tip:</b> Upload your CV so questions match your actual experience.", ["Upload your CV","Paste the job description","Generate & answer questions"]),
            "💰 Salary Insight": ("<b>Tip:</b> Be specific with location and industry for accurate benchmarks.", ["Enter job title & location","Add your skills","Get salary estimate"]),
            "🎓 Skills Finder":  ("<b>Tip:</b> Be specific with the job title to get the most relevant skills.", ["Enter the job title","Click Find Skills","Review skills & courses"]),
        }
        tip_text, steps = tips.get(page, ("",""))
        st.markdown(f'<div class="sidebar-tip">{tip_text}</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-section-title">How to use</div>', unsafe_allow_html=True)
        steps_html = "".join([f'<div class="sidebar-step"><div class="sidebar-step-num">{i+1}</div>{s}</div>' for i,s in enumerate(steps)])
        st.markdown(f'<div class="sidebar-steps">{steps_html}</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username  = ""
            st.session_state.entered   = False
            st.rerun()

    # ── 1. CV MATCHER ────────────────────────────────────────────
    if page == "🔍 CV Matcher":
        st.markdown('<div class="page-title">🔍 CV Matcher</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-sub">Paste your Job Description on the left and upload/paste your CV on the right.</div>', unsafe_allow_html=True)
        col_jd, col_cv = st.columns(2)
        with col_jd:
            st.markdown('<div class="col-label">📋 Job Description</div>', unsafe_allow_html=True)
            jd_text = st.text_area("", height=300, placeholder="Paste the job description here...", key="jd_cv", label_visibility="collapsed")
        with col_cv:
            st.markdown('<div class="col-label">📄 Your CV</div>', unsafe_allow_html=True)
            pdf_file = st.file_uploader("Upload CV as PDF", type=["pdf"], key="cv_pdf", label_visibility="collapsed")
            cv_text = ""
            if pdf_file:
                cv_text = extract_pdf_text(pdf_file)
                st.markdown(f'<div class="pdf-badge">✅ {pdf_file.name} — {len(cv_text)} chars extracted</div>', unsafe_allow_html=True)
            else:
                cv_text = st.text_area("Or paste CV text", height=220, placeholder="Paste your CV here...", key="cv_paste")
        if btn_row("Analyse Match ⚡", "cv", ["jd_cv","cv_paste","cv_result"]):
            if cv_text.strip() and jd_text.strip():
                with st.spinner("Analysing alignment..."):
                    st.session_state.cv_result = call_groq(
                        "You are an expert career coach and ATS specialist. Provide: 1) Match score out of 100, 2) Key strengths, 3) Missing keywords/skills, 4) Recommendations.",
                        f"CV:\n{cv_text}\n\nJob Description:\n{jd_text}")
            else:
                st.warning("Please provide both your CV and the Job Description.")
        if "cv_result" in st.session_state:
            st.markdown(f'<div class="result-box">{st.session_state.cv_result}</div>', unsafe_allow_html=True)

    # ── 2. COVER LETTER ──────────────────────────────────────────
    elif page == "✉️ Cover Letter":
        st.markdown('<div class="page-title">✉️ Cover Letter Builder</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-sub">Generate a tailored, professional cover letter in seconds.</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="col-label">📋 Job Description</div>', unsafe_allow_html=True)
            jd_cl = st.text_area("", height=240, placeholder="Paste the job description...", key="jd_cl", label_visibility="collapsed")
            tone  = st.selectbox("Tone", ["Professional","Confident","Enthusiastic","Concise"])
        with col2:
            st.markdown('<div class="col-label">📄 Your CV / Experience</div>', unsafe_allow_html=True)
            pdf_cl = st.file_uploader("Upload CV as PDF", type=["pdf"], key="cv_cl_pdf", label_visibility="collapsed")
            cv_cl = ""
            if pdf_cl:
                cv_cl = extract_pdf_text(pdf_cl)
                st.markdown(f'<div class="pdf-badge">✅ {pdf_cl.name} — {len(cv_cl)} chars extracted</div>', unsafe_allow_html=True)
            else:
                cv_cl = st.text_area("Or paste CV text", height=180, placeholder="Paste your CV or key experience...", key="cv_cl_paste")
            name = st.text_input("Your Name", value=st.session_state.username, key="cl_name")
        if btn_row("Generate Cover Letter ✉️", "cl", ["jd_cl","cv_cl_paste","cl_result"]):
            if cv_cl.strip() and jd_cl.strip():
                with st.spinner("Writing your cover letter..."):
                    st.session_state.cl_result = call_groq(
                        f"You are an expert cover letter writer. Write a compelling tailored cover letter in a {tone} tone. Sign off with the candidate's name.",
                        f"Candidate Name: {name}\n\nCV/Experience:\n{cv_cl}\n\nJob Description:\n{jd_cl}")
            else:
                st.warning("Please fill in your CV and the Job Description.")
        if "cl_result" in st.session_state:
            st.markdown(f'<div class="result-box">{st.session_state.cl_result}</div>', unsafe_allow_html=True)

    # ── 3. INTERVIEW PREP ────────────────────────────────────────
    elif page == "🎙️ Interview Prep":
        st.markdown('<div class="page-title">🎙️ Interview Simulator</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-sub">Upload your CV and paste the Job Description — get questions tailored to your profile.</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="col-label">📋 Job Description</div>', unsafe_allow_html=True)
            jd_iv = st.text_area("", height=280, placeholder="Paste the job description...", key="jd_iv", label_visibility="collapsed")
        with col2:
            st.markdown('<div class="col-label">📄 Your CV</div>', unsafe_allow_html=True)
            pdf_iv = st.file_uploader("Upload CV as PDF", type=["pdf"], key="cv_iv_pdf", label_visibility="collapsed")
            cv_iv = ""
            if pdf_iv:
                cv_iv = extract_pdf_text(pdf_iv)
                st.markdown(f'<div class="pdf-badge">✅ {pdf_iv.name} — {len(cv_iv)} chars extracted</div>', unsafe_allow_html=True)
            else:
                cv_iv = st.text_area("Or paste CV text", height=200, placeholder="Paste your CV here...", key="cv_iv_paste")
        if "iv_question" not in st.session_state: st.session_state.iv_question = ""
        if btn_row("Generate Question 🎯", "iv", ["jd_iv","cv_iv_paste","iv_question","iv_feedback"]):
            if jd_iv.strip():
                with st.spinner("Generating question..."):
                    cv_context = f"\n\nCandidate CV:\n{cv_iv}" if cv_iv.strip() else ""
                    st.session_state.iv_question = call_groq(
                        "You are a senior hiring manager. Generate one realistic interview question tailored to the job description and candidate CV. Just the question.",
                        f"Job Description:\n{jd_iv}{cv_context}")
            else:
                st.warning("Please paste the Job Description first.")
        if st.session_state.iv_question:
            st.markdown(f'<div class="result-box"><b>❓ Question:</b><br>{st.session_state.iv_question}</div>', unsafe_allow_html=True)
            st.markdown('<div class="col-label" style="margin-top:16px">✍️ Your Answer</div>', unsafe_allow_html=True)
            st.text_area("", height=180, placeholder="Type your answer here...", key="iv_answer", label_visibility="collapsed")
            if btn_row("Get Feedback 💬", "fb", ["iv_question","iv_answer","iv_feedback"]):
                ans = st.session_state.get("iv_answer","")
                if ans.strip():
                    with st.spinner("Evaluating your answer..."):
                        st.session_state.iv_feedback = call_groq(
                            "You are an expert interview coach. Give: 1) Score out of 10, 2) What was strong, 3) What was weak, 4) A suggested improved answer.",
                            f"Question:\n{st.session_state.iv_question}\n\nAnswer:\n{ans}")
                else:
                    st.warning("Please type your answer first.")
            if "iv_feedback" in st.session_state:
                st.markdown(f'<div class="result-box">{st.session_state.iv_feedback}</div>', unsafe_allow_html=True)

    # ── 4. SALARY INSIGHT ────────────────────────────────────────
    elif page == "💰 Salary Insight":
        st.markdown('<div class="page-title">💰 Salary Intelligence</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-sub">Get a data-driven salary estimate and negotiation strategy.</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="col-label">📌 Role Details</div>', unsafe_allow_html=True)
            job_title  = st.text_input("Job Title", placeholder="e.g. Senior Data Scientist", key="sal_title")
            location   = st.text_input("Location / Market", placeholder="e.g. Dubai, UAE", key="sal_loc")
            experience = st.slider("Years of Experience", 0, 25, 3, key="sal_exp")
        with col2:
            st.markdown('<div class="col-label">🏭 Context</div>', unsafe_allow_html=True)
            industry = st.text_input("Industry", placeholder="e.g. FinTech, Healthcare", key="sal_ind")
            skills   = st.text_area("Key Skills", height=140, placeholder="e.g. Python, ML, SQL, AWS...", key="sal_skills")
        if btn_row("Estimate Salary 💰", "sal", ["sal_title","sal_loc","sal_ind","sal_skills","sal_result"]):
            if job_title.strip() and location.strip():
                with st.spinner("Calculating market value..."):
                    st.session_state.sal_result = call_groq(
                        "You are a compensation specialist. Provide: 1) Salary range (low/mid/high) in local currency, 2) Factors, 3) Negotiation tips, 4) Benefits to negotiate.",
                        f"Job Title: {job_title}\nLocation: {location}\nIndustry: {industry}\nExperience: {experience} years\nSkills: {skills}")
            else:
                st.warning("Please enter at least a Job Title and Location.")
        if "sal_result" in st.session_state:
            st.markdown(f'<div class="result-box">{st.session_state.sal_result}</div>', unsafe_allow_html=True)

    # ── 5. SKILLS FINDER ─────────────────────────────────────────
    elif page == "🎓 Skills Finder":
        st.markdown('<div class="page-title">🎓 Skills & Course Finder</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-sub">Enter a job title and get the essential skills, tools, and recommended courses you need.</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="col-label">💼 Job Title</div>', unsafe_allow_html=True)
            sk_title = st.text_input("", placeholder="e.g. Data Scientist, UX Designer...", key="sk_title", label_visibility="collapsed")
            st.markdown('<div class="col-label" style="margin-top:16px">📊 Your Level</div>', unsafe_allow_html=True)
            sk_level = st.selectbox("", ["Beginner (no experience)","Junior (0–2 years)","Mid-level (2–5 years)","Senior (5+ years)"], key="sk_level", label_visibility="collapsed")
        with col2:
            st.markdown('<div class="col-label">🌍 Industry Focus (Optional)</div>', unsafe_allow_html=True)
            sk_industry = st.text_input("", placeholder="e.g. Finance, Healthcare, Tech...", key="sk_industry", label_visibility="collapsed")
            st.markdown('<div class="col-label" style="margin-top:16px">🎯 Specific Focus (Optional)</div>', unsafe_allow_html=True)
            sk_note = st.text_area("", height=68, placeholder="e.g. I want to focus on cloud skills...", key="sk_note", label_visibility="collapsed")
        if btn_row("Find Skills & Courses 🎓", "sk", ["sk_title","sk_industry","sk_note","sk_result"]):
            if sk_title.strip():
                with st.spinner("Researching skills and courses..."):
                    extra = f"\nIndustry: {sk_industry}" if sk_industry.strip() else ""
                    note  = f"\nFocus: {sk_note}" if sk_note.strip() else ""
                    st.session_state.sk_result = call_groq(
                        "You are a career advisor. List: 1) Core Technical Skills (6), 2) Soft Skills (4), 3) Tools & Technologies, 4) Top 5 Courses with platform, 5) 3-step Learning Roadmap, 6) Estimated time to job-ready.",
                        f"Job Title: {sk_title}\nLevel: {sk_level}{extra}{note}")
            else:
                st.warning("Please enter a job title.")
        if "sk_result" in st.session_state:
            st.markdown(f'<div class="result-box">{st.session_state.sk_result}</div>', unsafe_allow_html=True)
