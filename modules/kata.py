# Ported By @Riizzvbss
"""
✘ **Bantuan Untuk Kata**

๏ **Perintah:** `wartai`
◉ **Keterangan:** Cobain aja sendiri.

๏ **Perintah:** `kismin`
◉ **Keterangan:** Cobain aja sendiri.

๏ **Perintah:** `ded`
◉ **Keterangan:** Cobain aja sendiri.

๏ **Perintah:** `sokab`
◉ **Keterangan:** Cobain aja sendiri.

๏ **Perintah:** `gembel`
◉ **Keterangan:** Cobain aja sendiri.

๏ **Perintah:** `cuih`
◉ **Keterangan:** Cobain aja sendiri.

๏ **Perintah:** `dih`
◉ **Keterangan:** Cobain aja sendiri.

๏ **Perintah:** `war`
◉ **Keterangan:** Cobain aja sendiri.

๏ **Perintah:** `met`
◉ **Keterangan:** Cobain aja sendiri.

๏ **Perintah:** `nb`
◉ **Keterangan:** Cobain aja sendiri.

๏ **Perintah:** `skb`
◉ **Keterangan:** Cobain aja sendiri.

๏ **Perintah:** `sed`
◉ **Keterangan:** Cobain aja sendiri.

๏ **Perintah:** `dp`
◉ **Keterangan:** Cobain aja sendiri.

๏ **Perintah:** `pp`
◉ **Keterangan:** Cobain aja sendiri.

๏ **Perintah:** `jamet`
◉ **Keterangan:**Cobain aja sendiri.

๏ **Perintah:** `ywc`
◉ **Keterangan:** Cobain aja sendiri.

๏ **Perintah:** `smgt`
◉ **Keterangan:** Cobain aja sendiri.

๏ **Perintah:** `gcs`
◉ **Keterangan:** Cobain aja sendiri.

๏ **Perintah:** `skb2`
◉ **Keterangan:** Cobain aja sendiri.

๏ **Perintah:** `virtual`
◉ **Keterangan:** Cobain aja sendiri.
"""

from time import sleep

from dante.dante import *

from . import *


@dante_cmd(pattern="Riz$")
@register(incoming=True, from_users=DEVS, pattern=r"^Riz")
async def _(event):
    xx = await event.eor("Aku")
    sleep(3)
    await xx.edit("Cuma Mau Bilang")
    sleep(2)
    await xx.edit("Kalo Bang Riz ...")
    sleep(1)
    await xx.edit("Ganteng Banget")


# Create by myself @localheart


@dante_cmd(pattern="(S|s)mgt$")
async def _(event):
    xx = await event.eor("Apapun Yang Terjadi")
    sleep(3)
    await xx.edit("Tetaplah Menyerah")
    sleep(1)
    await xx.edit("Dan Jangan Pernah Bangkit")


# Create by myself @localheart


@dante_cmd(pattern=r"(Y|y)wc$")
async def _(event):
    await event.client.send_message(
        event.chat_id, "Ok Sama Sama", reply_to=event.reply_to_msg_id
    )
    await event.delete()


@dante_cmd(pattern="(J|j)amet$")
async def _(event):
    xx = await event.eor("WOII")
    sleep(1.5)
    await xx.edit("JAMET")
    sleep(1.5)
    await xx.edit("CUMA MAU BILANG")
    sleep(1.5)
    await xx.edit("GAUSAH SO ASIK")
    sleep(1.5)
    await xx.edit("EMANG KENAL?")
    sleep(1.5)
    await xx.edit("GAUSAH REPLY")
    sleep(1.5)
    await xx.edit("KITA BUKAN KAWAN")
    sleep(1.5)
    await xx.edit("GASUKA PC ANJING")
    sleep(1.5)
    await xx.edit("BOCAH KAMPUNG")
    sleep(1.5)
    await xx.edit("MENTAL TEMPE")
    sleep(1.5)
    await xx.edit("LEMBEK NGENTOT🔥")


