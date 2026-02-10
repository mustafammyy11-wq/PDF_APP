import streamlit as st
import os

# إعداد واجهة الموقع
st.set_page_config(page_title="أرشيف محطات الوزن", page_icon="🚛")

# نظام الدخول
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

def check_password():
    if st.session_state["pwd"] == "123":
        st.session_state["logged_in"] = True
    else:
        st.error("❌ الرمز غير صحيح")

if not st.session_state["logged_in"]:
    st.title("🔐 الدخول للنظام")
    st.text_input("أدخل رمز الدخول السري للمحطة", type="password", key="pwd", on_change=check_password)
else:
    st.title("📂 نظام أرشفة محطات الوزن المحورية")
    st.write("مرحباً بك! يمكنك الآن رفع ملفات PDF أو Word وسيتم حفظها في الأرشيف الدائم.")

    # خانة رفع الملفات
    uploaded_files = st.file_uploader("اختر الملفات لرفعها (PDF, Docx)", accept_multiple_files=True)
    
    if uploaded_files:
        for file in uploaded_files:
            st.success(f"✅ تم استلام الملف: {file.name}")
            st.info("جاري التجهيز للرفع إلى Google Drive...")
            # سيتم ربط حسابك في الخطوة القادمة عبر Settings

    # زر لمشاهدة الأرشيف
    if st.button("🔍 عرض الملفات المحفوظة"):
        st.warning("يتم الآن إعداد الاتصال بجوجل درايف...")

    if st.button("تسجيل الخروج"):
        st.session_state["logged_in"] = False
        st.rerun()
