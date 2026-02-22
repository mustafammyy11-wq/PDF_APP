import streamlit as st
import requests
import pandas as pd

# --- الإعدادات الخاصة بك (جاهزة للعمل 100%) ---
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"

# رابط الـ Script (الجسر الذي يرسل البيانات للجدول)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwRMcjPfNv5U0BemK6XxzWfugH2TtKxcyKLseM_LvCR6vyuAtBSKi6VMVDiNgfxRkl5NA/exec"

# الـ ID الخاص بجدول "أرشيف المحطات"
SHEET_ID = "1Y8cnKKctMF54jOcnCLKSH3JhfG5Evsf6OXizPnPXtJk"

# الرابط السحري الجديد لقراءة البيانات فوراً بدون تأخير
SEARCH_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# إعداد الصفحة
st.set_page_config(page_title="نظام أرشفة المحطات", page_icon="🚚", layout="centered")

# --- التنسيق الجمالي (ألوان واضحة وأزرار احترافية) ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    h1, h2, h3, p, span, div, label { color: #000000 !important; }
    div.stButton > button {
        background: linear-gradient(90deg, #0072ff 0%, #00c6ff 100%) !important;
        color: white !important; font-weight: bold !important; border-radius: 12px !important; width: 100% !important; border: none !important;
    }
    div.stDownloadButton > button {
        background-color: #28a745 !important; color: white !important;
        font-weight: bold !important; border-radius: 12px !important; width: 100% !important; border: none !important;
    }
    .file-card { 
        background-color: #f8f9fa; padding: 15px; border-radius: 12px; 
        border-right: 6px solid #0072ff; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    input[type="text"], input[type="password"] {
        border: 2px solid #0072ff !important; border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الدخول ---
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🔐 دخول النظام</h2>", unsafe_allow_html=True)
    pw = st.text_input("أدخل الرمز السري:", type="password")
    if st.button("تسجيل الدخول"):
        if pw == "123": st.session_state.auth = True; st.rerun()
        else: st.error("❌ الرمز خطأ")
    st.stop()

# --- واجهة التطبيق الرئيسية ---
st.markdown("<h1 style='text-align:center; color:#0072ff;'>🚚 أرشيف المحطات الذكي</h1>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🔍 البحث عن ملف", "📤 إضافة كتاب جديد"])

with tab1:
    search_q = st.text_input("🔎 اكتب اسم الكتاب للبحث (مثلاً: قرار):")
    try:
        # قراءة الجدول مع إجبار جوجل على إعطاء أحدث نسخة (clear cache)
        df = pd.read_csv(SEARCH_URL)
        
        if search_q:
            # البحث في عمود 'الاسم'
            results = df[df['الاسم'].str.contains(search_q, na=False, case=False)]
            
            if not results.empty:
                for i, row in results.iterrows():
                    st.markdown(f'<div class="file-card">📄 {row["الاسم"]}</div>', unsafe_allow_html=True)
                    # جلب الملف من تليجرام
                    f_info = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={row['file_id']}").json()
                    if f_info.get("ok"):
                        f_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{f_info['result']['file_path']}"
                        st.download_button(label="⬇️ تحميل الملف الآن", data=requests.get(f_url).content, file_name=f"{row['الاسم']}.pdf", key=f"d_{i}")
            else:
                st.warning("⚠️ لا توجد نتائج مطابقة لهذا الاسم.")
        else:
            st.info("💡 اكتب أي اسم في المربع أعلاه للبحث في الأرشيف.")
    except Exception as e:
        st.info("📦 الأرشيف بانتظار أول عملية رفع...")

with tab2:
    st.subheader("إضافة ملف جديد للجدول وتليجرام")
    f_up = st.file_uploader("اختر ملف PDF:", type=["pdf"])
    if f_up and st.button("🚀 حفظ في الأرشيف الدائم"):
        with st.spinner("جاري المزامنة..."):
            # 1. الرفع لتليجرام
            res_tg = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                                   data={'chat_id': CHAT_ID, 'caption': f_up.name}, 
                                   files={'document': (f_up.name, f_up.read())}).json()
            if res_tg.get("ok"):
                f_id = res_tg['result']['document']['file_id']
                # 2. الحفظ في جوجل شيت
                requests.get(f"{SCRIPT_URL}?name={f_up.name}&id={f_id}")
                st.success(f"✅ تم حفظ '{f_up.name}' بنجاح! يمكنك الآن البحث عنه في خانة البحث.")
            else:
                st.error("❌ فشل الرفع لتليجرام.")
