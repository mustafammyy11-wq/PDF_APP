import streamlit as st
import requests
import pandas as pd
import os

# --- الإعدادات ---
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"
DB_FILE = "files_db.csv"

st.set_page_config(page_title="محطات الوزن الذكية", page_icon="🚚", layout="centered")

# --- تنسيق CSS لجعل الواجهة احترافية ومرتبة ---
st.markdown("""
    <style>
    /* جعل الخلفية بيضاء بالكامل */
    .stApp { background-color: #ffffff !important; }
    
    /* تنسيق العنوان والشاحنة ليكونوا بجانب بعضهم */
    .header-style {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        margin-bottom: 20px;
    }
    .header-title {
        color: #0072ff;
        font-size: 28px;
        font-weight: bold;
        margin: 0;
    }
    .truck-img { width: 50px; }

    /* تنسيق كروت الملفات لتظهر مرتبة */
    .file-card {
        background-color: #f8f9fa;
        padding: 12px;
        border-radius: 10px;
        border-right: 5px solid #0072ff;
        margin-bottom: 5px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* زر التحميل الأخضر */
    .download-link {
        background-color: #28a745;
        color: white !important;
        padding: 6px 12px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الدخول بكلمة مرور ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("<h2 style='text-align: center;'>🔐 دخول النظام</h2>", unsafe_allow_html=True)
    pw = st.text_input("كلمة المرور:", type="password")
    if st.button("دخول"):
        if pw == "123":
            st.session_state["authenticated"] = True
            st.rerun()
    st.stop()

# --- الدوال الأساسية ---
def load_db():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["الاسم", "file_id"])

def save_db(name, f_id):
    df = load_db()
    new_data = pd.DataFrame({"الاسم": [name], "file_id": [f_id]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

def get_file_url(f_id):
    try:
        res = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={f_id}").json()
        if res.get("ok"):
            return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{res['result']['file_path']}"
    except: return None
    return None

# --- الواجهة الرئيسية (التنسيق المرتب) ---
st.markdown("""
    <div class="header-style">
        <p class="header-title">محطات الوزن الذكية</p>
        <span style="font-size: 40px;">🚚</span>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 البحث عن ملف PDF", "📤 أرشفة ملف PDF"])

with tab1:
    search_q = st.text_input("🔎 اكتب الاسم للبحث:", placeholder="مثلاً: صفاء")
    df = load_db()
    
    if search_q:
        results = df[df['الاسم'].str.contains(search_q, na=False, case=False)]
        
        if not results.empty:
            for _, row in results.iterrows():
                # جلب الرابط لعرض الزر فوراً
                d_url = get_file_url(row['file_id']) if pd.notna(row['file_id']) else None
                
                # ترتيب الصف: الاسم جهة اليمين والزر جهة اليسار
                col_name, col_btn = st.columns([3, 1])
                with col_name:
                    st.markdown(f'<div style="padding:10px;">📄 {row["الاسم"]}</div>', unsafe_allow_html=True)
                with col_btn:
                    if d_url:
                        st.markdown(f'<a href="{d_url}" target="_blank" class="download-link">⬇️ تحميل</a>', unsafe_allow_html=True)
                    else:
                        st.caption("غير متاح")
                st.divider()
        else:
            st.warning("⚠️ لا توجد نتائج مطابقة")

with tab2:
    f_up = st.file_uploader("اختر ملف PDF للرفع:", type=["pdf"])
    if f_up and st.button("🚀 حفظ في الأرشيف"):
        with st.spinner("جاري الرفع..."):
            res = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                                data={'chat_id': CHAT_ID, 'caption': f_up.name}, 
                                files={'document': (f_up.name, f_up.read())}).json()
            if res.get("ok"):
                save_db(f_up.name, res['result']['document']['file_id'])
                st.success("✅ تم الحفظ بنجاح")
