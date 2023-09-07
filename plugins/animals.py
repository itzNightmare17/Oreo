# OreO


"""
✘ Commands Available -

๏ `{i}cat`
◉  Gives a Cat Pic

๏ `{i}dog`
◉  Gives a Dog Pic

"""

import requests
from . import *

@oreo_cmd(pattern="dog$")
async def shibe(event):
    xx = await event.eor("`Processing...`")
    response = requests.get("https://shibe.online/api/shibes").json()
    if not response:
        await event.edit("**Could not find Dog image.**")
        return
    await event.client.send_message(entity=event.chat_id, file=response[0])
    await xx.delete()


@oreo_cmd(pattern="cat$")
async def cats(event):
    xx = await event.eor("`Processing...`")
    response = requests.get("https://shibe.online/api/cats").json()
    if not response:
        await event.edit("**Could not find cat image.**")
        return
    await event.client.send_message(entity=event.chat_id, file=response[0])
    await xx.delete()
#_________
