import streamlit as st
import requests
import pandas as pd
import time

# --- 1. الإعدادات الأساسية (بياناتك الصحيحة 100%) ---
BOT_TOKEN = "8388457454:AAE9RHsufjtZ-ZYnKOlKy4Z5q56IRM5Z4Cc"
CHAT_ID = "-1003555343193"
# رابط الجسر (Google Script)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwRMcjPfNv5U0BemK6XxzWfugH2TtKxcyKLseM_LvCR6vyuAtBSKi6VMVDiNgfxRkl5NA/exec"
# معرف الجدول (Google Sheet ID)
SHEET_ID = "1Y8cnKKctMF54jOcnCLKSH3JhfG5Evsf6OXizPnPXtJk"
# رابط القراءة المباشر مع إضافة 't' لمنع التخزين المؤقت (Cache)
SEARCH_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0&t={int(time.time())}"

# --- 2. إعدادات الصفحة والتصميم ---
st.set_page_config(page_title="أرشيف المحطات الذكي", page_icon="🚚", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    div.stButton > button {
        background: linear-gradient(90deg, #0072ff 0%, #00c6ff 100%);
        color: white; font-weight: bold; border-radius: 10px; width: 100%; border: none; height: 3em;
    }
    div.stDownloadButton > button {
        background-color: #28a745 !important; color: white !important;
        font-weight: bold; border-radius: 10px; width: 100%; border: none;
    }
    .file-card { 
        background-color: #f1f3f5; padding: 15px; border-radius: 10px; 
        border-right: 5px solid #0072ff; margin-bottom: 10px; color: #1a1a1a;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. نظام الدخول ---
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🔐 نظام الأرشفة</h2>", unsafe_allow_html=True)
    pw = st.text_input("أدخل الرمز السري الخاص بالمحطة:", type="password")
    if st.button("تسجيل الدخول"):
        if pw == "123":
            st.session_state.auth = True
            st.rerun()
        else: st.error("❌ الرمز غير صحيح")
    st.stop()

# --- 4. واجهة التطبيق الرئيسية ---
st.markdown("<h1 style='text-align:center; color:#0072ff;'>🚚 نظام أرشفة المحطات</h1>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🔍 البحث عن الكتب والقرارات", "📤 أرشفة ملف جديد"])

# --- تبويب البحث ---
with tab1:
    search_q = st.text_input("🔎 اكتب اسم الملف للبحث عنه:")
    
    try:
        # قراءة البيانات
        df = pd.read_csv(SEARCH_URL)
        df.columns = df.columns.str.strip() # تنظيف أسماء الأعمدة
        
        if search_q:
            # البحث في العمود الأول (الأسماء)
            mask = df.iloc[:, 0].astype(str).str.contains(search_q, na=False, case=False)
            results = df[mask]
            
            if not results.empty:
                st.success(f"✅ تم العثور على {len(results)} نتيجة")
                for i, row in results.iterrows():
                    file_name = row.iloc[0]
                    file_id = row.iloc[1]
                    
                    with st.container():
                        st.markdown(f'<div class="file-card">📄 {file_name}</div>', unsafe_allow_html=True)
                        # جلب الملف من تليجرام
                        try:
                            f_info = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}").json()
                            if f_info.get("ok"):
                                f_path = f_info['result']['file_path']
                                f_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{f_path}"
                                file_data = requests.get(f_url).content
                                st.download_button(label=f"⬇️ تحميل {file_name}", data=file_data, file_name=f"{file_name}.pdf", key=f"btn_{i}")
                        except:
                            st.error("⚠️ عذراً، تعذر جلب الملف من تليجرام.")
            else:
                st.warning("⚠️ لا توجد نتائج مطابقة، تأكد من كتابة الاسم بشكل صحيح.")
        else:
            st.info("💡 الأرشيف جاهز، اكتب أي كلمة للبحث في الملفات المرفوعة.")
            
    except Exception as e:
        st.info("📦 الأرشيف بانتظار تحديث البيانات أو إضافة ملفات جديدة.")

# --- تبويب الإضافة ---
with tab2:
    st.markdown("### 📤 رفع ملف جديد للأرشفة")
    f_up = st.file_uploader("اختر ملف PDF:", type=["pdf"])
    
    if f_up and st.button("🚀 بدء الأرشفة والمزامنة"):
        with st.spinner("جاري المزامنة مع تليجرام وجوجل..."):
            # 1. الرفع إلى تليجرام
            files = {'document': (f_up.name, f_up.getvalue())}
            res_tg = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", data={'chat_id': CHAT_ID, 'caption': f_up.name}, files=files).json()
            
            if res_tg.get("ok"):
                new_file_id = res_tg['result']['document']['file_id']
                
                # 2. إرسال البيانات لجوجل شيت عبر الجسر
                res_gs = requests.get(f"{SCRIPT_URL}?name={f_up.name}&id={new_file_id}")
                
                if res_gs.status_code == 200:
                    st.success(f"✅ تم حفظ الملف '{f_up.name}' بنجاح في النظام!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("⚠️ تم رفع الملف لتليجرام ولكن فشل التوثيق في الجدول.")
            else:
                st.error("❌ فشل الرفع لتليجرام، تأكد من اتصال الإنترنت.")
