FROM node:16.14.0-alpine3.14 AS builder

WORKDIR /opt/intermap

COPY package.json .
COPY package-lock.json .

RUN npm install

COPY . .

RUN npm run build