# dante - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/dante/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/dante/blob/main/LICENSE/>.

"""
✘ **Bantuan Untuk DM**

๏ **Perintah:** `toaudio` <balas file>
◉ **Keterangan:** Extrak Audio Dari Video.

๏ **Perintah:** `convert` <foto/audio/mp3/gif/voice> <balas ke file>
◉ **Keterangan:** Convert. convert `audio` dengan efek.
 **List Efek :** `bengek`, `jedug`, `echo`, `robot`

๏ **Perintah:** `glitch <balas ke gambar>`
◉ **Keterangan:** Memberikan gif glitchy.

๏ **Perintah:** `invertgif` <balas file>
◉ **Keterangan:** Membuat Gif Terbalik(negative).

๏ **Perintah:** `bwgif` <balas file>
◉ **Keterangan:** Jadikan Gif hitam putih

๏ **Perintah:** `rvgif` <balas file>
◉ **Keterangan:** Balikkan gif

๏ **Perintah:** `vtog` <balas file>
◉ **Keterangan:** Balas Ke Video, Ini akan Membuat Gif
  Video ke Gif.

๏ **Perintah:** `gif` <kata kunci>
◉ **Keterangan:** Mencari gif.

๏ **Perintah:** `size` <balas file>
◉ **Keterangan:** Mendapatkan ukuran media.

๏ **Perintah:** `resize` <number> <number>
◉ **Keterangan:** Ubah ukuran media.
"""

import asyncio
import io
import os
import random
import time

from PIL import Image

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from PIL import Image
except ImportError:
    LOGS.info(f"{__file__}: PIL  not Installed.")
    Image = None

from datetime import datetime as dt

from . import *

opn = []

conv_keys = {
    "img": "png",
    "sticker": "webp",
    "webp": "webp",
    "image": "png",
    "webm": "webm",
    "gif": "gif",
    "json": "json",
    "tgs": "tgs",
}

"""
@dante_cmd(
    pattern="(C|c)onvert( (.*)|$)",
)
async def uconverter(event):
    xx = await event.eor(get_string("com_1"))
    a = await event.get_reply_message()
    if a is None:
        return await event.eor("`Balas ke Media...`")
    input_ = event.pattern_match.group(1).strip()
    b = await a.download_media("resources/downloads/")
    if not b and (a.document and a.document.thumbs):
        b = await a.download_media(thumb=-1)
    if not b:
        return await xx.edit(get_string("cvt_3"))
    try:
        convert = conv_keys[input_]
    except KeyError:
        return await xx.edit(get_string("sts_3").format("gif/img/sticker/webm/webp"))
    file = await con.convert(b, outname="dante", convert_to=convert)
    if file:
        await event.client.send_file(
            event.chat_id, file, reply_to=event.reply_to_msg_id or event.id
        )
        os.remove(file)
    await xx.delete()
"""


