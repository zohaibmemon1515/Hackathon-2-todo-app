# syntax=docker/dockerfile:1

FROM python:3.13-slim AS base

WORKDIR /app

# Install system dependencies needed for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends gcc curl \
    && rm -rf /var/lib/apt/lists/*

FROM base AS builder

# Copy requirements and pyproject.toml first for dependency caching
COPY --link requirements.txt ./
COPY --link pyproject.toml ./

# Create virtual environment and install dependencies using pip cache
RUN python -m venv .venv \
    && .venv/bin/pip install -r requirements.txt

# Copy the rest of the application code (excluding files in .dockerignore)
COPY --link . .

FROM base AS final

# Create non-root user and group for security
RUN addgroup --system appgroup && adduser --system --group appuser

WORKDIR /app

# Copy the virtual environment and application code from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app /app

# Set PATH to use the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

USER appuser

# Healthcheck for FastAPI /health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
