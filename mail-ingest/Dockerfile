FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

COPY mail-ingest/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ shared/
COPY mail-ingest/mail_ingest.py .

CMD ["python", "mail_ingest.py"]