@dante_cmd(pattern="convert ?(foto|audio|gif|voice|photo|mp3)? ?(.*)")
async def cevir(event):
    ajg = event.pattern_match.group(1)
    try:
        if len(ajg) < 1:
            await eod(
                event,
                "**Perintah tidak diketahui! ketik** `{}help convert` **bila butuh bantuan**",
                time=30,
            )
            return
    except BaseException:
        await eod(
            event,
            "**Perintah tidak diketahui! ketik** `{}help convert` **bila butuh bantuan**",
            time=30,
        )
        return
    if ajg in ["foto", "photo"]:
        rep_msg = await event.get_reply_message()
        if not event.is_reply or not rep_msg.sticker:
            await eod(event, "`Balas ke stikers...`")
            return
        xxnx = await eor(event, "`Processing...`")
        foto = io.BytesIO()
        foto = await event.client.download_media(rep_msg.sticker, foto)
        im = Image.open(foto).convert("RGB")
        im.save("sticker.png", "png")
        await event.client.send_file(
            event.chat_id,
            "sticker.png",
            reply_to=rep_msg,
        )
        await xxnx.delete()
        os.remove("sticker.png")
    elif ajg in ["sound", "audio"]:
        EFEKTLER = ["bengek", "robot", "jedug", "fast", "echo"]
        efekt = event.pattern_match.group(2)
        if len(efekt) < 1:
            return await eod(
                event,
                "**Efek tidak ditemukan!**\n**Efek yang dapat Anda gunakan:** `bengek/robot/jedug/fast/echo",
                time=30,
            )
        rep_msg = await event.get_reply_message()
        if not event.is_reply or not (rep_msg.voice or rep_msg.audio):
            return await eod(event, "`Balas ke Audio...`")
        xxx = await eor(event, "`Processing...`")
        if efekt in EFEKTLER:
            indir = await rep_msg.download_media()
            KOMUT = {
                "bengek": '-filter_complex "rubberband=pitch=1.5"',
                "robot": "-filter_complex \"afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=512:overlap=0.75\"",
                "jedug": '-filter_complex "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1"',
                "fast": "-filter_complex \"afftfilt=real='hypot(re,im)*cos((random(0)*2-1)*2*3.14)':imag='hypot(re,im)*sin((random(1)*2-1)*2*3.14)':win_size=128:overlap=0.8\"",
                "echo": '-filter_complex "aecho=0.8:0.9:500|1000:0.2|0.1"',
            }
            ses = await asyncio.create_subprocess_shell(
                f"ffmpeg -i '{indir}' {KOMUT[efekt]} output.mp3"
            )
            await ses.communicate()
            await event.client.send_file(
                event.chat_id,
                "output.mp3",
                thumb="resources/extras/logo.jpg",
                reply_to=rep_msg,
            )
            await xxx.delete()
            os.remove(indir)
            os.remove("output.mp3")
        else:
            await xxx.eor(
                "**Efek tidak ditemukan!**\n**Efek yang dapat Anda gunakan:** `bengek/robot/jedug/fast/echo"
            )
    elif ajg == "mp3":
        rep_msg = await event.get_reply_message()
        if not event.is_reply or not rep_msg.video:
            return await eod(event, "**Harap balas ke Video!**")
        xx = await eor(event, "`Processing...`")
        video = io.BytesIO()
        video = await event.client.download_media(rep_msg.video)
        gif = await asyncio.create_subprocess_shell(
            f"ffmpeg -y -i '{video}' -vn -b:a 128k -c:a libmp3lame out.mp3"
        )
        await gif.communicate()
        await xx.eor(
            "**Efek yang Anda tentukan tidak ditemukan!**\n**Efek yang dapat Anda gunakan:** `bengek/robot/jedug/fast/echo`"
        )
        try:
            await event.client.send_file(
                event.chat_id,
                "out.mp3",
                thumb="resources/extras/logo.jpg",
                reply_to=rep_msg,
            )
        except BaseException:
            os.remove(video)
            return await xx.eor("**Gagal Convert...**")
        await xx.delete()
        os.remove("out.mp3")
        os.remove(video)
    else:
        await xx.eor(
            "**Perintah tidak diketahui! ketik** `{}help convert` **bila butuh bantuan**"
        )
        return


@dante_cmd(pattern="toaudio$")
async def makevoice(event):
    if not event.reply_to:
        return await eod(event, "**Mohon Balas Ke Audio atau video**")
    msg = await event.get_reply_message()
    if not event.is_reply or not (msg.audio or msg.video):
        return await eod(event, "**Mohon Balas Ke Audio atau video**")
    xxnx = await eor(event, "`Processing...`")
    dl = msg.file.name
    file = await msg.download_media(dl)
    await xxnx.edit("`Tunggu Sebentar...`")
    await runcmd(
        f"ffmpeg -i '{file}' -map 0:a -codec:a libopus -b:a 100k -vbr on dante.opus"
    )
    await event.client.send_file(
        event.chat_id, file="dante.opus", force_document=False, reply_to=msg
    )
    await xxnx.delete()
    os.remove(file)
    os.remove("dante.opus")


@dante_cmd(pattern="(G|g)litch$")
async def _(e):
    try:
        import glitch_me  # ignore :pylint
    except ModuleNotFoundError:
        await bash(
            "pip install -e git+https://github.com/1Danish-00/glitch_me.git#egg=glitch_me"
        )
    reply = await e.get_reply_message()
    if not reply or not reply.media:
        return await e.eor(get_string("cvt_3"))
    xx = await e.eor(get_string("glitch_1"))
    wut = mediainfo(reply.media)
    if wut.startswith(("pic", "sticker")):
        ok = await reply.download_media()
    elif reply.document and reply.document.thumbs:
        ok = await reply.download_media(thumb=-1)
    else:
        return await xx.eor(get_string("com_4"))
    cmd = f"glitch_me gif --line_count 200 -f 10 -d 50 '{ok}' dante.gif"
    stdout, stderr = await bash(cmd)
    await e.reply(file="dante.gif", force_document=False)
    await xx.delete()
    os.remove(ok)
    os.remove("dante.gif")


