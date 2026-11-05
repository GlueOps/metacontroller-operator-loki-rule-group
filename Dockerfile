FROM python:3.15.2-alpine@sha256:d499023466546cd88a358f80b46fba4016f32597bc4482bb1c47b483a07d457d

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
