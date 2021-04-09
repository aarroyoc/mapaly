FROM node:14.16.1-alpine3.13 AS builder

WORKDIR /opt/intermap

COPY package.json .
COPY package-lock.json .

RUN npm install

COPY . .

RUN npm run build