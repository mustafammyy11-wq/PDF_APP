import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# معرف المجلد من حسابك الشخصي
FOLDER_ID = "1RLkxpJM8CEunpNDUcANE_jVdFII7V5bW"

st.title("🏛️ نظام أرشفة مصطفى")

up = st.file_uploader("اختر ملف PDF:", type=["pdf"])

if up and st.button("🚀 رفع إلى ملفاتي"):
    try:
        # استخدام الأسرار المخزنة في Streamlit
        creds_info = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(creds_info)
        service = build('drive', 'v3', credentials=creds)

        with st.spinner("جاري الرفع لحسابك الشخصي..."):
            file_metadata = {
                'name': up.name,
                'parents': [FOLDER_ID]
            }
            media = MediaIoBaseUpload(io.BytesIO(up.read()), mimetype='application/pdf')
            
            # الرفع مع تفعيل صلاحيات المستخدم الشخصي
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            st.success("✅ تمت العملية بنجاح يا مصطفى!")
            st.balloons()
    except Exception as e:
        st.error(f"❌ خطأ: {e}")
