# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import math
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import streamlit as st

# =========================================================
# الهوية العامة
# =========================================================
APP_NAME = "المنصة التعليمية باقورة أعمال المهندس أدهم صبري"
APP_ICON = "👑"

JSON_QUESTIONS_FILE = "questions_bank.json"
XLSX_QUESTIONS_FILE = "arabic_questions_platform_upload.xlsx"

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# تنسيق فاخر
# =========================================================
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900;1000&display=swap');

        html, body, [class*="css"], [data-testid="stAppViewContainer"] {
            direction: rtl;
            text-align: right;
            font-family: 'Cairo', sans-serif !important;
        }

        .stApp {
            background:
                radial-gradient(circle at top right, rgba(59,130,246,0.18), transparent 22%),
                radial-gradient(circle at top left, rgba(251,191,36,0.10), transparent 18%),
                linear-gradient(180deg, #030712 0%, #081225 45%, #0b1932 100%);
            color: #f8fbff;
        }

        .block-container {
            max-width: 1450px;
            padding-top: 1.2rem;
            padding-bottom: 2rem;
        }

        .hero-box {
            position: relative;
            overflow: hidden;
            border-radius: 28px;
            padding: 28px 24px;
            background:
                linear-gradient(135deg, rgba(8,17,40,0.96), rgba(9,24,52,0.96)),
                radial-gradient(circle at 85% 20%, rgba(255,215,0,0.12), transparent 22%);
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 25px 60px rgba(0,0,0,0.34);
            margin-bottom: 20px;
        }

        .pill {
            display: inline-block;
            background: rgba(245, 158, 11, 0.12);
            border: 1px solid rgba(245, 158, 11, 0.35);
            color: #ffe7a7;
            padding: 8px 16px;
            border-radius: 999px;
            font-weight: 900;
            margin-bottom: 12px;
            font-size: 0.92rem;
        }

        .main-title {
            font-size: 2.4rem;
            font-weight: 1000;
            color: white;
            line-height: 1.6;
            margin-bottom: 8px;
            text-align: center;
        }

        .sub-title {
            text-align: center;
            font-size: 1.08rem;
            color: #d8e7ff;
            line-height: 1.9;
        }

        .info-card {
            background: rgba(9, 20, 45, 0.86);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 22px;
            padding: 18px;
            box-shadow: 0 14px 35px rgba(0,0,0,0.22);
            height: 100%;
        }

        .section-title {
            font-size: 1.45rem;
            font-weight: 1000;
            color: #fff3c2;
            margin: 10px 0 14px 0;
        }

        .minor {
            color: #bdd2ff;
            font-size: 0.96rem;
            line-height: 1.9;
        }

        .metric-box {
            background: linear-gradient(135deg, rgba(17,24,39,0.95), rgba(14,35,72,0.92));
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 16px;
            text-align: center;
            margin-bottom: 10px;
        }

        .metric-num {
            font-size: 1.8rem;
            font-weight: 1000;
            color: #ffffff;
        }

        .metric-label {
            color: #c6d6ff;
            font-weight: 700;
        }

        .question-shell {
            background: linear-gradient(180deg, rgba(8,18,40,0.98), rgba(9,24,52,0.95));
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 24px;
            padding: 22px;
            box-shadow: 0 18px 50px rgba(0,0,0,0.22);
            margin-top: 10px;
            margin-bottom: 16px;
        }

        .question-header {
            display: inline-block;
            padding: 8px 14px;
            background: rgba(59,130,246,0.16);
            border: 1px solid rgba(96,165,250,0.32);
            border-radius: 999px;
            color: #dbeafe;
            font-weight: 900;
            margin-bottom: 14px;
        }

        .question-text {
            font-size: 1.5rem;
            font-weight: 1000;
            color: #ffffff;
            line-height: 1.9;
            margin-bottom: 14px;
        }

        .small-badge {
            display: inline-block;
            margin-left: 8px;
            margin-bottom: 8px;
            padding: 6px 10px;
            border-radius: 999px;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.08);
            color: #dbeafe;
            font-size: 0.88rem;
            font-weight: 800;
        }

        .stButton > button {
            width: 100%;
            border-radius: 16px !important;
            font-weight: 900 !important;
            font-size: 1rem !important;
            border: 1px solid rgba(255,255,255,0.10) !important;
            padding: 0.7rem 1rem !important;
            background: linear-gradient(135deg, #0f3b8f, #1d4ed8) !important;
            color: white !important;
            box-shadow: 0 12px 28px rgba(29,78,216,0.22) !important;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            border-color: rgba(255,215,0,0.35) !important;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #050b17 0%, #091426 100%);
            border-left: 1px solid rgba(255,255,255,0.06);
        }

        [data-testid="stSidebar"] * {
            color: #f8fbff !important;
        }

        div[data-baseweb="radio"] label {
            background: rgba(16, 34, 68, 0.95) !important;
            border: 2px solid rgba(255, 215, 0, 0.28) !important;
            border-radius: 20px !important;
            padding: 16px 18px !important;
            margin-bottom: 12px !important;
        }

        div[data-baseweb="radio"] label:hover {
            background: rgba(23, 48, 93, 0.98) !important;
            border-color: rgba(255, 215, 0, 0.65) !important;
        }

        div[data-baseweb="radio"] label div {
            color: #ffffff !important;
            font-size: 1.18rem !important;
            font-weight: 1000 !important;
            line-height: 1.8 !important;
        }

        .result-good {
            background: rgba(22,163,74,0.16);
            border: 1px solid rgba(34,197,94,0.35);
            color: #dcfce7;
            padding: 16px;
            border-radius: 18px;
            font-weight: 800;
            line-height: 1.9;
            margin-top: 10px;
        }

        .result-bad {
            background: rgba(185,28,28,0.16);
            border: 1px solid rgba(248,113,113,0.35);
            color: #fee2e2;
            padding: 16px;
            border-radius: 18px;
            font-weight: 800;
            line-height: 1.9;
            margin-top: 10px;
        }

        .resource-card {
            background: rgba(8, 18, 40, 0.88);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 22px;
            padding: 18px;
            margin-bottom: 14px;
        }

        .resource-title {
            font-size: 1.12rem;
            font-weight: 1000;
            color: #fff;
            margin-bottom: 8px;
        }

        .resource-meta {
            color: #cfe0ff;
            font-size: 0.94rem;
            line-height: 1.9;
        }

        .footer-note {
            text-align: center;
            color: #a9c3ff;
            margin-top: 24px;
            font-size: 0.92rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# بيانات افتراضية تعليمية
# =========================================================
def get_default_lesson_summaries() -> List[Dict[str, str]]:
    return [
        {"subject": "الفيزياء", "unit": "الكهربية", "title": "قوانين كيرشوف", "summary": "شرح مبسط لقانوني الجهد والتيار مع خطوات تطبيق منظمة على الدوائر المركبة."},
        {"subject": "الفيزياء", "unit": "الضوء", "title": "الحيود والتداخل", "summary": "مقارنة دقيقة بين التداخل والحيود وأشهر صور المسائل الوزارية."},
        {"subject": "الرياضيات", "unit": "التكامل", "title": "التكامل بالتجزئة", "summary": "طريقة اختيار الدالة الأولى والثانية وأشهر التطبيقات على الأسية واللوغاريتمية."},
        {"subject": "الرياضيات", "unit": "التفاضل", "title": "النهايات والاتصال", "summary": "مراجعة مركزة على صور عدم التعيين وكيفية إثبات الاتصال."},
        {"subject": "الكيمياء", "unit": "الكيمياء العضوية", "title": "الهيدروكربونات", "summary": "تصنيف المركبات العضوية وعلاقات البنية بالتفاعل والخواص."},
        {"subject": "الكيمياء", "unit": "التحليل الكيميائي", "title": "المحاليل والاتزان", "summary": "توضيح مفاهيم الاتزان وثابت الاتزان والعوامل المؤثرة عليه."},
        {"subject": "الأحياء", "unit": "الوراثة", "title": "الشفرة الوراثية", "summary": "العلاقة بين DNA وRNA والبروتين مع خطوات الترجمة والنسخ."},
        {"subject": "الأحياء", "unit": "التكاثر", "title": "الانقسام الميوزي", "summary": "الفروق الجوهرية بين الانقسامين الميتوزي والميوزي في نقاط مركزة."},
        {"subject": "اللغة العربية", "unit": "البلاغة", "title": "التشبيه والاستعارة", "summary": "تمييز الصور البلاغية وكيفية استخراج الأثر الفني في الامتحان."},
        {"subject": "اللغة العربية", "unit": "النحو", "title": "أسلوب النداء", "summary": "أنواع المنادى وأحكام بنائه وإعرابه بطريقة امتحانية واضحة."},
        {"subject": "اللغة الإنجليزية", "unit": "Grammar", "title": "Reported Speech", "summary": "شرح تحويل الكلام المباشر إلى غير مباشر مع أهم الأفعال المساعدة والزمن."},
        {"subject": "اللغة الإنجليزية", "unit": "Reading", "title": "Reading Comprehension", "summary": "طريقة التعامل مع القطعة واستخراج الفكرة الرئيسية والمرادفات والإجابات الدقيقة."},
    ]


def get_default_pdf_resources() -> List[Dict[str, Any]]:
    return [
        {"title": "ملف الفيزياء 1 - قوانين كيرشوف", "subject": "الفيزياء", "unit": "الكهربية", "keywords": ["فيزياء", "كيرشوف", "دوائر", "جهد"], "drive_link": "https://drive.google.com/file/d/1xlzPmrUqCAR7XF4ZaBAFN6WhbvZum3_d/view?usp=drivesdk"},
        {"title": "ملف الفيزياء 2 - الحيود والتداخل", "subject": "الفيزياء", "unit": "الضوء", "keywords": ["فيزياء", "حيود", "تداخل"], "drive_link": "https://drive.google.com/file/d/1BQec3wMImmlX-Y82Ll8ppgMFr6N3aQuP/view?usp=drivesdk"},
        {"title": "ملف الرياضيات 1 - التكامل الأساسي", "subject": "الرياضيات", "unit": "التكامل", "keywords": ["رياضيات", "تكامل", "قواعد"], "drive_link": "https://drive.google.com/file/d/1TqlGSQ7__r2er05lfqAi1B2kdIrspXui/view?usp=drivesdk"},
        {"title": "ملف الرياضيات 2 - التكامل بالتجزئة", "subject": "الرياضيات", "unit": "التكامل بالتجزئة", "keywords": ["رياضيات", "تكامل", "تجزئة"], "drive_link": "https://drive.google.com/file/d/1Om2_yLrF1btqqr73JOdpAVewL47-BuW8/view?usp=drivesdk"},
        {"title": "ملف الكيمياء 1 - التركيب الذري", "subject": "الكيمياء", "unit": "التركيب الذري", "keywords": ["كيمياء", "ذرة", "إلكترون"], "drive_link": "https://drive.google.com/file/d/1uo6ZDwqV0CeN9MatZRfk79N07crJ3Gxw/view?usp=drivesdk"},
        {"title": "ملف الأحياء 1 - الوراثة", "subject": "الأحياء", "unit": "الوراثة", "keywords": ["أحياء", "DNA", "جينات"], "drive_link": "https://drive.google.com/file/d/1Vn6PQyoyEgvLGf7QB-l75tg_phNIQNDq/view?usp=drivesdk"},
        {"title": "ملف اللغة الإنجليزية 1 - Grammar", "subject": "اللغة الإنجليزية", "unit": "Grammar", "keywords": ["English", "Grammar", "Reported Speech"], "drive_link": "https://drive.google.com/file/d/1QjUZknxo9rp8/view?usp=drivesdk"},
    ]


def get_default_youtube_resources() -> List[Dict[str, Any]]:
    return [
        {"title": "شرح قوانين كيرشوف", "subject": "الفيزياء", "unit": "الكهربية", "description": "فيديو تأسيسي لحل المسائل المركبة خطوة بخطوة.", "url": "https://www.youtube.com/results?search_query=شرح+قوانين+كيرشوف+ثالثة+ثانوي", "keywords": ["فيزياء", "كيرشوف", "كهربية"]},
        {"title": "شرح التكامل بالتجزئة", "subject": "الرياضيات", "unit": "التكامل", "description": "مراجعة عملية على أشهر الأفكار الوزارية.", "url": "https://www.youtube.com/results?search_query=شرح+التكامل+بالتجزئة+ثالثة+ثانوي", "keywords": ["رياضيات", "تكامل", "تجزئة"]},
        {"title": "شرح الاتزان الكيميائي", "subject": "الكيمياء", "unit": "الاتزان", "description": "فهم سريع للمفاهيم والقوانين والتطبيقات.", "url": "https://www.youtube.com/results?search_query=شرح+الاتزان+الكيميائي+ثالثة+ثانوي", "keywords": ["كيمياء", "اتزان"]},
        {"title": "شرح الوراثة", "subject": "الأحياء", "unit": "الوراثة", "description": "تلخيص شامل ومراجعة للفصل.", "url": "https://www.youtube.com/results?search_query=شرح+الوراثة+ثالثة+ثانوي", "keywords": ["أحياء", "وراثة"]},
        {"title": "شرح البلاغة", "subject": "اللغة العربية", "unit": "البلاغة", "description": "تبسيط الصور البلاغية وأثرها الفني.", "url": "https://www.youtube.com/results?search_query=شرح+البلاغة+ثالثة+ثانوي", "keywords": ["عربي", "بلاغة"]},
        {"title": "English Grammar Review", "subject": "اللغة الإنجليزية", "unit": "Grammar", "description": "شرح مركز لقواعد ثالثة ثانوي.", "url": "https://www.youtube.com/results?search_query=english+grammar+third+secondary+egypt", "keywords": ["English", "Grammar", "Third Secondary"]},
    ]


def make_question(
    subject: str,
    unit: str,
    difficulty: str,
    question: str,
    options: List[str],
    answer: str,
    explanation: str,
    time_limit_sec: int,
) -> Dict[str, Any]:
    return {
        "subject": subject,
        "unit": unit,
        "difficulty": difficulty,
        "question": question,
        "options": options,
        "answer": answer,
        "explanation": explanation,
        "time_limit_sec": time_limit_sec,
    }


def get_default_questions() -> List[Dict[str, Any]]:
    return [
        make_question("الفيزياء", "الكهربية", "متوسط", "في دائرة كهربية مغلقة، مجموع فروق الجهد حول أي مسار مغلق يساوي:", ["أ) صفر", "ب) واحد", "ج) المقاومة الكلية", "د) شدة التيار"], "أ", "هذا هو مضمون قانون كيرشوف الثاني للجهد.", 60),
        make_question("الفيزياء", "الضوء", "متوسط", "عند زيادة عرض الشق في تجربة الحيود فإن أهداب الحيود:", ["أ) تتسع", "ب) تضيق", "ج) تختفي فورًا", "د) لا تتغير"], "ب", "يزداد عرض الشق فيقل اتساع الهدب المركزي والحيود عمومًا.", 60),
        make_question("الرياضيات", "التكامل", "سهل", "تكامل 2x بالنسبة إلى x يساوي:", ["أ) x² + ثابت", "ب) 2x² + ثابت", "ج) x + ثابت", "د) 2 + ثابت"], "أ", "لأن تكامل x^n يساوي x^(n+1)/(n+1).", 50),
        make_question("الرياضيات", "التكامل بالتجزئة", "صعب", "أي الصيغ الآتية تمثل قاعدة التكامل بالتجزئة؟", ["أ) ∫u dv = uv - ∫v du", "ب) ∫u dv = uv + ∫v du", "ج) ∫u dv = du/dv", "د) ∫u dv = u+v"], "أ", "القاعدة الصحيحة هي حاصل الضرب ناقص تكامل الجزء المتبقي.", 70),
        make_question("الكيمياء", "التركيب الذري", "سهل", "الجسيم المسؤول عن تحديد نوع العنصر هو:", ["أ) الإلكترون", "ب) البروتون", "ج) النيوترون", "د) الفوتون"], "ب", "عدد البروتونات هو العدد الذري الذي يحدد نوع العنصر.", 50),
        make_question("الكيمياء", "الاتزان", "متوسط", "العامل الذي لا يؤثر في ثابت الاتزان هو:", ["أ) درجة الحرارة", "ب) طبيعة المواد", "ج) تركيز المواد عند لحظة القياس", "د) اتجاه التفاعل"], "ج", "ثابت الاتزان يتغير مع الحرارة فقط بينما تراكيز اللحظة لا تغير قيمته.", 65),
        make_question("الأحياء", "الوراثة", "متوسط", "يحمل DNA الشفرة الوراثية في صورة:", ["أ) أحماض أمينية", "ب) قواعد نيتروجينية مرتبة", "ج) دهون فسفورية", "د) سكريات أحادية"], "ب", "ترتيب القواعد النيتروجينية هو الذي يحمل المعلومات الوراثية.", 60),
        make_question("الأحياء", "الانقسام", "متوسط", "الانقسام الميوزي يتميز بأنه:", ["أ) ينتج خليتين متماثلتين", "ب) يحافظ على العدد الكروموسومي", "ج) يخفض العدد الكروموسومي إلى النصف", "د) يحدث في الخلايا الجسدية فقط"], "ج", "الانقسام الميوزي اختزالي ويخفض العدد إلى النصف.", 60),
        make_question("اللغة العربية", "البلاغة", "متوسط", "في قولنا: العلم نور، الصورة البيانية هي:", ["أ) كناية", "ب) استعارة تصريحية", "ج) مجاز مرسل", "د) تشبيه تمثيلي"], "ب", "شبه العلم بالنور وصرح بالمشبه به وحذف المشبه.", 55),
        make_question("اللغة العربية", "النحو", "سهل", "أي الجمل التالية تمثل أسلوب نداء؟", ["أ) ما أجمل الصدق", "ب) يا طالبُ اجتهد", "ج) لن أهمل الواجب", "د) هل حضرت اليوم"], "ب", "وجود أداة النداء يا يدل على أسلوب النداء.", 50),
        make_question("اللغة الإنجليزية", "Grammar", "متوسط", "Choose the correct answer: If he studies hard, he ___ the exam.", ["A) pass", "B) passed", "C) will pass", "D) passing"], "C", "This is a first conditional sentence, so the correct form is will pass.", 55),
        make_question("اللغة الإنجليزية", "Reading", "متوسط", "The best title for a reading passage should usually express the:", ["A) smallest detail", "B) main idea", "C) writer's name", "D) hardest word"], "B", "A good title reflects the main idea of the whole passage.", 55),
    ]


# =========================================================
# أدوات مساعدة
# =========================================================
def normalize_text(text: Any) -> str:
    text = "" if text is None else str(text)
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_subject_name(subject: str) -> str:
    s = normalize_text(subject).lower()

    mapping = {
        "english": "اللغة الإنجليزية",
        "english language": "اللغة الإنجليزية",
        "لغة انجليزية": "اللغة الإنجليزية",
        "لغة إنجليزية": "اللغة الإنجليزية",
        "انجليزي": "اللغة الإنجليزية",
        "انجليزى": "اللغة الإنجليزية",
        "الانجليزي": "اللغة الإنجليزية",
        "الانجليزى": "اللغة الإنجليزية",
        "اللغة الانجليزية": "اللغة الإنجليزية",
        "اللغة الانجليزيه": "اللغة الإنجليزية",
        "اللغة الإنجليزية": "اللغة الإنجليزية",

        "arabic": "اللغة العربية",
        "اللغة العربية": "اللغة العربية",
        "عربي": "اللغة العربية",

        "math": "الرياضيات",
        "mathematics": "الرياضيات",
        "رياضيات": "الرياضيات",

        "physics": "الفيزياء",
        "فيزياء": "الفيزياء",

        "chemistry": "الكيمياء",
        "كيمياء": "الكيمياء",

        "biology": "الأحياء",
        "احياء": "الأحياء",
        "أحياء": "الأحياء",
    }

    return mapping.get(s, normalize_text(subject))


def answer_to_arabic_letter(value: str) -> Optional[str]:
    v = normalize_text(value).upper()
    answer_map = {
        "A": "أ",
        "B": "ب",
        "C": "ج",
        "D": "د",
        "أ": "أ",
        "ب": "ب",
        "ج": "ج",
        "د": "د",
        "1": "أ",
        "2": "ب",
        "3": "ج",
        "4": "د",
    }
    return answer_map.get(v)


def clean_option_prefix(text: str) -> str:
    t = normalize_text(text)
    t = re.sub(r"^[A-Dأبجدهـ]\s*[\)\-:\.]?\s*", "", t, flags=re.IGNORECASE)
    return t.strip()


def format_option(letter: str, text: str) -> str:
    return f"{letter}) {clean_option_prefix(text)}"


def infer_answer_letter_from_text(answer_value: str, options: List[str]) -> Optional[str]:
    direct = answer_to_arabic_letter(answer_value)
    if direct:
        return direct

    cleaned_answer = clean_option_prefix(answer_value)
    letters = ["أ", "ب", "ج", "د"]

    for idx, opt in enumerate(options):
        if clean_option_prefix(opt) == cleaned_answer:
            return letters[idx]

    return None


def validate_question_item(item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    required_keys = ["subject", "unit", "difficulty", "question", "options", "answer", "explanation", "time_limit_sec"]
    if not isinstance(item, dict):
        return None

    if not all(k in item for k in required_keys):
        return None

    subject = normalize_subject_name(item["subject"])
    unit = normalize_text(item["unit"])
    difficulty = normalize_text(item["difficulty"])
    question = normalize_text(item["question"])
    explanation = normalize_text(item["explanation"])

    raw_options = item["options"]
    if not isinstance(raw_options, list) or len(raw_options) != 4:
        return None

    options = [
        format_option("أ", raw_options[0]),
        format_option("ب", raw_options[1]),
        format_option("ج", raw_options[2]),
        format_option("د", raw_options[3]),
    ]

    answer = infer_answer_letter_from_text(item["answer"], options)
    if not answer:
        return None

    try:
        time_limit_sec = int(float(item["time_limit_sec"]))
        if time_limit_sec <= 0:
            time_limit_sec = 60
    except Exception:
        time_limit_sec = 60

    if not all([subject, unit, difficulty, question, explanation]):
        return None

    return {
        "subject": subject,
        "unit": unit,
        "difficulty": difficulty,
        "question": question,
        "options": options,
        "answer": answer,
        "explanation": explanation,
        "time_limit_sec": time_limit_sec,
    }


# =========================================================
# تحميل بنك الأسئلة
# =========================================================
def load_questions_from_json(file_path: str) -> List[Dict[str, Any]]:
    path = Path(file_path)
    if not path.exists():
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception:
        return []

    if not isinstance(raw, list):
        return []

    result = []
    for item in raw:
        valid = validate_question_item(item)
        if valid:
            result.append(valid)
    return result


def load_questions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    path = Path(file_path)
    if not path.exists():
        return []

    try:
        df = pd.read_excel(path)
    except Exception:
        return []

    if df.empty:
        return []

    df.columns = [normalize_text(col).lower() for col in df.columns]

    required_cols = [
        "subject", "unit", "difficulty", "question",
        "option_a", "option_b", "option_c", "option_d",
        "answer", "explanation", "time_limit_sec"
    ]

    if not all(col in df.columns for col in required_cols):
        return []

    questions: List[Dict[str, Any]] = []

    for _, row in df.iterrows():
        item = {
            "subject": row.get("subject", ""),
            "unit": row.get("unit", ""),
            "difficulty": row.get("difficulty", ""),
            "question": row.get("question", ""),
            "options": [
                row.get("option_a", ""),
                row.get("option_b", ""),
                row.get("option_c", ""),
                row.get("option_d", ""),
            ],
            "answer": row.get("answer", ""),
            "explanation": row.get("explanation", ""),
            "time_limit_sec": row.get("time_limit_sec", 60),
        }
        valid = validate_question_item(item)
        if valid:
            questions.append(valid)

    return questions


def get_questions() -> List[Dict[str, Any]]:
    json_questions = load_questions_from_json(JSON_QUESTIONS_FILE)
    if json_questions:
        return json_questions

    excel_questions = load_questions_from_excel(XLSX_QUESTIONS_FILE)
    if excel_questions:
        return excel_questions

    return get_default_questions()


# =========================================================
# البحث الذكي
# =========================================================
def smart_match_score(query: str, haystack: str) -> float:
    q = normalize_text(query).lower()
    h = normalize_text(haystack).lower()

    if not q or not h:
        return 0.0

    score = 0.0

    if q in h:
        score += 5.0

    q_words = [w for w in re.split(r"\s+", q) if w]
    if not q_words:
        return score

    for word in q_words:
        if word in h:
            score += 1.5

    return score


def run_search(
    query: str,
    lesson_summaries: List[Dict[str, Any]],
    pdf_resources: List[Dict[str, Any]],
    youtube_resources: List[Dict[str, Any]],
    questions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    query = normalize_text(query)
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
# إدارة الحالة
# =========================================================
def init_state() -> None:
    if "questions" not in st.session_state:
        st.session_state.questions = get_questions()

    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False

    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    if "answers" not in st.session_state:
        st.session_state.answers = {}

    if "selected_subject" not in st.session_state:
        st.session_state.selected_subject = None

    if "selected_difficulty" not in st.session_state:
        st.session_state.selected_difficulty = "الكل"

    if "selected_unit" not in st.session_state:
        st.session_state.selected_unit = "الكل"

    if "filtered_questions" not in st.session_state:
        st.session_state.filtered_questions = []

    if "answer_submitted" not in st.session_state:
        st.session_state.answer_submitted = False

    if "last_result" not in st.session_state:
        st.session_state.last_result = None

    if "deadline" not in st.session_state:
        st.session_state.deadline = None

    if "question_started_at" not in st.session_state:
        st.session_state.question_started_at = None

    if "exam_finished" not in st.session_state:
        st.session_state.exam_finished = False

    if "auto_skipped" not in st.session_state:
        st.session_state.auto_skipped = []

    if "quiz_seed" not in st.session_state:
        st.session_state.quiz_seed = int(time.time())


def reset_exam_runtime_state() -> None:
    st.session_state.quiz_started = False
    st.session_state.current_index = 0
    st.session_state.answers = {}
    st.session_state.filtered_questions = []
    st.session_state.answer_submitted = False
    st.session_state.last_result = None
    st.session_state.deadline = None
    st.session_state.question_started_at = None
    st.session_state.exam_finished = False
    st.session_state.auto_skipped = []
    st.session_state.quiz_seed = int(time.time())


def start_exam(filtered_questions: List[Dict[str, Any]]) -> None:
    st.session_state.filtered_questions = filtered_questions
    st.session_state.quiz_started = True
    st.session_state.current_index = 0
    st.session_state.answers = {}
    st.session_state.answer_submitted = False
    st.session_state.last_result = None
    st.session_state.exam_finished = False
    st.session_state.auto_skipped = []
    st.session_state.question_started_at = time.time()
    if filtered_questions:
        st.session_state.deadline = time.time() + filtered_questions[0]["time_limit_sec"]
    else:
        st.session_state.deadline = None


def set_next_question_deadline() -> None:
    questions = st.session_state.filtered_questions
    idx = st.session_state.current_index

    if 0 <= idx < len(questions):
        st.session_state.question_started_at = time.time()
        st.session_state.deadline = time.time() + questions[idx]["time_limit_sec"]
        st.session_state.answer_submitted = False
        st.session_state.last_result = None
    else:
        st.session_state.deadline = None
        st.session_state.question_started_at = None


# =========================================================
# مساعدات الامتحان
# =========================================================
def filter_questions(
    questions: List[Dict[str, Any]],
    subject: Optional[str],
    difficulty: str = "الكل",
    unit: str = "الكل",
) -> List[Dict[str, Any]]:
    result = questions[:]

    if subject:
        result = [q for q in result if q["subject"] == subject]

    if difficulty != "الكل":
        result = [q for q in result if q["difficulty"] == difficulty]

    if unit != "الكل":
        result = [q for q in result if q["unit"] == unit]

    return result


def get_subjects(questions: List[Dict[str, Any]]) -> List[str]:
    subjects = sorted(list({normalize_subject_name(q["subject"]) for q in questions}))
    return subjects


def get_units_for_subject(questions: List[Dict[str, Any]], subject: str) -> List[str]:
    units = sorted(list({q["unit"] for q in questions if q["subject"] == subject}))
    return units


def get_difficulties(questions: List[Dict[str, Any]]) -> List[str]:
    order = ["سهل", "متوسط", "صعب"]
    found = list({q["difficulty"] for q in questions})
    result = [d for d in order if d in found]
    for item in found:
        if item not in result:
            result.append(item)
    return result


def get_correct_option_text(question: Dict[str, Any]) -> str:
    letters = ["أ", "ب", "ج", "د"]
    idx = letters.index(question["answer"])
    return question["options"][idx]


def get_selected_letter_from_option(selected_option: str) -> Optional[str]:
    value = normalize_text(selected_option)
    match = re.match(r"^([أبجد]|[A-D])\)", value, flags=re.IGNORECASE)
    if not match:
        return None

    raw = match.group(1).upper()
    if raw == "A":
        return "أ"
    if raw == "B":
        return "ب"
    if raw == "C":
        return "ج"
    if raw == "D":
        return "د"

    return raw


def calculate_score(questions: List[Dict[str, Any]], answers: Dict[int, Dict[str, Any]]) -> Dict[str, Any]:
    total = len(questions)
    correct = 0
    wrong = 0
    skipped = 0

    for idx, q in enumerate(questions):
        info = answers.get(idx)
        if not info:
            skipped += 1
            continue

        if info.get("status") == "correct":
            correct += 1
        elif info.get("status") == "wrong":
            wrong += 1
        else:
            skipped += 1

    percent = round((correct / total) * 100, 2) if total else 0.0

    return {
        "total": total,
        "correct": correct,
        "wrong": wrong,
        "skipped": skipped,
        "percent": percent,
    }


# =========================================================
# واجهات العرض
# =========================================================
def render_header(questions: List[Dict[str, Any]]) -> None:
    subjects = get_subjects(questions)
    st.markdown(
        f"""
        <div class="hero-box">
            <div class="pill">منصة تعليمية عربية احترافية لطلاب الثانوية العامة</div>
            <div class="main-title">{APP_NAME}</div>
            <div class="sub-title">
                شرح تفصيلي للمناهج، بنك أسئلة احترافي، اختبارات تفاعلية سؤالًا بسؤال، روابط تعليمية، وبحث ذكي داخل المحتوى.
                <br>
                تم تحميل <b>{len(questions)}</b> سؤالاً عبر بنك الأسئلة الحالي، وتشمل المواد المتاحة الآن <b>{len(subjects)}</b> مادة.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard(
    questions: List[Dict[str, Any]],
    lessons: List[Dict[str, Any]],
    pdfs: List[Dict[str, Any]],
    videos: List[Dict[str, Any]],
) -> None:
    st.markdown('<div class="section-title">لوحة المنصة</div>', unsafe_allow_html=True)

    subjects = get_subjects(questions)
    english_count = len([q for q in questions if q["subject"] == "اللغة الإنجليزية"])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-box"><div class="metric-num">{len(questions)}</div><div class="metric-label">إجمالي الأسئلة</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-box"><div class="metric-num">{len(subjects)}</div><div class="metric-label">عدد المواد</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-box"><div class="metric-num">{len(lessons)}</div><div class="metric-label">ملخصات تعليمية</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-box"><div class="metric-num">{english_count}</div><div class="metric-label">أسئلة الإنجليزي</div></div>', unsafe_allow_html=True)

    left, right = st.columns([1.1, 1])
    with left:
        st.markdown(
            """
            <div class="info-card">
                <div class="section-title">ماذا تقدم المنصة؟</div>
                <div class="minor">
                    المنصة مصممة لتكون بيئة تعليمية راقية لطلاب الثانوية العامة، وتجمع بين الشرح المختصر عالي الجودة، وبنك أسئلة منظم،
                    واختبارات تفاعلية سؤالًا بعد سؤال، مع إظهار النتيجة فورًا وشرح الإجابة الصحيحة بشكل واضح.
                    كما تدعم تحميل بنك الأسئلة من ملف Excel بصيغة تعليمية قياسية.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        joined_subjects = " - ".join(subjects) if subjects else "لا توجد مواد"
        st.markdown(
            f"""
            <div class="info-card">
                <div class="section-title">المواد الحالية</div>
                <div class="minor">{joined_subjects}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title">أبرز الموارد التعليمية</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, item in enumerate(pdfs[:3]):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="resource-card">
                    <div class="resource-title">{item['title']}</div>
                    <div class="resource-meta">
                        المادة: {item['subject']}<br>
                        الوحدة: {item['unit']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_library(
    lessons: List[Dict[str, Any]],
    pdfs: List[Dict[str, Any]],
    videos: List[Dict[str, Any]],
) -> None:
    st.markdown('<div class="section-title">المكتبة التعليمية</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["الملخصات", "ملفات PDF", "روابط الشرح"])

    with tab1:
        for item in lessons:
            st.markdown(
                f"""
                <div class="resource-card">
                    <div class="resource-title">{item['title']}</div>
                    <div class="resource-meta">
                        المادة: {item['subject']}<br>
                        الوحدة: {item['unit']}<br>
                        الملخص: {item['summary']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab2:
        for item in pdfs:
            st.markdown(
                f"""
                <div class="resource-card">
                    <div class="resource-title">{item['title']}</div>
                    <div class="resource-meta">
                        المادة: {item['subject']}<br>
                        الوحدة: {item['unit']}<br>
                        الكلمات المفتاحية: {", ".join(item["keywords"])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.link_button("فتح الملف", item["drive_link"])

    with tab3:
        for item in videos:
            st.markdown(
                f"""
                <div class="resource-card">
                    <div class="resource-title">{item['title']}</div>
                    <div class="resource-meta">
                        المادة: {item['subject']}<br>
                        الوحدة: {item['unit']}<br>
                        الوصف: {item['description']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.link_button("فتح الشرح", item["url"])


def render_search(
    lessons: List[Dict[str, Any]],
    pdfs: List[Dict[str, Any]],
    videos: List[Dict[str, Any]],
    questions: List[Dict[str, Any]],
) -> None:
    st.markdown('<div class="section-title">البحث الذكي</div>', unsafe_allow_html=True)

    query = st.text_input("اكتب كلمة أو موضوعًا للبحث داخل الشرح والملفات والأسئلة")

    if not query.strip():
        st.info("اكتب كلمة مثل: كيرشوف - التكامل - grammar - الوراثة - البلاغة")
        return

    results = run_search(query, lessons, pdfs, videos, questions)

    t1, t2, t3, t4 = st.tabs(["الملخصات", "الملفات", "الفيديوهات", "الأسئلة"])

    with t1:
        if results["lessons"]:
            for item in results["lessons"]:
                st.markdown(
                    f"""
                    <div class="resource-card">
                        <div class="resource-title">{item['title']}</div>
                        <div class="resource-meta">{item['summary']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.warning("لا توجد نتائج في الملخصات.")

    with t2:
        if results["pdfs"]:
            for item in results["pdfs"]:
                st.markdown(
                    f"""
                    <div class="resource-card">
                        <div class="resource-title">{item['title']}</div>
                        <div class="resource-meta">المادة: {item['subject']} | الوحدة: {item['unit']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.link_button("فتح الملف", item["drive_link"], key=f"pdf_{item['title']}")
        else:
            st.warning("لا توجد نتائج في الملفات.")

    with t3:
        if results["youtube"]:
            for item in results["youtube"]:
                st.markdown(
                    f"""
                    <div class="resource-card">
                        <div class="resource-title">{item['title']}</div>
                        <div class="resource-meta">{item['description']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.link_button("فتح الشرح", item["url"], key=f"yt_{item['title']}")
        else:
            st.warning("لا توجد نتائج في الفيديوهات.")

    with t4:
        if results["questions"]:
            for item in results["questions"]:
                st.markdown(
                    f"""
                    <div class="resource-card">
                        <div class="resource-title">{item['question']}</div>
                        <div class="resource-meta">
                            المادة: {item['subject']} | الوحدة: {item['unit']} | المستوى: {item['difficulty']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.warning("لا توجد نتائج في الأسئلة.")


def render_exam_setup(questions: List[Dict[str, Any]]) -> None:
    st.markdown('<div class="section-title">الاختبارات التفاعلية</div>', unsafe_allow_html=True)

    if not questions:
        st.error("لا توجد أسئلة متاحة حاليًا.")
        return

    subjects = get_subjects(questions)
    if not subjects:
        st.error("تعذر استخراج المواد من بنك الأسئلة.")
        return

    default_subject = "اللغة الإنجليزية" if "اللغة الإنجليزية" in subjects else subjects[0]

    selected_subject = st.selectbox(
        "اختر المادة",
        subjects,
        index=subjects.index(default_subject),
        key="subject_selector",
    )

    subject_units = get_units_for_subject(questions, selected_subject)
    difficulty_options = ["الكل"] + get_difficulties(questions)
    unit_options = ["الكل"] + subject_units

    c1, c2 = st.columns(2)
    with c1:
        selected_difficulty = st.selectbox("اختر مستوى الصعوبة", difficulty_options, key="difficulty_selector")
    with c2:
        selected_unit = st.selectbox("اختر الوحدة", unit_options, key="unit_selector")

    filtered = filter_questions(
        questions=questions,
        subject=selected_subject,
        difficulty=selected_difficulty,
        unit=selected_unit,
    )

    c3, c4, c5 = st.columns(3)
    with c3:
        st.markdown(f'<div class="metric-box"><div class="metric-num">{len(filtered)}</div><div class="metric-label">الأسئلة المتاحة</div></div>', unsafe_allow_html=True)
    with c4:
        english_count = len([q for q in questions if q["subject"] == "اللغة الإنجليزية"])
        st.markdown(f'<div class="metric-box"><div class="metric-num">{english_count}</div><div class="metric-label">إجمالي أسئلة الإنجليزي</div></div>', unsafe_allow_html=True)
    with c5:
        st.markdown(f'<div class="metric-box"><div class="metric-num">{len(subjects)}</div><div class="metric-label">المواد المتاحة</div></div>', unsafe_allow_html=True)

    if selected_subject == "اللغة الإنجليزية" and len(filtered) == 0:
        st.error("مادة اللغة الإنجليزية موجودة في الاختيارات لكن لا توجد أسئلة مطابقة للفلتر الحالي. غيّر الوحدة أو الصعوبة إلى الكل.")
        return

    if len(filtered) == 0:
        st.warning("لا توجد أسئلة مطابقة للاختيار الحالي.")
        return

    if st.button("ابدأ الاختبار الآن", key="start_exam_btn"):
        start_exam(filtered)
        st.rerun()


def render_current_question() -> None:
    questions = st.session_state.filtered_questions
    idx = st.session_state.current_index

    if idx >= len(questions):
        st.session_state.exam_finished = True
        return

    q = questions[idx]

    if st.session_state.deadline is None:
        set_next_question_deadline()

    now = time.time()
    remaining = max(0, int(st.session_state.deadline - now)) if st.session_state.deadline else q["time_limit_sec"]

    st.markdown(
        f"""
        <div class="question-shell">
            <div class="question-header">السؤال {idx + 1} من {len(questions)}</div>
            <div>
                <span class="small-badge">المادة: {q['subject']}</span>
                <span class="small-badge">الوحدة: {q['unit']}</span>
                <span class="small-badge">المستوى: {q['difficulty']}</span>
                <span class="small-badge">الوقت: {q['time_limit_sec']} ثانية</span>
                <span class="small-badge">المتبقي: {remaining} ثانية</span>
            </div>
            <div class="question-text">{q['question']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if remaining <= 0 and not st.session_state.answer_submitted:
        st.session_state.answers[idx] = {
            "selected_option": None,
            "selected_letter": None,
            "correct_letter": q["answer"],
            "status": "skipped",
            "explanation": q["explanation"],
            "auto": True,
        }
        st.session_state.answer_submitted = True
        st.session_state.last_result = {
            "status": "skipped",
            "message": "انتهى الوقت لهذا السؤال وتم اعتباره غير مجاب.",
            "correct_option": get_correct_option_text(q),
            "explanation": q["explanation"],
        }
        st.session_state.auto_skipped.append(idx)

    choice_key = f"choice_{idx}"

    if not st.session_state.answer_submitted:
        selected_option = st.radio(
            "اختر الإجابة الصحيحة",
            options=q["options"],
            key=choice_key,
        )

        c1, c2 = st.columns([1.2, 1])
        with c1:
            if st.button("تأكيد الإجابة", key=f"submit_{idx}"):
                selected_letter = get_selected_letter_from_option(selected_option)
                is_correct = selected_letter == q["answer"]

                st.session_state.answers[idx] = {
                    "selected_option": selected_option,
                    "selected_letter": selected_letter,
                    "correct_letter": q["answer"],
                    "status": "correct" if is_correct else "wrong",
                    "explanation": q["explanation"],
                    "auto": False,
                }

                st.session_state.answer_submitted = True
                st.session_state.last_result = {
                    "status": "correct" if is_correct else "wrong",
                    "message": "إجابة صحيحة ممتازة." if is_correct else "إجابة غير صحيحة.",
                    "correct_option": get_correct_option_text(q),
                    "explanation": q["explanation"],
                }
                st.rerun()

        with c2:
            if st.button("إنهاء الاختبار الآن", key=f"finish_now_{idx}"):
                st.session_state.exam_finished = True
                st.rerun()

    if st.session_state.answer_submitted and st.session_state.last_result:
        result = st.session_state.last_result
        css_class = "result-good" if result["status"] == "correct" else "result-bad"

        st.markdown(
            f"""
            <div class="{css_class}">
                {result["message"]}<br><br>
                الإجابة الصحيحة: {result["correct_option"]}<br><br>
                الشرح: {result["explanation"]}
            </div>
            """,
            unsafe_allow_html=True,
        )

        c3, c4 = st.columns(2)
        with c3:
            if idx < len(questions) - 1:
                if st.button("السؤال التالي", key=f"next_{idx}"):
                    st.session_state.current_index += 1
                    set_next_question_deadline()
                    st.rerun()
            else:
                if st.button("عرض النتيجة النهائية", key=f"final_result_{idx}"):
                    st.session_state.exam_finished = True
                    st.rerun()

        with c4:
            if st.button("إنهاء الاختبار", key=f"finish_exam_{idx}"):
                st.session_state.exam_finished = True
                st.rerun()


def render_exam_result() -> None:
    questions = st.session_state.filtered_questions
    answers = st.session_state.answers
    result = calculate_score(questions, answers)

    st.markdown('<div class="section-title">النتيجة النهائية</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-box"><div class="metric-num">{result["total"]}</div><div class="metric-label">إجمالي الأسئلة</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-box"><div class="metric-num">{result["correct"]}</div><div class="metric-label">إجابات صحيحة</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-box"><div class="metric-num">{result["wrong"]}</div><div class="metric-label">إجابات خاطئة</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-box"><div class="metric-num">{result["percent"]}%</div><div class="metric-label">النسبة المئوية</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">مراجعة الإجابات</div>', unsafe_allow_html=True)

    for idx, q in enumerate(questions):
        answer_info = answers.get(idx, {})
        status = answer_info.get("status", "skipped")
        selected_option = answer_info.get("selected_option", "لم يتم اختيار إجابة")
        correct_option = get_correct_option_text(q)

        if status == "correct":
            color_class = "result-good"
            status_text = "إجابة صحيحة"
        elif status == "wrong":
            color_class = "result-bad"
            status_text = "إجابة غير صحيحة"
        else:
            color_class = "result-bad"
            status_text = "لم تتم الإجابة"

        st.markdown(
            f"""
            <div class="question-shell">
                <div class="question-header">السؤال {idx + 1}</div>
                <div class="question-text" style="font-size:1.15rem;">{q['question']}</div>
                <div class="{color_class}">
                    الحالة: {status_text}<br><br>
                    إجابتك: {selected_option}<br><br>
                    الإجابة الصحيحة: {correct_option}<br><br>
                    الشرح: {q['explanation']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("إعادة الاختبار من جديد", key="restart_exam"):
            reset_exam_runtime_state()
            st.rerun()
    with c2:
        if st.button("العودة لصفحة الاختبارات", key="back_to_exam_setup"):
            reset_exam_runtime_state()
            st.rerun()


def render_exam_page(questions: List[Dict[str, Any]]) -> None:
    if not st.session_state.quiz_started:
        render_exam_setup(questions)
        return

    if st.session_state.exam_finished:
        render_exam_result()
        return

    render_current_question()


# =========================================================
# الشريط الجانبي
# =========================================================
def render_sidebar(questions: List[Dict[str, Any]]) -> str:
    with st.sidebar:
        st.markdown(f"## {APP_ICON} {APP_NAME}")
        st.caption("إصدار عربي احترافي للثانوية العامة")

        page = st.radio(
            "انتقل إلى",
            ["الصفحة الرئيسية", "المكتبة التعليمية", "الاختبارات التفاعلية", "البحث الذكي"],
            key="main_page_selector"
        )

        st.markdown("---")

        st.markdown("### حالة بنك الأسئلة")
        excel_exists = Path(XLSX_QUESTIONS_FILE).exists()
        json_exists = Path(JSON_QUESTIONS_FILE).exists()

        st.success(f"ملف الإكسل الحالي: {XLSX_QUESTIONS_FILE}" if excel_exists else f"ملف الإكسل غير موجود: {XLSX_QUESTIONS_FILE}")
        if json_exists:
            st.info(f"يوجد أيضًا ملف JSON احتياطي: {JSON_QUESTIONS_FILE}")
        else:
            st.caption("لا يوجد ملف JSON احتياطي حاليًا.")

        subjects = get_subjects(questions)
        if subjects:
            st.markdown("### المواد المتاحة")
            for s in subjects:
                st.write(f"• {s}")

        st.markdown("---")
        if st.button("إعادة تحميل بنك الأسئلة", key="reload_questions"):
            st.session_state.questions = get_questions()
            reset_exam_runtime_state()
            st.success("تمت إعادة تحميل بنك الأسئلة.")
            st.rerun()

    return page


# =========================================================
# التشغيل الرئيسي
# =========================================================
def main() -> None:
    init_state()

    questions = st.session_state.questions
    lessons = get_default_lesson_summaries()
    pdfs = get_default_pdf_resources()
    videos = get_default_youtube_resources()

    render_header(questions)
    page = render_sidebar(questions)

    if page == "الصفحة الرئيسية":
        render_dashboard(questions, lessons, pdfs, videos)
    elif page == "المكتبة التعليمية":
        render_library(lessons, pdfs, videos)
    elif page == "الاختبارات التفاعلية":
        render_exam_page(questions)
    elif page == "البحث الذكي":
        render_search(lessons, pdfs, videos, questions)

    st.markdown(
        '<div class="footer-note">تم بناء الواجهة لتدعم العربية بالكامل، وتقرأ بنك الأسئلة مباشرة من ملف الإكسل الحالي داخل المستودع.</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
