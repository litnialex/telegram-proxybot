#!/usr/bin/env python3
import os
import asyncio
import logging
import traceback
import inspect
import html
import json
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from telegram import Bot, Update, ChatMember
from telegram.ext import filters
from telegram.constants import ParseMode, ReactionEmoji
from pysnooper import snoop

DB_URI = os.environ.get('DB_URI')
VERBOSE = os.environ.get('VERBOSE', False)
TELEGRAM_ID = os.environ.get('TELEGRAM_ID')
API_SECRET = os.environ.get('API_SECRET')
REVISION = os.environ.get('K_REVISION', '')
COMMIT = os.environ.get('COMMIT', '')
VERSION = f'version: {COMMIT} {REVISION}' if COMMIT or REVISION else ''

hello_text = (
        """This is your personal proxybot %s.\n"""
        """You can now share %s with the world!\n"""
         """All received messaged will be forwarded to you """
         """and you can easily send your replies back.\n"""
        """Homepage: https://proxybot.dev\n"""
        """Use /help for built-in commands reference.\n"""
        f"""{VERSION}"""
)
setautoreply_request_text = 'All right, provide your autoreply message now..'
setautoreply_confirm_text = 'Your autoreply message is now set to:\n%s'
setautoreply_wrong_type_text = (
    'Autoreply message must be text. /setautoreply command discarded'
)
no_match_text = 'No match for %s lookup, message discarded'

cmd_primary_ok_text = (
        """Done! """
        """From now on messages from new users will land here.\n"""
)
help_text = (
        "Supported commands:\n"
        "/start - Display welcome message\n"
        "/settings - Display all settings\n"
        "/setautoreply - Set your autoreply messages\n"
        "/setprimary - Route messages from new users in this chat\n"
        "/setsilent - Do not display technical Telegram message\n"
        "/setnosilent - Undo /setsilent\n\n"
        "All these commands are available only to you"
)
invalid_cmd_text = "Invalid command. /help for help"
setsilent_cmd_text = '/setsilent command acknowledged. /setnosilent to undo.'
setnosilent_cmd_text = '/setnosilent command acknowledged.'

log_create_new_rec = 'create new DB record for bot %s result: %s'
log_update_msg = "update ack=%s id=%s: %s"
log_insert_msg = 'insert ack=%s: %s'
log_status_msg = 'new status=%s for group %s'
migrate_chat_msg = "migrate chat from %s to %s for %s"
log_critical_msg = 'error_handler() fail - %s - update: %s - bot_data: %s'
secret_token_err_msg = "X-Telegram-Bot-Api-Secret-Token: %s != API_SECRET=%s"


# Logging settings
logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        level=logging.INFO if VERBOSE else logging.WARNING,
)
if not VERBOSE:
    logging.getLogger("httpx").setLevel(logging.WARNING)
logging = logging.getLogger(__name__)


def verboselog(text):
    if VERBOSE:
        logging.info(inspect.stack()[1][3] + ': ' + text)


def response(u_id, text, thread=None, parse_mode=None) -> dict:
    """Send message making request in response to incoming update"""
    resp = {
            'method': 'sendMessage',
            'chat_id': u_id,
            'text': text,
    }
    if thread:
        resp.update({'message_thread_id': thread})
    if parse_mode:
        resp.update({'parse_mode': parse_mode})
    return resp

async def error_handler(update, bot_data, error) -> dict:
    """Handle raised exception with notification to proxybot owner"""
    logging.error(f"{error} - {update.to_dict()}", exc_info=error)
    tb_list = traceback.format_exception(None, error, error.__traceback__)
    tb_string = "".join(tb_list)
    message = (
"An exception was raised while handling a message\n"
f"<pre>{html.escape(tb_string)}</pre>\n<pre>"
f"{html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False))}"
f"</pre>\n\n<pre>bot_data = {html.escape(str(bot_data))}</pre>"
    )
    return response(bot_data['tg_id'], message, parse_mode=ParseMode.HTML)


async def unset_emoji(update, chat, m_id):
    """Unset message_reaction for the specified message"""
    try:
        await update._bot.set_message_reaction(chat, m_id, reaction=None)
    except Exception as err:
        logging.error(f"unset reaction {chat} {m_id} - {err}")


async def set_autoreply(update, bot_data):
    conf = AsyncIOMotorClient(DB_URI)['conf']['bots']
    u_id = update.effective_user.id
    text = update.message.text
    if text:
        bot_data.pop('input_text')
        bot_data['setautoreply'] = update.message.text
        await conf.replace_one({'_id': bot_data['_id']}, bot_data)
        return_text = setautoreply_confirm_text % text
    else:
        return_text = setautoreply_wrong_type_text
    return response(u_id, return_text)


