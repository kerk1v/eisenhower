#!/bin/sh
python manage.py migrate
python manage.py setup_groups
python manage.py create_admin_user
python manage.py collectstatic --noinput
gunicorn eisenhower_matrix.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS:-3} \
    --timeout ${GUNICORN_TIMEOUT:-120} \
    --max-requests ${GUNICORN_MAX_REQUESTS:-1000} \
    --access-logfile - \
    --error-logfile - \
    --reload