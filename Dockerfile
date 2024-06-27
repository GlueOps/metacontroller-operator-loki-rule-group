FROM python:3.11.9-alpine@sha256:5745fa2b8591a756160721b8305adba3972fb26a9132789ed60160f21e55f5dc

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
