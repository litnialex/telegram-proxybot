# Запуск proxybot в качестве serverless функции

Вот пример того, как запустить proxybot в Google [Cloud Functions][cf] с помощью команды `gcloud`:
```
TELEGRAM_ID=1234123123
DB_URI="mongodb+srv://***:**********@cluster0._______.mongodb.net/"
REGION=europe-west1
gcloud functions deploy --gen2 --region=$REGION --runtime=python310 \
    --trigger-http --entry-point=entrypoint --allow-unauthenticated \
	--set-env-vars=TELEGRAM_ID=$TELEGRAM_ID,DB_URI=$DB_URI \
	--source=proxybot/ proxybot
```

Эта команда, запущенная из корневой папки репозитория, загрузит содержимое подпапки `proxybot` как функцию с именем `proxybot`.


## Регистрация webhook
Для начала получения сообщений от Telegram необходимо вызвать Telegram Bot API метод [setWebhook].

```
CLOUD_URL=https://***********.cloudfunctions.net/proxybot
TOKEN=123456789:NeotobrAfMymceuwackTeunLiudsudjocoi
curl -F "url=${CLOUD_URL}/${TOKEN}" https://api.telegram.org/bot${TOKEN}/setWebhook
```

Замените значения переменных `TELEGRAM_ID`, `DB_URI`, `REGION`, `CLOUD_URL`, `TOKEN` на ваши данные.


[cf]: https://cloud.google.com/functions
[setWebhook]: https://core.telegram.org/bots/api#setwebhook
