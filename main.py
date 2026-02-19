import streamlit as st
import requests
import pandas as pd
import os

# --- الإعدادات ---
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"
DB_FILE = "files_db.csv"

st.set_page_config(page_title="محطات الوزن الذكية", page_icon="🚚", layout="centered")

# --- تنسيق CSS احترافي وجميل ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    h1, h2, h3, p, span, label, div { color: #000000 !important; }

    /* تجميل شريط البحث والمدخلات */
    input[type="text"], input[type="password"] {
        color: #000000 !important;
        background-color: #ffffff !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 15px !important;
        padding: 12px !important;
        font-size: 16px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
    }
    input:focus { border-color: #0072ff !important; }

    /* تجميل زر تسجيل الدخول */
    div.stButton > button {
        background: linear-gradient(90deg, #0072ff 0%, #00c6ff 100%) !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        border: none !important;
        padding: 10px 20px !important;
        transition: 0.3s !important;
    }

    /* تجميل زر التحميل */
    div.stDownloadButton > button {
        background-color: #28a745 !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        width: 100% !important;
        border: none !important;
        height: 3em !important;
    }
    
    /* كروت النتائج */
    .file-card { 
        background-color: #f9f9f9 !important; 
        padding: 12px; border-radius: 12px; 
        border-right: 5px solid #0072ff; margin-bottom: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام تسجيل الدخول ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("<div style='text-align:center;'><h1 style='font-size:50px;'>🔐</h1></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin-bottom:20px;'>نظام الأرشفة الذكي</h2>", unsafe_allow_html=True)
    pw = st.text_input("أدخل الرمز السري الموحد:", type="password")
    if st.button("دخول للنظام"):
        if pw == "123":
            st.session_state["authenticated"] = True
            st.rerun()
        else: st.error("⚠️ الرمز السري غير صحيح")
    st.stop()

# --- دوال البحث والتحميل السريع ---
@st.cache_data(show_spinner=False)
def get_file_content(file_id):
    try:
        res = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}").json()
        if res.get("ok"):
            url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{res['result']['file_path']}"
            return requests.get(url).content
    except: return None
    return None

# --- الواجهة ---
st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 25px;">
        <h1 style="color: #0072ff !important; margin: 0; font-size: 26px;">محطات الوزن الذكية</h1>
        <span style="font-size: 35px;">🚚</span>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 البحث السريع", "📤 إضافة ملف جديد"])

with tab1:
    # شريط بحث جميل
    search_q = st.text_input("📝 ابحث عن اسم الكتاب أو الملف:", placeholder="مثلاً: صفاء...")
    
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        if search_q:
            results = df[df['الاسم'].str.contains(search_q, na=False, case=False)]
            if not results.empty:
                st.markdown(f"<p style='color:grey;'>تم العثور على {len(results)} ملفات</p>", unsafe_allow_html=True)
                for i, row in results.iterrows():
                    f_name = row['الاسم']
                    with st.container():
                        st.markdown(f'<div class="file-card">📄 {f_name}</div>', unsafe_allow_html=True)
                        
                        # تحميل المحتوى وتخزينه لمرة واحدة لسرعة البحث
                        if pd.notna(row['file_id']):
                            f_bytes = get_file_content(row['file_id'])
                            if f_bytes:
                                st.download_button(
                                    label=f"⬇️ تحميل الآن",
                                    data=f_bytes,
                                    file_name=f_name if f_name.lower().endswith(".pdf") else f"{f_name}.pdf",
                                    mime="application/pdf",
                                    key=f"btn_dl_{i}"
                                )
                        st.write("---")
            else: st.warning("🔍 لا توجد نتائج مطابقة")
    else: st.info("📭 الأرشيف لا يحتوي على ملفات بعد.")

with tab2:
    f_up = st.file_uploader("اختر ملف PDF:", type=["pdf"])
    if f_up and st.button("🚀 رفع للأرشيف"):
        with st.spinner("جاري المزامنة مع تليجرام..."):
            res = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                                data={'chat_id': CHAT_ID, 'caption': f_up.name}, 
                                files={'document': (f_up.name, f_up.read())}).json()
            if res.get("ok"):
                new_row = pd.DataFrame({"الاسم": [f_up.name], "file_id": [res['result']['document']['file_id']]})
                df_all = pd.concat([pd.read_csv(DB_FILE) if os.path.exists(DB_FILE) else pd.DataFrame(columns=["الاسم", "file_id"]), new_row], ignore_index=True)
                df_all.to_csv(DB_FILE, index=False)
                st.cache_data.clear() # مسح الذاكرة لتحديث النتائج فوراً
                st.success("✅ تم الحفظ بنجاح")
