import streamlit as st
from st_google_drive_connection import GoogleDriveConnection

st.set_page_config(page_title="مخزن محطة الوزن", layout="centered")

# الربط السحابي (سيطلب منك تسجيل الدخول مرة واحدة فقط كمدير)
conn = st.connection("google_drive", type=GoogleDriveConnection)

if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    pwd = st.text_input("أدخل رمز الدخول:", type="password")
    if pwd == "123":
        st.session_state["auth"] = True
        st.rerun()
else:
    st.title("📤 إرسال ملفات الوزن إلى المخزن")
    
    # الموظف يختار الملف هنا
    uploaded_file = st.file_uploader("اختر ملف الـ PDF أو Word", accept_multiple_files=False)
    
    if uploaded_file:
        # بمجرد اختيار الملف، يظهر زر الحفظ المباشر
        if st.button(f"إرسال {uploaded_file.name} إلى حسابي"):
            with st.spinner("جاري الرفع السحابي..."):
                # الكود الذي يرسل الملف لمجلدك في درايف
                conn.upload_file(content=uploaded_file.getvalue(), file_name=uploaded_file.name)
                st.success("✅ تم الرفع! الملف الآن في حسابك الشخصي.")
