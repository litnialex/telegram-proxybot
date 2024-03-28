Proxybot is a [Telegram](https://www.telegram.org) bot which forwards all incoming messages to the owner or into a telegram group, specified by the owner.
This group can also be a supergroup with threads (topics).

Replies are done simply texting back in the chat. Such messages always go to the last contact in  that chat.
Of course you can select any message and reply to that specific message.

Sound, video and all other media formats supported by Telegram can be proxied in this manner.

Proxybot provides full privacy for your personal telegram account and allows handling messages in teams.

Check yourself.

## Run proxybot as a service
Our bot [@InitProxybot](https://t.me/InitProxybot) can launch your proxybot in the cloud within seconds.

This is offered as a service from our team with an annual subscription fee of $20.

You get 4 months for free, prepay is not required.

## Launch by your own

Proxybot can be launched as a [serverless function](telegram-bot-serverless.md)  or as a [Flask applicaiton](telegram-bot-Flask.md).

In this case you will need to supply a working MongoDB connection,
which is used to store proxybot settings and connections tracking information.
You may start with [MongoDB Atlas](https://www.mongodb.com/docs/atlas/) free tier.

`TELEGRAM_ID` variable must contain the ID of the Telegram account  assigned "proxybot owner" privilege.
If you want to find out your telegram ID ask [@my_id_bot ](https://t.me/my_id_bot)


## Running multiple bots at once

You can run multiple proxybots with the same `TELEGRAM_ID` and `DB_URI` settings at once for many bots.
Just repeat the step to register webhook for each of your bots, replacing `TOKEN` with the token of each of the bots you want to run.

## Security considerations

Proxybot is designed with respect to your privacy and with security in mind. All messages are proxied in real-time and are not stored in any form. Only minimum required tracking data is stored to reliably provide proxy functionality.

`TOKEN` value is not stored anywhere in the database. Proxybot receives it as a part of the webhook URL and uses it while running to make requests to Telegram network.

`TELEGRAM_ID` is used to identify the owner of the bot and is stored in the database. It is used to send notification messages to the owner and to allow the owner to control the bot.

You may also define an API_SECRET variable to protect your bot from unauthorized access. In this case, when registering the webhook, you add ```-F secret_token=${API_SECRET}``` to the curl command.

## Support

If you have any questions or need help, please contact us in Telegram [@devproxybot](https://t.me/devproxybot)

