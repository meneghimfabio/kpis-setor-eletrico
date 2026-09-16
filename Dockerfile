# Stage 1: Build Frontend
FROM node:22-slim AS frontend-builder
WORKDIR /build
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Backend Runtime
FROM python:3.11-slim
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PORT=8080 \
    GCP_PROJECT_ID=kpisetoreletrico

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY backend/ ./

# Copy compiled frontend SPA to static directory
COPY --from=frontend-builder /build/dist /app/static

EXPOSE 8080

CMD ["python", "run.py"]
