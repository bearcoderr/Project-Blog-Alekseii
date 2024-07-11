# telegram_utils.py

import telegram
from django.conf import settings

def send_telegram_message(text):
    try:
        bot_token = settings.TELEGRAM_BOT_TOKEN
        chat_id = settings.TELEGRAM_CHANNEL_ID
        bot = telegram.Bot(token=bot_token)
        bot.send_message(chat_id=chat_id, text=text)
        print(f"Message sent to Telegram channel with ID {chat_id}: {text}")
        return True
    except Exception as e:
        print(f"Error sending message to Telegram channel with ID {chat_id}: {e}")
        return False
