import streamlit as st
import requests
import pandas as pd
import os

# --- الإعدادات ---
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"
DB_FILE = "files_db.csv"

st.set_page_config(page_title="محطات الوزن الذكية", page_icon="🚚", layout="centered")

# --- التنسيق البصري (ألوان واضحة جداً) ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    h1, h2, h3, p, span, label, div { color: #000000 !important; }
    .header-box { display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 20px; }
    .main-title { color: #0072ff !important; font-size: 26px !important; font-weight: bold; margin: 0; }
    .file-card { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-right: 6px solid #0072ff; margin-bottom: 10px; }
    /* تنسيق زر التحميل */
    .dl-btn {
        display: block; width: 100%; text-align: center;
        background-color: #28a745; color: white !important;
        padding: 12px; border-radius: 10px;
        text-decoration: none; font-weight: bold; margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام تسجيل الدخول (كما هو) ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("<h2 style='text-align: center;'>🔐 دخول النظام</h2>", unsafe_allow_html=True)
    pw = st.text_input("كلمة المرور:", type="password")
    if st.button("تسجيل الدخول"):
        if pw == "123":
            st.session_state["authenticated"] = True
            st.rerun()
        else: st.error("كلمة المرور خطأ")
    st.stop()

# --- الدوال ---
def load_db():
    if os.path.exists(DB_FILE): return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["الاسم", "file_id"])

def save_db(name, f_id):
    df = load_db()
    new_data = pd.DataFrame({"الاسم": [name], "file_id": [f_id]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

def get_url(f_id):
    try:
        res = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={f_id}").json()
        if res.get("ok"):
            return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{res['result']['file_path']}"
    except: return None

# --- الواجهة الرئيسية ---
st.markdown(f"""
    <div class="header-box">
        <h1 class="main-title">محطات الوزن الذكية</h1>
        <span style="font-size: 40px;">🚚</span>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 البحث عن ملف PDF", "📤 أرشفة ملف PDF"])

with tab1:
    search_q = st.text_input("🔎 ابحث عن الاسم (مثل: صفاء):", placeholder="اكتب هنا...")
    df = load_db()
    
    if search_q:
        results = df[df['الاسم'].str.contains(search_q, na=False, case=False)]
        if not results.empty:
            for _, row in results.iterrows():
                file_name = row['الاسم']
                st.markdown(f'<div class="file-card">📄 {file_name}</div>', unsafe_allow_html=True)
                
                d_url = get_url(row['file_id']) if pd.notna(row['file_id']) else None
                if d_url:
                    # إضافة خاصية download="{file_name}" تجبر المتصفح على الحفظ بنفس الاسم الأصلي
                    st.markdown(f'<a href="{d_url}" download="{file_name}" target="_blank" class="dl-btn">⬇️ تحميل ملف {file_name}</a>', unsafe_allow_html=True)
                st.write("")
        else: st.warning("⚠️ لا توجد نتائج.")

with tab2:
    f_up = st.file_uploader("اختر ملف PDF للرفع:", type=["pdf"])
    if f_up and st.button("🚀 حفظ في الأرشيف"):
        with st.spinner("جاري الرفع..."):
            res = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                                data={'chat_id': CHAT_ID, 'caption': f_up.name}, 
                                files={'document': (f_up.name, f_up.read())}).json()
            if res.get("ok"):
                save_db(f_up.name, res['result']['document']['file_id'])
                st.success(f"✅ تم حفظ '{f_up.name}' بنجاح")
