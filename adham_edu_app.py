# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import json
import base64
import random
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List, Any

import pandas as pd
import streamlit as st

# =========================================================
# حصن أدهم التعليمي V60 - Imperial World-Class Edition
# =========================================================

APP_TITLE = "حصن أدهم التعليمي 2026"
APP_VERSION = "V60"
APP_ICON = "🏛️"

BASE_DIR = Path(".")
DATA_DIR = BASE_DIR / "hisn_adham_data"
DATA_FILE = DATA_DIR / "student_data.json"
SYLLABUS_DIR = BASE_DIR / "Syllabus"

DATA_DIR.mkdir(parents=True, exist_ok=True)
SYLLABUS_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# التصميم الفاخر
# =========================================================
def inject_global_css() -> None:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }

    .stApp {
        background:
            radial-gradient(circle at top right, rgba(255,215,0,0.08), transparent 20%),
            radial-gradient(circle at top left, rgba(0,102,204,0.12), transparent 25%),
            linear-gradient(180deg, #08111b 0%, #0b1624 50%, #0d1b2a 100%);
        color: #f1f5f9;
    }

    .hero-box {
        background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.92));
        border: 1px solid rgba(255,215,0,0.18);
        border-radius: 28px;
        padding: 28px;
        margin-bottom: 22px;
        box-shadow: 0 20px 55px rgba(0,0,0,0.35);
    }

    .hero-title {
        text-align: center;
        color: #ffd700;
        font-size: 2.1rem;
        font-weight: 900;
        margin-bottom: 10px;
    }

    .hero-sub {
        text-align: center;
        color: #dbeafe;
        font-size: 1rem;
        line-height: 1.9;
    }

    .section-title {
        color: #ffe082;
        font-size: 1.3rem;
        font-weight: 800;
        border-right: 5px solid #ffd700;
        padding-right: 12px;
        margin: 14px 0 12px 0;
    }

    .glass-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.18);
    }

    .metric-card {
        background: linear-gradient(135deg, rgba(255,215,0,0.08), rgba(255,255,255,0.03));
        border: 1px solid rgba(255,215,0,0.16);
        border-radius: 22px;
        padding: 18px;
        min-height: 125px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.18);
    }

    .metric-label {
        color: #cbd5e1;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 10px;
    }

    .metric-value {
        color: #ffffff;
        font-weight: 900;
        font-size: 1.9rem;
        margin-bottom: 6px;
    }

    .metric-note {
        color: #93c5fd;
        font-size: 0.9rem;
        font-weight: 600;
    }

    .subject-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,215,0,0.04));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 18px;
        margin-bottom: 14px;
    }

    .subject-title {
        color: #fff3bf;
        font-weight: 800;
        font-size: 1.12rem;
        margin-bottom: 8px;
    }

    .subject-meta {
        color: #dbeafe;
        line-height: 1.8;
        font-size: 0.95rem;
    }

    .success-box {
        background: rgba(34,197,94,0.12);
        border: 1px solid rgba(34,197,94,0.35);
        color: #dcfce7;
        border-radius: 18px;
        padding: 15px;
        margin-top: 12px;
        font-weight: 700;
    }

    .error-box {
        background: rgba(239,68,68,0.12);
        border: 1px solid rgba(239,68,68,0.35);
        color: #fee2e2;
        border-radius: 18px;
        padding: 15px;
        margin-top: 12px;
        font-weight: 700;
    }

    .info-chip {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        background: rgba(255,215,0,0.10);
        border: 1px solid rgba(255,215,0,0.18);
        color: #ffe082;
        font-size: 0.88rem;
        font-weight: 700;
        margin-left: 6px;
        margin-bottom: 8px;
    }

    .small-note {
        color: #cbd5e1;
        line-height: 1.8;
        font-size: 0.92rem;
    }

    .stButton > button {
        width: 100%;
        min-height: 46px;
        border-radius: 14px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #facc15, #ffd700) !important;
        color: #111827 !important;
        border: 1px solid rgba(255,215,0,0.28) !important;
        box-shadow: 0 8px 20px rgba(250,204,21,0.22);
    }

    .stDownloadButton > button {
        width: 100%;
        min-height: 46px;
        border-radius: 14px !important;
        font-weight: 800 !important;
    }

    iframe {
        border-radius: 18px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        background: white !important;
    }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1220 0%, #111827 100%);
        border-left: 1px solid rgba(255,255,255,0.06);
    }

    .footer-note {
        text-align: center;
        color: #cbd5e1;
        margin-top: 30px;
        font-size: 0.9rem;
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)

