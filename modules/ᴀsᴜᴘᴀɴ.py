"""
✘ **Bantuan Untuk Asupan**

๏ **Perintah:** `asupan`
◉ **Keterangan:** Coba sendiri

๏ **Perintah:** `bokep`
◉ **Keterangan:** Coba sendiri

๏ **Perintah:** `ayang`
◉ **Keterangan:** Coba sendiri

๏ **Perintah:** `ppcp`
◉ **Keterangan:** Coba sendiri

๏ **Perintah:** `ppcp2`
◉ **Keterangan:** Coba sendiri

๏ **Perintah:** `anime`
◉ **Keterangan:** Coba sendiri

๏ **Perintah:** `anime2`
◉ **Keterangan:** Coba sendiri

๏ **Perintah:** `pap`
◉ **Keterangan:** Coba sendiri
"""

from secrets import choice

from telethon.tl.types import (InputMessagesFilterPhotos,
                               InputMessagesFilterVideo)
from telethon.tl.functions.channels import *
from telethon.tl.functions.messages import *
from . import *


@dante_cmd(pattern="[Aa][s][u][p][a][n]$")
async def _(event):
    xx = await eor(event, "`Tunggu Sebentar...`")
    try:
        asupannya = [
            asupan
            async for asupan in event.client.iter_messages(
                "@punyakenkan", filter=InputMessagesFilterVideo
            )
        ]
        await event.client.send_file(
            event.chat_id,
            file=choice(asupannya),
            reply_to=event.reply_to_msg_id,
            caption=f"**Asupan Nya {inline_mention(event.sender)}..**",
        )
        await xx.delete()
    except Exception:
        await xx.edit("**Tidak bisa menemukan video asupan.**")


@dante_cmd(pattern="[Bb][o][k][e][p]$")
async def _(event):
    if event.chat_id in NOSPAM_CHAT:
        return await eor(event, "**Perintah ini Dilarang digunakan di Group ini**")
    xx = await eor(event, "`Tunggu Sebentar...`")
    try:
        bokepnya = [
            bokep
            async for bokep in event.client.iter_messages(
                "@Punyapesulap", filter=InputMessagesFilterVideo
            )
        ]
        ajg = random.choice(bokepnya)
        pler = await event.client.download_media(ajg)
        await event.client.send_file(
            event.chat_id,
            file=pler,
            caption=f"**Coli Mulu {inline_mention(event.sender)}..**",
        )
        await xx.delete()
    except Exception:
        await xx.edit("**Tidak bisa menemukan bokep.**")
    #try:
        #await dante_bot(LeaveChannelRequest(-1001867672427))
    #except BaseException:
        #pass
    


@dante_cmd(pattern="[Aa][y][a][n][g]$")
async def _(event):
    xx = await eor(event, "`Tunggu Sebentar...`")
    try:
        ayangnya = [
            ayang
            async for ayang in event.client.iter_messages(
                "@CeweLogoPack", filter=InputMessagesFilterPhotos
            )
        ]
        await event.client.send_file(
            event.chat_id,
            file=choice(ayangnya),
            reply_to=event.reply_to_msg_id,
            caption=f"**Ayang Nya {inline_mention(event.sender)}..**",
        )
        await xx.delete()
    except Exception:
        await xx.edit("**Tidak bisa menemukan ayang.**")


@dante_cmd(pattern="(ppcp|Ppcp)$")
async def _(event):
    xx = await eor(event, "`Tunggu Sebentar...`")
    try:
        ppcpnya = [
            ppcp
            async for ppcp in event.client.iter_messages(
                "@ppcpcilik", filter=InputMessagesFilterPhotos
            )
        ]
        await event.client.send_file(
            event.chat_id,
            file=choice(ppcpnya),
            reply_to=event.reply_to_msg_id,
            caption=f"**Ppcp Nya {inline_mention(event.sender)}..**",
        )
        await xx.delete()
    except Exception:
        await xx.edit("**Tidak bisa menemukan ppcp.**")


@dante_cmd(pattern="(Ppcp2|ppcp2)$")
async def _(event):
    xx = await eor(event, "`Tunggu Sebentar...`")
    try:
        ajgg = [
            gg
            async for gg in event.client.iter_messages(
                "@mentahanppcp", filter=InputMessagesFilterPhotos
            )
        ]
        await event.client.send_file(
            event.chat_id,
            file=choice(ajgg),
            reply_to=event.reply_to_msg_id,
            caption=f"**Ppcp Nya {inline_mention(event.sender)}..**",
        )
        await xx.delete()
    except Exception:
        await xx.edit("**Tidak bisa menemukan ppcp2.**")


@dante_cmd(pattern="(Anime|anime)$")
async def _(event):
    xx = await eor(event, "`Tunggu Sebentar...`")
    try:
        nimek = [
            nime
            async for nime in event.client.iter_messages(
                "@animehikarixa", filter=InputMessagesFilterPhotos
            )
        ]
        await event.client.send_file(
            event.chat_id,
            file=choice(nimek),
            reply_to=event.reply_to_msg_id,
            caption=f"**Anime Nya {inline_mention(event.sender)}..**",
        )
        await xx.delete()
    except Exception:
        await xx.edit("**Tidak bisa menemukan anime.**")


@dante_cmd(pattern="(anime2|Anime2)$")
async def _(event):
    xx = await eor(event, "`Tunggu Sebentar...`")
    try:
        nimekk = [
            nim
            async for nim in event.client.iter_messages(
                "@animehikarixa", filter=InputMessagesFilterPhotos
            )
        ]
        await event.client.send_file(
            event.chat_id,
            file=choice(nimekk),
            reply_to=event.reply_to_msg_id,
            caption=f"**Anime Nya {inline_mention(event.sender)}..**",
        )
        await xx.delete()
    except Exception:
        await xx.edit("**Tidak bisa menemukan anime2.**")


@dante_cmd(pattern="(pap|Pap)$")
async def _(event):
    xx = await eor(event, "`Tunggu Sebentar...`")
    try:
        papjing = [
            jinglu
            async for jinglu in event.client.iter_messages(
                "@mm_kyran", filter=InputMessagesFilterPhotos
            )
        ]
        await event.client.send_file(
            event.chat_id,
            file=choice(papjing),
            reply_to=event.reply_to_msg_id,
            caption=f"**Pap Nya {inline_mention(event.sender)}..**",
        )
        await xx.delete()
    except Exception:
        await xx.edit("**Tidak bisa menemukan desahan cowo.**")
