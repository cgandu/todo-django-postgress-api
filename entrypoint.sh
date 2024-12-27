#!/bin/sh

python manage.py makemigrations
python manage.py migrate

if [ "$DEBUG" = "False" ]; then
    echo "Production environment"
    
    python manage.py collectstatic --noinput


    gunicorn --bind 0.0.0.0:$DJANGO_PORT todoapp.wsgi:application
else
    echo "Development environment detected"
    
    python manage.py runserver $DJANGO_HOST:$DJANGO_PORT
fi
