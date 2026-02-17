import streamlit as st
import requests
import pandas as pd
import os

# --- الإعدادات ---
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"
DB_FILE = "files_db.csv"

st.set_page_config(page_title="تطبيق محطات الوزن", page_icon="🚚", layout="centered")

# --- تنسيق CSS للواجهة البيضاء (Clean White UI) ---
st.markdown("""
    <style>
    /* جعل الخلفية بيضاء بالكامل */
    .stApp {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
    }
    /* تنسيق لوجو الشاحنة */
    .truck-header {
        font-size: 80px;
        text-align: center;
        margin-top: 10px;
    }
    /* الأزرار الملونة */
    .stButton>button {
        width: 100%;
        border-radius: 12px !important;
        background: linear-gradient(90deg, #0072ff 0%, #00c6ff 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        height: 3.2em;
        font-size: 16px;
        box-shadow: 0 4px 15px rgba(0,114,255,0.2);
    }
    /* كروت الملفات في الخلفية البيضاء */
    .file-card {
        background-color: #f8f9fa;
        padding: 18px;
        border-radius: 15px;
        border-right: 6px solid #0072ff;
        margin-bottom: 12px;
        color: #2c3e50;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    /* تعديل التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f1f3f5;
        border-radius: 10px;
        padding: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: bold;
        color: #495057;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        border-radius: 8px !important;
        color: #0072ff !important;
    }
    /* حقول الإدخال */
    input {
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الحماية (Password) ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown('<div class="truck-header">🚚</div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #2c3e50;'>تطبيق محطات الوزن</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #7f8c8d;'>نظام الأرشفة - يرجى تسجيل الدخول</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        password = st.text_input("", type="password", placeholder="كلمة المرور...")
        if st.button("🚀 دخول للنظام"):
            if password == "123":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ الرمز خاطئ")
    st.stop()

# --- الدوال البرمجية ---
def load_data():
    if os.path.exists(DB_FILE): return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["الاسم", "file_id"])

def save_to_db(name, file_id):
    df = load_data()
    new_data = pd.DataFrame({"الاسم": [name], "file_id": [file_id]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

def get_telegram_download_link(file_id):
    try:
        res = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}").json()
        return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{res['result']['file_path']}"
    except: return None

# --- الواجهة الرئيسية ---
st.markdown('<div style="text-align:right; font-size:40px;">🚚</div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #0072ff;'>محطات الوزن الذكية</h1>", unsafe_allow_html=True)

# تعديل أسماء التبويبات حسب طلبك
tab1, tab2 = st.tabs(["🔍 البحث عن ملف PDF", "📤 أرشفة ملف PDF"])

with tab1:
    search = st.text_input("📝 اكتب اسم الملف للبحث:", placeholder="ابحث هنا عن ملفات PDF...")
    df = load_data()
    if search:
        results = df[df['الاسم'].str.contains(search, na=False, case=False)]
        if not results.empty:
            for index, row in results.iterrows():
                st.markdown(f'<div class="file-card">📄 <b>{row["الاسم"]}</b></div>', unsafe_allow_html=True)
                link = get_telegram_download_link(row['file_id'])
                if link:
                    st.markdown(f'<a href="{link}" target="_blank" style="text-decoration:none;"><button style="width:100%; background-color:#28a745; color:white; border-radius:10px; border:none; padding:10px; cursor:pointer; font-weight:bold;">⬇️ تحميل الملف</button></a>', unsafe_allow_html=True)
                st.write("")
        else:
            st.warning("⚠️ لم يتم العثور على ملف بهذا الاسم")

with tab2:
    st.markdown("### 📥 إضافة ملف PDF جديد للأرشيف")
    up = st.file_uploader("اختر ملف PDF من جهازك", type=["pdf"])
    if up and st.button("🚀 بدء الأرشفة"):
        with st.spinner("جاري الحفظ في الأرشيف..."):
            res = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                                data={'chat_id': CHAT_ID, 'caption': up.name}, 
                                files={'document': (up.name, up.read())}).json()
            if res.get("ok"):
                save_to_db(up.name, res['result']['document']['file_id'])
                st.success("✅ تم حفظ الملف بنجاح!")
            else:
                st.error("❌ حدث خطأ أثناء الرفع")

if st.sidebar.button("🚪 تسجيل الخروج"):
    st.session_state["authenticated"] = False
    st.rerun()