async def command(update, bot_data):
    """Handle commands from proxybot owner"""
    conf = AsyncIOMotorClient(DB_URI)['conf']['bots']
    u_id = update.effective_user.id
    chat = update.effective_chat
    cmdtext = update.effective_message.text

    if cmdtext.startswith('/start'):
        await update._bot.initialize()
        return response(u_id, hello_text % (update._bot.name, update._bot.link))

    elif cmdtext.startswith('/setautoreply'):
        bot_data.update({'input_text': 'setautoreply'})
        update_settings = setautoreply_request_text

    elif cmdtext.startswith('/settings'):
        bot_data.pop('_id')
        return response(
                chat.id,
                f'<pre>{html.escape(json.dumps(bot_data, indent=2))}</pre>',
                parse_mode=ParseMode.HTML,
        )

    elif cmdtext.startswith('/setprimary'):
        # Unset setprimary if issued directly into bot's chat
        if chat.id == bot_data['tg_id']:
            if bot_data.get('setprimary'):
                bot_data.pop('setprimary')
                update_settings = cmd_primary_ok_text
        # Set setprimary to current chat, only if group in in groups list
        elif chat.id in [i['id'] for i in bot_data.get('groups', [])]:
            if bot_data.get('setprimary') != chat.id:
                bot_data['setprimary'] = chat.id
                update_settings = cmd_primary_ok_text
        # Do not allow /setprimary in a random group (or?)
        else:
            return response(chat.id, 'This group is not in your groups')
        if not 'update_settings' in locals():
            return response(chat.id, 'Nothing to change.')

    elif cmdtext.startswith('/setsilent'):
        res = await conf.update_one(
                {'_id': bot_data['_id']},
                {'$set': {'setsilent': True}},
        )
        return response(chat.id, setsilent_cmd_text)

    elif cmdtext.startswith('/setnosilent'):
        res = await conf.update_one(
                {'_id': bot_data['_id']},
                {'$unset': {'setsilent': True}},
        )
        return response(chat.id, setnosilent_cmd_text)

    elif cmdtext.startswith('/help'):
        return response(u_id, help_text)

    elif cmdtext.startswith('/i'):
        return {'ok': True, 'description': 'ignore'}

    else:
        return response(u_id, invalid_cmd_text)

    # Update settings if needed
    if 'update_settings' in locals():
        verboselog(f'UPDATE BOT_DATA: {bot_data}')
        res = await conf.replace_one({'_id': bot_data['_id']}, bot_data)
        return response(chat.id, update_settings)

async def handle_status(update, bot_data):
    """Handle my_chat_member, when bot is added/removed from groups"""
    # Discard if not by tg_id or special bot GroupAnonymousBot
    if not (update.effective_user.id == bot_data['tg_id'] or
            update.effective_user.username == 'GroupAnonymousBot'):
        return await discard(update, bot_data)
    groups = bot_data.get('groups', [])
    group = update.effective_chat.to_dict()
    new_status = update.my_chat_member.new_chat_member.status
    logging.info(log_status_msg % (new_status, group))

    if new_status == ChatMember.MEMBER and group not in groups:
        groups.append(group)
    elif new_status == ChatMember.LEFT and group in groups:
        groups.remove(group)
    else:
        verboselog('no settings update needed')
        return {'ok': True, 'description': 'no settings update needed'}

    conf = AsyncIOMotorClient(DB_URI)['conf']['bots']
    bot_data.update({'groups': groups})
    res = await conf.replace_one({'_id': bot_data['_id']}, bot_data)
    verboselog(log_update_msg % (
            res.acknowledged,
            bot_data['_id'],
            f'groups={groups}',
            )
    )
    return {'ok': True, 'description': 'settings updated'}


async def migrate_chat_id(update, bot_data):
    """Handle migrate_to_chat_id updates"""
    bot_id = bot_data['bot_id']
    old_id = update.message.chat.id
    new_id = update.message.migrate_to_chat_id
    logging.info(migrate_chat_msg % (old_id, new_id, bot_id))

    # Update tracking accordingly
    tracking = AsyncIOMotorClient(DB_URI)['tracking'][f'bot{bot_id}']
    db_res = await tracking.update_many(
            {'p_chat': old_id},
            {'$set': {'p_chat': new_id}}
    )
    logging.info(f'modified {db_res.modified_count} records')
    return {'ok': True, 'description': f'{update.update_id}: migrate handled'}


