FROM python:3.11.10-alpine@sha256:004b4029670f2964bb102d076571c9d750c2a43b51c13c768e443c95a71aa9f3

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
