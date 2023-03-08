import os

import openai
import telegram
from dotenv import load_dotenv
from telegram.ext import Filters, MessageHandler, Updater

totalMessage = 0
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
model_engine = (
    "text-davinci-002"  # or "text-davinci-003" for a more capable (and expensive) model
)

# define a function to generate a response using OpenAI
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


def handle_message(update, context):
    user_message = update.message.text
    totalMessage += 1
    print(totalMessage)
    prompt = f"User: {user_message}\nAI:"
    ai_response = generate_response(prompt)
    update.message.reply_text(totalMessage)


bot = telegram.Bot(token=os.getenv("env"))

updater = Updater(bot.token, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

updater.start_polling()
