FROM node:16.14.0-alpine3.14 AS builder

WORKDIR /opt/intermap

COPY ./intermap/package.json .
COPY ./intermap/package-lock.json .

RUN npm install

COPY ./intermap/ .

RUN npm run build && npm run bundle

FROM python:3.10.5

WORKDIR /opt/mapaly

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y gettext && \
    python -m pip install -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

COPY . .

COPY --from=builder /opt/intermap/build/bundle.js /opt/mapaly/mapaly/static/
COPY --from=builder /opt/intermap/node_modules/leaflet/dist/leaflet.css /opt/mapaly/mapaly/static/
COPY --from=builder /opt/intermap/node_modules/leaflet/dist/leaflet.js /opt/mapaly/mapaly/static/

RUN python manage.py collectstatic --noinput && \
    python manage.py compilemessages

CMD ["uwsgi", "--socket", ":3031", "--module", "mapaly.wsgi"]
