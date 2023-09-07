# Oreo - UserBot


from datetime import datetime as dt
from .. import udB


def get_stuff():
    return udB.get_key("AFK_DB") or []


def add_afk(msg, media_type, media):
    time = dt.now().strftime("%b %d %Y %I:%M:%S%p")
    udB.set_key("AFK_DB", [msg, media_type, media, time])
    return


def is_afk():
    afk = get_stuff()
    if afk:
        start_time = dt.strptime(afk[3], "%b %d %Y %I:%M:%S%p")
        afk_since = str(dt.now().replace(microsecond=0) - start_time)
        return afk[0], afk[1], afk[2], afk_since
    return False


def del_afk():
    return udB.del_key("AFK_DB")
