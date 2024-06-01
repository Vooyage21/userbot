

"""
✘ **Bantuan Untuk Blacklist**

๏ **Perintah:** `black` <kata>
◉ **Keterangan:** Daftar hitam kan kata didalam grup.

๏ **Perintah:** `white` <kata>
◉ **Keterangan:** Hapus kata dari daftar hitam.

๏ **Perintah:** `listblack`
◉ **Keterangan:** Lihat Semua Daftar Kata Terlarang .
"""

from dante.dB.blacklist_db import (add_blacklist, get_blacklist, list_blacklist,
                                  rem_blacklist)

from . import dante_bot, dante_cmd, events, get_string, udB


@dante_cmd(pattern="black( (.*)|$)", admins_only=True)
async def af(e):
    wrd = e.pattern_match.group(1).strip()
    chat = e.chat_id
    if not (wrd):
        return await e.eor(get_string("blk_1"), time=5)
    wrd = e.text[11:]
    heh = wrd.split(" ")
    for z in heh:
        add_blacklist(int(chat), z.lower())
    dante_bot.add_handler(blacklist, (incoming=True))
    await e.eor(get_string("blk_2").format(wrd))


@dante_cmd(pattern="white( (.*)|$)", admins_only=True)
async def rf(e):
    wrd = e.pattern_match.group(1).strip()
    chat = e.chat_id
    if not wrd:
        return await e.eor(get_string("blk_3"), time=5)
    wrd = e.text[14:]
    heh = wrd.split(" ")
    for z in heh:
        rem_blacklist(int(chat), z.lower())
    await e.eor(get_string("blk_4").format(wrd))


@dante_cmd(pattern="listblack", admins_only=True)
async def lsnote(e):
    if x := list_blacklist(e.chat_id):
        sd = get_string("blk_5")
        return await e.eor(sd + x)
    await e.eor(get_string("blk_6"))


async def blacklist(e):
    if x := get_blacklist(e.chat_id):
        for z in e.text.lower().split():
            for zz in x:
                if z == zz:
                    try:
                        await e.delete()
                        break
                    except BaseException:
                        break


if udB.get_key("BLACKLIST_DB"):
    dante_bot.add_handler(blacklist, (incoming=True))
