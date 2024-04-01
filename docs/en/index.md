Proxybot is a [Telegram](https://www.telegram.org) bot which forwards all incoming messages to the owner or into a telegram group, specified by the owner.
This group can also be a supergroup with topics.

Replies are done simply texting back in the chat. Such messages always go to the last contact in  that chat.
Of course, you can reply to any specific message in chat history by pressing "Reply" link in that message.

Voice-messages, video-messages, files and any other media format supported by Telegram can be proxied in this manner.

*Proxybot assists teams and individuals in managing public communications through their personal Telegram accounts.*


## Use proxybot as a service
This bot: [@InitProxybot](https://t.me/InitProxybot) can launch your proxybot in the cloud within seconds.

This is offered as a service from proxybot developer with an annual subscription fee of $20.

You get 4 months of free usage, prepay is not required.

*It's extremely easy to start using proxybot.*


## Launch by your own

Proxybot can be launched as a [serverless function](Telegram-Bot-Serverless.md) or as a [Flask application](Telegram-Bot-Flask.md).

In this case you will need to provide a valid MongoDB connection.
You may start with [MongoDB Atlas](https://www.mongodb.com/docs/atlas/) free tier.

`TELEGRAM_ID` variable must contain the ID of the Telegram account  assigned "proxybot owner" privilege, and only this account will be able to control bot via commands.
If you want to find out your telegram ID ask [@my_id_bot ](https://t.me/my_id_bot)


## Security considerations

Proxybot is designed with respect to personal privacy and security in mind.
It is a 100% Open Source software dedicated to the public domain.

`TOKEN` value is not stored anywhere in the database. Proxybot receives it as a part of the webhook URL and uses it only until finishing handling the incoming request.


## Feedback

Contact [@devproxybot](https://t.me/devproxybot) for any questions or feedback.
