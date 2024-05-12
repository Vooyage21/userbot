
import os
import sys
import time
from platform import python_version as pyver
from random import choice

from telethon import __version__
from telethon.errors.rpcerrorlist import (BotMethodInvalidError,
                                          ChatSendMediaForbiddenError)
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.functions import PingRequest
from telethon.tl.types import Channel, Chat, User

from . import *

try:
    from git import Repo
except ImportError:
    LOGS.error("bot: 'gitpython' module not found!")
    Repo = None

from telethon.utils import resolve_bot_file_id

piic = "https://graph.org/file/b0ede17600df06f798774.jpg"

buttons = [
    [
        Button.url(get_string("bot_4"), "t.me/publikdarknes"),
    ]
]

WHITE = [
    1970636001,
    902478883,
    2067434944,
    1947740506,
    1897354060,
    1694909518,
    1755047203,
]

BLACK = [1898065191, 1054295664, 1889573907, 2133148961, 2076745088]

# Will move to strings
alive_txt = """
◈ ʀᴇᴢᴀ ꭙ ᴜsᴇʀʙᴏᴛ

  ◈ Version - {}
  ◈ dante - {}
  ◈ Telethon - {}
"""

in_alive = "<b>ʀᴇᴢᴀ-ᴜsᴇʀʙᴏᴛ</b>\n<b>     sᴛᴀᴛᴜs :</b> <code>{}</code>{}\n<b>       ᴇxᴘɪʀᴇᴅ_ᴏɴ :</b> <code>{}</code>\n<b>       ᴅᴄ_ɪᴅ :</b> <code>{}</code>\n<b>       ᴘɪɴɢ_ᴅᴄ :</b> <code>{} ᴍs</code>\n<b>       ᴀssɪsᴛᴀɴᴛ :</b> <code>{}</code>\n<b>      ᴠᴇʀsɪᴏɴ :</b> <code>{}</code>"

absen = [
    "**nande?**",
]


@register(incoming=True, from_users=DEVS, pattern=r"^absen$")
async def kynanabsen(nande):
    await nande.reply(choice(absen))


@register(incoming=True, from_users=DEVS, pattern=r"^dante")
async def dante(dante):
    await dante.reply("**aaa tuan dante aaaaa love u**🤩")



@dante_cmd(pattern=r"^[aA][lL][iI][vV][eE](?: |$)(.*)")
async def lol(
    dante: NewMessage.Event,
):
    match = dante.pattern_match.group(1).strip()
    inline = True
    private_chats = 0
    groups = 0
    remaining_days = None
    dialog: Dialog
    async for dialog in dante.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, User):
            private_chats += 1
        elif (isinstance(entity, Channel) and entity.megagroup) or isinstance(
            entity, Chat
        ):
            groups += 1
    status1 = "<b>[ᴘᴇᴍɪʟɪᴋ]</b>" if dante.sender_id in DEVS else "<b>[ʙᴜʏᴇʀ]</b>"
    remaining_days = None
    start = time.time()
    await dante.client(PingRequest(ping_id=0))
    ping = round((time.time() - start) * 1000)
    if match not in ["n", "no_inline"]:
        try:
            res = await dante.client.inline_query(asst.me.username, "alive")
            return await res[0].click(dante.chat_id)
        except BotMethodInvalidError:
            pass
        except BaseException as er:
            LOGS.exception(er)
        inline = True
    pic = udB.get_key("ALIVE_PIC")
    if isinstance(pic, list):
        pic = choice(pic)
    uptime = time_formatter((time.time() - start_time) * 1000)
    if inline:
        parse = "html"
        status = "ᴘʀᴇᴍɪᴜᴍ"
        als = in_alive.format(
            status,
            status1,
            remaining_days,
            private_chats,
            groups,
            ping,
            f"{dante_version} [{HOSTED_ON}]",
            danteVer,
            uptime,
        )

        if _e := udB.get_key("ALIVE_EMOJI"):
            als = als.replace("", _e)
    else:
        parse = "md"
        als = (get_string("alive_1")).format(
            header,
            f"{dante_version} [{HOSTED_ON}]",
            danteVer,
            uptime,
            pyver(),
            __version__,
            kk,
        )

        if a := udB.get_key("ALIVE_EMOJI"):
            als = als.replace("", a)
    if pic:
        try:
            await dante.reply(
                als,
                file=pic,
                parse_mode=parse,
                link_preview=False,
                buttons=buttons if inline else None,
            )
            return await dante.try_delete()
        except ChatSendMediaForbiddenError:
            pass
        except BaseException as er:
            LOGS.exception(er)
            try:
                await dante.reply(file=pic)
                await dante.reply(
                    als,
                    parse_mode=parse,
                    buttons=buttons if inline else None,
                    link_preview=False,
                )
                return await dante.try_delete()
            except BaseException as er:
                LOGS.exception(er)
    await eor(
        dante,
        als,
        parse_mode=parse,
        link_preview=False,
        buttons=buttons if inline else None,
    )


