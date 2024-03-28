# Запуск в качестве приложения Flask

Для запуска proxybot в качестве [приложения Flask](https://flask.palletsprojects.com/en/latest/) вам понадобится действительный (может быть самоподписанный) SSL-сертификат для HTTPS.

В приведенном ниже примере мы создаем самоподписанный сертификат, действительный на 10 лет, который затем будет использоваться в методе [setWebhook](file:///home/sasha/dev/telegram-proxybot/docs/ru/Telegram-Bot-Flask.md#6%2C31-6%2C31).

```bash
HOST=proxybot.example.com
openssl req -newkey rsa:2048 -sha256 -nodes -keyout ssl/privkey.pem -x509 -days 3650 -out ssl/cert.pem -subj "/CN=${HOST}"
```

Переменная `HOST` должна содержать реальный IP-адрес или полностью определенное доменное имя, используемое для доступа к приложению.

Если SSL-сертификат и ключ отсутствуют в папке `./ssl`, Flask запустится и будет слушать порт 8080 без HTTPS. Затем вы можете использовать обратный прокси, такой как `nginx`, чтобы предоставить HTTPS.


## Запуск с помощью Docker
Эта команда запустит предварительно собранный контейнер docker proxybot.

```bash
TELEGRAM_ID=1234123123
DB_URI="mongodb+srv://***:**********@cluster0._______.mongodb.net/"
docker run --rm -p 8080:8080 -p 8443:8443 -v ./ssl:/app/ssl \
  -e TELEGRAM_ID=$TELEGRAM_ID -e DB_URI=$DB_URI litnialex/proxybot
```


## Запуск с помощью Docker Compose
Вы можете выбрать локальное создание контейнера `proxybot`, а также запустить стандартный контейнер `mongodb` и установить `DB_URI=mongodb://mongodb` для `proxybot`. Проверьте `docker-compose.yml` для получения дополнительной информации.

Укажите ваши переменные в файле `.env`.
Проверьте `.env.example` для получения списка всех принимаемых переменных и их значений по умолчанию. Запустите с помощью команды: `docker compose up`

# Регистрация вебхука
Метод API Telegram бота `setWebhook` должен быть вызван для начала получения сообщений от Telegram.

```bash
TOKEN=123456789:NeotobrAfMymceuwackTeunLiudsudjocoi
curl -F "url=${HOST}:8443/bot${TOKEN}" -F certificate=@ssl/cert.pem https://api.telegram.org/bot${TOKEN}/setWebhook
```