inject_global_css()

# =========================================================
# البيانات الأساسية
# =========================================================
SUBJECTS: Dict[str, Dict[str, Any]] = {
    "الفيزياء": {
        "icon": "⚡",
        "description": "قوانين كيرشوف - قانون أوم - القدرة - الشغل والطاقة - الموجات",
        "difficulty": "مرتفع",
        "topics": ["قانون أوم", "قوانين كيرشوف", "القدرة", "الشغل والطاقة", "الموجات"],
        "youtube": "https://www.youtube.com/results?search_query=فيزياء+ثانوية+عامة+2026"
    },
    "الكيمياء": {
        "icon": "🧪",
        "description": "الاتزان الكيميائي - العضوية - خامات الحديد - الأحماض والقواعد",
        "difficulty": "متوسط",
        "topics": ["خام الحديد", "الاتزان", "الأحماض والقواعد", "العضوية"],
        "youtube": "https://www.youtube.com/results?search_query=كيمياء+ثانوية+عامة+2026"
    },
    "الرياضيات البحتة": {
        "icon": "📐",
        "description": "التفاضل - التكامل - الجبر - الهندسة التحليلية",
        "difficulty": "مرتفع",
        "topics": ["التكامل", "النهايات", "الجبر", "الهندسة التحليلية"],
        "youtube": "https://www.youtube.com/results?search_query=رياضيات+بحتة+ثانوية+عامة+2026"
    },
    "الرياضيات التطبيقية": {
        "icon": "⚙️",
        "description": "الاستاتيكا - الديناميكا - العزوم - الاحتكاك",
        "difficulty": "مرتفع",
        "topics": ["العزوم", "الاحتكاك", "الاتزان", "الحركة"],
        "youtube": "https://www.youtube.com/results?search_query=رياضيات+تطبيقية+ثانوية+عامة+2026"
    },
    "اللغة العربية": {
        "icon": "📚",
        "description": "النحو - البلاغة - الأدب - النصوص - القراءة",
        "difficulty": "متوسط",
        "topics": ["النحو", "البلاغة", "الأدب", "النصوص", "القراءة"],
        "youtube": "https://www.youtube.com/results?search_query=لغة+عربية+ثانوية+عامة+2026"
    }
}

