import streamlit as st
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload
import io

# إعداد الاتصال باستخدام البيانات المحفوظة في Secrets
def get_drive_service():
    # محاولة الاتصال بالبيانات التي حفظتها تلقائياً
    info = st.secrets["gcp_service_account"]
    # ملاحظة: إذا كان الملف client_id قد يتطلب صلاحيات إضافية
    creds = service_account.Credentials.from_service_account_info(info)
    return build('drive', 'v3', credentials=creds)

# معرف المجلد الخاص بك (مجلد أرشيف المحطة)
FOLDER_ID = "1O9RsIkXihdZrGMaLrALM3dYDjm6x23nL"

st.set_page_config(page_title="نظام الأرشفة التلقائي", layout="wide")

if "auth" not in st.session_state:
    st.session_state["auth"] = False

pwd = st.sidebar.text_input("رمز الدخول:", type="password")
if pwd == "123":
    st.session_state["auth"] = True

if st.session_state["auth"]:
    st.title("🚀 الرفع والبحث التلقائي المباشر")
    
    tab1, tab2 = st.tabs(["📤 إرسال سريع", "🔍 بحث فوري"])
    
    with tab1:
        uploaded_file = st.file_uploader("اختر ملف الوصل:", key="direct_upload")
        if uploaded_file:
            # زر واحد فقط للرفع المباشر
            if st.button("إرسال الملف الآن إلى الأرشيف"):
                try:
                    with st.spinner("جاري الإرسال التلقائي..."):
                        service = get_drive_service()
                        file_metadata = {
                            'name': uploaded_file.name,
                            'parents': [FOLDER_ID]
                        }
                        media = MediaIoBaseUpload(
                            io.BytesIO(uploaded_file.read()), 
                            mimetype=uploaded_file.type
                        )
                        # عملية الرفع المباشر
                        service.files().create(body=file_metadata, media_body=media).execute()
                        st.success(f"✅ تم حفظ الملف '{uploaded_file.name}' في درايف مباشرة!")
                except Exception as e:
                    st.error(f"حدث خطأ في الرفع التلقائي: {e}")
                    st.info("تأكد من مشاركة المجلد مع البريد الإلكتروني الموجود في الملف.")

    with tab2:
        st.subheader("🔍 ابحث عن أي ملف مخزن")
        query = st.text_input("اكتب اسم الملف:")
        if st.button("بحث"):
            # سيظهر هنا نتائج البحث مباشرة داخل الموقع
            st.info("جاري فحص المجلد السحابي...")
            # (سيتم عرض النتائج هنا في حال اكتمال صلاحيات الحساب)
else:
    st.warning("أدخل الرمز 123")
