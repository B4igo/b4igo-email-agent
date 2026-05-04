FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY ai_service/requirements.txt .
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

COPY shared/ shared/
COPY ai_service/ ai_service/

EXPOSE 5300

CMD ["python", "-m", "ai_service.app"]