QUESTION_BANK: Dict[str, List[Dict[str, Any]]] = {
    "الفيزياء": [
        {
            "question": "إذا زاد طول سلك معدني إلى الضعف وقلت مساحة مقطعه إلى النصف، فإن مقاومته:",
            "options": {
                "A": "تزداد إلى أربعة أمثالها",
                "B": "تزداد إلى الضعف",
                "C": "تقل إلى النصف",
                "D": "تظل ثابتة"
            },
            "correct": "A",
            "explanation": """
قانون المقاومة:
R = ρL / A

إذا:
- L أصبح 2L
- A أصبحت A/2

إذن:
R الجديدة = ρ(2L) / (A/2) = 4ρL/A

إذًا المقاومة تزداد إلى أربعة أمثالها.
            """,
            "topic": "قانون أوم",
            "difficulty": "متوسط"
        },
        {
            "question": "مجموع فروق الجهد حول أي مسار مغلق في دائرة كهربية يساوي:",
            "options": {
                "A": "شدة التيار",
                "B": "صفر",
                "C": "المقاومة المكافئة",
                "D": "القدرة الكهربية"
            },
            "correct": "B",
            "explanation": """
وفقًا لقانون كيرشوف الثاني:
المجموع الجبري لفروق الجهد في أي مسار مغلق = صفر.
            """,
            "topic": "قوانين كيرشوف",
            "difficulty": "سهل"
        },
        {
            "question": "إذا كانت القدرة 220 وات وفرق الجهد 110 فولت، فإن شدة التيار تساوي:",
            "options": {
                "A": "0.5 أمبير",
                "B": "1 أمبير",
                "C": "2 أمبير",
                "D": "4 أمبير"
            },
            "correct": "C",
            "explanation": """
نستخدم العلاقة:
P = V × I

إذن:
I = P / V = 220 / 110 = 2 أمبير
            """,
            "topic": "القدرة",
            "difficulty": "سهل"
        }
    ],
    "الكيمياء": [
        {
            "question": "أي من العمليات التالية تؤدي إلى زيادة نسبة الحديد في الخام عن طريق إزالة الشوائب؟",
            "options": {
                "A": "التركيز",
                "B": "التكسير",
                "C": "التلبيد",
                "D": "التحميص"
            },
            "correct": "A",
            "explanation": """
عملية التركيز تهدف إلى رفع نسبة المادة المفيدة في الخام بإزالة أكبر قدر ممكن من الشوائب.
            """,
            "topic": "خام الحديد",
            "difficulty": "سهل"
        },
        {
            "question": "العامل الحفاز يقوم بـ:",
            "options": {
                "A": "زيادة كمية النواتج",
                "B": "تقليل طاقة التنشيط",
                "C": "تغيير ثابت الاتزان",
                "D": "إيقاف التفاعل"
            },
            "correct": "B",
            "explanation": """
العامل الحفاز يوفر مسارًا بديلًا أقل في طاقة التنشيط، وبالتالي يزيد سرعة التفاعل.
            """,
            "topic": "سرعة التفاعل",
            "difficulty": "سهل"
        }
    ],
    "الرياضيات البحتة": [
        {
            "question": "أنسب طريقة لحساب التكامل ∫ x e^x dx هي:",
            "options": {
                "A": "التعويض",
                "B": "التكامل بالتجزئة",
                "C": "الكسور الجزئية",
                "D": "الطريقة البيانية"
            },
            "correct": "B",
            "explanation": """
عندما يكون التكامل حاصل ضرب دالتين، إحداهما جبرية والأخرى أسية، فالطريقة الأنسب غالبًا هي التكامل بالتجزئة.
            """,
            "topic": "التكامل",
            "difficulty": "متوسط"
        },
        {
            "question": "النهاية lim (sin x / x) عندما x تؤول إلى الصفر تساوي:",
            "options": {
                "A": "0",
                "B": "1",
                "C": "∞",
                "D": "-1"
            },
            "correct": "B",
            "explanation": """
من النهايات الشهيرة:
lim (sin x / x) = 1 عندما x → 0
            """,
            "topic": "النهايات",
            "difficulty": "سهل"
        }
    ],
    "الرياضيات التطبيقية": [
        {
            "question": "العزم حول نقطة يساوي:",
            "options": {
                "A": "القوة ÷ الذراع",
                "B": "القوة × ذراعها العمودي",
                "C": "الكتلة × السرعة",
                "D": "الضغط × المساحة"
            },
            "correct": "B",
            "explanation": """
العزم = القوة × ذراع القوة العمودي
وهو مقياس لقدرة القوة على إحداث دوران.
            """,
            "topic": "العزوم",
            "difficulty": "سهل"
        }
    ],
    "اللغة العربية": [
        {
            "question": "في قولنا: 'العلم نور'، الأسلوب البلاغي هو:",
            "options": {
                "A": "تشبيه بليغ",
                "B": "استعارة مكنية",
                "C": "كناية",
                "D": "مجاز مرسل"
            },
            "correct": "A",
            "explanation": """
(العلم نور) تشبيه بليغ لأن أداة التشبيه ووجه الشبه محذوفان.
            """,
            "topic": "البلاغة",
            "difficulty": "متوسط"
        }
    ]
}

DAILY_TASKS = [
    "حل 15 سؤالًا في المادة الأضعف لديك.",
    "مراجعة قانونين أساسيين وكتابتهما بخط اليد.",
    "مراجعة ملف PDF واحد لمدة 25 دقيقة.",
    "مشاهدة شرح مركز لمدة 30 دقيقة ثم تلخيصه.",
    "إعادة حل سؤالين أخطأت فيهما سابقًا.",
    "اختبار سريع من 5 أسئلة لتثبيت الفهم."
]

