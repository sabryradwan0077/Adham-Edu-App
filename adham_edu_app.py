def init_state():
    if "questions" not in st.session_state:
        st.session_state.questions = get_questions()
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "answer_submitted" not in st.session_state:
        st.session_state.answer_submitted = False
    if "deadline" not in st.session_state:
        st.session_state.deadline = None
    if "question_started_at" not in st.session_state:
        st.session_state.question_started_at = None
    if "auto_skipped" not in st.session_state:
        st.session_state.auto_skipped = []
    if "exam_finished" not in st.session_state:
        st.session_state.exam_finished = False
    if "current_track" not in st.session_state:
        st.session_state.current_track = "الواجهة الرئيسية"
    # جديد
    if "exam_mode" not in st.session_state:
        st.session_state.exam_mode = "تدريبي"  # أو "نهائي"
    if "exam_subject" not in st.session_state:
        st.session_state.exam_subject = "الكل"