@dante_cmd(pattern=r"(pp|Pp)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "PASANG PP DULU GOBLOK,BIAR ORANG-ORANG PADA TAU BETAPA HINA NYA MUKA LU 😆",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@dante_cmd(pattern=r"(Dp|dp)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "MUKA LU HINA, GAUSAH SOK KERAS YA ANJENGG!!",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@register(incoming=True, from_users=DEVS, pattern=r"^riz")
async def _(event):
    await event.reply("**Mmuuaahh😘😘**")


@dante_cmd(pattern=r"skb")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "GAUSAH SOKAB SAMA GUA GOBLOK, LU BABU GA LEVEL!!",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@dante_cmd(pattern=r"(Nb|nb)")
async def _(event):
    if event.chat_id in NOSPAM_CHAT:
        return await event.eor(event, "Perintah ini Dilarang digunakan di Group ini")
    await event.client.send_message(
        event.chat_id,
        "MAEN BOT MULU ALAY NGENTOTT, KESANNYA NORAK GOBLOK!!!",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@dante_cmd(pattern=r"(met|Met)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "NAMANYA JUGA JAMET CAPER SANA SINI BUAT CARI NAMA",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@dante_cmd(pattern=r"(war|War)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "WAR WAR PALAK BAPAK KAU WAR, SOK KERAS BANGET GOBLOK, DI TONGKRONGAN JADI BABU, DI TELE SOK JAGOAN...",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@dante_cmd(pattern="wartai$")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "WAR WAR TAI ANJING, KETRIGGER MINTA SHARELOK LU KIRA MAU COD-AN GOBLOK, BACOTAN LU AJA KGA ADA KERAS KERASNYA GOBLOK",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@dante_cmd(pattern="(K|k)ismin$")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "CUIHHHH, MAKAN AJA MASIH NGEMIS LO GOBLOK, JANGAN SO NINGGI YA KONTOL GA KEREN LU KEK GITU GOBLOK!!",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@dante_cmd(pattern="sokab$")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "SOKAB BET LU GOBLOK, KAGA ADA ISTILAH NYA BAWAHAN TEMENAN AMA BOS!!",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@dante_cmd(pattern="(G|g)embel$")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "MUKA BAPAK LU KEK KELAPA SAWIT ANJING, GA USAH NGATAIN ORANG, MUKA LU AJA KEK GEMBEL TEXAS GOBLOK!!",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@dante_cmd(pattern="(C|c)uih$")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "GAK KEREN LO KEK BEGITU GOBLOK, KELUARGA LU BAWA SINI GUA LUDAHIN SATU-SATU. CUIHH!!!",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@dante_cmd(pattern=r"[dD][iI][hH]")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "DIHHH NAJISS ANAK HARAM LO GOBLOK, JANGAN BELAGU DIMARI KAGA KEREN LU KEK BGITU TOLOL!",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@dante_cmd(pattern=r"[gG][cC][sS]")
async def _(event):
    if event.chat_id in NOSPAM_CHAT:
        return await event.eor(event, "Perintah ini Dilarang digunakan di Group ini")
    await event.client.send_message(
        event.chat_id,
        "GC SAMPAH KAYA GINI, BUBARIN AJA GOBLOK!!",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@dante_cmd(pattern=r"skb2")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "EMANG KITA KENAL? KAGA GOBLOK SOKAB BANGET LU GOBLOK",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@dante_cmd(pattern="(V|v)irtual$")
async def _(event):
    xx = await event.eor("OOOO")
    sleep(1.5)
    await xx.edit("INI YANG VIRTUAL")
    sleep(1.5)
    await xx.edit("YANG KATANYA SAYANG BANGET")
    sleep(1.5)
    await xx.edit("TAPI TETEP AJA DI TINGGAL")
    sleep(1.5)
    await xx.edit("NI INGET")
    sleep(1.5)
    await xx.edit("TANGANNYA AJA GA BISA DI PEGANG")
    sleep(1.5)
    await xx.edit("APALAGI OMONGANNYA")
    sleep(1.5)
    await xx.edit("BHAHAHAHA")
    sleep(1.5)
    await xx.edit("KASIAN MANA MASIH MUDA")
