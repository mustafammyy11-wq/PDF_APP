import streamlit as st
import dropbox
import time

# الرمز الجديد الذي أرسلته لي في رسالتك الأخيرة
TOKEN = "sl.u.AGRMW3ytxebJSsw0BX96dy0VoF0Zmi3IZWyjxUXmulyYyfPpBbUKk3nUbJ3GeaAnaLI9o4fMvk-_PsmXcbbcbO-8ATGYuBnJjOUTjPih33q46vR38ZbJ_Ti-8YG_3-9sj48Q9bkhPdSNPA3_ikeYjtCsxDrzEOI5mLdlPPK6vB6dhum4s4n0-5NfJwoIEaSpxOxSwy1I402jtdOGzof5QGSpUhjBUDLoPSNHwkYSxfPVFAvDGWBMylN2U9RTakATU93phWKHKZJ2lkRl5BXQTENexW-h1eaujqwSkVwAdYPTOuQ0KDsxbiA7O-u6Aae8aet1NNP7xrix9Bt9D9aIIek84wT62BqIhcBwGFmjzp_BZHUh7qi4Y2HPuxQMtwXrzwNfWDEwyc6HTkL-kCJejtEkhtTlc5IOWMZtM3OyIHcSiWzTNxfcPHy7ZSkpJuwJj-loFjReX3hUSYDUfmzBoqWKQd-6J9Mem0zq6FAK4mV2IocwBU1wKetPZABhVt_h96rgLKDhV6tT3FvWWmfv6Bu70HsxR16sTtYgaogp6WhkVJgaXKBBBoHE8vHuyIyw1qdzI5EKO6_aDmJJr9aEtsQHWMuAMv7FYvmoRdtABjQJG17e3J9AGWZHEoXpEcjBLj6oky9zHKrNSWUFs43na6m66AgTYK7Uld4ClqMp6gXu_d5WKgtisWIOuEzEwcXdnCbOkyDVlCmttKcMeXse0eferVoZw6W8Ba2Liuvh4PKSEp7o6AcKqSVe6u3y70M-WdtYXqaYPdz1IF5KAeiJYbzUjBl15uzm2oNaXJ4V56x9sePd1OhGiSquGnPUecei4A1gZA76H5nhAUyx64YwyWoaW8105yD-E8-QsliDoK70PfFtwkzgcLk_F4l9PZ2tkoWrf8lWhojh7MWTNT_d3OtsYno8zLRR2sDKmZwgwj4s55m2bg3kTnjI5kQrKMfh3p0k8gQEMnmGLNxI4vX7OEC8RAohLuPMfTTmMI_DpU0UwQKX6ux4tVxzvta1EPeRtmLbvvUcdkpcnQ5JRSU03dsZrrBqnvu10Gbttf60xEGOkpWsRqYgaOpyWgJd0pvPaSIxKRqWRUKe4c_CR_l1AiU3q1CfrXxwm8mBDtOtwFZi9pkXkkmOTzeB9WKl52Pg6OkGUA7_1Pks4jNF1ZJ44pPHgoJiikMIZgtixXIaWAJ48foqwuL4kvg3lg9iRsoHJsZOvJNHM6UcS1lXXxQNhP97KZ1MGyfhMh_kkADFepJ8ry6nz91NOD70XOYpJAR8aBe0dwSL1EkoVacq-4O2sJmsOV5hBUvPtXo-TltVrRF9zBdON1rc83xaZ2QGZJPb-6nka0CkZ-N6nZewuE1IOJ6eWURnvYhrzz9hsDyREb2iHOzIpKco3oWEkg-R6wwGI243F4lCoB0AAvpLcpxTRvTXiFUe828UY2S9gnGHWYonouU3R_WpbEn6V3z4Y9aNGbw"

st.set_page_config(page_title="أرشيف مصطفى الجديد")
st.title("🏛️ نظام أرشفة مصطفى")

up = st.file_uploader("اختر ملف PDF للرفع:", type=["pdf"])

if up and st.button("🚀 رفع الملف"):
    try:
        # استخدام .strip() لإزالة أي مسافات زائدة من النسخ
        dbx = dropbox.Dropbox(TOKEN.strip())
        
        # تسمية الملف برقم الوقت لضمان النجاح التام وتفادي الأسماء العربية
        safe_name = f"/doc_{int(time.time())}.pdf"
        
        with st.spinner("جاري الرفع..."):
            dbx.files_upload(up.read(), safe_name, mode=dropbox.files.WriteMode.overwrite)
            
        st.success("✅ مبروك يا مصطفى! تم الرفع بنجاح.")
        st.balloons()
        
    except Exception as e:
        st.error(f"❌ حدث خطأ: {e}")
