FROM python:3.15.2-alpine@sha256:1656b7eaf309cadf99069ea9de335c7f67a8355789cfc6f1835a05818996f081

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
