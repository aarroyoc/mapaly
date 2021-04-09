FROM node:14.16.1-alpine3.13 AS builder

WORKDIR /opt/intermap

COPY ./intermap/package.json .
COPY ./intermap/package-lock.json .

RUN npm install

COPY ./intermap/ .

RUN npm run build
RUN npm run bundle

FROM python:3.9.4

WORKDIR /opt/mapaly

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
ENV DISPLAY=:99

RUN python -m pip install poetry

COPY . .

COPY --from=builder /opt/intermap/build/bundle.js /opt/mapaly/mapaly/static/
COPY --from=builder /opt/intermap/node_modules/leaflet/dist/leaflet.css /opt/mapaly/mapaly/static/
COPY --from=builder /opt/intermap/node_modules/leaflet/dist/leaflet.js /opt/mapaly/mapaly/static/

RUN poetry install --no-root

RUN poetry run python manage.py collectstatic --noinput

ENTRYPOINT ["poetry", "run"]