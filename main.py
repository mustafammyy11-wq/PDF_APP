import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# 1. إعدادات المجلد (تأكد أن هذا الرقم هو المكتوب في رابط المجلد عندك)
FOLDER_ID = "1O9RsIkXihdZrGMaLrALM3dYDjm6x23nL"

def get_drive_service():
    """الربط مع جوجل درايف باستخدام Secrets"""
    try:
        if "gcp_service_account" not in st.secrets:
            st.error("خطأ: لم يتم العثور على بيانات 'gcp_service_account' في Secrets.")
            return None
        
        info = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(info)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        st.error(f"خطأ في الربط: {e}")
        return None

# إعدادات الصفحة
st.set_page_config(page_title="أرشيف محطة الوزن", layout="centered")

# نظام الدخول البسيط
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

password = st.sidebar.text_input("أدخل رمز الدخول:", type="password")
if password == "123":
    st.session_state["authenticated"] = True

if st.session_state["authenticated"]:
    st.title("🏛️ نظام أرشفة المحطة المطور")
    
    service = get_drive_service()
    
    if service:
