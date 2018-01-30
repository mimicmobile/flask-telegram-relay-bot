FROM python:3.4.6
LABEL maintainer="Jeff Corcoran <jcorcoran+github@gmail.com>"
ARG BUILD_DATE
ARG VCS_REF

ENV DOCKER_BUILD_DATE=$BUILD_DATE
ENV DOCKER_VCS_REF=$VCS_REF

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.vcs-url="https://github.com/mimicmobile/flask-telegram-relay-bot.git" \
      org.label-schema.vcs-ref=$VCS_REF

RUN apt-get update; apt-get install -y openssl

COPY requirements.txt /usr/src/app/

RUN cd /usr/src/app && pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app

WORKDIR /usr/src/app

VOLUME /usr/src/app/certs

CMD [ "scripts/start.sh" ]