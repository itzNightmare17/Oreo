# Oreo - UserBot


import asyncio
import os
import random
import shutil
import time
from random import randint

from ..configs import Var

try:
    from pytz import timezone
except ImportError:
    timezone = None

from telethon.errors import (
    ChannelsTooMuchError,
    ChatAdminRequiredError,
    MessageIdInvalidError,
    MessageNotModifiedError,
    UserNotParticipantError,
)
from telethon.tl.custom import Button
from telethon.tl.functions.channels import (
    CreateChannelRequest,
    EditAdminRequest,
    EditPhotoRequest,
    InviteToChannelRequest,
)
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatPhotoEmpty,
    InputChatUploadedPhoto,
    InputMessagesFilterDocument,
)
from telethon.utils import get_peer_id
from decouple import config, RepositoryEnv
from .. import LOGS, OREConfig
from ..fns.helper import download_file, inline_mention, updater

db_url = 0


async def autoupdate_local_database():
    from .. import Var, asst, udB, oreo_bot

    global db_url
    db_url = (
        udB.get_key("TGDB_URL") or Var.TGDB_URL or oreo_bot._cache.get("TGDB_URL")
    )
    if db_url:
        _split = db_url.split("/")
        _channel = _split[-2]
        _id = _split[-1]
        try:
            await asst.edit_message(
                int(_channel) if _channel.isdigit() else _channel,
                message=_id,
                file="database.json",
                text="**Do not delete this file.**",
            )
        except MessageNotModifiedError:
            return
        except MessageIdInvalidError:
            pass
    try:
        LOG_CHANNEL = (
            udB.get_key("LOG_CHANNEL")
            or Var.LOG_CHANNEL
            or asst._cache.get("LOG_CHANNEL")
            or "me"
        )
        msg = await asst.send_message(
            LOG_CHANNEL, "**Do not delete this file.**", file="database.json"
        )
        asst._cache["TGDB_URL"] = msg.message_link
        udB.set_key("TGDB_URL", msg.message_link)
    except Exception as ex:
        LOGS.error(f"Error on autoupdate_local_database: {ex}")


def update_envs():
    """Update Var. attributes to udB"""
    from .. import udB
    _envs = [*list(os.environ)]
    if ".env" in os.listdir("."):
        [_envs.append(_) for _ in list(RepositoryEnv(config._find_file(".")).data)]
    for envs in _envs:
        if (
            envs in ["LOG_CHANNEL", "BOT_TOKEN", "BOTMODE", "DUAL_MODE", "language"]
            or envs in udB.keys()
        ):
            if _value := os.environ.get(envs):
                udB.set_key(envs, _value)
            else:
                udB.set_key(envs, config.config.get(envs))


async def startup_stuff():
    from .. import udB

    x = ["resources/auth", "resources/downloads"]
    for x in x:
        if not os.path.isdir(x):
            os.mkdir(x)

    CT = udB.get_key("CUSTOM_THUMBNAIL")
    if CT:
        path = "resources/extras/thumbnail.jpg"
        OREConfig.thumb = path
        try:
            await download_file(CT, path)
        except Exception as er:
            LOGS.exception(er)
    elif CT is False:
        OREConfig.thumb = None
    GT = udB.get_key("GDRIVE_AUTH_TOKEN")
    if GT:
        with open("resources/auth/gdrive_creds.json", "w") as t_file:
            t_file.write(GT)

    if udB.get_key("AUTH_TOKEN"):
        udB.del_key("AUTH_TOKEN")

    MM = udB.get_key("MEGA_MAIL")
    MP = udB.get_key("MEGA_PASS")
    if MM and MP:
        with open(".megarc", "w") as mega:
            mega.write(f"[Login]\nUsername = {MM}\nPassword = {MP}")

    TZ = udB.get_key("TIMEZONE")
    if TZ and timezone:
        try:
            timezone(TZ)
            os.environ["TZ"] = TZ
            time.tzset()
        except AttributeError as er:
            LOGS.debug(er)
        except BaseException:
            LOGS.critical(
                "Incorrect Timezone ,\nCheck Available Timezone From Here https://graph.org/Oreo-08-21-2\nSo Time is Default UTC"
            )
            os.environ["TZ"] = "UTC"
            time.tzset()


