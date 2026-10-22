FROM python:3.14.9-alpine@sha256:d55673c233e28839c1c0c69766428cb6d50174a2ecfdcf915b6f58a0b0991562

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
