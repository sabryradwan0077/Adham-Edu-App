# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import json
import math
import base64
import random
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List, Any, Optional

import pandas as pd
import streamlit as st

# =========================================================
# حصن أدهم التعليمي V100 - Ultra Imperial Fusion Edition
# دمج احترافي للكودين + تطوير شامل + تحسين الاستقرار والفخامة
# =========================================================

APP_TITLE = "حصن أدهم التعليمي"
APP_VERSION = "V100"
APP_ICON = "🏛️"

BASE_DIR = Path(".")
DATA_DIR = BASE_DIR / "hisn_adham_data"
DATA_FILE = DATA_DIR / "student_data.json"
SYLLABUS_DIR = BASE_DIR / "Syllabus"

DATA_DIR.mkdir(parents=True, exist_ok=True)
SYLLABUS_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title=f"{APP_TITLE} {APP_VERSION}",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS فخم جداً
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
            radial-gradient(circle at top left, rgba(59,130,246,0.12), transparent 22%),
            linear-gradient(180deg, #06101b 0%, #0a1522 45%, #0d1b2a 100%);
        color: #eef2ff;
    }

    .main > div {
        padding-top: 1.2rem;
    }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #08111b 0%, #101826 100%);
        border-left: 1px solid rgba(255,255,255,0.06);
    }

    .hero-box {
        background: linear-gradient(135deg, rgba(12,19,32,0.98), rgba(24,34,52,0.95));
        border: 1px solid rgba(255,215,0,0.18);
        border-radius: 30px;
        padding: 30px;
        margin-bottom: 22px;
        box-shadow: 0 24px 60px rgba(0,0,0,0.38);
        position: relative;
        overflow: hidden;
    }

    .hero-box:before {
        content: "";
        position: absolute;
        top: -60px;
        left: -60px;
        width: 160px;
        height: 160px;
        background: radial-gradient(circle, rgba(255,215,0,0.22), transparent 70%);
        border-radius: 50%;
    }

    .hero-box:after {
        content: "";
        position: absolute;
        bottom: -70px;
        right: -70px;
        width: 180px;
        height: 180px;
        background: radial-gradient(circle, rgba(59,130,246,0.20), transparent 70%);
        border-radius: 50%;
    }

    .hero-title {
        text-align: center;
        color: #ffd700;
        font-size: 2.2rem;
        font-weight: 900;
        margin-bottom: 8px;
        position: relative;
        z-index: 2;
    }

    .hero-sub {
        text-align: center;
        color: #dbeafe;
        font-size: 1rem;
        line-height: 2;
        position: relative;
        z-index: 2;
    }

    .section-title {
        color: #ffe082;
        font-size: 1.28rem;
        font-weight: 900;
        border-right: 5px solid #ffd700;
        padding-right: 12px;
        margin: 16px 0 14px 0;
    }

    .glass-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.045), rgba(255,255,255,0.025));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.18);
    }

    .metric-card {
        background: linear-gradient(135deg, rgba(255,215,0,0.08), rgba(255,255,255,0.03));
        border: 1px solid rgba(255,215,0,0.16);
        border-radius: 22px;
        padding: 18px;
        min-height: 130px;
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
        font-size: 1.95rem;
        margin-bottom: 6px;
    }

    .metric-note {
        color: #93c5fd;
        font-size: 0.9rem;
        font-weight: 600;
        line-height: 1.7;
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
        line-height: 1.9;
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
        line-height: 1.9;
        font-size: 0.94rem;
    }

    .file-card {
        background: linear-gradient(135deg, rgba(30,41,59,0.90), rgba(15,23,42,0.90));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 16px;
        margin-bottom: 10px;
    }

    .footer-note {
        text-align: center;
        color: #cbd5e1;
        margin-top: 32px;
        font-size: 0.9rem;
        opacity: 0.92;
    }

    .stButton > button,
    .stDownloadButton > button {
        width: 100%;
        min-height: 46px;
        border-radius: 14px !important;
        font-weight: 800 !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #facc15, #ffd700) !important;
        color: #111827 !important;
        border: 1px solid rgba(255,215,0,0.28) !important;
        box-shadow: 0 8px 20px rgba(250,204,21,0.22);
    }

    iframe {
        border-radius: 20px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        background: white !important;
    }

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #facc15, #38bdf8) !important;
    }
    </style>
    """, unsafe_allow_html=True)

inject_global_css()

# =========================================================
# استدعاء بنك الأسئلة الخارجي إن وجد
# =========================================================
try:
    from questions_bank import ST_QUESTIONS as EXTERNAL_QUESTION_BANK
except Exception:
    EXTERNAL_QUESTION_BANK = {}

# =========================================================
# البيانات الأساسية
# =========================================================
SUBJECTS: Dict[str, Dict[str, Any]] = {
    "الفيزياء": {
        "icon": "⚡",
        "description": "قانون أوم - قوانين كيرشوف - القدرة - الشغل والطاقة - الموجات",
        "difficulty": "مرتفع",
        "topics": ["قانون أوم", "قوانين كيرشوف", "القدرة", "الشغل والطاقة", "الموجات"],
        "youtube": "https://www.youtube.com/results?search_query=فيزياء+ثانوية+عامة+شرح"
    },
    "الكيمياء": {
        "icon": "🧪",
        "description": "الاتزان الكيميائي - العضوية - خامات الحديد - الأحماض والقواعد",
        "difficulty": "متوسط",
        "topics": ["خام الحديد", "الاتزان", "الأحماض والقواعد", "العضوية"],
        "youtube": "https://www.youtube.com/results?search_query=كيمياء+ثانوية+عامة+شرح"
    },
    "الرياضيات البحتة": {
        "icon": "📐",
        "description": "التفاضل - التكامل - الجبر - الهندسة التحليلية",
        "difficulty": "مرتفع",
        "topics": ["التكامل", "النهايات", "الجبر", "الهندسة التحليلية"],
        "youtube": "https://www.youtube.com/results?search_query=رياضيات+بحتة+ثانوية+عامة+شرح"
    },
    "الرياضيات التطبيقية": {
        "icon": "⚙️",
        "description": "الاستاتيكا - الديناميكا - العزوم - الاحتكاك",
        "difficulty": "مرتفع",
        "topics": ["العزوم", "الاحتكاك", "الاتزان", "الحركة"],
        "youtube": "https://www.youtube.com/results?search_query=رياضيات+تطبيقية+ثانوية+عامة+شرح"
    },
    "اللغة العربية": {
        "icon": "📚",
        "description": "النحو - البلاغة - الأدب - النصوص - القراءة",
        "difficulty": "متوسط",
        "topics": ["النحو", "البلاغة", "الأدب", "النصوص", "القراءة"],
        "youtube": "https://www.youtube.com/results?search_query=لغة+عربية+ثانوية+عامة+شرح"
    }
}

INTERNAL_QUESTION_BANK: Dict[str, List[Dict[str, Any]]] = {
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
            "answer": "A",
            "explanation": """قانون المقاومة:
