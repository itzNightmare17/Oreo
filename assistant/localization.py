# Oreo - UserBot


import re

from . import (
    Button,
    OREConfig,
    callback,
    get_back_button,
    get_languages,
    get_string,
    udB,
)


@callback("lang", owner=True)
async def setlang(event):
    languages = get_languages()
    tored = [
        Button.inline(
            f"{languages[ore]['natively']} [{ore.lower()}]",
            data=f"set_{ore}",
        )
        for ore in languages
    ]
    buttons = list(zip(tored[::2], tored[1::2]))
    if len(tored) % 2 == 1:
        buttons.append((tored[-1],))
    buttons.append([Button.inline("« Back", data="mainmenu")])
    await event.edit(get_string("ast_4"), buttons=buttons)


@callback(re.compile(b"set_(.*)"), owner=True)
async def settt(event):
    lang = event.data_match.group(1).decode("UTF-8")
    languages = get_languages()
    OREConfig.lang = lang
    udB.del_key("language") if lang == "en" else udB.set_key("language", lang)
    await event.edit(
        f"Your language has been set to {languages[lang]['natively']} [{lang}].",
        buttons=get_back_button("lang"),
    )
