FROM python:3.11.9-alpine@sha256:eb8afe385f10ccc9da8378e8712fea8b26f4ed009648f8afea4518836d8b3ed3

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
