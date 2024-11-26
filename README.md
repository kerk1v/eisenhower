# Eisenhower Matrix Task Management

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Django-based task management system implementing the Eisenhower Matrix methodology to help prioritize tasks based on their urgency and importance.

## Features

- Task organization using the Eisenhower Matrix (Important/Urgent quadrants)
- User authentication and authorization
- Admin interface for user management
- Responsive design with Tailwind CSS
- Docker support for easy deployment

## Quick Start with Pre-built Image

The easiest way to run the application is using the pre-built Docker image from GitHub Container Registry.

1. Create a `docker-compose.yml` file:

```yaml
services:
  web:
    image: ghcr.io/volkerkerkhoff/eisenhower:latest
    ports:
      - "8000:8000"
    volumes:
      - sqlite_data:/data
    environment:
      - DJANGO_SETTINGS_MODULE=eisenhower_matrix.settings
      - PYTHONPATH=/app
      - GUNICORN_WORKERS=3
      - GUNICORN_TIMEOUT=120
    restart: unless-stopped

volumes:
  sqlite_data:
    driver: local
```

2. Start the application:

```bash
docker-compose up -d
```

3. Access the application at http://localhost:8000

Default admin credentials:
- Username: admin
- Password: adminpassword

## Development Setup

If you want to develop or customize the application:

1. Clone the repository:
```bash
git clone https://github.com/volkerkerkhoff/eisenhower.git
cd eisenhower
```

2. Build and run with Docker Compose:
```bash
docker-compose up --build
```

## Environment Variables

The following environment variables can be configured:

- `GUNICORN_WORKERS`: Number of Gunicorn worker processes (default: 3)
- `GUNICORN_TIMEOUT`: Worker timeout in seconds (default: 120)
- `GUNICORN_MAX_REQUESTS`: Maximum requests per worker (default: 1000)

## Building and Publishing

The project includes GitHub Actions workflow for automated builds. To publish a new version:

1. Tag a new version:
```bash
git tag v1.0.0
git push origin v1.0.0
```

2. The workflow will automatically build and push the image to GitHub Container Registry with both `latest` and version tags.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2024 Volker Kerkhoff