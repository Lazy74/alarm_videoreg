import logging
import os
from logging.handlers import RotatingFileHandler

from config import settings


def setup_logger():
    # Создаем логгер
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Формат логов
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Проверка и создание директории для логов
    log_directory = os.path.dirname(settings.LOG_FILE)
    if log_directory and not os.path.exists(log_directory):
        os.makedirs(log_directory, exist_ok=True)
        logger.info(f"Создана директория для логов: {log_directory}")

    # Настройка RotatingFileHandler для ротации логов
    file_handler = RotatingFileHandler(
        filename=settings.LOG_FILE,
        maxBytes=settings.LOG_SIZE_LIMIT,
        backupCount=settings.MAX_LOG_FILES,
        encoding="utf-8",  # Кодировка файла
    )
    file_handler.setFormatter(formatter)

    # Добавляем обработчики: файловый и консольный
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
