#!/bin/bash

set -e

echo "Starting Server"

echo $(date -u) "- Migrating"
python manage.py migrate

echo $(date -u) "- Collecting static"
python manage.py collectstatic --noinput

exec "$@"