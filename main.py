import streamlit as st
import requests
import pandas as pd
import os

# --- الإعدادات ---
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"
DB_FILE = "files_db.csv"

st.set_page_config(page_title="محطات الوزن الذكية", page_icon="🚚", layout="centered")

# --- التنسيق النهائي لحل مشكلة الألوان السوداء ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    h1, h2, h3, p, span, label, div { color: #000000 !important; }
    
    /* تنسيق زر التحميل ليكون أخضر بكتابة بيضاء واضحة جداً */
    div.stDownloadButton > button {
        background-color: #28a745 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        width: 100% !important;
        font-weight: bold !important;
        height: 3.5em !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    
    /* تحسين شكل كرت الملف */
    .file-card { 
        background-color: #f1f3f5; padding: 12px; border-radius: 10px; 
        border-right: 5px solid #0072ff; margin-bottom: 5px; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام تسجيل الدخول ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("<h2 style='text-align: center;'>🔐 دخول النظام</h2>", unsafe_allow_html=True)
    pw = st.text_input("كلمة المرور:", type="password")
    if st.button("تسجيل الدخول"):
        if pw == "123":
            st.session_state["authenticated"] = True
            st.rerun()
    st.stop()

# --- الدوال المحسنة للسرعة ---
@st.cache_data
def load_db():
    if os.path.exists(DB_FILE): return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["الاسم", "file_id"])

def get_file_content(file_id):
    try:
        res = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}").json()
        if res.get("ok"):
            file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{res['result']['file_path']}"
            return requests.get(file_url).content
    except: return None

# --- الواجهة ---
st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 20px;">
        <h1 style="color: #0072ff !important; margin: 0;">محطات الوزن الذكية</h1>
        <span style="font-size: 40px;">🚚</span>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 البحث عن ملف PDF", "📤 أرشفة ملف PDF"])

with tab1:
    search_q = st.text_input("🔎 ابحث عن الاسم (مثل: صفاء):")
    df = load_db()
    
    if search_q:
        results = df[df['الاسم'].str.contains(search_q, na=False, case=False)]
        if not results.empty:
            for i, row in results.iterrows():
                file_name = row['الاسم']
                st.markdown(f'<div class="file-card">📄 {file_name}</div>', unsafe_allow_html=True)
                
                # تسريع البحث: لا يتم تحميل الملف إلا عند الضغط
                if pd.notna(row['file_id']):
                    # عرض زر التحميل بالاسم الأصلي وتنسيق اللون الأبيض
                    st.download_button(
                        label=f"⬇️ اضغط هنا لتحميل: {file_name}",
                        data=get_file_content(row['file_id']) if st.session_state.get(f"load_{i}") else b"",
                        file_name=file_name if file_name.lower().endswith(".pdf") else f"{file_name}.pdf",
                        mime="application/pdf",
                        key=f"btn_{i}",
                        on_click=lambda idx=i: st.session_state.update({f"load_{idx}": True})
                    )
                st.write("")
        else: st.warning("⚠️ لا توجد نتائج.")

with tab2:
    f_up = st.file_uploader("اختر ملف PDF:", type=["pdf"])
    if f_up and st.button("🚀 حفظ"):
        res = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                            data={'chat_id': CHAT_ID, 'caption': f_up.name}, 
                            files={'document': (f_up.name, f_up.read())}).json()
        if res.get("ok"):
            new_data = pd.DataFrame({"الاسم":
