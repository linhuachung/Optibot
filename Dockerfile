FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STATE_DIR=/data \
    AI_PROVIDER=gemini
WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY optibot/ ./optibot/
COPY main.py scrape.py upload.py ask.py system_prompt.txt ./

CMD ["python", "main.py"]
