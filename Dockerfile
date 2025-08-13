FROM python:3.11.13-alpine@sha256:8d8c6d3808243160605925c2a7ab2dc5c72d0e75651699b0639143613e0855b8

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
