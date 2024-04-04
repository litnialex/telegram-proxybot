# Run proxybot as a serverless function

Here is an example of how to launch proxybot in Google [Cloud Functions][cf] with `gcloud` command:
```
TELEGRAM_ID=1234123123
DB_URI="mongodb+srv://***:**********@cluster0._______.mongodb.net/"
REGION=europe-west1
gcloud functions deploy --gen2 --region=$REGION --runtime=python310 \
    --trigger-http --entry-point=entrypoint --allow-unauthenticated \
	--set-env-vars=TELEGRAM_ID=$TELEGRAM_ID,DB_URI=$DB_URI \
	--source=proxybot/ proxybot
```

This command, run from the [repository][repo] root folder, will upload contents of `proxybot` subfolder as a function named `proxybot`.


## Register the webhook

The Telegram bot API method [setWebhook] must be called to start receiving updates from Telegram.
```
CLOUD_URL=https://***********.cloudfunctions.net/proxybot
TOKEN=123456789:NeotobrAfMymceuwackTeunLiudsudjocoi
curl -F "url=${CLOUD_URL}/bot${TOKEN}" https://api.telegram.org/bot${TOKEN}/setWebhook
```

Replace `TELEGRAM_ID`, `DB_URI`, `REGION`, `CLOUD_URL`, `TOKEN` variable values with your data.

[cf]: https://cloud.google.com/functions
[repo]: https://github.com/litnialex/telegram-proxybot
[setWebhook]: https://core.telegram.org/bots/api#setwebhook
