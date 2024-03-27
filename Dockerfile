FROM python:3.11.8-alpine3.19@sha256:b6bd7d58b4e0f38cd151de9b96fffc9edf647bc6ba490ffe772d5d5eab11acda

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
