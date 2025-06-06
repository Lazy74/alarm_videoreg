import logging
import socket
import sys

from config import settings
from handlers import process_event
from logger import setup_logger
from telegram import send_telegram_message

setup_logger()


def run_server():

    # Создаем TCP-сервер
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((settings.HOST, settings.PORT))
        server_socket.listen()

        message = (
            f"Alarm Video Recorder to Zabbix Forwarder запущен. "
            f"Принимает соединения на порту {settings.PORT}. "
            f"Cервер Zabbix: {settings.IP_ZABBIX}:{settings.PORT_ZABBIX} "
            f"Уведомления в Telegram "
        )
        message += (
            "ВКЛЮЧЕНЫ" if settings.TELEGRAM_SEND_MESSAGE else "ВЫКЛЮЧЕНЫ"
        )
        logging.info(message)
        send_telegram_message(send_message=True, message=message)

        try:
            while True:
                conn, addr = server_socket.accept()
                with conn:
                    logging.info(f"Подключено к {addr}")
                    data = conn.recv(1024)
                    if not data:
                        continue
                    try:
                        decoded_data = data.decode("utf-8", errors="ignore")
                        process_event(decoded_data)
                    except Exception as e:
                        logging.exception(
                            f"Произошла ошибка при обработке данных: {e}"
                        )
        except KeyboardInterrupt:
            logging.info(
                "Получен сигнал KeyboardInterrupt. Завершение работы сервера..."
            )
        finally:
            server_socket.close()
            logging.info("Сервер остановлен.")
            sys.exit(0)


if __name__ == "__main__":
    run_server()
