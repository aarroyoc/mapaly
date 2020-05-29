FROM node:12.17.0

WORKDIR /opt/mapaly/mapaly/static/mapaly

RUN npm install -g eslint@7.1.0

COPY ./mapaly/static/mapaly/ .