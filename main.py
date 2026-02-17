import streamlit as st
import requests
import pandas as pd
import os

# --- الإعدادات ---
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"
DB_FILE = "files_db.csv"

st.set_page_config(page_title="تطبيق محطات الوزن", page_icon="🚚", layout="centered")

# --- تنسيق CSS مودرن (Dark Mode) يشبه الصورة ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .main-header {
        text-align: center;
        padding: 20px;
    }
    .truck-logo {
        font-size: 80px;
        text-align: center;
        margin-bottom: 10px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        color: white;
        border: none;
        font-weight: bold;
        padding: 10px;
    }
    .file-card {
        background-color: #1e2630;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #00c6ff;
        margin-bottom: 15px;
    }
    .stTextInput>div>div>input {
        background-color: #1e2630;
        color: white;
        border-radius: 10px;
        border: 1px solid #3e4957;
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الدخول ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown('<div class="truck-logo">🚚</div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>🔐 نظام محطات الوزن</h2>", unsafe_allow_html=True)
    
    password = st.text_input("أدخل كلمة المرور:", type="password")
    if st.button("دخول"):
        if password == "123":
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("❌ الرمز خاطئ")
    st.stop()

# --- الدوال ---
def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["الاسم", "file_id"])

def save_to_db(name, file_id):
    df = load_data()
    new_data = pd.DataFrame({"الاسم": [name], "file_id": [file_id]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

def get_telegram_download_link(file_id):
    try:
        res = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}").json()
        if res.get("ok"):
            return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{res['result']['file_path']}"
    except: return None

# --- الواجهة الرئيسية ---
st.markdown('<div class="truck-logo">🚚</div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; margin-top:-30px;'>محطات الوزن</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8899ac;'>نظام الأرشفة السحابي الذكي</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 بحث وتحميل", "📤 إضافة مستند"])

with tab1:
    search = st.text_input("📝 ابحث عن اسم المحطة أو الوصل:", placeholder="🔍 اكتب هنا...")
    df = load_data()
    if search:
        results = df[df['الاسم'].str.contains(search, na=False, case=False)]
        if not results.empty:
            for index, row in results.iterrows():
                st.markdown(f'<div class="file-card">📄 <b>{row["الاسم"]}</b></div>', unsafe_allow_html=True)
                link = get_telegram_download_link(row['file_id'])
                if link:
                    st.markdown(f'<a href="{link}" target="_blank" style="text-decoration:none;"><button style="width:100%; background-color:#28a745; color:white; border-radius:10px; border:none; padding:10px; cursor:pointer;">⬇️ تحميل الآن</button></a>', unsafe_allow_html=True)
                st.write("")
        else:
            st.warning("لم يتم العثور على نتائج.")

with tab2:
    st.markdown("### 📤 رفع ملف جديد للنظام")
    up = st.file_uploader("اختر ملف PDF", type=["pdf"])
    if up and st.button("🚀 رفع وأرشفة"):
        with st.spinner("جاري المزامنة مع تليجرام..."):
            res = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                                data={'chat_id': CHAT_ID, 'caption': up.name}, 
                                files={'document': (up.name, up.read())}).json()
            if res.get("ok"):
                save_to_db(up.name, res['result']['document']['file_id'])
                st.success("تم الحفظ في مخزن الشاحنات بنجاح!")
            else:
                st.error("فشل الرفع")

if st.sidebar.button("🚪 خروج"):
    st.session_state["authenticated"] = False
    st.rerun()
