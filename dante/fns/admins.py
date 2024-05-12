# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

import asyncio
import time
import uuid

from telethon import Button
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl import functions, types

try:
    from .. import _ayra_cache
    from .._misc import SUDO_M
except ImportError:
    _ayra_cache = {}
    SUDO_M = None


def ban_time(time_str):
    """Simplify ban time from text"""
    if not any(time_str.endswith(unit) for unit in ("s", "m", "h", "d")):
        time_str += "s"
    unit = time_str[-1]
    time_int = time_str[:-1]
    if not time_int.isdigit():
        raise Exception("Invalid time amount specified.")
    to_return = ""
    if unit == "s":
        to_return = int(time.time() + int(time_int))
    elif unit == "m":
        to_return = int(time.time() + int(time_int) * 60)
    elif unit == "h":
        to_return = int(time.time() + int(time_int) * 60 * 60)
    elif unit == "d":
        to_return = int(time.time() + int(time_int) * 24 * 60 * 60)
    return to_return


# ------------------Admin Check--------------- #


async def _callback_check(event):
    id_ = str(uuid.uuid1()).split("-")[0]
    time.time()
    msg = await event.reply(
        "Klik Tombol Di Bawah Ini untuk membuktikan diri sebagai Admin!",
        buttons=Button.inline("Klik Saya", f"cc_{id_}"),
    )
    if not _ayra_cache.get("admin_callback"):
        _ayra_cache.update({"admin_callback": {id_: None}})
    else:
        _ayra_cache["admin_callback"].update({id_: None})
    while not _ayra_cache["admin_callback"].get(id_):
        await asyncio.sleep(1)
    key = _ayra_cache.get("admin_callback", {}).get(id_)
    del _ayra_cache["admin_callback"][id_]
    return key


async def get_update_linked_chat(event):
    if _ayra_cache.get("LINKED_CHATS") and _ayra_cache["LINKED_CHATS"].get(event.chat_id):
        _ignore = _ayra_cache["LINKED_CHATS"][event.chat_id]["linked_chat"]
    else:
        channel = await event.client(
            functions.channels.GetFullChannelRequest(event.chat_id)
        )
        _ignore = channel.full_chat.linked_chat_id
        if _ayra_cache.get("LINKED_CHATS"):
            _ayra_cache["LINKED_CHATS"].update({event.chat_id: {"linked_chat": _ignore}})
        else:
            _ayra_cache.update(
                {"LINKED_CHATS": {event.chat_id: {"linked_chat": _ignore}}}
            )
    return _ignore


async def admin_check(event, require=None, silent: bool = False):
    if SUDO_M and event.sender_id in SUDO_M.owner_and_sudos():
        return True
    callback = None

    # for Anonymous Admin Support
    if (
        isinstance(event.sender, (types.Chat, types.Channel))
        and event.sender_id == event.chat_id
    ):
        if not require:
            return True
        callback = True
    if isinstance(event.sender, types.Channel):
        _ignore = await get_update_linked_chat(event)
        if _ignore and event.sender.id == _ignore:
            return False
        callback = True
    if callback:
        if silent:
            # work silently, same check is used for antiflood
            # and should not ask for Button Verification.
            return
        get_ = await _callback_check(event)
        if not get_:
            return
        user, perms = get_
        event._sender_id = user.id
        event._sender = user
    else:
        user = event.sender
        try:
            perms = await event.client.get_permissions(event.chat_id, user.id)
        except UserNotParticipantError:
            if not silent:
                await event.reply("Anda harus bergabung dengan obrolan ini terlebih dahulu!")
            return False
    if not perms.is_admin:
        if not silent:
            await event.eor("Hanya Admin yang dapat menggunakan perintah ini!", time=8)
        return
    if require and not getattr(perms, require, False):
        if not silent:
            await event.eor(f"Anda kehilangan hak `{require}`", time=8)
        return False
    return True


# ------------------Lock Unlock----------------


def lock_unlock(query, lock=True):
    """
    `Digunakan dalam plugin kunci`
     Apakah ada cara yang lebih baik untuk melakukan ini?
    """
    rights = types.ChatBannedRights(None)
    _do = lock
    if query == "msgs":
        for i in ["send_messages", "invite_users", "pin_messages" "change_info"]:
            setattr(rights, i, _do)
    elif query == "media":
        setattr(rights, "send_media", _do)
    elif query == "sticker":
        setattr(rights, "send_stickers", _do)
    elif query == "gif":
        setattr(rights, "send_gifs", _do)
    elif query == "games":
        setattr(rights, "send_games", _do)
    elif query == "inline":
        setattr(rights, "send_inline", _do)
    elif query == "polls":
        setattr(rights, "send_polls", _do)
    elif query == "invites":
        setattr(rights, "invite_users", _do)
    elif query == "pin":
        setattr(rights, "pin_messages", _do)
    elif query == "changeinfo":
        setattr(rights, "change_info", _do)
    else:
        return None
    return rights


# ---------------- END ---------------- #
