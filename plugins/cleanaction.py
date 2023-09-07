# Oreo

from . import get_help

__doc__ = get_help("help_cleanaction")


from telethon.utils import get_display_name
from . import get_string, udB, oreo_cmd


@oreo_cmd(pattern="addclean$", admins_only=True)
async def _(e):
    key = udB.get_key("CLEANCHAT") or []
    if e.chat_id in key:
        return await eod(e, get_string("clan_5"))
    key.append(e.chat_id)
    udB.set_key("CLEANCHAT", key)
    await e.eor(get_string("clan_1"), time=5)


@oreo_cmd(pattern="remclean$")
async def _(e):
    key = udB.get_key("CLEANCHAT") or []
    if e.chat_id in key:
        key.remove(e.chat_id)
        udB.set_key("CLEANCHAT", key)
    await e.eor(get_string("clan_2"), time=5)


@oreo_cmd(pattern="listclean$")
async def _(e):
    if k := udB.get_key("CLEANCHAT"):
        o = ""
        for x in k:
            try:
                title = get_display_name(await e.client.get_entity(x))
            except BaseException:
                title = get_string("clan_3")
            o += f"{x} {title}\n"
        return await e.eor(o)
    await e.eor(get_string("clan_4"), time=5)
