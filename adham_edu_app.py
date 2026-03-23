# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import random
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

import pandas as pd
import streamlit as st

# =========================================================
# حصن أدهم التعليمي V102 - Final Imperial Edition
# =========================================================

APP_TITLE = "حصن أدهم التعليمي"
APP_VERSION = "V102"
APP_ICON = "🏛️"

st.set_page_config(
    page_title=f"{APP_TITLE} {APP_VERSION}",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# إعدادات المسارات الآمنة
# =========================================================
BASE_DIR = Path(".")


def ensure_directory(path: Path) -> Path:
    if path.exists():
        if path.is_dir():
            return path
        st.error(f"يوجد عنصر باسم {path.name} لكنه ملف وليس مجلدًا. احذف الملف أو غيّر اسمه.")
        st.stop()
    path.mkdir(parents=True, exist_ok=True)
    return path


DATA_DIR = ensure_directory(BASE_DIR / "hisn_adham_data")
DATA_FILE = DATA_DIR / "student_data.json"

# =========================================================
# CSS إمبراطوري فخم + إبراز الاختيارات
# =========================================================
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
    padding-top: 1rem;
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

.drive-card {
    background: linear-gradient(135deg, rgba(30,41,59,0.90), rgba(15,23,42,0.90));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 14px;
}

.option-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 14px;
}

.option-legend-card {
    display: flex;
    align-items: center;
    gap: 12px;
    background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,215,0,0.04));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 14px;
    min-height: 80px;
    box-shadow: 0 8px 18px rgba(0,0,0,0.18);
}

.option-badge {
    min-width: 54px;
    width: 54px;
    height: 54px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 16px;
    background: linear-gradient(135deg, #ffd700, #facc15);
    color: #111827;
    font-size: 1.25rem;
    font-weight: 900;
    box-shadow: 0 10px 22px rgba(250,204,21,0.28);
    border: 1px solid rgba(255,215,0,0.35);
}

.option-text {
    color: #f8fafc;
    font-weight: 700;
    line-height: 1.8;
    font-size: 0.98rem;
}

div[data-testid="stRadio"] > div {
    gap: 0.55rem !important;
}

div[data-testid="stRadio"] label {
    background: linear-gradient(135deg, rgba(255,255,255,0.055), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.11);
    border-radius: 18px;
    padding: 14px 16px !important;
    margin-bottom: 8px;
    width: 100%;
    transition: all 0.2s ease;
}

div[data-testid="stRadio"] label:hover {
    border: 1px solid rgba(255,215,0,0.35);
    box-shadow: 0 8px 18px rgba(0,0,0,0.22);
}

div[data-testid="stRadio"] label p {
    color: #f8fafc !important;
    font-size: 1rem !important;
    font-weight: 800 !important;
    line-height: 1.9 !important;
}

.stButton > button,
.stDownloadButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 14px !important;
    font-weight: 800 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #facc15, #ffd700) !important;
    color: #111827 !important;
    border: 1px solid rgba(255,215,0,0.28) !important;
    box-shadow: 0 8px 20px rgba(250,204,21,0.22);
}

.stLinkButton a {
    width: 100%;
    display: inline-flex !important;
    justify-content: center !important;
    align-items: center !important;
    min-height: 48px !important;
    border-radius: 14px !important;
    font-weight: 800 !important;
    text-decoration: none !important;
    background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #facc15, #38bdf8) !important;
}

.footer-note {
    text-align: center;
    color: #cbd5e1;
    margin-top: 32px;
    font-size: 0.9rem;
    opacity: 0.92;
}

