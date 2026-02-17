import streamlit as st
import requests
import pandas as pd
import os

# --- الإعدادات ---
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"
DB_FILE = "files_db.csv"

st.set_page_config(page_title="تطبيق محطات الوزن", page_icon="🚚", layout="centered")

# --- تنسيق CSS لإجبار الواجهة على اللون الأسود والتصميم المودرن ---
st.markdown("""
    <style>
    /* جعل الخلفية سوداء بالكامل */
    .stApp {
        background-color: #0b0e14 !important;
        color: #ffffff !important;
    }
    /* تنسيق الحاوية الرئيسية */
    .main {
        background-color: #0b0e14;
    }
    /* لوجو الشاحنة */
    .truck-header {
        font-size: 100px;
        text-align: center;
        margin-top: 20px;
        filter: drop-shadow(0 0 10px #00c6ff);
    }
    /* واجهة الباسورد */
    .login-box {
        background-color: #1e2630;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #3e4957;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }
    /* الأزرار الملونة */
    .stButton>button {
        width: 100%;
        border-radius: 15px !important;
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        height: 3em;
        font-size: 18px;
    }
    /* كروت الملفات */
    .file-card {
        background-color: #1e2630;
        padding: 15px;
        border-radius: 12px;
        border-right: 6px solid #00c6ff;
        margin-bottom: 10px;
    }
    /* تعديل لون النصوص في التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        color: #8899ac;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        color: #00c6ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الحماية (Password) ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown('<div class="truck-header">🚚</div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: white;'>تطبيق محطات الوزن</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8899ac;'>يرجى إدخال رمز الدخول للمتابعة</p>", unsafe_allow_html=True)
    
    # وضع حقل الباسورد في منتصف الصفحة
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        password = st.text_input("", type="password", placeholder="كلمة المرور هنا...")
        if st.button("🚀 تسجيل الدخول"):
            if password == "123":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ الرمز غير صحيح")
    st.stop()

# --- بعد الدخول (الدوال والواجهة) ---
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

# الواجهة الرئيسية
st.markdown('<div style="text-align:right; font-size:40px;">🚚</div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #00c6ff;'>محطات الوزن الذكية</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 البحث عن الوصل", "📤 أرشفة وصل جديد"])

with tab1:
    search = st.text_input("📝 اكتب اسم المحطة أو الرقم للبحث:", placeholder="ابحث هنا...")
    df = load_data()
    if search:
        results = df[df['الاسم'].str.contains(search, na=False, case=False)]
        if not results.empty:
            for index, row in results.iterrows():
                st.markdown(f'<div class="file-card">📄 <b>{row["الاسم"]}</b></div>', unsafe_allow_html=True)
                link = get_telegram_download_link(row['file_id'])
                if link:
                    st.markdown(f'<a href="{link}" target="_blank" style="text-decoration:none;"><button style="width:100%; background-color:#28a745; color:white; border-radius:10px; border:none; padding:10px; cursor:pointer; font-weight:bold;">⬇️ تحميل المستند</button></a>', unsafe_allow_html=True)
                st.write("")
        else:
            st.warning("⚠️ لا توجد نتائج مطابقة")

with tab2:
    st.markdown("### 📤 رفع مستند إلى الأرشيف")
    up = st.file_uploader("اختر ملف PDF", type=["pdf"])
    if up and st.button("🚀 حفظ في النظام"):
        with st.spinner("جاري المزامنة مع تليجرام..."):
            res = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                                data={'chat_id': CHAT_ID, 'caption': up.name}, 
                                files={'document': (up.name, up.read())}).json()
            if res.get("ok"):
                save_to_db(up.name, res['result']['document']['file_id'])
                st.success("✅ تم الحفظ بنجاح")
            else:
                st.error("❌ فشل الرفع")

if st.sidebar.button("🚪 خروج"):
    st.session_state["authenticated"] = False
    st.rerun()
