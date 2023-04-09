FROM node:18.15.0-alpine3.17 AS builder

WORKDIR /opt/intermap

COPY ./intermap/package.json .
COPY ./intermap/package-lock.json .

RUN npm install

COPY ./intermap/ .

RUN npm run build && npm run bundle

FROM python:3.11.3

WORKDIR /opt/mapaly

RUN apt-get update && \
    apt-get install -y gettext && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install poetry==1.2.2

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry export -f requirements.txt | pip install -r /dev/stdin

COPY . .

COPY --from=builder /opt/intermap/build/bundle.js /opt/mapaly/mapaly/static/
COPY --from=builder /opt/intermap/node_modules/leaflet/dist/leaflet.css /opt/mapaly/mapaly/static/
COPY --from=builder /opt/intermap/node_modules/leaflet/dist/leaflet.js /opt/mapaly/mapaly/static/

RUN python manage.py collectstatic --noinput && \
    python manage.py compilemessages

CMD ["uwsgi", "--socket", ":3031", "--module", "mapaly.wsgi"]
