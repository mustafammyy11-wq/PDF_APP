import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# معرف المجلد فقط
FOLDER_ID = "1RLkxpJM8CEunpNDUcANE_jVdFII7V5bW"

st.title("🏛️ نظام الأرشفة الذكي")

up = st.file_uploader("اختر ملف PDF:", type=["pdf"])

if up and st.button("🚀 رفع الملف"):
    try:
        # قراءة المفاتيح من إعدادات Streamlit (Secrets)
        creds_info = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(creds_info)
        service = build('drive', 'v3', credentials=creds)

        with st.spinner("جاري الرفع..."):
            meta = {'name': up.name, 'parents': [FOLDER_ID]}
            media = MediaIoBaseUpload(io.BytesIO(up.read()), mimetype='application/pdf')
            
            file = service.files().create(
                body=meta, 
                media_body=media, 
                supportsAllDrives=True
            ).execute()
            
            st.success("✅ نجحت العملية! الملف الآن في درايف.")
            st.balloons()
    except Exception as e:
        st.error(f"❌ خطأ: {e}")
