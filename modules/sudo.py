# dante - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/dante/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/dante/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Sudo**

๏ **Perintah:** `addsudo`
◉ **Keterangan:** Tambahkan Pengguna Sudo dengan membalas ke pengguna atau menggunakan <spasi> userid yang terpisah

๏ **Perintah:** `delsudo`
◉ **Keterangan:** Hapus Pengguna Sudo dengan membalas ke pengguna atau menggunakan <spasi> userid yang terpisah

๏ **Perintah:** `listsudo`
◉ **Keterangan:** Daftar semua pengguna sudo.
"""

from dante._misc import sudoers
from telethon.tl.types import User

from . import dante_bot, dante_cmd, get_string, inline_mention, udB


@dante_cmd(pattern="addsudo( (.*)|$)", fullsudo=False)
async def _(dante):
    inputs = dante.pattern_match.group(1).strip()
    if dante.reply_to_msg_id:
        replied_to = await dante.get_reply_message()
        id = replied_to.sender_id
        name = await replied_to.get_sender()
    elif inputs:
        try:
            id = await dante.client.parse_id(inputs)
        except ValueError:
            try:
                id = int(inputs)
            except ValueError:
                id = inputs
        try:
            name = await dante.client.get_entity(int(id))
        except BaseException:
            name = None
    elif dante.is_private:
        id = dante.chat_id
        name = await dante.get_chat()
    else:
        return await dante.eor(get_string("sudo_1"), time=5)
    if name and isinstance(name, User) and (name.bot or name.verified):
        return await dante.eor(get_string("sudo_4"))
    name = inline_mention(name) if name else f"`{id}`"
    if id == dante_bot.uid:
        mmm = get_string("sudo_2")
    elif id in sudoers():
        mmm = f"{name} `sudah menjadi Pengguna SUDO ...`"
    else:
        udB.set_key("SUDO", "True")
        key = sudoers()
        key.append(id)
        udB.set_key("SUDOS", key)
        mmm = f"**Ditambahkan** {name} **sebagai Pengguna SUDO**"
    await dante.eor(mmm, time=5)


@dante_cmd(pattern="delsudo( (.*)|$)", fullsudo=False)
async def _(dante):
    inputs = dante.pattern_match.group(1).strip()
    if dante.reply_to_msg_id:
        replied_to = await dante.get_reply_message()
        id = replied_to.sender_id
        name = await replied_to.get_sender()
    elif inputs:
        try:
            id = await dante.client.parse_id(inputs)
        except ValueError:
            try:
                id = int(inputs)
            except ValueError:
                id = inputs
        try:
            name = await dante.client.get_entity(int(id))
        except BaseException:
            name = None
    elif dante.is_private:
        id = dante.chat_id
        name = await dante.get_chat()
    else:
        return await dante.eor(get_string("sudo_1"), time=5)
    name = inline_mention(name) if name else f"`{id}`"
    if id not in sudoers():
        mmm = f"{name} `bukan Pengguna SUDO ...`"
    else:
        key = sudoers()
        key.remove(id)
        udB.set_key("SUDOS", key)
        mmm = f"**DIHAPUS** {name} **dari Pengguna SUDO(s)**"
    await dante.eor(mmm, time=5)


@dante_cmd(
    pattern="listsudo$",
)
async def _(dante):
    sudos = sudoers()
    if not sudos:
        return await dante.eor(get_string("sudo_3"), time=5)
    msg = ""
    for i in sudos:
        try:
            name = await dante.client.get_entity(int(i))
        except BaseException:
            name = None
        if name:
            msg += f"• {inline_mention(name)} ( `{i}` )\n"
        else:
            msg += f"• `{i}` -> Pengguna tidak valid\n"
    m = udB.get_key("SUDO") or True
    if not m:
        m = "[False](https://graph.org/dante-11-29)"
    return await dante.eor(
        f"**SUDO MODE : {m}\n\nList of SUDO Users :**\n{msg}", link_preview=False
    )
