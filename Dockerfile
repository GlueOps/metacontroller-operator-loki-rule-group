FROM python:3.13.1-alpine@sha256:657dbdb20479a6523b46c06114c8fec7db448232f956a429d3cc0606d30c1b59

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
