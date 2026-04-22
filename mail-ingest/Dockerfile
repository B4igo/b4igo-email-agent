FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY mail-ingest/requirements.txt .
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

COPY shared/ shared/
COPY mail-ingest/mail_ingest.py .

CMD ["python", "mail_ingest.py"]
