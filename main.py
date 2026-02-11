import streamlit as st

# روابطك الخاصة
UPLOAD_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSf1oBdi4IILP7AE5x0Zt_thNnO1nCweW1sPa2epWRY64yoKMg/viewform"
DRIVE_FOLDER = "https://drive.google.com/drive/folders/1O9RsIkXihdZrGMaLrALM3dYDjm6x23nL"

st.set_page_config(page_title="أرشيف محطة الوزن", layout="centered")

if "auth" not in st.session_state:
    st.session_state["auth"] = False

pwd = st.sidebar.text_input("رمز الدخول:", type="password")
if pwd == "123":
    st.session_state["auth"] = True

if st.session_state["auth"]:
    st.title("📠 نظام الرفع المباشر للأرشيف")
    
    # واجهة الرفع التي يحبها الموظف
    st.subheader("📤 تحميل ملف جديد")
    uploaded_file = st.file_uploader("اسحب الملف هنا أو اضغط للاختيار:", type=['pdf', 'jpg', 'png', 'docx'])
    
    if uploaded_file:
        st.success(f"✅ تم تجهيز الملف: {uploaded_file.name}")
        st.info("الآن، اضغط على الزر أدناه لإتمام عملية التخزين بضغطة واحدة:")
        
        # زر الربط المباشر
        st.link_button("🚀 إرسال الآن للمخزن السحابي", UPLOAD_LINK)

    st.divider()

    # واجهة البحث
    st.subheader("🔍 البحث عن ملف قديم")
    search_q = st.text_input("اكتب اسم الملف:")
    if st.button("🔎 ابدأ البحث"):
        # يفتح صفحة نتائج البحث في مجلدك مباشرة
        res_url = f"https://drive.google.com/drive/u/0/search?q={search_q}"
        st.markdown(f"[إضغط هنا لعرض نتائج البحث عن {search_q}]({res_url})")

else:
    st.warning("يرجى إدخال الرمز 123")