# =========================================================
# التخزين المحلي
# =========================================================
def default_student_data() -> Dict[str, Any]:
    return {
        "student_name": "أدهم",
        "target_score": 95,
        "theme": "إمبراطوري ليلي",
        "stats": {
            "questions_answered": 0,
            "correct_answers": 0,
            "pdf_opened": 0,
            "video_clicks": 0,
            "mock_exams_taken": 0
        },
        "subject_progress": {subject: 0 for subject in SUBJECTS.keys()},
        "history": [],
        "achievements": [],
        "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def load_data() -> Dict[str, Any]:
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default_student_data()
    return default_student_data()

def save_data(data: Dict[str, Any]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

# =========================================================
# session state
# =========================================================
if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "question_result" not in st.session_state:
    st.session_state.question_result = None

if "exam_questions" not in st.session_state:
    st.session_state.exam_questions = []

if "exam_answers" not in st.session_state:
    st.session_state.exam_answers = {}

if "exam_submitted" not in st.session_state:
    st.session_state.exam_submitted = False

# =========================================================
# أدوات مساعدة
# =========================================================
def calc_percent(part: int, total: int) -> float:
    if total == 0:
        return 0.0
    return round((part / total) * 100, 1)

def get_accuracy() -> float:
    return calc_percent(
        data["stats"]["correct_answers"],
        data["stats"]["questions_answered"]
    )

def get_status_label() -> str:
    acc = get_accuracy()
    if data["stats"]["questions_answered"] == 0:
        return "بداية قوية"
    if acc >= 85:
        return "جاهزية ممتازة"
    if acc >= 70:
        return "أداء قوي"
    if acc >= 50:
        return "يحتاج صقل"
    return "خطة إنقاذ"

def metric_card(label: str, value: str, note: str) -> None:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)

def render_pdf(file_path: Path, height: int = 900) -> None:
    try:
        with open(file_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        pdf_html = f"""
        <iframe
            src="data:application/pdf;base64,{encoded}"
            width="100%"
            height="{height}"
            type="application/pdf">
        </iframe>
        """
        st.markdown(pdf_html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"تعذر عرض ملف PDF: {e}")

def list_pdf_files() -> List[Path]:
    return sorted([p for p in SYLLABUS_DIR.glob("*.pdf") if p.is_file()])

def generate_random_question(subject: str) -> Dict[str, Any] | None:
    bank = QUESTION_BANK.get(subject, [])
    if not bank:
        return None
    return random.choice(bank)

def award_achievement(title: str) -> None:
    if title not in data["achievements"]:
        data["achievements"].append(title)
        save_data(data)

def update_after_answer(subject: str, correct: bool, topic: str, difficulty: str) -> None:
    data["stats"]["questions_answered"] += 1
    if correct:
        data["stats"]["correct_answers"] += 1

    current_progress = data["subject_progress"].get(subject, 0)
    increase = 6 if correct else 2
    data["subject_progress"][subject] = min(100, current_progress + increase)

    data["history"].append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "subject": subject,
        "topic": topic,
        "difficulty": difficulty,
        "correct": correct,
        "mode": "single_question"
    })

    if data["stats"]["questions_answered"] >= 10:
        award_achievement("🏅 أول 10 إجابات")
    if data["stats"]["correct_answers"] >= 25:
        award_achievement("👑 25 إجابة صحيحة")
    if get_accuracy() >= 85 and data["stats"]["questions_answered"] >= 10:
        award_achievement("🔥 دقة أعلى من 85%")

    save_data(data)

def create_mock_exam(subject: str, num_questions: int = 5) -> List[Dict[str, Any]]:
    bank = QUESTION_BANK.get(subject, [])
    if not bank:
        return []
    if len(bank) >= num_questions:
        return random.sample(bank, num_questions)
    return [random.choice(bank) for _ in range(num_questions)]

def today_task() -> str:
    index = date.today().day % len(DAILY_TASKS)
    return DAILY_TASKS[index]

