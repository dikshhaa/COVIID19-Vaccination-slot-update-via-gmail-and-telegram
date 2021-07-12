import requests
import smtplib
import email
from datetime import datetime



# 1890536226:AAEZBwkNPNByfa5C2LAWHhuJyk2Em5mHx50

# https://api.telegram.org/bot1890536226:AAEZBwkNPNByfa5C2LAWHhuJyk2Em5mHx50/getMe
# send_text = 'https://api.telegram.org/bot/1890536226:AAEZBwkNPNByfa5C2LAWHhuJyk2Em5mHx50/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message


api_url_telegram= "https://api.telegram.org/bot1840937250:AAHTNzjlLCqlqZqhZaMNZxO2XwMXRs3TjyA/sendMessage?chat_id=-540212685&text="
group_id="-540212685"
# https://api.telegram.org/bot1840937250:AAHTNzjlLCqlqZqhZaMNZxO2XwMXRs3TjyA/sendMessage?chat_id=-540212685&text="hello"

while True:

    def create_session_info(center,session):
        return {"name": center["name"],
                "date": session["date"],
                "capacity": session["available_capacity"],
                "age_limit":session["min_age_limit"]}

    def get_sessions(data):
        for center in data["centers"]:
            for session in center["sessions"]:
                yield create_session_info(center, session)

    def is_available(session):
        return session["capacity"]>0

    def is_eighteen_plus(session):
        return session["age_limit"]==18

    def get_for_seven(start_date):
        url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
        params={"district_id":392,"date":start_date.strftime("%d-%m-%y")}
        resp=requests.get(url,params=params,headers=headers)
        data=resp.json()
        return [session for session in get_sessions(data) if is_eighteen_plus(session) and is_available(session)]


    def create_output(session_info):
        return f"{session_info['date']} - {session_info['name']} ({session_info['capacity']})"

    def send_message_telegram(message):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
        # final_telegram_url=api_url_telegram.replace("_groupid_",group_id)
        final_telegram_url=api_url_telegram+message
        response=requests.get(final_telegram_url,headers={'User-Agent': 'Custom'})
        print(response)


    content = "\n".join([create_output(session_info) for session_info in get_for_seven(datetime.today())])
    content1 =([create_output(session_info) for session_info in get_for_seven(datetime.today())])



    get_for_seven(datetime.today())

    username = "rammohnishdikshasrijan@gmail.com"
    password = "Rammohnishdiksha"
    if not content:
        print("No availability")



    else:
        email_msg = email.message.EmailMessage()
        email_msg["Subject"] = "Vaccination Slot Open"
        email_msg["From"] = username
        email_msg["To"] = username
        for i in content1:
            email_msg.set_content(i)

        with smtplib.SMTP(host='smtp.gmail.com', port='587') as server:
            server.starttls()
            server.login(username, password)
            server.send_message(email_msg, username, username)
        # for i in content1:
        #     send_message_telegram(i)

