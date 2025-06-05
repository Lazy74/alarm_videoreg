FROM python:3.11-alpine

WORKDIR /app
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY config.py .
COPY handlers.py .
COPY logger.py .
COPY main.py .
COPY requirements.txt .
COPY telegram.py .
COPY utils.py .
COPY zbx.py .

CMD ["python", "main.py"]
