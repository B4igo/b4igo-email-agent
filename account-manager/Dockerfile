FROM python:3.12-slim

WORKDIR /app

COPY account-manager/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ shared/
COPY client_secrets.json .
COPY account-manager/account_manager_app.py .

EXPOSE 5100

CMD ["python", "account_manager_app.py"]
