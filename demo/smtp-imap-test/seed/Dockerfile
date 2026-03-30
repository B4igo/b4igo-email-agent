FROM python:3.12-slim

WORKDIR /app
COPY accounts.json seed.py ./

CMD ["python", "-u", "seed.py"]
