import streamlit as st
import requests
import pandas as pd
import os

# بيانات تليجرام الخاصة بك
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"
DB_FILE = "files_db.csv"

# دالة لتحميل البيانات من الملف المحلي
def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["الاسم", "file_id"])

# دالة لحفظ بيانات الملف المرفوع
def save_to_db(name, file_id):
    df = load_data()
    new_data = pd.DataFrame({"الاسم": [name], "file_id": [file_id]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

# دالة لجلب رابط التحميل من تليجرام
def get_telegram_download_link(file_id):
    try:
        # الحصول على مسار الملف
        file_info = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}").json()
        file_path = file_info['result']['file_path']
        # تكوين رابط التحميل النهائي
        download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        return download_url
    except:
        return None

st.set_page_config(page_title="أرشيف مصطفى المطور", layout="wide")
st.title("🏛️ نظام أرشفة مصطفى - واجهة التحميل المباشر")

# --- قسم الرفع ---
with st.expander("📤 رفع مستند جديد"):
    up = st.file_uploader("اختر ملف PDF:", type=["pdf"])
    if up and st.button("🚀 رفع وحفظ"):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        files = {'document': (up.name, up.read())}
        data = {'chat_id': CHAT_ID, 'caption': up.name}
        
        with st.spinner("جاري المزامنة..."):
            res = requests.post(url, data=data, files=files).json()
            if res.get("ok"):
                # استخراج file_id الفريد للملف
                f_id = res['result']['document']['file_id']
                save_to_db(up.name, f_id)
                st.success(f"✅ تم الحفظ! يمكن للموظفين الآن تحميل {up.name}")
            else:
                st.error("❌ فشل الرفع")

st.divider()

# --- قسم البحث والتحميل ---
st.subheader("🔍 محرك البحث والتحميل للموظفين")
search_query = st.text_input("اكتب اسم الملف:")

df = load_data()

if search_query:
    results = df[df['الاسم'].str.contains(search_query, na=False, case=False)]
    
    if not results.empty:
        for index, row in results.iterrows():
            col1, col2 = st.columns([3, 1])
            col1.write(f"📄 {row['الاسم']}")
            
            # زر التحميل الذكي
            d_link = get_telegram_download_link(row['file_id'])
            if d_link:
                col2.markdown(f'<a href="{d_link}" target="_blank" style="text-decoration:none;"><button style="background-color:#4CAF50; color:white; border:none; padding:5px 10px; border-radius:5px; cursor:pointer;">⬇️ تحميل الملف</button></a>', unsafe_allow_view_content=True, unsafe_allow_html=True)
            else:
                col2.write("⚠️ خطأ في الرابط")
    else:
        st.warning("⚠️ لا يوجد ملف بهذا الاسم.")
else:
    st.info("قم برفع ملف أولاً ليظهر هنا، أو ابحث في الملفات السابقة.")
