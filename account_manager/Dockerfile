FROM python:3.12-slim

WORKDIR /app

COPY account_manager/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ shared/
# Real OAuth secrets are gitignored. The glob copies client_secrets.json when
# present and otherwise falls back to the tracked .example, so a fresh clone
# still builds. Provide a real client_secrets.json to enable the Gmail flow.
COPY client_secrets.json* ./
COPY account_manager/account_manager_app.py .

EXPOSE 5100

CMD ["python", "account_manager_app.py"]
