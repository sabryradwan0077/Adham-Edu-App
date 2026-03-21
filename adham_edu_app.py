# adham_edu_app.py
from __future__ import annotations

import json
import random
import sqlite3
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

import streamlit as st

# =========================================================
# إعدادات التطبيق
# =========================================================
APP_TITLE = "منصة أدهم التعليمية المتقدمة"
DB_PATH = "adham_edu_app.db"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# التنسيق الفاخر
# =========================================================
def apply_luxury_style():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Cairo', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at top right, rgba(32, 81, 143, 0.25), transparent 28%),
                radial-gradient(circle at top left, rgba(18, 55, 95, 0.35), transparent 25%),
                linear-gradient(180deg, #07111f 0%, #0a1729 35%, #0c1d33 100%);
            color: #eef5ff;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #08101b 0%, #0e2036 60%, #102947 100%);
            border-left: 1px solid rgba(157, 188, 224, 0.15);
        }

        section[data-testid="stSidebar"] * {
            color: #eef5ff !important;
        }

        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 1.5rem;
        }

        .hero-box {
            background: linear-gradient(135deg, rgba(10,26,46,0.95) 0%, rgba(16,45,78,0.95) 100%);
            border: 1px solid rgba(120, 170, 230, 0.20);
            border-radius: 28px;
            padding: 30px;
            box-shadow: 0 18px 48px rgba(0, 0, 0, 0.28);
            margin-bottom: 18px;
        }

        .hero-title {
            color: #ffffff;
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 8px;
        }

        .hero-sub {
            color: #c8dbf4;
            font-size: 1rem;
            line-height: 1.9;
        }

        .card {
            background: linear-gradient(180deg, rgba(12,24,40,0.96) 0%, rgba(15,31,52,0.96) 100%);
            border: 1px solid rgba(140, 180, 230, 0.16);
            border-radius: 24px;
            padding: 22px;
            margin-bottom: 16px;
            box-shadow: 0 14px 36px rgba(0, 0, 0, 0.22);
        }

        .mini-card {
            background: linear-gradient(180deg, rgba(11,22,37,0.96) 0%, rgba(15,29,47,0.96) 100%);
            border: 1px solid rgba(130, 171, 220, 0.14);
            border-radius: 20px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 10px 26px rgba(0, 0, 0, 0.18);
        }

        .metric-title {
            color: #9db8d8;
            font-size: 0.95rem;
            margin-bottom: 4px;
        }

        .metric-value {
            color: #ffffff;
            font-size: 1.8rem;
            font-weight: 800;
        }

        .section-title {
            color: #ffffff;
            font-size: 1.25rem;
            font-weight: 800;
            margin-bottom: 12px;
        }

        .subject-title {
            color: #ffffff;
            font-size: 1.45rem;
            font-weight: 800;
            margin-bottom: 12px;
        }

        .chapter-box {
            background: rgba(13, 28, 46, 0.9);
            border: 1px solid rgba(129, 166, 213, 0.14);
            border-radius: 18px;
            padding: 16px;
            margin-bottom: 14px;
        }

        .good-answer {
            background: linear-gradient(180deg, rgba(8, 64, 35, 0.95) 0%, rgba(9, 88, 44, 0.95) 100%);
            border: 1px solid rgba(95, 220, 145, 0.22);
            color: #effff3;
            border-radius: 18px;
            padding: 16px;
            margin-top: 10px;
            margin-bottom: 10px;
        }

        .bad-answer {
            background: linear-gradient(180deg, rgba(88, 21, 21, 0.95) 0%, rgba(112, 27, 27, 0.95) 100%);
            border: 1px solid rgba(255, 140, 140, 0.22);
            color: #fff2f2;
            border-radius: 18px;
            padding: 16px;
            margin-top: 10px;
            margin-bottom: 10px;
        }

        .exam-box {
            background: linear-gradient(180deg, rgba(12, 24, 40, 0.96) 0%, rgba(18, 33, 53, 0.96) 100%);
            border: 1px solid rgba(140, 180, 230, 0.14);
            border-radius: 22px;
            padding: 18px;
            margin-bottom: 14px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
        }

        .footer-note {
            text-align: center;
            color: #9db8d8;
            padding: 18px 0 4px 0;
            font-size: 0.9rem;
        }

        .stButton > button {
            width: 100%;
            border-radius: 14px;
            background: linear-gradient(135deg, #1a4f8c 0%, #2d6eb8 100%);
            color: white;
            border: 1px solid rgba(164, 199, 238, 0.25);
            font-weight: 800;
            padding: 0.65rem 1rem;
        }

        .stDownloadButton > button {
            width: 100%;
            border-radius: 14px;
            font-weight: 800;
        }

        .stRadio label {
            color: #eef5ff !important;
        }

        .stSelectbox label, .stMultiSelect label, .stTextInput label {
            color: #eef5ff !important;
        }

        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #2d6eb8 0%, #4a8dd8 100%);
        }

        .stAlert {
            border-radius: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

apply_luxury_style()

# =========================================================
# قاعدة البيانات
# =========================================================
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS exam_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            score REAL,
            total REAL,
            percentage REAL,
            exam_type TEXT,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS wrong_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            question_text TEXT,
            choices_json TEXT,
            correct_answer TEXT,
            explanation TEXT,
            source_type TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

def save_exam_score(subject: str, score: float, total: float, exam_type: str):
    percentage = round((score / total) * 100, 2) if total else 0.0
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO exam_scores (subject, score, total, percentage, exam_type, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        subject, score, total, percentage, exam_type,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

def save_wrong_answer(subject: str, question_text: str, choices: List[str], correct_answer: str, explanation: str, source_type: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO wrong_answers (subject, question_text, choices_json, correct_answer, explanation, source_type, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        subject,
        question_text,
        json.dumps(choices, ensure_ascii=False),
        correct_answer,
        explanation,
        source_type,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

def fetch_scores():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT subject, score, total, percentage, exam_type, created_at
        FROM exam_scores
        ORDER BY id DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def fetch_wrong_answers(subject: Optional[str] = None):
    conn = get_conn()
    cur = conn.cursor()
    if subject:
        cur.execute("""
            SELECT id, subject, question_text, choices_json, correct_answer, explanation, source_type, created_at
            FROM wrong_answers
            WHERE subject = ?
            ORDER BY id DESC
        """, (subject,))
    else:
        cur.execute("""
            SELECT id, subject, question_text, choices_json, correct_answer, explanation, source_type, created_at
            FROM wrong_answers
            ORDER BY id DESC
        """)
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_wrong_answer(item_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM wrong_answers WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

# =========================================================
# المواد
# =========================================================
SUBJECTS = [
    "الرياضيات البحتة - التفاضل والتكامل",
    "الرياضيات البحتة - الجبر والهندسة الفراغية",
    "الرياضيات التطبيقية - الاستاتيكا",
    "الرياضيات التطبيقية - الديناميكا",
    "الفيزياء",
    "الكيمياء",
    "اللغة العربية",
    "اللغة الإنجليزية",
]

# =========================================================
# ملخصات المنهج الموسعة
# =========================================================
LESSON_SUMMARIES: Dict[str, Dict[str, Any]] = {
    "الرياضيات البحتة - التفاضل والتكامل": {
        "intro": "عرض شامل لأهم وحدات منهج الصف الثالث الثانوي في التفاضل والتكامل، مع التركيز على القوانين المركزية التي تتكرر في أسئلة الامتحان النهائي.",
        "chapters": [
            {
                "title": "النهايات والاتصال",
                "laws": [
                    {"name": "نهاية مجموع دالتين", "latex": r"\lim_{x \to a}[f(x)+g(x)] = \lim_{x \to a} f(x) + \lim_{x \to a} g(x)"},
                    {"name": "الاتصال عند نقطة", "latex": r"\lim_{x \to a} f(x) = f(a)"},
                ],
            },
            {
                "title": "التفاضل وقاعدة القوة",
                "laws": [
                    {"name": "قاعدة القوة", "latex": r"\frac{d}{dx}(x^n)=n x^{n-1}"},
                    {"name": "مشتقة الثابت", "latex": r"\frac{d}{dx}(c)=0"},
                    {"name": "مشتقة مجموع دالتين", "latex": r"\frac{d}{dx}(f(x)+g(x))=f'(x)+g'(x)"},
                ],
            },
            {
                "title": "مشتقات الدوال المثلثية والأسية",
                "laws": [
                    {"name": "مشتقة الجيب", "latex": r"\frac{d}{dx}(\sin x)=\cos x"},
                    {"name": "مشتقة جيب التمام", "latex": r"\frac{d}{dx}(\cos x)=-\sin x"},
                    {"name": "مشتقة الدالة الأسية", "latex": r"\frac{d}{dx}(e^x)=e^x"},
                ],
            },
            {
                "title": "التكامل غير المحدد",
                "laws": [
                    {"name": "تكامل القوة", "latex": r"\int x^n\,dx=\frac{x^{n+1}}{n+1}+C \quad (n\neq -1)"},
                    {"name": "تكامل الثابت", "latex": r"\int c\,dx = cx + C"},
                    {"name": "التكامل العكسي للتفاضل", "latex": r"\int f'(x)\,dx=f(x)+C"},
                ],
            },
            {
                "title": "التكامل بالتجزئة",
                "laws": [
                    {"name": "قاعدة التكامل بالتجزئة", "latex": r"\int u\,dv = uv - \int v\,du"},
                    {"name": "اختيار u و dv", "latex": r"\text{اختر } u \text{ بحيث يسهل تفاضله، و } dv \text{ بحيث يسهل تكامله}"},
                ],
            },
        ],
    },
    "الرياضيات البحتة - الجبر والهندسة الفراغية": {
        "intro": "ملخص دقيق لأهم موضوعات الجبر والهندسة الفراغية، مع قوانين أساسية تساعد على حل أسئلة البرهان والتحليل والحساب.",
        "chapters": [
            {
                "title": "المتطابقات والتحليل",
                "laws": [
                    {"name": "مربع مجموع حدين", "latex": r"(a+b)^2 = a^2 + 2ab + b^2"},
                    {"name": "فرق مربعين", "latex": r"a^2-b^2=(a-b)(a+b)"},
                    {"name": "مكعب مجموع حدين", "latex": r"(a+b)^3=a^3+3a^2b+3ab^2+b^3"},
                ],
            },
            {
                "title": "المصفوفات والمحددات",
                "laws": [
                    {"name": "ضرب المصفوفات", "latex": r"(AB)_{ij}=\sum_k a_{ik}b_{kj}"},
                    {"name": "محدد مصفوفة 2×2", "latex": r"\begin{vmatrix} a & b \\ c & d \end{vmatrix}=ad-bc"},
                ],
            },
            {
                "title": "الأعداد المركبة",
                "laws": [
                    {"name": "الوحدة التخيلية", "latex": r"i^2=-1"},
                    {"name": "مقياس العدد المركب", "latex": r"|z|=\sqrt{a^2+b^2} \quad \text{حيث } z=a+bi"},
                ],
            },
            {
                "title": "الهندسة التحليلية",
                "laws": [
                    {"name": "المسافة بين نقطتين", "latex": r"d=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}"},
                    {"name": "ميل المستقيم", "latex": r"m=\frac{y_2-y_1}{x_2-x_1}"},
                ],
            },
            {
                "title": "الهندسة الفراغية",
                "laws": [
                    {"name": "علاقة المستقيم بالمستوى", "latex": r"\text{إذا كان المستقيم عموديًا على مستقيمين متقاطعين في مستوى، فهو عمودي على المستوى}"},
                    {"name": "حجم المنشور", "latex": r"\text{الحجم} = \text{مساحة القاعدة} \times \text{الارتفاع}"},
                ],
            },
        ],
    },
    "الرياضيات التطبيقية - الاستاتيكا": {
        "intro": "مراجعة منهجية للاستاتيكا تشمل القوى والعزوم والاتزان ومركز الثقل، مع القواعد الأساسية المستخدمة في المسائل الوزارية.",
        "chapters": [
            {
                "title": "القوى وتمثيلها",
                "laws": [
                    {"name": "مركبتا القوة", "latex": r"F_x = F\cos\theta \quad,\quad F_y = F\sin\theta"},
                    {"name": "محصلة قوتين", "latex": r"R=\sqrt{F_1^2+F_2^2+2F_1F_2\cos\theta}"},
                ],
            },
            {
                "title": "الاتزان الانتقالي",
                "laws": [
                    {"name": "الاتزان الأفقي", "latex": r"\Sigma F_x = 0"},
                    {"name": "الاتزان الرأسي", "latex": r"\Sigma F_y = 0"},
                ],
            },
            {
                "title": "العزوم",
                "laws": [
                    {"name": "عزم قوة حول نقطة", "latex": r"M = F \times d"},
                    {"name": "اتزان العزوم", "latex": r"\Sigma M = 0"},
                ],
            },
            {
                "title": "مركز الثقل",
                "laws": [
                    {"name": "مركز ثقل جسم منتظم", "latex": r"\text{يقع عند نقطة تماثله الهندسي}"},
                    {"name": "مركز ثقل عدة أوزان", "latex": r"\bar{x}=\frac{\Sigma Wx}{\Sigma W}"},
                ],
            },
            {
                "title": "نظرية لامي",
                "laws": [
                    {"name": "نظرية لامي", "latex": r"\frac{F_1}{\sin \alpha}=\frac{F_2}{\sin \beta}=\frac{F_3}{\sin \gamma}"},
                ],
            },
        ],
    },
    "الرياضيات التطبيقية - الديناميكا": {
        "intro": "ملخص شامل لأهم موضوعات الديناميكا: السرعة، العجلة، الحركة الخطية، المقذوفات، والحركة الدائرية.",
        "chapters": [
            {
                "title": "الحركة في خط مستقيم",
                "laws": [
                    {"name": "السرعة", "latex": r"v=\frac{ds}{dt}"},
                    {"name": "العجلة", "latex": r"a=\frac{dv}{dt}"},
                ],
            },
            {
                "title": "العجلة المنتظمة",
                "laws": [
                    {"name": "العلاقة الأولى", "latex": r"v=u+at"},
                    {"name": "العلاقة الثانية", "latex": r"s=ut+\frac{1}{2}at^2"},
                    {"name": "العلاقة الثالثة", "latex": r"v^2=u^2+2as"},
                ],
            },
            {
                "title": "الحركة الرأسية",
                "laws": [
                    {"name": "العجلة تحت تأثير الجاذبية", "latex": r"a=-g"},
                    {"name": "الإزاحة الرأسية", "latex": r"s=ut-\frac{1}{2}gt^2"},
                ],
            },
            {
                "title": "المقذوفات",
                "laws": [
                    {"name": "المدى الأفقي", "latex": r"R=\frac{u^2\sin 2\theta}{g}"},
                    {"name": "أقصى ارتفاع", "latex": r"H=\frac{u^2\sin^2\theta}{2g}"},
                ],
            },
            {
                "title": "الحركة الدائرية",
                "laws": [
                    {"name": "العجلة المركزية", "latex": r"a_c=\frac{v^2}{r}"},
                    {"name": "القوة المركزية", "latex": r"F=\frac{mv^2}{r}"},
                ],
            },
        ],
    },
    "الفيزياء": {
        "intro": "تجميع منظم لأهم فصول الفيزياء في الصف الثالث الثانوي، مع قوانين أساسية تشمل الكهرباء الحديثة والدوائر والتيار والمجالات.",
        "chapters": [
            {
                "title": "التيار الكهربي وقانون أوم",
                "laws": [
                    {"name": "قانون أوم", "latex": r"V = IR"},
                    {"name": "القدرة الكهربية", "latex": r"P = VI"},
                    {"name": "الطاقة الكهربية", "latex": r"W = VIt"},
                ],
            },
            {
                "title": "المقاومة والمقاومية",
                "laws": [
                    {"name": "المقاومة", "latex": r"R=\rho \frac{L}{A}"},
                    {"name": "الموصلية", "latex": r"\sigma=\frac{1}{\rho}"},
                ],
            },
            {
                "title": "قوانين كيرشوف",
                "laws": [
                    {"name": "قانون العقدة", "latex": r"\Sigma I_{\text{داخل}} = \Sigma I_{\text{خارج}}"},
                    {"name": "قانون الحلقة", "latex": r"\Sigma V = 0"},
                ],
            },
            {
                "title": "الحث الكهرومغناطيسي",
                "laws": [
                    {"name": "قانون فاراداي", "latex": r"\varepsilon = -\frac{d\Phi}{dt}"},
                    {"name": "الفيض المغناطيسي", "latex": r"\Phi = BA\cos\theta"},
                ],
            },
            {
                "title": "الفيزياء الحديثة",
                "laws": [
                    {"name": "طاقة الفوتون", "latex": r"E = hf"},
                    {"name": "معادلة أينشتاين الكهروضوئية", "latex": r"hf = \phi + \frac{1}{2}mv^2"},
                ],
            },
        ],
    },
    "الكيمياء": {
        "intro": "تجميع مهني لأهم أبواب الكيمياء في الصف الثالث الثانوي مع القوانين والعلاقات الكمية المتكررة في المسائل.",
        "chapters": [
            {
                "title": "المول والحساب الكيميائي",
                "laws": [
                    {"name": "عدد المولات", "latex": r"n=\frac{m}{M}"},
                    {"name": "عدد الجسيمات", "latex": r"N=nN_A"},
                ],
            },
            {
                "title": "الغازات",
                "laws": [
                    {"name": "قانون الغاز المثالي", "latex": r"PV=nRT"},
                    {"name": "حجم مول واحد من الغاز", "latex": r"22.4 \text{ لتر عند الظروف القياسية}"},
                ],
            },
            {
                "title": "المحاليل والتركيز",
                "laws": [
                    {"name": "المولارية", "latex": r"M=\frac{n}{V}"},
                    {"name": "النسبة المئوية الكتلية", "latex": r"\%\text{كتلية}=\frac{\text{كتلة المذاب}}{\text{كتلة المحلول}}\times 100"},
                ],
            },
            {
                "title": "الاتزان الكيميائي",
                "laws": [
                    {"name": "ثابت الاتزان", "latex": r"K_c=\frac{[C]^c[D]^d}{[A]^a[B]^b}"},
                    {"name": "مبدأ لوشاتيليه", "latex": r"\text{إذا تغير أحد العوامل المؤثرة على الاتزان، يتحرك النظام لمقاومة هذا التغير}"},
                ],
            },
            {
                "title": "الأكسدة والاختزال",
                "laws": [
                    {"name": "الأكسدة", "latex": r"\text{فقد إلكترونات}"},
                    {"name": "الاختزال", "latex": r"\text{اكتساب إلكترونات}"},
                ],
            },
        ],
    },
    "اللغة العربية": {
        "intro": "عرض منظم لأهم محاور اللغة العربية في الصف الثالث الثانوي: النحو، البلاغة، النصوص، القراءة، والتعبير.",
        "chapters": [
            {
                "title": "النحو",
                "laws": [
                    {"name": "إن وأخواتها", "latex": r"\text{تنصب المبتدأ وترفع الخبر}"},
                    {"name": "كان وأخواتها", "latex": r"\text{ترفع المبتدأ وتنصب الخبر}"},
                ],
            },
            {
                "title": "البلاغة",
                "laws": [
                    {"name": "التشبيه", "latex": r"\text{مقارنة بين شيئين اشتركا في صفة}"},
                    {"name": "الاستعارة", "latex": r"\text{تشبيه حذف أحد طرفيه}"},
                ],
            },
            {
                "title": "الأدب والنصوص",
                "laws": [
                    {"name": "مدرسة الإحياء", "latex": r"\text{العودة إلى التراث القديم في المعاني والأساليب}"},
                    {"name": "مدرسة الديوان", "latex": r"\text{التركيز على التجربة الذاتية والوحدة العضوية}"},
                ],
            },
            {
                "title": "القراءة",
                "laws": [
                    {"name": "فهم الفكرة العامة", "latex": r"\text{حدد الفكرة المحورية قبل تحليل التفاصيل}"},
                    {"name": "الاستنتاج", "latex": r"\text{استخرج المعنى الضمني من السياق لا من اللفظ المباشر فقط}"},
                ],
            },
            {
                "title": "التعبير",
                "laws": [
                    {"name": "مقدمة مترابطة", "latex": r"\text{ابدأ بفكرة ممهدة متصلة بالموضوع}"},
                    {"name": "وحدة الموضوع", "latex": r"\text{لا تنتقل بين الأفكار إلا بترتيب منطقي}"},
                ],
            },
        ],
    },
    "اللغة الإنجليزية": {
        "intro": "مراجعة شاملة في القواعد والمفردات والقراءة والكتابة لطلاب الصف الثالث الثانوي.",
        "chapters": [
            {
                "title": "الأزمنة",
                "laws": [
                    {"name": "المضارع التام", "latex": r"\text{S + have/has + P.P}"},
                    {"name": "الماضي التام", "latex": r"\text{S + had + P.P}"},
                ],
            },
            {
                "title": "الجمل الشرطية",
                "laws": [
                    {"name": "الشرط الأول", "latex": r"\text{If + present simple, will + infinitive}"},
                    {"name": "الشرط الثاني", "latex": r"\text{If + past simple, would + infinitive}"},
                ],
            },
            {
                "title": "المبني للمجهول",
                "laws": [
                    {"name": "التحويل للمجهول", "latex": r"\text{Object + be + P.P}"},
                ],
            },
            {
                "title": "الروابط والمفردات",
                "laws": [
                    {"name": "السبب والنتيجة", "latex": r"\text{because, since, therefore, so}"},
                    {"name": "التضاد", "latex": r"\text{however, although, but}"},
                ],
            },
            {
                "title": "الكتابة والقطعة",
                "laws": [
                    {"name": "الجملة الموضوعية", "latex": r"\text{ابدأ الفقرة بجملة رئيسية واضحة}"},
                    {"name": "التسلسل المنطقي", "latex": r"\text{رتب الأفكار من العام إلى الخاص}"},
                ],
            },
        ],
    },
}

# =========================================================
# بنك الأسئلة
# =========================================================
QUESTION_BANK: Dict[str, List[Dict[str, Any]]] = {
    "الرياضيات البحتة - التفاضل والتكامل": [
        {
            "question": "إذا كانت الدالة \( د(x)=x^5 \)، فما قيمة مشتقتها \( د'(x) \)؟",
            "options": {
                "A": r"\(5x^4\)",
                "B": r"\(x^4\)",
                "C": r"\(5x\)",
                "D": r"\(x^6\)",
            },
            "correct": "A",
            "solution_title": "الحل خطوة بخطوة",
            "solution_steps": [
                r"الدالة المعطاة هي \(x^5\).",
                r"نطبق قاعدة القوة: \(\frac{d}{dx}(x^n)=n x^{n-1}\).",
                r"إذن: \(\frac{d}{dx}(x^5)=5x^4\).",
            ],
        },
        {
            "question": "أوجد مشتقة \( 3x^4 - 2x^2 + 7 \).",
            "options": {
                "A": r"\(12x^3 - 4x\)",
                "B": r"\(12x^3 - 2x\)",
                "C": r"\(4x^3 - 2x\)",
                "D": r"\(12x^4 - 4x\)",
            },
            "correct": "A",
            "solution_title": "الحل خطوة بخطوة",
            "solution_steps": [
                r"مشتقة \(3x^4\) تساوي \(12x^3\).",
                r"مشتقة \(-2x^2\) تساوي \(-4x\).",
                r"مشتقة الثابت \(7\) تساوي \(0\).",
                r"إذن الناتج النهائي هو \(12x^3 - 4x\).",
            ],
        },
        {
            "question": "ما قيمة التكامل \( \int x^2 \, dx \) ؟",
            "options": {
                "A": r"\(\frac{x^3}{3}+C\)",
                "B": r"\(x^3+C\)",
                "C": r"\(\frac{x^2}{2}+C\)",
                "D": r"\(2x+C\)",
            },
            "correct": "A",
            "solution_title": "الحل خطوة بخطوة",
            "solution_steps": [
                r"نستخدم قاعدة تكامل القوة: \(\int x^n dx = \frac{x^{n+1}}{n+1}+C\).",
                r"عند \(n=2\) يصبح التكامل \(\frac{x^3}{3}+C\).",
            ],
        },
        {
            "question": "إذا كانت \( y=x^3+x^2-1 \)، فأوجد \( y'(2) \).",
            "options": {
                "A": "14",
                "B": "16",
                "C": "12",
                "D": "10",
            },
            "correct": "B",
            "solution_title": "الحل خطوة بخطوة",
            "solution_steps": [
                r"نشتق أولًا: \(y'=3x^2+2x\).",
                r"بالتعويض عن \(x=2\): \(3(2^2)+2(2)=12+4=16\).",
            ],
        },
        {
            "question": "أي من الآتي يمثل صيغة التكامل بالتجزئة؟",
            "options": {
                "A": r"\(\int u\,dv = uv - \int v\,du\)",
                "B": r"\(\int u\,dv = uv + \int v\,du\)",
                "C": r"\(\int u\,dv = du\,dv\)",
                "D": r"\(\int u\,dv = \frac{u}{v}\)",
            },
            "correct": "A",
            "solution_title": "الحل خطوة بخطوة",
            "solution_steps": [
                r"قاعدة التكامل بالتجزئة الأساسية هي:",
                r"\(\int u\,dv = uv - \int v\,du\).",
            ],
        },
    ],
    "الرياضيات التطبيقية - الاستاتيكا": [
        {
            "question": "في حالة الاتزان الأفقي لجسم، أي العلاقات الآتية صحيحة؟",
            "options": {
                "A": r"\(\Sigma F_x = 0\)",
                "B": r"\(\Sigma F_y = 0\)",
                "C": r"\(\Sigma M = 0\)",
                "D": r"\(F = ma\)",
            },
            "correct": "A",
            "solution_title": "الحل خطوة بخطوة",
            "solution_steps": [
                r"الاتزان الأفقي يعني أن محصلة المركبات الأفقية للقوى تساوي صفرًا.",
                r"إذن: \(\Sigma F_x = 0\).",
            ],
        },
        {
            "question": "إذا أثرت قوة مقدارها \(F\) على بعد عمودي \(d\) من نقطة الدوران، فإن العزم يساوي:",
            "options": {
                "A": r"\(M=F+d\)",
                "B": r"\(M=F\times d\)",
                "C": r"\(M=\frac{F}{d}\)",
                "D": r"\(M=Fd^2\)",
            },
            "correct": "B",
            "solution_title": "الحل خطوة بخطوة",
            "solution_steps": [
                r"تعريف العزم حول نقطة هو حاصل ضرب مقدار القوة في ذراعها العمودي.",
                r"إذن: \(M=F\times d\).",
            ],
        },
        {
            "question": "تتحقق نظرية لامي عندما يكون الجسم تحت تأثير:",
            "options": {
                "A": "قوتين فقط",
                "B": "ثلاث قوى متلاقية في حالة اتزان",
                "C": "أربع قوى متوازية",
                "D": "قوة واحدة فقط",
            },
            "correct": "B",
            "solution_title": "الحل خطوة بخطوة",
            "solution_steps": [
                r"نظرية لامي تُستخدم عندما تؤثر ثلاث قوى متلاقية على جسم في حالة اتزان.",
                r"وحينها: \(\frac{F_1}{\sin\alpha}=\frac{F_2}{\sin\beta}=\frac{F_3}{\sin\gamma}\).",
            ],
        },
    ],
    "الفيزياء": [
        {
            "question": "أي القوانين الآتية يمثل قانون أوم؟",
            "options": {
                "A": r"\(V=IR\)",
                "B": r"\(P=VI\)",
                "C": r"\(F=ma\)",
                "D": r"\(Q=It\)",
            },
            "correct": "A",
            "solution_title": "الحل خطوة بخطوة",
            "solution_steps": [
                r"قانون أوم يربط بين فرق الجهد والتيار والمقاومة.",
                r"الصيغة الصحيحة هي: \(V=IR\).",
            ],
        },
        {
            "question": "ماذا ينص قانون كيرشوف للعقدة؟",
            "options": {
                "A": "مجموع فروق الجهد في دائرة مغلقة يساوي واحدًا",
                "B": "مجموع التيارات الداخلة للعقدة يساوي مجموع التيارات الخارجة منها",
                "C": "المقاومة تساوي الجهد على التيار فقط",
                "D": "القدرة تساوي مربع التيار في المقاومة فقط",
            },
            "correct": "B",
            "solution_title": "الحل خطوة بخطوة",
            "solution_steps": [
                r"قانون كيرشوف الأول يطبق عند العقدة.",
                r"وينص على أن مجموع التيارات الداخلة يساوي مجموع التيارات الخارجة.",
                r"أي: \(\Sigma I_{\text{داخل}} = \Sigma I_{\text{خارج}}\).",
            ],
        },
        {
            "question": "ما الصيغة الصحيحة لقانون فاراداي للحث الكهرومغناطيسي؟",
            "options": {
                "A": r"\(\varepsilon = IR\)",
                "B": r"\(\varepsilon = -\frac{d\Phi}{dt}\)",
                "C": r"\(\Phi = \frac{dI}{dt}\)",
                "D": r"\(B = \mu I\)",
            },
            "correct": "B",
            "solution_title": "الحل خطوة بخطوة",
            "solution_steps": [
                r"قانون فاراداي ينص على أن القوة الدافعة المستحثة تساوي المعدل الزمني السالب لتغير الفيض.",
                r"إذن: \(\varepsilon = -\frac{d\Phi}{dt}\).",
            ],
        },
    ],
    "الكيمياء": [
        {
            "question": "إذا كانت كتلة المادة \(18\) جم وكتلتها المولية \(18\) جم/مول، فإن عدد المولات يساوي:",
            "options": {
                "A": "0.5 مول",
                "B": "1 مول",
                "C": "2 مول",
                "D": "18 مول",
            },
            "correct": "B",
            "solution_title": "الحل خطوة بخطوة",
            "solution_steps": [
                r"نستخدم العلاقة: \(n=\frac{m}{M}\).",
                r"بالتعويض: \(n=\frac{18}{18}=1\) مول.",
            ],
        },
        {
            "question": "أي العلاقات الآتية تمثل قانون الغاز المثالي؟",
            "options": {
                "A": r"\(PV=nRT\)",
                "B": r"\(V=IR\)",
                "C": r"\(K_c=[A][B]\)",
                "D": r"\(n=M\times m\)",
            },
            "correct": "A",
            "solution_title": "الحل خطوة بخطوة",
            "solution_steps": [
                r"القانون العام للغازات المثالية هو:",
                r"\(PV=nRT\).",
            ],
        },
        {
            "question": "المولارية تُحسب من العلاقة:",
            "options": {
                "A": r"\(M=\frac{n}{V}\)",
                "B": r"\(M=\frac{m}{n}\)",
                "C": r"\(M=nV\)",
                "D": r"\(M=\frac{V}{n}\)",
            },
            "correct": "A",
            "solution_title": "الحل خطوة بخطوة",
            "solution_steps": [
                r"المولارية هي عدد المولات لكل لتر من المحلول.",
                r"إذن: \(M=\frac{n}{V}\).",
            ],
        },
    ],
    "اللغة العربية": [
        {
            "question": "ما الأثر الإعرابي الصحيح لـ (إنَّ)؟",
            "options": {
                "A": "ترفع المبتدأ وتنصب الخبر",
                "B": "تنصب المبتدأ وترفع الخبر",
                "C": "تجزم الفعل المضارع",
                "D": "تنصب الفاعل",
            },
            "correct": "B",
            "solution_title": "الشرح",
            "solution_steps": [
                r"\(\text{إنَّ وأخواتها تنصب المبتدأ ويسمى اسمها، وترفع الخبر ويسمى خبرها.}\)",
            ],
        },
        {
            "question": "أي التعبيرات الآتية يُعد استعارة؟",
            "options": {
                "A": "العلم نور",
                "B": "الطالب كالأسد",
                "C": "الشمس مثل الذهب",
                "D": "الوقت كالسيف",
            },
            "correct": "A",
            "solution_title": "الشرح",
            "solution_steps": [
                r"\(\text{في قولنا: العلم نور، شُبِّه العلم بالنور وحُذف المشبه به على صورة استعارة.}\)",
            ],
        },
    ],
    "اللغة الإنجليزية": [
        {
            "question": "اختر الصيغة الصحيحة للمضارع التام:",
            "options": {
                "A": "Subject + had + past participle",
                "B": "Subject + have/has + past participle",
                "C": "Subject + am/is/are + verb+ing",
                "D": "Subject + will + infinitive",
            },
            "correct": "B",
            "solution_title": "الشرح",
            "solution_steps": [
                r"\(\text{المضارع التام يتكون من: Subject + have/has + P.P}\)",
            ],
        },
        {
            "question": "ما البناء الصحيح للشرط الأول؟",
            "options": {
                "A": "If + present simple, will + infinitive",
                "B": "If + past simple, would + infinitive",
                "C": "If + had + P.P, would have + P.P",
                "D": "If + present simple, present simple only",
            },
            "correct": "A",
            "solution_title": "الشرح",
            "solution_steps": [
                r"\(\text{الشرط الأول: If + present simple, will + infinitive}\)",
            ],
        },
    ],
}

# دعم المواد الأخرى لو لم توجد أسئلة كافية
for subject in SUBJECTS:
    QUESTION_BANK.setdefault(subject, [])

# =========================================================
# إنشاء نموذج امتحان من بنك الأسئلة
# =========================================================
def build_mock_exam(subject: str) -> List[Dict[str, Any]]:
    base = QUESTION_BANK.get(subject, [])
    if not base:
        return []
    if len(base) <= 5:
        return base
    return random.sample(base, min(8, len(base)))

# =========================================================
# إدارة الحالة
# =========================================================
def ensure_state():
    defaults = {
        "selected_subject": SUBJECTS[0],
        "exam_subject": SUBJECTS[0],
        "exam_started": False,
        "exam_submitted": False,
        "exam_questions": [],
        "exam_answers": {},
        "exam_start_time": None,
        "exam_duration_seconds": 3 * 60 * 60,
        "saved_exam_once": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

ensure_state()

# =========================================================
# أدوات مساعدة
# =========================================================
def metric_cards():
    scores = fetch_scores()
    wrongs = fetch_wrong_answers()
    total_exams = len(scores)
    avg = round(sum(x[3] for x in scores) / total_exams, 2) if total_exams else 0.0
    best = max([x[3] for x in scores], default=0.0)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f'<div class="mini-card"><div class="metric-title">عدد المحاكاة</div><div class="metric-value">{total_exams}</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="mini-card"><div class="metric-title">متوسط النسبة</div><div class="metric-value">{avg}%</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div class="mini-card"><div class="metric-title">أسئلة المراجعة</div><div class="metric-value">{len(wrongs)}</div></div>',
            unsafe_allow_html=True,
        )

def format_seconds(seconds_left: int) -> str:
    seconds_left = max(0, seconds_left)
    h = seconds_left // 3600
    m = (seconds_left % 3600) // 60
    s = seconds_left % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def calculate_exam_result(questions: List[Dict[str, Any]], answers: Dict[str, str]):
    score = 0
    details = []
    for i, q in enumerate(questions):
        qid = f"exam_q_{i}"
        selected = answers.get(qid)
        correct = q["correct"]
        is_ok = selected == correct
        if is_ok:
            score += 1
        details.append({
            "question": q["question"],
            "selected": selected,
            "correct": correct,
            "is_ok": is_ok,
            "options": q["options"],
            "solution_title": q["solution_title"],
            "solution_steps": q["solution_steps"],
        })
    return score, len(questions), details

def render_solution_steps(steps: List[str]):
    for step in steps:
        if "\\" in step or "$" in step:
            cleaned = step.strip()
            if cleaned.startswith(r"\(") or cleaned.startswith(r"\[") or cleaned.startswith(r"\frac") or cleaned.startswith(r"\Sigma") or cleaned.startswith(r"\int") or cleaned.startswith(r"\text"):
                try:
                    st.latex(cleaned.replace(r"\(", "").replace(r"\)", ""))
                except Exception:
                    st.write(f"• {step}")
            else:
                st.write(f"• {step}")
        else:
            st.write(f"• {step}")

# =========================================================
# الشريط الجانبي
# =========================================================
with st.sidebar:
    st.markdown("## التنقل داخل المنصة")
    page = st.radio(
        "اختر القسم",
        [
            "الصفحة الرئيسية",
            "ملخصات الدروس",
            "بنك الأسئلة التفاعلي",
            "قاعة محاكاة الامتحان",
            "المراجعة لاحقًا",
            "تتبع التقدم",
        ],
        index=0,
    )
    st.markdown("---")
    chosen_subject = st.selectbox("اختر المادة", SUBJECTS, index=SUBJECTS.index(st.session_state.selected_subject))
    st.session_state.selected_subject = chosen_subject
    st.markdown("---")
    st.caption("منصة عربية احترافية للمذاكرة المركزة والامتحان الذكي")

# =========================================================
# الصفحة الرئيسية
# =========================================================
if page == "الصفحة الرئيسية":
    st.markdown(
        f"""
        <div class="hero-box">
            <div class="hero-title">{APP_TITLE}</div>
            <div class="hero-sub">
                منصة تعليمية احترافية للصف الثالث الثانوي – شعبة علمي رياضة،
                تجمع بين العرض العلمي المنظم، التدريب التفاعلي، ومحاكاة الامتحان النهائي
                في تجربة عربية هادئة عالية المستوى.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_cards()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">مكونات المنصة</div>', unsafe_allow_html=True)
    st.write("• ملخصات منهجية موسعة لكل مادة مع تقسيمات الفصول الأساسية.")
    st.write("• أسئلة اختيار من متعدد بأربع بدائل واضحة A / B / C / D.")
    st.write("• اعتماد الإجابة لكل سؤال مع تصحيح فوري وحل خطوة بخطوة.")
    st.write("• قاعة محاكاة امتحان بزمن 3 ساعات واحتساب آلي للدرجة.")
    st.write("• سجل خاص بالأسئلة الخاطئة للعودة إليها في أي وقت.")
    st.write("• قاعدة بيانات محلية لحفظ نتائج المحاكاة وتتبع التقدم.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">أفضل طريقة للاستخدام</div>', unsafe_allow_html=True)
    st.info(
        "ابدأ بملخصات المادة، ثم درّب نفسك من خلال بنك الأسئلة التفاعلي، "
        "وبعد تثبيت القوانين انتقل إلى قاعة محاكاة الامتحان لقياس مستواك الواقعي."
    )
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ملخصات الدروس
# =========================================================
elif page == "ملخصات الدروس":
    subject = st.session_state.selected_subject
    content = LESSON_SUMMARIES.get(subject)

    st.markdown(f'<div class="subject-title">{subject}</div>', unsafe_allow_html=True)

    if not content:
        st.warning("لا توجد بيانات متاحة لهذه المادة حاليًا.")
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">الملخص العام</div>', unsafe_allow_html=True)
        st.write(content["intro"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">الفصول الرئيسية والقوانين الأساسية</div>', unsafe_allow_html=True)

        for chapter in content["chapters"]:
            st.markdown(f'<div class="chapter-box">', unsafe_allow_html=True)
            st.markdown(f"### {chapter['title']}")
            for law in chapter["laws"]:
                st.markdown(f"**{law['name']}**")
                st.latex(law["latex"])
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# بنك الأسئلة التفاعلي
# =========================================================
elif page == "بنك الأسئلة التفاعلي":
    subject = st.session_state.selected_subject
    st.markdown(f'<div class="subject-title">بنك الأسئلة التفاعلي — {subject}</div>', unsafe_allow_html=True)

    questions = QUESTION_BANK.get(subject, [])
    if not questions:
        st.warning("لا توجد أسئلة مضافة لهذه المادة حاليًا.")
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">أجب عن كل سؤال ثم اعتمد الإجابة للحصول على التصحيح الفوري</div>', unsafe_allow_html=True)

        for idx, q in enumerate(questions):
            st.markdown(f'<div class="exam-box">', unsafe_allow_html=True)
            st.markdown(f"**السؤال {idx + 1}:** {q['question']}")

            radio_key = f"quiz_choice_{subject}_{idx}"
            submit_key = f"quiz_submit_{subject}_{idx}"

            selected = st.radio(
                f"اختر الإجابة الصحيحة للسؤال {idx + 1}",
                options=["A", "B", "C", "D"],
                format_func=lambda x, opts=q["options"]: f"{x}) {opts[x]}",
                key=radio_key,
                horizontal=False,
                index=None,
            )

            if st.button("اعتماد الإجابة", key=submit_key):
                if selected is None:
                    st.warning("يجب اختيار إجابة أولًا قبل الاعتماد.")
                else:
                    correct_key = q["correct"]
                    choices_list = [f"{k}) {v}" for k, v in q["options"].items()]

                    if selected == correct_key:
                        st.markdown(
                            f"""
                            <div class="good-answer">
                                <b>إجابة صحيحة.</b><br>
                                الإجابة المعتمدة: {selected}) {q['options'][selected]}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""
                            <div class="bad-answer">
                                <b>إجابة غير صحيحة.</b><br>
                                إجابتك: {selected}) {q['options'][selected]}<br>
                                الإجابة الصحيحة: {correct_key}) {q['options'][correct_key]}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        save_wrong_answer(
                            subject=subject,
                            question_text=q["question"],
                            choices=choices_list,
                            correct_answer=f"{correct_key}) {q['options'][correct_key]}",
                            explanation=" | ".join(q["solution_steps"]),
                            source_type="بنك الأسئلة"
                        )

                    st.markdown(f"**{q['solution_title']}**")
                    render_solution_steps(q["solution_steps"])

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# قاعة محاكاة الامتحان
# =========================================================
elif page == "قاعة محاكاة الامتحان":
    st.markdown('<div class="subject-title">قاعة محاكاة الامتحان النهائي</div>', unsafe_allow_html=True)

    exam_subject = st.selectbox("اختر مادة الامتحان", SUBJECTS, index=SUBJECTS.index(st.session_state.exam_subject))
    st.session_state.exam_subject = exam_subject

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("بدء امتحان جديد"):
            st.session_state.exam_questions = build_mock_exam(exam_subject)
            st.session_state.exam_answers = {}
            st.session_state.exam_started = True
            st.session_state.exam_submitted = False
            st.session_state.exam_start_time = time.time()
            st.session_state.saved_exam_once = False
            st.rerun()

    with c2:
        st.info("مدة الامتحان: 3 ساعات")

    if st.session_state.exam_started and st.session_state.exam_subject == exam_subject:
        elapsed = int(time.time() - st.session_state.exam_start_time) if st.session_state.exam_start_time else 0
        remaining = st.session_state.exam_duration_seconds - elapsed

        t1, t2 = st.columns([1, 2])
        with t1:
            st.metric("الوقت المتبقي", format_seconds(remaining))
        with t2:
            st.progress(max(0, remaining) / st.session_state.exam_duration_seconds)

        if remaining <= 0:
            st.warning("انتهى زمن الامتحان وتم الانتقال إلى التصحيح النهائي.")
            st.session_state.exam_submitted = True

        if not st.session_state.exam_questions:
            st.warning("لا توجد أسئلة كافية لبناء امتحان لهذه المادة حاليًا.")
        else:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">نموذج الامتحان</div>', unsafe_allow_html=True)

            for idx, q in enumerate(st.session_state.exam_questions):
                qid = f"exam_q_{idx}"
                st.markdown(f'<div class="exam-box">', unsafe_allow_html=True)
                st.markdown(f"**السؤال {idx + 1}:** {q['question']}")

                ans = st.radio(
                    f"اختر الإجابة الصحيحة للسؤال {idx + 1}",
                    options=["A", "B", "C", "D"],
                    format_func=lambda x, opts=q["options"]: f"{x}) {opts[x]}",
                    key=f"exam_radio_{qid}",
                    index=None,
                    disabled=st.session_state.exam_submitted
                )

                if ans is not None:
                    st.session_state.exam_answers[qid] = ans

                st.markdown("</div>", unsafe_allow_html=True)

            if not st.session_state.exam_submitted:
                if st.button("تسليم الامتحان"):
                    st.session_state.exam_submitted = True
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

            if st.session_state.exam_submitted:
                score, total, details = calculate_exam_result(
                    st.session_state.exam_questions,
                    st.session_state.exam_answers
                )
                percentage = round((score / total) * 100, 2) if total else 0.0

                if not st.session_state.saved_exam_once:
                    save_exam_score(
                        subject=st.session_state.exam_subject,
                        score=score,
                        total=total,
                        exam_type="محاكاة نهائية"
                    )
                    st.session_state.saved_exam_once = True

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">النتيجة النهائية</div>', unsafe_allow_html=True)
                st.progress(percentage / 100 if total else 0)
                st.success(f"الدرجة النهائية: {score} من {total} — بنسبة {percentage}%")

                if percentage >= 85:
                    st.info("أداء ممتاز جدًا. استمر بهذا المستوى مع زيادة كثافة التدريب على التنويعات.")
                elif percentage >= 65:
                    st.info("أداء جيد، ويحتاج إلى مزيد من التثبيت في النقاط التي ظهر بها تراجع.")
                else:
                    st.warning("يلزم مراجعة مركزة للفصول الأساسية والعودة إلى سجل الأخطاء.")

                st.markdown("### تحليل الإجابات")
                for i, item in enumerate(details, start=1):
                    correct_key = item["correct"]
                    selected = item["selected"]

                    if item["is_ok"]:
                        st.markdown(
                            f"""
                            <div class="good-answer">
                                <b>السؤال {i}:</b> إجابة صحيحة.<br>
                                الاختيار الصحيح: {correct_key}) {item['options'][correct_key]}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""
                            <div class="bad-answer">
                                <b>السؤال {i}:</b> إجابة غير صحيحة.<br>
                                إجابتك: {selected if selected else "لم يتم اختيار إجابة"}<br>
                                الإجابة الصحيحة: {correct_key}) {item['options'][correct_key]}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        save_wrong_answer(
                            subject=st.session_state.exam_subject,
                            question_text=item["question"],
                            choices=[f"{k}) {v}" for k, v in item["options"].items()],
                            correct_answer=f"{correct_key}) {item['options'][correct_key]}",
                            explanation=" | ".join(item["solution_steps"]),
                            source_type="محاكاة الامتحان"
                        )

                    st.markdown(f"**{item['solution_title']}**")
                    render_solution_steps(item["solution_steps"])
                    st.markdown("---")

                st.markdown("</div>", unsafe_allow_html=True)

        if not st.session_state.exam_submitted:
            time.sleep(1)
            st.rerun()

    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("ابدأ امتحانًا جديدًا لاختبار مستواك في صورة قريبة من الامتحان الفعلي.")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# المراجعة لاحقًا
# =========================================================
elif page == "المراجعة لاحقًا":
    st.markdown('<div class="subject-title">سجل المراجعة اللاحقة</div>', unsafe_allow_html=True)

    filter_subject = st.selectbox("تصفية حسب المادة", ["كل المواد"] + SUBJECTS)
    rows = fetch_wrong_answers(None if filter_subject == "كل المواد" else filter_subject)

    if not rows:
        st.info("لا توجد أسئلة محفوظة للمراجعة في الوقت الحالي.")
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">الأسئلة التي تحتاج إلى مراجعة إضافية</div>', unsafe_allow_html=True)

        for row in rows:
            item_id, subject, q_text, choices_json, correct_answer, explanation, source_type, created_at = row
            choices = json.loads(choices_json)

            st.markdown(f'<div class="exam-box">', unsafe_allow_html=True)
            st.markdown(f"**المادة:** {subject}")
            st.markdown(f"**المصدر:** {source_type}")
            st.markdown(f"**تاريخ الحفظ:** {created_at}")
            st.markdown(f"**السؤال:** {q_text}")
            st.markdown("**الاختيارات:**")
            for c in choices:
                st.write(f"• {c}")
            st.markdown(f"**الإجابة الصحيحة:** {correct_answer}")
            st.markdown("**الشرح المختصر:**")
            for piece in explanation.split(" | "):
                st.write(f"• {piece}")

            if st.button("حذف من السجل", key=f"delete_wrong_{item_id}"):
                delete_wrong_answer(item_id)
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# تتبع التقدم
# =========================================================
elif page == "تتبع التقدم":
    st.markdown('<div class="subject-title">تتبع التقدم والنتائج</div>', unsafe_allow_html=True)
    rows = fetch_scores()

    if not rows:
        st.info("لا توجد نتائج محفوظة بعد. أكمل أول محاكاة امتحان ليبدأ تتبع التقدم.")
    else:
        total_count = len(rows)
        avg_perc = round(sum(r[3] for r in rows) / total_count, 2)
        best_perc = max(r[3] for r in rows)
        latest_perc = rows[0][3]

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f'<div class="mini-card"><div class="metric-title">آخر نسبة</div><div class="metric-value">{latest_perc}%</div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div class="mini-card"><div class="metric-title">المتوسط العام</div><div class="metric-value">{avg_perc}%</div></div>',
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f'<div class="mini-card"><div class="metric-title">أفضل نسبة</div><div class="metric-value">{best_perc}%</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">سجل نتائج المحاكاة</div>', unsafe_allow_html=True)

        subject_groups: Dict[str, List[float]] = {}
        for idx, row in enumerate(rows, start=1):
            subject, score, total, percentage, exam_type, created_at = row
            subject_groups.setdefault(subject, []).append(percentage)

            st.markdown(f'<div class="exam-box">', unsafe_allow_html=True)
            st.markdown(f"**#{idx}**")
            st.markdown(f"**المادة:** {subject}")
            st.markdown(f"**نوع التقييم:** {exam_type}")
            st.markdown(f"**الدرجة:** {score} / {total}")
            st.markdown(f"**النسبة:** {percentage}%")
            st.markdown(f"**التاريخ:** {created_at}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("### متوسط الأداء حسب المادة")
        for subject, vals in subject_groups.items():
            avg_sub = round(sum(vals) / len(vals), 2)
            st.write(f"**{subject}**")
            st.progress(avg_sub / 100)
            st.caption(f"متوسط الأداء في هذه المادة: {avg_sub}%")

        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# التذييل
# =========================================================
st.markdown(
    '<div class="footer-note">منصة تعليمية عربية احترافية مصممة لرفع كفاءة طالب الصف الثالث الثانوي — شعبة علمي رياضة.</div>',
    unsafe_allow_html=True,
    )
