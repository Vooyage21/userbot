# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

from asyncio import sleep

from telethon.errors import MessageDeleteForbiddenError, MessageNotModifiedError
from telethon.tl.custom import Message
from telethon.tl.types import MessageService

# edit or reply


async def eor(event, text=None, time=None, link_preview=False, edit_time=None, **args):
    reply_to = event.reply_to_msg_id or event
    if event.out and not isinstance(event, MessageService):
        if edit_time:
            await sleep(edit_time)
        if "file" in args and args["file"] and not event.media:
            await event.delete()
            ok = await event.client.send_message(
                event.chat_id,
                text,
                link_preview=link_preview,
                reply_to=reply_to,
                **args
            )
        else:
            try:
                ok = await event.edit(text, link_preview=link_preview, **args)
            except MessageNotModifiedError:
                ok = event
    else:
        ok = await event.client.send_message(
            event.chat_id, text, link_preview=link_preview, reply_to=reply_to, **args
        )

    if time:
        await sleep(time)
        return await ok.delete()
    return ok


async def eod(event, text=None, **kwargs):
    kwargs["time"] = kwargs.get("time", 8)
    return await eor(event, text, **kwargs)


async def _try_delete(event):
    try:
        return await event.delete()
    except (MessageDeleteForbiddenError):
        pass
    except BaseException as er:
        from . import LOGS

        LOGS.error("Kesalahan saat Menghapus Pesan..")
        LOGS.exception(er)


setattr(Message, "eor", eor)
setattr(Message, "try_delete", _try_delete)
