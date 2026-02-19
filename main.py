import streamlit as st
import requests
import pandas as pd
import os

# --- الإعدادات ---
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"
DB_FILE = "files_db.csv"

st.set_page_config(page_title="محطات الوزن الذكية", page_icon="🚚", layout="centered")

# --- تنسيق الألوان وإجبار الأزرار على الأبيض ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    
    /* جعل كل النصوص سوداء */
    h1, h2, h3, p, span, label, div { color: #000000 !important; }
    
    /* تنسيق كروت الملفات */
    .file-card { 
        background-color: #f8f9fa; padding: 15px; border-radius: 10px; 
        border-right: 6px solid #0072ff; margin-bottom: 5px; 
    }

    /* تنسيق زر التحميل - إجبار اللون الأبيض للنص */
    div.stButton > button {
        background-color: #28a745 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        width: 100% !important;
        font-weight: bold !important;
        height: 3.5em !important;
        border: none !important;
    }
    
    /* تنسيق حقول الإدخال */
    input {
        color: #000000 !important;
        background-color: #ffffff !important;
        border: 1px solid #0072ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام تسجيل الدخول ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("<h2 style='text-align: center;'>🔐 دخول النظام</h2>", unsafe_allow_html=True)
    pw = st.text_input("كلمة المرور:", type="password")
    if st.button("تسجيل الدخول", key="login_btn"):
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

# دالة لتحميل الملف فعلياً للحفاظ على الاسم
def download_file_logic(file_id, file_name):
    try:
        res = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}").json()
        if res.get("ok"):
            file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{res['result']['file_path']}"
            file_content = requests.get(file_url).content
            return file_content
    except: return None

# --- الواجهة الرئيسية ---
st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 20px;">
        <h1 style="color: #0072ff !important; margin: 0;">محطات الوزن الذكية</h1>
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
            for i, row in results.iterrows():
                file_name = row['الاسم']
                st.markdown(f'<div class="file-card">📄 {file_name}</div>', unsafe_allow_html=True)
                
                # استخدام مكون streamlit الأصلي للتحميل لضمان الاسم الصحيح
                if pd.notna(row['file_id']):
                    file_bytes = download_file_logic(row['file_id'], file_name)
                    if file_bytes:
                        st.download_button(
                            label=f"⬇️ تحميل ملف {file_name}",
                            data=file_bytes,
                            file_name=file_name if file_name.endswith(".pdf") else f"{file_name}.pdf",
                            mime="application/pdf",
                            key=f"dl_{i}"
                        )
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
