# Multi-stage production Dockerfile for Retail Pricing Microservice
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final runtime image
FROM python:3.11-slim AS runner

WORKDIR /app

# Security: Create non-root system user
RUN addgroup --system appgroup && adduser --system --group appuser

# Copy installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH

# Copy application code
COPY src/ ./src/
COPY README.md .

# Switch to non-root user
USER appuser

# Expose FastAPI HTTP port
EXPOSE 8000

# Container healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run production Uvicorn ASGI server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
