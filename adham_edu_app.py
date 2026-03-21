# adham_edu_app.py
from __future__ import annotations

import streamlit as st
import sqlite3
import random
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# =========================================================
# إعدادات التطبيق
# =========================================================
APP_TITLE = "منصة أدهم التعليمية - الصف الثالث الثانوي علمي رياضة"
DB_PATH = "adham_edu_app.db"

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
# تنسيق واجهة المستخدم
# =========================================================
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

def apply_style():
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(180deg, #f8fbff 0%, #eef4fb 100%);
            color: #0d223d;
        }
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0b1f36 0%, #12345a 100%);
            color: white;
        }
        section[data-testid="stSidebar"] * {
            color: white !important;
        }
        .main-card {
            background: white;
            border: 1px solid #d9e6f3;
            border-radius: 22px;
            padding: 20px;
            box-shadow: 0 8px 24px rgba(13, 34, 61, 0.08);
            margin-bottom: 16px;
        }
        .hero-box {
            background: linear-gradient(135deg, #0b1f36 0%, #184a7a 100%);
            color: white;
            border-radius: 24px;
            padding: 28px;
            box-shadow: 0 12px 32px rgba(11, 31, 54, 0.25);
            margin-bottom: 16px;
        }
        .metric-box {
            background: white;
            border: 1px solid #d9e6f3;
            border-radius: 18px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 6px 18px rgba(13, 34, 61, 0.06);
        }
        .small-note {
            color: #4b637f;
            font-size: 0.95rem;
        }
        .subject-title {
            color: #0b1f36;
            font-size: 1.45rem;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .section-title {
            color: #184a7a;
            font-size: 1.15rem;
            font-weight: 700;
            margin-top: 6px;
            margin-bottom: 10px;
        }
        .wrong-box {
            background: #fff8f8;
            border-right: 6px solid #b42318;
            border-radius: 16px;
            padding: 14px;
            margin-bottom: 12px;
            border: 1px solid #f2c7c7;
        }
        .good-box {
            background: #f7fff8;
            border-right: 6px solid #16a34a;
            border-radius: 16px;
            padding: 14px;
            margin-bottom: 12px;
            border: 1px solid #ccecd7;
        }
        .stButton > button {
            border-radius: 14px;
            font-weight: 700;
            border: 1px solid #12345a;
        }
        .stDownloadButton > button {
            border-radius: 14px;
            font-weight: 700;
        }
        .exam-box {
            background: white;
            border: 1px solid #d9e6f3;
            border-radius: 20px;
            padding: 18px;
            margin-bottom: 14px;
            box-shadow: 0 6px 18px rgba(13, 34, 61, 0.05);
        }
        .footer-note {
            text-align: center;
            color: #4b637f;
            padding: 15px 0 5px 0;
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)

apply_style()

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
    percentage = round((score / total) * 100, 2) if total else 0
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO exam_scores (subject, score, total, percentage, exam_type, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        subject,
        score,
        total,
        percentage,
        exam_type,
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
# المحتوى العلمي وملخصات الدروس
# =========================================================
LESSON_SUMMARIES: Dict[str, Dict[str, Any]] = {
    "الرياضيات البحتة - التفاضل والتكامل": {
        "intro": "مراجعة مركزة لأهم القوانين والأفكار الأساسية في التفاضل والتكامل بصورة مناسبة لطالب الصف الثالث الثانوي.",
        "rules": [
            {"title": "قاعدة القوة", "latex": r"\frac{d}{dx}(x^n)=n x^{n-1}", "explanation": "نضرب الأس في المعامل ثم ننقصه واحدًا."},
            {"title": "مشتقة الثابت", "latex": r"\frac{d}{dx}(c)=0", "explanation": "أي عدد ثابت مشتقته تساوي صفرًا."},
            {"title": "مشتقة مجموع دالتين", "latex": r"\frac{d}{dx}(f(x)+g(x))=f'(x)+g'(x)", "explanation": "نفاضل كل حد بمفرده."},
            {"title": "التكامل العكسي", "latex": r"\int x^n\,dx=\frac{x^{n+1}}{n+1}+C \quad (n\neq -1)", "explanation": "نزيد الأس واحدًا ثم نقسم على الأس الجديد."},
            {"title": "تكامل الثابت", "latex": r"\int c\,dx=cx+C", "explanation": "تكامل العدد الثابت يساوي العدد مضروبًا في المتغير."},
        ],
        "key_points": [
            "افهم العلاقة بين التفاضل والتكامل باعتبارهما عمليتين عكسيتين.",
            "ركز على أسئلة التعويض بعد إيجاد المشتقة.",
            "راجع الإشارات جيدًا عند تفاضل الحدود السالبة.",
        ],
    },
    "الرياضيات البحتة - الجبر والهندسة الفراغية": {
        "intro": "ملخص مركز للجبر والهندسة الفراغية مع القواعد التي تتكرر كثيرًا في الامتحانات النهائية.",
        "rules": [
            {"title": "مفكوك ذات الحدين", "latex": r"(a+b)^2=a^2+2ab+b^2", "explanation": "قاعدة أساسية تتكرر في التبسيط وإثبات المتطابقات."},
            {"title": "فرق مربعين", "latex": r"a^2-b^2=(a-b)(a+b)", "explanation": "مهمة في التحليل واختصار الكسور الجبرية."},
            {"title": "المسافة بين نقطتين", "latex": r"d=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}", "explanation": "تستخدم في الهندسة التحليلية والبرهان."},
            {"title": "اتجاه المستقيم", "latex": r"m=\frac{y_2-y_1}{x_2-x_1}", "explanation": "يمثل الميل أو معامل الاتجاه."},
        ],
        "key_points": [
            "لا تبدأ في الحل قبل تحديد المطلوب بدقة: تحليل، تبسيط، أو إثبات.",
            "في الهندسة الفراغية ارسم شكلاً تقريبيًا قبل البدء.",
            "راجع العلاقات بين المستقيمات والمستويات.",
        ],
    },
    "الرياضيات التطبيقية - الاستاتيكا": {
        "intro": "أهم قواعد الاتزان والعزوم وتحليل القوى بصورة مختصرة وعملية.",
        "rules": [
            {"title": "شرط الاتزان الأفقي", "latex": r"\Sigma F_x = 0", "explanation": "مجموع المركبات الأفقية للقوى يساوي صفرًا."},
            {"title": "شرط الاتزان الرأسي", "latex": r"\Sigma F_y = 0", "explanation": "مجموع المركبات الرأسية للقوى يساوي صفرًا."},
            {"title": "شرط اتزان العزوم", "latex": r"\Sigma M = 0", "explanation": "مجموع العزوم حول أي نقطة يساوي صفرًا."},
        ],
        "key_points": [
            "اختر نقطة أخذ العزم بذكاء لتقليل المجهولات.",
            "حدد اتجاه كل قوة قبل التحليل.",
            "راجع وحدات القياس والزوايا بدقة.",
        ],
    },
    "الرياضيات التطبيقية - الديناميكا": {
        "intro": "مراجعة سريعة للحركة في خط مستقيم وقوانين السرعة والعجلة.",
        "rules": [
            {"title": "السرعة", "latex": r"v=\frac{ds}{dt}", "explanation": "السرعة هي معدل تغير الإزاحة بالنسبة للزمن."},
            {"title": "العجلة", "latex": r"a=\frac{dv}{dt}", "explanation": "العجلة هي معدل تغير السرعة بالنسبة للزمن."},
            {"title": "العجلة المنتظمة", "latex": r"v=u+at", "explanation": "علاقة أساسية في الحركة بعجلة ثابتة."},
            {"title": "الإزاحة", "latex": r"s=ut+\frac{1}{2}at^2", "explanation": "لحساب المسافة أو الإزاحة في الحركة المنتظمة العجلة."},
        ],
        "key_points": [
            "ميز بين السرعة الابتدائية والنهائية.",
            "انتبه لإشارة العجلة في حالات التباطؤ.",
            "اكتب المعطيات أولًا ثم حدد القانون المناسب.",
        ],
    },
    "الفيزياء": {
        "intro": "ملخص للقوانين الأساسية التي تتكرر في مسائل الفيزياء لطلاب علمي رياضة.",
        "rules": [
            {"title": "قانون نيوتن الثاني", "latex": r"F=ma", "explanation": "القوة المحصلة تساوي الكتلة في العجلة."},
            {"title": "الشغل", "latex": r"W=F\,d\cos\theta", "explanation": "الشغل يعتمد على القوة والإزاحة والزاوية بينهما."},
            {"title": "القدرة", "latex": r"P=\frac{W}{t}", "explanation": "القدرة هي معدل بذل الشغل."},
            {"title": "قانون أوم", "latex": r"V=IR", "explanation": "العلاقة بين الجهد والتيار والمقاومة."},
        ],
        "key_points": [
            "ارسم مخططًا للمسألة قبل التعويض.",
            "راجع الوحدات وتناسقها في النهاية.",
            "حدد هل المطلوب كمية قياسية أم متجهة.",
        ],
    },
    "الكيمياء": {
        "intro": "مراجعة سريعة لبعض أهم العلاقات والقواعد العامة في الكيمياء.",
        "rules": [
            {"title": "عدد المولات", "latex": r"n=\frac{m}{M}", "explanation": "عدد المولات يساوي الكتلة على الكتلة المولية."},
            {"title": "التركيز المولاري", "latex": r"M=\frac{n}{V}", "explanation": "التركيز المولاري هو عدد المولات لكل لتر محلول."},
            {"title": "الغاز المثالي", "latex": r"PV=nRT", "explanation": "من أشهر العلاقات المستخدمة في مسائل الغازات."},
        ],
        "key_points": [
            "وازن المعادلة الكيميائية قبل البدء في أي حسابات.",
            "تأكد من تحويل الحجم إلى لتر عند الحاجة.",
            "ميز بين الكتلة المولية والكتلة الفعلية للمادة.",
        ],
    },
    "اللغة العربية": {
        "intro": "مراجعة لغوية مركزة في النحو والبلاغة والقراءة والنصوص.",
        "rules": [
            {"title": "إنَّ وأخواتها", "latex": r"\text{تنصب المبتدأ وترفع الخبر}", "explanation": "اسم إن منصوب وخبرها مرفوع."},
            {"title": "كان وأخواتها", "latex": r"\text{ترفع المبتدأ وتنصب الخبر}", "explanation": "تدخل على الجملة الاسمية فتغير حكم الجزأين."},
        ],
        "key_points": [
            "اقرأ السؤال النحوي مرتين وحدد الكلمة المطلوبة قبل الإعراب.",
            "في البلاغة اربط الصورة بالمعنى العام للنص.",
            "راجع مواضع الهمزة والألف اللينة.",
        ],
    },
    "اللغة الإنجليزية": {
        "intro": "مراجعة مركزة في القواعد، المفردات، والقراءة.",
        "rules": [
            {"title": "Present Perfect", "latex": r"\text{S + have/has + P.P}", "explanation": "يستخدم للتعبير عن فعل له أثر في الحاضر."},
            {"title": "If Conditionals", "latex": r"\text{If + present simple, will + infinitive}", "explanation": "حالة الشرط الأولى للتوقعات المستقبلية المحتملة."},
        ],
        "key_points": [
            "انتبه للكلمات الدالة على الزمن قبل اختيار القاعدة.",
            "في القطعة اقرأ الأسئلة أولًا ثم النص.",
            "راجع collocations والمفردات المتكررة في الامتحانات.",
        ],
    },
}

# =========================================================
# بنك الأسئلة
# =========================================================
QUESTION_BANK: Dict[str, List[Dict[str, Any]]] = {
    "الرياضيات البحتة - التفاضل والتكامل": [
        {
            "question": "إذا كانت \( د(x)=x^5 \) فإن \( د'(x) \) تساوي:",
            "choices": ["\(5x^4\)", "\(x^4\)", "\(5x\)", "\(x^6\)"],
            "answer": "\(5x^4\)",
            "explanation": "نطبق قاعدة القوة: نضرب الأس 5 في \(x^{5-1}\)، فتكون المشتقة \(5x^4\)."
        },
        {
            "question": "أوجد مشتقة \( 3x^4 - 2x^2 + 7 \).",
            "choices": ["\(12x^3 - 4x\)", "\(12x^3 - 2x\)", "\(4x^3 - 2x\)", "\(12x^4 - 4x\)"],
            "answer": "\(12x^3 - 4x\)",
            "explanation": "مشتقة \(3x^4\) هي \(12x^3\)، ومشتقة \(-2x^2\) هي \(-4x\)، والثابت صفر."
        },
        {
            "question": "إذا كانت \( y = x^3 + x^2 - 1 \) فأوجد \( y'(2) \).",
            "choices": ["14", "16", "12", "10"],
            "answer": "16",
            "explanation": "أولًا: \(y' = 3x^2 + 2x\)، ثم بالتعويض عن \(x=2\): \(3(4)+4=16\)."
        },
        {
            "question": "تكامل \( x^2 \) بالنسبة إلى \( x \) يساوي:",
            "choices": [r"\(\frac{x^3}{3}+C\)", r"\(2x+C\)", r"\(x^3+C\)", r"\(\frac{x^2}{2}+C\)"],
            "answer": r"\(\frac{x^3}{3}+C\)",
            "explanation": "نزيد الأس واحدًا ثم نقسم على الأس الجديد: \( \int x^2 dx = \frac{x^3}{3}+C \)."
        },
        {
            "question": "مشتقة العدد الثابت 9 تساوي:",
            "choices": ["0", "1", "9", "-9"],
            "answer": "0",
            "explanation": "مشتقة أي ثابت تساوي صفرًا."
        },
    ],
    "الرياضيات البحتة - الجبر والهندسة الفراغية": [
        {
            "question": "تحليل \( x^2 - 9 \) هو:",
            "choices": ["\( (x-3)(x+3) \)", "\( (x-9)(x+1) \)", "\( (x-3)^2 \)", "\( x(x-9) \)"],
            "answer": "\( (x-3)(x+3) \)",
            "explanation": "فرق مربعين: \(x^2-9 = x^2-3^2 = (x-3)(x+3)\)."
        },
        {
            "question": "إذا كان \( (a+b)^2 \) فإن الناتج يساوي:",
            "choices": ["\(a^2+2ab+b^2\)", "\(a^2-b^2\)", "\(a^2+b^2\)", "\(2a+2b\)"],
            "answer": "\(a^2+2ab+b^2\)",
            "explanation": "هذه هي متطابقة مربع مجموع حدين."
        },
        {
            "question": "ميل المستقيم المار بالنقطتين \( (1,2) \) و \( (3,6) \) يساوي:",
            "choices": ["1", "2", "3", "4"],
            "answer": "2",
            "explanation": "الميل \(m = (6-2)/(3-1)=4/2=2\)."
        },
    ],
    "الرياضيات التطبيقية - الاستاتيكا": [
        {
            "question": "في حالة الاتزان الانتقالي أفقيًا فإن:",
            "choices": [r"\(\Sigma F_x = 0\)", r"\(\Sigma F_y = 1\)", r"\(\Sigma M = 1\)", r"\(\Sigma F_x = mg\)"],
            "answer": r"\(\Sigma F_x = 0\)",
            "explanation": "شرط الاتزان الأفقي أن يكون مجموع المركبات الأفقية صفرًا."
        },
        {
            "question": "شرط اتزان العزوم حول نقطة ما هو:",
            "choices": [r"\(\Sigma M = 0\)", r"\(\Sigma F = 0\)", r"\(M = Fd\) فقط", r"\(\Sigma R = 1\)"],
            "answer": r"\(\Sigma M = 0\)",
            "explanation": "حتى يتحقق الاتزان الدوراني يجب أن يكون مجموع العزوم صفرًا."
        },
    ],
    "الرياضيات التطبيقية - الديناميكا": [
        {
            "question": "إذا كانت العجلة منتظمة فإن العلاقة الصحيحة هي:",
            "choices": [r"\(v=u+at\)", r"\(v=u-at^2\)", r"\(s=vt\) فقط دائمًا", r"\(a=uv\)"],
            "answer": r"\(v=u+at\)",
            "explanation": "هذه هي العلاقة الأساسية بين السرعة الابتدائية والنهائية والزمن والعجلة."
        },
        {
            "question": "العجلة تساوي:",
            "choices": [r"\(\frac{dv}{dt}\)", r"\(\frac{ds}{dt}\)", r"\(vt\)", r"\(\frac{dt}{dv}\)"],
            "answer": r"\(\frac{dv}{dt}\)",
            "explanation": "العجلة هي المعدل الزمني لتغير السرعة."
        },
    ],
    "الفيزياء": [
        {
            "question": "القوة المحصلة تساوي:",
            "choices": ["\(F=ma\)", "\(V=IR\)", "\(P=W/t\)", "\(W=Fd\cos\\theta\)"],
            "answer": "\(F=ma\)",
            "explanation": "هذا هو قانون نيوتن الثاني."
        },
        {
            "question": "قانون أوم هو:",
            "choices": ["\(V=IR\)", "\(F=ma\)", "\(P=VI^2\)", "\(R=IV\)"],
            "answer": "\(V=IR\)",
            "explanation": "العلاقة بين فرق الجهد والتيار والمقاومة هي \(V=IR\)."
        },
        {
            "question": "القدرة تساوي:",
            "choices": ["\(P=W/t\)", "\(P=F/t\)", "\(P=ma\)", "\(P=IR\)"],
            "answer": "\(P=W/t\)",
            "explanation": "القدرة هي معدل بذل الشغل بالنسبة للزمن."
        },
    ],
    "الكيمياء": [
        {
            "question": "عدد المولات يساوي:",
            "choices": [r"\(n=\frac{m}{M}\)", r"\(n=mM\)", r"\(n=\frac{M}{m}\)", r"\(n=PV\)"],
            "answer": r"\(n=\frac{m}{M}\)",
            "explanation": "عدد المولات = الكتلة ÷ الكتلة المولية."
        },
        {
            "question": "قانون الغاز المثالي هو:",
            "choices": ["\(PV=nRT\)", "\(V=IR\)", "\(M=n/V\)", "\(W=Fd\)"],
            "answer": "\(PV=nRT\)",
            "explanation": "هذا هو القانون العام للغازات المثالية."
        },
    ],
    "اللغة العربية": [
        {
            "question": "إنَّ وأخواتها:",
            "choices": [
                "تنصب المبتدأ وترفع الخبر",
                "ترفع المبتدأ وتنصب الخبر",
                "تنصب الفاعل",
                "تجزم الفعلين"
            ],
            "answer": "تنصب المبتدأ وترفع الخبر",
            "explanation": "اسم إن منصوب وخبرها مرفوع."
        },
        {
            "question": "كان وأخواتها:",
            "choices": [
                "ترفع المبتدأ وتنصب الخبر",
                "تنصب المبتدأ وترفع الخبر",
                "تجزم المضارع",
                "لا تؤثر في الجملة"
            ],
            "answer": "ترفع المبتدأ وتنصب الخبر",
            "explanation": "تدخل على الجملة الاسمية فترفع الاسم وتنصب الخبر."
        },
    ],
    "اللغة الإنجليزية": [
        {
            "question": "Choose the correct form: She _____ finished her homework.",
            "choices": ["has", "have", "had", "is"],
            "answer": "has",
            "explanation": "With 'She' in the present perfect, we use 'has'."
        },
        {
            "question": "First conditional structure is:",
            "choices": [
                "If + present simple, will + infinitive",
                "If + past simple, would + infinitive",
                "If + present simple, present simple",
                "If + past perfect, would have + P.P."
            ],
            "answer": "If + present simple, will + infinitive",
            "explanation": "This is the structure of the first conditional."
        },
    ],
}

# =========================================================
# الامتحانات الكاملة
# =========================================================
MOCK_EXAMS: Dict[str, List[Dict[str, Any]]] = {
    "الرياضيات البحتة - التفاضل والتكامل": QUESTION_BANK["الرياضيات البحتة - التفاضل والتكامل"] + [
        {
            "question": "إذا كانت \( f(x)=2x^3 \) فإن \( f'(x) \) تساوي:",
            "choices": ["\(6x^2\)", "\(2x^2\)", "\(3x^2\)", "\(6x^3\)"],
            "answer": "\(6x^2\)",
            "explanation": "نشتق \(2x^3\): المعامل 2 ثابت، ومشتقة \(x^3\) هي \(3x^2\)."
        },
        {
            "question": "تكامل \( 5 \) بالنسبة إلى \(x\) يساوي:",
            "choices": ["\(5x + C\)", "\(5 + C\)", "\(x^5 + C\)", "\(0\)"],
            "answer": "\(5x + C\)",
            "explanation": "تكامل الثابت \(c\) هو \(cx + C\)."
        },
        {
            "question": "إذا كانت \( y = 4x^2 \) فأوجد \( y'(1) \).",
            "choices": ["4", "8", "2", "16"],
            "answer": "8",
            "explanation": "المشتقة \(y' = 8x\)، وعند \(x=1\) تكون \(8\)."
        },
    ],
    "الفيزياء": QUESTION_BANK["الفيزياء"] + [
        {
            "question": "إذا أثرت قوة مقدارها 10 نيوتن على جسم كتلته 2 كجم، فإن العجلة تساوي:",
            "choices": ["5 م/ث²", "10 م/ث²", "2 م/ث²", "20 م/ث²"],
            "answer": "5 م/ث²",
            "explanation": "من \(F=ma\) إذن \(a=F/m = 10/2 = 5\)."
        },
        {
            "question": "وحدة القدرة هي:",
            "choices": ["وات", "جول", "أوم", "كولوم"],
            "answer": "وات",
            "explanation": "الوحدة القياسية للقدرة هي الوات."
        },
    ],
    "الكيمياء": QUESTION_BANK["الكيمياء"] + [
        {
            "question": "إذا كانت كتلة المادة 18 جم وكتلتها المولية 18 جم/مول، فإن عدد المولات يساوي:",
            "choices": ["1", "18", "0.5", "2"],
            "answer": "1",
            "explanation": "عدد المولات = 18 ÷ 18 = 1 مول."
        },
        {
            "question": "إذا زاد عدد المولات في قانون الغاز المثالي عند ثبوت باقي العوامل، فإن الضغط:",
            "choices": ["يزداد", "يقل", "ينعدم", "لا يتغير"],
            "answer": "يزداد",
            "explanation": "من العلاقة \(PV=nRT\)، بزيادة \(n\) يزداد \(P\) إذا ثبتت باقي العوامل."
        },
    ],
}

# =========================================================
# أدوات مساعدة
# =========================================================
def ensure_session_state():
    defaults = {
        "selected_subject": SUBJECTS[0],
        "quiz_pool": [],
        "quiz_answers_submitted": False,
        "quiz_selected_answers": {},
        "exam_subject": "الرياضيات البحتة - التفاضل والتكامل",
        "exam_questions": [],
        "exam_selected_answers": {},
        "exam_started": False,
        "exam_submitted": False,
        "exam_start_time": None,
        "exam_duration_seconds": 3 * 60 * 60,
        "last_exam_result": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

ensure_session_state()

def start_new_quiz(subject: str, count: int = 5):
    bank = QUESTION_BANK.get(subject, [])
    if not bank:
        st.session_state.quiz_pool = []
        return
    sample_count = min(count, len(bank))
    st.session_state.quiz_pool = random.sample(bank, sample_count)
    st.session_state.quiz_answers_submitted = False
    st.session_state.quiz_selected_answers = {}

def start_exam(subject: str):
    bank = MOCK_EXAMS.get(subject) or QUESTION_BANK.get(subject, [])
    if not bank:
        st.session_state.exam_questions = []
        return
    st.session_state.exam_subject = subject
    st.session_state.exam_questions = random.sample(bank, min(len(bank), 8))
    st.session_state.exam_selected_answers = {}
    st.session_state.exam_started = True
    st.session_state.exam_submitted = False
    st.session_state.exam_start_time = time.time()
    st.session_state.last_exam_result = None

def format_time(seconds_left: int) -> str:
    hours = max(seconds_left, 0) // 3600
    minutes = (max(seconds_left, 0) % 3600) // 60
    seconds = max(seconds_left, 0) % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def calculate_result(questions: List[Dict[str, Any]], selected_answers: Dict[str, str]):
    total = len(questions)
    score = 0
    details = []

    for idx, q in enumerate(questions):
        qid = f"q_{idx}"
        selected = selected_answers.get(qid)
        correct = selected == q["answer"]
        if correct:
            score += 1
        details.append({
            "question": q["question"],
            "selected": selected,
            "correct_answer": q["answer"],
            "correct": correct,
            "explanation": q["explanation"],
            "choices": q["choices"],
        })
    return score, total, details

def metric_row():
    scores = fetch_scores()
    total_exams = len(scores)
    avg_percentage = round(sum([s[3] for s in scores]) / total_exams, 2) if total_exams else 0.0
    wrong_total = len(fetch_wrong_answers())

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size:0.95rem;color:#4b637f;">عدد المحاكاة المنجزة</div>
            <div style="font-size:1.8rem;font-weight:800;color:#0b1f36;">{total_exams}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size:0.95rem;color:#4b637f;">متوسط الدرجات</div>
            <div style="font-size:1.8rem;font-weight:800;color:#0b1f36;">{avg_percentage}%</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size:0.95rem;color:#4b637f;">الأسئلة المؤجلة للمراجعة</div>
            <div style="font-size:1.8rem;font-weight:800;color:#0b1f36;">{wrong_total}</div>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# الواجهة الرئيسية
# =========================================================
with st.sidebar:
    st.markdown("## المنصة التعليمية")
    page = st.radio(
        "التنقل",
        [
            "الرئيسية",
            "ملخصات الدروس",
            "بنك الأسئلة التفاعلي",
            "قاعة محاكاة الامتحان",
            "المراجعة لاحقًا",
            "تتبع التقدم",
        ],
        index=0,
    )
    st.markdown("---")
    selected_subject = st.selectbox("اختر المادة", SUBJECTS, index=0)
    st.session_state.selected_subject = selected_subject
    st.markdown("---")
    st.caption("تصميم هادئ احترافي مناسب للمذاكرة المركزة")

# =========================================================
# الصفحة الرئيسية
# =========================================================
if page == "الرئيسية":
    st.markdown(f"""
    <div class="hero-box">
        <div style="font-size:2rem;font-weight:800;">{APP_TITLE}</div>
        <div style="margin-top:10px;font-size:1.05rem;line-height:1.9;">
            منصة تعليمية عملية للطالب في الصف الثالث الثانوي – شعبة علمي رياضة، 
            تجمع بين الملخصات المركزة، الأسئلة التفاعلية، ومحاكاة الامتحان النهائي.
        </div>
    </div>
    """, unsafe_allow_html=True)

    metric_row()

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("### ما الذي ستجده داخل المنصة؟")
    st.write("• ملخصات مركزة لأهم القوانين والقواعد في كل مادة.")
    st.write("• بنك أسئلة اختيار من متعدد مع تصحيح فوري وشرح لكل إجابة.")
    st.write("• قاعة امتحان بمحاكاة زمنية وتقدير للدرجة النهائية.")
    st.write("• سجل خاص بالأسئلة التي أُجيب عنها خطأ للعودة إليها لاحقًا.")
    st.write("• قاعدة بيانات محلية لحفظ نتائج المحاكاة وتتبع التحسن مع الوقت.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("### توجيه دراسي سريع")
    st.info(
        "ابدأ من ملخص المادة، ثم انتقل مباشرة إلى بنك الأسئلة، وبعد تثبيت القواعد "
        "ادخل قاعة محاكاة الامتحان لقياس مستواك الحقيقي."
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
        st.warning("لا توجد ملخصات مضافة لهذه المادة حاليًا.")
    else:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### نظرة عامة")
        st.write(content["intro"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### أهم القوانين والقواعد")
        for item in content["rules"]:
            st.markdown(f"**{item['title']}**")
            st.latex(item["latex"])
            st.caption(item["explanation"])
            st.markdown("---")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### ملاحظات ذهبية")
        for point in content["key_points"]:
            st.write(f"• {point}")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# بنك الأسئلة التفاعلي
# =========================================================
elif page == "بنك الأسئلة التفاعلي":
    subject = st.session_state.selected_subject
    st.markdown(f'<div class="subject-title">بنك الأسئلة التفاعلي — {subject}</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1])
    with col_a:
        quiz_count = st.selectbox("عدد أسئلة الجلسة", [3, 5, 7, 10], index=1)
    with col_b:
        if st.button("توليد جلسة أسئلة جديدة", use_container_width=True):
            start_new_quiz(subject, quiz_count)

    if not st.session_state.quiz_pool:
        start_new_quiz(subject, quiz_count)

    quiz_questions = st.session_state.quiz_pool

    if not quiz_questions:
        st.warning("لا توجد أسئلة متاحة لهذه المادة حاليًا.")
    else:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### أجب عن الأسئلة ثم اضغط تصحيح")
        with st.form("quiz_form"):
            for idx, q in enumerate(quiz_questions):
                qid = f"quiz_{idx}"
                st.markdown(f"**السؤال {idx + 1}:** {q['question']}")
                choice = st.radio(
                    f"اختر الإجابة الصحيحة للسؤال {idx + 1}",
                    q["choices"],
                    key=f"radio_{qid}",
                    index=None,
                )
                st.session_state.quiz_selected_answers[qid] = choice
                st.markdown("---")

            submitted = st.form_submit_button("تصحيح الإجابات")

        if submitted:
            st.session_state.quiz_answers_submitted = True

        if st.session_state.quiz_answers_submitted:
            score = 0
            total = len(quiz_questions)

            st.markdown("### النتيجة والتغذية الراجعة")
            for idx, q in enumerate(quiz_questions):
                qid = f"quiz_{idx}"
                selected = st.session_state.quiz_selected_answers.get(qid)
                correct = selected == q["answer"]

                if correct:
                    score += 1
                    st.markdown(
                        f'<div class="good-box"><b>السؤال {idx + 1}:</b> إجابة صحيحة.<br>'
                        f'<b>الشرح:</b> {q["explanation"]}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div class="wrong-box"><b>السؤال {idx + 1}:</b> إجابة غير صحيحة.<br>'
                        f'<b>إجابتك:</b> {selected if selected else "لم يتم اختيار إجابة"}<br>'
                        f'<b>الإجابة الصحيحة:</b> {q["answer"]}<br>'
                        f'<b>الشرح:</b> {q["explanation"]}</div>',
                        unsafe_allow_html=True
                    )
                    save_wrong_answer(
                        subject=subject,
                        question_text=q["question"],
                        choices=q["choices"],
                        correct_answer=q["answer"],
                        explanation=q["explanation"],
                        source_type="quiz"
                    )

            percentage = round((score / total) * 100, 2) if total else 0
            st.progress(percentage / 100)
            st.success(f"درجتك في هذه الجلسة: {score} من {total} — بنسبة {percentage}%")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# قاعة محاكاة الامتحان
# =========================================================
elif page == "قاعة محاكاة الامتحان":
    st.markdown('<div class="subject-title">قاعة محاكاة الامتحان النهائي</div>', unsafe_allow_html=True)

    available_exam_subjects = list(MOCK_EXAMS.keys())
    exam_subject = st.selectbox(
        "اختر مادة المحاكاة",
        available_exam_subjects,
        index=0 if st.session_state.exam_subject not in available_exam_subjects else available_exam_subjects.index(st.session_state.exam_subject)
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("بدء امتحان جديد", use_container_width=True):
            start_exam(exam_subject)
            st.rerun()
    with col2:
        st.info("زمن الامتحان الافتراضي: 3 ساعات")

    if st.session_state.exam_started and st.session_state.exam_subject == exam_subject:
        elapsed = int(time.time() - st.session_state.exam_start_time) if st.session_state.exam_start_time else 0
        remaining = st.session_state.exam_duration_seconds - elapsed

        top1, top2, top3 = st.columns([1, 1, 2])
        with top1:
            st.metric("المادة", st.session_state.exam_subject)
        with top2:
            st.metric("الوقت المتبقي", format_time(remaining))
        with top3:
            st.progress(max(0, remaining) / st.session_state.exam_duration_seconds)

        if remaining <= 0 and not st.session_state.exam_submitted:
            st.warning("انتهى زمن الامتحان. تم الانتقال إلى التصحيح النهائي.")
            st.session_state.exam_submitted = True

        exam_questions = st.session_state.exam_questions
        if exam_questions:
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            st.markdown("### نموذج الامتحان")
            for idx, q in enumerate(exam_questions):
                qid = f"q_{idx}"
                st.markdown(f'<div class="exam-box">', unsafe_allow_html=True)
                st.markdown(f"**السؤال {idx + 1}:** {q['question']}")
                ans = st.radio(
                    f"إجابة السؤال {idx + 1}",
                    q["choices"],
                    key=f"exam_radio_{qid}",
                    index=None,
                    disabled=st.session_state.exam_submitted
                )
                if ans is not None:
                    st.session_state.exam_selected_answers[qid] = ans
                st.markdown("</div>", unsafe_allow_html=True)

            if not st.session_state.exam_submitted:
                if st.button("تسليم الامتحان", type="primary", use_container_width=True):
                    st.session_state.exam_submitted = True
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

            if st.session_state.exam_submitted:
                score, total, details = calculate_result(
                    st.session_state.exam_questions,
                    st.session_state.exam_selected_answers
                )
                percentage = round((score / total) * 100, 2) if total else 0
                st.session_state.last_exam_result = (score, total, percentage, details)

                save_exam_score(
                    subject=st.session_state.exam_subject,
                    score=score,
                    total=total,
                    exam_type="محاكاة نهائية"
                )

                st.markdown('<div class="main-card">', unsafe_allow_html=True)
                st.markdown("### النتيجة النهائية")
                st.progress(percentage / 100)
                st.success(f"الدرجة: {score} من {total} — النسبة {percentage}%")

                if percentage >= 85:
                    st.balloons()
                    st.info("ممتاز جدًا. استمر على نفس المستوى مع زيادة التنوع في التدريب.")
                elif percentage >= 65:
                    st.info("أداء جيد، لكن ما زالت هناك أجزاء تحتاج إلى تثبيت بالمزيد من المراجعة.")
                else:
                    st.warning("يحتاج المستوى إلى مراجعة مركزة، خصوصًا في الأسئلة التي ظهرت بها أخطاء.")

                st.markdown("### تحليل الأسئلة")
                for i, item in enumerate(details, start=1):
                    if item["correct"]:
                        st.markdown(
                            f'<div class="good-box"><b>السؤال {i}:</b> صحيح.<br>'
                            f'<b>الشرح:</b> {item["explanation"]}</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="wrong-box"><b>السؤال {i}:</b> غير صحيح.<br>'
                            f'<b>إجابتك:</b> {item["selected"] if item["selected"] else "لم يتم اختيار إجابة"}<br>'
                            f'<b>الإجابة الصحيحة:</b> {item["correct_answer"]}<br>'
                            f'<b>الشرح:</b> {item["explanation"]}</div>',
                            unsafe_allow_html=True
                        )
                        save_wrong_answer(
                            subject=st.session_state.exam_subject,
                            question_text=item["question"],
                            choices=item["choices"],
                            correct_answer=item["correct_answer"],
                            explanation=item["explanation"],
                            source_type="exam"
                        )
                st.markdown("</div>", unsafe_allow_html=True)

        if not st.session_state.exam_submitted:
            time.sleep(1)
            st.rerun()

    else:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.write("ابدأ امتحانًا جديدًا من الأعلى لمحاكاة اختبار نهائي كامل بزمن تنازلي وتصحيح آلي.")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# المراجعة لاحقًا
# =========================================================
elif page == "المراجعة لاحقًا":
    st.markdown('<div class="subject-title">الأسئلة المؤجلة للمراجعة</div>', unsafe_allow_html=True)

    filter_subject = st.selectbox("تصفية حسب المادة", ["كل المواد"] + SUBJECTS)
    rows = fetch_wrong_answers(None if filter_subject == "كل المواد" else filter_subject)

    if not rows:
        st.info("لا توجد أسئلة محفوظة للمراجعة حاليًا.")
    else:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown(f"### عدد الأسئلة المحفوظة: {len(rows)}")
        for row in rows:
            item_id, subject, q_text, choices_json, correct_answer, explanation, source_type, created_at = row
            choices = json.loads(choices_json)

            st.markdown(
                f"""
                <div class="wrong-box">
                    <b>المادة:</b> {subject}<br>
                    <b>المصدر:</b> {source_type}<br>
                    <b>تاريخ الحفظ:</b> {created_at}<br><br>
                    <b>السؤال:</b> {q_text}<br><br>
                    <b>الاختيارات:</b>
                    <ul>
                        {''.join([f"<li>{c}</li>" for c in choices])}
                    </ul>
                    <b>الإجابة الصحيحة:</b> {correct_answer}<br>
                    <b>الشرح:</b> {explanation}
                </div>
                """,
                unsafe_allow_html=True
            )

            colx, coly = st.columns([1, 5])
            with colx:
                if st.button("حذف", key=f"del_{item_id}"):
                    delete_wrong_answer(item_id)
                    st.rerun()
            with coly:
                st.caption("بعد مراجعة السؤال وحله جيدًا يمكنك حذفه من القائمة.")
            st.markdown("---")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# تتبع التقدم
# =========================================================
elif page == "تتبع التقدم":
    st.markdown('<div class="subject-title">تتبع مستوى التقدم</div>', unsafe_allow_html=True)
    rows = fetch_scores()

    if not rows:
        st.info("لا توجد نتائج محفوظة بعد. أدخل قاعة محاكاة الامتحان وسجّل أول نتيجة.")
    else:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### آخر النتائج المسجلة")

        subjects_summary: Dict[str, List[float]] = {}
        for subject, score, total, percentage, exam_type, created_at in rows:
            subjects_summary.setdefault(subject, []).append(percentage)

        latest_percentage = rows[0][3]
        avg_percentage = round(sum([r[3] for r in rows]) / len(rows), 2)
        best_percentage = max([r[3] for r in rows])

        c1, c2, c3 = st.columns(3)
        c1.metric("آخر نسبة", f"{latest_percentage}%")
        c2.metric("المتوسط العام", f"{avg_percentage}%")
        c3.metric("أفضل نسبة", f"{best_percentage}%")

        st.markdown("### سجل المحاكاة")
        for idx, row in enumerate(rows, start=1):
            subject, score, total, percentage, exam_type, created_at = row
            st.markdown(
                f"""
                <div class="exam-box">
                    <b>#{idx}</b><br>
                    <b>المادة:</b> {subject}<br>
                    <b>نوع التقييم:</b> {exam_type}<br>
                    <b>الدرجة:</b> {score} / {total}<br>
                    <b>النسبة:</b> {percentage}%<br>
                    <b>التاريخ:</b> {created_at}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("### متوسط كل مادة")
        for sub, vals in subjects_summary.items():
            avg_sub = round(sum(vals) / len(vals), 2)
            st.write(f"**{sub}**")
            st.progress(min(avg_sub / 100, 1.0))
            st.caption(f"متوسط الأداء في هذه المادة: {avg_sub}%")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# تذييل
# =========================================================
st.markdown(
    '<div class="footer-note">تم تصميم هذه المنصة لتوفير تجربة دراسة عربية هادئة ومنظمة للصف الثالث الثانوي – علمي رياضة.</div>',
    unsafe_allow_html=True
)
