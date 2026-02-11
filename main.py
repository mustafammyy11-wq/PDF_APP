import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# تعريف المجلد
FOLDER_ID = "1O9RsIkXihdZrGMaLrALM3dYDjm6x23nL"

def get_drive_service():
    # جلب البيانات من سيكرتس
    info = st.secrets["gcp_service_account"]
    creds = service_account.Credentials.from_service_account_info(info)
    return build('drive', 'v3', credentials=creds)

st.set_page_config(page_title="أرشيف محطة الوزن المطور", layout="centered")

if "auth" not in st.session_state:
    st.session_state["auth"] = False

pwd = st.sidebar.text_input("رمز الدخول:", type="password")
if pwd == "123":
    st.session_state["auth"] = True

if st.session_state["auth"]:
    st.title("🏛️ الأرشيف الذكي - رفع وبحث فوري")
    
    service = get_drive_service()
    
    tab1, tab2 = st.tabs(["📤 إضافة ملف جديد", "🔍 بحث داخلي"])
    
    with tab1:
        st.subheader("إرسال الوصل إلى الدرايف")
        up_file = st.file_uploader("اختر الملف:", type=['pdf', 'jpg', 'png'])
        if up_file:
            if st.button("تأكيد الرفع الآن"):
                with st.spinner("جاري الإرسال صمتاً..."):
                    try:
                        file_metadata = {'name': up_file.name, 'parents': [FOLDER_ID]}
                        media = MediaIoBaseUpload(io.BytesIO(up_file.read()), mimetype=up_file.type)
                        service.files().create(body=file_metadata, media_body=media).execute()
                        st.success(f"✅ تم الحفظ بنجاح: {up_file.name}")
                    except Exception as e:
                        st.error(f"خطأ: تأكد من مشاركة المجلد مع ايميل الحساب الجديد.")

    with tab2:
        st.subheader("محرك البحث الداخلي")
        q = st.text_input("اكتب اسم الملف:")
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
                    col2.link_button("استعراض", item['webViewLink'])
            else:
                st.warning("لم يتم العثور على ملفات.")
else:
    st.info("الرجاء إدخال الرمز 123")
