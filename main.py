import os
from datetime import datetime
from googletrans import Translator
import openai
import telegram
from dotenv import load_dotenv
from telegram.ext import Filters, MessageHandler, Updater
from easygoogletranslate import EasyGoogleTranslate
users_data = []
user = {}
load_dotenv()
totalMessages = 0
openai.api_key = os.getenv("OPENAI_API_KEY")
model_engine = "text-davinci-002"


def generate_response(prompt):

    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        temperature=0.7,
    )
    message = response.choices[0].text.strip()
    return message


def check_total(update):

    user_id = update.message.from_user.id
    global users_data
    global user
    found = False
    for row in users_data:
        if row["id"] == user_id:
            found = True
            row["count"] += 1
            if row["count"] > 25:
                if row["count"] == 26:
                    allowed_time = datetime.now()
                    allowed_time = allowed_time.replace(hour=allowed_time.hour % 24 + 5)
                    row["ban_time"] = allowed_time
                    return True
                if isinstance(row["ban_time"], datetime):
                    if row["ban_time"] < datetime.now():
                        row["count"] = 0
                        return True
                update.message.reply_text("please wait ")
            else:
                return True
    if not found:
        user = {"id": user_id, "count": 0, "ban_time": datetime.now()}
        users_data.append(user)
        return True
def toEnglish(text):
    translator = EasyGoogleTranslate(
        target_language='en',
        timeout=10
    )
    return(translator.translate(text))
def toAmharic(text):
    translator = EasyGoogleTranslate(
        target_language='am',
        timeout=10
    )
    return(translator.translate(text))

def handle_message(update, context):
    if check_total(update):
        user_message = toEnglish(update.message.text)
        prompt = f"User: {user_message}\nAI:"
        ai_response = generate_response(prompt)
        update.message.reply_text(toAmharic(ai_response))


bot = telegram.Bot(token=os.getenv("env"))

updater = Updater(bot.token, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
updater.start_polling()
