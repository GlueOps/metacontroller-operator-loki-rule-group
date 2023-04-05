FROM python:3.11.2-bullseye

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