R = ρL / A

إذا أصبح:
L = 2L
A = A/2

فإن:
R الجديدة = ρ(2L) / (A/2) = 4ρL/A

إذن المقاومة تزداد إلى أربعة أمثالها.""",
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
            "answer": "B",
            "explanation": """طبقًا لقانون كيرشوف الثاني:
المجموع الجبري لفروق الجهد في أي مسار مغلق = صفر.""",
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
            "answer": "C",
            "explanation": """نستخدم العلاقة:
P = V × I

إذن:
I = P / V = 220 / 110 = 2 أمبير""",
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
            "answer": "A",
            "explanation": "عملية التركيز تهدف إلى رفع نسبة المادة المفيدة في الخام بإزالة الشوائب.",
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
            "answer": "B",
            "explanation": "العامل الحفاز يقلل طاقة التنشيط فيزيد سرعة التفاعل دون تغيير ثابت الاتزان.",
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
            "answer": "B",
            "explanation": """عندما يكون التكامل حاصل ضرب دالتين، إحداهما جبرية والأخرى أسية،
فالطريقة الأنسب غالبًا هي التكامل بالتجزئة.""",
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
            "answer": "B",
            "explanation": "من النهايات المشهورة: lim (sin x / x) = 1 عندما x → 0",
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
            "answer": "B",
            "explanation": "العزم = القوة × ذراعها العمودي، وهو مقياس لقدرة القوة على إحداث دوران.",
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
            "answer": "A",
            "explanation": "العلم نور: تشبيه بليغ لأن أداة التشبيه ووجه الشبه محذوفان.",
            "topic": "البلاغة",
            "difficulty": "متوسط"
        }
    ]
}

DAILY_TASKS = [
    "حل 15 سؤالًا في المادة الأضعف لديك.",
    "مراجعة قانونين أو قاعدتين وكتابتهما بخط اليد.",
    "مراجعة ملف PDF واحد لمدة 25 دقيقة.",
    "مشاهدة شرح مركز لمدة 30 دقيقة ثم تلخيصه.",
    "إعادة حل سؤالين أخطأت فيهما سابقًا.",
    "اختبار سريع من 5 أسئلة لتثبيت الفهم."
]

# =========================================================
# أدوات توحيد بنك الأسئلة
# =========================================================
def normalize_question_item(item: Dict[str, Any], fallback_subject: str = "") -> Optional[Dict[str, Any]]:
    if not isinstance(item, dict):
        return None

    question_text = item.get("question", "").strip()
    if not question_text:
        return None

    raw_options = item.get("options", [])
    normalized_options: Dict[str, str] = {}

    if isinstance(raw_options, dict):
        for key in ["A", "B", "C", "D"]:
            if key in raw_options:
                normalized_options[key] = str(raw_options[key]).strip()
    elif isinstance(raw_options, list):
        letters = ["A", "B", "C", "D"]
        for idx, option in enumerate(raw_options[:4]):
            normalized_options[letters[idx]] = str(option).strip()

    if len(normalized_options) < 2:
        return None

    correct = str(item.get("correct", item.get("answer", ""))).strip()
    if correct in normalized_options:
        correct_key = correct
    else:
        correct_key = ""
        for key, val in normalized_options.items():
            if str(val).strip() == str(item.get("answer", "")).strip():
                correct_key = key
                break
        if not correct_key:
            correct_key = list(normalized_options.keys())[0]

    explanation = str(item.get("explanation", "لا يوجد شرح متاح حالياً.")).strip()
    topic = str(item.get("topic", fallback_subject or "عام")).strip()
    difficulty = str(item.get("difficulty", "متوسط")).strip()

    return {
        "question": question_text,
        "options": normalized_options,
        "correct": correct_key,
        "answer": correct_key,
        "explanation": explanation,
        "topic": topic,
        "difficulty": difficulty
    }

def merge_question_banks() -> Dict[str, List[Dict[str, Any]]]:
    merged: Dict[str, List[Dict[str, Any]]] = {}

    all_subjects = set(INTERNAL_QUESTION_BANK.keys()) | set(EXTERNAL_QUESTION_BANK.keys()) | set(SUBJECTS.keys())

    for subject in all_subjects:
        collected: List[Dict[str, Any]] = []
        seen = set()

        for source_bank in [INTERNAL_QUESTION_BANK, EXTERNAL_QUESTION_BANK]:
            for item in source_bank.get(subject, []):
                normalized = normalize_question_item(item, fallback_subject=subject)
                if normalized:
                    sig = (
                        normalized["question"].strip(),
                        tuple(normalized["options"].items()),
                        normalized["correct"]
                    )
                    if sig not in seen:
                        seen.add(sig)
                        collected.append(normalized)

        if collected:
            merged[subject] = collected

    return merged

QUESTION_BANK = merge_question_banks()

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
        "favorites": [],
        "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def load_data() -> Dict[str, Any]:
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            template = default_student_data()
            template.update(loaded)
            template["stats"].update(loaded.get("stats", {}))
            template["subject_progress"].update(loaded.get("subject_progress", {}))
            return template
        except Exception:
            return default_student_data()
    return default_student_data()

def save_data(data: Dict[str, Any]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

# =========================================================
# Session State
# =========================================================
SESSION_DEFAULTS = {
    "current_question": None,
    "question_result": None,
    "exam_questions": [],
    "exam_answers": {},
    "exam_submitted": False,
    "last_subject_selected": None
}

for key, value in SESSION_DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# أدوات مساعدة
# =========================================================
def calc_percent(part: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round((part / total) * 100, 1)

def get_accuracy() -> float:
    return calc_percent(
        data["stats"].get("correct_answers", 0),
        data["stats"].get("questions_answered", 0)
    )

def get_status_label() -> str:
    answered = data["stats"].get("questions_answered", 0)
    acc = get_accuracy()
    if answered == 0:
        return "بداية قوية"
    if acc >= 90:
        return "نخبة القمة"
    if acc >= 80:
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

def render_pdf(file_path: Path, height: int = 950) -> None:
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
    return sorted([p for p in SYLLABUS_DIR.glob("*.pdf") if p.is_file()], key=lambda x: x.name.lower())

def generate_random_question(subject: str) -> Optional[Dict[str, Any]]:
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

    total = data["stats"]["questions_answered"]
    correct_count = data["stats"]["correct_answers"]

    if total >= 10:
        award_achievement("🏅 أول 10 إجابات")
    if correct_count >= 25:
        award_achievement("👑 25 إجابة صحيحة")
    if get_accuracy() >= 85 and total >= 10:
        award_achievement("🔥 دقة أعلى من 85%")
    if total >= 50:
        award_achievement("🚀 محارب الأسئلة - 50 سؤالاً")

    save_data(data)

def create_mock_exam(subject: str, num_questions: int = 5) -> List[Dict[str, Any]]:
    bank = QUESTION_BANK.get(subject, [])
    if not bank:
        return []
    if len(bank) >= num_questions:
        return random.sample(bank, num_questions)
    return [random.choice(bank) for _ in range(num_questions)]

def today_task() -> str:
    return DAILY_TASKS[date.today().day % len(DAILY_TASKS)]

def performance_message() -> str:
    answered = data["stats"].get("questions_answered", 0)
    acc = get_accuracy()
    if answered == 0:
        return "ابدأ أول اختبار الآن لتظهر مؤشرات الأداء الذكية."
    if acc >= 85:
        return "أداءك ممتاز جدًا، استمر بنفس النسق."
    if acc >= 70:
        return "مستواك قوي، لكن ما زال هناك هامش للتطوير."
    if acc >= 50:
        return "أنت على الطريق الصحيح لكن تحتاج تقليل الأخطاء."
    return "ابدأ بالمراجعة الأساسية ثم عد للاختبار."

def get_weakest_subject() -> str:
    progress = data.get("subject_progress", {})
    if not progress:
        return "غير محدد"
    return min(progress, key=progress.get)

def get_best_subject() -> str:
    progress = data.get("subject_progress", {})
    if not progress:
        return "غير محدد"
    return max(progress, key=progress.get)

def add_favorite_file(file_name: str) -> None:
    if file_name not in data["favorites"]:
        data["favorites"].append(file_name)
        save_data(data)

def format_size_kb(path: Path) -> str:
    return f"{round(path.stat().st_size / 1024, 2)} كيلوبايت"

# =========================================================
# Header
# =========================================================
st.markdown(f"""
<div class="hero-box">
    <div class="hero-title">🏛️ {APP_TITLE} — {APP_VERSION}</div>
    <div class="hero-sub">
        منصة تعليمية عربية احترافية فائقة الفخامة للثانوية العامة:
        مكتبة PDF ذكية، بنك أسئلة تفاعلي، اختبارات تجريبية، تحليلات أداء، خطة يومية، وتتبع تقدّم كامل
        في واجهة إمبراطورية راقية تجمع بين قوة الكودين في نسخة واحدة متكاملة.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# Sidebar
