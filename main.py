import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# معلومات حسابك
MAIL = "mustafairaq@project-e4fb2fde-9291-482a-b14.iam.gserviceaccount.com"
PK = r"""-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDcufrbwTEdJ81n
xso1o/FzJ8XD7o83BVg4Y9qJ3gCkXpnXWkyFtqSHdcBDlGt370RRxDpuQxdrhKcN
psEUKPm8woTRq0u67OZnDlJHR7w2eFeris562xfDHCgGH8yhX+P39w5p8hMUyBmp
6pZoyAE4zVGHTqvKmMLgJGp4S6NpQusui68IfV+umcf+QifwaglCfWIuOjjBm/9G
W5lqOElJSaNwrQoJZMrZqSYxCELQ3LAI+xwBZnMBm7Aisqs7G/zRM3J610zDXX0X
UQc3Y/HFK+3jGbuZsIpwBI+VnmII5D+YEseN1ADzyjr6bVIN6hvWIxSVb6x3vZ14
mDoAKTttAgMBAAECggEAJo9S9LsOUnKWnq+Kuc43Kw/iq7TsTgdf/xHqprUi1ZQ1
OfrrbVyX55Y5jVTLZXtmKwal0odj+wOEj4z3JAd4gXJV868CHtit84j79Lnidn2V
i0FHiwzlXM95aoB5piNzVulRGk8Q6EuAuD9kIU/3bq3ntUSYHF+Ng8y40OUd2hBk
hWsKOFHCMqLk0Dzx2R2LfgpdOwEiEKCC4Qwp/sSOWROeQ75jXkxMMI0eMplsfFmA
Nag52aSw41ZAHFGEs/336Yydl+4SArsJd/p9pQ7Yg8FTJo+v3rvEHKSjOqMSnXXC
EQ6MQm0eYyF//xW3QUMJ6uwiB9nVw1o08zy/+sPM4QKBgQD7+UemBYX0tHXkfbAk
O316+seEk+vpWqzz8TYHAE941ciaMQe4/Rs13lzWd2TvyIR+VBq3bTUYSvNjc+4B
aVs8iaB51L4Ud/qmb+imX6Ul9iQsOZxFv152qHVvxmnd1l8OO9e1GWKYTXFBLjHn
72H/A4b3NnLA2ka7PFEZQvXh2QKBgQDgQOFkDbjdhMruL/fF5vq37HwUzSq2ISKe
F2MsQJNld3ZoULyRipWYXIM7uCA/eP6hNmYBTaKBr7kDzHLCEY2u08J7sFMWx/9a
sIgSJUGtz3sooe+e/GIRcedFNiqVOUl60S6tdIYkBXKCEbBT2WNN0HwHdWVOPbJx
r/9qFz/VtQKBgQC8m7ul6jx7DxmwDuTqOh2TEGSIOLE920Ha15M5amIScPPXdxvw
vITBrdCQOI61bcK/TPUyl+xGYtQMfZqKM/K3Pc2BZF1jtOtJ6jqbTryvza8F65mu
G7D54N8G694Sz4QXg3PTe0zx9AXyZEG2+ti/qkQ8h+UdtkV7oYqS/ixPAQKBgDwX
Bo5B4wxwndPvRIxiFUKdeq40P8Kn5FfKWoesEhL5TOAs6ipxoR4/g+bHstRvPoPC
SNkGjYoEpSXwbbu06mszUQTFva34D2OktAFwvEWvuAeuRMAsTrbv95GjLwvnWtov
HTvbYmpaj1FtHfuJ38MlH2b8PRYXEC7Igz9RVYiVAoGAImaNeSPbdKLfTG90gNrP
j2DdcC/JgJKgPECqjKokgkevgZPQcs449+OcxxtrB/n+bf2tJCrUTiO6lvxi2gvU
4bccccv4fBMmkGYHsHsph+qNGiwPaKz6TmypAcspIGM06ajVLH1zLzw8EfDFHUu0
FzuPgWBddTbzyAfiPYFwGW8=
-----END PRIVATE KEY-----"""

st.set_page_config(page_title="نظام الأرشفة", page_icon="🏛️")
st.title("🏛️ نظام الأرشفة النهائي")

up = st.file_uploader("اختر ملف PDF للرفع:", type=["pdf"])

if up and st.button("🚀 رفع الملف الآن"):
    try:
        creds = service_account.Credentials.from_service_account_info({
            "type": "service_account", "project_id": "project-e4fb2fde-9291-482a-b14",
            "private_key": PK, "client_email": MAIL, "token_uri": "https://oauth2.googleapis.com/token"
        })
        service = build('drive', 'v3', credentials=creds)

        with st.spinner("جاري معالجة الملف والرفع..."):
            # الرفع بدون تحديد مجلد لتجنب خطأ 404 المجلد غير موجود
            meta = {'name': up.name}
            media = MediaIoBaseUpload(io.BytesIO(up.read()), mimetype='application/pdf')
            file = service.files().create(body=meta, media_body=media, fields='id, webViewLink').execute()
            
            # جعل الملف متاحاً للعرض لكي يفتح معك الرابط
            service.permissions().create(fileId=file.get('id'), body={'type': 'anyone', 'role': 'viewer'}).execute()

            st.success("✅ تم الرفع بنجاح تام!")
            st.balloons()
            
            # الرابط السحري الذي سيفتح الملف المرفوع
            st.markdown(f"### 📥 [اضغط هنا لفتح الملف الذي رفعته الآن]({file.get('webViewLink')})")
            st.info("ملاحظة: الرابط أعلاه سيفتح الملف مباشرة في المتصفح.")
            
    except Exception as e:
        st.error(f"❌ حدث خطأ تقني: {e}")
