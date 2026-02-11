import streamlit as st
import webbrowser

# رابط المجلد ونموذج الرفع الخاص بك
UPLOAD_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSf1oBdi4IILP7AE5x0Zt_thNnO1nCweW1sPa2epWRY64yoKMg/viewform"
DRIVE_FOLDER_ID = "1O9RsIkXihdZrGMaLrALM3dYDjm6x23nL"

st.set_page_config(page_title="أرشيف محطة الوزن", layout="centered")

if "auth" not in st.session_state:
    st.session_state["auth"] = False

pwd = st.sidebar.text_input("رمز الدخول:", type="password")
if pwd == "123":
    st.session_state["auth"] = True

if st.session_state["auth"]:
    st.title("📠 نظام الأرشفة الذكي")

    # 1. الرفع الفوري (بمجرد اختيار الملف يفتح صفحة الرفع)
    st.subheader("📤 رفع مباشر وسريع")
    uploaded_file = st.file_uploader("اختر ملف الوصل الآن للإرسال الفوري:", type=['pdf', 'jpg', 'png'])
    
    if uploaded_file:
        st.success(f"جاري تحويلك لإتمام حفظ {uploaded_file.name}...")
        # استخدام رابط مباشر يفتح فوراً
        st.markdown(f'<meta http-equiv="refresh" content="0;url={UPLOAD_LINK}">', unsafe_allow_html=True)
        st.link_button("إضغط هنا إذا لم يتم تحويلك تلقائياً", UPLOAD_LINK)

    st.divider()

    # 2. إصلاح زر البحث (تفعيل البحث المباشر في المجلد)
    st.subheader("🔍 البحث في الأرشيف")
    search_q = st.text_input("اكتب اسم الملف أو الرقم للبحث:")
    
    if st.button("🔎 ابدأ البحث"):
        if search_q:
            # رابط البحث المباشر داخل المجلد المحدد
            search_url = f"https://drive.google.com/drive/u/0/search?q=parent:{DRIVE_FOLDER_ID}%20{search_q}"
            st.info(f"يتم الآن البحث عن: {search_q}")
            st.markdown(f'<a href="{search_url}" target="_blank">إضغط هنا لمشاهدة نتائج البحث في نافذة جديدة</a>', unsafe_allow_html=True)
        else:
            st.warning("يرجى كتابة اسم الملف أولاً.")

else:
    st.warning("أدخل الرمز 123")
