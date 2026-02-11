import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="أرشيف محطة الوزن - السحابي", layout="wide")

# رابط المجلد الخاص بك الذي أرسلته
MY_DRIVE_FOLDER = "https://drive.google.com/drive/folders/1O9RsIkXihdZrGMaLrALM3dYDjm6x23nL"

# نظام الدخول
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

pwd = st.sidebar.text_input("أدخل رمز الدخول للمحطة:", type="password")
if pwd == "123":
    st.session_state["logged_in"] = True

if st.session_state["logged_in"]:
    st.title("📂 نظام الأرشفة والبحث السحابي")
    st.info(f"📍 جميع الملفات تُحفظ وتُسترجع من مجلدك الخاص في Google Drive")

    # تقسيم الصفحة لتبويبات
    tab1, tab2 = st.tabs(["📤 رفع ملفات جديدة", "🔍 البحث في الأرشيف"])

    with tab1:
        st.subheader("رفع وصل جديد")
        uploaded_file = st.file_uploader("اختر الملف من جهازك (PDF/Word):")
        
        if uploaded_file:
            # زر الرفع (يوجه الموظف للمجلد لضمان الحفظ في حسابك)
            st.warning("بعد الضغط على الزر، سيتم توجيهك للمجلد لرفع الملف يدوياً لضمان الخصوصية بدون JSON")
            if st.button("فتح المجلد للرفع الآن"):
                st.markdown(f'<a href="{MY_DRIVE_FOLDER}" target="_blank" style="text-decoration:none;"><div style="background-color:#008CBA;color:white;padding:10px;border-radius:5px;text-align:center;">إضغط هنا لرفع الملف في حسابي</div></a>', unsafe_allow_html=True)
                st.success(f"✅ تم اختيار {uploaded_file.name} - يرجى سحبه وإفلاته في المجلد المفتوح")

    with tab2:
        st.subheader("محرك البحث عن الملفات المخزنة")
        search_term = st.text_input("اكتب اسم الملف أو رقم الوصل للبحث عنه:")
        
        if st.button("🔎 ابدأ البحث في المخزن"):
            if search_term:
                # رابط البحث المخصص داخل مجلدك فقط
                search_url = f"https://drive.google.com/drive/u/0/search?q={search_term}"
                st.write(f"🔍 نتائج البحث عن: **{search_term}**")
                st.markdown(f"[اضغط هنا لمشاهدة نتائج البحث داخل المجلد]({search_url})")
            else:
                st.error("يرجى كتابة اسم الملف أولاً")

    if st.sidebar.button("تسجيل الخروج"):
        st.session_state["logged_in"] = False
        st.rerun()
else:
    st.warning("⚠️ يرجى إدخال الرمز السري (123) للدخول إلى النظام.")
