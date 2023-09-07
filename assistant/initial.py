# Oreo - UserBot


import re

from . import *

STRINGS = {
    1: """🎇 **Thanks for Deploying Oreo Userbot!**

• Here, are the Some Basic stuff from, where you can Know, about its Usage.""",
    2: """🎉** About Oreo**

🧿 Oreo is Pluggable and powerful Telethon Userbot, made in Python from Scratch. It is Aimed to Increase Security along with Addition of Other Useful Features.

❣ Made by **@bad_Oreo**""",
    3: """**💡• FAQs •**

-> [Username Tracker](https://t.me/OreoUpdates/22)
-> [Keeping Custom Addons Repo](https://t.me/OreoUpdates/26)
-> [Disabling Deploy message](https://t.me/OreoUpdates/25)
-> [Setting up TimeZone](https://t.me/OreoUpdates/20)
-> [About Inline PmPermit](https://t.me/OreoUpdates/19)
-> [About Dual Mode](https://t.me/OreoUpdates/16)
-> [Custom Thumbnail](https://t.me/OreoUpdates/13)
-> [About FullSudo](https://t.me/OreoUpdates/11)
-> [Setting Up PmBot](https://t.me/OreoUpdates/4)
-> [Also Check](https://t.me/OreoUpdates/14)

**• To Know About Updates**
  - Join @OreoSupportChat.""",
    4: f"""• `To Know All Available Commands`

  - `{HNDLR}help`
  - `{HNDLR}cmds`""",
    5: """• **For Any Other Query or Suggestion**
  - Move to **@OreoSupportChat**.

• Thanks for Reaching till END.""",
}


@callback(re.compile("initft_(\\d+)"))
async def init_depl(e):
    CURRENT = int(e.data_match.group(1))
    if CURRENT == 5:
        return await e.edit(
            STRINGS[5],
            buttons=Button.inline("<< Back", "initbk_4"),
            link_preview=False,
        )

    await e.edit(
        STRINGS[CURRENT],
        buttons=[
            Button.inline("<<", f"initbk_{str(CURRENT - 1)}"),
            Button.inline(">>", f"initft_{str(CURRENT + 1)}"),
        ],
        link_preview=False,
    )


@callback(re.compile("initbk_(\\d+)"))
async def ineiq(e):
    CURRENT = int(e.data_match.group(1))
    if CURRENT == 1:
        return await e.edit(
            STRINGS[1],
            buttons=Button.inline("Start Back >>", "initft_2"),
            link_preview=False,
        )

    await e.edit(
        STRINGS[CURRENT],
        buttons=[
            Button.inline("<<", f"initbk_{str(CURRENT - 1)}"),
            Button.inline(">>", f"initft_{str(CURRENT + 1)}"),
        ],
        link_preview=False,
    )
