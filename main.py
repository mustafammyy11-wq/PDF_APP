import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# 1. المفتاح الخاص (وضعته لك بطريقة "السطر الواحد" لتجنب أخطاء PEM)
KEY_STRING = (
    "-----BEGIN PRIVATE KEY-----\n"
    "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDcufrbwTEdJ81n\n"
    "xso1o/FzJ8XD7o83BVg4Y9qJ3gCkXpnXWkyFtqSHdcBDlGt370RRxDpuQxdrhKcN\n"
    "psEUKPm8woTRq0u67OZnDlJHR7w2eFeris562xfDHCgGH8yhX+P39w5p8hMUyBmp\n"
    "6pZoyAE4zVGHTqvKmMLgJGp4S6NpQusui68IfV+umcf+QifwaglCfWIuOjjBm/9G\n"
    "W5lqOElJSaNwrQoJZMrZqSYxCELQ3LAI+xwBZnMBm7Aisqs7G/zRM3J610zDXX0X\n"
    "UQc3Y/HFK+3jGbuZsIpwBI+VnmII5D+YEseN1ADzyjr6bVIN6hvWIxSVb6x3vZ14\n"
    "mDoAKTttAgMBAAECggEAJo9S9LsOUnKWnq+Kuc43Kw/iq7TsTgdf/xHqprUi1ZQ1\n"
    "OfrrbVyX55Y5jVTLZXtmKwal0odj+wOEj4z3JAd4gXJV868CHtit84j79Lnidn2V\n"
    "i0FHiwzlXM95aoB5piNzVulRGk8Q6EuAuD9kIU/3bq3ntUSYHF+Ng8y40OUd2hBk\nhWsKOFHCMqLk0Dzx2R2LfgpdOwEiEKCC4Qwp/sSOWROeQ75jXkxMMI0eMplsfFmA\Nag52aSw41ZAHFGEs/336Yydl+4SArsJd/p9pQ7Yg8FTJo+v3rvEHKSjOqMSnXXC\nEQ6MQm0eYyF//xW3QUMJ6uwiB9nVw1o08zy/+sPM4QKBgQD7+UemBYX0tHXkfbAk\nO316+seEk+vpWqzz8TYHAE941ciaMQe4/Rs13lzWd2TvyIR+VBq3bTUYSvNjc+4B\naVs8iaB51L4Ud/qmb+imX6Ul9iQsOZxFv152qHVvxmnd1l8OO9e1GWKYTXFBLjHn\n72H/A4b3NnLA2ka7PFEZQvXh2QKBgQDgQOFkDbjdhMruL/fF5vq37HwUzSq2ISKe\nF2MsQJNld3ZoULyRipWYXIM7uCA/eP6hNmYBTaKBr7kDzHLCEY2u08J7sFMWx/9a\nsIgSJUGtz3sooe+e/GIRcedFNiqVOUl60S6tdIYkBXKCEbBT2WNN0HwHdWVOPbJx\nr/9qFz/VtQKBgQC8m7ul6jx7DxmwDuTqOh2TEGSIOLE920Ha15M5amIScPPXdxvw\nvITBrdCQOI61bcK/TPUyl+xGYtQMfZqKM/K3Pc2BZF1jtOtJ6jqbTryvza8F65mu\nG7D54N8G694Sz4QXg3PTe0zx9AXyZEG2+ti/qkQ8h+UdtkV7oYqS/ixPAQKBgDwX\Bo5B4wxwndPvRIxiFUKdeq40P8Kn5FfKWoesEhL5TOAs6ipxoR4/g+bHstRvPoPC\nSNkGjYoEpSXwbbu06mszUQTFva34D2OktAFwvEWvuAeuRMAsTrbv95GjLwvnWtov\nHTvbYmpaj1FtHfuJ38MlH2b8PRYXEC7Igz9RVYiVAoGAImaNeSPbdKLfTG90gNrP\nj2DdcC/JgJKgPECqjKokgkevgZPQcs449+OcxxtrB/n+bf2tJCrUTiO6lvxi2gvU\n4bccccv4fBMmkGYHsHsph+qNGiwPaKz6TmypAcspIGM06ajVLH1zLzw8EfDFHUu0\nFzuPgWBddTbzyAfiPYFwGW8=\n"
    "-----END PRIVATE KEY-----\n"
)

# 2. بيانات الحساب ومعرف المجلد
GCP_JSON = {
    "type": "service_account",
    "project_id": "project-e4fb2fde-9291-482a-b14",
    "private_key": KEY_STRING,
    "client_email": "mustafairaq@project-e4fb2fde-9291-482a-b14.iam.gserviceaccount.com",
    "token_uri": "https://oauth2.googleapis.com/token",
}
FOLDER_ID = "1O9RsIkXihdZrGMaLrALM3dYDjm6x23nL"

def get_drive_service():
    try:
        creds = service_account.Credentials.from_service_account_info(GCP_JSON)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        st.error(f"خطأ في بناء الخدمة: {e}")
        return None

st.set_page_config(page_title="الأرشيف الذكي", layout="centered")

if st.sidebar.text_input("رمز الدخول:", type="password") == "123":
    st.title("🏛️ الأرشيف المركزي")
    service = get_drive_service()
    
    if service:
        try:
            # اختبار الاتصال بالمجلد
            folder = service.files().get(fileId=FOLDER_ID, fields='name').execute()
            st.success(f"✅ متصل بنجاح بمجلد: {folder['name']}")
            
            up_file = st.file_uploader("اختر ملف الوصل:")
            if up_file and st.button("تأكيد الرفع"):
                with st.spinner("جاري الرفع..."):
                    metadata = {'name': up_file.name, 'parents': [FOLDER_ID]}
                    media = MediaIoBaseUpload(io.BytesIO(up_file.read()), mimetype=up_file.type)
                    service.files().create(body=metadata, media_body=media).execute()
                    st.success("✅ تم الرفع!")
                    st.balloons()
        except Exception as e:
            st.error("⚠️ البرمجية لا ترى المجلد.")
            st.info(f"تأكد من مشاركة المجلد مع: {GCP_JSON['client_email']}")
else:
    st.info("أدخل الرمز 123 للبدء")
