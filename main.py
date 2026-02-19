import streamlit as st
import requests
import pandas as pd
import os

# --- الإعدادات ---
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"
DB_FILE = "files_db.csv"

st.set_page_config(page_title="محطات الوزن الذكية", page_icon="🚚", layout="centered")

# --- إجبار الألوان (ضد الوضع الداكن في الموبايل) ---
st.markdown("""
    <style>
    /* 1. الخلفية البيضاء الشاملة */
    .stApp { background-color: #ffffff !important; }
    
    /* 2. إجبار كل النصوص على اللون الأسود الداكن */
    h1, h2, h3, p, span, label, div, .stMarkdown { color: #000000 !important; }

    /* 3. تنسيق خانة الباسورد والبحث (خلفية فاتحة ونص أسود) */
    input[type="text"], input[type="password"] {
        color: #000000 !important;
        background-color: #f0f2f6 !important;
        border: 2px solid #0072ff !important;
        -webkit-text-fill-color: #000000 !important; /* للموبايلات */
    }

    /* 4. زر تسجيل الدخول (أزرق بكتابة بيضاء) */
    div.stButton > button {
        background-color: #0072ff !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
        width: 100% !important;
    }

    /* 5. زر التحميل الأخضر (كتابة بيضاء واضحة) */
    div.stDownloadButton > button {
        background-color: #28a745 !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        width: 100% !important;
        height: 3.5em !important;
        border: none !important;
    }
    
    /* 6. كروت الملفات */
    .file-card { 
        background-color: #f1f3f5 !important; 
        padding: 15px; 
        border-radius: 10px; 
        border-right: 6px solid #0072ff; 
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام تسجيل الدخول ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("<h2 style='text-align: center; color: #000000;'>🔐 دخول النظام</h2>", unsafe_allow_html=True)
    
    # وضع الخانة والزر في حاوية مرتبة
    pw = st.text_input("أدخل الرمز السري:", type="password", key="login_field")
    if st.button("تسجيل الدخول الآن"):
        if pw == "123":
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("الرمز السري غير صحيح")
    st.stop()

# --- دالة جلب الملف ---
def get_file_content(file_id):
    try:
        res = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}").json()
        if res.get("ok"):
            file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{res['result']['file_path']}"
            return requests.get(file_url).content
    except: return None
    return None

# --- الواجهة الرئيسية ---
st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 20px;">
        <h1 style="color: #0072ff !important; margin: 0; font-size: 26px;">محطات الوزن الذكية</h1>
        <span style="font-size: 35px;">🚚</span>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 البحث عن ملف PDF", "📤 أرشفة ملف PDF"])

with tab1:
    search_q = st.text_input("🔎 ابحث عن الاسم (مثلاً: صفاء):", key="search_field")
    
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        if search_q:
            results = df[df['الاسم'].str.contains(search_q, na=False, case=False)]
            if not results.empty:
                for i, row in results.iterrows():
                    f_name = row['الاسم']
                    st.markdown(f'<div class="file-card">📄 {f_name}</div>', unsafe_allow_html=True)
                    
                    if pd.notna(row['file_id']):
                        st.download_button(
                            label=f"⬇️ تحميل ملف {f_name}",
                            data=get_file_content(row['file_id']),
                            file_name=f"{f_name}.pdf" if not f_name.lower().endswith(".pdf") else f_name,
                            mime="application/pdf",
                            key=f"dl_btn_{i}"
                        )
                    st.write("")
            else: st.warning("⚠️ لا توجد نتائج.")

with tab2:
    f_up = st.file_uploader("اختر ملف PDF للرفع:", type=["pdf"])
    if f_up and st.button("🚀 حفظ في النظام"):
        with st.spinner("جاري الرفع..."):
            res = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                                data={'chat_id': CHAT_ID, 'caption': f_up.name}, 
                                files={'document': (f_up.name, f_up.read())}).json()
            if res.get("ok"):
                new_row = pd.DataFrame({"الاسم": [f_up.name], "file_id": [res['result']['document']['file_id']]})
                if os.path.exists(DB_FILE):
                    df_all = pd.concat([pd.read_csv(DB_FILE), new_row], ignore_index=True)
                else:
                    df_all = new_row
                df_all.to_csv(DB_FILE, index=False)
                st.success("✅ تم الحفظ بنجاح")
