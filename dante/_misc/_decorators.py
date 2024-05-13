
import asyncio
import inspect
import re
import sys
from io import BytesIO
from pathlib import Path
from time import gmtime, strftime
from traceback import format_exc

from strings import get_string
from telethon import Button
from telethon import __version__ as telever
from telethon import events
from telethon.errors.common import AlreadyInConversationError
from telethon.errors.rpcerrorlist import (
    AuthKeyDuplicatedError,
    BotInlineDisabledError,
    BotMethodInvalidError,
    ChatSendInlineForbiddenError,
    ChatSendMediaForbiddenError,
    ChatSendStickersForbiddenError,
    FloodWaitError,
    MessageDeleteForbiddenError,
    MessageIdInvalidError,
    MessageNotModifiedError,
    UserIsBotError,
)
from telethon.events import MessageEdited, NewMessage
from telethon.utils import get_displdan_name

from .. import *
from .. import _ignore_eval
from ..dB import DEVS
from ..dB._core import LIST, LOADED
from ..fns.admins import admin_check
from ..fns.helper import bash
from ..fns.helper import time_formatter as tf
from ..version import __version__ as pyver
from ..version import dante_version as dante_ver
from . import SUDO_M, owner_and_sudos
from ._wrappers import eod

MANAGER = udB.get_key("MANAGER")
TAKE_EDITS = udB.get_key("TAKE_EDITS")
black_list_chats = udB.get_key("BLACKLIST_CHATS")
allow_sudo = SUDO_M.should_allow_sudo


def compile_pattern(data, hndlr):
    if data.startswith("^"):
        data = data[1:]
    if data.startswith("."):
        data = data[1:]
    if hndlr in [" ", "NO_HNDLR"]:
        # No Hndlr Feature
        return re.compile("^" + data)
    return re.compile("\\" + hndlr + data)


