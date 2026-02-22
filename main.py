import streamlit as st
import requests
import pandas as pd

# --- الإعدادات الخاصة بك ---
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"

# الرابط الجديد الذي أرسلته أنت الآن (تم تحديثه)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwRMcjPfNv5U0BemK6XxzWfugH2TtKxcyKLseM_LvCR6vyuAtBSKi6VMVDiNgfxRkl5NA/exec"

# الـ ID الخاص بجدول "أرشيف المحطات"
SHEET_ID = "1Y8cnKKctMF54jOcnCLKSH3JhfG5Evsf6OXizPnPXtJk"

# رابط القراءة المباشر لضمان تحديث البيانات فوراً
SEARCH_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

st.set_page_config(page_title="أرشفة المحطات", page_icon="🚚", layout="centered")

# --- التنسيق الجمالي ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    h1, h2, h3, p, span, div, label { color: #000000 !important; }
    div.stButton > button {
        background: linear-gradient(90deg, #0072ff 0%, #00c6ff 100%) !important;
        color: white !important; font-weight: bold !important; border-radius: 12px !important; width: 100% !important;
    }
    div.stDownloadButton > button {
        background-color: #28a745 !important; color: white !important;
        font-weight: bold !important; border-radius: 12px !important; width: 100% !important;
    }
    .file-card { 
        background-color: #f8f9fa; padding: 15px; border-radius: 12px; 
        border-right: 6px solid #0072ff; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الدخول ---
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🔐 نظام الأرشفة</h2>", unsafe_allow_html=True)
    pw = st.text_input("الرمز السري:", type="password")
    if st.button("دخول"):
        if pw == "123": st.session_state.auth = True; st.rerun()
        else: st.error("❌ الرمز خطأ")
    st.stop()

# --- الواجهة ---
st.markdown("<h1 style='text-align:center; color:#0072ff;'>🚚 أرشيف المحطات</h1>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🔍 البحث عن ملف", "📤 إضافة ملف جديد"])

with tab1:
    search_q = st.text_input("🔎 ابحث عن اسم الكتاب:")
    try:
        # قراءة أحدث نسخة من الجدول
        df = pd.read_csv(SEARCH_URL)
        if search_q and not df.empty:
            res = df[df['الاسم'].str.contains(search_q, na=False, case=False)]
            if not res.empty:
                for i, row in res.iterrows():
                    st.markdown(f'<div class="file-card">📄 {row["الاسم"]}</div>', unsafe_allow_html=True)
                    f_info = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={row['file_id']}").json()
                    if f_info.get("ok"):
                        f_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{f_info['result']['file_path']}"
                        st.download_button("⬇️ تحميل الملف", requests.get(f_url).content, file_name=f"{row['الاسم']}.pdf", key=f"d_{i}")
            else: st.warning("لا توجد نتائج مطابقة.")
    except: st.info("بانتظار إضافة ملفات للأرشيف...")

with tab2:
    f_up = st.file_uploader("اختر ملف PDF:", type=["pdf"])
    if f_up and st.button("🚀 حفظ للأبد"):
        with st.spinner("جاري التخزين في تليجرام وجوجل..."):
            # 1. الرفع لتليجرام
            res_tg = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                                   data={'chat_id': CHAT_ID, 'caption': f_up.name}, 
                                   files={'document': (f_up.name, f_up.read())}).json()
            if res_tg.get("ok"):
                f_id = res_tg['result']['document']['file_id']
                # 2. التوثيق في جوجل شيت عبر الرابط الجديد
                requests.get(f"{SCRIPT_URL}?name={f_up.name}&id={f_id}")
                st.success(f"✅ تم حفظ {f_up.name} بنجاح!")
            else:
                st.error("فشل الرفع لتليجرام. تأكد من إعدادات البوت.")
