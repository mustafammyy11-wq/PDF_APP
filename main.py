import streamlit as st
import dropbox
import io

# ضع الرمز (Token) الخاص بك هنا بين علامتي التنصيص
TOKEN = "الرمز_الذي_أرسلته_هنا"

st.set_page_config(page_title="أرشيف مصطفى")
st.title("🏛️ نظام أرشفة مصطفى (نسخة Dropbox)")

# واجهة رفع الملفات
up = st.file_uploader("اختر ملف PDF للرفع:", type=["pdf"])

if up and st.button("🚀 رفع الملف الآن"):
    try:
        # الاتصال بـ Dropbox
        dbx = dropbox.Dropbox(TOKEN)
        
        with st.spinner("جاري الرفع إلى Dropbox..."):
            # رفع الملف إلى المجلد الرئيسي في دروب بوكس
            dbx.files_upload(up.read(), f"/{up.name}", mode=dropbox.files.WriteMode.overwrite)
            
        st.success("✅ مبروك يا مصطفى! تم الرفع بنجاح وبدون أي مشاكل مساحة.")
        st.balloons()
        
    except Exception as e:
        # إذا انتهت صلاحية الكود أو حدث خطأ في الصلاحيات
        st.error(f"❌ حدث خطأ: {e}")
        st.info("تأكد من تفعيل صلاحية 'files.content.write' في إعدادات تطبيق Dropbox.")
