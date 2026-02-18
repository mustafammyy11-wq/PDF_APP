import streamlit as st
import requests
import pandas as pd
import os

# --- الإعدادات ---
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"
DB_FILE = "files_db.csv"

st.set_page_config(page_title="تطبيق محطات الوزن", page_icon="🚚", layout="centered")

# --- تنسيق الواجهة البيضاء (UI) ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; color: #2c3e50 !important; }
    .main-btn {
        display: block; width: 100%; text-align: center;
        background-color: #28a745; color: white !important;
        padding: 10px; border-radius: 8px;
        text-decoration: none; font-weight: bold; margin-top: 5px;
    }
    .file-card {
        background-color: #f1f3f5; padding: 15px;
        border-radius: 10px; border-right: 5px solid #0072ff;
        margin-top: 15px; margin-bottom: 5px;
        font-size: 18px; font-weight: bold; color: #2c3e50;
    }
    .search-info { color: #7f8c8d; font-size: 14px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الحماية ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("<h2 style='text-align: center;'>🔐 نظام محطات الوزن</h2>", unsafe_allow_html=True)
    password = st.text_input("كلمة المرور:", type="password")
    if st.button("دخول"):
        if password == "123":
            st.session_state["authenticated"] = True
            st.rerun()
    st.stop()

# --- الدوال ---
def load_data():
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE)
        except:
            return pd.DataFrame(columns=["الاسم", "file_id"])
    return pd.DataFrame(columns=["الاسم", "file_id"])

def save_to_db(name, file_id):
    df = load_data()
    new_entry = pd.DataFrame({"الاسم": [name], "file_id": [file_id]})
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

def get_download_url(f_id):
    try:
        res = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={f_id}").json()
        if res.get("ok"):
            return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{res['result']['file_path']}"
    except: return None
    return None

# --- الواجهة الرئيسية ---
st.markdown('<div style="text-align:right; font-size:40px;">🚚</div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #0072ff;'>محطات الوزن الذكية</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 البحث عن ملف PDF", "📤 أرشفة ملف PDF"])

with tab1:
    search = st.text_input("🔎 اكتب الاسم للبحث (مثلاً: صفاء):")
    st.markdown('<p class="search-info">سيتم عرض جميع الملفات التي تحتوي على الكلمة المكتوبة.</p>', unsafe_allow_html=True)
    
    df = load_data()
    
    if search:
        # البحث عن أي اسم يحتوي على نص البحث (بدون الحساسية لحالة الأحرف)
        results = df[df['الاسم'].str.contains(search, na=False, case=False)]
        
        if not results.empty:
            st.success(f"تم العثور على ({len(results)}) ملفات مرتبطة بـ '{search}'")
            for i, row in results.iterrows():
                # عرض كرت لكل ملف موجود في النتائج
                st.markdown(f'<div class="file-card">📄 {row["الاسم"]}</div>', unsafe_allow_html=True)
                
                if pd.notna(row['file_id']):
                    d_url = get_download_url(row['file_id'])
                    if d_url:
                        st.markdown(f'<a href="{d_url}" target="_blank" class="main-btn">⬇️ تحميل ملف {row["الاسم"]}</a>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ ملف قديم - لا يتوفر زر تحميل")
        else:
            st.error(f"❌ لا توجد ملفات تحتوي على اسم '{search}'")

with tab2:
    st.subheader("إضافة ملف PDF جديد")
    up = st.file_uploader("اختر الملف", type=["pdf"])
    if up and st.button("🚀 بدء الأرشفة"):
        with st.spinner("جاري الرفع..."):
            res = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                                data={'chat_id': CHAT_ID, 'caption': up.name}, 
                                files={'document': (up.name, up.read())}).json()
            if res.get("ok"):
                f_id = res['result']['document']['file_id']
                save_to_db(up.name, f_id)
                st.success(f"✅ تم حفظ الملف '{up.name}' بنجاح!")
            else:
                st.error("فشل الرفع")
