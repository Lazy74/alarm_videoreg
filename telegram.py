import logging

import requests

from config import settings


def send_telegram_message(message) -> None:
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": settings.TELEGRAM_CHAT_ID, "text": message}

    try:
        response = requests.post(url, json=payload)
        if not response.ok:
            logging.error(f"Не удалось отправить сообщение: {response.text}")
        else:
            logging.info("Сообщение отправлено в Telegram. Текст сообщения:")
            logging.info(f"{message}")
    except Exception as e:
        logging.exception(f"Ошибка при отправке в Telegram: {e}")
