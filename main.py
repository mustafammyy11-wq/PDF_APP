import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# 1. المعرفات الأساسية
FOLDER_ID = "1RLkxpJM8CEunpNDUcANE_jVdFII7V5bW"
CLIENT_EMAIL = "mustafairaq@project-e4fb2fde-9291-482a-b14.iam.gserviceaccount.com"

# 2. المفتاح السري بتنسيق سطر واحد (لحل مشكلة PEM نهائياً)
PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\n" + \
"MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDcufrbwTEdJ81n\n" + \
"xso1o/FzJ8XD7o83BVg4Y9qJ3gCkXpnXWkyFtqSHdcBDlGt370RRxDpuQxdrhKcN\n" + \
"psEUKPm8woTRq0u67OZnDlJHR7w2eFeris562xfDHCgGH8yhX+P39w5p8hMUyBmp\n" + \
"6pZoyAE4zVGHTqvKmMLgJGp4S6NpQusui68IfV+umcf+QifwaglCfWIuOjjBm/9G\n" + \
"W5lqOElJSaNwrQoJZMrZqSYxCELQ3LAI+xwBZnMBm7Aisqs7G/zRM3J610zDXX0X\n" + \
"UQc3Y/HFK+3jGbuZsIpwBI+VnmII5D+YEseN1ADzyjr6bVIN6hvWIxSVb6x3vZ14\n" + \
"mDoAKTttAgMBAAECggEAJo9S9LsOUnKWnq+Kuc43Kw/iq7TsTgdf/xHqprUi1ZQ1\n" + \
"OfrrbVyX55Y5jVTLZXtmKwal0odj+wOEj4z3JAd4gXJV868CHtit84j79Lnidn2V\n" + \
"i0FHiwzlXM95aoB5piNzVulRGk8Q6EuAuD9kIU/3bq3ntUSYHF+Ng8y40OUd2hBk\n" + \
"hWsKOFHCMqLk0Dzx2R2LfgpdOwEiEKCC4Qwp/sSOWROeQ75jXkxMMI0eMplsfFmA\n" + \
"Nag52aSw41ZAHFGEs/336Yydl+4SArsJd/p9pQ7Yg8FTJo+v3rvEHKSjOqMSnXXC\n" + \
"EQ6MQm0eYyF//xW3QUMJ6uwiB9nVw1o08zy/+sPM4QKBgQD7+UemBYX0tHXkfbAk\n" + \
"O316+seEk+vpWqzz8TYHAE941ciaMQe4/Rs13lzWd2TvyIR+VBq3bTUYSvNjc+4B\n" + \
"aVs8iaB51L4Ud/qmb+imX6Ul9iQsOZxFv152qHVvxmnd1l8OO9e1GWKYTXFBLjHn\n" + \
"72H/A4b3NnLA2ka7PFEZQvXh2QKBgQDgQOFkDbjdhMruL/fF5vq37HwUzSq2ISKe\n" + \
"F2MsQJNld3ZoULyRipWYXIM7uCA/eP6hNmYBTaKBr7kDzHLCEY2u08J7sFMWx/9a\n" + \
"sIgSJUGtz3sooe+e/GIRcedFNiqVOUl60S6tdIYkBXKCEbBT2WNN0HwHdWVOPbJx\n" + \
"r/9qFz/VtQKBgQC8m7ul6jx7DxmwDuTqOh2TEGSIOLE920Ha15M5amIScPPXdxvw\n" + \
"vITBrdCQOI61bcK/TPUyl+xGYtQMfZqKM/K3Pc2BZF1jtOtJ6jqbTryvza8F65mu\n" + \
"G7D54N8G694Sz4QXg3PTe0zx9AXyZEG2+ti/qkQ8h+UdtkV7oYqS/ixPAQKBgDwX\n" + \
"Bo5B4wxwndPvRIxiFUKdeq40P8Kn5FfKWoesEhL5TOAs6ipxoR4/g+bHstRvPoPC\n" + \
"SNkGjYoEpSXwbbu06mszUQTFva34D2OktAFwvEWvuAeuRMAsTrbv95GjLwvnWtov\n" + \
"HTvbYmpaj1FtHfuJ38MlH2b8PRYXEC7Igz9RVYiVAoGAImaNeSPbdKLfTG90gNrP\n" + \
"j2DdcC/JgJKgPECqjKokgkevgZPQcs449+OcxxtrB/n+bf2tJCrUTiO6lvxi2gvU\n" + \
"4bccccv4fBMmkGYHsHsph+qNGiwPaKz6TmypAcspIGM06ajVLH1zLzw8EfDFHUu0\n" + \
"FzuPgWBddTbzyAfiPYFwGW8=\n" + \
"-----END PRIVATE KEY-----\n"

st.set_page_config(page_title="نظام الأرشفة")
st.title("🏛️ نظام أرشفة مصطفى")

up = st.file_uploader("ارفع ملف PDF:", type=["pdf"])

if up and st.button("🚀 رفع الآن"):
    try:
        # تجهيز بيانات الاعتماد
        creds_info = {
            "type": "service_account",
            "project_id": "project-e4fb2fde-9291-482a-b14",
            "private_key": PRIVATE_KEY,
            "client_email": CLIENT_EMAIL,
            "token_uri": "https://oauth2.googleapis.com/token",
        }
        
        creds = service_account.Credentials.from_service_account_info(creds_info)
        service = build('drive', 'v3', credentials=creds)

        with st.spinner("جاري تخطي قيود المساحة والرفع..."):
            file_metadata = {'name': up.name, 'parents': [FOLDER_ID]}
            media = MediaIoBaseUpload(io.BytesIO(up.read()), mimetype='application/pdf')
            
            # رفع الملف مع تفعيل دعم المساحة المشتركة
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id',
                supportsAllDrives=True 
            ).execute()
            
            st.success("✅ أخيراً! تم الرفع بنجاح يا مصطفى.")
            st.balloons()
            
    except Exception as e:
        st.error(f"⚠️ حدث خطأ أثناء الرفع: {e}")
