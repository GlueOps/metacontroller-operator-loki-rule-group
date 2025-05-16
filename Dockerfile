FROM python:3.11.12-alpine@sha256:d0199977fdae5d1109a89d0b0014468465e014a9834d0a566ea50871b3255ade

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