def performance_message() -> str:
    acc = get_accuracy()
    if data["stats"]["questions_answered"] == 0:
        return "ابدأ أول اختبار الآن لتظهر مؤشرات الأداء الذكية."
    if acc >= 85:
        return "أداءك ممتاز جدًا، استمر بنفس النسق."
    if acc >= 70:
        return "مستواك قوي، لكن ما زال هناك هامش للتطوير."
    if acc >= 50:
        return "أنت على الطريق الصحيح لكن تحتاج تقليل الأخطاء."
    return "ابدأ بالمراجعة الأساسية ثم عد للاختبار."

# =========================================================
# الهيدر
# =========================================================
st.markdown(f"""
<div class="hero-box">
    <div class="hero-title">🏛️ {APP_TITLE} — {APP_VERSION}</div>
    <div class="hero-sub">
        منصة تعليمية عربية احترافية فائقة الفخامة للثانوية العامة:
        مكتبة PDF ذكية، اختبارات تفاعلية، متابعة تقدم، خطط يومية، وتحليل أداء بمظهر إمبراطوري راقٍ.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# الشريط الجانبي
# =========================================================
with st.sidebar:
    st.markdown("## 🎛️ لوحة التحكم الإمبراطورية")
    page = st.radio(
        "اختر القسم:",
        [
            "🏠 الرئيسية",
            "📚 مكتبة الكتب (PDF)",
            "🧠 سؤال ذكي",
            "📝 اختبار تجريبي",
            "📺 أكاديمية الفيديو",
            "📈 التحليلات",
            "🎯 الخطة اليومية",
            "⚙️ الإعدادات"
        ]
    )

    st.markdown("---")
    st.markdown(f"**الطالب:** {data['student_name']}")
    st.markdown(f"**الحالة:** {get_status_label()}")
    st.markdown(f"**الهدف:** {data['target_score']}%")
    st.markdown("---")
    st.info("💡 نصيحة النخبة: لا تكتفِ بقراءة الدرس، بل اختبر نفسك فيه فورًا.")
    st.caption("ضع ملفات PDF داخل مجلد Syllabus لتظهر تلقائيًا في المنصة.")

# =========================================================
# الرئيسية
# =========================================================
if page == "🏠 الرئيسية":
    st.markdown('<div class="section-title">لوحة القيادة الرئيسية</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("إجمالي الأسئلة", str(data["stats"]["questions_answered"]), "تم حلها داخل المنصة")
    with c2:
        metric_card("نسبة الدقة", f"{get_accuracy()}%", "معدل الإجابات الصحيحة")
    with c3:
        metric_card("فتح ملفات PDF", str(data["stats"]["pdf_opened"]), "تفاعل المكتبة الرقمية")
    with c4:
        metric_card("الاختبارات التجريبية", str(data["stats"]["mock_exams_taken"]), "عدد الاختبارات المكتملة")

    st.markdown('<div class="section-title">المواد الدراسية</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    for i, (subject, info) in enumerate(SUBJECTS.items()):
        with [col1, col2][i % 2]:
            progress = data["subject_progress"].get(subject, 0)
            st.markdown(f"""
            <div class="subject-card">
                <div class="subject-title">{info['icon']} {subject}</div>
                <div class="subject-meta">
                    الوصف: {info['description']}<br>
                    مستوى الصعوبة: {info['difficulty']}<br>
                    التقدم الحالي: {progress}%
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(progress / 100)

    st.markdown('<div class="section-title">مهمة اليوم</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="glass-card">
        <span class="info-chip">الخطة اليومية</span>
        <div class="small-note">{today_task()}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">الإنجازات</div>', unsafe_allow_html=True)
    if data["achievements"]:
        for ach in data["achievements"]:
            st.markdown(f"<div class='glass-card'>{ach}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-card'>ابدأ الحل الآن لفتح أول إنجاز لك.</div>", unsafe_allow_html=True)

# =========================================================
# مكتبة الكتب
# =========================================================
elif page == "📚 مكتبة الكتب (PDF)":
    st.markdown('<div class="section-title">المكتبة الرقمية للكتب والمراجعات</div>', unsafe_allow_html=True)

    pdf_files = list_pdf_files()

    if not pdf_files:
        st.warning("لا توجد ملفات PDF داخل مجلد Syllabus حالياً.")
        st.info("أنشئ مجلدًا باسم Syllabus وضع بداخله الكتب أو المذكرات أو الملخصات.")
    else:
        file_names = [p.name for p in pdf_files]
        selected_name = st.selectbox("اختر الملف:", file_names)
        selected_path = next(p for p in pdf_files if p.name == selected_name)

        c1, c2 = st.columns(2)
        with c1:
            with open(selected_path, "rb") as f:
                st.download_button(
                    "📥 تحميل الملف",
                    data=f,
                    file_name=selected_path.name,
                    mime="application/pdf"
                )
        with c2:
            if st.button("📖 تسجيل فتح الملف"):
                data["stats"]["pdf_opened"] += 1
                save_data(data)
                st.success("تم تسجيل التفاعل مع الملف.")

        st.markdown(f"""
        <div class="glass-card">
            <div class="subject-title">📘 {selected_path.name}</div>
            <div class="small-note">
                الحجم: {round(selected_path.stat().st_size / 1024, 2)} كيلوبايت
            </div>
        </div>
        """, unsafe_allow_html=True)

        render_pdf(selected_path, height=950)

# =========================================================
# سؤال ذكي
# =========================================================
elif page == "🧠 سؤال ذكي":
    st.markdown('<div class="section-title">بنك الأسئلة الذكي</div>', unsafe_allow_html=True)

    subject = st.selectbox("اختر المادة:", list(SUBJECTS.keys()))
    info = SUBJECTS[subject]

    st.markdown(f"""
    <div class="glass-card">
        <span class="info-chip">المادة: {subject}</span>
        <span class="info-chip">الصعوبة: {info['difficulty']}</span>
        <span class="info-chip">الموضوعات: {len(info['topics'])}</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🎯 توليد سؤال جديد"):
        st.session_state.current_question = generate_random_question(subject)
        st.session_state.question_result = None

    q = st.session_state.current_question

    if q:
        st.markdown(f"""
        <div class="glass-card">
            <div class="subject-title">🧩 السؤال</div>
            <div class="small-note" style="font-size:1rem;color:#f8fafc;">{q['question']}</div>
            <div class="small-note" style="margin-top:10px;">الموضوع: {q['topic']} | المستوى: {q['difficulty']}</div>
        </div>
        """, unsafe_allow_html=True)

        options_labels = [f"{key}) {value}" for key, value in q["options"].items()]
        user_choice = st.radio("اختر الإجابة:", options_labels, key="single_question_answer")

        if st.button("✅ تأكيد الإجابة"):
            selected_key = user_choice.split(")")[0].strip()
            is_correct = selected_key == q["correct"]

            st.session_state.question_result = {
                "correct": is_correct,
                "correct_key": q["correct"],
                "explanation": q["explanation"]
            }

            update_after_answer(subject, is_correct, q["topic"], q["difficulty"])

    if st.session_state.question_result:
        res = st.session_state.question_result
        if res["correct"]:
            st.markdown("<div class='success-box'>✅ إجابة صحيحة — أداء ممتاز.</div>", unsafe_allow_html=True)
        else:
            st.markdown(
                f"<div class='error-box'>❌ إجابة غير صحيحة — الإجابة الصحيحة هي: {res['correct_key']}</div>",
                unsafe_allow_html=True
            )
        st.markdown("### ✍️ شرح الإجابة")
        st.markdown(res["explanation"])

# =========================================================
# اختبار تجريبي
# =========================================================
elif page == "📝 اختبار تجريبي":
    st.markdown('<div class="section-title">اختبار تجريبي مصغر</div>', unsafe_allow_html=True)

    subject = st.selectbox("اختر مادة الاختبار:", list(SUBJECTS.keys()), key="exam_subject")
    q_count = st.slider("عدد الأسئلة", min_value=3, max_value=10, value=5)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚀 إنشاء اختبار جديد"):
            st.session_state.exam_questions = create_mock_exam(subject, q_count)
            st.session_state.exam_answers = {}
            st.session_state.exam_submitted = False

    with c2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="small-note">{SUBJECTS[subject]['description']}</div>
        </div>
        """, unsafe_allow_html=True)

    exam_questions = st.session_state.exam_questions

    if exam_questions:
        for idx, q in enumerate(exam_questions, start=1):
            st.markdown(f"""
            <div class="glass-card">
                <div class="subject-title">السؤال {idx}</div>
                <div class="small-note">{q['question']}</div>
            </div>
            """, unsafe_allow_html=True)

            labels = [f"{k}) {v}" for k, v in q["options"].items()]
            answer = st.radio(
                f"إجابة السؤال {idx}",
                labels,
                key=f"exam_q_{idx}"
            )
            st.session_state.exam_answers[idx] = answer.split(")")[0].strip()

        if st.button("📌 تسليم الاختبار"):
            st.session_state.exam_submitted = True

        if st.session_state.exam_submitted:
            total = len(exam_questions)
            correct_count = 0

            st.markdown("### 📋 النتيجة التفصيلية")
            for idx, q in enumerate(exam_questions, start=1):
                user_ans = st.session_state.exam_answers.get(idx, "")
                is_correct = user_ans == q["correct"]
                if is_correct:
                    correct_count += 1
                    st.markdown(
                        f"<div class='success-box'>السؤال {idx}: إجابة صحيحة ✅</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"<div class='error-box'>السؤال {idx}: إجابة خاطئة ❌ | الصحيحة: {q['correct']}</div>",
                        unsafe_allow_html=True
                    )

                data["history"].append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "subject": subject,
                    "topic": q["topic"],
                    "difficulty": q["difficulty"],
                    "correct": is_correct,
                    "mode": "mock_exam"
                })

            data["stats"]["questions_answered"] += total
            data["stats"]["correct_answers"] += correct_count
            data["stats"]["mock_exams_taken"] += 1

            progress = data["subject_progress"].get(subject, 0)
            data["subject_progress"][subject] = min(100, progress + max(5, correct_count * 3))

            if correct_count == total:
                award_achievement("🏆 درجة كاملة في اختبار تجريبي")

            save_data(data)

            score_percent = calc_percent(correct_count, total)
            st.markdown(f"""
            <div class="glass-card">
                <div class="subject-title">النتيجة النهائية</div>
                <div class="small-note">
                    الدرجة: {correct_count} من {total}<br>
                    النسبة: {score_percent}%
                </div>
            </div>
            """, unsafe_allow_html=True)

