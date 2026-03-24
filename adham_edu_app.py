# -*- coding: utf-8 -*-
from __future__ import annotations

import time
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

import pandas as pd
import streamlit as st

# =========================================================
# المنصة التعليمية - باقورة أعمال المهندس أدهم صبري
# =========================================================
APP_NAME = "المنصة التعليمية باقورة أعمال المهندس أدهم صبري"
APP_ICON = "👑"

JSON_QUESTIONS_FILE = "questions_bank.json"
XLSX_QUESTIONS_FILE = "questions_bank.xlsx"

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS فاخر
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900;1000&display=swap');

    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif !important;
    }

    .stApp {
        background:
            radial-gradient(circle at top right, rgba(37, 99, 235, 0.22), transparent 24%),
            radial-gradient(circle at top left, rgba(255, 215, 0, 0.10), transparent 18%),
            linear-gradient(180deg, #020711 0%, #071225 35%, #0b1b35 70%, #07101f 100%);
        color: #f8fbff;
    }

    .block-container {
        padding-top: 1.1rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    .hero-shell {
        position: relative;
        overflow: hidden;
        border-radius: 30px;
        padding: 34px 28px 28px 28px;
        background:
            linear-gradient(135deg, rgba(9, 21, 46, 0.96), rgba(5, 12, 28, 0.97)),
            radial-gradient(circle at 85% 18%, rgba(255,215,90,0.16), transparent 22%);
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 24px 65px rgba(0,0,0,0.35);
        margin-bottom: 22px;
    }

    .brand-pill {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 999px;
        background: rgba(255, 215, 102, 0.10);
        border: 1px solid rgba(255, 215, 102, 0.24);
        color: #ffe8a3;
        font-size: 0.94rem;
        font-weight: 900;
        margin-bottom: 14px;
    }

    .main-title {
        font-size: 2.6rem;
        font-weight: 1000;
        line-height: 1.5;
        color: #ffffff;
        text-align: center;
        margin-bottom: 8px;
        text-shadow: 0 4px 26px rgba(90, 156, 255, 0.20);
    }

    .sub-title {
        font-size: 1.08rem;
        text-align: center;
        color: #d8e3f0;
        line-height: 2;
        margin-bottom: 18px;
    }

    .hero-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-top: 14px;
    }

    .hero-stat {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 16px;
        text-align: center;
    }

    .hero-stat-value {
        font-size: 1.6rem;
        font-weight: 1000;
        color: #ffffff;
        margin-bottom: 4px;
    }

    .hero-stat-label {
        font-size: 0.95rem;
        font-weight: 800;
        color: #d3dceb;
    }

    .section-shell {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 24px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0 14px 38px rgba(0,0,0,0.16);
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 1000;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .section-subtitle {
        color: #d7e0eb;
        font-size: 0.98rem;
        margin-bottom: 16px;
        line-height: 1.95;
    }

    .lux-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.045), rgba(255,255,255,0.03));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 18px;
        margin-bottom: 14px;
    }

    .lesson-card {
        background: linear-gradient(135deg, rgba(18,32,63,0.98), rgba(9,18,35,0.99));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 18px;
        margin-bottom: 14px;
    }

    .lesson-title {
        font-size: 1.12rem;
        font-weight: 1000;
        color: #ffffff;
        margin-bottom: 6px;
    }

    .lesson-meta {
        color: #d5deea;
        font-size: 0.93rem;
        line-height: 1.9;
        margin-bottom: 6px;
    }

    .small-note {
        color: #cad7e6;
        font-size: 0.95rem;
        line-height: 1.95;
    }

    .youtube-card {
        background: linear-gradient(135deg, rgba(66,13,24,0.9), rgba(28,9,14,0.95));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 18px;
        margin-bottom: 14px;
    }

    .yt-title {
        font-size: 1.06rem;
        font-weight: 1000;
        color: #ffffff;
        margin-bottom: 6px;
    }

    .yt-note {
        color: #f0d8de;
        font-size: 0.93rem;
        line-height: 1.95;
    }

    .question-shell {
        background: linear-gradient(135deg, rgba(18,31,62,0.98), rgba(9,17,32,0.99));
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
        background: linear-gradient(90deg, rgba(21,65,121,0.95), rgba(34,104,171,0.95));
        color: #ffffff;
        font-size: 0.95rem;
        font-weight: 1000;
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
        font-weight: 900;
        font-size: 0.92rem;
        border: 1px solid rgba(110,168,254,0.20);
    }

    .question-text {
        font-size: 1.5rem;
        line-height: 2.2;
        font-weight: 1000;
        color: #ffffff;
        margin-top: 8px;
        margin-bottom: 20px;
    }

    .timer-box {
        padding: 15px 18px;
        border-radius: 18px;
        font-size: 1.22rem;
        font-weight: 1000;
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
        font-weight: 900;
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
        font-weight: 900;
        margin-top: 14px;
        margin-bottom: 14px;
        line-height: 2;
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
        font-weight: 1000 !important;
        color: #ffffff !important;
        line-height: 2 !important;
    }

    .stButton > button,
    .stDownloadButton > button {
        width: 100%;
        border-radius: 16px;
        font-size: 1rem;
        font-weight: 1000;
        padding: 0.84rem 1rem;
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

    .footer-note {
        text-align: center;
        color: #b7c7db;
        font-size: 0.95rem;
        margin-top: 10px;
        line-height: 2;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# أدوات مساعدة
# =========================================================
def safe_rerun():
    try:
        st.rerun()
    except Exception:
        try:
            st.experimental_rerun()
        except Exception:
            pass

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

def is_valid_resource_item(item: Any, required_keys: List[str]) -> bool:
    if not isinstance(item, dict):
        return False
    return all(k in item for k in required_keys)

def sanitize_resources(resources: List[Any], required_keys: List[str]) -> List[Dict[str, Any]]:
    clean = []
    for item in resources:
        if is_valid_resource_item(item, required_keys):
            clean.append(item)
    return clean

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

def validate_question_item(item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    required_keys = ["subject", "unit", "difficulty", "question", "options", "answer", "explanation", "time_limit_sec"]
    if not isinstance(item, dict):
        return None
    if not all(k in item for k in required_keys):
        return None
    if not isinstance(item["options"], list) or len(item["options"]) != 4:
        return None

    item["subject"] = str(item["subject"]).strip()
    item["unit"] = str(item["unit"]).strip()
    item["difficulty"] = str(item["difficulty"]).strip()
    item["question"] = str(item["question"]).strip()
    item["options"] = [str(x).strip() for x in item["options"]]
    item["answer"] = str(item["answer"]).strip()
    item["explanation"] = str(item["explanation"]).strip()

    try:
        item["time_limit_sec"] = int(item["time_limit_sec"])
    except Exception:
        item["time_limit_sec"] = 60

    if item["answer"] not in ["أ", "ب", "ج", "د"]:
        return None

    return item

# =========================================================
# ملفات المنصة
# =========================================================
PDF_RESOURCES = [
    {"title": "ملف الفيزياء 1 - الكهرباء والدوائر", "subject": "الفيزياء", "unit": "التيار الكهربي وقانون أوم", "keywords": ["فيزياء", "كهرباء", "تيار", "فرق جهد", "مقاومة"], "drive_link": "https://drive.google.com/file/d/1xlzPmrUqCAR7XF4ZaBAFN6WhbvZum3_d/view?usp=drivesdk"},
    {"title": "ملف الفيزياء 2 - قوانين كيرشوف", "subject": "الفيزياء", "unit": "قوانين كيرشوف", "keywords": ["فيزياء", "كيرشوف", "دوائر", "عقدة", "حلقة"], "drive_link": "https://drive.google.com/file/d/1BQec3wMImmlX-Y82Ll8ppgMFr6N3aQuP/view?usp=drivesdk"},
    {"title": "ملف الفيزياء 3 - القدرة والطاقة", "subject": "الفيزياء", "unit": "القدرة والطاقة الكهربية", "keywords": ["فيزياء", "قدرة", "طاقة", "وات", "كيلووات"], "drive_link": "https://drive.google.com/file/d/1TqlGSQ7__r2er05lfqAi1B2kdIrspXui/view?usp=drivesdk"},
    {"title": "ملف الفيزياء 4 - المجال والمغناطيسية", "subject": "الفيزياء", "unit": "المجال المغناطيسي", "keywords": ["فيزياء", "مغناطيسية", "مجال", "فيض"], "drive_link": "https://drive.google.com/file/d/1Om2_yLrF1btqqr73JOdpAVewL47-BuW8/view?usp=drivesdk"},
    {"title": "ملف الفيزياء 5 - الحث الكهرومغناطيسي", "subject": "الفيزياء", "unit": "الحث الكهرومغناطيسي", "keywords": ["فيزياء", "حث", "فاراداي", "ملف", "فيض"], "drive_link": "https://drive.google.com/file/d/1uo6ZDwqV0CeN9MatZRfk79N07crJ3Gxw/view?usp=drivesdk"},
    {"title": "ملف الفيزياء 6 - الفيزياء الحديثة", "subject": "الفيزياء", "unit": "الذرة والفيزياء الحديثة", "keywords": ["فيزياء", "حديثة", "ذرة", "فوتون", "طيف"], "drive_link": "https://drive.google.com/file/d/1Vn6PQyoyEgvLGf7QB-l75tg_phNIQNDq/view?usp=drivesdk"},
    {"title": "ملف الرياضيات 1 - التفاضل", "subject": "الرياضيات", "unit": "المشتقات", "keywords": ["رياضيات", "تفاضل", "اشتقاق", "دوال"], "drive_link": "https://drive.google.com/file/d/1QjUZknxo9rp8GeeaB4S1OyzAHtDcbsfu/view?usp=drivesdk"},
    {"title": "ملف الرياضيات 2 - التطبيقات على التفاضل", "subject": "الرياضيات", "unit": "قيم عظمى وصغرى", "keywords": ["رياضيات", "تفاضل", "تطبيقات", "عظمى", "صغرى"], "drive_link": "https://drive.google.com/file/d/1LSmHETcXeYwA6qz-eyFX6ItZ6pXgvJ2m/view?usp=drivesdk"},
    {"title": "ملف الرياضيات 3 - التكامل", "subject": "الرياضيات", "unit": "التكامل الأساسي", "keywords": ["رياضيات", "تكامل", "دوال", "ثابت"], "drive_link": "https://drive.google.com/file/d/1BOzbTTX9mtQY-tNI_u_qibQu9et6byAS/view?usp=drivesdk"},
    {"title": "ملف الرياضيات 4 - التكامل بالتجزئة", "subject": "الرياضيات", "unit": "التكامل بالتجزئة", "keywords": ["رياضيات", "تكامل", "تجزئة", "صيغة"], "drive_link": "https://drive.google.com/file/d/1_K--sjkXTb_j3bWTn0fW2X8Il0UVvLAK/view?usp=drivesdk"},
    {"title": "ملف الرياضيات 5 - النهايات والاتصال", "subject": "الرياضيات", "unit": "النهايات والاتصال", "keywords": ["رياضيات", "نهايات", "اتصال"], "drive_link": "https://drive.google.com/file/d/1fkPapUqBblnO6KTTZqERZ8A7ErTNxZTg/view?usp=drivesdk"},
    {"title": "ملف الرياضيات 6 - الاحتمالات والجبر", "subject": "الرياضيات", "unit": "الاحتمالات والجبر", "keywords": ["رياضيات", "احتمال", "جبر", "تباديل", "توافيق"], "drive_link": "https://drive.google.com/file/d/1a9EV9ydkN-8jpVNby_JY4o7bLRzkgbDA/view?usp=drivesdk"},
    {"title": "ملف الكيمياء 1 - التركيب الذري", "subject": "الكيمياء", "unit": "التركيب الذري", "keywords": ["كيمياء", "ذرة", "بروتون", "إلكترون"], "drive_link": "https://drive.google.com/file/d/1J-cWygO1ODjPAfzTYsm9yfE2YBe-1yN-/view?usp=drivesdk"},
    {"title": "ملف الكيمياء 2 - الجدول الدوري", "subject": "الكيمياء", "unit": "الجدول الدوري", "keywords": ["كيمياء", "جدول دوري", "مجموعات", "دورات"], "drive_link": "https://drive.google.com/file/d/1IaVZdUUCtgE4cZ0jxOJ98tk9qdWZSlVV/view?usp=drivesdk"},
    {"title": "ملف الكيمياء 3 - الروابط الكيميائية", "subject": "الكيمياء", "unit": "الروابط الكيميائية", "keywords": ["كيمياء", "روابط", "أيونية", "تساهمية"], "drive_link": "https://drive.google.com/file/d/1WGrU1z6JWk_i22VRpP6OgeEiTrevw-bR/view?usp=drivesdk"},
    {"title": "ملف الكيمياء 4 - الأحماض والقواعد", "subject": "الكيمياء", "unit": "الأحماض والقواعد", "keywords": ["كيمياء", "أحماض", "قواعد", "pH"], "drive_link": "https://drive.google.com/file/d/1gJd_uScUA6vDwEZBTN-faiNYgy_BgYaL/view?usp=drivesdk"},
    {"title": "ملف الكيمياء 5 - المول والحسابات", "subject": "الكيمياء", "unit": "المول والحسابات الكيميائية", "keywords": ["كيمياء", "مول", "أفوجادرو", "كتلة مولية"], "drive_link": "https://drive.google.com/file/d/1OumLNESC2JaxqcbyjZP250KVzKy6cCqw/view?usp=drivesdk"},
    {"title": "ملف الكيمياء 6 - سرعة التفاعل والاتزان", "subject": "الكيمياء", "unit": "سرعة التفاعل والاتزان", "keywords": ["كيمياء", "سرعة", "اتزان", "عامل حفاز"], "drive_link": "https://drive.google.com/file/d/1gCZKhuD-CIJXMTIk8OcK1BgvmKlfBUpU/view?usp=drivesdk"},
    {"title": "ملف اللغة العربية 1 - النحو الأساسي", "subject": "اللغة العربية", "unit": "الفاعل والمفعول", "keywords": ["عربي", "نحو", "فاعل", "مفعول"], "drive_link": "https://drive.google.com/file/d/1vsa7WGbOoO9RMKPqKjjiGxRApjwVFHI3/view?usp=drivesdk"},
    {"title": "ملف اللغة العربية 2 - إن وأخواتها", "subject": "اللغة العربية", "unit": "إن وأخواتها", "keywords": ["عربي", "نحو", "إن", "اسم إن", "خبر إن"], "drive_link": "https://drive.google.com/file/d/1A2tQUulnajZFccFiz5DMfvGQ2RrrqVbt/view?usp=drivesdk"},
    {"title": "ملف اللغة العربية 3 - البلاغة", "subject": "اللغة العربية", "unit": "التشبيه والاستعارة والكناية", "keywords": ["عربي", "بلاغة", "تشبيه", "استعارة", "كناية"], "drive_link": "https://drive.google.com/file/d/1QOkVnt3Sm66_ahiH-MKxlUrrMPxi0SOP/view?usp=drivesdk"},
    {"title": "ملف اللغة العربية 4 - الأساليب", "subject": "اللغة العربية", "unit": "النداء والنفي والتعجب", "keywords": ["عربي", "أساليب", "تعجب", "نداء", "نفي"], "drive_link": "https://drive.google.com/file/d/1O3udsSq5ck3NHjbzYaHvqIhptgHWPAG1/view?usp=drivesdk"},
    {"title": "ملف اللغة العربية 5 - القراءة والنصوص", "subject": "اللغة العربية", "unit": "القراءة والتحليل", "keywords": ["عربي", "قراءة", "نصوص", "تحليل"], "drive_link": "https://drive.google.com/file/d/1Xp2lVzOcPXLh-BqRX9A6Xeku22KYwCVP/view?usp=drivesdk"}
]

YOUTUBE_RESOURCES = [
    {"title": "شرح الفيزياء - الدوائر الكهربية", "subject": "الفيزياء", "unit": "التيار وقانون أوم وكيرشوف", "keywords": ["فيزياء", "كهرباء", "كيرشوف", "أوم"], "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "description": "فيديو مساعد لشرح أساسيات الكهرباء وقوانين الدوائر بصورة مبسطة."},
    {"title": "شرح الفيزياء - الحث والفيزياء الحديثة", "subject": "الفيزياء", "unit": "الحث الكهرومغناطيسي والذرة", "keywords": ["فيزياء", "حث", "حديثة", "ذرة"], "youtube_url": "https://www.youtube.com/watch?v=ysz5S6PUM-U", "description": "شرح داعم لأفكار الحث الكهرومغناطيسي والانتقال إلى الفيزياء الحديثة."},
    {"title": "شرح الرياضيات - التفاضل", "subject": "الرياضيات", "unit": "المشتقات والتطبيقات", "keywords": ["رياضيات", "تفاضل", "مشتقات"], "youtube_url": "https://www.youtube.com/watch?v=jNQXAC9IVRw", "description": "مراجعة مرئية للمشتقات والتطبيقات الامتحانية الأشهر."},
    {"title": "شرح الرياضيات - التكامل والنهايات", "subject": "الرياضيات", "unit": "التكامل والنهايات", "keywords": ["رياضيات", "تكامل", "نهايات"], "youtube_url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ", "description": "فيديو مساعد لتثبيت أفكار التكامل والنهايات بصورة مرتبة."},
    {"title": "شرح الكيمياء - الذرة والروابط", "subject": "الكيمياء", "unit": "التركيب الذري والروابط الكيميائية", "keywords": ["كيمياء", "ذرة", "روابط"], "youtube_url": "https://www.youtube.com/watch?v=9bZkp7q19f0", "description": "عرض مبسط للمفاهيم الأساسية في التركيب الذري والروابط."},
    {"title": "شرح الكيمياء - الأحماض والاتزان", "subject": "الكيمياء", "unit": "الأحماض والقواعد وسرعة التفاعل", "keywords": ["كيمياء", "أحماض", "قواعد", "اتزان"], "youtube_url": "https://www.youtube.com/watch?v=oHg5SJYRHA0", "description": "دعم بصري لأهم أفكار الأحماض والقواعد والاتزان الكيميائي."},
    {"title": "شرح العربية - النحو", "subject": "اللغة العربية", "unit": "الفاعل وإن وأخواتها", "keywords": ["عربي", "نحو", "فاعل", "إن"], "youtube_url": "https://www.youtube.com/watch?v=3JZ_D3ELwOQ", "description": "فيديو مساعد لتوضيح أشهر أبواب النحو المطلوبة."},
    {"title": "شرح العربية - البلاغة والتحليل", "subject": "اللغة العربية", "unit": "التشبيه والاستعارة وتحليل النص", "keywords": ["عربي", "بلاغة", "تحليل"], "youtube_url": "https://www.youtube.com/watch?v=L_jWHffIx5E", "description": "مراجعة مرئية تساعد على فهم البلاغة وتحليل النصوص."}
]

LESSON_SUMMARIES = [
    {"subject": "الفيزياء", "title": "ملخص الكهرباء والدوائر الكهربية", "unit": "التيار - فرق الجهد - المقاومة - كيرشوف", "summary": "يتناول هذا الملخص أساسيات التيار الكهربي وقانون أوم ثم ينتقل إلى تحليل الدوائر باستخدام قوانين كيرشوف، مع التركيز على فهم العلاقات الأساسية قبل البدء في المسائل."},
    {"subject": "الفيزياء", "title": "ملخص الحث والفيزياء الحديثة", "unit": "الحث الكهرومغناطيسي - الذرة - الفوتونات", "summary": "يربط هذا الملخص بين ظواهر الحث الكهرومغناطيسي وبعض مبادئ الفيزياء الحديثة مثل الطيف الذري والفوتونات، ويعرض الأفكار في تسلسل مناسب للمراجعة."},
    {"subject": "الرياضيات", "title": "ملخص التفاضل والتطبيقات", "unit": "المشتقات - المماس - القيم العظمى والصغرى", "summary": "يبدأ الملخص بقواعد الاشتقاق الأساسية ثم ينتقل إلى استخدام المشتقات في دراسة تغير الدوال وإيجاد القيم العظمى والصغرى بطريقة امتحانية واضحة."},
    {"subject": "الرياضيات", "title": "ملخص التكامل والنهايات", "unit": "التكامل - النهايات - الاحتمالات", "summary": "يقدم هذا الملخص مراجعة مركزة لأفكار التكامل والنهايات وبعض مسائل الاحتمالات، مع ربط الخطوات الرياضية بفهم الفكرة لا بالحفظ فقط."},
    {"subject": "الكيمياء", "title": "ملخص التركيب الذري والروابط", "unit": "الذرة - الجدول الدوري - الروابط", "summary": "يركز الملخص على مكونات الذرة والعلاقة بين التوزيع الإلكتروني وخواص العناصر، ثم ينتقل إلى الروابط الكيميائية وأنواعها ومتى تتكون."},
    {"subject": "الكيمياء", "title": "ملخص الأحماض والقواعد والاتزان", "unit": "pH - المول - سرعة التفاعل - الاتزان", "summary": "يجمع هذا المحور بين المفاهيم الأساسية في الأحماض والقواعد والمول والاتزان وسرعة التفاعل، مع تبسيط المصطلحات وربطها بالأسئلة المتوقعة."},
    {"subject": "اللغة العربية", "title": "ملخص النحو العملي", "unit": "الفاعل - المفعول - إن وأخواتها", "summary": "يوضح هذا الملخص أساسيات الإعراب التي تتكرر في الامتحانات، ويعرض الأمثلة بطريقة مباشرة تسهّل التمييز بين مواقع الكلمات في الجملة."},
    {"subject": "اللغة العربية", "title": "ملخص البلاغة والأساليب والتحليل", "unit": "التشبيه - الاستعارة - التعجب - تحليل النص", "summary": "يستعرض هذا الملخص أهم الصور البيانية والأساليب، ثم يوضح كيفية الاقتراب من النص الأدبي بفهم الفكرة العامة والنبرة المسيطرة أولًا."}
]

PDF_RESOURCES = sanitize_resources(PDF_RESOURCES, ["title", "subject", "unit", "keywords", "drive_link"])
YOUTUBE_RESOURCES = sanitize_resources(YOUTUBE_RESOURCES, ["title", "subject", "unit", "keywords", "youtube_url", "description"])
LESSON_SUMMARIES = sanitize_resources(LESSON_SUMMARIES, ["subject", "title", "unit", "summary"])

# =========================================================
# بنك الأسئلة الافتراضي
# =========================================================
def get_default_questions() -> List[Dict[str, Any]]:
    return [
        make_question("الفيزياء", "التيار الكهربي", "سهل", "إذا مر تيار شدته 2 أمبير في موصل لمدة 5 ثوانٍ، فما مقدار الشحنة الكهربية المارة؟", ["أ) 2 كولوم", "ب) 5 كولوم", "ج) 10 كولوم", "د) 20 كولوم"], "ج", "الشحنة = شدة التيار × الزمن = 2 × 5 = 10 كولوم.", 45),
        make_question("الفيزياء", "قانون أوم", "سهل", "مقاومة مقدارها 4 أوم موصلة بفرق جهد 12 فولت، فما شدة التيار المار فيها؟", ["أ) 2 أمبير", "ب) 3 أمبير", "ج) 4 أمبير", "د) 6 أمبير"], "ب", "شدة التيار = فرق الجهد ÷ المقاومة = 12 ÷ 4 = 3 أمبير.", 45),
        make_question("الفيزياء", "قوانين كيرشوف", "متوسط", "ينص قانون كيرشوف الأول على أن المجموع الجبري للتيارات عند نقطة التقاء يساوي:", ["أ) المقاومة", "ب) الجهد", "ج) صفر", "د) مالا نهاية"], "ج", "التيارات الداخلة إلى العقدة تساوي التيارات الخارجة منها، لذلك يكون المجموع الجبري صفرًا.", 55),
        make_question("الفيزياء", "القدرة الكهربية", "متوسط", "جهاز كهربي يعمل عند فرق جهد 220 فولت وشدة تيار 5 أمبير، فما قدرته؟", ["أ) 44 وات", "ب) 220 وات", "ج) 1100 وات", "د) 4400 وات"], "ج", "القدرة = فرق الجهد × شدة التيار = 220 × 5 = 1100 وات.", 50),
        make_question("الفيزياء", "السعة الكهربية", "صعب", "إذا تضاعفت مساحة لوحي مكثف مستوٍ مع ثبات المسافة بينهما، فإن السعة الكهربية:", ["أ) تقل للنصف", "ب) تظل ثابتة", "ج) تتضاعف", "د) تصبح أربعة أمثال"], "ج", "السعة تتناسب طرديًا مع مساحة اللوحين، لذا تتضاعف السعة.", 65),
        make_question("الفيزياء", "المقاومة النوعية", "متوسط", "تعتمد مقاومة موصل منتظم على:", ["أ) طوله ومساحة مقطعه فقط", "ب) نوع مادته فقط", "ج) طوله ونوع مادته ومساحة مقطعه", "د) لونه ودرجة لمعانه"], "ج", "المقاومة تعتمد على طول الموصل ومساحة مقطعه ونوع مادته من خلال المقاومة النوعية.", 55),
        make_question("الفيزياء", "المجال المغناطيسي", "متوسط", "الخطوط التي تمثل المجال المغناطيسي حول مغناطيس دائم تكون:", ["أ) مستقيمة دائمًا", "ب) لا تتقاطع", "ج) تبدأ من الجنوب إلى الشمال خارج المغناطيس", "د) بلا اتجاه"], "ب", "خطوط المجال المغناطيسي لا تتقاطع لأن للمجال عند كل نقطة اتجاهًا واحدًا.", 55),
        make_question("الفيزياء", "الحث الكهرومغناطيسي", "صعب", "ينشأ تيار حثي في ملف عندما:", ["أ) يثبت الفيض المغناطيسي خلاله", "ب) يتغير الفيض المغناطيسي خلاله", "ج) يبرد الملف فقط", "د) تزداد كتلته"], "ب", "وفق قانون فاراداي يتولد تيار حثي عندما يتغير الفيض المغناطيسي المار بالملف.", 65),
        make_question("الفيزياء", "الفيزياء الحديثة", "متوسط", "الفوتون هو:", ["أ) جسيم عديم الطاقة", "ب) كمية منفصلة من الطاقة الضوئية", "ج) نوع من البروتونات", "د) موجة صوتية"], "ب", "الفوتون هو الكم أو الحزمة المنفصلة من الطاقة الكهرومغناطيسية.", 60),
        make_question("الفيزياء", "الطاقة الكهربية", "سهل", "عند تشغيل جهاز قدرته 1000 وات لمدة ساعة واحدة، تكون الطاقة المستهلكة:", ["أ) 1 كيلووات.ساعة", "ب) 100 كيلووات.ساعة", "ج) 10 كيلووات.ساعة", "د) 0.1 كيلووات.ساعة"], "أ", "1000 وات = 1 كيلووات، وخلال ساعة يستهلك 1 كيلووات.ساعة.", 45),

        make_question("الرياضيات", "التفاضل", "سهل", "ما مشتقة الدالة س = x² ؟", ["أ) x", "ب) 2x", "ج) x³", "د) 2"], "ب", "باستخدام قاعدة القوة مشتقة x² تساوي 2x.", 40),
        make_question("الرياضيات", "التكامل", "سهل", "ما قيمة التكامل ∫ 3x² dx ؟", ["أ) x³ + ثابت", "ب) 3x³ + ثابت", "ج) x² + ثابت", "د) 6x + ثابت"], "أ", "تكامل 3x² يساوي x³ + ثابت التكامل.", 45),
        make_question("الرياضيات", "النهايات", "متوسط", "النهاية عندما x تقترب من 1 للتعبير (x² − 1) ÷ (x − 1) تساوي:", ["أ) 0", "ب) 1", "ج) 2", "د) غير معرفة"], "ج", "نحلل x² − 1 إلى (x − 1)(x + 1) ثم نختصر، فتكون النهاية 2.", 55),
        make_question("الرياضيات", "الاحتمالات", "متوسط", "إذا ألقي حجر نرد منتظم مرة واحدة، فما احتمال ظهور عدد أولي؟", ["أ) 1/6", "ب) 1/3", "ج) 1/2", "د) 2/3"], "ج", "الأعداد الأولية على حجر النرد هي 2 و3 و5 وعددها 3 من 6، فالاحتمال 1/2.", 50),
        make_question("الرياضيات", "التكامل بالتجزئة", "صعب", "أي العبارات الآتية تمثل صيغة التكامل بالتجزئة تمثيلًا صحيحًا؟", ["أ) ∫u dv = uv − ∫v du", "ب) ∫u dv = uv + ∫v du", "ج) ∫u dv = du × dv", "د) ∫u dv = u/v + ثابت"], "أ", "هذه هي الصيغة القياسية للتكامل بالتجزئة.", 70),
        make_question("الرياضيات", "المشتقات", "متوسط", "إذا كانت د(س)= 5س³، فإن د'(س) تساوي:", ["أ) 15س²", "ب) 5س²", "ج) 3س²", "د) 15س³"], "أ", "مشتقة 5س³ هي 15س².", 45),
        make_question("الرياضيات", "القيم العظمى والصغرى", "صعب", "لإيجاد القيم العظمى أو الصغرى لدالة، نبدأ عادةً بـ:", ["أ) تكامل الدالة", "ب) مساواة مشتقتها الأولى بالصفر", "ج) ضربها في ثابت", "د) حذف المتغير"], "ب", "نقاط التطرف المحتملة تظهر عندما تساوي المشتقة الأولى صفرًا أو تكون غير معرفة.", 60),
        make_question("الرياضيات", "الاقتران الخطي", "سهل", "إذا كانت الدالة ص = 3س + 2، فميل المستقيم يساوي:", ["أ) 2", "ب) 3", "ج) 5", "د) 1/3"], "ب", "في الصورة ص = م س + ب يكون الميل هو معامل س أي 3.", 35),
        make_question("الرياضيات", "النهايات", "متوسط", "إذا كانت النهاية من اليمين والنهاية من اليسار عند نقطة ما غير متساويتين، فإن النهاية الكلية:", ["أ) موجودة", "ب) تساوي صفرًا", "ج) غير موجودة", "د) تساوي واحدًا"], "ج", "وجود النهاية الكلية يتطلب تساوي النهاية اليمنى واليسرى.", 50),
        make_question("الرياضيات", "الاحتمالات", "متوسط", "عند سحب بطاقة واحدة من بين 10 بطاقات مرقمة من 1 إلى 10، فما احتمال الحصول على عدد زوجي؟", ["أ) 1/10", "ب) 1/5", "ج) 1/2", "د) 3/4"], "ج", "الأعداد الزوجية هي 2 و4 و6 و8 و10 أي 5 بطاقات من أصل 10، فالاحتمال 1/2.", 45),

        make_question("الكيمياء", "التركيب الذري", "سهل", "العدد الذري للعنصر يساوي عدد:", ["أ) النيوترونات", "ب) البروتونات", "ج) النيوكلونات", "د) مستويات الطاقة"], "ب", "العدد الذري يساوي عدد البروتونات في نواة الذرة.", 40),
        make_question("الكيمياء", "الجدول الدوري", "سهل", "العناصر الموجودة في نفس المجموعة في الجدول الدوري تتشابه في:", ["أ) الكتلة الذرية فقط", "ب) عدد النيوترونات", "ج) الخواص الكيميائية", "د) الحالة الفيزيائية فقط"], "ج", "لتقارب عدد إلكترونات التكافؤ تتشابه خواص عناصر المجموعة الواحدة.", 45),
        make_question("الكيمياء", "الأحماض والقواعد", "متوسط", "محلول قيمة الأس الهيدروجيني له تساوي 2 يُعد محلولًا:", ["أ) متعادلًا", "ب) قاعديًا", "ج) حمضيًا", "د) منظمًا فقط"], "ج", "أي قيمة pH أقل من 7 تشير إلى محلول حمضي.", 45),
        make_question("الكيمياء", "المول", "متوسط", "يحتوي مول واحد من أي مادة على:", ["أ) 10²³ جسيم", "ب) 6.02 × 10²³ جسيم", "ج) 3.01 × 10²³ جسيم", "د) 12 جسيمًا"], "ب", "هذا هو عدد أفوجادرو.", 50),
        make_question("الكيمياء", "سرعة التفاعل", "صعب", "يعمل العامل الحفاز على زيادة سرعة التفاعل لأنه:", ["أ) يزيد طاقة التنشيط", "ب) يقلل طاقة التنشيط", "ج) يغير النواتج", "د) يغيّر الاتزان فقط"], "ب", "العامل الحفاز يوفر مسارًا بديلًا بطاقة تنشيط أقل.", 65),
        make_question("الكيمياء", "الروابط الكيميائية", "متوسط", "الرابطة التي تنشأ من مشاركة الذرات في الإلكترونات تُسمى:", ["أ) رابطة أيونية", "ب) رابطة تساهمية", "ج) رابطة فلزية", "د) رابطة هيدروجينية"], "ب", "المشاركة في الإلكترونات تميز الرابطة التساهمية.", 50),
        make_question("الكيمياء", "التركيب الذري", "سهل", "الجسيم المتعادل كهربائيًا داخل النواة هو:", ["أ) الإلكترون", "ب) البروتون", "ج) النيوترون", "د) الفوتون"], "ج", "النيوترون جسيم متعادل يوجد في النواة.", 40),
        make_question("الكيمياء", "الجدول الدوري", "متوسط", "يزداد النشاط الفلزي بوجه عام في الجدول الدوري عند الاتجاه:", ["أ) من اليسار إلى اليمين", "ب) من أعلى إلى أسفل في المجموعة", "ج) من أسفل إلى أعلى", "د) بلا نمط"], "ب", "النشاط الفلزي يزداد عادةً نزولًا لأسفل في المجموعة.", 55),
        make_question("الكيمياء", "الأحماض والقواعد", "متوسط", "إذا كانت قيمة pH لمحاليل أربعة هي 1 و7 و9 و13 فإن المحلول المتعادل هو:", ["أ) 1", "ب) 7", "ج) 9", "د) 13"], "ب", "المحلول المتعادل قيمة pH له تساوي 7.", 45),
        make_question("الكيمياء", "المول والحسابات", "صعب", "إذا كانت الكتلة المولية لمركب ما 18 جم/مول، فكم مولًا توجد في 36 جم منه؟", ["أ) 1 مول", "ب) 2 مول", "ج) 3 مول", "د) 18 مول"], "ب", "عدد المولات = الكتلة ÷ الكتلة المولية = 36 ÷ 18 = 2.", 60),

        make_question("اللغة العربية", "النحو", "سهل", "اختر الجملة الصحيحة من حيث رفع الفاعل:", ["أ) حضرَ الطالبُ", "ب) حضرَ الطالبَ", "ج) حضرَ الطالبِ", "د) حضرَ الطالبْ"], "أ", "الفاعل يجب أن يكون مرفوعًا.", 45),
        make_question("اللغة العربية", "النحو", "متوسط", "في الجملة: إن العلمَ نورٌ، كلمة العلمَ تعرب:", ["أ) خبر إن", "ب) اسم إن", "ج) فاعل", "د) مفعول به"], "ب", "بعد إن يأتي اسمها منصوبًا.", 55),
        make_question("اللغة العربية", "البلاغة", "متوسط", "يقوم التشبيه في البلاغة العربية على:", ["أ) كلمة واحدة فقط", "ب) المقارنة بين شيئين", "ج) فعل ومفعول فقط", "د) جملة بلا معنى"], "ب", "التشبيه مقارنة بين شيئين يشتركان في صفة ما.", 55),
        make_question("اللغة العربية", "الأساليب", "صعب", "في التعبير: ما أجملَ السماءَ، يكون الأسلوب:", ["أ) أمر", "ب) استفهام", "ج) تعجب", "د) نفي"], "ج", "هذه من صيغ التعجب القياسية: ما أفعل.", 55),
        make_question("اللغة العربية", "تحليل النصوص", "صعب", "عند تحليل نص أدبي تحليلاً احترافيًا، فإن أول خطوة صحيحة تكون:", ["أ) عد الكلمات فقط", "ب) تحديد الفكرة المحورية والنبرة العامة", "ج) معرفة عمر الكاتب فقط", "د) عد علامات الترقيم"], "ب", "التحليل يبدأ بفهم الفكرة والنبرة العامة.", 65),
        make_question("اللغة العربية", "النحو", "سهل", "في الجملة: كتبَ الطالبُ الدرسَ، كلمة الدرسَ تعرب:", ["أ) فاعل", "ب) مبتدأ", "ج) مفعول به", "د) خبر"], "ج", "الدرس وقع عليه فعل الكتابة، فهو مفعول به.", 45),
        make_question("اللغة العربية", "إن وأخواتها", "متوسط", "أي الجمل الآتية صحيحة؟", ["أ) إنَّ المجتهدون ناجحون", "ب) إنَّ المجتهدَ ناجحٌ", "ج) إنَّ المجتهدُ ناجحٌ", "د) إنَّ المجتهدِ ناجحٌ"], "ب", "اسم إن منصوب وخبرها مرفوع.", 55),
        make_question("اللغة العربية", "البلاغة", "متوسط", "قولنا: العلمُ نورٌ، يُعد في البلاغة:", ["أ) تشبيهًا بليغًا", "ب) كناية", "ج) جناسًا", "د) سجعًا"], "أ", "تم حذف أداة التشبيه ووجه الشبه، فهو تشبيه بليغ.", 55),
        make_question("اللغة العربية", "الأساليب", "متوسط", "أي التعبيرات الآتية يمثل أسلوب نداء؟", ["أ) هل حضر الطالب؟", "ب) لا تهمل واجبك", "ج) يا طالبُ اجتهد", "د) ما أجملَ الصدق"], "ج", "وجود أداة النداء يا يدل على أسلوب النداء.", 50),
        make_question("اللغة العربية", "القراءة والتحليل", "صعب", "عند استنتاج الفكرة العامة من نص، الأنسب أن تعتمد أولًا على:", ["أ) كلمة واحدة فقط", "ب) الجمل الهامشية", "ج) تكرار المعاني الرئيسة وترابط الفقرات", "د) عدد السطور"], "ج", "الفكرة العامة تُستنتج من ترابط المعاني الأساسية في النص كله.", 60),
    ]

def load_questions_from_json(file_path: str) -> List[Dict[str, Any]]:
    path = Path(file_path)
    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

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

    df = pd.read_excel(path)

    required_cols = [
        "subject", "unit", "difficulty", "question",
        "option_a", "option_b", "option_c", "option_d",
        "answer", "explanation", "time_limit_sec"
    ]

    if not all(col in df.columns for col in required_cols):
        return []

    questions = []
    for _, row in df.iterrows():
        item = {
            "subject": row["subject"],
            "unit": row["unit"],
            "difficulty": row["difficulty"],
            "question": row["question"],
            "options": [
                f"أ) {row['option_a']}",
                f"ب) {row['option_b']}",
                f"ج) {row['option_c']}",
                f"د) {row['option_d']}",
            ],
            "answer": str(row["answer"]).strip(),
            "explanation": row["explanation"],
            "time_limit_sec": row["time_limit_sec"],
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
# إدارة الحالة
# =========================================================
def init_state():
    if "questions" not in st.session_state:
        try:
            st.session_state.questions = get_questions()
        except Exception:
            st.session_state.questions = []

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
    if "exam_mode" not in st.session_state:
        st.session_state.exam_mode = "تدريبي"
    if "exam_subject" not in st.session_state:
        st.session_state.exam_subject = "الكل"

def get_filtered_questions_by_subject(subject_name: str) -> List[Dict[str, Any]]:
    all_questions = get_questions()
    if subject_name == "الكل":
        return all_questions
    return [q for q in all_questions if normalize_text(q["subject"]) == normalize_text(subject_name)]

def reset_exam():
    selected_subject = st.session_state.get("exam_subject", "الكل")
    st.session_state.questions = get_filtered_questions_by_subject(selected_subject)
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

    safe_rerun()

def get_timer_class(seconds_left: int, total_seconds: int) -> str:
    ratio = seconds_left / max(total_seconds, 1)
    if ratio > 0.5:
        return "timer-safe"
    elif ratio > 0.2:
        return "timer-mid"
    return "timer-danger"

def render_timer_fallback(seconds_left: int, time_limit: int):
    timer_class = get_timer_class(seconds_left, time_limit)
    mins = seconds_left // 60
    secs = seconds_left % 60
    st.markdown(
        f'<div class="timer-box {timer_class}">الوقت المتبقي: {mins:02d}:{secs:02d}</div>',
        unsafe_allow_html=True
    )

# =========================================================
# تهيئة
# =========================================================
init_state()
questions = st.session_state.questions

# =========================================================
# رأس المنصة
# =========================================================
st.markdown(f"""
<div class="hero-shell">
    <div style="text-align:center;">
        <div class="brand-pill">إبداع تقني • فخامة بصرية • تجربة تعليمية متكاملة</div>
        <div class="main-title">{APP_NAME}</div>
        <div class="sub-title">
            منصة تعليمية متكاملة تجمع بين الشرح المنظم، والبحث الذكي، والاختبارات الاحترافية،
            وروابط ملفات الدراسة، وفيديوهات يوتيوب التعليمية في واجهة ملكية مصممة لتبهر الطالب من أول نظرة وحتى آخر نتيجة.
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
    st.markdown("### مصدر بنك الأسئلة")
    if Path(JSON_QUESTIONS_FILE).exists():
        st.success(f"تم العثور على {JSON_QUESTIONS_FILE}")
    elif Path(XLSX_QUESTIONS_FILE).exists():
        st.success(f"تم العثور على {XLSX_QUESTIONS_FILE}")
    else:
        st.info("يتم الآن استخدام بنك الأسئلة الافتراضي داخل الكود.")

    st.markdown("---")
    st.markdown("### إعدادات الاختبار")
    available_subjects = ["الكل"] + sorted(list({q["subject"] for q in get_questions()}))
    st.selectbox("اختر مادة الاختبار", available_subjects, key="exam_subject")
    st.selectbox("اختر وضع الاختبار", ["تدريبي", "نهائي"], key="exam_mode")

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
    if st.button("إعادة تحميل بنك الأسئلة"):
        st.session_state.questions = get_questions()
        safe_rerun()

    if st.button("بدء اختبار جديد بالكامل"):
        reset_exam()
        safe_rerun()

# =========================================================
# البحث الذكي
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
    st.warning("لا توجد نتائج مطابقة حاليًا. جرّب كلمات أخرى.")

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# الواجهة الرئيسية
# =========================================================
if page == "الواجهة الرئيسية":
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">رسالة المنصة</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-subtitle">
        هذه المنصة نظام تعليمي متكامل يجمع الشرح، والملفات، والفيديوهات، والاختبارات الاحترافية داخل تجربة فاخرة
        تجعل الطالب ينتقل بين الفهم والمراجعة والتقييم دون تشتيت.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ماذا تقدم المنصة؟")
        st.markdown("""
        <div class="lux-card">ملخصات تعليمية منظمة لكل مادة.</div>
        <div class="lux-card">مكتبة ملفات Google Drive قابلة للمعاينة والتحميل.</div>
        <div class="lux-card">اختبار احترافي سؤالًا بعد سؤال مع مؤقت ونتائج مفصلة.</div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("#### مميزات التجربة")
        st.markdown("""
        <div class="lux-card">واجهة عربية كاملة واتجاه RTL مع بطاقات بصرية راقية.</div>
        <div class="lux-card">بحث ذكي داخل الشرح والملفات والفيديوهات والأسئلة.</div>
        <div class="lux-card">إمكانية تحميل بنك الأسئلة من ملف خارجي JSON أو Excel.</div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "مركز الشرح":
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">مركز الشرح الدراسي</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">ملخصات تعليمية منظمة داخل المنصة تمهد للفهم قبل الانتقال إلى الملفات أو الفيديوهات أو الاختبار.</div>', unsafe_allow_html=True)

    subject_filter = st.selectbox("اختر المادة", ["الكل"] + sorted(list({x["subject"] for x in LESSON_SUMMARIES})))
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

elif page == "مكتبة الملفات":
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">مكتبة الملفات التعليمية</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">اختر الملف المناسب للمادة أو الوحدة، وافتحه مباشرة أو قم بتحميله من خلال Google Drive.</div>', unsafe_allow_html=True)

    if not PDF_RESOURCES:
        st.error("لا توجد ملفات صالحة داخل مكتبة الملفات.")
    else:
        subject_pdf_filter = st.selectbox("تصفية حسب المادة", ["الكل"] + sorted(list({x["subject"] for x in PDF_RESOURCES})))
        filtered_pdfs = PDF_RESOURCES if subject_pdf_filter == "الكل" else [x for x in PDF_RESOURCES if x["subject"] == subject_pdf_filter]

        selected_pdf = st.selectbox("اختر ملفًا من المكتبة", options=[item["title"] for item in filtered_pdfs])
        pdf_item = next((item for item in filtered_pdfs if item["title"] == selected_pdf), None)

        if pdf_item:
            st.markdown(f"""
            <div class="lesson-card">
                <div class="lesson-title">{pdf_item['title']}</div>
                <div class="lesson-meta">المادة: {pdf_item['subject']} | الوحدة: {pdf_item['unit']}</div>
                <div class="small-note">يمكن فتح المعاينة داخل المنصة أو تحميل الملف مباشرة من Google Drive.</div>
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

elif page == "مكتبة يوتيوب":
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">مكتبة فيديوهات يوتيوب التعليمية</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">فيديوهات مقترحة للدعم البصري والشرح الممتد.</div>', unsafe_allow_html=True)

    if not YOUTUBE_RESOURCES:
        st.error("لا توجد فيديوهات صالحة داخل مكتبة يوتيوب.")
    else:
        selected_video = st.selectbox("اختر الفيديو المناسب", options=[item["title"] for item in YOUTUBE_RESOURCES])
        video_item = next((item for item in YOUTUBE_RESOURCES if item["title"] == selected_video), None)

        if video_item:
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

elif page == "الاختبار الذكي":
    if not st.session_state.quiz_started:
        st.markdown('<div class="section-shell">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">الاختبار الذكي المتسلسل</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="section-subtitle">
            هذا القسم يعمل بمنطق احترافي: سؤال واحد فقط في كل مرة، ولا يظهر زر السؤال التالي إلا بعد إرسال الإجابة،
            ولكل سؤال زمن خاص به، وإذا انتهى الوقت يتم الانتقال تلقائيًا للسؤال التالي.
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="lux-card">
            <strong>المادة المختارة:</strong> {st.session_state.exam_subject}<br>
            <strong>وضع الاختبار:</strong> {st.session_state.exam_mode}
        </div>
        """, unsafe_allow_html=True)

        if st.button("ابدأ الاختبار الآن"):
            reset_exam()
            safe_rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        if not st.session_state.questions:
            st.markdown('<div class="section-shell">', unsafe_allow_html=True)
            st.error("لا توجد أسئلة متاحة للمادة المختارة حاليًا.")
            st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.exam_finished:
            st.markdown('<div class="section-shell">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">تم الانتهاء من الاختبار</div>', unsafe_allow_html=True)
            st.success("اكتمل الاختبار. يمكنك الآن الانتقال إلى لوحة النتائج للاطلاع على التقرير الكامل.")
            if st.button("إعادة الاختبار من البداية"):
                reset_exam()
                safe_rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            ensure_timer_for_current_question()

            idx = st.session_state.current_index
            q = st.session_state.questions[idx]
            total_questions = len(st.session_state.questions)

            time_limit = int(q.get("time_limit_sec", 60))
            seconds_left = max(0, int(st.session_state.deadline - time.time())) if st.session_state.deadline else time_limit

            fragment_supported = hasattr(st, "fragment")

            if fragment_supported:
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
                    render_timer_fallback(seconds_left, time_limit)
                    if seconds_left <= 0 and not st.session_state.answer_submitted:
                        move_to_next_question(timeout_skip=True)
            else:
                render_timer_fallback(seconds_left, time_limit)
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
                options = ["-- اختر الإجابة --"] + q["options"]
                selected = st.radio("اختر الإجابة الصحيحة", options=options, key=choice_key)

                if selected == "-- اختر الإجابة --":
                    selected = None

                c1, c2 = st.columns([2, 1])
                with c1:
                    submit_btn = st.button("إرسال الإجابة", disabled=selected is None)
                with c2:
                    st.info("لن يظهر زر السؤال التالي إلا بعد إرسال الإجابة.")

                if submit_btn and selected is not None:
                    st.session_state[choice_key] = selected
                    submit_current_answer()
                    safe_rerun()

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
                        safe_rerun()

            st.markdown('</div>', unsafe_allow_html=True)

elif page == "لوحة النتائج":
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">لوحة النتائج والتقارير</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">تقرير تفصيلي يوضح أداء الطالب في الاختبار مع إمكانية تحميل النتائج في ملف CSV.</div>', unsafe_allow_html=True)

    total = len(st.session_state.questions)
    all_answers = st.session_state.answers
    correct = sum(1 for a in all_answers.values() if a["is_correct"])
    incorrect = sum(1 for a in all_answers.values() if (not a["is_correct"] and not a.get("timed_out")))
    timed_out = sum(1 for a in all_answers.values() if a.get("timed_out"))
    score_percent = round((correct / total) * 100, 2) if total else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div style="font-size:1.8rem;font-weight:1000;">{total}</div><div>إجمالي الأسئلة</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div style="font-size:1.8rem;font-weight:1000;">{correct}</div><div>الإجابات الصحيحة</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div style="font-size:1.8rem;font-weight:1000;">{incorrect}</div><div>الإجابات الخاطئة</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div style="font-size:1.8rem;font-weight:1000;">{timed_out}</div><div>تخطي تلقائي</div></div>', unsafe_allow_html=True)

    st.progress(score_percent / 100 if total else 0)
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

st.markdown("""
<div class="footer-note">
    هذه النسخة تدعم التحميل التلقائي للأسئلة من JSON أو Excel، وتعود تلقائيًا إلى بنك الأسئلة الداخلي إذا لم تجد الملفات الخارجية.
</div>
""", unsafe_allow_html=True)
