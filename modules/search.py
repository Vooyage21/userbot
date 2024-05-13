# dante - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/dante/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/dante/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Search**

๏ **Perintah:** `google`
◉ **Keterangan:** Cari sesuatu di google.

๏ **Perintah:** `github`
◉ **Keterangan:** Cari tahu profile github

๏ **Perintah:** `gimg`
◉ **Keterangan:** Cari gambar menggunakan google.
"""
import os

import requests
from bs4 import BeautifulSoup as bs

try:
    from PIL import Image
except ImportError:
    Image = None
try:
    import cv2
except ImportError:
    cv2 = None
from telethon.tl.types import DocumentAttributeAudio

from . import *


@dante_cmd(
    pattern="github (.*)",
)
async def gitsearch(event):
    usrname = event.pattern_match.group(1).strip()
    if not usrname:
        return await event.eor(get_string("srch_1"))
    url = f"https://api.github.com/users/{usrname}"
    ay = await async_searcher(url, re_json=True)
    try:
        uname = ay["login"]
        uid = ay["id"]
        upic = f"https://avatars.githubusercontent.com/u/{uid}"
        ulink = ay["html_url"]
        uacc = ay["name"]
        ucomp = ay["company"]
        ublog = ay["blog"]
        ulocation = ay["location"]
        ubio = ay["bio"]
        urepos = ay["public_repos"]
        ufollowers = ay["followers"]
        ufollowing = ay["following"]
    except BaseException:
        return await event.eor(get_string("srch_2"))
    fullusr = f"""
**[GITHUB]({ulink})**
**Name** - {uacc}
**UserName** - {uname}
**ID** - {uid}
**Company** - {ucomp}
**Blog** - {ublog}
**Location** - {ulocation}
**Bio** - {ubio}
**Repos** - {urepos}
**Followers** - {ufollowers}
**Following** - {ufollowing}
"""
    await event.respond(fullusr, file=upic)
    await event.delete()


@dante_cmd(
    pattern="google( (.*)|$)",
    manager=True,
)
async def google(event):
    inp = event.pattern_match.group(1).strip()
    if not inp:
        return await eod(event, get_string("autopic_1"))
    x = await event.eor(get_string("com_2"))
    gs = await google_search(inp)
    if not gs:
        return await eod(x, get_string("autopic_2").format(inp))
    out = ""
    for res in gs:
        text = res["title"]
        url = res["link"]
        des = res["description"]
        out += f" 👉🏻  [{text}]({url})\n`{des}`\n\n"
    omk = f"**Google Search Query:**\n`{inp}`\n\n**Resays:**\n{out}"
    await x.eor(omk, link_preview=False)


@dante_cmd(pattern="gimg( (.*)|$)")
async def goimg(event):
    query = event.pattern_match.group(1).strip()
    if not query:
        return await event.eor(get_string("autopic_1"))
    nn = await event.eor(get_string("com_1"))
    lmt = 5
    if ";" in query:
        try:
            lmt = int(query.split(";")[1])
            query = query.split(";")[0]
        except BaseException:
            pass
    images = await get_google_images(query)
    for img in images[:lmt]:
        try:
            await event.client.send_file(event.chat_id, file=img["original"])
        except Exception as er:
            LOGS.exception(er)
    await nn.delete()


@dante_cmd(pattern="reverse$")
async def reverse(event):
    reply = await event.get_reply_message()
    if not reply:
        return await event.eor("`Reply to an Image`")
    ay = await event.eor(get_string("com_1"))
    dl = await reply.download_media()
    file = await con.convert(dl, convert_to="png")
    img = Image.open(file)
    x, y = img.size
    files = {"encoded_image": (file, open(file, "rb"))}
    grs = requests.post(
        "https://www.google.com/searchbyimage/upload",
        files=files,
        allow_redirects=False,
    )
    loc = grs.headers.get("Location")
    response = await async_searcher(
        loc,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0",
        },
    )
    xx = bs(response, "html.parser")
    div = xx.find_all("div", {"class": "r5a77d"})[0]
    alls = div.find("a")
    link = alls["href"]
    text = alls.text
    await ay.edit(f"`Dimension ~ {x} : {y}`\nSauce ~ [{text}](google.com{link})")
    images = await get_google_images(text)
    for z in images[:2]:
        try:
            await event.client.send_file(
                event.chat_id,
                file=z["original"],
                caption="Similar Images Realted to Search",
            )
        except Exception as er:
            LOGS.exception(er)
    os.remove(file)


@dante_cmd(
    pattern="saavn( (.*)|$)",
)
async def siesace(e):
    song = e.pattern_match.group(1).strip()
    if not song:
        return await e.eor("`Give me Something to Search", time=5)
    eve = await e.eor(f"`Searching for {song} on Saavn...`")
    try:
        data = (await saavn_search(song))[0]
    except IndexError:
        return await eve.eor(f"`{song} not found on saavn.`")
    try:
        title = data["title"]
        url = data["url"]
        img = data["image"]
        duration = data["duration"]
        performer = data["artists"]
    except KeyError:
        return await eve.eor("`Something went wrong.`")
    song, _ = await fast_download(url, filename=f"{title}.m4a")
    thumb, _ = await fast_download(img, filename=f"{title}.jpg")
    song, _ = await e.client.fast_uploader(song, to_delete=True)
    await eve.eor(
        file=song,
        text=f"`{title}`\n`From Saavn`",
        attributes=[
            DocumentAttributeAudio(
                duration=int(duration),
                title=title,
                performer=performer,
            )
        ],
        supports_streaming=True,
        thumb=thumb,
    )
    await eve.delete()
    os.remove(thumb)
