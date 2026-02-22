import streamlit as st
import requests
import pandas as pd
import time

# --- 1. الإعدادات ---
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwRMcjPfNv5U0BemK6XxzWfugH2TtKxcyKLseM_LvCR6vyuAtBSKi6VMVDiNgfxRkl5NA/exec"
SHEET_ID = "1Y8cnKKctMF54jOcnCLKSH3JhfG5Evsf6OXizPnPXtJk"
SEARCH_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0&t={int(time.time())}"

st.set_page_config(page_title="أرشيف المحطات", page_icon="🚚")

# --- 2. تنسيق الألوان والبحث (لجعلها واضحة في الهاتف) ---
st.markdown("""
    <style>
    /* جعل الأزرار ملونة وواضحة دائماً */
    .stButton > button {
        background-color: #0072ff !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        height: 50px !important;
        width: 100% !important;
    }
    /* جعل شريط البحث بارزاً بخلفية فاتحة */
    .stTextInput input {
        background-color: #f0f2f6 !important;
        color: black !important;
        border: 2px solid #0072ff !important;
        border-radius: 10px !important;
    }
    /* تنسيق كروت النتائج */
    .file-card { 
        background-color: #ffffff; padding: 15px; border-radius: 10px; 
        border-right: 6px solid #0072ff; margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1); color: black;
    }
    /* توضيح التبويبات */
    .stTabs [data-baseweb="tab"] {
        font-size: 16px !important;
        font-weight: bold !important;
        color: #0072ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. نظام الدخول ---
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🔐 دخول النظام</h2>", unsafe_allow_html=True)
    pw = st.text_input("رمز الدخول:", type="password")
    if st.button("دخول"):
        if pw == "123":
            st.session_state.auth = True
            st.rerun()
        else: st.error("❌ الرمز خطأ")
    st.stop()

# --- 4. الواجهة الرئيسية ---
st.markdown("<h1 style='text-align:center; color:#0072ff;'>🚚 أرشيف المحطات</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 البحث عن ملف", "📤 إضافة ملف جديد"])

with tab1:
    st.markdown("### 🔎 ابحث هنا:")
    search_q = st.text_input("", placeholder="اكتب اسم الكتاب هنا...")
    
    try:
        df = pd.read_csv(SEARCH_URL)
        df.columns = df.columns.str.strip()
        
        if search_q:
            results = df[df.iloc[:, 0].astype(str).str.contains(search_q, na=False, case=False)]
            if not results.empty:
                for i, row in results.iterrows():
                    st.markdown(f'<div class="file-card">📄 {row.iloc[0]}</div>', unsafe_allow_html=True)
                    f_info = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={row.iloc[1]}").json()
                    if f_info.get("ok"):
                        f_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{f_info['result']['file_path']}"
                        st.download_button("⬇️ تحميل الملف", requests.get(f_url).content, file_name=f"{row.iloc[0]}.pdf", key=f"dl_{i}")
            else:
                st.warning("⚠️ لا توجد نتائج.")
        else:
            st.info("💡 اكتب اسم الملف (مثل: كباشي) للبحث.")
    except:
        st.info("📦 بانتظار تحديث البيانات...")

with tab2:
    st.markdown("### 📤 رفع ملف جديد")
    f_up = st.file_uploader("اختر ملف PDF:", type=["pdf"])
    if f_up and st.button("🚀 حفظ الملف"):
        with st.spinner("جاري الرفع..."):
            res_tg = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                                   data={'chat_id': CHAT_ID, 'caption': f_up.name}, 
                                   files={'document': (f_up.name, f_up.read())}).json()
            if res_tg.get("ok"):
                f_id = res_tg['result']['document']['file_id']
                requests.get(f"{SCRIPT_URL}?name={f_up.name}&id={f_id}")
                st.success(f"✅ تم حفظ {f_up.name}")
                time.sleep(1)
                st.rerun()
