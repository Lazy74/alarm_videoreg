import json
import logging
import re
from typing import Optional


def clean_data(raw_data: str) -> str:
    """Удаляет мусор перед первым JSON-объектом."""
    return re.sub(r"^[^\{]*", "", raw_data.strip())


def extract_json(data: str) -> Optional[dict]:
    """Пытается распарсить JSON из строки."""
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        logging.exception("Ошибка парсинга JSON: %s", e)
        return None
