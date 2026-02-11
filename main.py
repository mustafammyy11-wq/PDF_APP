import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# جلب الخدمة
def get_drive_service():
    try:
        info = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(info)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        st.error(f"خطأ في ملف الجيسون (Secrets): {e}")
        return None

st.set_page_config(page_title="أرشيف المحطة", layout="centered")

# تأكد من معرف المجلد هنا
FOLDER_ID = "1O9RsIkXihdZrGMaLrALM3dYDjm6x23nL"

if st.sidebar.text_input("الرمز:", type="password") == "123":
    st.title("🏛️ الأرشيف الذكي")
    service = get_drive_service()
    
    if service:
        # اختبار الاتصال بالمجلد
        try:
            folder = service.files().get(fileId=FOLDER_ID, fields='name').execute()
            st.success(f"✅ متصل بنجاح بمجلد: {folder['name']}")
        except Exception:
            st.error("❌ البرمجية لا ترى المجلد. تأكد من مشاركة المجلد مع الايميل كـ Editor.")
            st.info(f"الايميل المطلوب مشاركته: {st.secrets['gcp_service_account']['client_email']}")

        # قسم الرفع
        u_file = st.file_uploader("اختر ملف للرفع:")
        if u_file and st.button("رفع الآن"):
            try:
                file_metadata = {'name': u_file.name, 'parents': [FOLDER_ID]}
                media = MediaIoBaseUpload(io.BytesIO(u_file.read()), mimetype=u_file.type)
                service.files().create(body=file_metadata, media_body=media).execute()
                st.balloons()
                st.success("تم الرفع بنجاح!")
            except Exception as e:
                st.error(f"حدث خطأ أثناء الرفع: {e}")

        # قسم البحث
        st.divider()
        search_q = st.text_input("بحث عن ملف:")
        if search_q:
            results = service.files().list(
                q=f"'{FOLDER_ID}' in parents and name contains '{search_q}'",
                fields="files(id, name, webViewLink)"
            ).execute()
            items = results.get('files', [])
            for item in items:
                st.write(f"📄 {item['name']}")
                st.link_button("فتح", item['webViewLink'])
