import streamlit as st
import requests
import pandas as pd
import time

# --- 1. الإعدادات (نفس بياناتك السابقة) ---
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwRMcjPfNv5U0BemK6XxzWfugH2TtKxcyKLseM_LvCR6vyuAtBSKi6VMVDiNgfxRkl5NA/exec"
SHEET_ID = "1Y8cnKKctMF54jOcnCLKSH3JhfG5Evsf6OXizPnPXtJk"
SEARCH_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0&t={int(time.time())}"

st.set_page_config(page_title="أرشيف المحطات", page_icon="🚚", layout="centered")

# --- 2. تنسيق CSS مخصص للهاتف (لحل مشكلة اختفاء الأزرار والبحث) ---
st.markdown("""
    <style>
    /* جعل الخلفية بيضاء تماماً */
    .stApp { background-color: #FFFFFF; }
    
    /* تنسيق شريط البحث ليكون واضحاً جداً */
    .stTextInput input {
        border: 2px solid #0072ff !important;
        border-radius: 15px !important;
        padding: 15px !important;
        font-size: 18px !important;
        background-color: #f0f2f6 !important;
        color: #000000 !important;
    }
    
    /* تنسيق الأزرار لتكون ملونة وواضحة دائماً */
    .stButton > button {
        background: #0072ff !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: bold !important;
        height: 50px !important;
        width: 100% !important;
        display: block !important;
        margin-top: 10px !important;
    }
    
    /* تنسيق التبويبات (Tabs) لتكون واضحة */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #e9ecef;
        border-radius: 8px;
        color: #495057;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0072ff !important;
        color: white !important;
    }

    /* كروت عرض النتائج */
    .file-card { 
        background-color: #f8f9fa; padding: 20px; border-radius: 15px; 
        border-right: 8px solid #0072ff; margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. الدخول ---
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center; color: #0072ff;'>🚚 دخول النظام</h2>", unsafe_allow_html=True)
    pw = st.text_input("رمز الدخول:", type="password")
    if st.button("دخول"):
        if pw == "123": st.session_state.auth = True; st.rerun()
        else: st.error("❌ الرمز خطأ")
    st.stop()

# --- 4. الواجهة الرئيسية ---
st.markdown("<h1 style='text-align:center; color:#0072ff; margin-bottom: 20px;'>🚚 نظام أرشفة المحطات</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 البحث السريع", "📤 إضافة كتاب"])

with tab1:
    st.markdown("### 🔎 ابحث عن اسم الكتاب:")
    # شريط البحث الآن واضح وبارز
    search_q = st.text_input("", placeholder="اكتب هنا.. (مثلاً: كباشي، قرار، توجيه)", key="main_search")
    
    try:
        df = pd.read_csv(SEARCH_URL)
        df.columns = df.columns.str.strip()
        
        if search_q:
            results = df[df.iloc[:, 0].astype(str).str.contains(search_q, na=False, case=False)]
            if not results.empty:
                st.info(f"📍 تم العثور على {len(results)} ملف")
                for i, row in results.iterrows():
                    with st.container():
                        st.markdown(f'<div class="file-card">📄 {row.iloc[0]}</div>', unsafe_allow_html=True)
                        f_info = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={row.iloc[1]}").json()
                        if f_info.get("ok"):
                            f_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{f_info['result']['file_path']}"
                            st.download_button("⬇️ تحميل الملف الآن", requests.get(f_url).content, file_name=f"{row.iloc[0]}.pdf", key=f"dl_{i}")
            else:
                st.warning("⚠️ لا توجد نتائج لهذا الاسم.")
        else:
            st.markdown("<p style='text-align:center; color:gray;'>الأرشيف جاهز للبحث في الملفات المرفوعة حالياً.</p>", unsafe_allow_html=True)
    except:
        st.info("📦 بانتظار تحديث البيانات...")

with tab2:
    st.markdown("### 📤 رفع ملف جديد")
    f_up = st.file_uploader("اختر ملف PDF من الهاتف:", type=["pdf"])
    if f_up and st.button("🚀 حفظ ومزامنة"):
        with st.spinner("جاري الرفع..."):
            res_tg = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                                   data={'chat_id': CHAT_ID, 'caption': f_up.name}, 
                                   files={'document': (f_up.name, f_up.read())}).json()
            if res_tg.get("ok"):
                f_id = res_tg['result']['document']['file_id']
                requests.get(f"{SCRIPT_URL}?name={f_up.name}&id={f_id}")
                st.success(f"✅ تم حفظ {f_up.name} بنجاح!")
                time.sleep(2)
                st.rerun()rt time
