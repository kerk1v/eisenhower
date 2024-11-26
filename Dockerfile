# Use Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV NODE_MAJOR 20

# Set work directory
WORKDIR /app

# Install system dependencies including Node.js
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_${NODE_MAJOR}.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

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

# Create entrypoint script
RUN echo '#!/bin/sh\n\
python manage.py migrate\n\
python manage.py setup_groups\n\
python manage.py create_admin_user\n\
python manage.py collectstatic --noinput\n\
gunicorn eisenhower_matrix.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS:-3} \
    --timeout ${GUNICORN_TIMEOUT:-120} \
    --max-requests ${GUNICORN_MAX_REQUESTS:-1000} \
    --access-logfile - \
    --error-logfile - \
    --reload\n\
' > /app/entrypoint.sh \
&& chmod +x /app/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]