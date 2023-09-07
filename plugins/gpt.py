# OreO


"""
**Get Answers from Chat GPT**
> No need of any API key.

**• Example: **
> `{i}gpt How to get a url in Python`
"""

from io import BytesIO
from . import async_searcher, LOGS, oreo_cmd


@oreo_cmd(pattern="gpt( ([\s\S]*)|$)")
async def chatgpt(e):
    query = e.pattern_match.group(2)
    reply = await e.get_reply_message()
    if not query:
        if reply and reply.text:
            query = reply.message
    if not query:
        return await e.eor("`Gimme a Question to ask from ChatGPT`")

    oro = await e.eor("__Generating answer...__")
    payloads = {
        "message": query,
        "chat_mode": "assistant",
        "dialog_messages": "[{'bot': '', 'user': ''}]"
    }
    try:
        response = await async_searcher(
            "https://api.safone.me/chatgpt",
            post=True,
            json=payloads,
            re_json=True,
            headers = {"Content-Type": "application/json"},
        )
        if not (response and "message" in response):
            LOGS.error(response)
            raise ValueError("Invalid Response from Server")

        response = response.get("message")
        if len(response + query) < 4080:
            to_edit = (
                f"<b>Query:</b>\n~ <i>{query}</i>\n\n<b>ChatGPT:</b>\n~ <i>{response}</i>"
            )
            await oro.edit(to_edit, parse_mode="html")
            return
        with BytesIO(response.encode()) as file:
            file.name = "gpt_response.txt"
            await e.client.send_file(
                e.chat_id, file, caption=f"`{query[:1020]}`", reply_to=e.reply_to_msg_id
            )
        await oro.try_delete()
    except Exception as exc:
        LOGS.exception(exc)
        await oro.edit(f"**Ran into an Error:** \n`{exc}`" )