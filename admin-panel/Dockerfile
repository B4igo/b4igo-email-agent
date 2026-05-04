FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

COPY admin-panel/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY admin-panel/ /app/

# Vendor frontend dependencies (htmx + xterm.js + fit addon).
RUN set -e; \
    cd /app/static; \
    curl -fsSL -o htmx.min.js     https://unpkg.com/htmx.org@1.9.12/dist/htmx.min.js; \
    curl -fsSL -o xterm.js        https://unpkg.com/xterm@5.3.0/lib/xterm.js; \
    curl -fsSL -o xterm.css       https://unpkg.com/xterm@5.3.0/css/xterm.css; \
    curl -fsSL -o xterm-addon-fit.js https://unpkg.com/xterm-addon-fit@0.8.0/lib/xterm-addon-fit.js

EXPOSE 5400

CMD ["uvicorn", "admin_panel:app", "--host", "0.0.0.0", "--port", "5400"]
