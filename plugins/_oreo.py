# oreo

from telethon.errors import (
    BotMethodInvalidError,
    ChatSendInlineForbiddenError,
    ChatSendMediaForbiddenError,
)

from . import LOG_CHANNEL, LOGS, Button, asst, eor, get_string, oreo_cmd

REPOMSG = """
• **OreO USERBOT** •\n
• Repo - [Click Here](https://github.com/itzNightmare17/Oreo)
• Addons - [Click Here](https://github.com/itzNightmare17/OreoAddons)
• Support - @OreoSupportChat
"""

RP_BUTTONS = [
    [
        Button.url(get_string("bot_3"), "https://github.com/itzNightmare17/Oreo"),
        Button.url("Addons", "https://github.com/itzNightmare17/OreoAddons"),
    ],
    [Button.url("Support Group", "t.me/OreoSupportChat")],
]

ORESTRING = """🎇 **Thanks for Deploying OreO Userbot!**

• Here, are the Some Basic stuff from, where you can Know, about its Usage."""


@oreo_cmd(
    pattern="repo$",
    manager=True,
)
async def repify(e):
    try:
        q = await e.client.inline_query(asst.me.username, "")
        await q[0].click(e.chat_id)
        return await e.delete()
    except (
        ChatSendInlineForbiddenError,
        ChatSendMediaForbiddenError,
        BotMethodInvalidError,
    ):
        pass
    except Exception as er:
        LOGS.info(f"Error while repo command : {str(er)}")
    await e.eor(REPOMSG)


@oreo_cmd(pattern="oreo$")
async def useOreo(rs):
    button = Button.inline("Start >>", "initft_2")
    msg = await asst.send_message(
        LOG_CHANNEL,
        ORESTRING,
        file="https://graph.org/file/ef9478d8cf1df77dc68ce.jpg",
        buttons=button,
    )
    if not (rs.chat_id == LOG_CHANNEL and rs.client._bot):
        await eor(rs, f"**[Click Here]({msg.message_link})**")
