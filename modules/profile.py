# dante - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/dante/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/dante/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Profile**

๏ **Perintah:** `setname` <first name/last name>
◉ **Keterangan:** Ubah nama anda.

๏ **Perintah:** `setbio` <balas pesan>
◉ **Keterangan:** Ubah bio anda.

๏ **Perintah:** `setfp` <balas pesan>
◉ **Keterangan:** Ubah foto profil anda.

๏ **Perintah:** `delfp` <jumlah>
◉ **Keterangan:** Hapus satu foto profil, jika tidak ada nilai yang diberikan atau hapus jumlah foto.
"""
import os

from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import (DeletePhotosRequest,
                                          UploadProfilePhotoRequest)

from . import dante_cmd, eod, eor, get_string, mediainfo

TMP_DOWNLOAD_DIRECTORY = "resources/downloads/"

# bio changer


@dante_cmd(pattern="(S|s)etbio( (.*)|$)", fullsudo=False)
async def _(dante):
    ok = await dante.eor("...")
    set = dante.pattern_match.group(1).strip()
    try:
        await dante.client(UpdateProfileRequest(about=set))
        await eod(ok, f"Bio profil diubah menjadi\n`{set}`")
    except Exception as ex:
        await eod(ok, f"Terjadi kesalahan.\n`{str(ex)}`")


# name changer


@dante_cmd(pattern="(S|s)etname ?((.|//)*)", fullsudo=False)
async def _(dante):
    ok = await dante.eor("...")
    names = dante.pattern_match.group(1).strip()
    first_name = names
    last_name = ""
    if "//" in names:
        first_name, last_name = names.split("//", 1)
    try:
        await dante.client(
            UpdateProfileRequest(
                first_name=first_name,
                last_name=last_name,
            ),
        )
        await eod(ok, f"Nama diubah menjadi `{names}`")
    except Exception as ex:
        await eod(ok, f"Terjadi kesalahan.\n`{str(ex)}`")


# profile pic


@dante_cmd(pattern="(s|S)etfp$", fullsudo=False)
async def _(dante):
    if not dante.is_reply:
        return await dante.eor("`Balas ke Media..`", time=5)
    reply_message = await dante.get_reply_message()
    ok = await dante.eor(get_string("com_1"))
    replfile = await reply_message.download_media()
    file = await dante.client.upload_file(replfile)
    try:
        if "pic" in mediainfo(reply_message.media):
            await dante.client(UploadProfilePhotoRequest(file))
        else:
            await dante.client(UploadProfilePhotoRequest(video=file))
        await eod(ok, "`Foto Profil Berhasil Diubah !`")
    except Exception as ex:
        await eod(ok, f"Terjadi kesalahan.\n`{str(ex)}`")
    os.remove(replfile)


# delete profile pic(s)


@dante_cmd(pattern="(D|d)elfp( (.*)|$)", fullsudo=False)
async def remove_profilepic(delpfp):
    ok = await eor(delpfp, "`...`")
    group = delpfp.text[8:]
    if group == "all":
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1
    pfplist = await delpfp.client.get_profile_photos("me", limit=lim)
    await delpfp.client(DeletePhotosRequest(pfplist))
    await eod(ok, f"`Berhasil dihapus {len(pfplist)} gambar profil(s).`")


@dante_cmd(pattern="(p|P)oto( (.*)|$)")
async def gpoto(e):
    dante = e.pattern_match.group(1).strip()
    a = await e.eor(get_string("com_1"))
    just_dl = dante in ["-dl", "--dl"]
    if just_dl:
        dante = None
    if not dante:
        if e.is_reply:
            gs = await e.get_reply_message()
            dante = gs.sender_id
        else:
            dante = e.chat_id
    okla = await e.client.download_profile_photo(dante)
    if not okla:
        return await eor(a, "`Foto Profil Tidak Ditemukan...`")
    if not just_dl:
        await a.delete()
        await e.reply(file=okla)
        return os.remove(okla)
    await a.edit(f"Mengunduh pfp ke [ `{okla}` ].")
