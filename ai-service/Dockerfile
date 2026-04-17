FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

COPY ai-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ shared/
COPY ai-service/app.py .

EXPOSE 5300

CMD ["python", "app.py"]
