FROM node:12.19.0 AS builder

WORKDIR /opt/intermap

COPY package.json .
COPY package-lock.json .

RUN npm install

COPY . .

RUN npm run build