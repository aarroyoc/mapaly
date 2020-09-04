# mapaly
Mapaly is an educational geography website

## Development

```
poetry install --no-root
poetry shell
> python manage.py runserver
```

If you want to update packages:
```
poetry update
poetry export -frequirements.txt > requirements.txt
```

If you modify the models:
```
> python manage.py makemigrations
> python manage.py migrate
```

## Local Testing

Docker:
```
docker-compose -f docker-compose.yml -f docker-compose.test.yml run django-test

```
Local (with Chromium/ChromeDriver installed):
On Intermap:
```
npm run build
npm run bundle
npm run test
```
On Root:
```
cp intermap/build/bundle.js mapaly/static/
cp intermap/node_modules/leaflet/dist/leaflet.css mapaly/static/
cp intermap/node_modules/leaflet/dist/leaflet.js mapaly/static/
flake8 --ignore=E501
mypy . --ignore-missing-imports
python manage.py test
```

## Run app local
```
docker-compose up
```
