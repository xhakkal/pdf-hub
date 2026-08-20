# Multi-stage build: build frontend first, then copy to backend
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ .
RUN npm run build

# Backend stage
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy built frontend to serve static files
COPY --from=frontend-builder /app/frontend/dist ./static

# Create temp directory
RUN mkdir -p /tmp/pdf_temp/output

EXPOSE 5000

ENV FLASK_PORT=5000
ENV TEMP_DIR=/tmp/pdf_temp

CMD gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120 app:app