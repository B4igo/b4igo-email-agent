FROM python:3.12-slim

WORKDIR /app

FROM python:3.12-slim

# Add system dependencies required by OpenCV / Docling
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libxcb1 \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY ai_service/requirements.txt .
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

COPY shared/ shared/
COPY ai_service/app.py .

EXPOSE 5300

CMD ["python", "app.py"]
