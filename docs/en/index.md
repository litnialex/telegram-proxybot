Proxybot is a [Telegram] bot which forwards all incoming messages to the owner
or into a telegram group, specified by the owner.
This group can also be a supergroup with topics.

Replies are done simply texting back in the chat.
Such messages always go to the last contact in  that chat.
Of course, you can reply to any specific message in chat history
by pressing "Reply" link in that message.

Voice-messages, video-messages, files and any other media format
supported by Telegram can be proxied in this manner.

*Proxybot assists teams and individuals in managing public communications through their personal Telegram accounts.*


## Use proxybot as a service
This bot: [@InitProxybot] can launch your proxybot in the cloud within seconds.

This is offered as a service from proxybot developer with an annual subscription fee of $20.

You get 4 months of free usage, prepay is not required.

*It's extremely easy to start using proxybot.*


## Launch by your own

Proxybot can be launched as a [serverless function] or as a [Flask application].

In this case you will need to provide a valid MongoDB connection.
You may start with [MongoDB Atlas] free tier.

`TELEGRAM_ID` variable must contain the ID of the Telegram account assigned
"proxybot owner" privilege.
Only this account will be able to control bot via commands.
If you want to find out your telegram ID ask [@my_id_bot].


## Security considerations

Proxybot is designed with respect to personal privacy and security in mind.
The source code of the bot is 100% open and free.
When you use our service to run proxybot we take the responsability to run
exactly the same code, which is published in the [repository].

`TOKEN` value is not stored anywhere in the database.
Proxybot receives it as part of the webhook URL
and uses it only until finishing handling the incoming request.


## Feedback

Contact [@devproxybot] for any questions or feedback.


[serverless function]: Telegram-Bot-Serverless.md
[Flask application]: Telegram-Bot-Flask.md
[@InitProxybot]: https://t.me/InitProxybot
[@my_id_bot]: https://t.me/my_id_bot
[@devproxybot]: https://t.me/devproxybot
[Telegram]: https://www.telegram.org
[MongoDB Atlas]: https://www.mongodb.com/docs/atlas/
[repository]: https://github.com/litnialex/telegram-proxybot
