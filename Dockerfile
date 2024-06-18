FROM python:3.11.9-alpine@sha256:e8effbb94ea2e5439c6b69c97c6455ff11fce94b7feaaed84bb0f2300d798cb7

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
