# Backend Dockerfile for RAG Voice AI

# Base image: Python 3.12 slim version (smaller size, no unnecessary packages)
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies:
# - curl: for health checks and downloading uv installer
# - Clean up apt cache to reduce image size
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv (Python package manager) from Astral's GitHub Container Registry
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv


# Copy Python dependency files first (to leverage Docker cache)
# This way, if only application code changes, Docker can reuse the layer with installed dependencies
COPY pyproject.toml uv.lock ./

# Install Python dependencies using uv:
# - --frozen: ensures uv.lock is respected (no changes to dependencies)
# - --no-cache: don't use pip cache to reduce image size
RUN uv sync --frozen --no-cache

# Copy entire application code
# Done after dependencies so code changes don't trigger dependency reinstall
COPY . .

# Create directory for application logs
RUN mkdir -p /app/logs

# Expose port 8001 (backend API port)
EXPOSE 8001

# Health check: AWS ECS will use this to verify container is healthy
# --interval=30s: check every 30 seconds
# --timeout=10s: fail if check takes >10 seconds
# --start-period=40s: give app 40 seconds to start before first check
# --retries=3: mark unhealthy after 3 failed checks
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Run uvicorn server:
# - main:app: run FastAPI app from main.py
# - --host 0.0.0.0: listen on all network interfaces (required in Docker)
# - --port 8001: listen on port 8001
# - --workers 1: use 1 worker process (increase for production)
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]