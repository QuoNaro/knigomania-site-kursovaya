#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
  echo "Waiting for postgres..."
  while ! nc -z book.db 5432; do
    sleep 0.1
  done
  echo "PostgreSQL started"
fi



python manage.py collectstatic --clear --noinput 
python manage.py makemigrations --noinput
python manage.py migrate --noinput
gunicorn --config gunicorn_config.py config.wsgi:application