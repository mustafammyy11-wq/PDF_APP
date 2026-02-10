import streamlit as st
import os
from PyPDF2 import PdfReader
from docx import Document

# --- إعدادات الصفحة العامة ---
st.set_page_config(page_title="مدير ملفات محطات الوزن المحورية", layout="wide")

# --- 1. نظام تسجيل الدخول ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def check_password():
    if st.session_state["pwd_input"] == "123":
        st.session_state["authenticated"] = True
        del st.session_state["pwd_input"] # حذف كلمة السر من الذاكرة للأمان
    else:
        st.error("❌ كلمة المرور غير صحيحة")

if not st.session_state["authenticated"]:
    st.title("🔐 الدخول للنظام")
    st.text_input("أدخل رمز الدخول السري:", type="password", key="pwd_input", on_change=check_password)
    st.info("ملاحظة: هذا النظام مخصص لموظفي محطات الوزن فقط.")
    st.stop() # إيقاف البرنامج هنا حتى يتم إدخال الرمز الصحيح

# --- 2. إعداد المجلدات بعد تسجيل الدخول ---
SAVE_DIR = "my_pdfs"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# --- 3. الواجهة الرئيسية (واجهة موحدة) ---
st.title("📂 مدير ملفات محطات الوزن المحورية")
st.markdown(f"**مرحباً بك في النظام المركزي** | [تسجيل الخروج](javascript:window.location.reload())")
st.divider()

# تقسيم الصفحة (الرفع على اليمين والبحث على اليسار)
col_upload, col_search = st.columns([1, 2.5])

with col_upload:
    st.subheader("📤 رفع ملفات جديدة")
    uploaded_files = st.file_uploader("اختر ملفات PDF أو Word", type=["pdf", "docx"], accept_multiple_files=True)
    if uploaded_files:
        for f_in in uploaded_files:
            with open(os.path.join(SAVE_DIR, f_in.name), "wb") as f:
                f.write(f_in.getbuffer())
        st.success(f"تم رفع {len(uploaded_files)} ملف بنجاح!")
        st.button("تحديث القائمة") # زر للتحديث اليدوي إذا لزم الأمر

with col_search:
    st.subheader("🔍 البحث والتحميل الفوري")
    search_query = st.text_input("ابحث عن اسم الملف، رقم المحطة، أو نص من الداخل...", placeholder="اكتب كلمة البحث هنا...")

    files = os.listdir(SAVE_DIR)
    
    if search_query:
        results = []
        with st.spinner('جاري فحص المستندات...'):
            for file_name in files:
                file_path = os.path.join(SAVE_DIR, file_name)
                match = False
                source_info = ""

                # أ. البحث في اسم الملف
                if search_query.lower() in file_name.lower():
                    match = True
                    source_info = "تطابق في الاسم"
                
                # ب. البحث داخل محتوى الملفات
                else:
                    if file_name.endswith(".pdf"):
                        try:
                            reader = PdfReader(file_path)
                            for page in reader.pages:
                                if search_query.lower() in page.extract_text().lower():
                                    match = True
                                    source_info = "وُجد داخل محتوى PDF"
                                    break
                        except: pass
                    elif file_name.endswith(".docx"):
                        try:
                            doc = Document(file_path)
                            full_text = "\n".join([p.text for p in doc.paragraphs])
                            if search_query.lower() in full_text.lower():
                                match = True
                                source_info = "وُجد داخل محتوى Word"
                        except: pass

                if match:
                    results.append((file_name, source_info))

        # عرض النتائج
        if results:
            st.write(f"✅ تم العثور على ({len(results)}) نتيجة:")
            for res_name, res_info in results:
                # تصميم بطاقة النتيجة
                with st.expander(f"📄 {res_name}", expanded=True):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.caption(f"المصدر: {res_info}")
                    with c2:
                        with open(os.path.join(SAVE_DIR, res_name), "rb") as file_bytes:
                            st.download_button(
                                label="📥 تحميل",
                                data=file_bytes,
                                file_name=res_name,
                                key=f"btn_{res_name}"
                            )
        else:
            st.warning("⚠️ لا توجد ملفات تطابق بحثك.")
    else:
        # عرض ترحيبي عند عدم البحث
        if not files:
            st.info("لا توجد ملفات مرفوعة حالياً. ابدأ برفع الملفات من القائمة الجانبية.")
        else:
            st.write(f"إجمالي الملفات المتوفرة في النظام: {len(files)} ملف.")
            st.caption("أدخل أي كلمة في خانة البحث أعلاه للعثور على ملفاتك وتحميلها.")