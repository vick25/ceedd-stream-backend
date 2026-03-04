#!/usr/bin/env sh

set -e

python manage.py migrate --noinput

gunicorn ceedd_stream_api.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --timeout 180