async def discard(update, bot_data):
    """Discard silently or with notification Teleram update message"""
    if bot_data.get('setsilent') == True:
        return {'ok': True, 'description': f'{update.update_id}: discard'}
    message = (
"Ignoring received message.\nUse /setsilent command to mute.\n\n<pre>"
f"{html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False))}"
"</pre>"
    )
    return response(bot_data['tg_id'], message, parse_mode=ParseMode.HTML)


async def reply(update, bot_data) -> dict:
    """Send Replies from proxybot owner's chats to telegram users"""
    def search_by(origin):
        """Search by u_id of original meesage if not hidden, else by name"""
        return (
            {'u_name': origin.sender_user_name} if origin.type == 'hidden_user'
            else {'u_id': origin.sender_user.id}
        )

    message = update.effective_message
    bot_id = update._bot.token.split(':')[0]
    p_chat = update.effective_chat.id
    p_thread = message.message_thread_id
    current = {'p_chat': p_chat, 'p_thread': p_thread}

    # Check if it's an input for a command
    if bot_data.get('input_text') == 'setautoreply':
        if update.effective_user.id == bot_data['tg_id']:
            return await set_autoreply(update, bot_data)

    # Ignore text messages (in groups) starting with /i(gnore)
    if message.text and message.text.startswith('/i'):
        return {'ok': True, 'description': 'ignore'}

    # If Reply contains an original message
    if message.external_reply:
        search = search_by(message.external_reply.origin)
    elif (message.reply_to_message and
          message.reply_to_message.forward_origin):
        search = search_by(message.reply_to_message.forward_origin)
    # Else lookup for a match with current chat thread
    else:
        search = current

    # Lookup tracking data
    tracking = AsyncIOMotorClient(DB_URI)['tracking']['bot'+bot_id]
    track = tracking.find(search).sort({'timestamp': -1})
    track = await track.to_list(length=1)
    verboselog(f'lookup {search}": {track}')

    if track:
        track = track[0]
        # unset emoji for last message from this user in background
        unset_emoji_task = asyncio.create_task(
                unset_emoji(update, track['p_chat'], track['u_last_id'])
        )
        # update timestamp when msg is explicit "Reply to"
        if 'u_id' or 'u_name' in search:
            current.update({'timestamp': datetime.now()})
        # Check if p_chat or p_thred changed or timestamp added
        if not current.items() < track.items():
            track.update(current)
            res = await tracking.replace_one({'_id': track['_id']}, track)
            verboselog(log_update_msg % (res.acknowledged, track['_id'], current))
    # No track, but we have u_id in original message. Create a new track record
    elif 'u_id' in search:
        track = search
        track.update(current)
        res = await tracking.insert_one(track)
        verboselog(log_insert_msg % (res.acknowledged, track))
    # No track, no u_id, no nothing
    else:
        return response(p_chat, no_match_text % search, p_thread)

    # Wait for unset_emoji_task running in background to complete
    if 'unset_emoji_task' in locals():
        await unset_emoji_task

    # Main thing - copyMessage from proxybot owner to Telegram user
    return {
        'method': 'copyMessage',
        'chat_id': track['u_chat'], # if 'u_chat' in track else track['u_id'],
        'from_chat_id': p_chat,
        'message_id': message.message_id,
        'message_thread_id': track['u_thread'] if 'u_thread' in track else None,
    }


async def forward(update, bot_data) -> dict:
    """Forward messages from telegram users to proxybot owner's chat"""
    bot_id = update._bot.token.split(':')[0]
    u_id = update.effective_user.id
    u_chat = update.effective_chat.id
    u_name = update.effective_user.full_name
    u_thread = update.effective_message.message_thread_id
    jobs = []
    is_start_msg = (update.message and update.message.text and
            update.message.text == '/start') or False

    # Lookup tracking data by u_id
    tracking = AsyncIOMotorClient(DB_URI)['tracking']['bot'+bot_id]
    track = await tracking.find_one({'u_id': u_id})
    # Forward messages from new users according to bot's settings
    if not track:
        track = {'p_chat': bot_data.get('setprimary') or bot_data.get('tg_id')}
    verboselog(f'lookup u_id={u_id}: {track}')

    # unset emoji for last message from this user
    if track and track.get('u_last_id'):
        jobs.append(asyncio.create_task(
                unset_emoji(update, track['p_chat'], track['u_last_id'])
        ))

    # Send autoreply to /start message if set
    if is_start_msg and bot_data.get('setautoreply'):
        jobs.append(update._bot.send_message(u_id, bot_data['setautoreply']))

    # Forward message
    sent_msg = await update._bot.forward_message(
        track['p_chat'],
        u_chat,
        update.effective_message.message_id,
        message_thread_id=track['p_thread'] if 'p_thread' in track else None,
    )
    verboselog(f"forwarded as message id {sent_msg.id}")

    # Populate tracking data with current update
    track.update({
            'u_id': u_id,
            'u_chat': u_chat,
            'u_name': u_name,
            'u_thread': u_thread,
            'u_last_id': sent_msg.id,
            'timestamp': datetime.now(),
    })

    # Update or insert a new tracking record
    if '_id' in track:
        res = await tracking.replace_one({'_id': track['_id']}, track)
        _id = track['_id']
    else:
        res = await tracking.insert_one(track)
        _id = res.inserted_id
    verboselog(f"track {_id} update acknowledged={res.acknowledged}")

    # Wait for background jobs to complete
    await asyncio.gather(*jobs)

    # Set last message emoji reaction in response
    return {
        'method': 'setMessageReaction',
        'chat_id': track['p_chat'],
        'message_id': sent_msg.id,
        'reaction': [{"type":"emoji","emoji":"⚡"}],
    } if not is_start_msg else {
        'ok': True,
        'description': f'{update.update_id}: done',
    }


