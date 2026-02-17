import streamlit as st
import requests
import pandas as pd
import os

# بياناتك الخاصة
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"
DB_FILE = "files_db.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["الاسم", "file_id"])

def save_to_db(name, file_id):
    df = load_data()
    new_data = pd.DataFrame({"الاسم": [name], "file_id": [file_id]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

def get_telegram_download_link(file_id):
    try:
        file_info = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}").json()
        if file_info.get("ok"):
            file_path = file_info['result']['file_path']
            return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    except:
        return None
    return None

st.set_page_config(page_title="أرشيف مصطفى المطور", layout="wide")
st.title("🏛️ نظام أرشفة مصطفى الموحد")

# --- قسم الرفع ---
with st.expander("📤 رفع مستند جديد"):
    up = st.file_uploader("اختر ملف PDF:", type=["pdf"])
    if up and st.button("🚀 حفظ في الأرشيف"):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        files = {'document': (up.name, up.read())}
        data = {'chat_id': CHAT_ID, 'caption': up.name}
        
        with st.spinner("جاري المزامنة مع تليجرام..."):
            res = requests.post(url, data=data, files=files).json()
            if res.get("ok"):
                f_id = res['result']['document']['file_id']
                save_to_db(up.name, f_id)
                st.success(f"✅ تم الحفظ بنجاح!")
            else:
                st.error("❌ فشل الرفع")

st.divider()

# --- قسم البحث والتحميل للموظفين ---
st.subheader("🔍 محرك البحث والتحميل للموظفين")
search_query = st.text_input("اكتب اسم الملف:")

df = load_data()

if search_query:
    results = df[df['الاسم'].str.contains(search_query, na=False, case=False)]
    
    if not results.empty:
        for index, row in results.iterrows():
            col1, col2 = st.columns([3, 1])
            col1.write(f"📄 {row['الاسم']}")
            
            # جلب رابط التحميل
            d_link = get_telegram_download_link(row['file_id'])
            if d_link:
                # تصحيح الخطأ البرمجي في كتابة markdown
                col2.markdown(f'<a href="{d_link}" target="_blank" style="text-decoration:none;"><button style="background-color:#4CAF50; color:white; border:none; padding:8px 15px; border-radius:5px; cursor:pointer; width:100%;">⬇️ تحميل</button></a>', unsafe_allow_html=True)
            else:
                col2.warning("⚠️ الرابط غير متاح")
    else:
        st.warning("⚠️ لا يوجد ملف بهذا الاسم.")
