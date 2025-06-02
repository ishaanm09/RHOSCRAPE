###############################################
# Dockerfile — Railway web service
# ---------------------------------------------
# * Uses slim Python 3.11 base image
# * Installs the shared libraries Chromium needs
# * Installs Python deps *and* Playwright Chromium   ← happens once at build‑time
# * Falls back to gunicorn entry‑point (Railway can still override via startCommand)
###############################################

FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# -------------------------------------------------
# 1️⃣  System libraries required by headless Chrome
# -------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libnss3 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 \
        libdrm-dev libgbm-dev libxdamage1 libxfixes3 \
        libxcomposite1 libasound2 libxrandr2 libxss1 \
        xdg-utils fonts-liberation && \
    rm -rf /var/lib/apt/lists/*

# -------------------------------------------------
# 2️⃣  Python deps + Playwright browser install
# -------------------------------------------------
WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    # Pre‑install Chromium so runtime never downloads it again
    python -m playwright install --with-deps chromium

# -------------------------------------------------
# 3️⃣  Copy source code *after* deps to leverage Docker layer cache
# -------------------------------------------------
COPY . .

# -------------------------------------------------
# 4️⃣  Gunicorn defaults (Railway can override via startCommand)
#     Same settings you put in railway.toml
# -------------------------------------------------
ENV GUNICORN_CMD_ARGS="--timeout 300 --workers 2"
EXPOSE 8000

CMD ["gunicorn", "api_server:app", "-b", "0.0.0.0:8000"]
