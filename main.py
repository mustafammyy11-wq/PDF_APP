import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# تأكد من هذا الرقم بدقة (انسخه من رابط المجلد في المتصفح)
FOLDER_ID = "1O9RsIkXihdZrGMaLrALM3dYDjm6x23nL"

def get_drive_service():
    try:
        # التأكد من وجود البيانات في Secrets
        if "gcp_service_account" not in st.secrets:
            st.error("❌ بيانات Secrets غير موجودة! تأكد من وضع الجيسون في إعدادات Streamlit.")
            return None
        info = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(info)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        st.error(f"❌ خطأ في الاتصال: {e}")
        return None

st.set_page_config(page_title="نظام أرشفة المحطة", layout="centered")

# تسجيل الدخول
pwd = st.sidebar.text_input("رمز الدخول:", type="password")
if pwd == "123":
    st.title("🏛️ الأرشيف المركزي")
    service = get_drive_service()
    
    if service:
        # اختبار هل البرمجية ترى المجلد فعلاً؟
        try:
            folder_check = service.files().get(fileId=FOLDER_ID, fields='name, id').execute()
            st.success(f"✅ متصل بنجاح بمجلد: {folder_check['name']}")
            
            tab1, tab2 = st.tabs(["📤 الرفع المباشر", "🔍 البحث الذكي"])
            
            with tab1:
                up_file = st.file_uploader("اختر ملف الوصل:")
                if up_file and st.button("تأكيد الرفع الآن"):
                    with st.spinner("جاري الإرسال..."):
                        try:
                            file_metadata = {'name': up_file.name, 'parents': [FOLDER_ID]}
                            media = MediaIoBaseUpload(io.BytesIO(up_file.read()), mimetype=up_file.type)
                            service.files().create(body=file_metadata, media_body=media).execute()
                            st.balloons()
                            st.success("✅ تم الرفع بنجاح!")
                        except Exception as upload_error:
                            st.error(f"❌ فشل الرفع الفعلي: {upload_error}")

            with tab2:
                q = st.text_input("ابحث عن الملف بالاسم:")
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
                            col2.link_button("فتح", item['webViewLink'])
                    else:
                        st.warning("لم يتم العثور على ملفات.")
        
        except Exception as folder_error:
            st.error("⚠️ البرمجية لا ترى المجلد! يرجى التأكد من الخطوتين أدناه:")
            st.info(f"1. هل رقم المجلد {FOLDER_ID} صحيح؟\n2. هل شاركت المجلد مع هذا الإيميل: {st.secrets['gcp_service_account']['client_email']}")

else:
    st.info("الرجاء إدخال الرمز 123 في القائمة الجانبية.")
