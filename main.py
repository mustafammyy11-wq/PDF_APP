import streamlit as st

# الرابط الخاص بك الذي أرسلته
UPLOAD_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSf1oBdi4IILP7AE5x0Zt_thNnO1nCweW1sPa2epWRY64yoKMg/viewform?usp=sf_link"

# رابط مجلد الأرشيف (الذي أرسلته لي سابقاً) لمشاهدة الملفات
DRIVE_FOLDER_URL = "https://drive.google.com/drive/folders/1O9RsIkXihdZrGMaLrALM3dYDjm6x23nL"

st.set_page_config(page_title="أرشيف محطة الوزن", layout="centered")

# نظام الدخول البسيط
if "auth" not in st.session_state:
    st.session_state["auth"] = False

pwd = st.sidebar.text_input("رمز الدخول (الرمز السري):", type="password")
if pwd == "123":
    st.session_state["auth"] = True

if st.session_state["auth"]:
    st.title("📠 نظام أرشفة محطة الوزن المركزي")
    st.write("مرحباً بك! يمكنك الآن رفع الوصلات الجديدة أو البحث في الأرشيف.")
    
    tab1, tab2 = st.tabs(["📤 إرسال وصل جديد", "🔍 البحث في الأرشيف"])
    
    with tab1:
        st.subheader("إرسال سريع")
        st.info("عند الضغط على الزر أدناه، ستفتح لك صفحة لرفع الملف. بعد اختيار الملف، اضغط على 'Submit' أو 'إرسال'.")
        # زر يفتح نموذج جوجل الذي أنشأته
        st.link_button("🚀 ارفع الملف الآن للمخزن", UPLOAD_FORM_URL)
        
    with tab2:
        st.subheader("البحث عن الملفات المخزنة")
        q = st.text_input("اكتب اسم الملف أو تاريخه للبحث عنه:")
        if st.button("🔎 ابدأ البحث"):
            # هذا الزر يفتح البحث داخل جوجل درايف مباشرة
            search_url = f"https://drive.google.com/drive/u/0/search?q={q}"
            st.markdown(f"🔍 [اضغط هنا لرؤية نتائج البحث عن: {q}]({search_url})")
            
        st.divider()
        st.write("أو يمكنك تصفح المجلد بالكامل من هنا:")
        st.link_button("📂 فتح مجلد الأرشيف بالكامل", DRIVE_FOLDER_URL)
else:
    st.warning("⚠️ يرجى إدخال الرمز السري (123) للدخول إلى النظام.")

# تنبيه هام لمصطفى
st.sidebar.divider()
st.sidebar.caption("ملاحظة: تأكد من مسح أي بيانات قديمة في خانة Secrets لتجنب الأخطاء.")
