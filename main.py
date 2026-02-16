import streamlit as st
import dropbox

# الرمز الذي أرسلته لي سابقاً
TOKEN = "Sl.u.AGS7ch6JDFieqji8u_ZrQq4TnoBGOnZVH_MRBo1LeM6qtUjv2SoSvN-3V9FtqXVhXH50n60jS6JzyQ3CbcGSCbSx8LI8bUvVQBOh6jFxL-uklsonRFFL4mLVxCdDWHsGQwZka1v5mLuIbOhQ5l3XijapivyHpUmeDmTvqETQmG-SGw1B7YNDpisM6eaMu2dKqaCWLQyYMudojgd7ewjM2jC4InKGvtxV79JnWm-1VbqhxsPL5SL_CdXtsFDo6ETYBOYPb6H57NZgCiofAwiFnSER3ePsW7vs1klE3pwx4jnIUFXWB2ek8kCYE84aU3SWKOW9kP7AcfaVi5JtksR_T_d3v7VN3_1wD6IyBbq9RTI54P-lnZ4kBMaqYCcEdd5vG81XwliLHdyL_qz54zKWHmlex53hyNjy9Rw2JF2RX7CkVdRc81dM2l3F4NJGsF8sDqDHJwYlaVH8kL_-waftSQRFQrSx4DOC_svHVEnyQbFDYBD1u_FaZBA3np6Ajce2friWZxFN7TtiBd5ebzMB8vkSQq0-MKPPixCo8_scDMdKMZ0uxnldR2J7urTm_U9ZsoYO5G9-WhoCVOTaRX705VTQBmweFygnh2quwp1VlgjL1I9gFTVxOtQ67R4onsiUZmBEh9J49I9b-X5LfAQhtxVkns7IhJzDTKUVieaLO-l3H0Rj2qLrVrutOhGMIQZBqtVHEcPuQv6-rLmrckNcNeIPSZu2XuAEKARC3qe2cEj4oCwSWwL933polI0VwdG4tJKRJqMDjfLgXsFRo0pUvJc6AJKhFLj5GYYQyVatr6Zd03JnRJCMWFWrOKo-3XS2KEmEqktwP_a6RWXx8pzAvorXwcz0gl_3L5KqHSIV39G3wmmECvHXC1QtrvSbqSk2SLrMOCECzlErT4QRfLt5LcP7fX89isTuxdGVWX_C0zBHUAaP0N2nvIfxkd2Ts9bc4qHtY_2-g3blT8qn78A_w8h_z6B0kTYS_DqSe9K5gqBZm97s-i5ZRryp6V-SuS6xlu0CyiqEhgnshZWasJoYj94yl9_R5Cs0VYiWXdMMwl-ra8pN5Xoze4M3j63T0s-CL80q82mJYx2jftitsF1cHZH8oVJxj6Fox2tl9D3-NT2Ig_mFWJQ-BXrUSKmAx_D-wXFjxHeYOPfQ8zMTS63tzDqet5CeEIuDiqB-7wpFOeFHonpLK0lwYNAlSHZRzdd6hLA2AqLKKRqQDsYUGE5eclcvJfZp2CLTyTwTFjtZxFdMSay97hDLFGiLU1K-xkjb_5zLtYjG7W_fVYAOv0dRpBCJ1el7C0aei_od-Eb33yZHYRptIcby-uD8KKkCBWmM9-AIRrZHGuTgBMkvkm-6NqSR87-SgCYA5KPeVWOPIfvx5Tvw09hiz5VKDF4olr-26S6jlE-uGckcEh0jGRjndH1tBCsm4BrN79XrQicCTLcpHLhEPs_tSMD0GYDS487eT9A"

st.title("🏛️ نظام أرشفة مصطفى")

up = st.file_uploader("اختر ملف PDF:", type=["pdf"])

if up and st.button("🚀 رفع الآن"):
    try:
        dbx = dropbox.Dropbox(TOKEN)
        # تسمية الملف باسم إنجليزي ثابت لتفادي خطأ الصورة 3fe9af11
        short_name = "/archive_file.pdf" 
        
        with st.spinner("جاري الرفع..."):
            dbx.files_upload(up.read(), short_name, mode=dropbox.files.WriteMode.overwrite)
            st.success("✅ أخيراً! تمت العملية بنجاح.")
            st.balloons()
    except Exception as e:
        st.error(f"❌ الخطأ هو: {e}")