async def telegramma(request):
    """Telegram Message Accept"""
    """Function Is called from Flask route or Google Functions entrypoint"""

    try:
        # Assure critical varaibles are set
        assert TELEGRAM_ID, 'TELEGRAM_ID environment variable is not defined'
        assert DB_URI, 'DB_URI environment variable is not defined'

        # Check if X-Telegram-Bot-Api-Secret-Token matches API_SECRET env
        secret_token = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
        if secret_token != API_SECRET:
            logging.warning(secret_token_err_msg % (secret_token, API_SECRET))
            return '', 401

        # Get TOKEN from request path or 'token' param
        verboselog(f'JSON: {request.json}')
        TOKEN = request.path.lstrip('/') or request.args.get('token')
        assert TOKEN, 'TOKEN is empty'
        bot = Bot(TOKEN)
        bot_id = int(TOKEN.split(':')[0])

        # Get configuration data from DB or create a new record
        conf = AsyncIOMotorClient(DB_URI)['conf']['bots']
        bot_data = await conf.find_one({'bot_id': bot_id})
        if not bot_data:
            await bot.initialize()
            bot_data = {
                    'bot_id': bot_id,
                    'bot_name': bot.name,
                    'create_agent': 'ad-hoc',
                    'tg_id': int(TELEGRAM_ID),
                    'create_date': datetime.now().strftime('%Y-%m-%d'),
            }
            db_res = await conf.insert_one(bot_data)
            logging.warning(log_create_new_rec % (bot_id, db_res.acknowledged))
        else:
            assert bot_data['tg_id'], f'tg_id for {bot_id} undefined'
        verboselog(f'BOT_DATA: {bot_data}')
        tg_id = bot_data['tg_id']
        tg_groups = [i['id'] for i in bot_data.get('groups', [])]

        # Create update object from JSON data
        update = Update.de_json(data=request.json, bot=bot)
        assert update.effective_user, f'no user - {update.to_dict()}'
        u_id = update.effective_user.id

    # Deal with exception logging an error and notify TELEGRAM_ID
    except Exception as e:
        logging.error(f'dismiss update: {e}', exc_info=e)
        notify_id = tg_id if 'tg_id' in locals() else TELEGRAM_ID
        if notify_id:
            return response(notify_id, f'Error: {e}')
        else:
            return {'ok': False, 'description': 'Critical error'}

    # Choose a handler function and execute it
    try:
        # Accept commands only from proxybot owner
        if (u_id == tg_id and filters.Command().check_update(update)):
            dispatch = command
        # Hanle status updates
        elif update.my_chat_member:
            dispatch = handle_status
        # Handle migrate_to_chat_id (group to supergroup with ID change)
        elif update.message and update.message.migrate_to_chat_id:
            dispatch = migrate_chat_id
        # Discard (with notify) all other status change messages
        elif filters.StatusUpdate.ALL.check_update(update):
            logging.info(f'discard status update - {update.to_dict()}')
            dispatch = discard
        # Discard (with notify) all updates without message (like message_reaction)
        elif not update.effective_message:
            logging.info(f'discard non-message update - {update.to_dict()}')
            dispatch = discard
        # reply() function handles messages from proxybot owner and his groups
        elif (u_id == tg_id or update.effective_chat.id in tg_groups):
            dispatch = reply
        # All the rest is forwarded to proxybot owner (owner's group)
        else:
            dispatch = forward
        # Run chosen dispatcher
        res = await dispatch(update, bot_data)
    except Exception as e:
        res = await error_handler(update, bot_data, e)
    return res
