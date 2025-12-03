FROM python:3.14.1-alpine@sha256:4f699e4afac838c50be76deac94a6dde0e287d5671fd8e95eb410f850801b237

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
