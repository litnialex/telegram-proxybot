# Run as a Flask application
To run proxybot as a [Flask application](https://flask.palletsprojects.com/en/latest/) you will need a valid (may be self-signed) SSL certificate for HTTPS.

In example below we are creating a self-signed certificate valid for 10 years,
and later it will be used in `setWebhook` method.
```
HOST=proxybot.example.com
openssl req -newkey rsa:2048 -sha256 -nodes -keyout ssl/privkey.pem -x509 -days 3650 -out ssl/cert.pem -subj "/CN=${HOST}"
```

`HOST` variable must contain a real IP address or a fully qualified domain name used to reach the application.

If SSL certificate and key are not present in ./ssl foder, Flask will launch and listen on port 8080 without HTTPS. You can then use a reverse proxy like `nginx` to provide HTTPS.


## Run with Docker

This command will launch pre-built proxybot docker container.
```
TELEGRAM_ID=1234123123
DB_URI="mongodb+srv://***:**********@cluster0._______.mongodb.net/"
docker run --rm -p 8080:8080 -p 8443:8443 -v ./ssl:/app/ssl \
  -e TELEGRAM_ID=$TELEGRAM_ID -e DB_URI=$DB_URI litnialex/proxybot
```


## Run with Docker Compose

You may choose to build `proxybot` container locally, as well as to start a standard `mongodb` container and set `DB_URI=mongodb://mongodb` for `proxybot`. Check `docker-compose.yml` for details.

Provide your variables in `.env` file.
Check `.env.example` for the list of all accepted vars and their default values. Launch with command: `docker compose up`

## Register the webhook

The Telegram bot API method `setWebhook` must be called to start receiving updates from Telegram.

```
TOKEN=123456789:NeotobrAfMymceuwackTeunLiudsudjocoi
curl -F "url=${HOST}:8443/bot${TOKEN}" -F certificate=@ssl/cert.pem https://api.telegram.org/bot${TOKEN}/setWebhook
```

