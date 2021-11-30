import os
import time
from datetime import datetime
import logging

import telegram
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
OWNER_CHAT_ID = os.getenv('OWNER_CHAT_ID')

RETRY_TIME = 60
HOURS_5 = 3600 * 5


def send_message(bot, chat_id, message):
    bot.send_message(chat_id, message)
    logging.info(f'Бот отправил сообщение {message}')


"""
def check_response(bot, response):
    
    last_author_id = updates[0]['message']
"""


def check_tokens():
    error_msg = 'Отсутствует обязательная переменная окружения:'
    if TELEGRAM_TOKEN is None:
        logging.critical(f'{error_msg} "TELEGRAM_TOKEN".')
        return False
    if TELEGRAM_CHAT_ID is None:
        logging.critical(f'{error_msg} "TELEGRAM_CHAT_ID".')
        return False
    return True


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    utc_time = datetime.utcnow()
    while True:
        try:
            if utc_time.hour == 19 and utc_time.minute == 30:
                message = 'Леночка, выпей таблетку \n:*'
                send_message(bot, TELEGRAM_CHAT_ID, message)
            time.sleep(RETRY_TIME)

            updates = bot.get_updates()
            text_of_last = updates[0]['message']['text']
            if text_of_last != message:
                send_message(bot, OWNER_CHAT_ID, text_of_last)
                message = text_of_last

            utc_time = datetime.utcnow()
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
