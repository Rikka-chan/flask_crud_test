#!/bin/sh

source app_env
python manage.py db migrate
python manage.py db upgrade

exec gunicorn -b :5000 --access-logfile - --error-logfile - run:app