@media (max-width: 768px) {
    .option-grid {
        grid-template-columns: 1fr;
    }

    .hero-title {
        font-size: 1.7rem;
    }

    .metric-value {
        font-size: 1.6rem;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# روابط Google Drive
# =========================================================
DRIVE_LINKS = {
    "الرياضيات التطبيقية (1)": "https://drive.google.com/file/d/1xlzPmrUqCAR7XF4ZaBAFN6WhbvZum3_d/view",
    "الرياضيات التطبيقية (2)": "https://drive.google.com/file/d/1BQec3wMImmlX-Y82Ll8ppgMFr6N3aQuP/view",
    "الرياضيات البحتة (1)": "https://drive.google.com/file/d/1TqlGSQ7__r2er05lfqAi1B2kdIrspXui/view",
    "الرياضيات البحتة (2)": "https://drive.google.com/file/d/1Om2_yLrF1btqqr73JOdpAVewL47-BuW8/view",
    "الفيزياء (1)": "https://drive.google.com/file/d/1uo6ZDwqV0CeN9MatZRfk79N07crJ3Gxw/view",
    "الفيزياء (2)": "https://drive.google.com/file/d/1Vn6PQyoyEgvLGf7QB-l75tg_phNIQNDq/view",
    "الكيمياء (1)": "https://drive.google.com/file/d/1QjUZknxo9rp8GeeaB4S1OyzAHtDcbsfu/view",
    "الكيمياء (2)": "https://drive.google.com/file/d/1LSmHETcXeYwA6qz-eyFX6ItZ6pXgvJ2m/view",
    "اللغة العربية (1)": "https://drive.google.com/file/d/1IaVZdUUCtgE4cZ0jxOJ98tk9qdWZSlVV/view",
    "اللغة العربية (2)": "https://drive.google.com/file/d/1WGrU1z6JWk_i22VRpP6OgeEiTrevw-bR/view",
    "اللغة الإنجليزية (1)": "https://drive.google.com/file/d/1BOzbTTX9mtQY-tNI_u_qibQu9et6byAS/view",
    "اللغة الإنجليزية (2)": "https://drive.google.com/file/d/1_K--sjkXTb_j3bWTn0fW2X8Il0UVvLAK/view",
    "بنك الأسئلة الشامل": "https://drive.google.com/file/d/1Xp2lVzOcPXLh-BqRX9A6Xeku22KYwCVP/view"
}

# =========================================================
# المواد
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
    },
    "اللغة الإنجليزية": {
        "icon": "🌍",
        "description": "Grammar - Reading - Vocabulary - Writing",
        "difficulty": "متوسط",
        "topics": ["Grammar", "Reading", "Vocabulary", "Writing"],
        "youtube": "https://www.youtube.com/results?search_query=لغة+انجليزية+ثانوية+عامة+شرح"
    }
}

