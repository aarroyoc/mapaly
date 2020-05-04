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
