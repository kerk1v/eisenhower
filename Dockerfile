# Use Python Alpine base image
FROM python:3.11-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV NODE_MAJOR 20

# Set work directory
WORKDIR /app

# Install system dependencies and Node.js
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    curl \
    nodejs \
    npm \
    dos2unix \
    && rm -rf /var/cache/apk/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Install Node.js dependencies and build CSS
RUN npm install
RUN npm run build

# Create data directory for SQLite
RUN mkdir -p /data

# Fix line endings and set permissions
RUN dos2unix /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]