# =========================================================
with st.sidebar:
    st.markdown("## 🎛️ لوحة التحكم الإمبراطورية")

    page = st.radio(
        "اختر القسم:",
        [
            "🏠 الرئيسية",
            "📚 المكتبة الرقمية",
            "🧠 بنك الأسئلة التفاعلي",
            "📝 الاختبار التجريبي",
            "📺 أكاديمية الفيديو",
            "📈 التحليلات",
            "🎯 الخطة اليومية",
            "⚙️ الإعدادات"
        ]
    )

    st.markdown("---")
    st.markdown(f"**الطالب:** {data.get('student_name', 'أدهم')}")
    st.markdown(f"**الحالة:** {get_status_label()}")
    st.markdown(f"**الهدف:** {data.get('target_score', 95)}%")
    st.markdown(f"**أضعف مادة:** {get_weakest_subject()}")
    st.markdown("---")
    st.info("💡 نصيحة القمة: لا تكتفِ بقراءة الدرس، بل اختبر نفسك فيه فورًا.")
    st.caption("ضع ملفات PDF داخل مجلد Syllabus لتظهر تلقائيًا داخل المكتبة.")

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

    subjects_to_show = list(SUBJECTS.items())
    for i, (subject, info) in enumerate(subjects_to_show):
        with [col1, col2][i % 2]:
            progress = data["subject_progress"].get(subject, 0)
            question_count = len(QUESTION_BANK.get(subject, []))
            st.markdown(f"""
            <div class="subject-card">
                <div class="subject-title">{info['icon']} {subject}</div>
                <div class="subject-meta">
                    الوصف: {info['description']}<br>
                    مستوى الصعوبة: {info['difficulty']}<br>
                    عدد الأسئلة المتاحة: {question_count}<br>
                    التقدم الحالي: {progress}%
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(progress / 100)

    st.markdown('<div class="section-title">مهمة اليوم</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="glass-card">
        <span class="info-chip">الخطة اليومية</span>
        <span class="info-chip">أفضل مادة لديك: {get_best_subject()}</span>
        <span class="info-chip">المادة التي تحتاج دعمًا: {get_weakest_subject()}</span>
        <div class="small-note">{today_task()}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">الإنجازات</div>', unsafe_allow_html=True)
    if data["achievements"]:
        cols = st.columns(2)
        for i, ach in enumerate(data["achievements"]):
            with cols[i % 2]:
                st.markdown(f"<div class='glass-card'>{ach}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-card'>ابدأ الحل الآن لفتح أول إنجاز لك.</div>", unsafe_allow_html=True)

    if data.get("favorites"):
        st.markdown('<div class="section-title">الملفات المفضلة</div>', unsafe_allow_html=True)
        for fav in data["favorites"][-5:][::-1]:
            st.markdown(f"<div class='glass-card'>⭐ {fav}</div>", unsafe_allow_html=True)

# =========================================================
# المكتبة الرقمية
# =========================================================
elif page == "📚 المكتبة الرقمية":
    st.markdown('<div class="section-title">المكتبة الرقمية للكتب والمذكرات والملخصات</div>', unsafe_allow_html=True)

    pdf_files = list_pdf_files()

    if not pdf_files:
        st.warning("لا توجد ملفات PDF داخل مجلد Syllabus حالياً.")
        st.info("أنشئ مجلدًا باسم Syllabus وضع بداخله الكتب أو الملخصات أو المراجعات النهائية.")
    else:
        search_term = st.text_input("🔎 ابحث عن ملف", placeholder="اكتب اسم الكتاب أو جزءًا منه")
        filtered = [
            p for p in pdf_files
            if search_term.strip().lower() in p.name.lower()
        ] if search_term.strip() else pdf_files

        if not filtered:
            st.error("لا توجد نتائج مطابقة لبحثك.")
        else:
            file_names = [p.name for p in filtered]
            selected_name = st.selectbox("اختر الملف:", file_names)
            selected_path = next(p for p in filtered if p.name == selected_name)

            left, right = st.columns([1.2, 1])
            with left:
                st.markdown(f"""
                <div class="file-card">
                    <div class="subject-title">📘 {selected_path.name}</div>
                    <div class="small-note">
                        الحجم: {format_size_kb(selected_path)}<br>
                        المسار: {selected_path.parent}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with right:
                with open(selected_path, "rb") as f:
                    file_bytes = f.read()

                st.download_button(
                    "📥 تحميل الملف",
                    data=file_bytes,
                    file_name=selected_path.name,
                    mime="application/pdf"
                )

                c1, c2 = st.columns(2)
                with c1:
                    if st.button("📖 تسجيل فتح الملف"):
                        data["stats"]["pdf_opened"] += 1
                        save_data(data)
                        st.success("تم تسجيل فتح الملف.")
                with c2:
                    if st.button("⭐ إضافة للمفضلة"):
                        add_favorite_file(selected_path.name)
                        st.success("تمت الإضافة إلى المفضلة.")

            st.markdown("### 👁️ عرض الملف")
            render_pdf(selected_path, height=980)

            st.markdown("### 📚 جميع الملفات المتاحة")
            for p in filtered:
                st.markdown(f"""
                <div class="glass-card">
                    <span class="info-chip">PDF</span>
                    <span class="info-chip">{format_size_kb(p)}</span>
                    <div class="small-note">{p.name}</div>
                </div>
                """, unsafe_allow_html=True)

# =========================================================
# بنك الأسئلة التفاعلي
# =========================================================
elif page == "🧠 بنك الأسئلة التفاعلي":
    st.markdown('<div class="section-title">بنك الأسئلة التفاعلي الذكي</div>', unsafe_allow_html=True)

    available_subjects = [s for s in SUBJECTS.keys() if QUESTION_BANK.get(s)]
    if not available_subjects:
        st.error("لا يوجد بنك أسئلة متاح حالياً. يمكنك إضافة ملف questions_bank.py أو الاعتماد على البنك الداخلي.")
    else:
        subject = st.selectbox("اختر المادة:", available_subjects)
        info = SUBJECTS.get(subject, {"difficulty": "متوسط", "topics": []})

        st.markdown(f"""
        <div class="glass-card">
            <span class="info-chip">المادة: {subject}</span>
            <span class="info-chip">الصعوبة العامة: {info['difficulty']}</span>
            <span class="info-chip">عدد الأسئلة: {len(QUESTION_BANK.get(subject, []))}</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🎯 توليد سؤال جديد"):
            st.session_state.current_question = generate_random_question(subject)
            st.session_state.question_result = None

        q = st.session_state.current_question

        if q:
            st.markdown(f"""
            <div class="glass-card">
                <div class="subject-title">❓ السؤال</div>
                <div class="small-note" style="font-size:1rem;color:#f8fafc;">{q['question']}</div>
                <div class="small-note" style="margin-top:10px;">
                    الموضوع: {q['topic']} | المستوى: {q['difficulty']}
                </div>
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
                    "correct_text": q["options"].get(q["correct"], ""),
                    "explanation": q["explanation"]
                }

                update_after_answer(subject, is_correct, q["topic"], q["difficulty"])

        if st.session_state.question_result:
            res = st.session_state.question_result
            if res["correct"]:
                st.markdown("<div class='success-box'>✅ إجابة صحيحة — أداء ممتاز جدًا.</div>", unsafe_allow_html=True)
            else:
                st.markdown(
                    f"<div class='error-box'>❌ إجابة غير صحيحة — الإجابة الصحيحة هي: {res['correct_key']}) {res['correct_text']}</div>",
                    unsafe_allow_html=True
                )

            st.markdown("### ✍️ شرح الإجابة")
            st.markdown(res["explanation"])

# =========================================================
# الاختبار التجريبي
# =========================================================
elif page == "📝 الاختبار التجريبي":
    st.markdown('<div class="section-title">الاختبار التجريبي المصغر</div>', unsafe_allow_html=True)

    available_subjects = [s for s in SUBJECTS.keys() if QUESTION_BANK.get(s)]
    if not available_subjects:
        st.error("لا توجد أسئلة كافية لإنشاء اختبار تجريبي.")
    else:
        subject = st.selectbox("اختر مادة الاختبار:", available_subjects, key="exam_subject")
        max_q = max(3, min(10, len(QUESTION_BANK.get(subject, [])))) if QUESTION_BANK.get(subject) else 3
        q_count = st.slider("عدد الأسئلة", min_value=3, max_value=max_q, value=min(5, max_q))

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
                            f"<div class='error-box'>السؤال {idx}: إجابة خاطئة ❌ | الصحيحة: {q['correct']}) {q['options'][q['correct']]}</div>",
                            unsafe_allow_html=True
                        )

                    st.markdown(f"**الشرح المختصر للسؤال {idx}:**")
                    st.markdown(q["explanation"])

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
                        النسبة: {score_percent}%<br>
                        التقييم: {"ممتاز" if score_percent >= 85 else "جيد جدًا" if score_percent >= 70 else "يحتاج مراجعة"}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# =========================================================
