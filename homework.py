import os
import time
from datetime import datetime
import logging

import telegram
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 60
HOURS_5 = 3600 * 5


def send_message(bot, message):
    bot.send_message(TELEGRAM_CHAT_ID, message)
    logging.info(f'Бот отправил сообщение {message}')


"""
def check_response(bot):
    updates = bot.get_updates()
    text_of_last = updates[0]['message']['text']
    if text_of_last in ['ОК', 'Ок', 'ок', 'OK', 'Ok', 'ok', 'Выпила', 'выпила', 'Спасибо', 'спасибо']:
        return True
    else:
        return False
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
                send_message(bot, 'Леночка, выпей таблетку \n:*')
            time.sleep(RETRY_TIME)
            utc_time = datetime.utcnow()
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
