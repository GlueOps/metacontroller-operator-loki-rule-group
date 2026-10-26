FROM python:3.15.2-alpine@sha256:827d76cd0da4f700a703df95e7a70fec2ecc7fa9fd528638ab2e8aa96fbf8e0e

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
