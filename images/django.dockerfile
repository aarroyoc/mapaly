FROM node:12.18.3 AS builder

WORKDIR /opt/intermap

COPY ./intermap/package.json .
COPY ./intermap/package-lock.json .

RUN npm install

COPY ./intermap/ .

RUN npm run build
RUN npm run bundle

FROM python:3.8.5

WORKDIR /opt/mapaly

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .

COPY --from=builder /opt/intermap/build/bundle.js /opt/mapaly/mapaly/static/
COPY --from=builder /opt/intermap/node_modules/leaflet/dist/leaflet.css /opt/mapaly/mapaly/static/
COPY --from=builder /opt/intermap/node_modules/leaflet/dist/leaflet.js /opt/mapaly/mapaly/static/

RUN python manage.py collectstatic --noinput

CMD ["uwsgi", "--socket", ":3031", "--module", "mapaly.wsgi"]
