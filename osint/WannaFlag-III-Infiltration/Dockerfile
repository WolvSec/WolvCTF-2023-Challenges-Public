FROM node:19-bullseye-slim

RUN mkdir -p /ctf/app
WORKDIR /ctf/app
COPY ./package.json ./
COPY ./package-lock.json ./
RUN npm install

COPY ./index.js ./
COPY ./website ./website

EXPOSE 80

USER node
CMD ["node", "index.js"]
