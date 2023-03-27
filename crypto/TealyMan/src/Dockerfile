FROM alpine:latest AS builder

WORKDIR /temp

RUN apk add --no-cache nodejs npm python3 py3-pip python3-dev libffi-dev gcc musl-dev

COPY package.json tsconfig.json deploy.ts setup.ts requirements.txt contracts.py ./

RUN pip3 install --no-cache-dir --upgrade pip \
  && pip3 install --no-cache-dir -r requirements.txt

RUN npm install && rm -rf /temp/node_modules/algosms/node_modules

RUN mkdir -p build && python3 contracts.py

RUN node_modules/.bin/tsc && cd build && node setup.js && cd .. && rm -rf build/setup.js

FROM alpine:latest

RUN apk add --no-cache nodejs

WORKDIR /ctf/app

COPY --from=builder /temp/node_modules node_modules

COPY --from=builder /temp/build .

COPY app.ts start.sh ./

RUN chmod +x start.sh

ENTRYPOINT [ "/ctf/app/start.sh" ]
