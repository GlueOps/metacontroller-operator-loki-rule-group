FROM python:3.13.8-alpine@sha256:7466fcadc01effec6ae9b26f147673090a9828a16ecd7cfa5898855e3bbf12db

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
