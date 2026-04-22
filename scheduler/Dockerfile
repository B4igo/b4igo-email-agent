FROM python:3.12-slim

WORKDIR /app

COPY scheduler/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ shared/
COPY scheduler/scheduler.py .

EXPOSE 5200

CMD ["python", "scheduler.py"]
