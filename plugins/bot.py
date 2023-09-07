# oreo

from . import get_help

__doc__ = get_help("help_bot")

import os
import sys
import time
from platform import python_version as pyver
from random import choice

from telethon import __version__
from telethon.errors.rpcerrorlist import (
    BotMethodInvalidError,
    ChatSendMediaForbiddenError,
)

from pyOreo.version import __version__ as OreVer

from . import HOSTED_ON, LOGS

try:
    from git import Repo
except ImportError:
    LOGS.error("bot: 'gitpython' module not found!")
    Repo = None

from telethon.utils import resolve_bot_file_id

from . import (
    ATRA_COL,
    LOGS,
    OWNER_NAME,
    OREO_IMAGES,
    Button,
    Carbon,
    Telegraph,
    Var,
    allcmds,
    asst,
    bash,
    call_back,
    callback,
    def_logs,
    eor,
    get_string,
    heroku_logs,
    in_pattern,
    inline_pic,
    restart,
    shutdown,
    start_time,
    time_formatter,
    udB,
    oreo_cmd,
    oreo_version,
    updater,
)


def OREPIC():
    return inline_pic() or choice(OREO_IMAGES)


buttons = [
    [
        Button.url(get_string("bot_3"), "https://github.com/itzNightmare17/OREO"),
        Button.url(get_string("bot_4"), "t.me/OreoSupportChat"),
    ]
]

# Will move to strings
alive_txt = """
The OreO Userbot

  ◍ Version - {}
  ◍ Py-Oreo - {}
  ◍ Telethon - {}
"""

in_alive = "{}\n\n🌀 <b>OreO Version -><b> <code>{}</code>\n🌀 <b>PyOreo -></b> <code>{}</code>\n🌀 <b>Python -></b> <code>{}</code>\n🌀 <b>Uptime -></b> <code>{}</code>\n🌀 <b>Branch -></b>[ {} ]\n\n• <b>Creator @bad_OreO</b>"


@callback("alive")
async def alive(event):
    text = alive_txt.format(oreo_version, OreVer, __version__)
    await event.answer(text, alert=True)


@oreo_cmd(
    pattern="alive( (.*)|$)",
)
async def lol(ore):
    match = ore.pattern_match.group(1).strip()
    inline = None
    if match in ["inline", "i"]:
        try:
            res = await ore.client.inline_query(asst.me.username, "alive")
            return await res[0].click(ore.chat_id)
        except BotMethodInvalidError:
            pass
        except BaseException as er:
            LOGS.exception(er)
        inline = True
    pic = udB.get_key("ALIVE_PIC")
    if isinstance(pic, list):
        pic = choice(pic)
    uptime = time_formatter((time.time() - start_time) * 1000)
    header = udB.get_key("ALIVE_TEXT") or get_string("bot_1")
    y = Repo().active_branch
    xx = Repo().remotes[0].config_reader.get("url")
    rep = xx.replace(".git", f"/tree/{y}")
    kk = f" `[{y}]({rep})` "
    if inline:
        kk = f"<a href={rep}>{y}</a>"
        parse = "html"
        als = in_alive.format(
            header,
            f"{oreo_version} [{HOSTED_ON}]",
            OreVer,
            pyver(),
            uptime,
            kk,
        )

        if _e := udB.get_key("ALIVE_EMOJI"):
            als = als.replace("🌀", _e)
    else:
        parse = "md"
        als = (get_string("alive_1")).format(
            header,
            OWNER_NAME,
            f"{oreo_version} [{HOSTED_ON}]",
            OreVer,
            uptime,
            pyver(),
            __version__,
            kk,
        )

        if a := udB.get_key("ALIVE_EMOJI"):
            als = als.replace("✵", a)
    if pic:
        try:
            await ore.reply(
                als,
                file=pic,
                parse_mode=parse,
                link_preview=False,
                buttons=buttons if inline else None,
            )
            return await ore.try_delete()
        except ChatSendMediaForbiddenError:
            pass
        except BaseException as er:
            LOGS.exception(er)
            try:
                await ore.reply(file=pic)
                await ore.reply(
                    als,
                    parse_mode=parse,
                    buttons=buttons if inline else None,
                    link_preview=False,
                )
                return await ore.try_delete()
            except BaseException as er:
                LOGS.exception(er)
    await eor(
        ore,
        als,
        parse_mode=parse,
        link_preview=False,
        buttons=buttons if inline else None,
    )


@oreo_cmd(pattern="ping$", chats=[], type=["official", "assistant"])
async def _(event):
    start = time.time()
    x = await event.eor("•• Pᴏɴɢ ••")
    end = round((time.time() - start) * 1000)
    uptime = time_formatter((time.time() - start_time) * 1000)
    await x.edit(get_string("ping").format(end, uptime))


