# dante - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/dante/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/dante/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk PM Permit**

๏ **Perintah:** `ok`
◉ **Keterangan:** Setujui pesan.

๏ **Perintah:** `no`
◉ **Keterangan:** Tolak pesan.

๏ **Perintah:** `block`
◉ **Keterangan:** Blokir pengguna.

๏ **Perintah:** `unblock`
◉ **Keterangan:** Buka blokir pengguna.

๏ **Perintah:** `nologpm`
◉ **Keterangan:** Berhenti mencatat pesan pengguna tsb.

๏ **Perintah:** `logpm`
◉ **Keterangan:** Mencatat pesan pengguna tsb.

๏ **Perintah:** `listok`
◉ **Keterangan:** Mendapatkan daftar pengguna yang disetujui.
"""

import asyncio
import re
from os import remove

from dante.dB import DEVS
from dante.dB.logusers_db import *
from dante.dB.pmpermit_db import *

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None
from telethon import events
from telethon.errors import MessageNotModifiedError
from telethon.tl.functions.contacts import (BlockRequest, GetBlockedRequest,
                                            UnblockRequest)
from telethon.tl.functions.messages import ReportSpamRequest
from telethon.utils import get_display_name, resolve_bot_file_id

from . import *

# ========================= CONSTANTS =============================

COUNT_PM = {}
LASTMSG = {}
WARN_MSGS = {}
U_WARNS = {}
PMPIC = udB.get_key("PMPIC")
LOG_CHANNEL = udB.get_key("LOG_CHANNEL")
DISABLE_PMDEL = udB.set_key("DISABLE_PMDEL", True)
UND = get_string("pmperm_1")
UNS = get_string("pmperm_2")
NO_REPLY = get_string("pmperm_3")

UNAPPROVED_MSG = (
    "**Pesan Keamanan {ON}!**\n\n{UND}\n\nAnda Punya {warn}/{twarn} peringatan!"
)
if udB.get_key("PM_TEXT"):
    UNAPPROVED_MSG = (
        "**Pesan Keamanan dari {ON}!**\n\n"
        + udB.get_key("PM_TEXT")
        + "\n\nKamu Punya {warn}/{twarn} peringatan!"
    )
# 1
WARNS = udB.get_key("PMWARNS") or 3
PMCMDS = [
    f"{HNDLR}a",
    f"{HNDLR}ok",
    f"{HNDLR}no",
    f"{HNDLR}tolak",
    f"{HNDLR}block",
    f"{HNDLR}unblock",
]

_not_approved = {}
_to_delete = {}

my_bot = asst.me.username


def update_pm(userid, message, warns_given):
    try:
        WARN_MSGS.update({userid: message})
    except KeyError:
        pass
    try:
        U_WARNS.update({userid: warns_given})
    except KeyError:
        pass


async def delete_pm_warn_msgs(chat: int):
    try:
        await _to_delete[chat].delete()
    except KeyError:
        pass


# =================================================================


if udB.get_key("PMLOG"):

    @dante_cmd(
        pattern="(l|L)ogpm$",
    )
    async def _(e):
        if not e.is_private:
            return await e.eor("`Use me in Private.`", time=3)
        if not is_logger(e.chat_id):
            return await e.eor("`Wasn't logging msgs from here.`", time=3)

        nolog_user(e.chat_id)
        return await e.eor("`Now I Will log msgs from here.`", time=3)

    @dante_cmd(
        pattern="(n|N)ologpm$",
    )
    async def _(e):
        if not e.is_private:
            return await e.eor("`Use me in Private.`", time=3)
        if is_logger(e.chat_id):
            return await e.eor("`Wasn't logging msgs from here.`", time=3)

        log_user(e.chat_id)
        return await e.eor("`Now I Won't log msgs from here.`", time=3)

    @dante_bot.on(
        events.NewMessage(
            incoming=True,
            func=lambda e: e.is_private,
        ),
    )
    async def permitpm(event):
        user = await event.get_sender()
        if user.bot or user.is_self or user.verified or is_logger(user.id):
            return
        await event.forward_to(udB.get_key("PMLOGGROUP") or LOG_CHANNEL)


if udB.get_key("PMSETTING"):
    if udB.get_key("AUTOAPPROVE"):

        @dante_bot.on(
            events.NewMessage(
                outgoing=True,
                func=lambda e: e.is_private and e.out and not e.text.startswith(HNDLR),
            ),
        )
        async def autoappr(e):
            miss = await e.get_chat()
            if miss.bot or miss.is_self or miss.verified or miss.id in DEVS:
                return
            if is_approved(miss.id):
                return
            approve_user(miss.id)
            await delete_pm_warn_msgs(miss.id)
            try:
                await dante_bot.edit_folder(miss.id, folder=0)
            except BaseException:
                pass
            try:
                await asst.edit_message(
                    LOG_CHANNEL,
                    _not_approved[miss.id],
                    f"#AutoApproved : <b>OutGoing Message.\nUser : {inline_mention(miss, html=True)}</b> [<code>{miss.id}</code>]",
                    parse_mode="html",
                )
            except KeyError:
                await asst.send_message(
                    LOG_CHANNEL,
                    f"#AutoApproved : <b>OutGoing Message.\nUser : {inline_mention(miss, html=True)}</b> [<code>{miss.id}</code>]",
                    parse_mode="html",
                )
            except MessageNotModifiedError:
                pass

    @dante_bot.on(
        events.NewMessage(
            incoming=True,
            func=lambda e: e.is_private
            and e.sender_id not in DEVS
            and not e.out
            and not e.sender.bot
            and not e.sender.is_self
            and not e.sender.verified,
        )
    )
    async def permitpm(event):
        inline_pm = Redis("INLINE_PM") or False
        user = event.sender
        if not is_approved(user.id) and event.text != UND:
            if Redis("MOVE_ARCHIVE"):
                try:
                    await dante_bot.edit_folder(user.id, folder=1)
                except BaseException as er:
                    LOGS.info(er)
            if event.media and not udB.get_key("DISABLE_PMDEL"):
                await event.delete()
            name = user.first_name
            fullname = get_display_name(user)
            username = f"@{user.username}"
            mention = inline_mention(user)
            count = len(get_approved())
            try:
                wrn = COUNT_PM[user.id] + 1
                await asst.edit_message(
                    int(udB.get_key("LOG_CHANNEL")),
                    _not_approved[user.id],
                    f"Pesan masuk dari **{mention}** [`{user.id}`] dengan **{wrn}/{WARNS}** peringatan!",
                    buttons=[
                        Button.inline("Setujui", data=f"approve_{user.id}"),
                        Button.inline("Blokir", data=f"block_{user.id}"),
                    ],
                )
            except KeyError:
                _not_approved[user.id] = await asst.send_message(
                    int(udB.get_key("LOG_CHANNEL")),
                    f"Pesan masuk dari **{mention}** [`{user.id}`] dengan **1/{WARNS}** peringatan!",
                    buttons=[
                        Button.inline("Setujui", data=f"approve_{user.id}"),
                        Button.inline("Blokir", data=f"block_{user.id}"),
                    ],
                )
                wrn = 1
            except MessageNotModifiedError:
                wrn = 1
            if user.id in LASTMSG:
                prevmsg = LASTMSG[user.id]
                if event.text != prevmsg:
                    if "Pesan Keamanan" in event.text:
                        return
                    await delete_pm_warn_msgs(user.id)
                    message_ = UNAPPROVED_MSG.format(
                        ON=OWNER_NAME,
                        warn=wrn,
                        twarn=WARNS,
                        UND=UND,
                        name=name,
                        fullname=fullname,
                        username=username,
                        count=count,
                        mention=mention,
                    )
                    update_pm(user.id, message_, wrn)
                    if inline_pm:
                        results = await dante_bot.inline_query(my_bot, f"ip_{user.id}")
                        try:
                            _to_delete[user.id] = await results[0].click(
                                user.id, reply_to=event.id, hide_via=True
                            )
                        except Exception as e:
                            LOGS.info(str(e))
                    elif PMPIC:
                        _to_delete[user.id] = await dante_bot.send_file(
                            user.id,
                            PMPIC,
                            caption=message_,
                        )
                    else:
                        _to_delete[user.id] = await dante_bot.send_message(
                            user.id, message_
                        )

                else:
                    await delete_pm_warn_msgs(user.id)
                    message_ = UNAPPROVED_MSG.format(
                        ON=OWNER_NAME,
                        warn=wrn,
                        twarn=WARNS,
                        UND=UND,
                        name=name,
                        fullname=fullname,
                        username=username,
                        count=count,
                        mention=mention,
                    )
                    update_pm(user.id, message_, wrn)
                    if inline_pm:
                        try:
                            results = await dante_bot.inline_query(
                                my_bot, f"ip_{user.id}"
                            )
                            _to_delete[user.id] = await results[0].click(
                                user.id, reply_to=event.id, hide_via=True
                            )
                        except Exception as e:
                            LOGS.info(str(e))
                    elif PMPIC:
                        _to_delete[user.id] = await dante_bot.send_file(
                            user.id,
                            PMPIC,
                            caption=message_,
                        )
                    else:
                        _to_delete[user.id] = await dante_bot.send_message(
                            user.id, message_
                        )
                LASTMSG.update({user.id: event.text})
            else:
                await delete_pm_warn_msgs(user.id)
                message_ = UNAPPROVED_MSG.format(
                    ON=OWNER_NAME,
                    warn=wrn,
                    twarn=WARNS,
                    UND=UND,
                    name=name,
                    fullname=fullname,
                    username=username,
                    count=count,
                    mention=mention,
                )
                update_pm(user.id, message_, wrn)
                if inline_pm:
                    try:
                        results = await dante_bot.inline_query(my_bot, f"ip_{user.id}")
                        _to_delete[user.id] = await results[0].click(
                            user.id, reply_to=event.id, hide_via=True
                        )
                    except Exception as e:
                        LOGS.info(str(e))
                elif PMPIC:
                    _to_delete[user.id] = await dante_bot.send_file(
                        user.id,
                        PMPIC,
                        caption=message_,
                    )
                else:
                    _to_delete[user.id] = await dante_bot.send_message(user.id, message_)
            LASTMSG.update({user.id: event.text})
            if user.id not in COUNT_PM:
                COUNT_PM.update({user.id: 1})
            else:
                COUNT_PM[user.id] = COUNT_PM[user.id] + 1
            if COUNT_PM[user.id] >= WARNS:
                await delete_pm_warn_msgs(user.id)
                _to_delete[user.id] = await event.respond(UNS)
                try:
                    del COUNT_PM[user.id]
                    del LASTMSG[user.id]
                except KeyError:
                    await asst.send_message(
                        int(udB.get_key("LOG_CHANNEL")),
                        "PMPermit eror, tolong restart bot !!",
                    )
                    return LOGS.info("COUNT_PM is messed.")
                await dante_bot(BlockRequest(user.id))
                await dante_bot(ReportSpamRequest(peer=user.id))
                await asst.edit_message(
                    int(udB.get_key("LOG_CHANNEL")),
                    _not_approved[user.id],
                    f"**{mention}** [`{user.id}`] Diblokir karena spamming.",
                )

    @dante_cmd(pattern="(start|stop|clear)archive$", fullsudo=False)
    async def _(e):
        x = e.pattern_match.group(1).strip()
        if x == "start":
            udB.set_key("MOVE_ARCHIVE", "True")
            await e.eor("Now I will move new Unapproved DM's to archive", time=5)
        elif x == "stop":
            udB.set_key("MOVE_ARCHIVE", "False")
            await e.eor("Now I won't move new Unapproved DM's to archive", time=5)
        elif x == "clear":
            try:
                await e.client.edit_folder(unpack=1)
                await e.eor("Unarchived all chats", time=5)
            except Exception as mm:
                await e.eor(str(mm), time=5)

    @dante_cmd(pattern="[oO][kK](?: |$)", fullsudo=False)
    async def approvepm(apprvpm):
        if apprvpm.reply_to_msg_id:
            user = (await apprvpm.get_reply_message()).sender
        elif apprvpm.is_private:
            user = await apprvpm.get_chat()
        else:
            return await apprvpm.edit(NO_REPLY)
        if user.id in DEVS:
            return await eor(
                apprvpm,
                "Dia adalah Developer Saya.",
            )
        if not is_approved(user.id):
            approve_user(user.id)
            try:
                await delete_pm_warn_msgs(user.id)
                await apprvpm.client.edit_folder(user.id, folder=0)
            except BaseException:
                pass
            await eod(
                apprvpm,
                f"<b>{inline_mention(user, html=True)}</b> <code>Disetujui untuk Pesan !</code>",
                parse_mode="html",
            )
            try:
                await asst.edit_message(
                    int(udB.get_key("LOG_CHANNEL")),
                    _not_approved[user.id],
                    f"#APPROVED\n\n<b>{inline_mention(user, html=True)}</b> [<code>{user.id}</code>] <code>Telah disetujui untuk mengirim pesan!</code>",
                    buttons=[
                        Button.inline("Tolak", data=f"disapprove_{user.id}"),
                        Button.inline("Blokir", data=f"block_{user.id}"),
                    ],
                    parse_mode="html",
                )
            except KeyError:
                _not_approved[user.id] = await asst.send_message(
                    int(udB.get_key("LOG_CHANNEL")),
                    f"#APPROVED\n\n<b>{inline_mention(user, html=True)}</b> [<code>{user.id}</code>] <code>Disetujui untuk mengirim Pesan.</code>",
                    buttons=[
                        Button.inline("Tolak", data=f"disapprove_{user.id}"),
                        Button.inline("Blokir", data=f"block_{user.id}"),
                    ],
                    parse_mode="html",
                )
            except MessageNotModifiedError:
                pass
        else:
            await apprvpm.eor("`Pengguna sudah Disetujui.`", time=5)

    @dante_cmd(pattern="[nN][oO](?: |$)", fullsudo=False)
    async def disapprovepm(e):
        if e.reply_to_msg_id:
            user = (await e.get_reply_message()).sender
        elif e.is_private:
            user = await e.get_chat()
        else:
            return await e.edit(NO_REPLY)
        if user.id in DEVS:
            return await eor(
                e,
                "`Dia adalah Developer Saya.`",
            )
        if is_approved(user.id):
            disapprove_user(user.id)
            await eod(
                e,
                f"<b>{inline_mention(user, html=True)}</b> <code>Ditolak untuk mengirim Pesan!</code>",
                parse_mode="html",
            )
            try:
                await asst.edit_message(
                    int(udB.get_key("LOG_CHANNEL")),
                    _not_approved[user.id],
                    f"#DISAPPROVED\n\n<b>{inline_mention(user, html=True)}</b> [<code>{user.id}</code>] <code>Ditolak Untuk mengirim Pesan.</code>",
                    buttons=[
                        Button.inline("Ok", data=f"approve_{user.id}"),
                        Button.inline("Blokir", data=f"block_{user.id}"),
                    ],
                    parse_mode="html",
                )
            except KeyError:
                _not_approved[user.id] = await asst.send_message(
                    int(udB.get_key("LOG_CHANNEL")),
                    f"#DISAPPROVED\n\n<b>{inline_mention(user, html=True)}</b> [<code>{user.id}</code>] <code>Ditolak untuk mengirim pesan.</code>",
                    buttons=[
                        Button.inline("Setujui", data=f"approve_{user.id}"),
                        Button.inline("Blokir", data=f"block_{user.id}"),
                    ],
                    parse_mode="html",
                )
            except MessageNotModifiedError:
                pass
        else:
            await eod(
                e,
                f"<b>{inline_mention(user, html=True)}</b> <code>Belum Disetujui.</code>",
                parse_mode="html",
            )


@dante_cmd(pattern="(B|b)lock( (.*)|$)", fullsudo=False)
async def blockpm(block):
    match = block.pattern_match.group(1).strip()
    if block.reply_to_msg_id:
        user = (await block.get_reply_message()).sender_id
    elif match:
        try:
            user = await block.client.parse_id(match)
        except Exception as er:
            return await block.eor(str(er))
    elif block.is_private:
        user = block.chat_id
    else:
        return await eor(block, NO_REPLY, time=10)

    await block.client(BlockRequest(user))
    aname = await block.client.get_entity(user)
    await block.eor(f"{inline_mention(aname)} [`{user}`] `telah diblokir!`")
    try:
        disapprove_user(user)
    except AttributeError:
        pass
    try:
        await asst.edit_message(
            int(udB.get_key("LOG_CHANNEL")),
            _not_approved[user],
            f"#BLOCKED\n\n{inline_mention(aname)} [`{user}`] telah ** diblokir**.",
            buttons=[
                Button.inline("UnBlock", data=f"unblock_{user}"),
            ],
        )
    except KeyError:
        _not_approved[user] = await asst.send_message(
            int(udB.get_key("LOG_CHANNEL")),
            f"#BLOCKED\n\n{inline_mention(aname)} [`{user}`] telah **diblokir**.",
            buttons=[
                Button.inline("Buka Blokir", data=f"unblock_{user}"),
            ],
        )
    except MessageNotModifiedError:
        pass


@dante_cmd(pattern="unblock( (.*)|$)", fullsudo=False)
async def unblockpm(event):
    match = event.pattern_match.group(1).strip()
    reply = await event.get_reply_message()
    if reply:
        user = reply.sender_id
    elif match:
        if match == "all":
            msg = await event.eor(get_string("com_1"))
            u_s = await event.client(GetBlockedRequest(0, 0))
            count = len(u_s.users)
            if not count:
                return await eor(msg, "__You have not blocked Anyone...__")
            for user in u_s.users:
                await asyncio.sleep(1)
                await event.client(UnblockRequest(user.id))
            # GetBlockedRequest return 20 users at most.
            if count < 20:
                return await eor(msg, f"__Unblocked {count} Users!__")
            while u_s.users:
                u_s = await event.client(GetBlockedRequest(0, 0))
                for user in u_s.users:
                    await asyncio.sleep(3)
                    await event.client(UnblockRequest(user.id))
                count += len(u_s.users)
            return await eor(msg, f"__Unblocked {count} users.__")

        try:
            user = await event.client.parse_id(match)
        except Exception as er:
            return await event.eor(str(er))
    elif event.is_private:
        user = event.chat_id
    else:
        return await event.eor(NO_REPLY, time=10)
    try:
        await event.client(UnblockRequest(user))
        aname = await event.client.get_entity(user)
        await event.eor(f"{inline_mention(aname)} [`{user}`] `telah dibuka blokirnya!`")
    except Exception as et:
        return await event.eor(f"ERROR - {et}")
    try:
        await asst.edit_message(
            udB.get_key("LOG_CHANNEL"),
            _not_approved[user],
            f"#UNBLOCKED\n\n{inline_mention(aname)} [`{user}`] telah ** dibuka blokirnya**.",
            buttons=[
                Button.inline("Blokir", data=f"block_{user}"),
            ],
        )
    except KeyError:
        _not_approved[user] = await asst.send_message(
            udB.get_key("LOG_CHANNEL"),
            f"#UNBLOCKED\n\n{inline_mention(aname)} [`{user}`] telah ** dibuka blokirnya**.",
            buttons=[
                Button.inline("Blokir", data=f"block_{user}"),
            ],
        )
    except MessageNotModifiedError:
        pass


@dante_cmd(pattern="(L|l)istok", owner=True)
async def list_approved(event):
    xx = await event.eor(get_string("com_1"))
    all = get_approved()
    if not all:
        return await xx.eor("`You haven't approved anyone yet!`", time=5)
    users = []
    for i in all:
        try:
            name = get_display_name(await dante_bot.get_entity(i))
        except BaseException:
            name = ""
        users.append([name.strip(), str(i)])
    with open("approved_pms.txt", "w") as list_appr:
        if tabulate:
            list_appr.write(
                tabulate(users, headers=["UserName", "UserID"], showindex="always")
            )
        else:
            text = "".join(f"[{user[-1]}] - {user[0]}" for user in users)
            list_appr.write(text)
    await event.reply(
        f"List of users approved by [{OWNER_NAME}](tg://user?id={OWNER_ID})",
        file="approved_pms.txt",
    )

    await xx.delete()
    remove("approved_pms.txt")


@callback(
    re.compile(
        b"approve_(.*)",
    ),
    from_users=[dante_bot.uid],
)
async def apr_in(event):
    uid = int(event.data_match.group(1).decode("UTF-8"))
    if uid in DEVS:
        await event.edit("It's a dev! Approved!")
    if not is_approved(uid):
        approve_user(uid)
        try:
            await dante_bot.edit_folder(uid, folder=0)
        except BaseException:
            pass
        try:
            user = await dante_bot.get_entity(uid)
        except BaseException:
            return await event.delete()
        await event.edit(
            f"#APPROVED\n\n<b>{inline_mention(user, html=True)}</b> [<code>{user.id}</code>] <code>Disetujui untuk mengirim Pesan !</code>",
            buttons=[
                [
                    Button.inline("Tolak", data=f"disapprove_{uid}"),
                    Button.inline("Blokir", data=f"block_{uid}"),
                ],
            ],
            parse_mode="html",
        )
        await delete_pm_warn_msgs(uid)
        await event.answer("Disetujui untuk mengirim Pesan.", alert=True)
    else:
        await event.edit(
            "`User may already be approved.`",
            buttons=[
                [
                    Button.inline("Tolak", data=f"disapprove_{uid}"),
                    Button.inline("Blokir", data=f"block_{uid}"),
                ],
            ],
        )


@callback(
    re.compile(
        b"disapprove_(.*)",
    ),
    from_users=[dante_bot.uid],
)
async def disapr_in(event):
    uid = int(event.data_match.group(1).decode("UTF-8"))
    if is_approved(uid):
        disapprove_user(uid)
        try:
            user = await dante_bot.get_entity(uid)
        except BaseException:
            return await event.delete()
        await event.edit(
            f"#DISAPPROVED\n\n<b>{inline_mention(user, html=True)}</b> [<code>{user.id}</code>] <code>Ditolak untuk mengirim pesan !</code>",
            buttons=[
                [
                    Button.inline("Setujui", data=f"approve_{uid}"),
                    Button.inline("Blokir", data=f"block_{uid}"),
                ],
            ],
            parse_mode="html",
        )
        await event.answer("Ditolak untuk mengirim pesan.", alert=True)
    else:
        await event.edit(
            "`User was never approved!`",
            buttons=[
                [
                    Button.inline("Tolak", data=f"disapprove_{uid}"),
                    Button.inline("Blokir", data=f"block_{uid}"),
                ],
            ],
        )


@callback(
    re.compile(
        b"block_(.*)",
    ),
    from_users=[dante_bot.uid],
)
async def blck_in(event):
    uid = int(event.data_match.group(1).decode("UTF-8"))
    try:
        await dante_bot(BlockRequest(uid))
    except BaseException:
        pass
    try:
        user = await dante_bot.get_entity(uid)
    except BaseException:
        return await event.delete()
    await event.edit(
        f"BLOCKED\n\n<b>{inline_mention(user, html=True)}</b> [<code>{user.id}</code>] <code>diblokir!</code>",
        buttons=Button.inline("Buka Blokir", data=f"unblock_{uid}"),
        parse_mode="html",
    )
    await event.answer("Berhasil Diblokir.", alert=True)


@callback(
    re.compile(
        b"unblock_(.*)",
    ),
    from_users=[dante_bot.uid],
)
async def unblck_in(event):
    uid = int(event.data_match.group(1).decode("UTF-8"))
    try:
        await dante_bot(UnblockRequest(uid))
    except BaseException:
        pass
    try:
        user = await dante_bot.get_entity(uid)
    except BaseException:
        return await event.delete()
    await event.edit(
        f"#UNBLOCKED\n\n<b>{inline_mention(user, html=True)}</b> [<code>{user.id}</code>] <code>telah dibuka blokirnya!</code>",
        buttons=Button.inline("Blokir", data=f"block_{uid}"),
        parse_mode="html",
    )
    await event.answer("Berhasil Dibuka Blokir.", alert=True)


@callback("deletedissht")
async def ytfuxist(e):
    try:
        await e.answer("Deleted.")
        await e.delete()
    except BaseException:
        await dante_bot.delete_messages(e.chat_id, e.id)


@in_pattern(re.compile("ip_(.*)"), owner=True)
async def in_pm_ans(event):
    from_user = int(event.pattern_match.group(1).strip())
    try:
        warns = U_WARNS[from_user]
    except Exception as e:
        LOGS.info(e)
        warns = "?"
    try:
        msg_ = WARN_MSGS[from_user]
    except KeyError:
        msg_ = "**Pesan Keamanan {OWNER_NAME}**"
    wrns = f"{warns}/{WARNS}"
    buttons = [
        [
            Button.inline("Peringatan", data=f"admin_only{from_user}"),
            Button.inline(wrns, data=f"don_{wrns}"),
        ]
    ]
    include_media = True
    mime_type, res = None, None
    cont = None
    try:
        ext = PMPIC.split(".")[-1].lower()
    except (AttributeError, IndexError):
        ext = None
    if ext in ["img", "jpg", "png"]:
        _type = "photo"
        mime_type = "image/jpg"
    elif ext in ["mp4", "mkv", "gif"]:
        mime_type = "video/mp4"
        _type = "gif"
    else:
        try:
            res = resolve_bot_file_id(PMPIC)
        except ValueError:
            pass
        if res:
            res = [
                await event.builder.document(
                    res,
                    title="Inline PmPermit",
                    description="[↻ꝛɪᴢ](https://t.me/riizzvbss)",
                    text=msg_,
                    buttons=buttons,
                    link_preview=False,
                )
            ]
        else:
            _type = "article"
            include_media = False
    if not res:
        if include_media:
            cont = types.InputWebDocument(PMPIC, 0, mime_type, [])
        res = [
            event.builder.article(
                title="Inline PMPermit.",
                type=_type,
                text=msg_,
                description="[↻ꝛɪᴢ](https://t.me/riizzvbss)",
                include_media=include_media,
                buttons=buttons,
                thumb=cont,
                content=cont,
            )
        ]
    await event.answer(res, switch_pm="• dante •", switch_pm_param="start")


@callback(re.compile("admin_only(.*)"), from_users=[dante_bot.uid])
async def _admin_tools(event):
    chat = int(event.pattern_match.group(1).strip())
    await event.edit(
        buttons=[
            [
                Button.inline("Setujui", data=f"approve_{chat}"),
                Button.inline("Blokir", data=f"block_{chat}"),
            ],
            [Button.inline("Kembali", data=f"pmbk_{chat}")],
        ],
    )


@callback(re.compile("don_(.*)"))
async def _mejik(e):
    data = e.pattern_match.group(1).strip().decode("utf-8").split("/")
    text = "👮‍♂ Peringatan Hitungan : " + data[0]
    text += "\n🤖 Jumlah Peringatan Total : " + data[1]
    await e.answer(text, alert=True)


@callback(re.compile("pmbk_(.*)"))
async def edt(event):
    from_user = int(event.pattern_match.group(1).strip())
    try:
        warns = U_WARNS[from_user]
    except Exception as e:
        LOGS.info(str(e))
        warns = "0"
    wrns = f"{warns}/{WARNS}"
    await event.edit(
        buttons=[
            [
                Button.inline("Peringatan", data=f"admin_only{from_user}"),
                Button.inline(wrns, data=f"don_{wrns}"),
            ]
        ],
    )
