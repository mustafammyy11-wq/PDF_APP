import streamlit as st
import requests

# البيانات المستخرجة من صورك
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"

st.set_page_config(page_title="أرشيف مصطفى - تليجرام", layout="wide")

st.title("🏛️ نظام أرشفة مصطفى (تليجرام)")
st.success("✅ النظام متصل الآن بمساحة تخزين غير محدودة")

# --- قسم الرفع ---
st.subheader("📤 رفع مستند جديد")
uploaded_file = st.file_uploader("اختر ملف PDF:", type=["pdf"])

if uploaded_file and st.button("🚀 حفظ في الأرشيف"):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        # تجهيز الملف مع اسمه الأصلي
        files = {'document': (uploaded_file.name, uploaded_file.read())}
        data = {'chat_id': CHAT_ID, 'caption': f"📄 ملف: {uploaded_file.name}"}
        
        with st.spinner("جاري النقل إلى مخزن تليجرام..."):
            response = requests.post(url, data=data, files=files)
        
        if response.status_code == 200:
            st.success(f"✅ تم حفظ '{uploaded_file.name}' بنجاح!")
            st.balloons()
        else:
            st.error("❌ فشل الرفع، تأكد من اتصال الإنترنت.")
    except Exception as e:
        st.error(f"❌ حدث خطأ: {e}")

st.divider()

# --- قسم البحث ---
st.subheader("🔍 البحث عن الملفات")
st.info("للبحث عن ملفاتك، افتح قناتك (ارشيف مصطفى) في تليجرام واستخدم زر البحث 🔍 المدمج هناك.")
