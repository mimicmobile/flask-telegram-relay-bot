#!/bin/bash

DIR=$(echo $PWD | sed 's/\/scripts//')  # Strip off scripts/ dir if we're in there
cd $DIR

if [ -e "./variables.env" ]; then
  set -a; . ./variables.env
fi

./scripts/generate_ssl_cert.sh

# Setup default port
if [ -z "$PORT" ]; then
  PORT=8443
fi

if [[ -z "$HOST" || -z "$TOKEN" || -z "SOURCE_TOKEN" ]]; then
  echo ""
  echo "You MUST launch this docker container with at least the follow env variables:"
  echo ""
  echo "  HOST (Your FQDN that Telegram connects to for webhook events)"
  echo "  TOKEN (Your telegram generated token from BotFather)"
  echo "  SOURCE_TOKEN (A token of your choosing that your source connects to to relay)"
  echo ""
  echo "i.e. HOST=example.com TOKEN=ASHFL:KU296_DSAFKLAH90 SOURCE_TOKEN=ABC1234"
  echo "     Your source would send JSON payloads to https://example.com:8443/ABC1234"
  echo "     Telegram would send webhook events to https://example.com:8443/ASHFL:KU296_DSAFKLAH90"
  echo ""
  exit
fi

echo ""
echo "Send POST requests to:"
echo ""
echo "  https://$HOST:$PORT/$SOURCE_TOKEN"
echo ""
echo "  Test using curl:"
echo "  $ curl -k -X POST -d '{\"message\": \"Hello world!\"}' https://$HOST:$PORT/$SOURCE_TOKEN"
echo ""

cd bot && \
gunicorn \
  -w 1 \
  -k gevent \
  --keyfile ../certs/key.pem \
  --certfile ../certs/cert.pem \
  -e SOURCE_TOKEN=$SOURCE_TOKEN \
  -e HOST=$HOST \
  -e CERT=../certs/cert.pem \
  -e TOKEN=$TOKEN \
  -b 0.0.0.0:$PORT \
  main:app

cd ..