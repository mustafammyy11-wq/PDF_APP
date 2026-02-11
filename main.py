import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# هذا هو الرقم الدقيق لمجلدك بناءً على الرابط في صورتك
FOLDER_ID = "1O9RsIkXihdZrGMaLrALM3dYDjm6x23nL"

def get_drive_service():
    try:
        if "gcp_service_account" not in st.secrets:
            st.error("بيانات Secrets غير مكتملة")
            return None
        info = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(info)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        st.error(f"خطأ في الاتصال: {e}")
        return None

st.set_page_config(page_title="نظام أرشفة المحطة", layout="centered")

# تسجيل الدخول
if st.sidebar.text_input("رمز الدخول:", type="password") == "123":
    st.title("🏛️ الأرشيف المركزي")
    service = get_drive_service()
    
    if service:
        try:
            # اختبار الاتصال بالمجلد
            folder_info = service.files().get(fileId=FOLDER_ID, fields='name').execute()
            st.success(f"✅ تم الاتصال بنجاح بمجلد: {folder_info['name']}")
            
            tab1, tab2 = st.tabs(["📤 رفع وصل جديد", "🔍 البحث في الأرشيف"])
            
            with tab1:
                up_file = st.file_uploader("اختر صورة الوصل أو PDF:")
                if up_file and st.button("تأكيد الرفع الآن"):
                    with st.spinner("جاري الحفظ..."):
                        file_metadata = {'name': up_file.name, 'parents': [FOLDER_ID]}
                        media = MediaIoBaseUpload(io.BytesIO(up_file.read()), mimetype=up_file.type)
                        service.files().create(body=file_metadata, media_body=media).execute()
                        st.balloons()
                        st.success(f"✅ تم الرفع بنجاح!")

            with tab2:
                q = st.text_input("ابحث عن اسم الملف:")
                if q:
                    results = service.files().list(
                        q=f"'{FOLDER_ID}' in parents and name contains '{q}'",
                        fields="files(id, name, webViewLink)"
                    ).execute()
                    items = results.get('files', [])
                    if items:
                        for item in items:
                            col1, col2 = st.columns([3, 1])
                            col1.write(f"📄 {item['name']}")
                            col2.link_button("فتح الملف", item['webViewLink'])
                    else:
                        st.warning("لا توجد نتائج.")
        
        except Exception:
            st.error("⚠️ البرمجية لا ترى المجلد! تأكد من رقم المجلد والمشاركة.")
            st.info(f"الإيميل المطلوب: {st.secrets['gcp_service_account']['client_email']}")
else:
    st.info("أدخل الرمز 123")
