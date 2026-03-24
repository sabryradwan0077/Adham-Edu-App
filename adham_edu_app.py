# -*- coding: utf-8 -*-
from __future__ import annotations

import time
import re
from typing import Dict, List, Any, Optional

import pandas as pd
import streamlit as st

# =========================================================
# منصة أدهم صبري التعليمية
# =========================================================
APP_NAME = "منصة أدهم صبري التعليمية"
APP_ICON = "🎓"

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# تنسيقات الواجهة
# =========================================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #07111f 0%, #0c1930 100%);
        color: #f4f7fb;
        direction: rtl;
        text-align: right;
    }

    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
    }

    .main-title {
        font-size: 2.5rem;
        font-weight: 900;
        color: #ffffff;
        text-align: center;
        margin-bottom: 0.3rem;
    }

    .sub-title {
        font-size: 1.05rem;
        text-align: center;
        color: #d6deea;
        margin-bottom: 1.5rem;
    }

    .hero-card {
        background: linear-gradient(135deg, rgba(21,33,60,0.97), rgba(11,20,37,0.97));
        padding: 22px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.09);
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        margin-bottom: 18px;
    }

    .exam-box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 18px;
        padding: 22px;
        margin-top: 14px;
        margin-bottom: 14px;
    }

    .question-badge {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        background: #12365f;
        color: #ffffff;
        font-size: 0.95rem;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .question-text {
        font-size: 1.45rem;
        line-height: 2.15;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 20px;
    }

    .subject-chip {
        display: inline-block;
        margin-left: 8px;
        margin-bottom: 8px;
        padding: 7px 13px;
        border-radius: 999px;
        background: rgba(72, 153, 255, 0.16);
        color: #dbe9ff;
        font-weight: 800;
        font-size: 0.92rem;
    }

    .timer-box {
        padding: 14px 18px;
        border-radius: 14px;
        font-size: 1.25rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 15px;
    }

    .timer-safe {
        background: rgba(42, 157, 87, 0.16);
        border: 1px solid rgba(42, 157, 87, 0.45);
        color: #bff5cf;
    }

    .timer-mid {
        background: rgba(244, 162, 97, 0.16);
        border: 1px solid rgba(244, 162, 97, 0.45);
        color: #ffe0bc;
    }

    .timer-danger {
        background: rgba(231, 111, 81, 0.18);
        border: 1px solid rgba(231, 111, 81, 0.50);
        color: #ffd1c6;
    }

    .feedback-success {
        background: rgba(42, 157, 87, 0.16);
        border: 1px solid rgba(42, 157, 87, 0.45);
        color: #d9ffe6;
        padding: 16px;
        border-radius: 14px;
        font-weight: 800;
        margin-top: 12px;
        margin-bottom: 12px;
        line-height: 1.9;
    }

    .feedback-error {
        background: rgba(231, 111, 81, 0.18);
        border: 1px solid rgba(231, 111, 81, 0.50);
        color: #ffe1da;
        padding: 16px;
        border-radius: 14px;
        font-weight: 800;
        margin-top: 12px;
        margin-bottom: 12px;
        line-height: 1.9;
    }

    .info-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 10px;
    }

    .resource-card {
        background: rgba(255,255,255,0.05);
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.10);
        padding: 16px;
        margin-bottom: 12px;
    }

    .search-title {
        font-size: 1.2rem;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 0.6rem;
    }

    .small-note {
        color: #c5cfdb;
        font-size: 0.95rem;
    }

    .metric-card {
        background: rgba(255,255,255,0.05);
        padding: 16px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.08);
        text-align: center;
    }

    div[data-baseweb="radio"] label {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 12px;
        width: 100%;
        transition: 0.2s ease;
    }

    div[data-baseweb="radio"] label:hover {
        border-color: #6ea8fe;
        background: rgba(110,168,254,0.12);
    }

    div[data-baseweb="radio"] label div {
        font-size: 1.22rem !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        line-height: 2 !important;
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        font-size: 1rem;
        font-weight: 900;
        padding: 0.82rem 1rem;
    }

    .stDownloadButton > button {
        width: 100%;
        border-radius: 12px;
        font-size: 1rem;
        font-weight: 900;
        padding: 0.82rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# دوال مساعدة
# =========================================================
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

def parse_remote_questions_from_csv(url: str) -> List[Dict[str, Any]]:
    try:
        df = pd.read_csv(url)
        required = {
            "subject", "unit", "difficulty", "question",
            "option_a", "option_b", "option_c", "option_d",
            "answer", "explanation"
        }
        if not required.issubset(set(df.columns)):
            return []

        records = []
        for _, row in df.iterrows():
            records.append({
                "subject": str(row.get("subject", "")).strip(),
                "unit": str(row.get("unit", "")).strip(),
                "difficulty": str(row.get("difficulty", "متوسط")).strip(),
                "question": str(row.get("question", "")).strip(),
                "options": [
                    f"أ) {str(row.get('option_a', '')).strip()}",
                    f"ب) {str(row.get('option_b', '')).strip()}",
                    f"ج) {str(row.get('option_c', '')).strip()}",
                    f"د) {str(row.get('option_d', '')).strip()}",
                ],
                "answer": str(row.get("answer", "")).strip(),
                "explanation": str(row.get("explanation", "")).strip(),
                "time_limit_sec": int(row.get("time_limit_sec", 60)) if str(row.get("time_limit_sec", "")).strip() else 60
            })
        return [q for q in records if q["question"] and len(q["options"]) == 4 and q["answer"]]
    except Exception:
        return []

def make_question(
    subject: str,
    unit: str,
    difficulty: str,
    question: str,
    options: List[str],
    answer: str,
    explanation: str,
    time_limit_sec: int
) -> Dict[str, Any]:
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

# =========================================================
# بنك الأسئلة المدمج - 40 سؤالًا
# =========================================================
def get_builtin_questions() -> List[Dict[str, Any]]:
    questions = [
        # الفيزياء
        make_question(
            "الفيزياء", "التيار الكهربي", "سهل",
            "إذا مر تيار شدته 2 أمبير في سلك لمدة 5 ثوانٍ، فما مقدار الشحنة الكهربية المارة؟",
            ["أ) 2 كولوم", "ب) 5 كولوم", "ج) 10 كولوم", "د) 20 كولوم"],
            "ج",
            "نطبق العلاقة: الشحنة = شدة التيار × الزمن، إذن الشحنة = 2 × 5 = 10 كولوم.",
            45
        ),
        make_question(
            "الفيزياء", "قانون أوم", "سهل",
            "مقاومة مقدارها 4 أوم موصلة بفرق جهد 12 فولت، فما شدة التيار المار فيها؟",
            ["أ) 2 أمبير", "ب) 3 أمبير", "ج) 4 أمبير", "د) 6 أمبير"],
            "ب",
            "طبقًا لقانون أوم: شدة التيار = فرق الجهد ÷ المقاومة = 12 ÷ 4 = 3 أمبير.",
            45
        ),
        make_question(
            "الفيزياء", "قوانين كيرشوف", "متوسط",
            "ينص قانون كيرشوف الأول على أن المجموع الجبري للتيارات عند نقطة التقاء يساوي:",
            ["أ) المقاومة", "ب) الجهد", "ج) صفر", "د) مالا نهاية"],
            "ج",
            "لأن مجموع التيارات الداخلة إلى العقدة يساوي مجموع التيارات الخارجة منها، فيكون المجموع الجبري صفراً.",
            50
        ),
        make_question(
            "الفيزياء", "القدرة الكهربية", "متوسط",
            "سخان كهربي يعمل عند فرق جهد 220 فولت وشدة تيار 5 أمبير، فما قدرته؟",
            ["أ) 44 وات", "ب) 220 وات", "ج) 1100 وات", "د) 4400 وات"],
            "ج",
            "القدرة = فرق الجهد × شدة التيار = 220 × 5 = 1100 وات.",
            50
        ),
        make_question(
            "الفيزياء", "الفيض المغناطيسي", "متوسط",
            "يعتمد الفيض المغناطيسي المار خلال سطح على:",
            ["أ) شدة المجال فقط", "ب) المساحة فقط", "ج) شدة المجال والمساحة والزاوية", "د) الزمن فقط"],
            "ج",
            "لأن الفيض المغناطيسي Φ = B A cosθ، لذلك يعتمد على شدة المجال والمساحة والزاوية.",
            55
        ),
        make_question(
            "الفيزياء", "الحث الكهرومغناطيسي", "متوسط",
            "تزداد القوة الدافعة الكهربية المستحثة في ملف عندما:",
            ["أ) يزداد معدل تغير الفيض المغناطيسي", "ب) يبقى الملف ساكنًا دائمًا", "ج) تنعدم المقاومة فقط", "د) يقل عدد الإلكترونات"],
            "أ",
            "وفق قانون فاراداي فإن القوة الدافعة الكهربية المستحثة تتناسب مع معدل تغير الفيض المغناطيسي.",
            55
        ),
        make_question(
            "الفيزياء", "السعة الكهربية", "صعب",
            "إذا تضاعفت مساحة لوحي مكثف مستوي مع ثبات المسافة بينهما، فإن السعة الكهربية:",
            ["أ) تقل إلى النصف", "ب) تظل ثابتة", "ج) تتضاعف", "د) تصبح أربعة أمثال"],
            "ج",
            "لأن السعة C = εA/d، فإذا تضاعفت المساحة A مع ثبات d فإن السعة تتضاعف.",
            60
        ),
        make_question(
            "الفيزياء", "التأثير الكهروضوئي", "صعب",
            "عند زيادة تردد الضوء الساقط فوق التردد الحرج، فإن أقصى طاقة حركية للإلكترونات المنبعثة:",
            ["أ) تقل", "ب) تساوي صفرًا", "ج) تزداد", "د) لا تتأثر مطلقًا"],
            "ج",
            "طبقًا لمعادلة أينشتاين: تزداد الطاقة الحركية بزيادة تردد الضوء إذا كان أكبر من التردد الحرج.",
            65
        ),
        make_question(
            "الفيزياء", "نموذج بور", "صعب",
            "في نموذج بور للذرة، يشع الإلكترون طاقة عندما:",
            ["أ) يبقى في نفس المدار", "ب) ينتقل إلى مستوى طاقة أقل", "ج) تزداد سرعته فقط", "د) يصطدم بالنيوترونات"],
            "ب",
            "يشع الإلكترون طاقة عندما ينتقل من مستوى طاقة أعلى إلى مستوى طاقة أقل.",
            60
        ),
        make_question(
            "الفيزياء", "الفيزياء النووية", "صعب",
            "تتميز جسيمات ألفا بقدرة اختراق ضعيفة لأن:",
            ["أ) ليس لها كتلة", "ب) لها شحنة كبيرة وكتلة نسبية كبيرة", "ج) سرعتها أقل من الضوء فقط", "د) متعادلة كهربياً"],
            "ب",
            "لأن جسيمات ألفا ذات شحنة كبيرة وكتلة كبيرة نسبيًا، فتفقد طاقتها بسرعة عند مرورها في المادة.",
            70
        ),

        # الرياضيات
        make_question(
            "الرياضيات", "التفاضل", "سهل",
            "ما مشتقة الدالة س = x² ؟",
            ["أ) x", "ب) 2x", "ج) x³", "د) 2"],
            "ب",
            "باستخدام قاعدة القوة: مشتقة x² تساوي 2x.",
            40
        ),
        make_question(
            "الرياضيات", "التكامل", "سهل",
            "ما قيمة التكامل ∫ 3x² dx ؟",
            ["أ) x³ + ثابت", "ب) 3x³ + ثابت", "ج) x² + ثابت", "د) 6x + ثابت"],
            "أ",
            "تكامل 3x² يساوي x³ + ثابت.",
            45
        ),
        make_question(
            "الرياضيات", "حساب المثلثات", "سهل",
            "قيمة جا 90° تساوي:",
            ["أ) 0", "ب) 1/2", "ج) 1", "د) -1"],
            "ج",
            "القيمة المعلومة في حساب المثلثات هي جا 90° = 1.",
            35
        ),
        make_question(
            "الرياضيات", "النهايات", "متوسط",
            "النهاية عندما x تقترب من 1 للتعبير (x² − 1) ÷ (x − 1) تساوي:",
            ["أ) 0", "ب) 1", "ج) 2", "د) غير معرفة"],
            "ج",
            "نفكك x² − 1 إلى (x − 1)(x + 1)، ثم نختصر فنحصل على x + 1، وعند x = 1 تكون النهاية 2.",
            55
        ),
        make_question(
            "الرياضيات", "تطبيقات التفاضل", "متوسط",
            "إذا كانت الدالة د(س) = x³ − 3x فإن مشتقتها هي:",
            ["أ) 3x² − 3", "ب) x² − 3", "ج) 3x − 3", "د) x³"],
            "أ",
            "مشتقة x³ هي 3x² ومشتقة −3x هي −3، إذن المشتقة 3x² − 3.",
            50
        ),
        make_question(
            "الرياضيات", "المصفوفات", "متوسط",
            "إذا كانت A مصفوفة من الرتبة 2 × 3 و B من الرتبة 3 × 2 فإن حاصل الضرب AB يكون من الرتبة:",
            ["أ) 2 × 2", "ب) 3 × 3", "ج) 2 × 3", "د) 3 × 2"],
            "أ",
            "عند ضرب مصفوفتين تكون أبعاد الناتج هي الأبعاد الخارجية، فيكون الناتج 2 × 2.",
            50
        ),
        make_question(
            "الرياضيات", "الاحتمالات", "متوسط",
            "إذا ألقي حجر نرد منتظم مرة واحدة، فما احتمال ظهور عدد أولي؟",
            ["أ) 1/6", "ب) 1/3", "ج) 1/2", "د) 2/3"],
            "ج",
            "الأعداد الأولية على حجر النرد هي 2 و3 و5، إذن الاحتمال = 3/6 = 1/2.",
            50
        ),
        make_question(
            "الرياضيات", "الأعداد المركبة", "صعب",
            "إذا كان i² = -1 فإن i³ يساوي:",
            ["أ) 1", "ب) -1", "ج) i", "د) -i"],
            "د",
            "لأن i³ = i² × i = -1 × i = -i.",
            55
        ),
        make_question(
            "الرياضيات", "الهندسة التحليلية", "صعب",
            "ما ميل المستقيم المار بالنقطتين (1 ، 2) و(5 ، 10)؟",
            ["أ) 1", "ب) 2", "ج) 3", "د) 4"],
            "ب",
            "الميل = (10 − 2) ÷ (5 − 1) = 8 ÷ 4 = 2.",
            55
        ),
        make_question(
            "الرياضيات", "التكامل بالتجزئة", "صعب",
            "أي العبارات الآتية تمثل صيغة التكامل بالتجزئة تمثيلًا صحيحًا؟",
            ["أ) ∫u dv = uv − ∫v du", "ب) ∫u dv = uv + ∫v du", "ج) ∫u dv = du × dv", "د) ∫u dv = u/v + ثابت"],
            "أ",
            "الصيغة الصحيحة للتكامل بالتجزئة هي: ∫u dv = uv − ∫v du.",
            70
        ),

        # الكيمياء
        make_question(
            "الكيمياء", "التركيب الذري", "سهل",
            "العدد الذري للعنصر يساوي عدد:",
            ["أ) النيوترونات", "ب) البروتونات", "ج) النيوكلونات", "د) مستويات الطاقة"],
            "ب",
            "العدد الذري هو عدد البروتونات الموجودة في نواة الذرة.",
            40
        ),
        make_question(
            "الكيمياء", "الجدول الدوري", "سهل",
            "العناصر الموجودة في نفس المجموعة في الجدول الدوري تتشابه في:",
            ["أ) الكتلة الذرية فقط", "ب) عدد النيوترونات", "ج) الخواص الكيميائية", "د) الحالة الفيزيائية فقط"],
            "ج",
            "لأن عناصر المجموعة الواحدة لها نفس عدد إلكترونات التكافؤ تقريبًا فتتشابه كيميائيًا.",
            45
        ),
        make_question(
            "الكيمياء", "الروابط الكيميائية", "سهل",
            "تنشأ الرابطة التساهمية نتيجة:",
            ["أ) انتقال الإلكترونات", "ب) مشاركة الإلكترونات", "ج) فقد النيوترونات", "د) اكتساب البروتونات"],
            "ب",
            "الرابطة التساهمية تنتج من مشاركة الذرات في الإلكترونات.",
            45
        ),
        make_question(
            "الكيمياء", "المول", "متوسط",
            "يحتوي مول واحد من أي مادة على:",
            ["أ) 10²³ جسيم", "ب) 6.02 × 10²³ جسيم", "ج) 3.01 × 10²³ جسيم", "د) 12 جسيمًا"],
            "ب",
            "عدد أفوجادرو يساوي 6.02 × 10²³ جسيمًا في المول الواحد.",
            50
        ),
        make_question(
            "الكيمياء", "الغازات", "متوسط",
            "وفق قانون بويل، وعند ثبوت درجة الحرارة، يكون الضغط متناسبًا عكسيًا مع:",
            ["أ) الكثافة", "ب) الكتلة", "ج) الحجم", "د) درجة الحرارة"],
            "ج",
            "ينص قانون بويل على أن الضغط يتناسب عكسيًا مع الحجم عند ثبوت درجة الحرارة.",
            50
        ),
        make_question(
            "الكيمياء", "الأحماض والقواعد", "متوسط",
            "محلول قيمة الأس الهيدروجيني له تساوي 2 يُعد محلولًا:",
            ["أ) متعادلًا", "ب) قاعديًا", "ج) حمضيًا", "د) منظمًا فقط"],
            "ج",
            "كل محلول تقل قيمة pH له عن 7 يعد محلولًا حمضيًا.",
            45
        ),
        make_question(
            "الكيمياء", "الأكسدة والاختزال", "صعب",
            "تعرف عملية الأكسدة بأنها:",
            ["أ) اكتساب إلكترونات", "ب) فقد إلكترونات", "ج) اكتساب نيوترونات", "د) فقد بروتونات"],
            "ب",
            "الأكسدة تعني فقد الإلكترونات، أما الاختزال فيعني اكتسابها.",
            55
        ),
        make_question(
            "الكيمياء", "الكيمياء الحرارية", "صعب",
            "التفاعل الطارد للحرارة هو التفاعل الذي:",
            ["أ) يمتص حرارة", "ب) يطلق حرارة", "ج) يتوقف عند درجة الغرفة", "د) يحتاج كهرباء فقط"],
            "ب",
            "التفاعل الطارد للحرارة يطلق حرارة إلى الوسط المحيط.",
            55
        ),
        make_question(
            "الكيمياء", "الكيمياء العضوية", "صعب",
            "الصيغة العامة للألكانات هي:",
            ["أ) CnH2n", "ب) CnH2n+2", "ج) CnH2n−2", "د) CnHn"],
            "ب",
            "الألكانات من الهيدروكربونات المشبعة وصيغتها العامة CnH2n+2.",
            60
        ),
        make_question(
            "الكيمياء", "سرعة التفاعل", "صعب",
            "يعمل العامل الحفاز على زيادة سرعة التفاعل الكيميائي لأنه:",
            ["أ) يزيد طاقة التنشيط", "ب) يقلل طاقة التنشيط", "ج) يغير نواتج التفاعل", "د) يغير ثابت الاتزان فقط"],
            "ب",
            "العامل الحفاز يوفر مسارًا بديلًا للتفاعل بطاقة تنشيط أقل.",
            65
        ),

        # اللغة العربية
        make_question(
            "اللغة العربية", "النحو", "سهل",
            "اختر الجملة الصحيحة من حيث رفع الفاعل:",
            ["أ) حضرَ الطالبُ", "ب) حضرَ الطالبَ", "ج) حضرَ الطالبِ", "د) حضرَ الطالبْ"],
            "أ",
            "الفاعل يجب أن يكون مرفوعًا، ولذلك تكون الكلمة الصحيحة: الطالبُ.",
            45
        ),
        make_question(
            "اللغة العربية", "النحو", "سهل",
            "مثنى كلمة معلم هو:",
            ["أ) معلمين", "ب) معلمان", "ج) معلمات", "د) معلمون"],
            "ب",
            "مثنى كلمة معلم في حالة الرفع هو معلمان.",
            45
        ),
        make_question(
            "اللغة العربية", "البلاغة", "متوسط",
            "يقوم التشبيه في البلاغة العربية على:",
            ["أ) كلمة واحدة فقط", "ب) راوٍ فقط", "ج) المقارنة بين شيئين", "د) فعل ومفعول فقط"],
            "ج",
            "التشبيه يعتمد على المقارنة بين شيئين يشتركان في صفة معينة.",
            55
        ),
        make_question(
            "اللغة العربية", "القراءة", "متوسط",
            "الفكرة العامة للفقرة يقصد بها:",
            ["أ) أطول جملة فيها", "ب) المعنى الرئيس الذي تدور حوله الأفكار", "ج) أول كلمة فقط", "د) العنوان وحده"],
            "ب",
            "الفكرة العامة هي المعنى المركزي الذي تنتظم حوله بقية الأفكار داخل الفقرة.",
            50
        ),
        make_question(
            "اللغة العربية", "النحو", "متوسط",
            "في الجملة: إن العلمَ نورٌ، كلمة العلمَ تعرب:",
            ["أ) خبر إن", "ب) اسم إن", "ج) فاعل", "د) مفعول به"],
            "ب",
            "بعد إن يأتي اسمها منصوبًا، ولذلك فالعلمَ: اسم إن منصوب.",
            55
        ),
        make_question(
            "اللغة العربية", "الأدب", "متوسط",
            "يقوم الشعر العربي التقليدي غالبًا على:",
            ["أ) الفقرة الحرة فقط", "ب) الوزن والقافية", "ج) انعدام الإيقاع", "د) الحوار فقط"],
            "ب",
            "الشعر العربي التقليدي يقوم على الوزن والقافية.",
            55
        ),
        make_question(
            "اللغة العربية", "النحو", "صعب",
            "اختر الجملة التي ورد فيها الفعل مبنيًا للمجهول بصورة صحيحة:",
            ["أ) كتبَ الدرسُ", "ب) كُتِبَ الدرسُ", "ج) كتبَ الدرسَ", "د) يكتبُ الدرسَ"],
            "ب",
            "في البناء للمجهول يتغير ضبط الفعل ويحل المفعول به محل الفاعل نائبًا عنه، لذلك الصواب: كُتِبَ الدرسُ.",
            60
        ),
        make_question(
            "اللغة العربية", "البلاغة", "صعب",
            "تختلف الاستعارة عن التشبيه في أن الاستعارة:",
            ["أ) تستخدم أداة تشبيه صريحة", "ب) تحذف أداة التشبيه وغالبًا أحد الطرفين", "ج) تخلو من الصورة", "د) لا تستخدم إلا في النثر"],
            "ب",
            "الاستعارة تشبيه حُذف أحد طرفيه أو أداة التشبيه فيه، ولذلك تكون أبلغ من التشبيه الصريح.",
            65
        ),
        make_question(
            "اللغة العربية", "الأساليب", "صعب",
            "في التعبير: ما أجملَ السماءَ، يكون الأسلوب:",
            ["أ) أمر", "ب) استفهام", "ج) تعجب", "د) نفي"],
            "ج",
            "صيغة ما أفعلَ من أشهر صيغ التعجب القياسية في العربية.",
            55
        ),
        make_question(
            "اللغة العربية", "تحليل النصوص", "صعب",
            "عند تحليل نص أدبي تحليلاً احترافيًا، فإن أول خطوة صحيحة تكون:",
            ["أ) عد علامات الترقيم فقط", "ب) تحديد الفكرة المحورية والنبرة العامة", "ج) عد الكلمات فقط", "د) معرفة عمر الكاتب فقط"],
            "ب",
            "التحليل الأدبي الرصين يبدأ بتحديد الفكرة العامة والنبرة المسيطرة قبل الانتقال إلى الصور والأساليب.",
            65
        ),
    ]
    return questions

# =========================================================
# روابط Google Drive
# =========================================================
PDF_RESOURCES = [
    {
        "title": "ملف الفيزياء - الكهرباء والفيزياء الحديثة",
        "subject": "الفيزياء",
        "unit": "الكهرباء / الفيزياء الحديثة",
        "keywords": ["فيزياء", "كهرباء", "كيرشوف", "حديثة", "نووية", "ذرية"],
        "drive_link": "https://drive.google.com/file/d/PUT_REAL_FILE_ID_1/view?usp=sharing"
    },
    {
        "title": "ملف الرياضيات - التفاضل والتكامل والجبر",
        "subject": "الرياضيات",
        "unit": "تفاضل / تكامل / جبر",
        "keywords": ["رياضيات", "تكامل", "تفاضل", "نهايات", "مصفوفات", "احتمالات"],
        "drive_link": "https://drive.google.com/file/d/PUT_REAL_FILE_ID_2/view?usp=sharing"
    },
    {
        "title": "ملف الكيمياء - العامة والعضوية",
        "subject": "الكيمياء",
        "unit": "التركيب الذري / الروابط / العضوية",
        "keywords": ["كيمياء", "عضوية", "أحماض", "غازات", "مول", "سرعة التفاعل"],
        "drive_link": "https://drive.google.com/file/d/PUT_REAL_FILE_ID_3/view?usp=sharing"
    },
    {
        "title": "ملف اللغة العربية - النحو والبلاغة والأدب",
        "subject": "اللغة العربية",
        "unit": "النحو / البلاغة / الأدب",
        "keywords": ["عربي", "نحو", "بلاغة", "أدب", "قراءة", "تحليل النصوص"],
        "drive_link": "https://drive.google.com/file/d/PUT_REAL_FILE_ID_4/view?usp=sharing"
    },
]

# ضع هنا رابط CSV المنشور من Google Sheets إذا توفر
QUESTIONS_BANK_CSV_URL = ""

# =========================================================
# تحميل الأسئلة
# =========================================================
@st.cache_data(show_spinner=False)
def load_questions() -> List[Dict[str, Any]]:
    remote_questions = []
    if QUESTIONS_BANK_CSV_URL.strip():
        remote_questions = parse_remote_questions_from_csv(QUESTIONS_BANK_CSV_URL)

    if len(remote_questions) >= 40:
        questions = remote_questions[:40]
    else:
        questions = get_builtin_questions()

    for q in questions:
        q["answer"] = str(q["answer"]).strip().upper()
        q["time_limit_sec"] = int(q.get("time_limit_sec", 60))
    return questions

# =========================================================
# محرك البحث الذكي
# =========================================================
def run_smart_search(query: str, questions: List[Dict[str, Any]], resources: List[Dict[str, Any]]) -> Dict[str, Any]:
    query = query.strip()
    lesson_hits = []
    question_hits = []

    if not query:
        return {"lessons": [], "questions": []}

    for res in resources:
        score = 0
        score += smart_match_score(query, res.get("title", ""))
        score += smart_match_score(query, res.get("subject", ""))
        score += smart_match_score(query, res.get("unit", ""))
        for kw in res.get("keywords", []):
            score += smart_match_score(query, kw)
        if score > 0:
            lesson_hits.append((score, res))

    for q in questions:
        haystack = " ".join([
            q.get("subject", ""),
            q.get("unit", ""),
            q.get("difficulty", ""),
            q.get("question", ""),
            q.get("explanation", ""),
            " ".join(q.get("options", []))
        ])
        score = smart_match_score(query, haystack)
        if score > 0:
            question_hits.append((score, q))

    lesson_hits.sort(key=lambda x: x[0], reverse=True)
    question_hits.sort(key=lambda x: x[0], reverse=True)

    return {
        "lessons": [item[1] for item in lesson_hits[:8]],
        "questions": [item[1] for item in question_hits[:10]]
    }

# =========================================================
# إدارة الحالة
# =========================================================
def init_state(questions: List[Dict[str, Any]]) -> None:
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "questions" not in st.session_state:
        st.session_state.questions = questions
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

def reset_exam():
    questions = load_questions()
    st.session_state.questions = questions
    st.session_state.current_index = 0
    st.session_state.answers = {}
    st.session_state.answer_submitted = False
    st.session_state.deadline = None
    st.session_state.question_started_at = None
    st.session_state.auto_skipped = []
    st.session_state.quiz_started = True
    st.session_state.exam_finished = False

def start_question_timer(question: Dict[str, Any]):
    st.session_state.question_started_at = time.time()
    st.session_state.deadline = time.time() + int(question.get("time_limit_sec", 60))

def ensure_timer_for_current_question():
    idx = st.session_state.current_index
    questions = st.session_state.questions
    if idx < len(questions) and st.session_state.deadline is None:
        start_question_timer(questions[idx])

def answer_letter_from_option(option_text: str) -> str:
    if not option_text:
        return ""
    option_text = option_text.strip()
    return option_text[0]

def submit_current_answer():
    idx = st.session_state.current_index
    questions = st.session_state.questions
    if idx >= len(questions):
        return

    question = questions[idx]
    chosen = st.session_state.get(f"q_choice_{idx}")
    if not chosen:
        return

    chosen_letter = answer_letter_from_option(chosen)
    st.session_state.answers[idx] = {
        "selected_option": chosen,
        "selected_letter": chosen_letter,
        "correct_letter": question["answer"],
        "is_correct": chosen_letter == question["answer"],
        "timed_out": False,
        "subject": question["subject"],
        "unit": question["unit"],
        "question": question["question"]
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
# واجهة البداية
# =========================================================
st.markdown(f'<div class="main-title">{APP_NAME}</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">نظام اختبارات احترافي متسلسل • بحث ذكي • ربط ملفات Google Drive</div>',
    unsafe_allow_html=True
)

questions = load_questions()
init_state(questions)

# =========================================================
# الشريط الجانبي
# =========================================================
with st.sidebar:
    st.markdown("### لوحة التحكم")
    st.info("يتم عرض سؤال واحد فقط في كل مرة، ولا ينتقل الطالب إلى السؤال التالي إلا بعد الإجابة، وإذا انتهى الوقت يتم التخطي تلقائيًا.")

    total_questions = len(st.session_state.questions)
    answered_count = len(st.session_state.answers)
    correct_count = sum(1 for a in st.session_state.answers.values() if a["is_correct"])
    skipped_count = sum(1 for a in st.session_state.answers.values() if a.get("timed_out"))

    st.metric("إجمالي الأسئلة", total_questions)
    st.metric("الأسئلة المجابة", answered_count)
    st.metric("الإجابات الصحيحة", correct_count)
    st.metric("الأسئلة المتخطاة تلقائيًا", skipped_count)

    if st.button("بدء اختبار جديد"):
        reset_exam()

    if st.button("إعادة تحميل الأسئلة من المصدر"):
        st.cache_data.clear()
        new_questions = load_questions()
        st.session_state.questions = new_questions
        st.success("تمت إعادة تحميل الأسئلة بنجاح.")

# =========================================================
# البحث الذكي
# =========================================================
st.markdown('<div class="hero-card">', unsafe_allow_html=True)
st.markdown('<div class="search-title">البحث الذكي عن الدروس والموضوعات</div>', unsafe_allow_html=True)

search_query = st.text_input(
    "ابحث عن درس أو وحدة أو موضوع محدد",
    placeholder="مثال: قوانين كيرشوف - التكامل بالتجزئة - الأحماض والقواعد - النحو"
)

search_results = run_smart_search(search_query, st.session_state.questions, PDF_RESOURCES) if search_query else {"lessons": [], "questions": []}

col_s1, col_s2 = st.columns(2)

with col_s1:
    st.markdown("#### الدروس والملفات المطابقة")
    if search_query and search_results["lessons"]:
        for lesson in search_results["lessons"]:
            st.markdown(f"""
            <div class="resource-card">
                <div style="font-size:1.05rem;font-weight:900;color:#fff;">{lesson['title']}</div>
                <div class="small-note">المادة: {lesson['subject']} | الوحدة: {lesson['unit']}</div>
            </div>
            """, unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.link_button("فتح المعاينة", to_gdrive_preview(lesson["drive_link"]))
            with c2:
                st.link_button("تحميل الملف", to_gdrive_download(lesson["drive_link"]))
    elif search_query:
        st.warning("لم يتم العثور على ملفات مطابقة في الموارد الحالية.")
    else:
        st.caption("استخدم مربع البحث للوصول إلى الدروس والملفات المناسبة بسرعة.")

with col_s2:
    st.markdown("#### أسئلة مرتبطة بالبحث")
    if search_query and search_results["questions"]:
        for q in search_results["questions"][:5]:
            st.markdown(f"""
            <div class="info-card">
                <div style="font-weight:900;color:#fff;">{q['subject']} • {q['unit']}</div>
                <div class="small-note">{q['question']}</div>
            </div>
            """, unsafe_allow_html=True)
    elif search_query:
        st.warning("لا توجد أسئلة مطابقة لعملية البحث.")
    else:
        st.caption("يمكنك أيضًا البحث داخل بنك الأسئلة للوصول السريع للموضوعات.")

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# شاشة البداية قبل الاختبار
# =========================================================
if not st.session_state.quiz_started:
    st.markdown('<div class="hero-card">', unsafe_allow_html=True)
    st.markdown("### وصف نظام الاختبار")
    st.write("""
    هذه المنصة تعمل بمنطق امتحاني احترافي:
    - عرض سؤال واحد فقط في كل مرة.
    - لا يظهر زر السؤال التالي إلا بعد إرسال الإجابة.
    - لكل سؤال مؤقت مستقل حسب طوله وصعوبته.
    - عند انتهاء الوقت يتم الانتقال تلقائيًا للسؤال التالي.
    - الاختبار يضم 40 سؤالًا متنوعًا لتغطية مواد ووحدات متعددة.
    """)
    if st.button("دخول الاختبار الآن"):
        reset_exam()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# =========================================================
# شاشة النتيجة النهائية
# =========================================================
if st.session_state.exam_finished:
    all_answers = st.session_state.answers
    total = len(st.session_state.questions)
    correct = sum(1 for a in all_answers.values() if a["is_correct"])
    incorrect = sum(1 for a in all_answers.values() if (not a["is_correct"] and not a.get("timed_out")))
    timed_out = sum(1 for a in all_answers.values() if a.get("timed_out"))
    score_percent = round((correct / total) * 100, 2) if total else 0

    st.markdown('<div class="hero-card">', unsafe_allow_html=True)
    st.markdown("## التقرير النهائي للاختبار")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div style="font-size:1.8rem;font-weight:900;">{total}</div><div>إجمالي الأسئلة</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div style="font-size:1.8rem;font-weight:900;">{correct}</div><div>الإجابات الصحيحة</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div style="font-size:1.8rem;font-weight:900;">{incorrect}</div><div>الإجابات الخاطئة</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div style="font-size:1.8rem;font-weight:900;">{timed_out}</div><div>تخطى تلقائيًا</div></div>', unsafe_allow_html=True)

    st.progress(score_percent / 100)
    st.success(f"النسبة النهائية: {score_percent}%")

    report_rows = []
    for idx, q in enumerate(st.session_state.questions):
        a = all_answers.get(idx, {})
        report_rows.append({
            "رقم السؤال": idx + 1,
            "المادة": q["subject"],
            "الوحدة": q["unit"],
            "نص السؤال": q["question"],
            "إجابة الطالب": a.get("selected_letter"),
            "الإجابة الصحيحة": q["answer"],
            "النتيجة": "صحيح" if a.get("is_correct") else ("انتهى الوقت" if a.get("timed_out") else "خطأ")
        })

    report_df = pd.DataFrame(report_rows)
    st.dataframe(report_df, use_container_width=True, hide_index=True)

    csv_data = report_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "تحميل تقرير النتائج CSV",
        data=csv_data,
        file_name="تقرير_نتائج_منصة_أدهم_صبري.csv",
        mime="text/csv"
    )

    if st.button("إعادة الاختبار من جديد"):
        reset_exam()

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# =========================================================
# شاشة السؤال الحالي
# =========================================================
ensure_timer_for_current_question()

idx = st.session_state.current_index
questions = st.session_state.questions
question = questions[idx]
total_questions = len(questions)

time_limit = int(question.get("time_limit_sec", 60))
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

st.markdown('<div class="exam-box">', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="question-badge">السؤال {idx + 1} من {total_questions}</div>
    <div>
        <span class="subject-chip">{question['subject']}</span>
        <span class="subject-chip">{question['unit']}</span>
        <span class="subject-chip">درجة الصعوبة: {question['difficulty']}</span>
        <span class="subject-chip">الزمن: {question['time_limit_sec']} ثانية</span>
    </div>
    <div class="question-text">{question['question']}</div>
    """,
    unsafe_allow_html=True
)

choice_key = f"q_choice_{idx}"

if not st.session_state.answer_submitted:
    selected = st.radio(
        "اختر الإجابة الصحيحة",
        options=question["options"],
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
            f'<div class="feedback-success">إجابة صحيحة ✅<br><br>التفسير: {question["explanation"]}</div>',
            unsafe_allow_html=True
        )
    else:
        correct_option_text = next(
            (opt for opt in question["options"] if opt.startswith(question["answer"])),
            f"{question['answer']})"
        )
        st.markdown(
            f'<div class="feedback-error">إجابة غير صحيحة ❌<br><br>الإجابة الصحيحة: {correct_option_text}<br><br>التفسير: {question["explanation"]}</div>',
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

# =========================================================
# عرض ملفات مرتبطة بالمادة الحالية
# =========================================================
st.markdown("### ملف شرح مقترح مرتبط بالسؤال الحالي")
related_resources = [r for r in PDF_RESOURCES if normalize_text(r["subject"]) == normalize_text(question["subject"])]

if related_resources:
    selected_resource_title = st.selectbox(
        "اختر الملف المطلوب فتحه",
        options=[r["title"] for r in related_resources],
        index=0
    )
    selected_resource = next(r for r in related_resources if r["title"] == selected_resource_title)

    preview_url = to_gdrive_preview(selected_resource["drive_link"])
    download_url = to_gdrive_download(selected_resource["drive_link"])

    c1, c2 = st.columns(2)
    with c1:
        st.link_button("فتح معاينة الملف", preview_url)
    with c2:
        st.link_button("تحميل الملف", download_url)

    st.components.v1.html(
        f"""
        <iframe
            src="{preview_url}"
            width="100%"
            height="700"
            style="border:none;border-radius:14px;overflow:hidden;">
        </iframe>
        """,
        height=720,
        scrolling=True
    )
else:
    st.info("لا يوجد حاليًا ملف مرتبط بهذه المادة. ضع روابط Google Drive الحقيقية داخل المتغير PDF_RESOURCES.")

st.caption("لتفعيل الربط الحقيقي مع Google Drive، استبدل الروابط التجريبية بالروابط الفعلية لملفاتك، وأضف رابط CSV الحقيقي لبنك الأسئلة إذا كان متاحًا.")
