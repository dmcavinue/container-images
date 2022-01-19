FROM node:16.13.2-alpine

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

RUN apk update && apk add --no-cache chromium

RUN mkdir /app
WORKDIR /app

COPY package.json .
COPY server.js .

RUN npm install

CMD ["node", "server.js"]