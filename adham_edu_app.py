# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import json
import math
import random
import base64
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List, Any, Tuple

import pandas as pd
import streamlit as st

# =========================================================
# ADHAM EDUCATION FORTRESS V50 - WORLD CLASS EDITION
# =========================================================

APP_TITLE = "حصن أدهم التعليمي V50"
APP_ICON = "🎓"
DATA_DIR = Path("adham_fortress_data")
DATA_FILE = DATA_DIR / "student_profile.json"
SYLLABUS_DIR = Path("Syllabus")

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# Bootstrap
# =========================================================
DATA_DIR.mkdir(parents=True, exist_ok=True)
SYLLABUS_DIR.mkdir(parents=True, exist_ok=True)

# =========================================================
# Theme / CSS
# =========================================================
def inject_css() -> None:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');

    html, body, [class*="st-"], .stMarkdown, .stText, .stSelectbox, .stButton, .stRadio, .stTabs {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: right;
    }

    .stApp {
        background:
            radial-gradient(circle at top right, rgba(26,58,109,0.35), transparent 30%),
            radial-gradient(circle at top left, rgba(255,215,0,0.08), transparent 25%),
            linear-gradient(180deg, #07111d 0%, #0b1624 50%, #0d1828 100%);
        color: #edf2f7;
    }

    .main-shell {
        background: linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 28px;
        padding: 22px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.35);
        backdrop-filter: blur(8px);
        margin-bottom: 18px;
    }

    .hero-box {
        border-radius: 30px;
        padding: 32px 28px;
        background:
            linear-gradient(135deg, rgba(11,27,49,0.92), rgba(15,30,56,0.88)),
            linear-gradient(135deg, #0e2039, #0d1a2f);
        border: 1px solid rgba(255,215,0,0.18);
        box-shadow: 0 24px 70px rgba(0,0,0,0.35);
        margin-bottom: 22px;
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 900;
        color: #ffd54f;
        margin-bottom: 8px;
        text-align: center;
        text-shadow: 0 2px 18px rgba(255, 215, 0, 0.15);
    }

    .hero-subtitle {
        font-size: 1.02rem;
        color: #dbe7ff;
        text-align: center;
        line-height: 1.9;
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #ffe082;
        margin: 8px 0 14px 0;
        padding-right: 10px;
        border-right: 4px solid #ffd54f;
    }

    .metric-card {
        border-radius: 22px;
        padding: 18px 18px;
        background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.025));
        border: 1px solid rgba(255,255,255,0.08);
        min-height: 128px;
        box-shadow: 0 12px 35px rgba(0,0,0,0.22);
    }

    .metric-label {
        color: #b8c6db;
        font-size: 0.95rem;
        margin-bottom: 10px;
        font-weight: 700;
    }

    .metric-value {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 900;
        margin-bottom: 8px;
    }

    .metric-note {
        color: #9ed3ff;
        font-size: 0.93rem;
        font-weight: 600;
    }

    .glass-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.045), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 24px;
        padding: 18px;
        box-shadow: 0 12px 32px rgba(0,0,0,0.20);
        margin-bottom: 14px;
    }

    .subject-tile {
        background: linear-gradient(135deg, rgba(255,215,0,0.07), rgba(255,255,255,0.03));
        border: 1px solid rgba(255,215,0,0.16);
        border-radius: 20px;
        padding: 18px;
        box-shadow: 0 10px 28px rgba(0,0,0,0.20);
        margin-bottom: 12px;
    }

    .subject-name {
        color: #fff0b3;
        font-size: 1.15rem;
        font-weight: 800;
    }

    .subject-meta {
        color: #d7e6ff;
        font-size: 0.92rem;
        line-height: 1.8;
    }

    .result-success {
        background: rgba(34, 197, 94, 0.12);
        border: 1px solid rgba(34, 197, 94, 0.45);
        color: #d9ffe7;
        border-radius: 18px;
        padding: 16px;
        font-weight: 700;
        margin-top: 12px;
    }

    .result-error {
        background: rgba(239, 68, 68, 0.10);
        border: 1px solid rgba(239, 68, 68, 0.40);
        color: #ffe0e0;
        border-radius: 18px;
        padding: 16px;
        font-weight: 700;
        margin-top: 12px;
    }

    .info-chip {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(255,215,0,0.11);
        border: 1px solid rgba(255,215,0,0.18);
        color: #ffe082;
        font-size: 0.88rem;
        font-weight: 700;
        margin: 0 0 8px 8px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 14px !important;
        min-height: 46px;
        font-weight: 800 !important;
        border: 1px solid rgba(255,215,0,0.30) !important;
        background: linear-gradient(135deg, #f4c430, #ffd54f) !important;
        color: #111827 !important;
        box-shadow: 0 8px 22px rgba(244,196,48,0.28);
    }

    .stDownloadButton > button {
        width: 100%;
        border-radius: 14px !important;
        min-height: 46px;
        font-weight: 800 !important;
    }

    .stSelectbox label, .stRadio label, .stTextInput label, .stTextArea label {
        font-weight: 800 !important;
        color: #f5f7fb !important;
    }

    div[data-testid="stMetric"] {
        background: transparent !important;
        border: none !important;
    }

    .footer-note {
        text-align: center;
        color: #b7c9e3;
        font-size: 0.9rem;
        margin-top: 24px;
        opacity: 0.9;
    }

    iframe {
        border-radius: 20px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        background: #fff;
    }

    .small-muted {
        color: #b8c6db;
        font-size: 0.9rem;
        line-height: 1.8;
    }
    </style>
    """, unsafe_allow_html=True)

inject_css()

# =========================================================
# Master Data
# =========================================================
SUBJECTS_DATA: Dict[str, Dict[str, Any]] = {
    "اللغة العربية": {
        "icon": "📜",
        "description": "نحو، بلاغة، أدب، نصوص، قراءة، تعبير",
        "difficulty": "متوسط",
        "yt": "https://www.youtube.com/results?search_query=لغة+عربية+ثانوية+عامة+2026",
        "topics": ["النحو", "البلاغة", "الأدب", "النصوص", "القراءة", "التعبير"]
    },
    "اللغة الإنجليزية": {
        "icon": "🌍",
        "description": "Vocabulary, Grammar, Reading, Writing",
        "difficulty": "متوسط",
        "yt": "https://www.youtube.com/results?search_query=انجليزي+ثانوية+عامة+2026",
        "topics": ["Grammar", "Vocabulary", "Reading", "Writing"]
    },
    "الفيزياء": {
        "icon": "⚡",
        "description": "الكهربية، الحركة، الشغل والطاقة، الدوائر، الموجات",
        "difficulty": "مرتفع",
        "yt": "https://www.youtube.com/results?search_query=فيزياء+ثانوية+عامة+2026",
        "topics": ["قوانين كيرشوف", "التيار الكهربي", "الحركة", "الشغل والطاقة", "الموجات"]
    },
    "الكيمياء": {
        "icon": "🧪",
        "description": "العضوية، الاتزان، الأحماض والقواعد، الكيمياء الكهربية",
        "difficulty": "متوسط",
        "yt": "https://www.youtube.com/results?search_query=كيمياء+ثانوية+عامة+2026",
        "topics": ["الاتزان الكيميائي", "الأحماض والقواعد", "الكيمياء العضوية", "الخلايا الجلفانية"]
    },
    "الأحياء": {
        "icon": "🧬",
        "description": "الوراثة، الدعامة والحركة، التكاثر، الهرمونات",
        "difficulty": "متوسط",
        "yt": "https://www.youtube.com/results?search_query=احياء+ثانوية+عامة+2026",
        "topics": ["الوراثة", "الهرمونات", "التكاثر", "الدعامة والحركة"]
    },
    "الرياضيات البحتة": {
        "icon": "📐",
        "description": "التفاضل، التكامل، الجبر، الهندسة التحليلية",
        "difficulty": "مرتفع",
        "yt": "https://www.youtube.com/results?search_query=رياضيات+بحتة+ثانوية+عامة+2026",
        "topics": ["التكامل بالتجزئة", "النهايات", "المصفوفات", "الهندسة التحليلية"]
    },
    "الرياضيات التطبيقية": {
        "icon": "⚙️",
        "description": "الاستاتيكا، الديناميكا، العزوم، الاحتكاك",
        "difficulty": "مرتفع",
        "yt": "https://www.youtube.com/results?search_query=رياضيات+تطبيقية+ثانوية+عامة+2026",
        "topics": ["العزوم في الاستاتيكا", "الاحتكاك", "الحركة الخطية", "المقذوفات"]
    }
}

QUESTION_BANK: Dict[str, List[Dict[str, Any]]] = {
    "الفيزياء": [
        {
            "question": "عند تطبيق قانون كيرشوف الثاني على دائرة كهربية، فإن مجموع فروق الجهد حول أي مسار مغلق يساوي:",
            "options": {
                "A": "فرق الجهد الكلي للمصدر فقط",
                "B": "صفر",
                "C": "شدة التيار الكلية",
                "D": "المقاومة المكافئة"
            },
            "correct": "B",
            "explanation": """
قانون كيرشوف الثاني ينص على أن المجموع الجبري لفروق الجهد في أي مسار مغلق يساوي صفرًا.

$$\\sum V = 0$$

وذلك لأن الطاقة المكتسبة من المصادر تساوي الطاقة المفقودة عبر المقاومات والعناصر الأخرى.
            """,
            "topic": "قوانين كيرشوف",
            "difficulty": "متوسط"
        },
        {
            "question": "إذا كانت القدرة الكهربية لجهاز تساوي 220 واط ويعمل على فرق جهد 110 فولت، فإن شدة التيار المار فيه تساوي:",
            "options": {
                "A": "0.5 أمبير",
                "B": "1 أمبير",
                "C": "2 أمبير",
                "D": "4 أمبير"
            },
            "correct": "C",
            "explanation": """
نستخدم العلاقة:

$$P = V \\times I$$

إذن:

$$I = \\frac{P}{V} = \\frac{220}{110} = 2\\ \\text{أمبير}$$
            """,
            "topic": "القدرة الكهربية",
            "difficulty": "سهل"
        }
    ],
    "الكيمياء": [
        {
            "question": "أي العبارات التالية تصف العامل الحفاز بدقة؟",
            "options": {
                "A": "يزيد كمية النواتج النهائية",
                "B": "يرفع حرارة التفاعل تلقائيًا",
                "C": "يقلل طاقة التنشيط دون أن يستهلك",
                "D": "يغير ثابت الاتزان"
            },
            "correct": "C",
            "explanation": """
العامل الحفاز يعمل على توفير مسار بديل للتفاعل بطاقة تنشيط أقل، ولذلك يزيد سرعة التفاعل دون أن يُستهلك.

ولا يغير ثابت الاتزان، بل يؤثر فقط على سرعة الوصول إلى الاتزان.
            """,
            "topic": "سرعة التفاعل",
            "difficulty": "سهل"
        }
    ],
    "الرياضيات البحتة": [
        {
            "question": "إذا كان $$\\int x e^x \\, dx$$، فإن الطريقة الأنسب للحل هي:",
            "options": {
                "A": "التعويض",
                "B": "التكامل بالتجزئة",
                "C": "الكسور الجزئية",
                "D": "التقريب العددي"
            },
            "correct": "B",
            "explanation": """
عندما يكون التكامل ناتج ضرب دالتين إحداهما جبرية والأخرى أسية، فالطريقة المناسبة غالبًا هي التكامل بالتجزئة:

$$\\int u \\, dv = uv - \\int v \\, du$$

نختار:
- $$u = x$$
- $$dv = e^x dx$$
            """,
            "topic": "التكامل بالتجزئة",
            "difficulty": "متوسط"
        }
    ],
    "الرياضيات التطبيقية": [
        {
            "question": "في الاستاتيكا، يُحسب العزم حول نقطة باستخدام:",
            "options": {
                "A": "القوة ÷ الذراع",
                "B": "القوة × ذراعها",
                "C": "الكتلة × السرعة",
                "D": "الضغط × المساحة"
            },
            "correct": "B",
            "explanation": """
العزم يساوي حاصل ضرب القوة في ذراع القوة العمودي:

$$\\tau = F \\times d$$

حيث:
- $$F$$ القوة
- $$d$$ ذراع القوة العمودي
            """,
            "topic": "العزوم",
            "difficulty": "سهل"
        }
    ],
    "اللغة العربية": [
        {
            "question": "الأسلوب البلاغي في قولنا: 'العلم نور' هو:",
            "options": {
                "A": "تشبيه بليغ",
                "B": "كناية",
                "C": "استعارة مكنية",
                "D": "مجاز مرسل"
            },
            "correct": "A",
            "explanation": """
'العلم نور' من التشبيه البليغ لأن:
- المشبه: العلم
- المشبه به: النور
- حُذفت أداة التشبيه ووجه الشبه

فبقي التركيب في صورة تشبيه بليغ.
            """,
            "topic": "البلاغة",
            "difficulty": "متوسط"
        }
    ],
    "اللغة الإنجليزية": [
        {
            "question": "Choose the correct sentence:",
            "options": {
                "A": "He have finished his homework.",
                "B": "He has finished his homework.",
                "C": "He finishing his homework.",
                "D": "He finish his homework."
            },
            "correct": "B",
            "explanation": """
The correct present perfect structure is:

**He has finished his homework.**

Because:
- Subject = He
- Auxiliary = has
- Past participle = finished
            """,
            "topic": "Grammar",
            "difficulty": "سهل"
        }
    ],
    "الأحياء": [
        {
            "question": "الحمض النووي المسؤول عن نقل الشفرة الوراثية من النواة إلى الريبوسوم هو:",
            "options": {
                "A": "DNA",
                "B": "rRNA",
                "C": "mRNA",
                "D": "tRNA"
            },
            "correct": "C",
            "explanation": """
الـ mRNA هو الحمض النووي الريبوزي الرسول، ووظيفته نقل الشفرة الوراثية من DNA داخل النواة إلى الريبوسومات ليتم تصنيع البروتين.
            """,
            "topic": "الوراثة",
            "difficulty": "سهل"
        }
    ]
}

DAILY_TASKS = [
    "حل 20 سؤالًا في المادة الأصعب لديك.",
    "مراجعة قانون أو قاعدة رئيسية من درس الأمس.",
    "قراءة ملخص واحد من مكتبة الـ PDF.",
    "مشاهدة فيديو شرح مركز لمدة 30 دقيقة.",
    "حل سؤالين مقاليين وكتابة خطوات الحل.",
    "إعادة اختبار خاطئ من بنك الأسئلة وتحليل الخطأ."
]

# =========================================================
# Persistence
# =========================================================
def default_profile() -> Dict[str, Any]:
    return {
        "student_name": "أدهم",
        "target_score": 95,
        "theme_mode": "إمبراطوري ليلي",
        "stats": {
            "questions_answered": 0,
            "correct_answers": 0,
            "study_minutes": 0,
            "pdf_views": 0,
            "video_clicks": 0
        },
        "subject_progress": {subject: 0 for subject in SUBJECTS_DATA.keys()},
        "exam_history": [],
        "last_login": str(datetime.now())
    }

def load_profile() -> Dict[str, Any]:
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception:
            return default_profile()
    return default_profile()

def save_profile(data: Dict[str, Any]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

profile = load_profile()

# =========================================================
# Session State
# =========================================================
if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = list(SUBJECTS_DATA.keys())[0]

# =========================================================
# Helpers
# =========================================================
def percent(part: int, whole: int) -> float:
    if whole <= 0:
        return 0.0
    return round((part / whole) * 100, 1)

def get_pdf_files() -> List[Path]:
    return sorted([p for p in SYLLABUS_DIR.glob("*.pdf") if p.is_file()])

def render_pdf(file_path: Path, height: int = 900) -> None:
    try:
        with open(file_path, "rb") as f:
            encoded_pdf = base64.b64encode(f.read()).decode("utf-8")
        iframe = f"""
        <iframe
            src="data:application/pdf;base64,{encoded_pdf}"
            width="100%"
            height="{height}"
            type="application/pdf">
        </iframe>
        """
        st.markdown(iframe, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"تعذر عرض الملف: {e}")

def smart_study_status() -> str:
    answered = profile["stats"]["questions_answered"]
    correct = profile["stats"]["correct_answers"]
    accuracy = percent(correct, answered)
    if answered == 0:
        return "بداية قوية"
    if accuracy >= 85:
        return "جاهزية ممتازة"
    if accuracy >= 70:
        return "أداء جيد جدًا"
    if accuracy >= 50:
        return "يحتاج رفع الدقة"
    return "التركيز مطلوب"

def next_daily_task() -> str:
    today_index = date.today().day % len(DAILY_TASKS)
    return DAILY_TASKS[today_index]

def get_random_question(subject: str) -> Dict[str, Any] | None:
    questions = QUESTION_BANK.get(subject, [])
    if not questions:
        return None
    return random.choice(questions)

def record_answer(subject: str, is_correct: bool, topic: str, difficulty: str) -> None:
    profile["stats"]["questions_answered"] += 1
    if is_correct:
        profile["stats"]["correct_answers"] += 1

    # رفع تقدّم المادة تدريجيًا
    old_progress = profile["subject_progress"].get(subject, 0)
    increment = 5 if is_correct else 2
    profile["subject_progress"][subject] = min(100, old_progress + increment)

    profile["exam_history"].append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "subject": subject,
        "topic": topic,
        "difficulty": difficulty,
        "correct": is_correct
    })

    save_profile(profile)

def render_metric_card(label: str, value: str, note: str) -> None:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)

def chart_dataframe() -> pd.DataFrame:
    history = profile.get("exam_history", [])
    if not history:
        return pd.DataFrame(columns=["المادة", "الإجابات", "الصحيحة"])
    df = pd.DataFrame(history)
    grouped = (
        df.groupby("subject")["correct"]
        .agg(["count", "sum"])
        .reset_index()
        .rename(columns={"subject": "المادة", "count": "الإجابات", "sum": "الصحيحة"})
    )
    return grouped

def performance_message() -> str:
    total = profile["stats"]["questions_answered"]
    correct = profile["stats"]["correct_answers"]
    acc = percent(correct, total)
    if total == 0:
        return "ابدأ أول اختبار الآن لتظهر مؤشرات الأداء والتحليل."
    if acc >= 85:
        return "مستوى متميز جدًا، استمر في المحافظة على نفس النسق."
    if acc >= 70:
        return "مستواك قوي، لكن ما زال هناك هامش لتحسين الدقة والسرعة."
    if acc >= 50:
        return "هناك أساس جيد، لكن تحتاج إلى مراجعة الأخطاء المتكررة."
    return "ابدأ بخطة إنقاذ سريعة: مراجعة الأساسيات ثم اختبار قصير يومي."

# =========================================================
# Sidebar
# =========================================================
with st.sidebar:
    st.markdown("## 🎛️ غرفة التحكم التنفيذية")
    page = st.radio(
        "اختر الواجهة:",
        [
            "🏠 الرئيسية",
            "📚 المكتبة الرقمية",
            "🧠 بنك الأسئلة الذكي",
            "📺 أكاديمية الفيديو",
            "📈 التحليلات والأداء",
            "🗓️ الخطة اليومية",
            "⚙️ الإعدادات"
        ]
    )

    st.markdown("---")
    st.markdown(f"**الطالب:** {profile['student_name']}")
    st.markdown(f"**الحالة:** {smart_study_status()}")
    st.markdown(f"**الهدف:** {profile['target_score']}%")
    st.markdown("---")
    st.info("💡 نصيحة النخبة: لا تكرر المعلومة فقط، بل اختبر نفسك عليها.")
    st.caption("📁 ضع ملفات PDF داخل مجلد Syllabus لتظهر تلقائيًا في المكتبة.")

# =========================================================
# Header
# =========================================================
st.markdown("""
<div class="hero-box">
    <div class="hero-title">🏛️ حصن أدهم التعليمي — منصة النخبة 2026</div>
    <div class="hero-subtitle">
        منصة تعليمية عربية احترافية مصممة لتجربة ثانوية عامة من الطراز الرفيع:
        مكتبة ذكية، اختبارات تفاعلية، تحليل أداء، متابعة يومية، وتجربة بصرية فاخرة.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# Pages
# =========================================================
if page == "🏠 الرئيسية":
    st.markdown('<div class="section-title">لوحة القيادة الرئيسية</div>', unsafe_allow_html=True)

    total_questions = profile["stats"]["questions_answered"]
    correct_answers = profile["stats"]["correct_answers"]
    accuracy = percent(correct_answers, total_questions)
    pdf_views = profile["stats"]["pdf_views"]
    video_clicks = profile["stats"]["video_clicks"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("إجمالي الأسئلة", str(total_questions), "تم حلها داخل المنصة")
    with c2:
        render_metric_card("نسبة الدقة", f"{accuracy}%", "معدل الإجابات الصحيحة")
    with c3:
        render_metric_card("مرات فتح ملفات PDF", str(pdf_views), "تفاعل مع المكتبة الرقمية")
    with c4:
        render_metric_card("ضغطات الفيديو", str(video_clicks), "متابعة المحتوى المرئي")

    st.markdown('<div class="section-title">المواد الدراسية</div>', unsafe_allow_html=True)
    cols = st.columns(2)
    subjects = list(SUBJECTS_DATA.items())

    for idx, (subject, info) in enumerate(subjects):
        with cols[idx % 2]:
            progress = profile["subject_progress"].get(subject, 0)
            st.markdown(f"""
            <div class="subject-tile">
                <div class="subject-name">{info['icon']} {subject}</div>
                <div class="subject-meta">
                    الوصف: {info['description']}<br>
                    مستوى الصعوبة: {info['difficulty']}<br>
                    التقدم الحالي: {progress}%
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(progress / 100)

    st.markdown('<div class="section-title">المهمة اليومية المقترحة</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="glass-card">
        <span class="info-chip">خطة اليوم</span>
        <div class="small-muted">{next_daily_task()}</div>
    </div>
    """, unsafe_allow_html=True)

elif page == "📚 المكتبة الرقمية":
    st.markdown('<div class="section-title">المكتبة الرقمية للكتب والمراجعات</div>', unsafe_allow_html=True)

    pdf_files = get_pdf_files()

    if not pdf_files:
        st.warning("لا توجد ملفات PDF داخل مجلد Syllabus حالياً. أضف ملفاتك وسيتم اكتشافها تلقائيًا.")
    else:
        file_names = [f.name for f in pdf_files]
        selected_name = st.selectbox("اختر الملف الذي تريد فتحه:", file_names)
        selected_path = next(p for p in pdf_files if p.name == selected_name)

        c1, c2 = st.columns([1, 1])
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
                profile["stats"]["pdf_views"] += 1
                save_profile(profile)
                st.success("تم تسجيل التفاعل مع الملف.")

        st.markdown(f"""
        <div class="glass-card">
            <div class="subject-name">📘 {selected_path.name}</div>
            <div class="small-muted">
                الحجم التقريبي: {round(selected_path.stat().st_size / 1024, 2)} كيلوبايت
            </div>
        </div>
        """, unsafe_allow_html=True)

        render_pdf(selected_path, height=950)

elif page == "🧠 بنك الأسئلة الذكي":
    st.markdown('<div class="section-title">بنك الأسئلة الذكي</div>', unsafe_allow_html=True)

    subject = st.selectbox("اختر المادة:", list(SUBJECTS_DATA.keys()), key="subject_select")
    st.session_state.selected_subject = subject

    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("🎯 توليد سؤال جديد"):
            question_data = get_random_question(subject)
            if question_data:
                st.session_state.current_question = question_data
                st.session_state.last_result = None
            else:
                st.warning("لا توجد أسئلة متاحة حالياً لهذه المادة.")

    with col_b:
        st.markdown(f"""
        <div class="glass-card">
            <span class="info-chip">المادة الحالية</span>
            <span class="info-chip">الموضوعات: {len(SUBJECTS_DATA[subject]['topics'])}</span>
            <span class="info-chip">الصعوبة: {SUBJECTS_DATA[subject]['difficulty']}</span>
        </div>
        """, unsafe_allow_html=True)

    q = st.session_state.current_question
    if q:
        st.markdown(f"""
        <div class="glass-card">
            <div class="subject-name">🧩 السؤال</div>
            <div class="small-muted" style="font-size:1rem;color:#f5f7fb;margin-top:10px;">
                {q['question']}
            </div>
            <div class="small-muted" style="margin-top:10px;">
                الموضوع: {q['topic']} | المستوى: {q['difficulty']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        options_map = q["options"]
        radio_labels = [f"{key}) {value}" for key, value in options_map.items()]
        selected_option = st.radio("اختر الإجابة:", radio_labels, key="answer_radio")

        if st.button("✅ تأكيد الإجابة"):
            selected_key = selected_option.split(")")[0].strip()
            is_correct = selected_key == q["correct"]
            st.session_state.last_result = {
                "is_correct": is_correct,
                "correct_key": q["correct"],
                "explanation": q["explanation"]
            }
            record_answer(subject, is_correct, q["topic"], q["difficulty"])

    if st.session_state.last_result:
        result = st.session_state.last_result
        if result["is_correct"]:
            st.markdown("""
            <div class="result-success">
                ✅ إجابة صحيحة — ممتاز جدًا، استمر على هذا المستوى.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-error">
                ❌ إجابة غير صحيحة — الإجابة الصحيحة هي: {result['correct_key']}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### ✍️ الشرح خطوة بخطوة")
        st.markdown(result["explanation"])

elif page == "📺 أكاديمية الفيديو":
    st.markdown('<div class="section-title">أكاديمية الفيديو التعليمية</div>', unsafe_allow_html=True)

    for subject, info in SUBJECTS_DATA.items():
        with st.expander(f"{info['icon']} {subject}"):
            st.markdown(f"""
            <div class="glass-card">
                <div class="subject-name">{subject}</div>
                <div class="small-muted">
                    {info['description']}<br>
                    موضوعات بارزة: {", ".join(info['topics'])}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"فتح دروس {subject}", key=f"video_{subject}"):
                profile["stats"]["video_clicks"] += 1
                save_profile(profile)
                st.link_button(f"🎥 الذهاب إلى دروس {subject}", info["yt"])

elif page == "📈 التحليلات والأداء":
    st.markdown('<div class="section-title">التحليلات ومؤشرات الأداء</div>', unsafe_allow_html=True)

    total_questions = profile["stats"]["questions_answered"]
    correct_answers = profile["stats"]["correct_answers"]
    wrong_answers = max(total_questions - correct_answers, 0)
    accuracy = percent(correct_answers, total_questions)

    c1, c2, c3 = st.columns(3)
    with c1:
        render_metric_card("الإجابات الصحيحة", str(correct_answers), "إجمالي ما تم حله بشكل صحيح")
    with c2:
        render_metric_card("الإجابات الخاطئة", str(wrong_answers), "الأسئلة التي تحتاج مراجعة")
    with c3:
        render_metric_card("الدقة الكلية", f"{accuracy}%", performance_message())

    st.markdown("### 📊 تقدم المواد")
    progress_rows = []
    for subject in SUBJECTS_DATA.keys():
        progress_rows.append({
            "المادة": subject,
            "نسبة التقدم": profile["subject_progress"].get(subject, 0)
        })
    progress_df = pd.DataFrame(progress_rows)
    st.dataframe(progress_df, use_container_width=True, hide_index=True)

    st.markdown("### 🧾 سجل الأداء المختصر")
    df = chart_dataframe()
    if df.empty:
        st.info("لا توجد بيانات كافية بعد. ابدأ بحل بعض الأسئلة.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)

    if profile.get("exam_history"):
        st.markdown("### 🕒 آخر المحاولات")
        recent = pd.DataFrame(profile["exam_history"]).tail(10).iloc[::-1]
        recent = recent.rename(columns={
            "timestamp": "الوقت",
            "subject": "المادة",
            "topic": "الموضوع",
            "difficulty": "الصعوبة",
            "correct": "النتيجة"
        })
        recent["النتيجة"] = recent["النتيجة"].map({True: "صحيحة", False: "خاطئة"})
        st.dataframe(recent, use_container_width=True, hide_index=True)

elif page == "🗓️ الخطة اليومية":
    st.markdown('<div class="section-title">الخطة اليومية التنفيذية</div>', unsafe_allow_html=True)

    acc = percent(profile["stats"]["correct_answers"], profile["stats"]["questions_answered"])

    if acc >= 80:
        level_plan = "اليوم مناسب لاختبار متوسط إلى مرتفع الصعوبة مع مراجعة سريعة قبل النوم."
    elif acc >= 60:
        level_plan = "يُفضّل تقسيم اليوم بين مراجعة أساسيات + اختبار قصير + تصحيح الأخطاء."
    else:
        level_plan = "خطة إنقاذ: ابدأ بملخصات الدروس، ثم حل 5 أسئلة فقط لكل مادة صعبة."

    st.markdown(f"""
    <div class="glass-card">
        <div class="subject-name">📌 توصية اليوم</div>
        <div class="small-muted">{level_plan}</div>
    </div>
    """, unsafe_allow_html=True)

    tasks = [
        next_daily_task(),
        "حل اختبار قصير في المادة ذات أقل نسبة تقدم.",
        "فتح ملف PDF واحد ومراجعته لمدة 25 دقيقة.",
        "مشاهدة فيديو واحد فقط مع تدوين 5 ملاحظات.",
        "إعادة حل سؤال خاطئ سابقًا حتى تثبيت الفكرة."
    ]

    for i, task in enumerate(tasks, start=1):
        st.markdown(f"""
        <div class="glass-card">
            <span class="info-chip">المهمة {i}</span>
            <div class="small-muted">{task}</div>
        </div>
        """, unsafe_allow_html=True)

elif page == "⚙️ الإعدادات":
    st.markdown('<div class="section-title">الإعدادات الشخصية</div>', unsafe_allow_html=True)

    new_name = st.text_input("اسم الطالب", value=profile.get("student_name", "أدهم"))
    new_target = st.slider("الهدف النهائي (%)", 50, 100, int(profile.get("target_score", 95)))
    theme = st.selectbox("النمط البصري", ["إمبراطوري ليلي", "ذهبي رسمي", "أزرق ملكي"], index=0)

    if st.button("💾 حفظ الإعدادات"):
        profile["student_name"] = new_name.strip() or "أدهم"
        profile["target_score"] = new_target
        profile["theme_mode"] = theme
        profile["last_login"] = str(datetime.now())
        save_profile(profile)
        st.success("تم حفظ الإعدادات بنجاح.")

    st.markdown("### 🧹 أدوات النظام")
    if st.button("إعادة تعيين سجل الأداء"):
        current_name = profile.get("student_name", "أدهم")
        current_target = profile.get("target_score", 95)
        current_theme = profile.get("theme_mode", "إمبراطوري ليلي")

        profile = default_profile()
        profile["student_name"] = current_name
        profile["target_score"] = current_target
        profile["theme_mode"] = current_theme
        save_profile(profile)

        st.session_state.current_question = None
        st.session_state.last_result = None
        st.success("تم تصفير الأداء مع الإبقاء على الإعدادات الأساسية.")

# =========================================================
# Footer
# =========================================================
st.markdown("""
<div class="footer-note">
    تم تطوير هذه النسخة لتكون نواة منصة تعليمية عربية فائقة الفخامة وقابلة للتوسع إلى:
    حسابات متعددة، ذكاء اصطناعي، واجهات مدرس/ولي أمر، اختبارات شاملة، تقارير PDF، ولوحة إدارة مركزية.
</div>
""", unsafe_allow_html=True)
