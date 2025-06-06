FROM python:3.11-alpine

WORKDIR /app
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY config.py handlers.py logger.py main.py telegram.py utils.py zbx.py ./

CMD ["python", "main.py"]
