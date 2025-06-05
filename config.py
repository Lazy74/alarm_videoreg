import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = os.path.join(BASE_DIR, ".env")


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Настройки Telegram
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: int = 0
    TELEGRAM_SEND_MESSAGE: bool = False

    # # Настройки TCP-сервера
    HOST: str = "0.0.0.0"
    PORT: int = 15002

    # Настройка логирования
    LOG_FILE: str = os.path.join(BASE_DIR, "logs", "app.log")
    MAX_LOG_FILES: int = 5
    # log_size_limit
    LOG_SIZE_LIMIT: int = 1024 * 1024 * 1  # 10 МБ

    # Настройка подключения к zabbix
    IP_ZABBIX: str
    PORT_ZABBIX: int


# Экземпляр настроек
settings = Settings()
