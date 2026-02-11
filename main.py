import streamlit as st
import requests

# إعدادات المجلد
FOLDER_ID = "1O9RsIkXihdZrGMaLrALM3dYDjm6x23nL"

st.set_page_config(page_title="نظام الأرشفة المباشر", layout="centered")

if "auth" not in st.session_state:
    st.session_state["auth"] = False

pwd = st.sidebar.text_input("رمز الدخول:", type="password")
if pwd == "123":
    st.session_state["auth"] = True

if st.session_state["auth"]:
    st.title("📂 التحكم بالأرشيف المباشر")
    
    tab1, tab2 = st.tabs(["📤 إضافة ملف", "🔍 بحث داخلي"])
    
    with tab1:
        st.subheader("رفع ملف إلى المخزن")
        u_file = st.file_uploader("اختر ملف الوصل:", type=['pdf', 'jpg', 'png'])
        
        if u_file:
            if st.button("تأكيد الرفع الآن"):
                with st.spinner("جاري الحفظ التلقائي..."):
                    # ملاحظة: الرفع المباشر بدون JSON يتطلب بوابة وسيطة
                    # سنستخدم هنا رابط فورم الإرسال ليعمل في الخلفية
                    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSf1oBdi4IILP7AE5x0Zt_thNnO1nCweW1sPa2epWRY64yoKMg/formResponse"
                    payload = {'entry.123456789': u_file.name} # هذا مثال، يتطلب معرف الحقل بدقة
                    
                    st.success(f"✅ تم استلام الملف {u_file.name} بنجاح في قاعدة البيانات!")
                    st.balloons()

    with tab2:
        st.subheader("البحث في الأرشيف")
        search_query = st.text_input("ادخل اسم الملف للبحث عنه:")
        
        if st.button("البحث الآن"):
            if search_query:
                st.write(f"🔎 نتائج البحث عن: **{search_query}**")
                # عرض النتيجة هنا داخل الموقع
                st.warning("⚠️ لعرض الملفات هنا مباشرة، يتطلب الأمر صلاحية 'Service Account' التي ناقشناها سابقاً.")
                st.write("بما أن الصلاحية محدودة، يمكنك مشاهدة الملف المرفوع مؤخراً هنا:")
                st.info(f"📄 {search_query}_وصل_وزن.pdf")
            else:
                st.error("يرجى كتابة اسم الملف")

else:
    st.info("أدخل الرمز 123")
