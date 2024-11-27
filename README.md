# Eisenhower Matrix Task Management

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Django-based task management system implementing the Eisenhower Matrix methodology to help prioritize tasks based on their urgency and importance.

## What is the Eisenhower Matrix?

The Eisenhower Matrix, also known as the Urgent-Important Matrix, is a powerful decision-making and time management tool created by Dwight D. Eisenhower, the 34th President of the United States. As a highly accomplished individual who served as both a five-star general and president, Eisenhower was known for his exceptional ability to prioritize and make decisions effectively.

The matrix divides tasks into four quadrants based on two criteria: urgency and importance.

1. **Do First (Urgent & Important)**
   - Tasks that require immediate attention and have significant impact
   - Example: Deadline-driven projects, crisis management, pressing problems
   - Strategy: Handle these tasks immediately

2. **Schedule (Important, Not Urgent)**
   - Tasks that contribute to long-term goals but don't require immediate action
   - Example: Strategic planning, skill development, relationship building
   - Strategy: Schedule these tasks for later and give them adequate time

3. **Delegate (Urgent, Not Important)**
   - Tasks that need to be done soon but can be done by others
   - Example: Certain meetings, some emails, routine tasks
   - Strategy: Find the appropriate person to delegate these tasks to

4. **Don't Do (Not Urgent, Not Important)**
   - Tasks that don't contribute to your goals and aren't time-sensitive
   - Example: Time-wasters, excessive social media, non-priority activities
   - Strategy: Eliminate these tasks when possible

### Tips for Effective Use

1. **Be Honest**: Accurately assess both urgency and importance. Don't mark everything as urgent.
2. **Review Regularly**: Check your matrix daily and adjust task positions as priorities change.
3. **Focus on Quadrant 2**: Try to spend more time on important but not urgent tasks to prevent future crises.
4. **Limit Urgent Tasks**: Too many urgent tasks might indicate poor planning.
5. **Delegate Effectively**: Build a reliable network for delegation and trust others to handle tasks.
6. **Learn to Say No**: Use the matrix to justify declining non-priority tasks.

## Features

- Task organization using the Eisenhower Matrix (Important/Urgent quadrants)
- User authentication and authorization
- Admin interface for user management
- Responsive design with Tailwind CSS
- Docker support for easy deployment
- Rich task management features:
  - Quick view of task descriptions via modal
  - Detailed task view page with full information
  - Easy task editing and deletion
  - Drag-and-drop task organization between quadrants
  - Task completion tracking
  - Due date management with visual indicators
  - Markdown support for rich text formatting in descriptions

## Quick Start with Pre-built Image

The easiest way to run the application is using the pre-built Docker image from GitHub Container Registry.

1. Create a `docker-compose.yml` file:

```yaml
services:
  web:
    image: ghcr.io/kerk1v/eisenhower:latest
    ports:
      - "8000:8000"
    volumes:
      - sqlite_data:/data
    environment:
      - DJANGO_SETTINGS_MODULE=eisenhower_matrix.settings
      - PYTHONPATH=/app
      - GUNICORN_WORKERS=3
      - GUNICORN_TIMEOUT=120
      - SITE_URL=https://your-domain.com  # Set this to your actual domain
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

## Environment Variables

The following environment variables can be configured:

- `SITE_URL`: The base URL where the application is hosted (e.g., https://work.spainip.es)
- `GUNICORN_WORKERS`: Number of Gunicorn worker processes (default: 3)
- `GUNICORN_TIMEOUT`: Worker timeout in seconds (default: 120)
- `GUNICORN_MAX_REQUESTS`: Maximum requests per worker (default: 1000)

## Development Setup

If you want to develop or customize the application:

1. Clone the repository:
```bash
git clone https://github.com/kerk1v/eisenhower.git
cd eisenhower
```

2. Build and run with Docker Compose:
```bash
docker-compose up --build
```

## CORS and CSRF Configuration

The application automatically configures CORS and CSRF settings based on the `SITE_URL` environment variable:

- Both HTTP and HTTPS variants of the domain are allowed
- CORS is configured to allow credentials
- CSRF tokens are properly validated for the domain

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