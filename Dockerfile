FROM python:3.11.10-alpine@sha256:65c34f59d896f939f204e64c2f098db4a4c235be425bd8f0804fd389b1e5fd80

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./sync.py .
COPY ./src ./src

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install fastapi uvicorn



CMD ["fastapi", "run", "app/sync.py", "--port", "80"]