async def autobot():
    from .. import udB, oreo_bot

    if udB.get_key("BOT_TOKEN"):
        return
    await oreo_bot.start()
    LOGS.info("MAKING A TELEGRAM BOT FOR YOU AT @BotFather, Kindly Wait")
    who = oreo_bot.me
    name = who.first_name + "'s Bot"
    if who.username:
        username = who.username + "_bot"
    else:
        username = "oreo_" + (str(who.id))[5:] + "_bot"
    bf = "@BotFather"
    await oreo_bot(UnblockRequest(bf))
    await oreo_bot.send_message(bf, "/cancel")
    await asyncio.sleep(1)
    await oreo_bot.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    isdone = (await oreo_bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("That I cannot do.") or "20 bots" in isdone:
        LOGS.critical(
            "Please make a Bot from @BotFather and add it's token in BOT_TOKEN, as an env var and restart me."
        )
        import sys

        sys.exit(1)
    await oreo_bot.send_message(bf, name)
    await asyncio.sleep(1)
    isdone = (await oreo_bot.get_messages(bf, limit=1))[0].text
    if not isdone.startswith("Good."):
        await oreo_bot.send_message(bf, "My Assistant Bot")
        await asyncio.sleep(1)
        isdone = (await oreo_bot.get_messages(bf, limit=1))[0].text
        if not isdone.startswith("Good."):
            LOGS.critical(
                "Please make a Bot from @BotFather and add it's token in BOT_TOKEN, as an env var and restart me."
            )
            import sys

            sys.exit(1)
    await oreo_bot.send_message(bf, username)
    await asyncio.sleep(1)
    isdone = (await oreo_bot.get_messages(bf, limit=1))[0].text
    await oreo_bot.send_read_acknowledge("botfather")
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = "oreo_" + (str(who.id))[6:] + str(ran) + "_bot"
        await oreo_bot.send_message(bf, username)
        await asyncio.sleep(1)
        isdone = (await oreo_bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("Done!"):
        token = isdone.split("`")[1]
        udB.set_key("BOT_TOKEN", token)
        await enable_inline(oreo_bot, username)
        LOGS.info(
            f"Done. Successfully created @{username} to be used as your assistant bot!"
        )
    else:
        LOGS.info(
            "Please Delete Some Of your Telegram bots at @Botfather or Set Var BOT_TOKEN with token of a bot"
        )

        import sys

        sys.exit(1)


async def autopilot():
    from .. import asst, udB, oreo_bot

    channel = udB.get_key("LOG_CHANNEL")
    new_channel = None
    if channel:
        try:
            chat = await oreo_bot.get_entity(channel)
        except BaseException as err:
            LOGS.exception(err)
            udB.del_key("LOG_CHANNEL")
            channel = None
    if not channel:

        async def _save(exc):
            udB._cache["LOG_CHANNEL"] = oreo_bot.me.id
            await asst.send_message(
                oreo_bot.me.id, f"Failed to Create Log Channel due to {exc}.."
            )

        if oreo_bot._bot:
            msg_ = "'LOG_CHANNEL' not found! Add it in order to use 'BOTMODE'"
            LOGS.error(msg_)
            return await _save(msg_)
        LOGS.info("Creating a Log Channel for You!")
        try:
            r = await oreo_bot(
                CreateChannelRequest(
                    title="My Oreo Logs",
                    about="My Oreo Log Group\n\n Join @OreoSupportChat",
                    megagroup=True,
                ),
            )
        except ChannelsTooMuchError as er:
            LOGS.critical(
                "You Are in Too Many Channels & Groups , Leave some And Restart The Bot"
            )
            return await _save(str(er))
        except BaseException as er:
            LOGS.exception(er)
            LOGS.info(
                "Something Went Wrong , Create A Group and set its id on config var LOG_CHANNEL."
            )

            return await _save(str(er))
        new_channel = True
        chat = r.chats[0]
        channel = get_peer_id(chat)
        udB.set_key("LOG_CHANNEL", channel)
    assistant = True
    try:
        await oreo_bot.get_permissions(int(channel), asst.me.username)
    except UserNotParticipantError:
        try:
            await oreo_bot(InviteToChannelRequest(int(channel), [asst.me.username]))
        except BaseException as er:
            LOGS.info("Error while Adding Assistant to Log Channel")
            LOGS.exception(er)
            assistant = False
    except BaseException as er:
        assistant = False
        LOGS.exception(er)
    if assistant and new_channel:
        try:
            achat = await asst.get_entity(int(channel))
        except BaseException as er:
            achat = None
            LOGS.info("Error while getting Log channel from Assistant")
            LOGS.exception(er)
        if achat and not achat.admin_rights:
            rights = ChatAdminRights(
                add_admins=True,
                invite_users=True,
                change_info=True,
                ban_users=True,
                delete_messages=True,
                pin_messages=True,
                anonymous=False,
                manage_call=True,
            )
            try:
                await oreo_bot(
                    EditAdminRequest(
                        int(channel), asst.me.username, rights, "Assistant"
                    )
                )
            except ChatAdminRequiredError:
                LOGS.info(
                    "Failed to promote 'Assistant Bot' in 'Log Channel' due to 'Admin Privileges'"
                )
            except BaseException as er:
                LOGS.info("Error while promoting assistant in Log Channel..")
                LOGS.exception(er)
    if isinstance(chat.photo, ChatPhotoEmpty):
        photo, _ = await download_file(
            "https://graph.org/file/5d391857a93f929ecc8f1.jpg", "channelphoto.jpg"
        )
        ll = await oreo_bot.upload_file(photo)
        try:
            await oreo_bot(
                EditPhotoRequest(int(channel), InputChatUploadedPhoto(ll))
            )
        except BaseException as er:
            LOGS.exception(er)
        os.remove(photo)


# customize assistant


async def customize():
    from .. import asst, udB, oreo_bot

    rem = None
    try:
        chat_id = udB.get_key("LOG_CHANNEL")
        if asst.me.photo:
            return
        LOGS.info("Customising Ur Assistant Bot in @BOTFATHER")
        UL = f"@{asst.me.username}"
        if not oreo_bot.me.username:
            sir = oreo_bot.me.first_name
        else:
            sir = f"@{oreo_bot.me.username}"
        file = random.choice(
            [
                "https://graph.org/file/5ab97a090b07aeafa4091.jpg",
                "https://graph.org/file/cf8f48c0fd029c3ff85b0.jpg",
                "resources/extras/oreo_assistant.jpg",
            ]
        )
        if not os.path.exists(file):
            file, _ = await download_file(file, "profile.jpg")
            rem = True
        msg = await asst.send_message(
            chat_id, "**Auto Customisation** Started on @Botfather"
        )
        await asyncio.sleep(1)
        await oreo_bot.send_message("botfather", "/cancel")
        await asyncio.sleep(1)
        await oreo_bot.send_message("botfather", "/setuserpic")
        await asyncio.sleep(1)
        isdone = (await oreo_bot.get_messages("botfather", limit=1))[0].text
        if isdone.startswith("Invalid bot"):
            LOGS.info("Error while trying to customise assistant, skipping...")
            return
        await oreo_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await oreo_bot.send_file("botfather", file)
        await asyncio.sleep(2)
        await oreo_bot.send_message("botfather", "/setabouttext")
        await asyncio.sleep(1)
        await oreo_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await oreo_bot.send_message(
            "botfather", f"✨ Hello ✨!! I'm Assistant Bot of {sir}"
        )
        await asyncio.sleep(2)
        await oreo_bot.send_message("botfather", "/setdescription")
        await asyncio.sleep(1)
        await oreo_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await oreo_bot.send_message(
            "botfather",
            f"✨ Powerful Oreo Assistant Bot ✨\n✨ Master ~ {sir} ✨\n\n✨ Powered By ~ @bad_OreO ✨",
        )
        await asyncio.sleep(2)
        await msg.edit("Completed **Auto Customisation** at @BotFather.")
        if rem:
            os.remove(file)
        LOGS.info("Customisation Done")
    except Exception as e:
        LOGS.exception(e)


async def plug(plugin_channels):
    from .. import oreo_bot
    from .utils import load_addons

    if oreo_bot._bot:
        LOGS.info("Plugin Channels can't be used in 'BOTMODE'")
        return
    if os.path.exists("addons") and not os.path.exists("addons/.git"):
        shutil.rmtree("addons")
    if not os.path.exists("addons"):
        os.mkdir("addons")
    if not os.path.exists("addons/__init__.py"):
        with open("addons/__init__.py", "w") as f:
            f.write("from plugins import *\n\nbot = oreo_bot")
    LOGS.info("• Loading Plugins from Plugin Channel(s) •")
    for chat in plugin_channels:
        LOGS.info(f"{'•'*4} {chat}")
        try:
            async for x in oreo_bot.iter_messages(
                chat, search=".py", filter=InputMessagesFilterDocument, wait_time=10
            ):
                plugin = "addons/" + x.file.name.replace("_", "-").replace("|", "-")
                if not os.path.exists(plugin):
                    await asyncio.sleep(0.6)
                    if x.text == "#IGNORE":
                        continue
                    plugin = await x.download_media(plugin)
                    try:
                        load_addons(plugin)
                    except Exception as e:
                        LOGS.info(f"Oreo - PLUGIN_CHANNEL - ERROR - {plugin}")
                        LOGS.exception(e)
                        os.remove(plugin)
        except Exception as er:
            LOGS.exception(er)


# some stuffs
# edit

async def fetch_ann():
    from .. import asst, udB
    from ..fns.tools import async_searcher

    get_ = udB.get_key("OLDANN") or []
    chat_id = udB.get_key("LOG_CHANNEL")

    try:
        updts = await async_searcher(
            "https://oreo-api.vercel.app/announcements", post=True, re_json=True
        )
        for upt in updts:
            key = list(upt.keys())[0]
            if key not in get_:
                cont = upt[key]
                if isinstance(cont, dict) and cont.get("lang"):
                    if cont["lang"] != (udB.get_key("language") or "en"):
                        continue
                    cont = cont["msg"]
                if isinstance(cont, str):
                    await asst.send_message(chat_id, cont)
                elif isinstance(cont, dict) and cont.get("chat"):
                    await asst.forward_messages(chat_id, cont["msg_id"], cont["chat"])
                else:
                    LOGS.info(cont)
                    LOGS.info(
                        "Invalid Type of Announcement Detected!\nMake sure you are on latest version.."
                    )
                get_.append(key)
        udB.set_key("OLDANN", get_)
    except Exception as er:
        LOGS.exception(er)


async def ready():
    from .. import asst, udB, oreo_bot

    chat_id = udB.get_key("LOG_CHANNEL")
    spam_sent = None
    if not udB.get_key("INIT_DEPLOY"):  # Detailed Message at Initial Deploy
        MSG = """🎇 **Thanks for Deploying Oreo Userbot!**
• Here, are the Some Basic stuff from, where you can Know, about its Usage."""
        PHOTO = "https://graph.org/file/a61337021b052c0797fdf.jpg"
        BTTS = Button.inline("• Click to Start •", "initft_2")
        udB.set_key("INIT_DEPLOY", "Done")
    else:
        MSG = f"**OreO has been deployed!**\n➖➖➖➖➖➖➖➖➖➖\n**UserMode**: {inline_mention(oreo_bot.me)}\n**Assistant**: @{asst.me.username}\n➖➖➖➖➖➖➖➖➖➖\n**Support**: @OreoSupportChat\n➖➖➖➖➖➖➖➖➖➖"
        BTTS, PHOTO = None, None
        prev_spam = udB.get_key("LAST_UPDATE_LOG_SPAM")
        if prev_spam:
            try:
                await oreo_bot.delete_messages(chat_id, int(prev_spam))
            except Exception as E:
                LOGS.info("Error while Deleting Previous Update Message :" + str(E))
        if await updater():
            BTTS = Button.inline("Update Available", "updtavail")

    try:
        spam_sent = await asst.send_message(chat_id, MSG, file=PHOTO, buttons=BTTS)
    except ValueError as e:
        try:
            await (await oreo_bot.send_message(chat_id, str(e))).delete()
            spam_sent = await asst.send_message(chat_id, MSG, file=PHOTO, buttons=BTTS)
        except Exception as g:
            LOGS.info(g)
    except Exception as el:
        LOGS.info(el)
        try:
            spam_sent = await oreo_bot.send_message(chat_id, MSG)
        except Exception as ef:
            LOGS.exception(ef)
    if spam_sent and not spam_sent.media:
        udB.set_key("LAST_UPDATE_LOG_SPAM", spam_sent.id)
    await fetch_ann()


async def WasItRestart(udb):
    key = udb.get_key("_RESTART")
    if not key:
        return
    from .. import asst, oreo_bot

    try:
        data = key.split("_")
        who = asst if data[0] == "bot" else oreo_bot
        await who.edit_message(
            int(data[1]), int(data[2]), "__»Restarted Successfully...__"
        )
    except Exception as er:
        LOGS.exception(er)
    udb.del_key("_RESTART")


def _version_changes(udb):
    for _ in [
        "BOT_USERS",
        "BOT_BLS",
        "VC_SUDOS",
        "SUDOS",
        "CLEANCHAT",
        "LOGUSERS",
        "PLUGIN_CHANNEL",
        "CH_SOURCE",
        "CH_DESTINATION",
        "BROADCAST",
    ]:
        key = udb.get_key(_)
        if key and str(key)[0] != "[":
            key = udb.get(_)
            new_ = [
                int(z) if z.isdigit() or (z.startswith("-") and z[1:].isdigit()) else z
                for z in key.split()
            ]
            udb.set_key(_, new_)


async def enable_inline(oreo_bot, username):
    bf = "BotFather"
    await oreo_bot.send_message(bf, "/setinline")
    await asyncio.sleep(1)
    await oreo_bot.send_message(bf, f"@{username}")
    await asyncio.sleep(1)
    await oreo_bot.send_message(bf, "Search")
    await oreo_bot.send_read_acknowledge(bf)
