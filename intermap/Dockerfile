FROM node:12.18.1 AS builder

WORKDIR /opt/intermap

COPY package.json .
COPY package-lock.json .

RUN npm install

COPY . .

RUN npm run build
RUN npm run test
RUN npm run bundle

FROM nginx:1.19.0

WORKDIR /opt/intermap

EXPOSE 1144

COPY --from=builder /opt/intermap/build/bundle.js ./bundle.js
COPY --from=builder /opt/intermap/main.css .
COPY --from=builder /opt/intermap/node_modules/leaflet/dist/leaflet.css .
COPY --from=builder /opt/intermap/node_modules/leaflet/dist/leaflet.js .
COPY nginx.conf /etc/nginx/conf.d/default.conf
