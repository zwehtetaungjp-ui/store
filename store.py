import streamlit as st
import requests
from datetime import datetime

# Streamlit Page Setting
st.set_page_config(
    page_title="ဂိုထောင် ပစ္စည်းစစ်ဆေးရေး",
    page_icon="📦",
    layout="wide"
)

# Telegram Config
BOT_TOKEN = "8683276106:AAHIDeDyVGRRjJUuIEH-YPHIJjuZ3eXHL3s"
CHAT_ID = "6826543956"

# ပစ္စည်းများစာရင်း Data (၃၀ ခု)
ITEMS_DATA = [
    {"id": 1, "name": "ပစ္စည်း ၁", "img": "https://www.bing.com/images/search?view=detailV2&ccid=KgFb17o1&id=E82203BBE71D67B576C01381702CE1DA5A4C83B4&thid=OIP.KgFb17o15i0Q1T0RdDhjpgHaEK&mediaurl=https%3A%2F%2Fwww.mashed.com%2Fimg%2Fgallery%2F23-eggplant-recipes-even-meat-eaters-will-love%2Fl-intro-1662170192.jpg&exph=901&expw=1600&q=eggplant&form=IRPRST&ck=52D83518ECD0AA12C52B0EC501686A4C&selectedindex=11&itb=0&cw=1250&ch=592&ajaxhist=0&ajaxserp=0&vt=0&sim=11"},
    {"id": 2, "name": "ပစ္စည်း ၂", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 3, "name": "ပစ္စည်း ၃", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 4, "name": "ပစ္စည်း ၄", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 5, "name": "ပစ္စည်း ၅", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 6, "name": "ပစ္စည်း ၆", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 7, "name": "ပစ္စည်း ၇", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 8, "name": "ပစ္စည်း ၈", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 9, "name": "ပစ္စည်း ၉", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 10, "name": "ပစ္စည်း ၁၀", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 11, "name": "ပစ္စည်း ၁၁", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 12, "name": "ပစ္စည်း ၁၂", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 13, "name": "ပစ္စည်း ၁၃", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 14, "name": "ပစ္စည်း ၁၄", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 15, "name": "ပစ္စည်း ၁၅", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 16, "name": "ပစ္စည်း ၁၆", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 17, "name": "ပစ္စည်း ၁၇", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 18, "name": "ပစ္စည်း ၁၈", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 19, "name": "ပစ္စည်း ၁၉", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 20, "name": "ပစ္စည်း ၂၀", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 21, "name": "ပစ္စည်း ၂၁", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 22, "name": "ပစ္စည်း ၂၂", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 23, "name": "ပစ္စည်း ၂၃", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 24, "name": "ပစ္စည်း ၂၄", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 25, "name": "ပစ္စည်း ၂၅", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 26, "name": "ပစ္စည်း ၂၆", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 27, "name": "ပစ္စည်း ၂၇", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 28, "name": "ပစ္စည်း ၂၈", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 29, "name": "ပစ္စည်း ၂၉", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 30, "name": "ပစ္စည်း ၃၀", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
]

# Session state စတင် သတ်မှတ်ခြင်း (Page Switch လုပ်ရန်)
if "page" not in st.session_state:
    st.session_state.page = 1
if "checked_data" not in st.session_state:
    st.session_state.checked_data = {}

# Telegram သို့ စာပို့ပေးသည့် Function
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID ,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {"ok": False, "description": str(e)}

# ----------------PAGE 1: စာရင်း ရိုက်ထည့်သည့် စာမျက်နှာ ----------------
if st.session_state.page == 1:
    st.title("発注 (ဂိုထောင် ပစ္စည်းစစ်ဆေးရေး)")
    st.write("数を入力してください")

    # Input Form
    with st.form("inventory_form"):
        # Grid ကဲ့သို့ ၃ ကော်လံ ခွဲပြခြင်း
        cols_per_row = 3
        form_data = {}

        for i in range(0, len(ITEMS_DATA), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(ITEMS_DATA):
                    item = ITEMS_DATA[i + j]
                    with cols[j]:
                        st.image(item["img"], width=80)
                        st.markdown(f"*{item['name']}*")
                        # Input box
                        qty = st.number_input(
                            label=f"qty_{item['id']}", 
                            min_value=0, 
                            step=1, 
                            key=f"input_{item['id']}",
                            label_visibility="collapsed"
                        )
                        if qty > 0:
                            form_data[item["name"]] = qty
                        st.divider()

        # Check Button
        submitted = st.form_submit_button("Check စစ်ဆေးမည်", use_container_width=True, type="primary")

        if submitted:
            if not form_data:
                st.error("⚠️ အနည်းဆုံး ပစ္စည်းတစ်ခု၏ အရေအတွက်ကို ရိုက်ထည့်ပါ!")
            else:
                st.session_state.checked_data = form_data
                st.session_state.page = 2
                st.rerun()

# ----------------PAGE 2: အတည်ပြုပြီး Telegram သို့ ပို့သည့် စာမျက်နှာ ----------------
elif st.session_state.page == 2:
    if st.button("← ပြင်ဆင်မည်　直す"):
        st.session_state.page = 1
        st.rerun()

    st.title("စစ်ဆေးထားသည့် စာရင်း　発注リスト")

    # ရွေးချယ်ထားသော စာရင်းများ ပြသခြင်း
    st.subheader("Selected Items,ရွေးချယ်ထားသော ပစ္စည်းများ:")
    for name, qty in st.session_state.checked_data.items():
        st.write(f"• *{name}*: {qty} ခု")

    st.divider()

    # Telegram သို့ ပို့မည့် ခလုတ်
    if st.button("Send to Telegram 🚀", use_container_width=True, type="primary"):
        # Message စာသား ပြင်ဆင်ခြင်း
        message_text = "📦 ဂိုထောင် ပစ္စည်းစစ်ဆေးပြီး စာရင်း\n\n"
        for name, qty in st.session_state.checked_data.items():
            message_text += f"• {name}: {qty} ခု\n"
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_text += f"\n📅 ရက်စွဲ: {current_time}"

        with st.spinner("送信中。。。Telegram သို့ စာပို့နေပါသည်..."):
            res = send_telegram_message(message_text)

        if res.get("ok"):
            st.success("✅できた Done Telegram သို့ စာရင်းများ ပို့ဆောင်ပြီးပါပြီ!")
            st.balloons()
        else:
            st.error(f"❌エラー ပို့ဆောင်မှု မအောင်မြင်ပါ: {res.get('description')}")
