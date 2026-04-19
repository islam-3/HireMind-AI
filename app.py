# --- 4. SIDEBAR (التصميم الجديد والفخم) ---
with st.sidebar:
    # اللوجو بشكل أكبر وأفخم
    st.markdown('<p style="font-size: 2.2rem; font-weight: 900; color: #f0f6fc; text-align: center; margin-bottom: 0px;">🧠 HireMind</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 0.9rem; color: #8b949e; text-align: center; margin-bottom: 30px;">Strategic AI Auditing</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # بطاقة إحصائيات جذابة
    total_candidates = len(st.session_state.history)
    st.markdown(f"""
        <div style="background: linear-gradient(145deg, #161b22, #30363d); padding: 20px; border-radius: 15px; border: 1px solid #484f58; text-align: center;">
            <p style="color: #8b949e; margin: 0; font-size: 0.8rem; text-transform: uppercase;">Total Candidates</p>
            <p style="color: #ffffff; margin: 0; font-size: 2.5rem; font-weight: bold;">{total_candidates}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # قسم سجل المرشحين (Recent History)
    if st.session_state.history:
        st.markdown('<p style="color: #f0f6fc; font-weight: bold; font-size: 1.1rem;">📝 Analysis History</p>', unsafe_allow_html=True)
        for entry in reversed(st.session_state.history[-5:]): # عرض آخر 5 فقط
            color = "#238636" if entry['Score'] >= 7 else "#d29922" if entry['Score'] >= 5 else "#da3633"
            st.markdown(f"""
                <div style="padding: 10px; border-bottom: 1px solid #30363d;">
                    <span style="color: {color}; font-weight: bold;">{entry['Score']}/10</span> 
                    <span style="color: #c9d1d9; margin-left: 10px;">{entry['Name']}</span>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # زر الحذف بتصميم أهدأ
    if st.button("🗑️ Reset All Sessions"):
        st.session_state.history = []
        st.session_state.current_result = None
        st.rerun()
