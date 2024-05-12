
import re

from dante import _dante_cache
from telethon.errors.rpcerrorlist import UserNotParticipantError

from . import *


@dante_cmd(pattern="d(kick|ban)", manager=True, require="ban_users")
async def dowj(e):
    replied = await e.get_reply_message()
    if replied:
        user = replied.sender_id
    else:
        return await e.eor("Balas ke pesan...")
    try:
        await replied.delete()
        if e.pattern_match.group(1).strip() == "kick":
            await e.client.kick_participant(e.chat_id, user)
            te = "Kicked"
        else:
            await e.client.edit_permissions(e.chat_id, user, view_messages=False)
            te = "Banned"
        await e.eor(f"{te} Successfully!")
    except Exception as E:
        await e.eor(str(E))


@callback(re.compile("cc_(.*)"), func=_dante_cache.get("admin_callback"))
async def callback_(event):
    data = event.data_match.group(1).decode("utf-8")
    if data not in _dante_cache.get("admin_callback", {}):
        return
    try:
        perm = await event.client.get_permissions(event.chat_id, event.sender_id)
    except UserNotParticipantError:
        return await event.answer("Join the Group First!", alert=True)
    if not perm.is_admin:
        return await event.answer("You are not an Admin!", alert=True)
    _dante_cache["admin_callback"].update({data: (event.sender, perm)})
    await event.answer("Verification Done!")
    await event.delete()
