FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim AS runner

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -u 10001 -m -s /bin/bash mlopsuser

COPY --from=builder /root/.local /home/mlopsuser/.local
COPY app /app/app

RUN mkdir -p /app/uploads && chown -R mlopsuser:mlopsuser /app

ENV PATH=/home/mlopsuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

USER mlopsuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
