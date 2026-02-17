import streamlit as st
import requests
import pandas as pd
import os

# --- الإعدادات وبيانات الاتصال ---
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"
DB_FILE = "files_db.csv"

# إعداد واجهة الصفحة لتشبه الموبايل
st.set_page_config(page_title="تطبيق محطات الوزن", page_icon="⚖️", layout="centered")

# --- تنسيق CSS لجعل الواجهة تشبه الموبايل ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #007bff;
        color: white;
        border: none;
    }
    .file-card {
        background-color: white;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الحماية (Password) ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("<h2 style='text-align: center;'>🔐 دخول النظام</h2>", unsafe_allow_html=True)
    password = st.text_input("أدخل كلمة المرور للدخول:", type="password")
    if st.button("تسجيل الدخول"):
        if password == "123":
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("❌ كلمة المرور غير صحيحة")
    st.stop() # إيقاف التنفيذ حتى يتم إدخال الباسورد

# --- الدوال البرمجية ---
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

# --- واجهة التطبيق الرئيسية (بعد الدخول) ---
st.markdown("<h1 style='text-align: center; color: #004a99;'>⚖️ محطات الوزن</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>نظام أرشفة المستندات الذكي</p>", unsafe_allow_html=True)

# التبديل بين الرفع والبحث (مثل تبويبات الموبايل)
tabs = st.tabs(["🔍 البحث عن ملف", "📤 رفع جديد"])

# --- التبويب الأول: البحث (للموظف) ---
with tabs[0]:
    search_query = st.text_input("📝 اكتب اسم المحطة أو الملف:", placeholder="مثال: محطة القائم")
    df = load_data()
    
    if search_query:
        results = df[df['الاسم'].str.contains(search_query, na=False, case=False)]
        if not results.empty:
            for index, row in results.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="file-card">
                        <b>📄 {row['الاسم']}</b>
                    </div>
                    """, unsafe_allow_html=True)
                    d_link = get_telegram_download_link(row['file_id'])
                    if d_link:
                        st.markdown(f'<a href="{d_link}" target="_blank" style="text-decoration:none;"><button style="width:100%; background-color:#28a745; color:white; border-radius:10px; border:none; padding:10px;">⬇️ تحميل المستند</button></a>', unsafe_allow_html=True)
                    st.write("")
        else:
            st.warning("لم يتم العثور على نتائج")

# --- التبويب الثاني: الرفع (لك) ---
with tabs[1]:
    st.markdown("### إضافة ملف للأرشيف")
    up = st.file_uploader("اختر ملف PDF:", type=["pdf"])
    if up and st.button("🚀 بدء الرفع والارشفة"):
        with st.spinner("جاري المزامنة..."):
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
            files = {'document': (up.name, up.read())}
            data = {'chat_id': CHAT_ID, 'caption': up.name}
            res = requests.post(url, data=data, files=files).json()
            if res.get("ok"):
                save_to_db(up.name, res['result']['document']['file_id'])
                st.success("تم الحفظ بنجاح!")
            else:
                st.error("فشل في الرفع")

# زر تسجيل الخروج في الأسفل
if st.sidebar.button("تسجيل الخروج"):
    st.session_state["authenticated"] = False
    st.rerun()