# =========================================================
# بنك أسئلة داخلي احتياطي
# =========================================================
INTERNAL_QUESTION_BANK: Dict[str, List[Dict[str, Any]]] = {
    "الفيزياء": [
        {
            "question": "إذا زاد طول سلك معدني إلى الضعف وقلت مساحة مقطعه إلى النصف، فإن مقاومته:",
            "options": {"A": "تزداد إلى أربعة أمثالها", "B": "تزداد إلى الضعف", "C": "تقل إلى النصف", "D": "تظل ثابتة"},
            "correct": "A",
            "explanation": "R = ρL / A، فإذا تضاعف الطول ونُصفت المساحة زادت المقاومة إلى أربعة أمثالها.",
            "topic": "قانون أوم",
            "difficulty": "متوسط"
        },
        {
            "question": "مجموع فروق الجهد حول أي مسار مغلق يساوي:",
            "options": {"A": "شدة التيار", "B": "صفر", "C": "المقاومة المكافئة", "D": "القدرة"},
            "correct": "B",
            "explanation": "طبقًا لقانون كيرشوف الثاني، المجموع الجبري لفروق الجهد في مسار مغلق يساوي صفرًا.",
            "topic": "قوانين كيرشوف",
            "difficulty": "سهل"
        }
    ],
    "الكيمياء": [
        {
            "question": "العامل الحفاز يقوم بـ:",
            "options": {"A": "زيادة كمية النواتج", "B": "تقليل طاقة التنشيط", "C": "تغيير ثابت الاتزان", "D": "إيقاف التفاعل"},
            "correct": "B",
            "explanation": "العامل الحفاز يقلل طاقة التنشيط فيزيد سرعة التفاعل دون تغيير ثابت الاتزان.",
            "topic": "سرعة التفاعل",
            "difficulty": "سهل"
        }
    ],
    "الرياضيات البحتة": [
        {
            "question": "أنسب طريقة لحساب التكامل ∫ x e^x dx هي:",
            "options": {"A": "التعويض", "B": "التكامل بالتجزئة", "C": "الكسور الجزئية", "D": "الطريقة البيانية"},
            "correct": "B",
            "explanation": "عندما يكون التكامل حاصل ضرب دالة جبرية وأخرى أسية فالأنسب غالبًا التكامل بالتجزئة.",
            "topic": "التكامل",
            "difficulty": "متوسط"
        }
    ],
    "الرياضيات التطبيقية": [
        {
            "question": "العزم حول نقطة يساوي:",
            "options": {"A": "القوة ÷ الذراع", "B": "القوة × ذراعها العمودي", "C": "الكتلة × السرعة", "D": "الضغط × المساحة"},
            "correct": "B",
            "explanation": "العزم = القوة × ذراعها العمودي.",
            "topic": "العزوم",
            "difficulty": "سهل"
        }
    ],
    "اللغة العربية": [
        {
            "question": "في قولنا: العلم نور، الأسلوب البلاغي هو:",
            "options": {"A": "تشبيه بليغ", "B": "استعارة مكنية", "C": "كناية", "D": "مجاز مرسل"},
            "correct": "A",
            "explanation": "تشبيه بليغ لأن أداة التشبيه ووجه الشبه محذوفان.",
            "topic": "البلاغة",
            "difficulty": "متوسط"
        }
    ],
    "اللغة الإنجليزية": [
        {
            "question": "Choose the correct sentence:",
            "options": {"A": "He go to school", "B": "He goes to school", "C": "He going to school", "D": "He gone to school"},
            "correct": "B",
            "explanation": "With he/she/it in the present simple, the verb usually takes s/es.",
            "topic": "Grammar",
            "difficulty": "سهل"
        }
    ]
}

# =========================================================
# بنك خارجي اختياري
# =========================================================
try:
    from questions_bank import ST_QUESTIONS as EXTERNAL_QUESTION_BANK
except Exception:
    EXTERNAL_QUESTION_BANK = {}

# =========================================================
# توليد أسئلة ديناميكية عند الحاجة
# =========================================================
def generate_dynamic_questions(subject: str, count: int = 20) -> List[Dict[str, Any]]:
    topic_map = {
        "الفيزياء": ["قانون أوم", "كيرشوف", "الحث المغناطيسي", "الفيزياء الحديثة"],
        "الكيمياء": ["العناصر الانتقالية", "التحليل الكيميائي", "الكيمياء العضوية", "الاتزان الكيميائي"],
        "الرياضيات البحتة": ["التفاضل", "التكامل", "النهايات", "الجبر"],
        "الرياضيات التطبيقية": ["الاستاتيكا", "الديناميكا", "العزوم", "الاحتكاك"],
        "اللغة العربية": ["النحو", "البلاغة", "الأدب", "النصوص"],
        "اللغة الإنجليزية": ["Grammar", "Reading", "Vocabulary", "Writing"]
    }

    topics = topic_map.get(subject, ["عام"])
    generated = []

    for i in range(1, count + 1):
        topic = random.choice(topics)
        generated.append({
            "question": f"سؤال تدريبي متقدم في {topic}: ما النتيجة الأقرب للصواب في الحالة التطبيقية رقم {i}؟",
            "options": {
                "A": "تزداد للضعف",
                "B": "تقل للنصف",
                "C": "تظل ثابتة",
                "D": "يعتمد ذلك على المعطيات"
            },
            "correct": "D" if i % 4 == 0 else "A",
            "explanation": f"الشرح الإرشادي: راجع موضوع {topic} وحدد أثر تغيّر المعطيات على النتيجة النهائية.",
            "topic": topic,
            "difficulty": "متوسط"
        })
    return generated