@oreo_cmd(
    pattern="cmds$",
)
async def cmds(event):
    await allcmds(event, Telegraph)


heroku_api = Var.HEROKU_API


@oreo_cmd(
    pattern="restart$",
    fullsudo=True,
)
async def restartbt(ore):
    ok = await ore.eor(get_string("bot_5"))
    call_back()
    who = "bot" if ore.client._bot else "user"
    udB.set_key("_RESTART", f"{who}_{ore.chat_id}_{ok.id}")
    if heroku_api:
        return await restart(ok)
    await bash("git pull && pip3 install -r requirements.txt")
 #   if len(sys.argv) > 1:
 #       os.execl(sys.executable, sys.executable, "main.py")
 #   else:
    os.execl(sys.executable, sys.executable, "-m", "pyOreo")


@oreo_cmd(
    pattern="shutdown$",
    fullsudo=True,
)
async def shutdownbot(ore):
    await shutdown(ore)


@oreo_cmd(
    pattern="logs( (.*)|$)",
    chats=[],
)
async def _(event):
    opt = event.pattern_match.group(1).strip()
    file = f"oreo{sys.argv[-1]}.log" if len(sys.argv) > 1 else "oreo.log"
    if opt == "heroku":
        await heroku_logs(event)
    elif opt == "carbon" and Carbon:
        event = await event.eor(get_string("com_1"))
        with open(file, "r") as f:
            code = f.read()[-2500:]
        file = await Carbon(
            file_name="oreo-logs",
            code=code,
            backgroundColor=choice(ATRA_COL),
        )
        if isinstance(file, dict):
            await event.eor(f"`{file}`")
            return
        await event.reply("**Oreo Logs.**", file=file)
    elif opt == "open":
        with open("oreo.log", "r") as f:
            file = f.read()[-4000:]
        return await event.eor(f"`{file}`")
    else:
        await def_logs(event, file)
    await event.try_delete()


@in_pattern("alive", owner=True)
async def inline_alive(ore):
    pic = udB.get_key("ALIVE_PIC")
    if isinstance(pic, list):
        pic = choice(pic)
    uptime = time_formatter((time.time() - start_time) * 1000)
    header = udB.get_key("ALIVE_TEXT") or get_string("bot_1")
    y = Repo().active_branch
    xx = Repo().remotes[0].config_reader.get("url")
    rep = xx.replace(".git", f"/tree/{y}")
    kk = f"<a href={rep}>{y}</a>"
    als = in_alive.format(
        header, f"{oreo_version} [{HOSTED_ON}]", OreVer, pyver(), uptime, kk
    )

    if _e := udB.get_key("ALIVE_EMOJI"):
        als = als.replace("🌀", _e)
    builder = ore.builder
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
                        description="Team OreO",
                        parse_mode="html",
                        buttons=buttons,
                    )
                ]
            return await ore.answer(results)
        except BaseException as er:
            LOGS.exception(er)
    result = [
        await builder.article(
            "Alive", text=als, parse_mode="html", link_preview=False, buttons=buttons
        )
    ]
    await ore.answer(result)


@oreo_cmd(pattern="update( (.*)|$)")
async def _(e):
    xx = await e.eor(get_string("upd_1"))
    if e.pattern_match.group(1).strip() and (
        "fast" in e.pattern_match.group(1).strip()
        or "soft" in e.pattern_match.group(1).strip()
    ):
        await bash("git pull -f && pip3 install -r requirements.txt")
        call_back()
        await xx.edit(get_string("upd_7"))
        os.execl(sys.executable, "python3", "-m", "pyOreo")
        # return
    m = await updater()
    branch = (Repo.init()).active_branch
    if m:
        x = await asst.send_file(
            udB.get_key("LOG_CHANNEL"),
            OREPIC(),
            caption="• **Update Available** •",
            force_document=False,
            buttons=Button.inline("Changelogs", data="changes"),
        )
        Link = x.message_link
        await xx.edit(
            f'<strong><a href="{Link}">[ChangeLogs]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )
    else:
        await xx.edit(
            f'<code>Your BOT is </code><strong>up-to-date</strong><code> with </code><strong><a href="https://github.com/itzNightmare17/OREO/tree/{branch}">[{branch}]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )


@callback("updtavail", owner=True)
async def updava(event):
    await event.delete()
    await asst.send_file(
        udB.get_key("LOG_CHANNEL"),
        OREPIC(),
        caption="• **Update Available** •",
        force_document=False,
        buttons=Button.inline("Changelogs", data="changes"),
    )
