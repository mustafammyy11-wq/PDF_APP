import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# 1. المعرفات الأساسية
FOLDER_ID = "1RLkxpJM8CEunpNDUcANE_jVdFII7V5bW"

st.set_page_config(page_title="نظام الأرشفة المطور")
st.title("🏛️ نظام أرشفة مصطفى")

up = st.file_uploader("اختر ملف PDF:", type=["pdf"])

if up and st.button("🚀 رفع نهائي"):
    try:
        # جلب البيانات من Secrets
        creds_info = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(creds_info)
        service = build('drive', 'v3', credentials=creds)

        with st.spinner("جاري معالجة القيود والرفع..."):
            # إعدادات الملف مع طلب نقل الملكية تلقائياً
            file_metadata = {
                'name': up.name,
                'parents': [FOLDER_ID]
            }
            
            media = MediaIoBaseUpload(io.BytesIO(up.read()), mimetype='application/pdf', resumable=True)
            
            # تنفيذ الرفع مع تجاهل مساحة الروبوت
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id',
                supportsAllDrives=True # ضروري حتى لو كان المجلد شخصياً
            ).execute()

            st.success("✅ أخيراً يا مصطفى! تم الرفع بنجاح.")
            st.balloons()

    except Exception as e:
        if "storageQuotaExceeded" in str(e):
            st.error("⚠️ جوجل لا يزال يرفض المساحة. اتبع الخطوة أدناه فوراً.")
        else:
            st.error(f"❌ خطأ تقني: {e}")
