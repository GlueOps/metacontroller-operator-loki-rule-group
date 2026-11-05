FROM python:3.15.2-alpine@sha256:2b4b04f31a4a009c1fadf7ce9338471f288488199cf43dcd1af71f244ea550aa

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "/app/sync.py"]
