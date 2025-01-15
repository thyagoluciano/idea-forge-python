# --- Stage 1: Builder Stage ---
FROM python:3.11-alpine3.19 AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache gcc musl-dev build-base

# Copy only requirements file
COPY requirements.txt .

# Upgrade pip and setuptools
RUN pip install --no-cache-dir --upgrade pip setuptools

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


# --- Stage 2: Final Stage ---
FROM python:3.11-alpine3.19

WORKDIR /app

# Copy application from builder stage
COPY --from=builder /app /app

# Copy source code
COPY . .

# Remove unnecessary files
RUN rm -rf __pycache__ && \
    find . -name "*.pyc" -delete && \
    find . -name "*.pyo" -delete

# Run application
CMD ["python", "src/main.py"]