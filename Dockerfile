FROM python:3.14.0-alpine@sha256:e1a567200b6d518567cc48994d3ab4f51ca54ff7f6ab0f3dc74ac5c762db0800

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
