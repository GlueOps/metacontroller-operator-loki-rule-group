FROM python:3.14.0-alpine@sha256:9c32c2f24d00536cac7d4d356d82c5274fb17366c52aa59ed0cc4c06f8b60a35

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
