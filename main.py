import streamlit as st
import requests
import pandas as pd
import os

# --- الإعدادات ---
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"
DB_FILE = "files_db.csv"

st.set_page_config(page_title="محطات الوزن الذكية", page_icon="🚚", layout="centered")

# --- حل مشكلة الألوان المختفية في الموبايل ---
st.markdown("""
    <style>
    /* إجبار الخلفية على اللون الأبيض والنص على الأسود */
    .stApp {
        background-color: #ffffff !important;
    }
    h1, h2, h3, p, span, label {
        color: #2c3e50 !important;
    }
    /* تنسيق خانة الباسورد لتكون واضحة */
    input {
        color: #000000 !important;
        background-color: #f0f2f6 !important;
        border: 1px solid #dcdfe6 !important;
    }
    /* تنسيق زر الدخول */
    .stButton>button {
        background-color: #0072ff !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
    }
    /* تنسيق كروت الملفات */
    .file-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-right: 6px solid #0072ff;
        margin-bottom: 10px;
        color: #2c3e50 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الحماية (Password) ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    # عرض أيقونة القفل
    st.markdown("<h1 style='text-align: center;'>🔐</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>دخول النظام</h2>", unsafe_allow_html=True)
    
    # حقل الباسورد مع تسمية واضحة
    pw = st.text_input("أدخل كلمة المرور الموحدة:", type="password", key="login_pw")
    
    if st.button("تسجيل الدخول"):
        if pw == "123":
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("❌ كلمة المرور غير صحيحة")
    st.stop()

# --- الدوال البرمجية ---
def load_db():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["الاسم", "file_id"])

def save_db(name, f_id):
    df = load_db()
    new_data = pd.DataFrame({"الاسم": [name], "file_id": [f_id]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

def get_url(f_id):
    try:
        res = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={f_id}").json()
        return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{res['result']['file_path']}"
    except: return None

# --- الواجهة الرئيسية بعد الدخول ---
st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
        <h1 style="color: #0072ff !important; margin: 0;">محطات الوزن الذكية</h1>
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
                d_url = get_url(row['file_id']) if pd.notna(row['file_id']) else None
                st.markdown(f'<div class="file-card">📄 {row["الاسم"]}</div>', unsafe_allow_html=True)
                if d_url:
                    st.markdown(f'<a href="{d_url}" target="_blank" style="text-decoration:none;"><button style="width:100%; background-color:#28a745; color:white; border:none; padding:10px; border-radius:8px; cursor:pointer; font-weight:bold;">⬇️ تحميل الملف</button></a>', unsafe_allow_html=True)
                st.write("---")
        else:
            st.warning("⚠️ لا توجد نتائج")

with tab2:
    f_up = st.file_uploader("اختر ملف PDF:", type=["pdf"])
    if f_up and st.button("🚀 حفظ الملف الآن"):
        with st.spinner("جاري الرفع..."):
            res = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                                data={'chat_id': CHAT_ID, 'caption': f_up.name}, 
                                files={'document': (f_up.name, f_up.read())}).json()
            if res.get("ok"):
                save_db(f_up.name, res['result']['document']['file_id'])
                st.success("✅ تم الحفظ بنجاح")