# =========================================================
# توحيد صيغة الأسئلة
# =========================================================
def normalize_question_item(item: Dict[str, Any], fallback_subject: str = "") -> Optional[Dict[str, Any]]:
    if not isinstance(item, dict):
        return None

    question_text = str(item.get("question", "")).strip()
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
    if correct not in normalized_options:
        correct = "A"

    return {
        "question": question_text,
        "options": normalized_options,
        "correct": correct,
        "explanation": str(item.get("explanation", item.get("hint", "لا يوجد شرح متاح حالياً."))).strip(),
        "topic": str(item.get("topic", fallback_subject or "عام")).strip(),
        "difficulty": str(item.get("difficulty", "متوسط")).strip()
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
                        normalized["question"],
                        tuple(normalized["options"].items()),
                        normalized["correct"]
                    )
                    if sig not in seen:
                        seen.add(sig)
                        collected.append(normalized)

        if len(collected) < 12:
            dynamic_needed = 12 - len(collected)
            for item in generate_dynamic_questions(subject, dynamic_needed):
                normalized = normalize_question_item(item, fallback_subject=subject)
                if normalized:
                    sig = (
                        normalized["question"],
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
# التخزين
# =========================================================
def default_student_data() -> Dict[str, Any]:
    return {
        "student_name": "أدهم",
        "target_score": 95,
        "theme": "إمبراطوري ليلي",
        "stats": {
            "questions_answered": 0,
            "correct_answers": 0,
            "drive_opened": 0,
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
    template = default_student_data()

    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)

            if isinstance(loaded, dict):
                template.update(loaded)

            if isinstance(loaded.get("stats"), dict):
                template["stats"].update(loaded["stats"])

            if isinstance(loaded.get("subject_progress"), dict):
                template["subject_progress"].update(loaded["subject_progress"])

        except Exception:
            pass

    template.setdefault("student_name", "أدهم")
    template.setdefault("target_score", 95)
    template.setdefault("theme", "إمبراطوري ليلي")
    template.setdefault("history", [])
    template.setdefault("achievements", [])
    template.setdefault("favorites", [])
    template.setdefault("last_seen", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    template.setdefault("stats", {})
    template["stats"].setdefault("questions_answered", 0)
    template["stats"].setdefault("correct_answers", 0)
    template["stats"].setdefault("drive_opened", 0)
    template["stats"].setdefault("video_clicks", 0)
    template["stats"].setdefault("mock_exams_taken", 0)

    template.setdefault("subject_progress", {})
    for subject in SUBJECTS.keys():
        template["subject_progress"].setdefault(subject, 0)

    return template


def save_data(data: Dict[str, Any]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


data = load_data()
save_data(data)

# =========================================================
# Session State
# =========================================================
defaults = {
    "current_question": None,
    "current_question_subject": None,
    "question_result": None,
    "exam_questions": [],
    "exam_subject": None,
    "exam_answers": {},
    "exam_submitted": False
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================================================
# أدوات مساعدة
# =========================================================
def calc_percent(part: int, total: int) -> float:
    return round((part / total) * 100, 1) if total else 0.0


def get_accuracy() -> float:
    return calc_percent(
        data.get("stats", {}).get("correct_answers", 0),
        data.get("stats", {}).get("questions_answered", 0)
    )


def metric_card(label: str, value: str, note: str) -> None:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def get_status_label() -> str:
    answered = data.get("stats", {}).get("questions_answered", 0)
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


def add_favorite(name: str) -> None:
    if name not in data.get("favorites", []):
        data.setdefault("favorites", [])
        data["favorites"].append(name)
        save_data(data)


def increment_stat(key: str, amount: int = 1) -> None:
    data.setdefault("stats", {})
    data["stats"][key] = data["stats"].get(key, 0) + amount
    save_data(data)


def update_after_answer(subject: str, correct: bool, topic: str, difficulty: str, mode: str = "single_question") -> None:
    data.setdefault("stats", {})
    data["stats"]["questions_answered"] = data["stats"].get("questions_answered", 0) + 1
    if correct:
        data["stats"]["correct_answers"] = data["stats"].get("correct_answers", 0) + 1

    progress = data.get("subject_progress", {}).get(subject, 0)
    data.setdefault("subject_progress", {})
    data["subject_progress"][subject] = min(100, progress + (6 if correct else 2))

    data.setdefault("history", [])
    data["history"].append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "subject": subject,
        "topic": topic,
        "difficulty": difficulty,
        "correct": correct,
        "mode": mode
    })

    save_data(data)


def create_exam(subject: str, num_questions: int = 10) -> List[Dict[str, Any]]:
    bank = QUESTION_BANK.get(subject, [])
    if not bank:
        return []
    if len(bank) >= num_questions:
        return random.sample(bank, num_questions)

    combined = bank.copy()
    dynamic_needed = num_questions - len(combined)
    combined.extend(generate_dynamic_questions(subject, dynamic_needed))
    return combined[:num_questions]


def format_option_label(key: str, text: str) -> str:
    plain_text = re.sub(r"\s+", " ", str(text)).strip()
    return f"{key} | {plain_text}"


def render_option_legend(q: Dict[str, Any]) -> None:
    html = '<div class="option-grid">'
    for key, val in q["options"].items():
        html += f"""
        <div class="option-legend-card">
            <span class="option-badge">{key}</span>
            <span class="option-text">{val}</span>
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def get_drive_items_by_subject(subject: str) -> List[tuple]:
    result = []
    for title, link in DRIVE_LINKS.items():
        if subject in title:
            result.append((title, link))
    return result


def reset_single_question_state(subject: str) -> None:
    if st.session_state.current_question_subject != subject:
        st.session_state.current_question = None
        st.session_state.question_result = None
        st.session_state.current_question_subject = subject


def reset_exam_state(subject: str) -> None:
    if st.session_state.exam_subject != subject:
        st.session_state.exam_questions = []
        st.session_state.exam_answers = {}
        st.session_state.exam_submitted = False
        st.session_state.exam_subject = subject

# =========================================================
# Header
# =========================================================
st.markdown(f"""
<div class="hero-box">
    <div class="hero-title">🏛️ {APP_TITLE} — {APP_VERSION}</div>
    <div class="hero-sub">
        منصة تعليمية عربية احترافية بواجهة ملكية فاخرة:
        مكتبة سحابية عبر Google Drive، بنك أسئلة تفاعلي، اختبارات كبيرة مرنة،
        وتحليلات أداء كاملة مع مفاتيح اختيارات بارزة وواضحة جدًا.
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
            "☁️ المكتبة السحابية",
            "🧠 بنك الأسئلة التفاعلي",
            "📝 الاختبار الكبير",
            "📺 أكاديمية الفيديو",
            "📈 التحليلات",
            "⚙️ الإعدادات"
        ]
    )
    st.markdown("---")
    st.markdown(f"**الطالب:** {data.get('student_name', 'أدهم')}")
    st.markdown(f"**الحالة:** {get_status_label()}")
    st.markdown(f"**الهدف:** {data.get('target_score', 95)}%")
    st.info("💡 تم تأمين البيانات القديمة تلقائيًا لمنع أعطال المفاتيح الناقصة.")

# =========================================================
# الرئيسية
# =========================================================
if page == "🏠 الرئيسية":
    st.markdown('<div class="section-title">لوحة القيادة الرئيسية</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("إجمالي الأسئلة", str(data.get("stats", {}).get("questions_answered", 0)), "تم حلها داخل المنصة")
    with c2:
        metric_card("نسبة الدقة", f"{get_accuracy()}%", "معدل الإجابات الصحيحة")
    with c3:
        metric_card("روابط Drive المفتوحة", str(data.get("stats", {}).get("drive_opened", 0)), "تفاعل المكتبة السحابية")
    with c4:
        metric_card("الاختبارات الكبرى", str(data.get("stats", {}).get("mock_exams_taken", 0)), "اختبارات مكتملة")

    st.markdown('<div class="section-title">المواد الدراسية</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    for i, (subject, info) in enumerate(SUBJECTS.items()):
        with [col1, col2][i % 2]:
            progress = data.get("subject_progress", {}).get(subject, 0)
            st.markdown(f"""
            <div class="subject-card">
                <div class="subject-title">{info['icon']} {subject}</div>
                <div class="subject-meta">
                    الوصف: {info['description']}<br>
                    مستوى الصعوبة: {info['difficulty']}<br>
                    عدد الأسئلة المتاحة: {len(QUESTION_BANK.get(subject, []))}<br>
                    عدد ملفات Drive: {len(get_drive_items_by_subject(subject))}<br>
                    التقدم الحالي: {progress}%
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(progress / 100)

    if data.get("favorites"):
        st.markdown('<div class="section-title">المفضلة</div>', unsafe_allow_html=True)
        for item in data["favorites"][-5:][::-1]:
            st.markdown(f"<div class='glass-card'>⭐ {item}</div>", unsafe_allow_html=True)

# =========================================================
# المكتبة السحابية
# =========================================================
elif page == "☁️ المكتبة السحابية":
    st.markdown('<div class="section-title">المكتبة السحابية عبر Google Drive</div>', unsafe_allow_html=True)

    subject_filter = st.selectbox("فلترة حسب المادة:", ["الكل"] + list(SUBJECTS.keys()))
    items = list(DRIVE_LINKS.items())

    if subject_filter != "الكل":
        items = [(title, link) for title, link in items if subject_filter in title]

    if not items:
        st.warning("لا توجد ملفات مطابقة لهذه المادة حالياً.")
    else:
        selected_name = st.selectbox("اختر الملف:", [x[0] for x in items])
        selected_link = dict(items)[selected_name]

        st.markdown(f"""
        <div class="drive-card">
            <div class="subject-title">📂 {selected_name}</div>
            <div class="small-note">
                الملف متاح عبر Google Drive.
                يمكنك تسجيل الفتح ثم الانتقال إليه مباشرة.
            </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("📌 تسجيل فتح الملف"):
                increment_stat("drive_opened", 1)
                st.success("تم تسجيل فتح الرابط.")
        with c2:
            if st.button("⭐ إضافة للمفضلة", key=f"fav_{selected_name}"):
                add_favorite(selected_name)
                st.success("تمت الإضافة إلى المفضلة.")

        st.link_button("🚀 افتح الملف الآن", selected_link)

        st.markdown("### 📚 جميع الملفات المتاحة")
        for title, _ in items:
            st.markdown(f"""
            <div class="glass-card">
                <span class="info-chip">Google Drive</span>
                <div class="small-note">{title}</div>
            </div>
            """, unsafe_allow_html=True)

# =========================================================
# بنك الأسئلة
# =========================================================
elif page == "🧠 بنك الأسئلة التفاعلي":
    st.markdown('<div class="section-title">بنك الأسئلة التفاعلي الذكي</div>', unsafe_allow_html=True)

    available_subjects = [s for s in SUBJECTS.keys() if QUESTION_BANK.get(s)]
    subject = st.selectbox("اختر المادة:", available_subjects)
    reset_single_question_state(subject)

    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("🎯 توليد سؤال جديد"):
            st.session_state.current_question = random.choice(QUESTION_BANK[subject])
            st.session_state.question_result = None
            st.session_state.current_question_subject = subject

    with col_b:
        drive_items = get_drive_items_by_subject(subject)
        if drive_items:
            st.link_button("📘 افتح مرجع المادة", drive_items[0][1])

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

        st.markdown("### 🔑 مفتاح الاختيارات")
        render_option_legend(q)

        user_choice = st.radio(
            "اختر الإجابة الصحيحة:",
            [format_option_label(k, v) for k, v in q["options"].items()],
            key=f"single_question_answer_{subject}"
        )

        if st.button("✅ تأكيد الإجابة"):
            selected_key = user_choice.split("|")[0].strip()
            is_correct = selected_key == q["correct"]

            st.session_state.question_result = {
                "correct": is_correct,
                "correct_key": q["correct"],
                "correct_text": q["options"].get(q["correct"], ""),
                "explanation": q["explanation"]
            }

            update_after_answer(subject, is_correct, q["topic"], q["difficulty"], mode="single_question")

    if st.session_state.question_result:
        res = st.session_state.question_result
        if res["correct"]:
            st.markdown("<div class='success-box'>✅ إجابة صحيحة — أداء ممتاز جدًا.</div>", unsafe_allow_html=True)
        else:
            st.markdown(
                f"<div class='error-box'>❌ إجابة غير صحيحة — الصحيحة: {res['correct_key']} | {res['correct_text']}</div>",
                unsafe_allow_html=True
            )
        st.markdown("### ✍️ شرح الإجابة")
        st.markdown(res["explanation"])

# =========================================================
# الاختبار الكبير
# =========================================================
elif page == "📝 الاختبار الكبير":
    st.markdown('<div class="section-title">الاختبار الكبير بعدد أسئلة مرن</div>', unsafe_allow_html=True)

    available_subjects = [s for s in SUBJECTS.keys() if QUESTION_BANK.get(s)]
    subject = st.selectbox("اختر مادة الاختبار:", available_subjects, key="exam_subject_selector")
    reset_exam_state(subject)

    question_count = st.slider(
        "عدد الأسئلة",
        min_value=5,
        max_value=40,
        value=20,
        step=5
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚀 إنشاء اختبار جديد"):
            st.session_state.exam_questions = create_exam(subject, question_count)
            st.session_state.exam_answers = {}
            st.session_state.exam_submitted = False
            st.session_state.exam_subject = subject

    with c2:
        drive_items = get_drive_items_by_subject(subject)
        if drive_items:
            st.link_button("📘 مرجع المادة على Drive", drive_items[0][1])

    exam_questions = st.session_state.exam_questions

    if exam_questions:
        st.markdown(f"""
        <div class="glass-card">
            <div class="subject-title">🧠 اختبار {subject}</div>
            <div class="small-note">عدد الأسئلة الحالي: {len(exam_questions)}</div>
        </div>
        """, unsafe_allow_html=True)

        for idx, q in enumerate(exam_questions, start=1):
            with st.expander(f"السؤال رقم {idx}", expanded=False):
                st.markdown(f"**{q['question']}**")
                st.markdown("#### 🔑 الاختيارات")
                render_option_legend(q)

                labels = [format_option_label(k, v) for k, v in q["options"].items()]
                answer = st.radio(
                    f"إجابة السؤال {idx}",
                    labels,
                    key=f"exam_q_{subject}_{idx}"
                )
                st.session_state.exam_answers[idx] = answer.split("|")[0].strip()

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
                    st.markdown(f"<div class='success-box'>السؤال {idx}: إجابة صحيحة ✅</div>", unsafe_allow_html=True)
                else:
                    st.markdown(
                        f"<div class='error-box'>السؤال {idx}: إجابة خاطئة ❌ | الصحيحة: {q['correct']} | {q['options'][q['correct']]}</div>",
                        unsafe_allow_html=True
                    )

                st.markdown(f"**الشرح:** {q['explanation']}")

                data.setdefault("history", [])
                data["history"].append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "subject": subject,
                    "topic": q["topic"],
                    "difficulty": q["difficulty"],
                    "correct": is_correct,
                    "mode": "big_exam"
                })

            data.setdefault("stats", {})
            data["stats"]["questions_answered"] = data["stats"].get("questions_answered", 0) + total
            data["stats"]["correct_answers"] = data["stats"].get("correct_answers", 0) + correct_count
            data["stats"]["mock_exams_taken"] = data["stats"].get("mock_exams_taken", 0) + 1

            data.setdefault("subject_progress", {})
            current_progress = data["subject_progress"].get(subject, 0)
            data["subject_progress"][subject] = min(100, current_progress + max(5, correct_count * 2))

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
                    الموضوعات الرئيسية: {", ".join(info['topics'])}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.link_button(f"📺 فتح شروحات {subject}", info["youtube"])
            if st.button(f"📌 تسجيل مشاهدة {subject}", key=f"video_track_{subject}"):
                increment_stat("video_clicks", 1)
                st.success("تم تسجيل المشاهدة.")

# =========================================================
# التحليلات
# =========================================================
elif page == "📈 التحليلات":
    st.markdown('<div class="section-title">التحليلات ومؤشرات الأداء</div>', unsafe_allow_html=True)

    total_q = data.get("stats", {}).get("questions_answered", 0)
    correct_q = data.get("stats", {}).get("correct_answers", 0)
    wrong_q = max(total_q - correct_q, 0)
    accuracy = get_accuracy()

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("الإجابات الصحيحة", str(correct_q), "مجموع الحلول الصحيحة")
    with c2:
        metric_card("الإجابات الخاطئة", str(wrong_q), "مجموع الأخطاء المسجلة")
    with c3:
        metric_card("الدقة الكلية", f"{accuracy}%", "كلما ارتفعت الدقة زادت الجاهزية")

    progress_df = pd.DataFrame([
        {"المادة": subject, "نسبة التقدم": data.get("subject_progress", {}).get(subject, 0)}
        for subject in SUBJECTS.keys()
    ])
    st.dataframe(progress_df, use_container_width=True, hide_index=True)

    if data.get("history"):
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
        st.dataframe(history_df.iloc[::-1], use_container_width=True, hide_index=True)
    else:
        st.info("لا توجد بيانات كافية بعد.")

# =========================================================
# الإعدادات
# =========================================================
elif page == "⚙️ الإعدادات":
    st.markdown('<div class="section-title">إعدادات المنصة</div>', unsafe_allow_html=True)

    student_name = st.text_input("اسم الطالب", value=data.get("student_name", "أدهم"))
    target_score = st.slider("الهدف النهائي", 50, 100, int(data.get("target_score", 95)))

    if st.button("💾 حفظ الإعدادات"):
        data["student_name"] = student_name.strip() or "أدهم"
        data["target_score"] = target_score
        data["last_seen"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_data(data)
        st.success("تم حفظ الإعدادات بنجاح.")

    if st.button("🧹 إعادة ضبط السجل"):
        old_name = data.get("student_name", "أدهم")
        old_target = data.get("target_score", 95)
        new_data = default_student_data()
        new_data["student_name"] = old_name
        new_data["target_score"] = old_target
        save_data(new_data)
        st.success("تمت إعادة الضبط. أعد تحميل الصفحة.")

# =========================================================
# Footer
# =========================================================
st.markdown("""
<div class="footer-note">
    حصن أدهم التعليمي — النسخة النهائية الفاخرة بمفاتيح اختيارات بارزة وبيانات مؤمنة ومكتبة سحابية واختبارات مرنة.
</div>
""", unsafe_allow_html=True)
