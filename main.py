import streamlit as st
import requests
import pandas as pd
import os

# --- الإعدادات ---
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"
DB_FILE = "files_db.csv"

st.set_page_config(page_title="محطات الوزن الذكية", page_icon="🚚", layout="centered")

# --- التنسيق النهائي: إجبار اللون الأبيض للنص في الأزرار ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    h1, h2, h3, p, span, label, div { color: #000000 !important; }
    
    /* تنسيق زر التحميل: خلفية خضراء ونص أبيض ناصع */
    div.stDownloadButton > button {
        background-color: #28a745 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        width: 100% !important;
        font-weight: bold !important;
        height: 3.5em !important;
        border: none !important;
    }
    /* عند تمرير الماوس على الزر */
    div.stDownloadButton > button:hover {
        background-color: #218838 !important;
        color: #ffffff !important;
    }
    
    /* تنسيق كرت الملف */
    .file-card { 
        background-color: #f1f3f5; padding: 12px; border-radius: 10px; 
        border-right: 5px solid #0072ff; margin-bottom: 5px; 
        font-weight: bold;
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

# --- دالة جلب الملف (تُستدعى فقط عند الضغط لتسريع البحث) ---
def get_file_bytes(file_id):
    try:
        res = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}").json()
        if res.get("ok"):
            file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{res['result']['file_path']}"
            return requests.get(file_url).content
    except: return None
    return None

# --- الواجهة (ترتيب الأيقونة مع العنوان) ---
st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 20px;">
        <h1 style="color: #0072ff !important; margin: 0; font-size: 28px;">محطات الوزن الذكية</h1>
        <span style="font-size: 40px;">🚚</span>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 البحث عن ملف PDF", "📤 أرشفة ملف PDF"])

with tab1:
    search_q = st.text_input("🔎 ابحث عن الاسم (مثل: صفاء):", placeholder="اكتب هنا...")
    
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        if search_q:
            results = df[df['الاسم'].str.contains(search_q, na=False, case=False)]
            if not results.empty:
                for i, row in results.iterrows():
                    f_name = row['الاسم']
                    st.markdown(f'<div class="file-card">📄 {f_name}</div>', unsafe_allow_html=True)
                    
                    # زر التحميل السريع
                    if pd.notna(row['file_id']):
                        # تحميل المحتوى فقط إذا ضغط المستخدم
                        st.download_button(
                            label=f"⬇️ تحميل ملف {f_name}",
                            data=get_file_bytes(row['file_id']),
                            file_name=f_name if f_name.lower().endswith(".pdf") else f"{f_name}.pdf",
                            mime="application/pdf",
                            key=f"dl_{i}"
                        )
                    st.write("")
            else: st.warning("⚠️ لا توجد نتائج.")
    else: st.info("الأرشيف فارغ حالياً.")

with tab2:
    f_up = st.file_uploader("اختر ملف PDF للرفع:", type=["pdf"])
    if f_up and st.button("🚀 حفظ في الأرشيف"):
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
