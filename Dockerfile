FROM python:3.11.11-alpine@sha256:fbcb089a803d5673f225dc923b8e29ecc7945e9335465037b6961107b9da3d61

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
