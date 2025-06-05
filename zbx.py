import logging
import time

from zabbix_utils import ItemValue, Sender

from config import settings


def send_zabbix_old(host: str, key: str, value: str) -> None:

    sender = Sender(settings.IP_ZABBIX, settings.PORT_ZABBIX)
    data = [ItemValue(host=host, key=key, value=value)]
    logging.info(f"send zabbix траппер: {data}")
    response = sender.send(data)
    logging.info(f"response: {response}")


def send_zabbix(host: str, key: str, value: str) -> None:
    sender = Sender(settings.IP_ZABBIX, settings.PORT_ZABBIX)

    # Этап 1: Отправка данных для создания элемента данных
    discovery_key = "discovery.channels"
    discovery_value = '{"data":[{"{#CHANNEL}":"' + key + '"}]}'
    discovery_data = [
        ItemValue(host=host, key=discovery_key, value=discovery_value)
    ]

    logging.info(f"Отправка данных для обнаружения: {discovery_data}")
    discovery_response = sender.send(discovery_data)
    logging.info(f"Ответ на запрос обнаружения: {discovery_response}")

    # Пауза т.к. требуется некоторое время для формирования элемента данных
    # time.sleep(2)

    # Этап 2: Отправка основного значения
    main_data = [
        ItemValue(host=host, key=f"channel.status[{key}]", value=value)
    ]
    logging.info(f"Отправка основного значения: {main_data}")
    main_response = sender.send(main_data)
    logging.info(f"Ответ на основной запрос: {main_response}")
