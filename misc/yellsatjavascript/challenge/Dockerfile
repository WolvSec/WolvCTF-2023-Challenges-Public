FROM node:19-bullseye-slim as chroot

RUN /usr/sbin/useradd --no-create-home -u 2000 user

COPY chall.js /home/user/

FROM gcr.io/kctf-docker/challenge@sha256:d884e54146b71baf91603d5b73e563eaffc5a42d494b1e32341a5f76363060fb

COPY --from=chroot / /chroot

COPY nsjail.cfg /home/user/

CMD kctf_setup && \
    kctf_drop_privs \
    socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"kctf_pow nsjail -E flag='wctf{javascript_!==_java}' -C /home/user/nsjail.cfg -- /usr/local/bin/node /home/user/chall.js"
