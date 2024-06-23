***Proxybot assists teams and individuals to manage securely customer communications from their personal Telegram apps.***

This **Proxybot** is a [Telegram] bot designed to forward all incoming messages to its owner. Proxybot enables it's owner to:

 * **Receive all incoming messages**: When the bot's username is published, any messages sent to the bot are forwarded to the owner.
 * **Reply to messages on behalf of the bot**: The bot's owner can reply back to customers directly in the chat with the bot.

<img style="max-height:550px;" src="demo1.gif" />

Messages to the chat with bot always go to the last contact.
To reply to a specific message from the chat history, simply select the message and press "Reply" as demonstrated above.
Bot marks with ⚡️ symbol last unreplied message from each customer.

Also a good way to organize clients communications is by creating a **supergroup with topics** and setting it as a default place to receive messages. Proxybot will then automatically create an individual topic for every new contact. Here is how it looks like:

<img style="max-height:550px;" src="demo2.gif" />

To reapeat this you will need:

 1. Create a group
 1. Enable topics in group's settings (making it a supergroup)
 1. Add the bot to the group
 1. Promote bot to admin with "Мanage topics" and "Delete messages" privileges
 1. Issue `/setdefault` command in General topic of the supergroup
 1. (Optional) add more members to the group. Any member of the group can make replies in the same way as the bot owner does.


**Voice** messages, **video** messages, **files** and any other media-format
supported by the Telegram can be proxied in this manner.

## Use proxybot as a service
This bot: [@InitProxybot] can launch your proxybot in the cloud within seconds.

This is offered as a service from proxybot developer with an annual subscription fee of $20.

You get 4 months of free usage, prepay is not required.

*It's extremely easy to start using proxybot.*

<iframe width="315" height="560"
src="https://www.youtube.com/embed/OgT1-AoHagU"
title="YouTube video player" frameborder="0"
allow="accelerometer; autoplay; clipboard-write; encrypted-media;gyroscope;
picture-in-picture; web-share" allowfullscreen>
</iframe>

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
