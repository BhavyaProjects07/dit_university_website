#!/usr/bin/env bash
# Install dependencies

set -0 errexit

pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
