FROM python:3.4.6
MAINTAINER mimicmobile

# nginx

RUN apt-get update; apt-get install -y openssl

COPY requirements.txt /usr/src/app/

RUN cd /usr/src/app && pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app

WORKDIR /usr/src/app

VOLUME /usr/src/app/certs

CMD [ "scripts/start.sh" ]