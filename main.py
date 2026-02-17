import streamlit as st
import requests
import pandas as pd
import os

# بياناتك الخاصة بتليجرام
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"
DB_FILE = "files_db.csv"

# دالة لتحميل قاعدة البيانات
def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["الاسم", "الرابط"])

# دالة لحفظ بيانات ملف جديد
def save_to_db(name, link):
    df = load_data()
    new_data = pd.DataFrame({"الاسم": [name], "الرابط": [link]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

st.set_page_config(page_title="أرشيف مصطفى الذكي", layout="wide")

st.title("🏛️ نظام الأرشفة الموحد (تليجرام)")

# --- القسم الأول: الرفع (Upload) ---
with st.expander("📤 رفع ملف جديد (اضغط هنا لفتح القسم)"):
    up = st.file_uploader("اختر ملف PDF:", type=["pdf"])
    if up and st.button("🚀 بدء الحفظ"):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        files = {'document': (up.name, up.read())}
        data = {'chat_id': CHAT_ID, 'caption': up.name}
        
        with st.spinner("جاري المزامنة مع تليجرام..."):
            res = requests.post(url, data=data, files=files)
            if res.status_code == 200:
                # الحصول على رابط داخلي للملف (اختياري) أو مجرد تأكيد
                save_to_db(up.name, "محفوظ في تليجرام")
                st.success(f"✅ تم حفظ {up.name} بنجاح!")
            else:
                st.error("❌ حدث خطأ في الاتصال")

st.divider()

# --- القسم الثاني: البحث (Search) ---
st.subheader("🔍 محرك بحث الموظفين")
search_query = st.text_input("اكتب اسم الملف للبحث:")

df = load_data()

if search_query:
    # البحث في الأسماء التي تحتوي على النص المكتوب
    results = df[df['الاسم'].str.contains(search_query, na=False, case=False)]
    
    if not results.empty:
        st.write(f"📂 تم العثور على ({len(results)}) ملف:")
        for index, row in results.iterrows():
            col1, col2 = st.columns([3, 1])
            col1.write(f"📄 {row['الاسم']}")
            if col2.button("فتح/تحميل", key=index):
                st.info("💡 الملف موجود في قناة التليجرام باسمه الحالي.")
    else:
        st.warning("⚠️ لا يوجد ملف بهذا الاسم في الأرشيف.")
else:
    st.write("اكتب شيئاً أعلاه لتبدأ البحث...")

# عرض أرشيف سريع لآخر 5 ملفات
if not df.empty:
    with st.sidebar:
        st.subheader("🕒 آخر الملفات المضافة")
        st.table(df.tail(5)['الاسم'])
