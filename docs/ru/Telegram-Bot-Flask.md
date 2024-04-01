# Запуск в качестве приложения Flask

Для запуска proxybot в качестве [приложения Flask][flask] вам понадобится действительный (может быть самоподписным) SSL-сертификат для HTTPS.

В приведенном ниже примере мы создаем самоподписный сертификат, действительный 10 лет, который позже используем в методе `setWebhook`.

```bash
HOST=proxybot.example.com
openssl req -newkey rsa:2048 -sha256 -nodes -keyout ssl/privkey.pem -x509 -days 3650 -out ssl/cert.pem -subj "/CN=${HOST}"
```

Переменная `HOST` должна содержать реальный IP-адрес или полное доменное имя, используемое для доступа к приложению из сети Telegram.

Если SSL-сертификат и ключ отсутствуют в папке `./ssl`, приложение все-равно запустится и будет принимать HTTP запросы на порту 8080. Тогда нужно организовать приём HTTPS запросов из сети Телеграм другим способом, например Nginx-сервером, и проксировать их в приложение.


## Запуск с помощью Docker
Эта команда запустит предварительно собранный контейнер docker proxybot.

```bash
TELEGRAM_ID=1234123123
DB_URI="mongodb+srv://***:**********@cluster0._______.mongodb.net/"
docker run --rm -p 8080:8080 -p 8443:8443 -v ./ssl:/app/ssl \
  -e TELEGRAM_ID=$TELEGRAM_ID -e DB_URI=$DB_URI litnialex/proxybot
```


## Запуск с помощью Docker Compose
Вы можете выбрать локальное создание контейнера `proxybot`, а также запустить стандартный контейнер `mongodb` и установить `DB_URI=mongodb://mongodb` для `proxybot`. Проверьте `docker-compose.yml` в корневой папке [репозитория][repo] для получения дополнительной информации.

Укажите ваши переменные в файле `.env`.
Проверьте `.env.example` для получения списка всех принимаемых переменных и их значений по умолчанию. Запустите с помощью команды: `docker compose up`


## Регистрация вебхука
Метод API Telegram бота `setWebhook` должен быть вызван для начала получения сообщений от Telegram.

```bash
TOKEN=123456789:NeotobrAfMymceuwackTeunLiudsudjocoi
curl -F "url=${HOST}:8443/bot${TOKEN}" -F certificate=@ssl/cert.pem https://api.telegram.org/bot${TOKEN}/setWebhook
```

Можно дополнительно задать переменную API_SECRET и укзать её в webhook. Для этого команде `curl` добавляется опция ```-F secret_token=${API_SECRET}```. Тогда неавторизованные запросы будут игнорироваться.

Возможна обработка запросов на разные proxybot'ы одним и тем же приложением. Для этого просто повторяйте регистрацию webhook для каждого из бота, соответственно изменяя значение переменной `TOKEN`.

[flask]: https://flask.palletsprojects.com/en/latest/
[repo]: https://github.com/litnialex/telegram-proxybot
