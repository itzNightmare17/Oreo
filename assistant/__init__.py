# OREO - UserBot
                                     
 
                                                                    
                                                      
                                                                                                                     

from telethon import Button, custom

from plugins import ATRA_COL, InlinePlugin
from pyOreo import *
from pyOreo import _ore_cache
from pyOreo._misc import owner_and_sudos
from pyOreo._misc._assistant import asst_cmd, callback, in_pattern
from pyOreo.fns.helper import *
from pyOreo.fns.tools import get_stored_file
from strings import get_languages, get_string

OWNER_NAME = oreo_bot.full_name
OWNER_ID = oreo_bot.uid

AST_PLUGINS = {}


async def setit(event, name, value):
    try:
        udB.set_key(name, value)
    except BaseException as er:
        LOGS.exception(er)
        return await event.edit("`Something Went Wrong`")


def get_back_button(name):
    return [Button.inline("« Bᴀᴄᴋ", data=f"{name}")]
