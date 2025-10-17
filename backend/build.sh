#!/usr/bin/env bash
# exit on error
set -o errexit

# Install system dependencies for psycopg2
apt-get update
apt-get install -y libpq-dev gcc

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate --no-input
