import streamlit as st
import requests
from datetime import datetime

# ⚠️ ၁။ st.set_page_config ကို အမြဲတမ်း ပထမဆုံး Streamlit Command အဖြစ် ထားရပါမည်
st.set_page_config(
    page_title="Check Items for Order あべの",
    page_icon="📦",
    layout="wide"
)

# ⚠️ ၂။ Primary Button များကို အစိမ်းရောင် ပြောင်းရန် CSS Style
st.markdown(
    """
    <style>
    /* Primary Button အရောင်ကို အစိမ်းရောင် ပြောင်းခြင်း */
    button[data-testid="stBaseButton-primary"] {
        background-color: #28a745 !important;
        color: white !important;
        border-color: #28a745 !important;
    }
    button[data-testid="stBaseButton-primary"]:hover {
        background-color: #218838 !important;
        border-color: #1e7e34 !important;
    }
    
    /* Form ရဲ့ Submit Button ကိုလည်း အစိမ်းရောင် ပြောင်းပေးခြင်း */
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #28a745 !important;
        color: white !important;
        border-color: #28a745 !important;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #218838 !important;
        border-color: #1e7e34 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Telegram Config
BOT_TOKEN = "8683276106:AAHIDeDyVGRRjJUuIEH-YPHIJjuZ3eXHL3s"
CHAT_ID = "6826543956"

# ပစ္စည်းများစာရင်း Data (၃၀ ခု)
ITEMS_DATA = [
    {"id": 1, "name": "なすび", "img": "pictures for Store/eggplant.png"},
    {"id": 2, "name": "かぼちゃ", "img": "pictures for Store/pukim.png"},
    {"id": 3, "name": "れんこん", "img": "pictures for Store/renkon.png"},
    {"id": 5, "name": "白ネギ", "img": "pictures for Store/shironegi.png"},
    {"id": 6, "name": "青ネギ", "img": "pictures for Store/aonegi.png"},
    {"id": 7, "name": "だいこん", "img": "pictures for Store/daikon.png"},
    {"id": 8, "name": "大葉", "img": "pictures for Store/oba.png"},
    {"id": 9, "name": "玉ねぎ", "img": "pictures for Store/onion.png"},
    {"id": 4, "name": "さつまいも", "img": "pictures for Store/satsumai.png"},
    {"id": 10, "name": "ပစ္စည်း ၁၀", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 11, "name": "からあげソース", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 12, "name": "からあげ粉", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 13, "name": "小粉", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 14, "name": "天ぷら粉", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 15, "name": "ソースカツタレ", "img": "pictures for Store/sosukatsu.png"},
    {"id": 16, "name": "カレー", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 17, "name": "なんばんタレ", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 18, "name": "ပစ္စည်း ၁၈", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 19, "name": "ပစ္စည်း ၁၉", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 20, "name": "ပစ္စည်း ၂၀", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 21, "name": "ပစ္စည်း ၂၁", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 22, "name": "ပစ္စည်း ၂၂", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 23, "name": "ပစ္စည်း ၂၃", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 24, "name": "ပစ္စည်း ၂၄", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 25, "name": "ပစ္စည်း ၂၅", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 26, "name": "ပစ္စည်း ၂၆", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 27, "name": "うどん", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 28, "name": "🌾こめ", "img": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"},
    {"id": 29, "name": "油", "img": "pictures for Store/oil.png"},
    {"id": 30, "name": "たまご（卵）", "img": "pictures for Store/egg.png"},
]

# Session state စတင် သတ်မှတ်ခြင်း (Page Switch နှင့် Input Values များ မှတ်ထားရန်)
if "page" not in st.session_state:
    st.session_state.page = 1
if "checked_data" not in st.session_state:
    st.session_state.checked_data = {}
# ✨ တန်ဖိုးများကို မပျောက်အောင် သိမ်းရန် Dictionary သစ်တစ်ခု ထည့်သွင်းခြင်း
if "input_values" not in st.session_state:
    st.session_state.input_values = {}

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
        cols_per_row = 3
        form_data = {}

        for i in range(0, len(ITEMS_DATA), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(ITEMS_DATA):
                    item = ITEMS_DATA[i + j]
                    item_id = item["id"]
                    
                    # ယခင် ရိုက်ထားဖူးသော တန်ဖိုးရှိရင် ပြန်ယူ၊ မရှိရင် 0 လို့ သတ်မှတ်
                    saved_val = st.session_state.input_values.get(item_id, 0)

                    with cols[j]:
                        st.image(item["img"], width=200)
                        st.markdown(f"*{item['name']}*")
                        
                        # ✨ value=saved_val ထည့်ပေးထားသောကြောင့် နောက်ပြန်လာရင် တန်ဖိုးမပျောက်ပါ
                        qty = st.number_input(
                            label=f"qty_{item_id}", 
                            min_value=0, 
                            value=saved_val,
                            step=1, 
                            key=f"input_{item_id}",
                            label_visibility="collapsed"
                        )
                        
                        # ရိုက်ထည့်ထားသည့် တန်ဖိုးများကို မှတ်ထားခြင်း
                        st.session_state.input_values[item_id] = qty
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
    if st.button("← ပြင်ဆင်မည် 直す"):
        st.session_state.page = 1
        st.rerun()

    st.title("စစ်ဆေးထားသည့် စာရင်း 発注リスト")

    # ရွေးချယ်ထားသော စာရင်းများ ပြသခြင်း
    st.subheader("Selected Items,ရွေးချယ်ထားသော ပစ္စည်းများ:")
    for name, qty in st.session_state.checked_data.items():
        st.write(f"•   *{name}*  :  {qty}  点")

    st.divider()

    # Telegram သို့ ပို့မည့် ခလုတ်
    if st.button("Send to TG 送信", use_container_width=True, type="primary"):
        # Message စာသား ပြင်ဆင်ခြင်း
        message_text = "📦 ဂိုထောင် ပစ္စည်းစစ်ဆေးပြီး စာရင်း\n\n"
        for name, qty in st.session_state.checked_data.items():
            message_text += f"• {name} : {qty}  点\n"
        
        current_time = datetime.now().strftime("%Y-%m-%d")
        message_text += f"\n📅 Date ရက်စွဲ: {current_time}"

        with st.spinner("送信中。。。Telegram သို့ စာပို့နေပါသည်..."):
            res = send_telegram_message(message_text)

        if res.get("ok"):
            st.success("✅できた Done Telegram သို့ စာရင်းများ ပို့ဆောင်ပြီးပါပြီ!")
            st.balloons()
            # ပို့ပြီးသွားပါက ရိုက်ထားသမျှ Data များကို Clear လုပ်ချင်ပါက အောက်ပါ ကုဒ် ၂ ကြောင်းကို ပြန်ဖွင့်နိုင်ပါတယ်
            # st.session_state.input_values = {}
            # st.session_state.checked_data = {}
        else:
            st.error(f"❌エラー ပို့ဆောင်မှု မအောင်မြင်ပါ: {res.get('description')}")