# أكاديمية الفيديو
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
                    الموضوعات الرئيسية: {", ".join(info['topics'])}
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
        metric_card("الإجابات الخاطئة", str(wrong_q), "مجموع الأخطاء المسجلة")
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
        history_df["الوضع"] = history_df["الوضع"].map({
            "single_question": "سؤال فردي",
            "mock_exam": "اختبار تجريبي"
        }).fillna(history_df["الوضع"])

        st.markdown("### 🕒 سجل النشاط")
        st.dataframe(history_df.iloc[::-1], use_container_width=True, hide_index=True)

        grouped = (
            pd.DataFrame(data["history"])
            .groupby("subject")["correct"]
            .agg(["count", "sum"])
            .reset_index()
        )
        grouped["accuracy"] = grouped.apply(
            lambda row: calc_percent(int(row["sum"]), int(row["count"])),
            axis=1
        )
        grouped.columns = ["المادة", "إجمالي الإجابات", "الإجابات الصحيحة", "نسبة الدقة"]
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
    weakest = get_weakest_subject()

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
        f"ابدأ بالمادة الأضعف لديك: {weakest}.",
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
    col1, col2 = st.columns(2)

    with col1:
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

    with col2:
        if st.button("مسح المفضلة فقط"):
            data["favorites"] = []
            save_data(data)
            st.success("تم مسح المفضلة بنجاح.")

    st.markdown("### ℹ️ معلومات تقنية")
    st.markdown(f"""
    <div class="glass-card">
        <div class="small-note">
            اسم التطبيق: {APP_TITLE}<br>
            الإصدار: {APP_VERSION}<br>
            مجلد الكتب: {SYLLABUS_DIR}<br>
            ملف البيانات: {DATA_FILE}<br>
            عدد المواد: {len(SUBJECTS)}<br>
            عدد الأسئلة الكلي: {sum(len(v) for v in QUESTION_BANK.values())}
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# Footer
# =========================================================
st.markdown("""
<div class="footer-note">
    حصن أدهم التعليمي — إصدار فائق التطوير قابل للتوسع إلى:
    حسابات متعددة، ولي أمر، مدرس، تقارير PDF، ذكاء اصطناعي، بنك أسئلة ضخم، ولوحات متابعة أكثر قوة.
</div>
""", unsafe_allow_html=True)
