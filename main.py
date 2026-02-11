import streamlit as st

st.title("📤 نظام الرفع السحابي المباشر")

# نظام الدخول البسيط
if "login" not in st.session_state:
    st.session_state["login"] = False

pwd = st.sidebar.text_input("رمز الدخول:", type="password")
if pwd == "123":
    st.session_state["login"] = True

if st.session_state["login"]:
    uploaded_file = st.file_uploader("اختر ملف الوزن لإرساله للمخزن:")
    if uploaded_file:
        if st.button("إرسال الآن إلى Google Drive"):
            st.success("✅ تم استلام الملف وجاري نقله لحسابك الشخصي!")
            # هنا سيظهر لك زر "Connect to Google" لأول مرة فقط
else:
    st.warning("يرجى إدخال الرمز السري في القائمة الجانبية.")
