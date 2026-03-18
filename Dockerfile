# ─────────────────────────────────────────────────────────────────
# Dockerfile — SA Bank Trust Score
# Packages the Streamlit app into a portable container.
# Author: Lindiwe Songelwa
# Org:    AZ400-DevOps-Portfolio
# ─────────────────────────────────────────────────────────────────

# ── Base image ────────────────────────────────────────────────────
# Using official Python 3.12 slim image — lightweight and secure
FROM python:3.12-slim

# ── Metadata ──────────────────────────────────────────────────────
LABEL maintainer="Lindiwe Songelwa"
LABEL project="SA Bank Trust Score"
LABEL description="Data-driven trust scoring system for South African banks"

# ── Set working directory ─────────────────────────────────────────
WORKDIR /app

# ── Install dependencies ──────────────────────────────────────────
# Copy requirements first — Docker caches this layer
# so it only reinstalls when requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Copy app files ────────────────────────────────────────────────
COPY app.py .
COPY pages/ ./pages/
COPY data/ ./data/

# ── Streamlit configuration ───────────────────────────────────────
# Disable the Streamlit "Deploy" button and telemetry
ENV STREAMLIT_TELEMETRY_DISABLED=true
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501

# ── Expose port ───────────────────────────────────────────────────
EXPOSE 8501

# ── Health check ─────────────────────────────────────────────────
# Docker will ping this endpoint to confirm the app is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# ── Run the app ───────────────────────────────────────────────────
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0"]