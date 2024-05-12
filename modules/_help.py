# dante - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/dante/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/dante/blob/main/LICENSE/>.

from dante.dB._core import HELP, LIST
from dante.fns.tools import cmd_regex_replace
from telethon.errors.rpcerrorlist import (BotInlineDisabledError,
                                          BotMethodInvalidError,
                                          BotResponseTimeoutError)
from telethon.tl.custom import Button

from . import HNDLR, LOGS, asst, dante_cmd, get_string

_main_help_menu = [
    [
        Button.inline(get_string("help_4"), data="uh_Official_"),
    ],
]


dante_cmd(pattern="[hH][eE][lL][pP]( (.*)|$)")
async def _help(dante):
    plug = dante.pattern_match.group(1).strip()
    chat = await dante.get_chat()
    if plug:
        try:
            if plug in HELP["Official"]:
                output = f"**Plugin** - `{plug}`\n"
                for i in HELP["Official"][plug]:
                    output += i
                output += "\n© dante"
                await dante.eor(output)
            else:
                try:
                    x = get_string("help_11").format(plug)
                    for d in LIST[plug]:
                        x += HNDLR + d
                        x += "\n"
                    x += "\n© dante"
                    await dante.eor(x)
                except BaseException:
                    file = None
                    compare_strings = []
                    for file_name in LIST:
                        compare_strings.append(file_name)
                        value = LIST[file_name]
                        for j in value:
                            j = cmd_regex_replace(j)
                            compare_strings.append(j)
                            if j.strip() == plug:
                                file = file_name
                                break
                    if not file:
                        # the enter command/plugin name is not found
                        text = f"`{plug}` is not a valid plugin!"
                        if best_match := next(
                            (
                                _
                                for _ in compare_strings
                                if plug in _ and not _.startswith("_")
                            ),
                            None,
                        ):
                            text += f"\nDid you mean `{best_match}`?"
                        return await dante.eor(text)
                    output = f"**Perintah** `{plug}` **ditemukan dalam** - `{file}`\n"
                    if file in HELP["Official"]:
                        for i in HELP["Official"][file]:
                            output += i
                    output += "\n© dante"
                    await dante.eor(output)
        except BaseException as er:
            LOGS.exception(er)
            await dante.eor("Error 🤔 occured.")
    else:
        try:
            results = await dante.client.inline_query(asst.me.username, "dante")
        except BotMethodInvalidError:
            z = []
            for x in LIST.values():
                z.extend(x)
            cmd = len(z) + 10
            return await dante.reply(
                get_string("inline_4").format(
                    OWNER_NAME,
                    len(HELP["Official"]),
                    cmd,
                ),
                buttons=_main_help_menu,
            )
        except BotResponseTimeoutError:
            return await dante.eor(
                get_string("help_2").format(HNDLR),
            )
        except BotInlineDisabledError:
            return await dante.eor(get_string("help_3"))
        await results[0].click(chat.id, reply_to=dante.reply_to_msg_id, hide_via=True)
        await dante.delete()
