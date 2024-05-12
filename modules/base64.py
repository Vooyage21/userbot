
"""
✘ **Bantuan Untuk Base64**

๏ **Perintah:** `encode` <berikan pesan/balas pesan>
◉ **Keterangan:** Encode base64.

๏ **Perintah:** `decode` <berikan pesan/balas pesan>
◉ **Keterangan:** Decode base64.
"""

import base64

from . import dante_cmd


@dante_cmd(pattern="encode ?(.*)")
async def encod(e):
    match = e.pattern_match.group(1)
    if not match and e.is_reply:
        gt = await e.get_reply_message()
        if gt.text:
            match = gt.text
    if not (match or e.is_reply):
        return await e.eor("`Beri aku Sesuatu untuk Dikodekan..`")
    byt = match.encode("ascii")
    et = base64.b64encode(byt)
    atc = et.decode("ascii")
    await e.eor(f"**=>> Encoded Text :** `{match}`\n\n**=>> OUTPUT :**\n`{atc}`")


@dante_cmd(pattern="decode ?(.*)")
async def encod(e):
    match = e.pattern_match.group(1)
    if not match and e.is_reply:
        gt = await e.get_reply_message()
        if gt.text:
            match = gt.text
    if not (match or e.is_reply):
        return await e.eor("`Beri aku Sesuatu untuk Diuraikan..`")
    byt = match.encode("ascii")
    try:
        et = base64.b64decode(byt)
        atc = et.decode("ascii")
        await e.eor(f"**=>> Decoded Text :** `{match}`\n\n**=>> OUTPUT :**\n`{atc}`")
    except Exception as p:
        await e.eor(f"**ERROR :** {str(p)}")