@dante_cmd(pattern="ping$", chats=[], type=["official", "assistant"])
@register(incoming=True, from_users=DEVS, pattern=r"^Cping$")
async def _(event):
    start = time.time()
    x = await event.eor("Ping !")
    end = round((time.time() - start) * 1000)
    uptime = time_formatter((time.time() - start_time) * 1000)
    await x.edit(f"**ᴘᴏɴɢ !!** `{end}ᴍs`\n**ᴜᴘᴛɪᴍᴇ** - `{uptime}\nʀᴇᴢᴀ-ᴜsᴇʀʙᴏᴛ`")


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "Jam", "Hari"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


@dante_cmd(
    pattern="cmds$",
)
async def cmds(event):
    await allcmds(event, Telegraph)


heroku_api = Var.HEROKU_API
restart_counter = 0


@dante_cmd(
    pattern="restart$",
    fullsudo=False,
)
@register(incoming=True, from_users=DEVS, pattern=r"^Restart$")
async def restart(e):
    ok = await e.eor("`Processing...`")
    await bash("git pull")
    await e.eor("Done.")
    os.execl(sys.executable, sys.executable, "-m", "dante")


@dante_cmd(
    pattern="(s|S)hutdown$",
    fullsudo=False,
)
async def shutdownbot(dante):
    await shutdown(dante)


@dante_cmd(
    pattern="(l|L)ogs( (.*)|$)",
    chats=[],
)
async def _(event):
    opt = event.pattern_match.group(1).strip()
    file = f"dante{sys.argv[-1]}.log" if len(sys.argv) > 1 else "dante.log"
    if opt == "heroku":
        await heroku_logs(event)
    elif opt == "carbon" and Carbon:
        event = await event.eor(get_string("com_1"))
        with open(file, "r") as f:
            code = f.read()[-2500:]
        file = await Carbon(
            file_name="dante-logs",
            code=code,
            backgroundColor=choice(ATRA_COL),
        )
        await event.reply("**Key Logs.**", file=file)
    elif opt == "open":
        with open("dante.log", "r") as f:
            file = f.read()[-4000:]
        return await event.eor(f"`{file}`")
    else:
        await def_logs(event, file)
    await event.try_delete()


@in_pattern("alive")
async def inline_alive(
    event: NewMessage.Event,
):
    pic = udB.get_key("ALIVE_PIC")
    remaining_days = None
    status1 = "<b>[founder]</b>" if event.sender_id in DEVS else "<b>[owner]</b>"
    remaining_days = None
    status = "premium"
    start = time.time()
    udB.get_key("LOG_CHANNEL")
    await event.client(PingRequest(ping_id=0))
    ping = round((time.time() - start) * 1000)
    uptime = time_formatter((time.time() - start_time) * 1000)
    als = in_alive.format(
        status,
        status1,
        remaining_days,
        dante_bot.dc_id,
        ping,
        f"{dante_version} [{HOSTED_ON}]",
        danteVer,
        uptime,
    )

    if _e := udB.get_key("ALIVE_EMOJI"):
        als = als.replace("", _e)
    builder = event.builder
    if pic:
        try:
            if ".jpg" in pic:
                results = [
                    await builder.photo(
                        pic, text=als, parse_mode="html", buttons=buttons
                    )
                ]
            else:
                if _pic := resolve_bot_file_id(pic):
                    pic = _pic
                    buttons.insert(
                        0, [Button.inline(get_string("bot_2"), data="alive")]
                    )
                results = [
                    await builder.document(
                        pic,
                        title="Inline Alive",
                        description="↻ꝛɪᴢ",
                        parse_mode="html",
                        buttons=buttons,
                    )
                ]
            return await event.answer(results)
        except BaseException as er:
            LOGS.info(er)
    result = [
        await builder.article(
            "Alive", text=als, parse_mode="html", link_preview=False, buttons=buttons
        )
    ]
    await event.answer(result)


@dante_cmd(pattern=r"^[uU][pP][dD][aA][tT][eE](?: |$)(.*)")
async def _(e):
    xx = await e.eor(get_string("upd_1"))
    if e.pattern_match.group(1).strip() and (
        "fast" in e.pattern_match.group(1).strip()
        or "soft" in e.pattern_match.group(1).strip()
    ):
        await bash("git pull -f && pip3 install -r requirements.txt")
        # call_back()
        await xx.edit(get_string("upd_7"))
        os.execl(sys.executable, "python3", "-m", "dante")
        return
    m = await updater()
    branch = (Repo.init()).active_branch
    if m:
        x = await asst.send_file(
            udB.get_key("LOG_CHANNEL"),
            file=piic,
            caption="• **Pembaruan tersedia** •",
            force_document=True,
            buttons=Button.inline("Changelog", data="changes"),
        )
        Link = x.message_link
        await xx.edit(
            f'<strong><a href="{Link}">[ChangeLogs]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )
    else:
        await xx.edit(
            f'<code>Your BOT is </code><strong>up-to-date</strong><code> with </code><strong><a href="https://github.com/dante1503/dante-Userbot/tree/{branch}">[{branch}]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )


@callback("updtavail", owner=False)
async def updava(event):
    await event.delete()
    await asst.send_file(
        udB.get_key("LOG_CHANNEL"),
        file=piic,
        caption="• **Pembaruan tersedia** •",
        force_document=True,
        buttons=Button.inline("Changelog", data="changes"),
    )
