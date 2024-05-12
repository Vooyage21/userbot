

from . import LOG_CHANNEL, Button, asst, dante_cmd, eor, get_string

REPOMSG = """
Nyari apa bg?
"""

RP_BUTTONS = [
    [
        Button.url(get_string("bot_3"), "https://t.me/StreamSupportMp3"),
    ],
    [Button.url("Support", "t.me/StreamSupportMp3")],
]

AYSTRING = """🎇 **Terima kasih telah mengunakan dante-Userbot**

• Here, are the Some Basic stuff from, where you can Know, about its Usage."""


@dante_cmd(pattern="repo")
async def usedante(rs):
    button = Button.inline("Start >>", "initft_2")
    msg = await asst.send_message(
        rs.chat_id,
        AYSTRING,
        file="https://mallucampaign.in/images/img_1715419813.jpg",
        buttons=button,
    )
    if not (rs.chat_id == LOG_CHANNEL and rs.client._bot):
        await eor(rs, f"**[Click Here]({msg.message_link})**")
