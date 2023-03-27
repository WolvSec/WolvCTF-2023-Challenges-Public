FROM python:3.11

RUN python3 -m pip install flask gunicorn
RUN apt-get update && apt-get install -y gcc xxd

RUN mkdir -p /ctf/app
WORKDIR /ctf/app

COPY ./ ./

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0", "app:app"]