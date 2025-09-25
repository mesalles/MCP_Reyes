# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy project files
COPY . .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir .

EXPOSE 8084

CMD ["python", "start_server.py", "--host", "0.0.0.0", "--port", "8084"]