# =========================================================
# الفيديو
# =========================================================
elif page == "📺 أكاديمية الفيديو":
    st.markdown('<div class="section-title">أكاديمية الفيديو التعليمية</div>', unsafe_allow_html=True)

    for subject, info in SUBJECTS.items():
        with st.expander(f"{info['icon']} {subject}", expanded=False):
            st.markdown(f"""
            <div class="glass-card">
                <div class="subject-title">{subject}</div>
                <div class="small-note">
                    {info['description']}<br>
                    موضوعات رئيسية: {", ".join(info['topics'])}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"📺 فتح شروحات {subject}", key=f"video_{subject}"):
                data["stats"]["video_clicks"] += 1
                save_data(data)
                st.link_button(f"الانتقال إلى شروحات {subject}", info["youtube"])

# =========================================================
# التحليلات
# =========================================================
elif page == "📈 التحليلات":
    st.markdown('<div class="section-title">التحليلات ومؤشرات الأداء</div>', unsafe_allow_html=True)

    total_q = data["stats"]["questions_answered"]
    correct_q = data["stats"]["correct_answers"]
    wrong_q = max(total_q - correct_q, 0)
    accuracy = get_accuracy()

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("الإجابات الصحيحة", str(correct_q), "مجموع الحلول الصحيحة")
    with c2:
        metric_card("الإجابات الخاطئة", str(wrong_q), "مجموع الأسئلة غير الصحيحة")
    with c3:
        metric_card("الدقة الكلية", f"{accuracy}%", performance_message())

    st.markdown("### 📘 نسب التقدم حسب المواد")
    progress_df = pd.DataFrame([
        {"المادة": subject, "نسبة التقدم": data["subject_progress"].get(subject, 0)}
        for subject in SUBJECTS.keys()
    ])
    st.dataframe(progress_df, use_container_width=True, hide_index=True)

    if data["history"]:
        history_df = pd.DataFrame(data["history"])
        history_df = history_df.rename(columns={
            "time": "الوقت",
            "subject": "المادة",
            "topic": "الموضوع",
            "difficulty": "الصعوبة",
            "correct": "النتيجة",
            "mode": "الوضع"
        })
        history_df["النتيجة"] = history_df["النتيجة"].map({True: "صحيحة", False: "خاطئة"})
        st.markdown("### 🕒 سجل النشاط")
        st.dataframe(history_df.iloc[::-1], use_container_width=True, hide_index=True)

        grouped = (
            pd.DataFrame(data["history"])
            .groupby("subject")["correct"]
            .agg(["count", "sum"])
            .reset_index()
        )
        grouped.columns = ["المادة", "إجمالي الإجابات", "الإجابات الصحيحة"]
        st.markdown("### 📊 ملخص حسب المادة")
        st.dataframe(grouped, use_container_width=True, hide_index=True)
    else:
        st.info("لا توجد بيانات كافية بعد. ابدأ بحل الأسئلة لتظهر التحليلات.")

# =========================================================
# الخطة اليومية
# =========================================================
elif page == "🎯 الخطة اليومية":
    st.markdown('<div class="section-title">الخطة اليومية التنفيذية</div>', unsafe_allow_html=True)

    acc = get_accuracy()

    if acc >= 85:
        plan = "أنت مؤهل اليوم لاختبار قوي ثم مراجعة مركزة للأخطاء النادرة."
    elif acc >= 70:
        plan = "أفضل تقسيم اليوم: مراجعة قصيرة + اختبار متوسط + تصحيح مباشر."
    elif acc >= 50:
        plan = "ركز اليوم على الأساسيات مع 5 أسئلة تدريبية فقط لكل مادة صعبة."
    else:
        plan = "خطة إنقاذ: ابدأ بالشرح ثم الأسئلة السهلة ثم التدرج."

    tasks = [
        today_task(),
        "حل اختبار سريع من 5 أسئلة.",
        "فتح مذكرة PDF واحدة ومراجعتها 25 دقيقة.",
        "مشاهدة فيديو واحد فقط وتلخيص أهم 3 نقاط.",
        "إعادة سؤالين خاطئين سابقًا حتى تثبيت الفكرة."
    ]

    st.markdown(f"""
    <div class="glass-card">
        <div class="subject-title">📌 توصية ذكية</div>
        <div class="small-note">{plan}</div>
    </div>
    """, unsafe_allow_html=True)

    for i, task in enumerate(tasks, start=1):
        st.markdown(f"""
        <div class="glass-card">
            <span class="info-chip">المهمة {i}</span>
            <div class="small-note">{task}</div>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# الإعدادات
# =========================================================
elif page == "⚙️ الإعدادات":
    st.markdown('<div class="section-title">إعدادات المنصة</div>', unsafe_allow_html=True)

    student_name = st.text_input("اسم الطالب", value=data.get("student_name", "أدهم"))
    target_score = st.slider("الهدف النهائي", 50, 100, int(data.get("target_score", 95)))
    theme_mode = st.selectbox("النمط البصري", ["إمبراطوري ليلي", "ذهبي رسمي", "أزرق ملكي"], index=0)

    if st.button("💾 حفظ الإعدادات"):
        data["student_name"] = student_name.strip() or "أدهم"
        data["target_score"] = target_score
        data["theme"] = theme_mode
        data["last_seen"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_data(data)
        st.success("تم حفظ الإعدادات بنجاح.")

    st.markdown("### 🧹 أدوات النظام")
    if st.button("إعادة ضبط السجل والإحصاءات"):
        current_name = data.get("student_name", "أدهم")
        current_target = data.get("target_score", 95)
        current_theme = data.get("theme", "إمبراطوري ليلي")

        new_data = default_student_data()
        new_data["student_name"] = current_name
        new_data["target_score"] = current_target
        new_data["theme"] = current_theme

        save_data(new_data)
        st.success("تمت إعادة ضبط السجل بنجاح. أعد تحميل الصفحة.")

# =========================================================
# الفوتر
# =========================================================
st.markdown("""
<div class="footer-note">
    حصن أدهم التعليمي — إصدار احترافي قابل للتوسع لاحقًا إلى:
    حسابات متعددة، ولي أمر، مدرس، تقارير PDF، ذكاء اصطناعي، وبنك أسئلة ضخم.
</div>
""", unsafe_allow_html=True)
