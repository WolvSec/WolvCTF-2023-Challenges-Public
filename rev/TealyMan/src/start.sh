#!/bin/sh

node --experimental-fetch /ctf/app/deploy.js &
node /ctf/app/app.ts
