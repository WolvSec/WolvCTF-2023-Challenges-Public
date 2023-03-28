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

ENV FLAG=wctf{n@w_My_aD_tRuLY_1S_sT1ylISH_dONT_yUO_tH1nK?}
ENV SECRET=E31DC62A206A0BBCC3B4BF94DCED0

COPY ./package.json ./
COPY ./package-lock.json ./
RUN npm install

COPY ./ ./

EXPOSE 8080

# User
RUN addgroup -S ctf && adduser -S ctf -G ctf
USER ctf:ctf

CMD ["/bin/sh", "start.sh"]
