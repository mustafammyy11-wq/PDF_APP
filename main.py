import streamlit as st
import dropbox
import time

# الرمز الجديد الذي أرسلته (تم تنظيفه تلقائياً)
TOKEN = "Sl.u.AGSzRDbnUvdUAxw49UmcasJ4qQDR0D86awmmBIlUx3bUn_Q-484mQXP-PaB6d3fwK0NeF_SvJk4gYU3fC-gTJ9uEz0Bs8BCqH4D7K4MUoHH2d96dTWzIXyefsvulmSjZjNHp_OipPuCeC2I4uDDspCE8tBO2yK6plyplyZBSBAe-QHs73Gnbety7AiRkRkcytDVihNcZ8xa2ClLhciclgTcVZml9V5AzLxD1vqDzBoB3B4PnPsSOPbcFxFFS0WteMRzU4_d8C2lbwtEZKjif5aCKlMV1k-SuecklEw9YTLohhU6WWbAL52QGxM7CfzBe3AzwCnMlH8cC7Wgb-QukVwk0s2TEkxg64XnXCT0bx8ZfpaTNmpi2O7tR-imXd7-iRWR3zJPKEOc1A6vgSTVMjxx-LSXc_3KQcK9jCTdIBdbtmUxWdPYbFcFrm2Kcfze-iUDjHlllM7d0RYVn6SABQPHe18tXkUV0FpPhReD4FrhwGY0uPU3lp9FYFf-6QLlPNJUdpgaozQkBQoBq-7NPwpR6nWqsMVLAAUXPeSqWM_gIWIeNwJuZRICpU_g1XGZud81nzoXJl_xsqhuXNzGO13m6ueL7A6_hJtTQOYNF6azloEV-epPGCeEQV7HiBjEL2LlWTI4V4HyxrcPs9n5_tL_PRoxl45tEZJfogx9a5_6SgAmje35sBrxyhzFTGyYS75bLsP6fp4d-E8Q-cL6d0dOmVRsFBkx9_5my3Y55O81Z3LXlGfsVr-NWyKnouOqKTT7jbol0H14RJb-P6wY5a_JnJ_RrV1AvI_kft89mPZ8zQfL63EFyms6Hyfmrl4XQE0Zd-QhLubzGq4UqCU7lBwB1XYKQfyMFCJyUY138w7T6atPc7dLrcoyiC7x7x84IgS5lNyg4HaPY2h_Fz7wT6BUOqMER74rBSvacyU9BJ0eK9MC71lAdGyw6gJBqlYwd75-8K3rG-ReISEsCxGB_Zkfj_RhWIPdpdpqbUiJtigCucLoAPJa4y3YuG_T0Xm0ImHtFnhi_FLZGP26JDIbGIjFc2pf1Uw3cobCnZ4XXZmXwjO79jfZxIY2HBaiqFsrlltuz5tLiA_TehehJTlc6xnQLCHnYbjtFkc16Cr77Q4K5kDrP_TxuR1Kgn8CPPAEaBZ-ZR6CgjiggQ-I0GmDNv02tiJnWZrUGp2LxuF_i9PdTl7rmBSJCayABQYTZZN7arcBMk1CWwzjluqLj96RDfuAR6y1mNUXGcoDS0lXvbCWII0HOXbQegS5aroSGAh5bE0guAAKcWd-BltPfl62vVn09NZp4KlumkvxBETs8qx8JNYPQkz79zroMVW3SIbyzTB63TLpClZA-tkvYcBFPYrGLC0LQwjHBn9oJ031SJcw7VdsUfl0RlLdhBti42QNHdGRn6Y7RlY1Fs6WI7CuMINeGjjfNAAPYh0QLMpgFQbcWwEhTblGd9AXrrFfqFY6QXgQ"

st.set_page_config(page_title="أرشيف مصطفى")
st.title("🏛️ نظام أرشفة مصطفى (Dropbox)")

up = st.file_uploader("اختر ملف PDF للرفع:", type=["pdf"])

if up and st.button("🚀 بدء الرفع"):
    try:
        dbx = dropbox.Dropbox(TOKEN)
        
        # استخدام الوقت الحالي كاسم للملف لضمان عدم تكرار الأسماء وتجنب مشاكل اللغة
        file_name = f"/doc_{int(time.time())}.pdf"
        
        with st.spinner("جاري التواصل مع Dropbox..."):
            dbx.files_upload(up.read(), file_name, mode=dropbox.files.WriteMode.overwrite)
            
        st.success("✅ مبروك يا مصطفى! تم الرفع بنجاح تام.")
        st.balloons()
        
    except Exception as e:
        if "expired" in str(e).lower():
            st.error("❌ انتهت صلاحية الرمز، يرجى توليد واحد جديد من Dropbox.")
        elif "scope" in str(e).lower():
            st.error("❌ لم يتم حفظ الصلاحيات! تأكد من ضغط زر Submit في Dropbox.")
        else:
            st.error(f"❌ حدث خطأ: {e}")
