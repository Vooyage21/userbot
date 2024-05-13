# dante - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/dante/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/dante/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Nulis**

๏ **Perintah:** `nulis` <berikan pesan/balas pesan>
◉ **Keterangan:** Buat kamu yg males nulis.
"""

import requests
from telethon.errors import ChatSendMediaForbiddenError

from . import *


@dante_cmd(pattern=r"(N|n)ulis( (.*)|$)")
async def handwrite(event):
    reply_msg = await event.get_reply_message()
    text = reply_msg.text if reply_msg else event.pattern_match.group(3)
    m = await event.reply("`Processing...`")
    req = requests.get(f"https://api.sdbots.tk/write?text={text}").url
    try:
        await event.client.send_file(
            event.chat.id,
            req,
            caption=f"**Ditulis Oleh: {inline_mention(event.sender)}**",
        )
    except ChatSendMediaForbiddenError:
        await m.edit("Dilarang mengirim media digrup ini 😥!")
        return
    await m.delete()
