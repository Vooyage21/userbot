# dante - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/dante/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/dante/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Limit**

๏ **Perintah:** `limit`
◉ **Keterangan:** Periksa Anda terbatas atau tidak.
"""

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import dante_cmd


@dante_cmd(pattern="(L|l)imit$")
async def demn(dante):
    chat = "@SpamBot"
    msg = await dante.eor("Memeriksa Jika Anda Terbatas...")
    async with dante.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(incoming=True, from_users=178220800)
            )
            await conv.send_message("/start")
            response = await response
            await dante.client.send_read_acknowledge(chat)
        except YouBlockedUserError:
            await msg.edit("Silakan Buka Blokir @SpamBot ")
            return
        await msg.edit(f"~ {response.message.message}")
