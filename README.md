# Telegram Relay Bot

[![Docker Automated build](https://img.shields.io/docker/automated/mimicmobile/flask-telegram-relay-bot.svg)](https://hub.docker.com/r/mimicmobile/flask-telegram-relay-bot/)
[![Docker Stars](https://img.shields.io/docker/stars/mimicmobile/flask-telegram-relay-bot.svg)](https://hub.docker.com/r/mimicmobile/flask-telegram-relay-bot/)
[![Docker Pulls](https://img.shields.io/docker/pulls/mimicmobile/flask-telegram-relay-bot.svg)](https://hub.docker.com/r/mimicmobile/flask-telegram-relay-bot/)
[![](https://images.microbadger.com/badges/image/mimicmobile/flask-telegram-relay-bot.svg)](https://microbadger.com/images/mimicmobile/flask-telegram-relay-bot "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/commit/mimicmobile/flask-telegram-relay-bot.svg)](https://microbadger.com/images/mimicmobile/flask-telegram-relay-bot "Get your own commit badge on microbadger.com")

This bot acts as a relay between an existing service and Telegram.  It listens for a unique `POST` `JSON` request from a service and relays (via Webhooks) that message to your Telegram chat(s) of choice.

A bot token is **required** and can be obtained by messaging [@BotFather](https://telegram.me/BotFather).

## Configuration
This bot uses environment variables to configure and run.  At the minimum, `HOST`, `SOURCE_TOKEN` and `TOKEN` are required.

### Variables
* HOST (**required**) - The FQDN/IP your bot is listening on
* POST (default: 8443)
* SOURCE_TOKEN (**required**) - A unique token of any length that **you** define
* TOKEN (**required**) - Telegram bot token
* PERMANENT_CHATS - A comma separated string of chat IDs you want your bot to always send messages to
* OWNER_ID - Your (owner) telegram id (get ids for `PERMANENT_CHATS` and `OWNER_ID` by messaging [@RawDataBot](https://telegram.me/RawDataBot))
* ADMIN_LEVEL (default: 1) - Determines can control the bot.
  * 1=Channel admins + Owner
  * 2=Channel admins
  * 3=Owner only
* DEBUG (default: 0) - If set to 1, will enable Flask debug logging

### Environment file
The easiest method is to place the above variables you're using in a `variables.env` file.

## API spec
This bot listens on a `https://HOST:PORT/SOURCE_TOKEN` for a `POST` request with a `JSON` string body.  _HTML tags are supported_.
At the moment the only field parsed from the JSON object is `message`.

**IMPORTANT**
 
   Telegram requires Webhooks to be received over `HTTPS`! **This means we're creating and using self-signed certs**.  This is all taken care for you when the bot starts.  Beware that you may need to grab the public cert from the `certs/` directory (locally or inside the docker container) depending on how you're sending your `POST request` from your service.

### curl example
```bash
curl -k -X POST -d '{ "message": "Hello world!" }' https://HOST:PORT/SOURCE_TOKEN
```
### JSON body example with HTML
```json
{ "message": "<b>Alice</b> updated Client <b>XDA Developers</b> account permissions: <code>ADDRESS</code>" }
```

## Connecting services
Having your service deliver `HTTP POST requests` can be done many ways.  If you're using Python or Django, one such way could be to use the [Python logging facility](https://docs.python.org/3/library/logging.html).

Using this fork of the [Python Logging Loggly Handler](https://github.com/mimicmobile/loggly-python-handler), you can see how a logger would be configured in `Python` / `Django`.
Regardless of how you're sending your requests, your URL is always https://`HOST`:`PORT`/`SOURCE_TOKEN`

## Install
_The recommended usage is through Docker._  To install locally clone and install the python requirements:
```bash
git clone https://github.com/mimicmobile/flask-telegram-relay-bot
pip install -r requirements.txt
```

## Usage
*Add necessary variables to `variables.env` file*
### Docker
```bash
docker run --env-file variables.env --name telegram-bot -p 8443:8443 mimicmobile/flask-telegram-relay-bot
```
### Locally
```bash
./scripts/start.sh
```

## Bot commands
The following commands are currently available:
* `/register` - Registers channel/group to receive relay messages
* `/unregister` - Unregister channel.  Bot will leave
* `/mute` - Mute output in _all_ channels
* `/unmute` - Unmute output
* `/about` - About this bot

## Thanks
This bot was heavily influenced by [this gist](https://gist.github.com/leandrotoledo/4e9362acdc5db33ae16c) by [leandrotoledo](https://github.com/leandrotoledo)