def dante_cmd(
    pattern=None, manager=False, dante_bot=dante_bot, asst=asst, **kwargs
):
    owner_only = kwargs.get("owner_only", False)
    groups_only = kwargs.get("groups_only", False)
    admins_only = kwargs.get("admins_only", False)
    fullsudo = kwargs.get("fullsudo", False)
    only_devs = kwargs.get("only_devs", False)
    func = kwargs.get("func", lambda e: not e.via_bot_id)

    def decor(dec):
        async def wrapp(dan):
            if not dan.out:
                if owner_only:
                    return
                if dan.sender_id not in owner_and_sudos():
                    return
                if dan.sender_id in _ignore_eval:
                    return await eod(
                        dan,
                        get_string("py_d1"),
                    )
                if fullsudo and dan.sender_id not in SUDO_M.fullsudos:
                    return await eod(dan, get_string("py_d2"), time=15)
            chat = dan.chat
            if hasattr(chat, "title"):
                if (
                    "#noub" in chat.title.lower()
                    and not (chat.admin_rights or chat.creator)
                    and not (dan.sender_id in DEVS)
                ):
                    return
            if admins_only:
                if dan.is_private:
                    return await eod(dan, get_string("py_d3"))
                if not (chat.admin_rights or chat.creator):
                    return await eod(dan, get_string("py_d5"))
            if only_devs and not udB.get_key("I_DEV"):
                return await eod(
                    dan,
                    get_string("py_d4").format(HNDLR),
                    time=10,
                )
            if groups_only and dan.is_private:
                return await eod(dan, get_string("py_d5"))
            try:
                await dec(dan)
            except FloodWaitError as fwerr:
                await asst.send_message(
                    udB.get_key("LOG_CHANNEL"),
                    f"`FloodWaitError:\n{str(fwerr)}\n\nSleeping for {tf((fwerr.seconds + 10)*1000)}`",
                )
                await dante_bot.disconnect()
                await asyncio.sleep(fwerr.seconds + 10)
                await dante_bot.connect()
                await asst.send_message(
                    udB.get_key("LOG_CHANNEL"),
                    "`Bot is working again`",
                )
                return
            except ChatSendInlineForbiddenError:
                return await eod(dan, "`Inline Locked In This Chat.`")
            except (ChatSendMediaForbiddenError, ChatSendStickersForbiddenError):
                return await eod(dan, get_string("py_d8"))
            except (BotMethodInvalidError, UserIsBotError):
                return await eod(dan, get_string("py_d6"))
            except AlreadyInConversationError:
                return await eod(
                    dan,
                    get_string("py_d7"),
                )
            except (BotInlineDisabledError) as er:
                return await eod(dan, f"`{er}`")
            except (
                MessageIdInvalidError,
                MessageNotModifiedError,
                MessageDeleteForbiddenError,
            ) as er:
                LOGS.exception(er)
            except AuthKeyDuplicatedError as er:
                LOGS.exception(er)
                await asst.send_message(
                    udB.get_key("LOG_CHANNEL"),
                    "Session String expired, create new session from 👇",
                    buttons=[
                        Button.url("Bot", "t.me/NdanaStringBot?start="),
                    ],
                )
                sys.exit()
            except events.StopPropagation:
                raise events.StopPropagation
            except KeyboardInterrupt:
                pass
            except Exception as e:
                LOGS.exception(e)
                date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                naam = get_displdan_name(chat)
                ftext = "**dante Client Error:** `Forward this to` @StreamSupportMp3\n\n"
                ftext += "**dante Version:** `" + str(pyver)
                ftext += "`\n**Userbot Version:** `" + str(dante_ver)
                ftext += "`\n**Telethon Version:** `" + str(telever)
                ftext += f"`\n**Hosted At:** `{HOSTED_ON}`\n\n"
                ftext += "--------START dante CRASH LOG--------"
                ftext += "\n**Date:** `" + date
                ftext += "`\n**Group:** `" + str(dan.chat_id) + "` " + str(naam)
                ftext += "\n**Sender ID:** `" + str(dan.sender_id)
                ftext += "`\n**Replied:** `" + str(dan.is_reply)
                ftext += "`\n\n**Event Trigger:**`\n"
                ftext += str(dan.text)
                ftext += "`\n\n**Traceback info:**`\n"
                ftext += str(format_exc())
                ftext += "`\n\n**Error text:**`\n"
                ftext += str(sys.exc_info()[1])
                ftext += "`\n\n--------END dante CRASH LOG--------"
                ftext += "\n\n\n**Last 5 commits:**`\n"

                stdout, stderr = await bash('git log --pretty=format:"%an: %s" -5')
                result = stdout + (stderr or "")

                ftext += f"{result}`"

                if len(ftext) > 4096:
                    with BytesIO(ftext.encode()) as file:
                        file.name = "logs.txt"
                        error_log = await asst.send_file(
                            udB.get_key("LOG_CHANNEL"),
                            file,
                            caption="**dante Client Error:** `Forward this to` @StreamSupportMp3\n\n",
                        )
                else:
                    error_log = await asst.send_message(
                        udB.get_key("LOG_CHANNEL"),
                        ftext,
                    )
                if dan.out:
                    await dan.edit(
                        f"<b><a href={error_log.message_link}>[An error occurred]</a></b>",
                        link_preview=False,
                        parse_mode="html",
                    )

        cmd = None
        blacklist_chats = False
        chats = None
        if black_list_chats:
            blacklist_chats = True
            chats = list(black_list_chats)
        _add_new = allow_sudo and HNDLR != SUDO_HNDLR
        if _add_new:
            if pattern:
                cmd = compile_pattern(pattern, SUDO_HNDLR)
            dante_bot.add_event_handler(
                wrapp,
                NewMessage(
                    pattern=cmd,
                    incoming=True,
                    forwards=False,
                    func=func,
                    chats=chats,
                    blacklist_chats=blacklist_chats,
                ),
            )
        if pattern:
            cmd = compile_pattern(pattern, HNDLR)
        dante_bot.add_event_handler(
            wrapp,
            NewMessage(
                outgoing=True if _add_new else None,
                pattern=cmd,
                forwards=False,
                func=func,
                chats=chats,
                blacklist_chats=blacklist_chats,
            ),
        )
        if TAKE_EDITS:

            def func_(x):
                return not x.via_bot_id and not (x.is_channel and x.chat.broadcast)

            dante_bot.add_event_handler(
                wrapp,
                MessageEdited(
                    pattern=cmd,
                    forwards=False,
                    func=func_,
                    chats=chats,
                    blacklist_chats=blacklist_chats,
                ),
            )
        if manager and MANAGER:
            allow_all = kwargs.get("allow_all", False)
            allow_pm = kwargs.get("allow_pm", False)
            require = kwargs.get("require", None)

            async def manager_cmd(dan):
                if not allow_all and not (await admin_check(dan, require=require)):
                    return
                if not allow_pm and dan.is_private:
                    return
                try:
                    await dec(dan)
                except Exception as er:
                    if chat := udB.get_key("MANAGER_LOG"):
                        text = f"**#MANAGER_LOG\n\nChat:** `{get_displdan_name(dan.chat)}` `{dan.chat_id}`"
                        text += f"\n**Replied :** `{dan.is_reply}`\n**Command :** {dan.text}\n\n**Error :** `{er}`"
                        try:
                            return await asst.send_message(
                                chat, text, link_preview=False
                            )
                        except Exception as er:
                            LOGS.exception(er)
                    LOGS.info(f"• MANAGER [{dan.chat_id}]:")
                    LOGS.exception(er)

            if pattern:
                cmd = compile_pattern(pattern, "/")
            asst.add_event_handler(
                manager_cmd,
                NewMessage(
                    pattern=cmd,
                    forwards=False,
                    incoming=True,
                    func=func,
                    chats=chats,
                    blacklist_chats=blacklist_chats,
                ),
            )
        if DUAL_MODE and not (manager and DUAL_HNDLR == "/"):
            if pattern:
                cmd = compile_pattern(pattern, DUAL_HNDLR)
            asst.add_event_handler(
                wrapp,
                NewMessage(
                    pattern=cmd,
                    incoming=True,
                    forwards=False,
                    func=func,
                    chats=chats,
                    blacklist_chats=blacklist_chats,
                ),
            )
        file = Path(inspect.stack()[1].filename)
        if "addons/" in str(file):
            if LOADED.get(file.stem):
                LOADED[file.stem].append(wrapp)
            else:
                LOADED.update({file.stem: [wrapp]})
        if pattern:
            if LIST.get(file.stem):
                LIST[file.stem].append(pattern)
            else:
                LIST.update({file.stem: [pattern]})
        return wrapp

    return decor
