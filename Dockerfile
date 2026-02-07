FROM python:3.14.3-alpine@sha256:faee120f7885a06fcc9677922331391fa690d911c020abb9e8025ff3d908e510

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
