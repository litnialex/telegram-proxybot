# Run as a Flask application

To run proxybot as a [Flask application][flask] you will need a valid SSL certificate for HTTPS, which may be a self-signed certificate.

In example below we are creating a self-signed certificate valid for 10 years,
and later it will be used in `setWebhook` method.

```bash
HOST=proxybot.example.com
openssl req -newkey rsa:2048 -sha256 -nodes -keyout ssl/privkey.pem -x509 -days 3650 -out ssl/cert.pem -subj "/CN=${HOST}"
```

`HOST` variable must contain a real IP address or a fully qualified domain name for reaching the application from Telegram network.

If SSL certificate and key are not found in ./ssl folder application will launch anycase, but will accept HTTP at port 8080.
You must then use then another frontend web-server, like nginx, to accept HTTPS requests from Telegram network and pass them to the application.


## Run with Docker

This command will launch pre-built proxybot docker container.
```bash
TELEGRAM_ID=1234123123
DB_URI="mongodb+srv://***:**********@cluster0._______.mongodb.net/"
docker run --rm -p 8080:8080 -p 8443:8443 -v ./ssl:/app/ssl \
  -e TELEGRAM_ID=$TELEGRAM_ID -e DB_URI=$DB_URI litnialex/proxybot
```


## Run with Docker Compose

You may choose to build `proxybot` container locally, as well as to start a standard `mongodb` container and set `DB_URI=mongodb://mongodb`. Check `docker-compose.yml` in [repository][repo] root folder for details.

Provide your variables in `.env` file.
Check `.env.example` for the list of all accepted vars and their default values.

Launch with command: 
```bash
docker compose up
```

## Register the webhook

The Telegram bot API method [setWebhook] must be called to start receiving updates from Telegram.

```bash
TOKEN=123456789:NeotobrAfMymceuwackTeunLiudsudjocoi
curl -F "url=${HOST}:8443/bot${TOKEN}" -F certificate=@ssl/cert.pem https://api.telegram.org/bot${TOKEN}/setWebhook
```

Additionally, you may define an API_SECRET variable to prevent unauthorized webhook calls.
For that, define AP_SECRET variable and add ```-F secret_token=${API_SECRET}``` in last command.

You may run multiple bots within the same application.
Just repeat last step for each of your bots.


[flask]: https://flask.palletsprojects.com/en/latest/
[repo]: https://github.com/litnialex/telegram-proxybot
[setWebhook]: https://core.telegram.org/bots/api#setwebhook