@dante_cmd(pattern="(bw|Bw|Invert|invert)$")
async def igif(e):
    match = e.pattern_match.group(1).strip()
    a = await e.get_reply_message()
    if not (a and a.media):
        return await e.eor("`Reply To gif only`", time=5)
    wut = mediainfo(a.media)
    if "gif" not in wut:
        return await e.eor("`Reply To Gif Only`", time=5)
    xx = await e.eor(get_string("com_1"))
    z = await a.download_media()
    if match == "bw":
        cmd = f'ffmpeg -i "{z}" -vf format=gray dante.gif -y'
    else:
        cmd = f'ffmpeg -i "{z}" -vf lutyuv="y=negval:u=negval:v=negval" dante.gif -y'
    try:
        await bash(cmd)
        await e.client.send_file(e.chat_id, "dante.gif", supports_streaming=True)
        os.remove(z)
        os.remove("dante.gif")
        await xx.delete()
    except Exception as er:
        LOGS.info(er)


@dante_cmd(pattern="(R|r)vgif$")
async def reverse_gif(event):
    a = await event.get_reply_message()
    if not (a and a.media) and "video" not in mediainfo(a.media):
        return await e.eor("`Balas ke Video saja`", time=5)
    msg = await event.eor(get_string("com_1"))
    file = await a.download_media()
    await bash(f'ffmpeg -i "{file}" -vf reverse -af areverse reversed.mp4 -y')
    await event.respond("- **Video/GIF Terbalik**", file="reversed.mp4")
    await msg.delete()
    os.remove(file)
    os.remove("reversed.mp4")


@dante_cmd(pattern="(Gif|gif)( (.*)|$)")
async def gifs(dante):
    get = dante.pattern_match.group(1).strip()
    xx = random.randint(0, 5)
    n = 0
    if ";" in get:
        try:
            n = int(get.split(";")[-1])
        except IndexError:
            pass
    if not get:
        return await dante.eor("`gif <query>`")
    m = await dante.eor(get_string("com_2"))
    gifs = await dante.client.inline_query("gif", get)
    if not n:
        await gifs[xx].click(
            dante.chat_id, reply_to=dante.reply_to_msg_id, silent=True, hide_via=True
        )
    else:
        for x in range(n):
            await gifs[x].click(
                dante.chat_id, reply_to=dante.reply_to_msg_id, silent=True, hide_via=True
            )
    await m.delete()


@dante_cmd(pattern="(V|v)tog$")
async def vtogif(e):
    a = await e.get_reply_message()
    if not (a and a.media):
        return await e.eor("`Reply To video only`", time=5)
    wut = mediainfo(a.media)
    if "video" not in wut:
        return await e.eor("`Reply To Video Only`", time=5)
    xx = await e.eor(get_string("com_1"))
    dur = a.media.document.attributes[0].duration
    tt = time.time()
    if int(dur) < 120:
        z = await a.download_media()
        await bash(
            f'ffmpeg -i {z} -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 dante.gif -y'
        )
    else:
        filename = a.file.name
        if not filename:
            filename = "video_" + dt.now().isoformat("_", "seconds") + ".mp4"
        vid = await downloader(filename, a.media.document, xx, tt, get_string("com_5"))
        z = vid.name
        await bash(
            f'ffmpeg -ss 3 -t 100 -i {z} -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 dante.gif'
        )

    await e.client.send_file(e.chat_id, "dante.gif", support_stream=True)
    os.remove(z)
    os.remove("dante.gif")
    await xx.delete()


@dante_cmd(pattern="(size|Size)")
async def size(e):
    r = await e.get_reply_message()
    if not (r and r.media):
        return await e.eor(get_string("ascii_1"))
    k = await e.eor(get_string("com_1"))
    if hasattr(r.media, "document"):
        img = await e.client.download_media(r, thumb=-1)
    else:
        img = await r.download_media()
    im = Image.open(img)
    x, y = im.size
    await k.edit(f"Dimensi Gambar Ini Adalah\n`{x} x {y}`")
    os.remove(img)


@dante_cmd(pattern="(resize|Resize)( (.*)|$)")
async def size(e):
    r = await e.get_reply_message()
    if not (r and r.media):
        return await e.eor(get_string("ascii_1"))
    sz = e.pattern_match.group(1).strip()
    if not sz:
        return await eor(
            "Berikan Beberapa Ukuran Untuk Diubah Ukurannya, Seperti `resize 720 1080` ",
            time=5,
        )
    k = await e.eor(get_string("com_1"))
    if hasattr(r.media, "document"):
        img = await e.client.download_media(r, thumb=-1)
    else:
        img = await r.download_media()
    sz = sz.split()
    if len(sz) != 2:
        return await eor(
            k,
            "Berikan Beberapa Ukuran Untuk Diubah Ukurannya, Seperti `resize 720 1080` ",
            time=5,
        )
    x, y = int(sz[0]), int(sz[1])
    im = Image.open(img)
    ok = im.resize((x, y))
    ok.save(img, format="PNG", optimize=True)
    await e.reply(file=img)
    os.remove(img)
    await k.delete()
