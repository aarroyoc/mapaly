FROM node:12.18.1 AS builder

WORKDIR /opt/intermap

COPY package.json .
COPY package-lock.json .

RUN npm install

COPY . .

RUN npm run build

CMD npm run test