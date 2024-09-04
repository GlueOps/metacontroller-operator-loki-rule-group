FROM python:3.11.9-alpine@sha256:1bcefb95bd059ea0240d2fe86a994cf13ab7465d00836871cf1649bb2e98fb9f

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
