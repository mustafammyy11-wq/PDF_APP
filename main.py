import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# 1. إعدادات المجلد والمعلومات الأساسية
FOLDER_ID = "1O9RsIkXihdZrGMaLrALM3dYDjm6x23nL"

def get_drive_service():
    """الربط مع جوجل درايف باستخدام Secrets"""
    try:
        info = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(info)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        st.error(f"خطأ في ملف الجيسون: {e}")
        return None

st.set_page_config(page_title="أرشيف محطة الوزن", layout="centered")

# نظام الدخول
password = st.sidebar.text_input("أدخل رمز الدخول:", type="password")
if password == "123":
    st.title("🏛️ الأرشيف الذكي")
    service = get_drive_service()
    
    if service:
        # تبويبات العمل
        tab1, tab2 = st.tabs(["📤 رفع وصل", "🔍 بحث"])
        
        with tab1:
            uploaded_file = st.file_uploader("اختر ملف:")
            if uploaded_file and st.button("تأكيد الرفع"):
                try:
                    file_metadata = {'name': uploaded_file.name, 'parents': [FOLDER_ID]}
                    media = MediaIoBaseUpload(io.BytesIO(uploaded_file.read()), mimetype=uploaded_file.type)
                    service.files().create(body=file_metadata, media_body=media).execute()
                    st.success("✅ تم الرفع بنجاح!")
                except Exception as e:
                    st.error(f"فشل الرفع: تأكد من مشاركة المجلد مع الايميل الموضح بالأسفل.")
                    st.info(f"الايميل: {st.secrets['gcp_service_account']['client_email']}")

        with tab2:
            q = st.text_input("ابحث عن ملف:")
            if q:
                query_str = f"'{FOLDER_ID}' in parents and name contains '{q}'"
                results = service.files().list(q=query_str, fields="files(id, name, webViewLink)").execute()
                items = results.get('files', [])
                for item in items:
                    st.write(f"📄 {item['name']}")
                    st.link_button("فتح", item['webViewLink'])
else:
    st.warning("أدخل الرمز 123")
