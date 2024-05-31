# dante - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/dante/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/dante/blob/main/LICENSE/>.

import asyncio
from dante.dB import stickers
from dante.dB.forcesub_db import get_forcesetting
from dante.dB.gban_mute_db import is_gbanned
from dante.dB.greetings_db import get_goodbye, get_welcome, must_thank
from dante.dB.nsfw_db import is_profan
from dante.fns.helper import inline_mention
from dante.fns.tools import async_searcher, create_tl_btn, get_chatbot_reply
from telethon import events
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.utils import get_display_name

try:
    from ProfanityDetector import detector
except ImportError:
    detector = None
from . import LOG_CHANNEL, LOGS, asst, dante_bot, get_string, types, udB
from ._inline import something


@dante_bot.on(events.ChatAction())
async def Function(event):
    try:
        await DummyHandler(event)
    except Exception as er:
        LOGS.exception(er)


async def DummyHandler(dante):
    # clean chat actions
    key = udB.get_key("CLEANCHAT") or []
    if dante.chat_id in key:
        try:
            await dante.delete()
        except BaseException:
            pass

    # thank members
    if must_thank(dante.chat_id):
        chat_count = (await dante.client.get_participants(dante.chat_id, limit=0)).total
        if chat_count % 100 == 0:
            stik_id = chat_count / 100 - 1
            sticker = stickers[stik_id]
            await dante.respond(file=sticker)
    # force subscribe
    if (
        udB.get_key("FORCESUB")
        and ((dante.user_joined or dante.user_added))
        and get_forcesetting(dante.chat_id)
    ):
        user = await dante.get_user()
        if not user.bot:
            joinchat = get_forcesetting(dante.chat_id)
            try:
                await dante_bot(GetParticipantRequest(int(joinchat), user.id))
            except UserNotParticipantError:
                await dante_bot.edit_permissions(
                    dante.chat_id, user.id, send_messages=False
                )
                res = await dante_bot.inline_query(
                    asst.me.username, f"fsub {user.id}_{joinchat}"
                )
                await res[0].click(dante.chat_id, reply_to=dante.action_message.id)

    if dante.user_joined or dante.added_by:
        user = await dante.get_user()
        chat = await dante.get_chat()
        # gbans and @dante checks
        if udB.get_key("dante_BANS"):
            try:
                is_banned = await async_searcher(
                    "https://bans.dante/api/status",
                    json={"userId": user.id},
                    post=True,
                    re_json=True,
                )
                if is_banned["is_banned"]:
                    await dante.client.edit_permissions(
                        chat.id,
                        user.id,
                        view_messages=False,
                    )
                    await dante.client.send_message(
                        chat.id,
                        f'**@danteBans:** Banned user detected and banned!\n`{str(is_banned)}`.\nBan reason: {is_banned["reason"]}',
                    )

            except BaseException:
                pass
        reason = is_gbanned(user.id)
        if reason and chat.admin_rights:
            try:
                await dante.client.edit_permissions(
                    chat.id,
                    user.id,
                    view_messages=False,
                )
                gban_watch = get_string("can_1").format(inline_mention(user), reason)
                await dante.reply(gban_watch)
            except Exception as er:
                LOGS.exception(er)

        elif get_welcome(dante.chat_id):
            user = await dante.get_user()
            chat = await dante.get_chat()
            title = chat.title or "this chat"
            count = (
                chat.participants_count
                or (await dante.client.get_participants(chat, limit=0)).total
            )
            mention = inline_mention(user)
            name = user.first_name
            fullname = get_display_name(user)
            uu = user.username
            username = f"@{uu}" if uu else mention
            wel = get_welcome(dante.chat_id)
            med = wel["media"] or None
            userid = user.id
            msg = None
            if msgg := wel["welcome"]:
                msg = msgg.format(
                    mention=mention,
                    group=title,
                    count=count,
                    name=name,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                )
            if wel.get("button"):
                btn = create_tl_btn(wel["button"])
                await something(dante, msg, med, btn)
            elif msg:
                send = await dante.reply(
                    msg,
                    file=med,
                )
                await asyncio.sleep(150)
                await send.delete()
            else:
                await dante.reply(file=med)
    elif (dante.user_left or dante.user_kicked) and get_goodbye(dante.chat_id):
        user = await dante.get_user()
        chat = await dante.get_chat()
        title = chat.title or "this chat"
        count = (
            chat.participants_count
            or (await dante.client.get_participants(chat, limit=0)).total
        )
        mention = inline_mention(user)
        name = user.first_name
        fullname = get_display_name(user)
        uu = user.username
        username = f"@{uu}" if uu else mention
        wel = get_goodbye(dante.chat_id)
        med = wel["media"]
        userid = user.id
        msg = None
        if msgg := wel["goodbye"]:
            msg = msgg.format(
                mention=mention,
                group=title,
                count=count,
                name=name,
                fullname=fullname,
                username=username,
                userid=userid,
            )
        if wel.get("button"):
            btn = create_tl_btn(wel["button"])
            await something(dante, msg, med, btn)
        elif msg:
            send = await dante.reply(
                msg,
                file=med,
            )
            await asyncio.sleep(150)
            await send.delete()
        else:
            await dante.reply(file=med)

"""
@dante_bot.on(events.NewMessage(incoming=True))
async def chatBot_replies(e):
    sender = await e.get_sender()
    if not isinstance(sender, types.User):
        return
    key = udB.get_key("CHATBOT_USERS") or {}
    if e.text and key.get(e.chat_id) and sender.id in key[e.chat_id]:
        msg = await get_chatbot_reply(e.message.message)
        if msg:
            sleep = udB.get_key("CHATBOT_SLEEP") or 1.5
            await asyncio.sleep(sleep)
            await e.reply(msg)
    chat = await e.get_chat()
    if e.is_group and not sender.bot:
        if sender.username:
            await uname_stuff(e.sender_id, sender.username, sender.first_name)
    elif e.is_private and not sender.bot:
        if chat.username:
            await uname_stuff(e.sender_id, chat.username, chat.first_name)
    if detector and is_profan(e.chat_id) and e.text:
        x, y = detector(e.text)
        if y:
            await e.delete()
"""

@dante_bot.on(events.Raw(types.UpdateUserName))
async def uname_change(e):
    await uname_stuff(e.user_id, e.username, e.first_name)


async def uname_stuff(id, uname, name):
    if udB.get_key("USERNAME_LOG"):
        old_ = udB.get_key("USERNAME_DB") or {}
        old = old_.get(id)
        # Ignore Name Logs
        if old and old == uname:
            return
        if old and uname:
            await asst.send_message(
                LOG_CHANNEL,
                get_string("can_2").format(old, uname),
            )
        elif old:
            await asst.send_message(
                LOG_CHANNEL,
                get_string("can_3").format(f"[{name}](tg://user?id={id})", old),
            )
        elif uname:
            await asst.send_message(
                LOG_CHANNEL,
                get_string("can_4").format(f"[{name}](tg://user?id={id})", uname),
            )

        old_[id] = uname
        udB.set_key("USERNAME_DB", old_)
