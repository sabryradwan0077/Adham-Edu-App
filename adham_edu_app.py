# -*- coding: utf-8 -*-
from __future__ import annotations

import time
import re
from typing import Dict, List, Any, Optional

import pandas as pd
import streamlit as st

# =========================================================
# المنصة التعليمية - باقورة أعمال المهندس أدهم صبري
# نسخة متكاملة: شرح + اختبارات + ملفات + فيديوهات يوتيوب + بحث ذكي
# =========================================================

APP_NAME = "المنصة التعليمية باقورة أعمال المهندس أدهم صبري"
APP_ICON = "👑"

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# هوية بصرية فاخرة جدًا
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif !important;
    }

    .stApp {
        background:
            radial-gradient(circle at top right, rgba(31, 79, 168, 0.22), transparent 26%),
            radial-gradient(circle at top left, rgba(214, 170, 54, 0.12), transparent 22%),
            linear-gradient(180deg, #030814 0%, #071225 35%, #0a1831 70%, #08101f 100%);
        color: #f8fbff;
    }

    .block-container {
        padding-top: 1.3rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    .hero-shell {
        position: relative;
        overflow: hidden;
        border-radius: 28px;
        padding: 34px 28px 28px 28px;
        background:
            linear-gradient(135deg, rgba(10,25,53,0.92), rgba(5,14,31,0.96)),
            radial-gradient(circle at 85% 20%, rgba(255,215,90,0.18), transparent 22%);
        border: 1px solid rgba(255,255,255,0.09);
        box-shadow: 0 20px 60px rgba(0,0,0,0.35);
        margin-bottom: 22px;
    }

    .hero-shell::before {
        content: "";
        position: absolute;
        inset: 0;
        background:
            linear-gradient(120deg, transparent 0%, rgba(255,255,255,0.04) 20%, transparent 40%);
        pointer-events: none;
    }

    .brand-line {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 999px;
        background: rgba(255, 215, 102, 0.10);
        border: 1px solid rgba(255, 215, 102, 0.24);
        color: #ffe8a3;
        font-size: 0.95rem;
        font-weight: 800;
        margin-bottom: 14px;
    }

    .main-title {
        font-size: 2.65rem;
        font-weight: 900;
        line-height: 1.45;
        color: #ffffff;
        text-align: center;
        margin-bottom: 8px;
        text-shadow: 0 3px 25px rgba(108,151,255,0.18);
    }

    .sub-title {
        font-size: 1.08rem;
        text-align: center;
        color: #d6e2f1;
        line-height: 2;
        margin-bottom: 18px;
    }

    .hero-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-top: 12px;
    }

    .hero-stat {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 16px;
        text-align: center;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
    }

    .hero-stat-value {
        font-size: 1.55rem;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 4px;
    }

    .hero-stat-label {
        font-size: 0.96rem;
        font-weight: 700;
        color: #cbd7e6;
    }

    .section-shell {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 24px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0 14px 40px rgba(0,0,0,0.18);
    }

    .section-title {
        font-size: 1.35rem;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .section-subtitle {
        color: #d4ddeb;
        font-size: 0.98rem;
        margin-bottom: 16px;
        line-height: 1.9;
    }

    .lux-card {
        background:
            linear-gradient(180deg, rgba(255,255,255,0.045), rgba(255,255,255,0.03));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 18px;
        margin-bottom: 14px;
    }

    .lesson-card {
        background:
            linear-gradient(135deg, rgba(20,34,68,0.95), rgba(11,20,39,0.98));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 18px;
        margin-bottom: 14px;
    }

    .lesson-title {
        font-size: 1.14rem;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 6px;
    }

    .lesson-meta {
        color: #d2dbea;
        font-size: 0.93rem;
        line-height: 1.9;
    }

    .question-shell {
        background:
            linear-gradient(135deg, rgba(19,32,64,0.98), rgba(11,19,36,0.99));
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 24px;
        padding: 24px;
        margin-top: 12px;
        margin-bottom: 16px;
        box-shadow: 0 14px 35px rgba(0,0,0,0.22);
    }

    .question-badge {
        display: inline-block;
        padding: 8px 15px;
        border-radius: 999px;
        background: linear-gradient(90deg, rgba(19,63,119,0.95), rgba(28,101,167,0.95));
        color: #ffffff;
        font-size: 0.95rem;
        font-weight: 900;
        margin-bottom: 12px;
    }

    .chip {
        display: inline-block;
        margin-left: 8px;
        margin-bottom: 8px;
        padding: 7px 13px;
        border-radius: 999px;
        background: rgba(110,168,254,0.13);
        color: #e2edff;
        font-weight: 800;
        font-size: 0.92rem;
        border: 1px solid rgba(110,168,254,0.20);
    }

    .question-text {
        font-size: 1.48rem;
        line-height: 2.2;
        font-weight: 900;
        color: #ffffff;
        margin-top: 8px;
        margin-bottom: 20px;
    }

    .timer-box {
        padding: 15px 18px;
        border-radius: 18px;
        font-size: 1.22rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 15px;
    }

    .timer-safe {
        background: rgba(42, 157, 87, 0.15);
        border: 1px solid rgba(42, 157, 87, 0.42);
        color: #c7f6d5;
    }

    .timer-mid {
        background: rgba(244, 162, 97, 0.15);
        border: 1px solid rgba(244, 162, 97, 0.40);
        color: #ffe1bc;
    }

    .timer-danger {
        background: rgba(231, 111, 81, 0.18);
        border: 1px solid rgba(231, 111, 81, 0.45);
        color: #ffd7cf;
    }

    .success-box {
        background: rgba(42, 157, 87, 0.16);
        border: 1px solid rgba(42, 157, 87, 0.42);
        color: #ddffe8;
        padding: 18px;
        border-radius: 18px;
        font-weight: 800;
        margin-top: 14px;
        margin-bottom: 14px;
        line-height: 2;
    }

    .error-box {
        background: rgba(231, 111, 81, 0.16);
        border: 1px solid rgba(231, 111, 81, 0.45);
        color: #ffe3dc;
        padding: 18px;
        border-radius: 18px;
        font-weight: 800;
        margin-top: 14px;
        margin-bottom: 14px;
        line-height: 2;
    }

    .youtube-card {
        background:
            linear-gradient(135deg, rgba(66,13,24,0.9), rgba(28,9,14,0.95));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 18px;
        margin-bottom: 14px;
    }

    .yt-title {
        font-size: 1.06rem;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 6px;
    }

    .yt-note {
        color: #efd2d8;
        font-size: 0.93rem;
        line-height: 1.9;
    }

    .small-note {
        color: #cad7e6;
        font-size: 0.95rem;
        line-height: 1.9;
    }

    .metric-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 18px;
        text-align: center;
    }

    div[data-baseweb="radio"] label {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 18px;
        padding: 16px 18px;
        margin-bottom: 12px;
        width: 100%;
        transition: 0.2s ease;
    }

    div[data-baseweb="radio"] label:hover {
        border-color: #90b7ff;
        background: rgba(110,168,254,0.12);
        transform: translateY(-1px);
    }

    div[data-baseweb="radio"] label div {
        font-size: 1.22rem !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        line-height: 2 !important;
    }

    .stButton > button,
    .stDownloadButton > button {
        width: 100%;
        border-radius: 16px;
        font-size: 1rem;
        font-weight: 900;
        padding: 0.82rem 1rem;
        border: 1px solid rgba(255,255,255,0.12);
        background: linear-gradient(135deg, #183866, #11294d);
        color: white;
        box-shadow: 0 8px 20px rgba(0,0,0,0.16);
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        border-color: rgba(255,255,255,0.25);
        transform: translateY(-1px);
    }

    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 14px !important;
    }

    .footer-note {
        text-align: center;
        color: #b7c7db;
        font-size: 0.95rem;
        margin-top: 10px;
        line-height: 2;
    }

    @media (max-width: 1100px) {
        .hero-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        .main-title {
            font-size: 2rem;
        }
        .question-text {
            font-size: 1.25rem;
        }
    }

    @media (max-width: 700px) {
        .hero-grid {
            grid-template-columns: 1fr;
        }
        .main-title {
            font-size: 1.7rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# بيانات المنصة
# =========================================================
def make_question(subject: str, unit: str, difficulty: str, question: str,
                  options: List[str], answer: str, explanation: str,
                  time_limit_sec: int) -> Dict[str, Any]:
    return {
        "subject": subject,
        "unit": unit,
        "difficulty": difficulty,
        "question": question,
        "options": options,
        "answer": answer,
        "explanation": explanation,
        "time_limit_sec": time_limit_sec
    }

def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", str(text).strip().lower())

def smart_match_score(query: str, text: str) -> int:
    q = normalize_text(query)
    t = normalize_text(text)
    if not q:
        return 0
    score = 0
    for token in q.split():
        if token in t:
            score += 10
    if q in t:
        score += 25
    return score

def extract_gdrive_file_id(url: str) -> Optional[str]:
    if not url:
        return None
    patterns = [
        r"/file/d/([a-zA-Z0-9_-]+)",
        r"id=([a-zA-Z0-9_-]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def to_gdrive_preview(url: str) -> str:
    file_id = extract_gdrive_file_id(url)
    if file_id:
        return f"https://drive.google.com/file/d/{file_id}/preview"
    return url

def to_gdrive_download(url: str) -> str:
    file_id = extract_gdrive_file_id(url)
    if file_id:
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    return url

# =========================================================
# ملفات الشرح PDF
# =========================================================
PDF_RESOURCES = [
    {
        "title": "ملف الفيزياء - الكهرباء والفيزياء الحديثة",
        "subject": "الفيزياء",
        "unit": "الكهرباء / الفيزياء الحديثة",
        "keywords": ["فيزياء", "كهرباء", "قوانين كيرشوف", "حركة", "مغناطيسية", "ذرة"],
        "drive_link": "https://drive.google.com/file/d/PUT_REAL_FILE_ID_1/view?usp=sharing"
    },
    {
        "title": "ملف الرياضيات - التفاضل والتكامل والجبر",
        "subject": "الرياضيات",
        "unit": "تفاضل / تكامل / جبر / هندسة",
        "keywords": ["رياضيات", "تفاضل", "تكامل", "نهايات", "احتمالات", "مصفوفات"],
        "drive_link": "https://drive.google.com/file/d/PUT_REAL_FILE_ID_2/view?usp=sharing"
    },
    {
        "title": "ملف الكيمياء - العامة والعضوية",
        "subject": "الكيمياء",
        "unit": "التركيب الذري / الروابط / العضوية",
        "keywords": ["كيمياء", "عضوية", "أحماض", "قواعد", "مول", "تفاعل"],
        "drive_link": "https://drive.google.com/file/d/PUT_REAL_FILE_ID_3/view?usp=sharing"
    },
    {
        "title": "ملف اللغة العربية - النحو والبلاغة والأدب",
        "subject": "اللغة العربية",
        "unit": "النحو / البلاغة / الأدب / القراءة",
        "keywords": ["عربي", "نحو", "بلاغة", "أدب", "قراءة", "تحليل نصوص"],
        "drive_link": "https://drive.google.com/file/d/PUT_REAL_FILE_ID_4/view?usp=sharing"
    },
]

# =========================================================
# روابط يوتيوب
# ضع الروابط الحقيقية مكان الروابط التجريبية
# =========================================================
YOUTUBE_RESOURCES = [
    {
        "title": "شرح الفيزياء - الباب الأول",
        "subject": "الفيزياء",
        "unit": "الكهرباء",
        "keywords": ["فيزياء", "كهرباء", "تيار", "أوم", "كيرشوف"],
        "youtube_url": "https://www.youtube.com/watch?v=PUT_REAL_VIDEO_ID_1",
        "description": "شرح مركز وواضح لأساسيات الكهرباء وقوانينها والمسائل الوزارية."
    },
    {
        "title": "شرح الرياضيات - التفاضل والتكامل",
        "subject": "الرياضيات",
        "unit": "التفاضل والتكامل",
        "keywords": ["رياضيات", "تفاضل", "تكامل", "نهايات"],
        "youtube_url": "https://www.youtube.com/watch?v=PUT_REAL_VIDEO_ID_2",
        "description": "فيديو شرح منظم يبدأ من الفكرة الأساسية وحتى التطبيقات الامتحانية."
    },
    {
        "title": "شرح الكيمياء - الأحماض والقواعد والعضوية",
        "subject": "الكيمياء",
        "unit": "الأحماض والقواعد / العضوية",
        "keywords": ["كيمياء", "أحماض", "قواعد", "عضوية"],
        "youtube_url": "https://www.youtube.com/watch?v=PUT_REAL_VIDEO_ID_3",
        "description": "مراجعة قوية لأهم النقاط النظرية والجزئيات المتكررة في الامتحانات."
    },
    {
        "title": "شرح اللغة العربية - النحو والبلاغة",
        "subject": "اللغة العربية",
        "unit": "النحو / البلاغة",
        "keywords": ["عربي", "نحو", "بلاغة", "أساليب"],
        "youtube_url": "https://www.youtube.com/watch?v=PUT_REAL_VIDEO_ID_4",
        "description": "شرح مبسط واحترافي يساعد الطالب على الفهم السريع والتثبيت."
    },
]

# =========================================================
# محتوى الشرح داخل المنصة
# =========================================================
LESSON_SUMMARIES = [
    {
        "subject": "الفيزياء",
        "title": "مدخل إلى الكهرباء والدوائر الكهربية",
        "unit": "التيار - فرق الجهد - المقاومة - قانون أوم",
        "summary": "في هذا الدرس يتعرف الطالب إلى المفاهيم الأساسية للكهرباء، والعلاقة بين التيار وفرق الجهد والمقاومة، وطريقة حل المسائل الأساسية بصورة منظمة تمهيدًا لباقي الأبواب."
    },
    {
        "subject": "الرياضيات",
        "title": "التفاضل والتكامل بطريقة امتحانية",
        "unit": "المشتقات - التطبيقات - التكامل",
        "summary": "يتناول هذا الدرس قواعد الاشتقاق والتطبيقات المباشرة عليها، ثم ينتقل إلى التكامل والصيغ الأساسية وأهم الأفكار التي تظهر في الامتحانات الرسمية."
    },
    {
        "subject": "الكيمياء",
        "title": "التركيب الذري والروابط الكيميائية",
        "unit": "الذرة - الجدول الدوري - الروابط",
        "summary": "يشرح هذا المحور البناء الذري، وتوزيع الإلكترونات، وعلاقة ذلك بتدرج الخواص الكيميائية وتكوين الروابط الأيونية والتساهمية."
    },
    {
        "subject": "اللغة العربية",
        "title": "مدخل احترافي إلى النحو والبلاغة",
        "unit": "الفاعل - اسم إن - الاستعارة - التشبيه",
        "summary": "يركز هذا الدرس على القواعد التي يكثر ورودها في الامتحانات، مع تدريب الطالب على الفهم الدقيق للإعراب والتمييز بين الأساليب والصور البلاغية."
    },
]

# =========================================================
# بنك الأسئلة
# =========================================================
def get_questions() -> List[Dict[str, Any]]:
    return [
        make_question("الفيزياء", "التيار الكهربي", "سهل",
                      "إذا مر تيار شدته 2 أمبير في موصل لمدة 5 ثوانٍ، فما مقدار الشحنة الكهربية المارة؟",
                      ["أ) 2 كولوم", "ب) 5 كولوم", "ج) 10 كولوم", "د) 20 كولوم"],
                      "ج",
                      "نطبق العلاقة: الشحنة = شدة التيار × الزمن، إذن الشحنة = 2 × 5 = 10 كولوم.",
                      45),

        make_question("الفيزياء", "قانون أوم", "سهل",
                      "مقاومة مقدارها 4 أوم موصلة بفرق جهد 12 فولت، فما شدة التيار المار فيها؟",
                      ["أ) 2 أمبير", "ب) 3 أمبير", "ج) 4 أمبير", "د) 6 أمبير"],
                      "ب",
                      "طبقًا لقانون أوم: شدة التيار = فرق الجهد ÷ المقاومة = 12 ÷ 4 = 3 أمبير.",
                      45),

        make_question("الفيزياء", "قوانين كيرشوف", "متوسط",
                      "ينص قانون كيرشوف الأول على أن المجموع الجبري للتيارات عند نقطة التقاء يساوي:",
                      ["أ) المقاومة", "ب) الجهد", "ج) صفر", "د) مالا نهاية"],
                      "ج",
                      "مجموع التيارات الداخلة إلى العقدة يساوي مجموع التيارات الخارجة منها، ولذلك يكون المجموع الجبري صفراً.",
                      55),

        make_question("الفيزياء", "القدرة الكهربية", "متوسط",
                      "جهاز كهربي يعمل عند فرق جهد 220 فولت وشدة تيار 5 أمبير، فما قدرته؟",
                      ["أ) 44 وات", "ب) 220 وات", "ج) 1100 وات", "د) 4400 وات"],
                      "ج",
                      "القدرة = فرق الجهد × شدة التيار = 220 × 5 = 1100 وات.",
                      50),

        make_question("الفيزياء", "السعة الكهربية", "صعب",
                      "إذا تضاعفت مساحة لوحي مكثف مستوٍ مع ثبات المسافة بينهما، فإن السعة الكهربية:",
                      ["أ) تقل للنصف", "ب) تظل ثابتة", "ج) تتضاعف", "د) تصبح أربعة أمثال"],
                      "ج",
                      "السعة تتناسب طرديًا مع المساحة وعكسيًا مع المسافة، لذا مع ثبات المسافة وتضاعف المساحة تتضاعف السعة.",
                      65),

        make_question("الرياضيات", "التفاضل", "سهل",
                      "ما مشتقة الدالة س = x² ؟",
                      ["أ) x", "ب) 2x", "ج) x³", "د) 2"],
                      "ب",
                      "باستخدام قاعدة القوة، مشتقة x² تساوي 2x.",
                      40),

        make_question("الرياضيات", "التكامل", "سهل",
                      "ما قيمة التكامل ∫ 3x² dx ؟",
                      ["أ) x³ + ثابت", "ب) 3x³ + ثابت", "ج) x² + ثابت", "د) 6x + ثابت"],
                      "أ",
                      "تكامل 3x² يساوي x³ + ثابت التكامل.",
                      45),

        make_question("الرياضيات", "النهايات", "متوسط",
                      "النهاية عندما x تقترب من 1 للتعبير (x² − 1) ÷ (x − 1) تساوي:",
                      ["أ) 0", "ب) 1", "ج) 2", "د) غير معرفة"],
                      "ج",
                      "نحلل x² − 1 إلى (x − 1)(x + 1)، ثم نختصر فيتبقى x + 1، وعند x = 1 تكون النهاية 2.",
                      55),

        make_question("الرياضيات", "الاحتمالات", "متوسط",
                      "إذا ألقي حجر نرد منتظم مرة واحدة، فما احتمال ظهور عدد أولي؟",
                      ["أ) 1/6", "ب) 1/3", "ج) 1/2", "د) 2/3"],
                      "ج",
                      "الأعداد الأولية على حجر النرد هي 2 و3 و5، أي 3 نواتج من 6، فيكون الاحتمال 1/2.",
                      50),

        make_question("الرياضيات", "التكامل بالتجزئة", "صعب",
                      "أي العبارات الآتية تمثل صيغة التكامل بالتجزئة تمثيلًا صحيحًا؟",
                      ["أ) ∫u dv = uv − ∫v du", "ب) ∫u dv = uv + ∫v du", "ج) ∫u dv = du × dv", "د) ∫u dv = u/v + ثابت"],
                      "أ",
                      "الصيغة القياسية للتكامل بالتجزئة هي: ∫u dv = uv − ∫v du.",
                      70),

        make_question("الكيمياء", "التركيب الذري", "سهل",
                      "العدد الذري للعنصر يساوي عدد:",
                      ["أ) النيوترونات", "ب) البروتونات", "ج) النيوكلونات", "د) مستويات الطاقة"],
                      "ب",
                      "العدد الذري يعبّر عن عدد البروتونات داخل نواة الذرة.",
                      40),

        make_question("الكيمياء", "الجدول الدوري", "سهل",
                      "العناصر الموجودة في نفس المجموعة في الجدول الدوري تتشابه في:",
                      ["أ) الكتلة الذرية فقط", "ب) عدد النيوترونات", "ج) الخواص الكيميائية", "د) الحالة الفيزيائية فقط"],
                      "ج",
                      "عناصر المجموعة الواحدة تتشابه في عدد إلكترونات التكافؤ تقريبًا، لذلك تتقارب في الخواص الكيميائية.",
                      45),

        make_question("الكيمياء", "الأحماض والقواعد", "متوسط",
                      "محلول قيمة الأس الهيدروجيني له تساوي 2 يُعد محلولًا:",
                      ["أ) متعادلًا", "ب) قاعديًا", "ج) حمضيًا", "د) منظمًا فقط"],
                      "ج",
                      "المحاليل التي تقل قيمة pH لها عن 7 تكون حمضية.",
                      45),

        make_question("الكيمياء", "المول", "متوسط",
                      "يحتوي مول واحد من أي مادة على:",
                      ["أ) 10²³ جسيم", "ب) 6.02 × 10²³ جسيم", "ج) 3.01 × 10²³ جسيم", "د) 12 جسيمًا"],
                      "ب",
                      "عدد أفوجادرو يساوي 6.02 × 10²³ جسيمًا في المول الواحد.",
                      50),

        make_question("الكيمياء", "سرعة التفاعل", "صعب",
                      "يعمل العامل الحفاز على زيادة سرعة التفاعل لأنه:",
                      ["أ) يزيد طاقة التنشيط", "ب) يقلل طاقة التنشيط", "ج) يغير النواتج", "د) يغيّر الاتزان فقط"],
                      "ب",
                      "العامل الحفاز يوفر مسارًا بديلًا بطاقة تنشيط أقل، فيزداد معدل التفاعل.",
                      65),

        make_question("اللغة العربية", "النحو", "سهل",
                      "اختر الجملة الصحيحة من حيث رفع الفاعل:",
                      ["أ) حضرَ الطالبُ", "ب) حضرَ الطالبَ", "ج) حضرَ الطالبِ", "د) حضرَ الطالبْ"],
                      "أ",
                      "الفاعل يجب أن يكون مرفوعًا، ولذلك تكون الصورة الصحيحة: الطالبُ.",
                      45),

        make_question("اللغة العربية", "النحو", "متوسط",
                      "في الجملة: إن العلمَ نورٌ، كلمة العلمَ تعرب:",
                      ["أ) خبر إن", "ب) اسم إن", "ج) فاعل", "د) مفعول به"],
                      "ب",
                      "بعد إن يأتي اسمها منصوبًا، ولذلك تعرب كلمة العلمَ: اسم إن منصوب.",
                      55),

        make_question("اللغة العربية", "البلاغة", "متوسط",
                      "يقوم التشبيه في البلاغة العربية على:",
                      ["أ) كلمة واحدة فقط", "ب) المقارنة بين شيئين", "ج) فعل ومفعول فقط", "د) جملة بلا معنى"],
                      "ب",
                      "التشبيه يقوم على المقارنة بين شيئين يشتركان في صفة معينة.",
                      55),

        make_question("اللغة العربية", "الأساليب", "صعب",
                      "في التعبير: ما أجملَ السماءَ، يكون الأسلوب:",
                      ["أ) أمر", "ب) استفهام", "ج) تعجب", "د) نفي"],
                      "ج",
                      "صيغة ما أفعلَ من أشهر صيغ التعجب القياسية في العربية.",
                      55),

        make_question("اللغة العربية", "تحليل النصوص", "صعب",
                      "عند تحليل نص أدبي تحليلاً احترافيًا، فإن أول خطوة صحيحة تكون:",
                      ["أ) عد الكلمات فقط", "ب) تحديد الفكرة المحورية والنبرة العامة", "ج) معرفة عمر الكاتب فقط", "د) عد علامات الترقيم"],
                      "ب",
                      "التحليل الأدبي الرصين يبدأ بتحديد الفكرة العامة والنبرة المسيطرة قبل الصور والأساليب.",
                      65),
    ]

# =========================================================
# البحث الذكي
# =========================================================
def run_search(query: str,
               lesson_summaries: List[Dict[str, Any]],
               pdf_resources: List[Dict[str, Any]],
               youtube_resources: List[Dict[str, Any]],
               questions: List[Dict[str, Any]]) -> Dict[str, Any]:
    query = query.strip()
    if not query:
        return {"lessons": [], "pdfs": [], "youtube": [], "questions": []}

    lessons = []
    pdfs = []
    youtube = []
    question_hits = []

    for item in lesson_summaries:
        hay = " ".join([item["subject"], item["title"], item["unit"], item["summary"]])
        score = smart_match_score(query, hay)
        if score > 0:
            lessons.append((score, item))

    for item in pdf_resources:
        hay = " ".join([item["title"], item["subject"], item["unit"], " ".join(item["keywords"])])
        score = smart_match_score(query, hay)
        if score > 0:
            pdfs.append((score, item))

    for item in youtube_resources:
        hay = " ".join([item["title"], item["subject"], item["unit"], item["description"], " ".join(item["keywords"])])
        score = smart_match_score(query, hay)
        if score > 0:
            youtube.append((score, item))

    for item in questions:
        hay = " ".join([
            item["subject"], item["unit"], item["difficulty"], item["question"],
            item["explanation"], " ".join(item["options"])
        ])
        score = smart_match_score(query, hay)
        if score > 0:
            question_hits.append((score, item))

    lessons.sort(key=lambda x: x[0], reverse=True)
    pdfs.sort(key=lambda x: x[0], reverse=True)
    youtube.sort(key=lambda x: x[0], reverse=True)
    question_hits.sort(key=lambda x: x[0], reverse=True)

    return {
        "lessons": [x[1] for x in lessons[:6]],
        "pdfs": [x[1] for x in pdfs[:6]],
        "youtube": [x[1] for x in youtube[:6]],
        "questions": [x[1] for x in question_hits[:6]],
    }

# =========================================================
# حالة الجلسة
# =========================================================
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

def reset_exam():
    st.session_state.questions = get_questions()
    st.session_state.quiz_started = True
    st.session_state.current_index = 0
    st.session_state.answers = {}
    st.session_state.answer_submitted = False
    st.session_state.deadline = None
    st.session_state.question_started_at = None
    st.session_state.auto_skipped = []
    st.session_state.exam_finished = False

def start_question_timer(question: Dict[str, Any]):
    st.session_state.question_started_at = time.time()
    st.session_state.deadline = time.time() + int(question.get("time_limit_sec", 60))

def ensure_timer_for_current_question():
    idx = st.session_state.current_index
    if idx < len(st.session_state.questions) and st.session_state.deadline is None:
        start_question_timer(st.session_state.questions[idx])

def answer_letter_from_option(option_text: str) -> str:
    if not option_text:
        return ""
    return option_text.strip()[0]

def submit_current_answer():
    idx = st.session_state.current_index
    questions = st.session_state.questions
    if idx >= len(questions):
        return

    chosen = st.session_state.get(f"q_choice_{idx}")
    if not chosen:
        return

    q = questions[idx]
    chosen_letter = answer_letter_from_option(chosen)
    st.session_state.answers[idx] = {
        "selected_option": chosen,
        "selected_letter": chosen_letter,
        "correct_letter": q["answer"],
        "is_correct": chosen_letter == q["answer"],
        "timed_out": False,
        "subject": q["subject"],
        "unit": q["unit"],
        "question": q["question"]
    }
    st.session_state.answer_submitted = True

def move_to_next_question(timeout_skip: bool = False):
    idx = st.session_state.current_index
    questions = st.session_state.questions

    if idx < len(questions):
        q = questions[idx]
        if timeout_skip and idx not in st.session_state.answers:
            st.session_state.answers[idx] = {
                "selected_option": None,
                "selected_letter": None,
                "correct_letter": q["answer"],
                "is_correct": False,
                "timed_out": True,
                "subject": q["subject"],
                "unit": q["unit"],
                "question": q["question"]
            }
            st.session_state.auto_skipped.append(idx)

    st.session_state.current_index += 1
    st.session_state.answer_submitted = False
    st.session_state.deadline = None
    st.session_state.question_started_at = None

    if st.session_state.current_index >= len(questions):
        st.session_state.exam_finished = True
    else:
        start_question_timer(questions[st.session_state.current_index])

    st.rerun()

def get_timer_class(seconds_left: int, total_seconds: int) -> str:
    ratio = seconds_left / max(total_seconds, 1)
    if ratio > 0.5:
        return "timer-safe"
    elif ratio > 0.2:
        return "timer-mid"
    return "timer-danger"

# =========================================================
# تهيئة
# =========================================================
init_state()
questions = st.session_state.questions

# =========================================================
# رأس المنصة
# =========================================================
st.markdown("""
<div class="hero-shell">
    <div style="text-align:center;">
        <div class="brand-line">إبداع تقني • فخامة بصرية • تجربة تعليمية متكاملة</div>
        <div class="main-title">المنصة التعليمية باقورة أعمال المهندس أدهم صبري</div>
        <div class="sub-title">
            منصة تعليمية متكاملة تجمع بين الشرح المنظم، والبحث الذكي، والاختبارات الاحترافية، وروابط ملفات الدراسة،
            وفيديوهات يوتيوب التعليمية في واجهة ملكية مصممة لتبهر الطالب من أول نظرة وحتى آخر نتيجة.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="hero-grid">
    <div class="hero-stat">
        <div class="hero-stat-value">{len(LESSON_SUMMARIES)}</div>
        <div class="hero-stat-label">محاور شرح رئيسية</div>
    </div>
    <div class="hero-stat">
        <div class="hero-stat-value">{len(PDF_RESOURCES)}</div>
        <div class="hero-stat-label">ملفات PDF تعليمية</div>
    </div>
    <div class="hero-stat">
        <div class="hero-stat-value">{len(YOUTUBE_RESOURCES)}</div>
        <div class="hero-stat-label">مقترحات فيديو يوتيوب</div>
    </div>
    <div class="hero-stat">
        <div class="hero-stat-value">{len(questions)}</div>
        <div class="hero-stat-label">أسئلة تدريبية احترافية</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# الشريط الجانبي
# =========================================================
with st.sidebar:
    st.markdown("### مركز القيادة")
    page = st.radio(
        "اختر القسم",
        [
            "الواجهة الرئيسية",
            "مركز الشرح",
            "مكتبة الملفات",
            "مكتبة يوتيوب",
            "الاختبار الذكي",
            "لوحة النتائج"
        ],
        key="current_track"
    )

    st.markdown("---")
    total_q = len(st.session_state.questions)
    answered_count = len(st.session_state.answers)
    correct_count = sum(1 for a in st.session_state.answers.values() if a["is_correct"])
    skipped_count = sum(1 for a in st.session_state.answers.values() if a.get("timed_out"))

    st.metric("إجمالي الأسئلة", total_q)
    st.metric("المعالَج من الأسئلة", answered_count)
    st.metric("الإجابات الصحيحة", correct_count)
    st.metric("التخطي التلقائي", skipped_count)

    st.markdown("---")
    if st.button("بدء اختبار جديد بالكامل"):
        reset_exam()

# =========================================================
# البحث الذكي العالمي
# =========================================================
st.markdown('<div class="section-shell">', unsafe_allow_html=True)
st.markdown('<div class="section-title">البحث الذكي الشامل داخل المنصة</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">ابحث عن درس، أو وحدة، أو مادة، أو نوع سؤال، أو شرح، أو ملف PDF، أو فيديو يوتيوب، وسيتم عرض كل ما يتعلق ببحثك داخل المنصة.</div>', unsafe_allow_html=True)

search_query = st.text_input(
    "اكتب ما تريد البحث عنه",
    placeholder="مثال: قوانين كيرشوف - التكامل - الأحماض والقواعد - النحو - الاستعارة"
)

search_results = run_search(search_query, LESSON_SUMMARIES, PDF_RESOURCES, YOUTUBE_RESOURCES, questions) if search_query else None

if search_results:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### نتائج الشرح والملفات")
        if search_results["lessons"]:
            for item in search_results["lessons"]:
                st.markdown(f"""
                <div class="lesson-card">
                    <div class="lesson-title">{item['title']}</div>
                    <div class="lesson-meta">المادة: {item['subject']} | الوحدة: {item['unit']}</div>
                    <div class="small-note">{item['summary']}</div>
                </div>
                """, unsafe_allow_html=True)
        if search_results["pdfs"]:
            for item in search_results["pdfs"]:
                st.markdown(f"""
                <div class="lux-card">
                    <div class="lesson-title">{item['title']}</div>
                    <div class="lesson-meta">المادة: {item['subject']} | الوحدة: {item['unit']}</div>
                </div>
                """, unsafe_allow_html=True)
                a1, a2 = st.columns(2)
                with a1:
                    st.link_button("فتح معاينة الملف", to_gdrive_preview(item["drive_link"]))
                with a2:
                    st.link_button("تحميل الملف", to_gdrive_download(item["drive_link"]))

    with c2:
        st.markdown("#### نتائج الفيديوهات والأسئلة")
        if search_results["youtube"]:
            for item in search_results["youtube"]:
                st.markdown(f"""
                <div class="youtube-card">
                    <div class="yt-title">{item['title']}</div>
                    <div class="yt-note">المادة: {item['subject']} | الوحدة: {item['unit']}</div>
                    <div class="yt-note">{item['description']}</div>
                </div>
                """, unsafe_allow_html=True)
                st.link_button("فتح فيديو يوتيوب", item["youtube_url"])
        if search_results["questions"]:
            for item in search_results["questions"]:
                st.markdown(f"""
                <div class="lux-card">
                    <div class="lesson-title">{item['subject']} • {item['unit']}</div>
                    <div class="small-note">{item['question']}</div>
                </div>
                """, unsafe_allow_html=True)
elif search_query:
    st.warning("لا توجد نتائج مطابقة حاليًا. جرّب كلمات أخرى أو أضف موارد وروابط أكثر تخصصًا داخل الكود.")

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# الواجهة الرئيسية
# =========================================================
if page == "الواجهة الرئيسية":
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">رسالة المنصة</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-subtitle">
        هذه المنصة ليست مجرد صفحة لعرض أسئلة أو ملفات، بل هي نظام تعليمي متكامل يجمع في مكان واحد:
        الشرح المختصر المنظم، وروابط ملفات الدراسة، ومحتوى يوتيوب المقترح، ونظام اختبار ذكي متسلسل،
        ولوحة نتائج واضحة تساعد الطالب على معرفة مستواه الحقيقي بصورة احترافية.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ماذا تقدم المنصة؟")
        st.markdown("""
        <div class="lux-card">
            شرح مبسط ومنظم داخل نفس الواجهة، مع تقسيم المحتوى حسب المواد والوحدات، وإتاحة الوصول السريع للمعلومة من خلال البحث الذكي.
        </div>
        <div class="lux-card">
            ربط مباشر بملفات PDF وروابط Google Drive حتى يصبح الطالب قادرًا على الانتقال من الفهم إلى المراجعة دون تشتيت.
        </div>
        <div class="lux-card">
            مكتبة فيديوهات يوتيوب تعليمية تساعد على تثبيت الفهم وتوسيع الشرح من خلال المصادر المرئية.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("#### لماذا هذه الواجهة مختلفة؟")
        st.markdown("""
        <div class="lux-card">
            تم تصميم التجربة البصرية لتشعر الطالب أنه داخل منصة فاخرة لا داخل نموذج تقليدي، مع توازن بين الجمال والوضوح وسهولة الاستخدام.
        </div>
        <div class="lux-card">
            الألوان والخطوط والبطاقات والمؤشرات الزمنية كلها مصممة بحيث تعطي إحساسًا بالرقي والثقة والاحتراف.
        </div>
        <div class="lux-card">
            المنصة قابلة للتطوير بسهولة بإضافة مواد ووحدات جديدة وروابط أكثر وبنوك أسئلة أضخم.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# مركز الشرح
# =========================================================
elif page == "مركز الشرح":
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">مركز الشرح الدراسي</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">ملخصات تعليمية منظمة داخل المنصة تمهد للطالب الفهم السريع قبل الانتقال إلى الملفات أو الفيديوهات أو الاختبار.</div>', unsafe_allow_html=True)

    subject_filter = st.selectbox(
        "اختر المادة",
        ["الكل"] + sorted(list({x["subject"] for x in LESSON_SUMMARIES}))
    )

    filtered_lessons = LESSON_SUMMARIES if subject_filter == "الكل" else [x for x in LESSON_SUMMARIES if x["subject"] == subject_filter]

    for lesson in filtered_lessons:
        st.markdown(f"""
        <div class="lesson-card">
            <div class="lesson-title">{lesson['title']}</div>
            <div class="lesson-meta">المادة: {lesson['subject']} | الوحدة: {lesson['unit']}</div>
            <div class="small-note">{lesson['summary']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# مكتبة الملفات
# =========================================================
elif page == "مكتبة الملفات":
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">مكتبة الملفات التعليمية</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">اختر الملف المناسب للمادة أو الوحدة، وافتحه مباشرة أو قم بتحميله من خلال Google Drive.</div>', unsafe_allow_html=True)

    selected_pdf = st.selectbox(
        "اختر ملفًا من المكتبة",
        options=[item["title"] for item in PDF_RESOURCES]
    )
    pdf_item = next(item for item in PDF_RESOURCES if item["title"] == selected_pdf)

    st.markdown(f"""
    <div class="lesson-card">
        <div class="lesson-title">{pdf_item['title']}</div>
        <div class="lesson-meta">المادة: {pdf_item['subject']} | الوحدة: {pdf_item['unit']}</div>
        <div class="small-note">يمكن فتح المعاينة داخل المنصة أو تحميل الملف مباشرة من الرابط المتصل بـ Google Drive.</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.link_button("فتح المعاينة", to_gdrive_preview(pdf_item["drive_link"]))
    with c2:
        st.link_button("تحميل الملف", to_gdrive_download(pdf_item["drive_link"]))

    st.components.v1.html(
        f"""
        <iframe
            src="{to_gdrive_preview(pdf_item["drive_link"])}"
            width="100%"
            height="720"
            style="border:none;border-radius:18px;overflow:hidden;">
        </iframe>
        """,
        height=740,
        scrolling=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# مكتبة يوتيوب
# =========================================================
elif page == "مكتبة يوتيوب":
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">مكتبة فيديوهات يوتيوب التعليمية</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">فيديوهات مقترحة للدعم البصري والشرح الممتد. استبدل الروابط التجريبية بروابطك الفعلية للحصول على أفضل تجربة.</div>', unsafe_allow_html=True)

    selected_video = st.selectbox(
        "اختر الفيديو المناسب",
        options=[item["title"] for item in YOUTUBE_RESOURCES]
    )
    video_item = next(item for item in YOUTUBE_RESOURCES if item["title"] == selected_video)

    st.markdown(f"""
    <div class="youtube-card">
        <div class="yt-title">{video_item['title']}</div>
        <div class="yt-note">المادة: {video_item['subject']} | الوحدة: {video_item['unit']}</div>
        <div class="yt-note">{video_item['description']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.link_button("فتح الفيديو على يوتيوب", video_item["youtube_url"])

    st.video(video_item["youtube_url"])
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# الاختبار الذكي
# =========================================================
elif page == "الاختبار الذكي":
    if not st.session_state.quiz_started:
        st.markdown('<div class="section-shell">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">الاختبار الذكي المتسلسل</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="section-subtitle">
            هذا القسم يعمل بمنطق احترافي:
            سؤال واحد فقط في كل مرة، ولا يظهر زر السؤال التالي إلا بعد إرسال الإجابة،
            ولكل سؤال زمن خاص به، وإذا انتهى الوقت يتم الانتقال تلقائيًا للسؤال التالي.
        </div>
        """, unsafe_allow_html=True)

        if st.button("ابدأ الاختبار الآن"):
            reset_exam()
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        if st.session_state.exam_finished:
            st.markdown('<div class="section-shell">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">تم الانتهاء من الاختبار</div>', unsafe_allow_html=True)
            st.success("اكتمل الاختبار. يمكنك الآن الانتقال إلى لوحة النتائج للاطلاع على التقرير الكامل.")
            if st.button("إعادة الاختبار من البداية"):
                reset_exam()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            ensure_timer_for_current_question()

            idx = st.session_state.current_index
            q = st.session_state.questions[idx]
            total_questions = len(st.session_state.questions)

            time_limit = int(q.get("time_limit_sec", 60))
            seconds_left = max(0, int(st.session_state.deadline - time.time())) if st.session_state.deadline else time_limit

            try:
                @st.fragment(run_every="1s")
                def render_live_timer():
                    current_seconds_left = max(0, int(st.session_state.deadline - time.time())) if st.session_state.deadline else time_limit
                    if current_seconds_left <= 0 and not st.session_state.answer_submitted:
                        move_to_next_question(timeout_skip=True)
                        return

                    timer_class = get_timer_class(current_seconds_left, time_limit)
                    mins = current_seconds_left // 60
                    secs = current_seconds_left % 60
                    st.markdown(
                        f'<div class="timer-box {timer_class}">الوقت المتبقي: {mins:02d}:{secs:02d}</div>',
                        unsafe_allow_html=True
                    )

                render_live_timer()
            except Exception:
                timer_class = get_timer_class(seconds_left, time_limit)
                mins = seconds_left // 60
                secs = seconds_left % 60
                st.markdown(
                    f'<div class="timer-box {timer_class}">الوقت المتبقي: {mins:02d}:{secs:02d}</div>',
                    unsafe_allow_html=True
                )
                if seconds_left <= 0 and not st.session_state.answer_submitted:
                    move_to_next_question(timeout_skip=True)

            st.markdown('<div class="question-shell">', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="question-badge">السؤال {idx + 1} من {total_questions}</div>
                <div>
                    <span class="chip">{q['subject']}</span>
                    <span class="chip">{q['unit']}</span>
                    <span class="chip">درجة الصعوبة: {q['difficulty']}</span>
                    <span class="chip">الزمن: {q['time_limit_sec']} ثانية</span>
                </div>
                <div class="question-text">{q['question']}</div>
                """,
                unsafe_allow_html=True
            )

            choice_key = f"q_choice_{idx}"

            if not st.session_state.answer_submitted:
                selected = st.radio(
                    "اختر الإجابة الصحيحة",
                    options=q["options"],
                    key=choice_key,
                    index=None
                )

                c1, c2 = st.columns([2, 1])
                with c1:
                    submit_btn = st.button("إرسال الإجابة", disabled=selected is None)
                with c2:
                    st.info("لن يظهر زر السؤال التالي إلا بعد إرسال الإجابة.")

                if submit_btn and selected is not None:
                    submit_current_answer()
                    st.rerun()

            else:
                answer_record = st.session_state.answers.get(idx, {})
                is_correct = answer_record.get("is_correct", False)

                if is_correct:
                    st.markdown(
                        f'<div class="success-box">إجابة صحيحة ✅<br><br>التفسير: {q["explanation"]}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    correct_option_text = next(
                        (opt for opt in q["options"] if opt.startswith(q["answer"])),
                        f"{q['answer']})"
                    )
                    st.markdown(
                        f'<div class="error-box">إجابة غير صحيحة ❌<br><br>الإجابة الصحيحة: {correct_option_text}<br><br>التفسير: {q["explanation"]}</div>',
                        unsafe_allow_html=True
                    )

                if idx < total_questions - 1:
                    if st.button("السؤال التالي"):
                        move_to_next_question(timeout_skip=False)
                else:
                    if st.button("إنهاء الاختبار"):
                        st.session_state.exam_finished = True
                        st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-shell">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">مراجع مرتبطة بالسؤال الحالي</div>', unsafe_allow_html=True)

            related_pdf = [x for x in PDF_RESOURCES if normalize_text(x["subject"]) == normalize_text(q["subject"])]
            related_vid = [x for x in YOUTUBE_RESOURCES if normalize_text(x["subject"]) == normalize_text(q["subject"])]

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### ملف مقترح")
                if related_pdf:
                    item = related_pdf[0]
                    st.markdown(f"""
                    <div class="lesson-card">
                        <div class="lesson-title">{item['title']}</div>
                        <div class="lesson-meta">المادة: {item['subject']} | الوحدة: {item['unit']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.link_button("فتح الملف", to_gdrive_preview(item["drive_link"]))
                else:
                    st.info("لا يوجد ملف مرتبط بهذه المادة حاليًا.")

            with c2:
                st.markdown("#### فيديو مقترح")
                if related_vid:
                    item = related_vid[0]
                    st.markdown(f"""
                    <div class="youtube-card">
                        <div class="yt-title">{item['title']}</div>
                        <div class="yt-note">{item['description']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.link_button("فتح الفيديو", item["youtube_url"])
                else:
                    st.info("لا يوجد فيديو مرتبط بهذه المادة حاليًا.")

            st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# لوحة النتائج
# =========================================================
elif page == "لوحة النتائج":
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">لوحة النتائج والتقارير</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">تقرير تفصيلي يوضح أداء الطالب في الاختبار، مع إمكانية تحميل النتائج في ملف CSV.</div>', unsafe_allow_html=True)

    total = len(st.session_state.questions)
    all_answers = st.session_state.answers
    correct = sum(1 for a in all_answers.values() if a["is_correct"])
    incorrect = sum(1 for a in all_answers.values() if (not a["is_correct"] and not a.get("timed_out")))
    timed_out = sum(1 for a in all_answers.values() if a.get("timed_out"))
    score_percent = round((correct / total) * 100, 2) if total else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div style="font-size:1.8rem;font-weight:900;">{total}</div><div>إجمالي الأسئلة</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div style="font-size:1.8rem;font-weight:900;">{correct}</div><div>الإجابات الصحيحة</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div style="font-size:1.8rem;font-weight:900;">{incorrect}</div><div>الإجابات الخاطئة</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div style="font-size:1.8rem;font-weight:900;">{timed_out}</div><div>تخطي تلقائي</div></div>', unsafe_allow_html=True)

    st.progress(score_percent / 100)
    st.success(f"النسبة النهائية: {score_percent}%")

    report_rows = []
    for idx, q in enumerate(st.session_state.questions):
        a = all_answers.get(idx, {})
        report_rows.append({
            "رقم السؤال": idx + 1,
            "المادة": q["subject"],
            "الوحدة": q["unit"],
            "السؤال": q["question"],
            "إجابة الطالب": a.get("selected_letter"),
            "الإجابة الصحيحة": q["answer"],
            "النتيجة": "صحيح" if a.get("is_correct") else ("انتهى الوقت" if a.get("timed_out") else "خطأ")
        })

    df = pd.DataFrame(report_rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    csv_data = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "تحميل التقرير بصيغة CSV",
        data=csv_data,
        file_name="نتائج_المنصة_التعليمية_ادهم_صبري.csv",
        mime="text/csv"
    )

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# تذييل
# =========================================================
st.markdown("""
<div class="footer-note">
    هذه النسخة مصممة لتكون واجهة تعليمية فاخرة ومتكاملة وقابلة للتطوير.
    للحصول على التشغيل الفعلي الكامل، استبدل روابط Google Drive وروابط YouTube التجريبية بروابطك الحقيقية داخل الكود.
</div>
""", unsafe_allow_html=True)
