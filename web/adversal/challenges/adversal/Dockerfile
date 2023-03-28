FROM node:alpine

WORKDIR /ctf/app

RUN apk add --no-cache \
      chromium \
      nss \
      freetype \
      harfbuzz \
      ca-certificates \
      ttf-freefont \
      nodejs

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

ENV FLAG=wctf{mY_@d_1S_r3AlLY_sTyl1sh_1sNt_1T}
ENV SECRET=F7F58A55DF6FC757DD537586C5472

COPY ./package.json ./
COPY ./package-lock.json ./
RUN npm install

COPY ./ ./

EXPOSE 8080

# User
RUN addgroup -S ctf && adduser -S ctf -G ctf
USER ctf:ctf

CMD ["/bin/sh", "start.sh"]
