FROM python:3.12.8-alpine@sha256:fd340d298d9d537a33c859f03bcc60e8e2542968e16f998bb0e232e25b4b23bd

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
