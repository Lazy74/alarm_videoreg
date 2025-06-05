import logging
from typing import Dict

from config import settings
from telegram import send_telegram_message
from zbx import send_zabbix

# Список разрешенных типов событий
ALLOWED_EVENT_TYPES = {"Alarm"}
# Список исключаемых событий
EXCLUDED_EVENTS = {"HumanDetect"}


def process_event(data: str) -> None:
    """
    Обрабатывает полученное событие: фильтрует и
    отправляет уведомление при необходимости.
    """
    from utils import clean_data, extract_json

    cleaned_data = clean_data(data)
    json_data = extract_json(cleaned_data)

    if not json_data:
        return
    else:
        logging.info(f"Получено сообщение: {json_data}")

    event = json_data.get("Event")
    type_message = json_data.get("Type")

    if type_message in ALLOWED_EVENT_TYPES and event not in EXCLUDED_EVENTS:
        date = json_data.get("StartTime") or json_data.get("StopTime")
        if not date:
            logging.warning("Нет доступной даты (StartTime или StopTime).")
            return

        channel = int(json_data.get("Channel")) + 1
        key = f"channel {channel}"
        # key = f"status_channel_{channel}"
        if json_data.get("Status") == "Start":
            value = 4
        else:
            value = 0

        host_name = json_data.get("Address")

        send_zabbix(host=host_name, key=key, value=value)

        if settings.TELEGRAM_SEND_MESSAGE:
            message = format_telegram_message(json_data)
            send_telegram_message(message)
    else:
        logging.info(f'Событие "{event}" типа "{type_message}" исключено.')


def format_telegram_message(data: Dict) -> str:
    """
    Формирует строку сообщения из данных события.
    """
    return (
        f"Дата: {data.get('StartTime') or data.get('StopTime')}\n"
        f"Событие: {data.get('Event')} ({data.get('Status')})\n"
        f"ID: {data.get('SerialID')}\n"
        f"Канал: {data.get('Channel')}"
    )
