"""
✘ **Bantuan Untuk Welcome**

๏ **Perintah:** `savwel` <berikan pesan/balas pesan>
◉ **Keterangan:** Set welcome message in the current chat.

๏ **Perintah:** `rmwel`
◉ **Keterangan:** Delete the welcome in the current chat.

๏ **Perintah:** `getwel`
◉ **Keterangan:** Get the welcome message in the current chat.

๏ **Perintah:** `savgod` <berikan pesan/balas pesan>
◉ **Keterangan:** Set goodbye message in the current chat.

๏ **Perintah:** `rmgod`
◉ **Keterangan:** Delete the goodbye in the current chat.

๏ **Perintah:** `getgod`
◉ **Keterangan:** Get the goodbye message in the current chat.
"""
import os

from dante.dB.greetings_db import (add_goodbye, add_welcome, delete_goodbye,
                                  delete_welcome, get_goodbye, get_welcome)
from dante.fns.tools import create_tl_btn, format_btn, get_msg_button
from telegraph import upload_file as uf
from telethon.utils import pack_bot_file_id

from . import *
from ._inline import something

Note = "\n\nNote: `{group}`, `{count}`, `{name}`, `{fullname}`, `{username}`, `{userid}` can be used as formatting parameters.\n\n"


@dante_cmd(pattern="savwel", groups_only=True)
async def setwel(event):
    x = await event.eor(get_string("com_1"))
    r = await event.get_reply_message()
    btn = format_btn(r.buttons) if (r and r.buttons) else None
    try:
        text = event.text.split(maxsplit=1)[1]
    except IndexError:
        text = r.text if r else None
    if r and r.media:
        wut = mediainfo(r.media)
        if wut.startswith(("pic", "gif")):
            dl = await r.download_media()
            variable = uf(dl)
            os.remove(dl)
            m = f"https://graph.org{variable[0]}"
        elif wut == "video":
            if r.media.document.size > 8 * 1000 * 1000:
                return await eor(x, get_string("com_4"), time=5)
            dl = await r.download_media()
            variable = uf(dl)
            os.remove(dl)
            m = f"https://graph.org{variable[0]}"
        elif wut == "web":
            m = None
        else:
            m = pack_bot_file_id(r.media)
        if r.text:
            txt = r.text
            if not btn:
                txt, btn = get_msg_button(r.text)
            add_welcome(event.chat_id, txt, m, btn)
        else:
            add_welcome(event.chat_id, None, m, btn)
        await eor(x, get_string("grt_1"))
    elif text:
        if not btn:
            txt, btn = get_msg_button(text)
        add_welcome(event.chat_id, txt, None, btn)
        await eor(x, get_string("grt_1"))
    else:
        await eor(x, get_string("grt_3"), time=5)


@dante_cmd(pattern="rmwel", groups_only=True)
async def clearwel(event):
    if not get_welcome(event.chat_id):
        return await event.eor(get_string("grt_4"), time=5)
    delete_welcome(event.chat_id)
    await event.eor(get_string("grt_5"), time=5)


@dante_cmd(pattern="getwel", groups_only=True)
async def listwel(event):
    wel = get_welcome(event.chat_id)
    if not wel:
        return await event.eor(get_string("grt_4"), time=5)
    msgg, med = wel["welcome"], wel["media"]
    if wel.get("button"):
        btn = create_tl_btn(wel["button"])
        return await something(event, msgg, med, btn)
    await event.reply(f"**Welcome Note in this chat**\n\n`{msgg}`", file=med)
    await event.delete()


@dante_cmd(pattern="savgod", groups_only=True)
async def setgb(event):
    x = await event.eor(get_string("com_1"))
    r = await event.get_reply_message()
    btn = format_btn(r.buttons) if (r and r.buttons) else None
    try:
        text = event.text.split(maxsplit=1)[1]
    except IndexError:
        text = r.text if r else None
    if r and r.media:
        wut = mediainfo(r.media)
        if wut.startswith(("pic", "gif")):
            dl = await r.download_media()
            variable = uf(dl)
            os.remove(dl)
            m = f"https://graph.org{variable[0]}"
        elif wut == "video":
            if r.media.document.size > 8 * 1000 * 1000:
                return await eor(x, get_string("com_4"), time=5)
            dl = await r.download_media()
            variable = uf(dl)
            os.remove(dl)
            m = f"https://graph.org{variable[0]}"
        elif wut == "web":
            m = None
        else:
            m = pack_bot_file_id(r.media)
        if r.text:
            txt = r.text
            if not btn:
                txt, btn = get_msg_button(r.text)
            add_goodbye(event.chat_id, txt, m, btn)
        else:
            add_goodbye(event.chat_id, None, m, btn)
        await eor(x, "`Goodbye note saved`")
    elif text:
        if not btn:
            txt, btn = get_msg_button(text)
        add_goodbye(event.chat_id, txt, None, btn)
        await eor(x, "`Goodbye note saved`")
    else:
        await eor(x, get_string("grt_7"), time=5)


@dante_cmd(pattern="rmgod", groups_only=True)
async def clearwgb(event):
    if not get_goodbye(event.chat_id):
        return await event.eor(get_string("grt_6"), time=5)
    delete_goodbye(event.chat_id)
    await event.eor("`Goodbye Note Deleted`", time=5)


@dante_cmd(pattern="getgod", groups_only=True)
async def listgd(event):
    wel = get_goodbye(event.chat_id)
    if not wel:
        return await event.eor(get_string("grt_6"), time=5)
    msgg = wel["goodbye"]
    med = wel["media"]
    if wel.get("button"):
        btn = create_tl_btn(wel["button"])
        return await something(event, msgg, med, btn)
    await event.reply(f"**Goodbye Note in this chat**\n\n`{msgg}`", file=med)
    await event.delete()
