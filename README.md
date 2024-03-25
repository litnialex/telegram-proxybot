# How it works

Proxybot is a telegram bot which forwards all incoming messages to the owner or into a telegram group, specified by the owner. Telegram group can also be a supergroup with threads (topics).

Replies are done simply texting back in the chat. Such messages always go to the last contact in  that chat. Of course you can select any message and reply to that specific message.

Sound, video and all other media formats supported by Telegram can be proxied in this manner.

Proxybot provides full privacy for your personal telegram account and allows handling messages in teams. 

Check yourself.

# Run proxybot as a service
The easest way to check how proxybot works is through 2 simple steps:
1. Get your bot's API token from @botFather
2. Go to @cloudrunbot, run /newbot and insert the API token of your bot

Every bot registration gets a few months of free service and in the meanwhile you can activate suscription or choose to launch by your own.

# Launch by your own
Proxybot can be launched as a serverless function, as a docker container or as a Flask applicaiton. 

In any of this scenarios you will  need to supply a working MongoDB connection and populate it through `DB_URI` variable. MongoDB is used to store proxybot settings and connections tracking information. You may start with [[https://www.mongodb.com/docs/atlas/|MongoDB Atlas]] free tier.

`TELEGRAM_ID` variable should have as value the ID of a Telegram account  assigned "proxybot owner" privilege. It doesn't need to be the same as bot's API token owner, and, by the way, it is impossible to find out which Telegram account is owning a bot.

## Launch as a serverless function
Here is an example how to launch in Google Functions using Google's `gcloud` command:
```
TELEGRAM_ID=1234123123
DB_URI="mongodb+srv://***:**********@cluster0._______.mongodb.net/"
REGION=europe-west1
gcloud functions deploy --gen2 --runtime=python310 --trigger-http \
	--entry-point=entrypoint --allow-unauthenticated \
	--set-env-vars=TELEGRAM_ID=${TELEGRAM_ID},DB_URI=${DB_URI} \
	--source=proxybot/ proxybot
```

This command, run from the repository root folder, will upload contents of `proxybot` subfolder into Google Functions with name `proxybot`.

Lastly a `setWebhook` bot API method should be called to start receiving updates from Telegram by serverless function. 
```
CLOUD_URL=https://***********.cloudfunctions.net/proxybot
TOKEN=123456789:NeotobrAfMymceuwackTeunLiudsudjocoi
curl -F "url=${CLOUD_URL}/bot${TOKEN}" https://api.telegram.org/bot${TOKEN}/setWebhook
```

Replace TELEGRAM_ID, DB_URI, REGION, CLOUD_URL, TOKEN values from these examples with your data.

## Launch in Docker
You can build and launch proxybot in Docker container.

Docker running host must have an IP address or a Fully Qualified Domain Name reachable globally set as `HOST` variable
```
HOST=proxybot.example.com
```


And SSL certificate for HTTPS. In this example we are creating a self-signed certificate valid for 10 years, and later it will be used in `setWebhook` method.
```
openssl req -newkey rsa:2048 -sha256 -nodes -keyout ssl/privkey.pem -x509 -days 3650 -out ssl/cert.pem -subj "/CN=${HOST}"
```

Run locally `mongodb` and `proxybot` containers
```
TELEGRAM_ID=1234123123
docker compose up
```

This builds `proxybot` container and uses standard `mongo:latest` container to provide a working MongoDB  connection available as ```DB_URI=mongodb://mongodb``` from inside `proxybot` container. Refer to `docker-compose.yml` for details.

Finally, register webhook
```
TOKEN=123456789:NeotobrAfMymceuwackTeunLiudsudjocoi
curl -F "url=${HOST}:8443/bot${TOKEN}" -F certificate=@ssl/cert.pem https://api.telegram.org/bot${TOKEN}/setWebhook
```

It's recommended to set your variables in `.env` file. Check `.env.example` for the list of all accepted vars and their default values.

