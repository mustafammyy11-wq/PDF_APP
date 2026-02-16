import streamlit as st
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import io

# 1. معرف المجلد الشخصي
FOLDER_ID = "1RLkxpJM8CEunpNDUcANE_jVdFII7V5bW"

st.title("🏛️ نظام أرشفة مصطفى (الرفع المباشر)")

up = st.file_uploader("اختر ملف PDF:", type=["pdf"])

if up and st.button("🚀 تنفيذ الرفع"):
    try:
        # 2. إعداد الصلاحيات باستخدام PyDrive2 لتجاوز قيود Quota
        scope = ['https://www.googleapis.com/auth/drive']
        creds_info = st.secrets["gcp_service_account"]
        
        # إنشاء ملف مؤقت للمفاتيح (ضروري لهذه المكتبة)
        gauth = GoogleAuth()
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
        gauth.credentials = creds
        drive = GoogleDrive(gauth)

        with st.spinner("جاري كسر قيود المساحة والرفع..."):
            # 3. إنشاء الملف وتحديده لمجلدك الشخصي
            file_drive = drive.CreateFile({
                'title': up.name,
                'parents': [{'id': FOLDER_ID}]
            })
            
            # رفع المحتوى
            file_drive.content = io.BytesIO(up.read())
            file_drive.Upload() # الرفع المباشر

            st.success("✅ أخيراً! تمت العملية بنجاح ووصل الملف.")
            st.balloons()

    except Exception as e:
        st.error(f"❌ محاولة أخيرة فشلت: {e}")
        st.info("نصيحة: إذا استمر هذا الخطأ، جرب إنشاء إيميل (Service Account) جديد تماماً، فقد يكون هذا الإيميل محظوراً من جوجل.")
