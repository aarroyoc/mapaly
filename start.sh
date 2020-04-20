python manage.py collectstatic --noinput
python manage.py migrate
uwsgi --socket :3031 --module mapaly.wsgi