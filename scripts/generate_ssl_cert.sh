#!/bin/bash

DIR=$(echo $PWD | sed 's/\/scripts//')  # Strip off scripts/ dir if we're in there

if [ ! -e "$DIR/certs/cert.pem" ] || [ ! -e "$DIR/certs/key.pem" ]
then

  if [ -z "$HOST" ]; then
    echo "No \$HOST env var defined.  Cannot generate SSL cert!!"
    exit
  fi

  [ -d $DIR/certs ] || mkdir $DIR/certs
  echo ">> generating self signed cert"
  openssl req -x509 -newkey rsa:4086 \
  -subj "/C=XX/ST=XXXX/L=XXXX/O=XXXX/CN=${HOST}" \
  -keyout "$DIR/certs/key.pem" \
  -out "$DIR/certs/cert.pem" \
  -days 3650 -nodes -sha256
fi