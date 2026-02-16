import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# 1. بيانات الربط (جاهزة ومصلحة تماماً)
FOLDER_ID = "1O9RsIkXihdZrGMaLrALM3dYDjm6x23nL"

# تم تنسيق المفتاح هنا ليعمل 100% دون أخطاء PEM
PRIVATE_KEY = (
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

credentials_info = {
    "type": "service_account",
    "project_id": "project-e4fb2fde-9291-482a-b14",
    "private_key": PRIVATE_KEY,
    "client_email": "mustafairaq@project-e4fb2fde-9291-482a-b14.iam.gserviceaccount.com",
    "token_uri": "https://oauth2.googleapis.com/token",
}

# 2. وظيفة إنشاء الاتصال
def get_drive_service():
    creds = service_account.Credentials.from_service_account_info(credentials_info)
    return build('drive', 'v3', credentials=creds)

# 3. واجهة البرنامج
st.set_page_config(page_title="أرشيف المحطة", layout="centered")
st.title("🏛️ نظام الأرشفة المركزي")

password = st.sidebar.text_input("رمز الدخول:", type="password")

if password == "123":
    try:
        service = get_drive_service()
        # فحص الاتصال بالمجلد
        folder_metadata = service.files().get(fileId=FOLDER_ID, fields='name').execute()
        st.success(f"✅ متصل بمجلد: {folder_metadata['name']}")

        tab1, tab2 = st.tabs(["📤 رفع ملف", "🔍 بحث"])

        with tab1:
            uploaded_file = st.file_uploader("اختر ملف:")
            if uploaded_file and st.button("تأكيد الرفع"):
                with st.spinner("جاري الرفع..."):
                    file_metadata = {'name': uploaded_file.name, 'parents': [FOLDER_ID]}
                    media = MediaIoBaseUpload(io.BytesIO(uploaded_file.read()), mimetype=uploaded_file.type)
                    service.files().create(body=file_metadata, media_body=media).execute()
                    st.success("تم الرفع بنجاح!")
                    st.balloons()

        with tab2:
            query = st.text_input("ابحث عن اسم ملف:")
            if query:q=f"'{FOLDER_ID}' in parents and name contains '{query}'",
                    fields="files(id, name, webViewLink)"
                ).execute()
                items = results.get('files', [])
                if items:
                    for item in items:
                        st.write(f"📄 {item['name']}")
                        st.link_button("فتح الرابط", item['webViewLink'])
                else:
                    st.warning("لا يوجد ملف بهذا الاسم.")

    except Exception as e:
        st.error(f"⚠️ خطأ في الاتصال: {e}")
else:
    st.info("أدخل الرمز 123 للبدء")
                results = service.files().list(
