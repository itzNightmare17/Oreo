# Oreo


"""
✘ **Get Image from Bing !!**
• `{i}bing Monsoon`
• `{i}bing -gif Snowfall ; <count>`
• `{i}bing -line Avengers ; 10`

✘ Available filters:
•  `-gif` - Get GIFs
•  `-nsfw` - show nsfw content.
•  `-line`
•  `-transparent`
•  `-clipart`
"""

import asyncio
import imghdr
from functools import partial
from pathlib import Path
from random import choice, shuffle
import re
from secrets import token_hex
from shutil import rmtree
from urllib.parse import quote_plus, unquote, unquote_plus, urlsplit

import aiohttp

from . import (
    LOGS,
    async_searcher,
    check_filename,
    get_string,
    run_async,
    some_random_headers,
    split_list,
    oreo_cmd,
)


class BingScrapper:
    def __init__(self, query, limit, hide_nsfw=True, filter=None):
        assert bool(query), "No query provided.."
        assert type(limit) == int, "limit must be of type Integer"
        self.query = query
        self.limit = limit
        self.page_counter = 0
        self.hide_nsfw = "on" if bool(hide_nsfw) else "off"
        self.url_args = self._filter_to_args(filter)
        self._valid_exts = tuple(
            ".jpg .jpeg .exif .gif .bmp .png .webp .jpe .tiff".split()
        )
        self.headers = {
            "User-Agent": choice(some_random_headers),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
            "Accept-Encoding": "none",
            "Accept-Language": "en-US,en;q=0.8",
            "Connection": "keep-alive",
        }

    def _filter_to_args(self, shorthand):
        if not shorthand:
            return ""
        shorthand = shorthand.lower()
        if shorthand in ("line", "linedrawing"):
            return "&qft=+filterui:photo-linedrawing"
        elif shorthand == "photo":
            return "&qft=+filterui:photo-photo"
        elif shorthand == "clipart":
            return "&qft=+filterui:photo-clipart"
        elif shorthand in ("gif", "animatedgif"):
            return "&qft=+filterui:photo-animatedgif"
        elif shorthand == "transparent":
            return "&qft=+filterui:photo-transparent"
        else:
            return ""

    @run_async
    def _save_to_file(self, filename, content):
        with open(filename, "wb+") as f:
            f.write(content)

    @staticmethod
    def get_filename_from_url(url, folder):
        if path := urlsplit(url).path:
            filename = Path(path).name
            filename = unquote_plus(filename)
            if len(filename) > 63:
                filename = Path(filename).with_stem(filename[:63])
        else:
            filename = token_hex(nbytes=7)
        return Path(folder).joinpath(filename)

    async def _handle_request(self, filename, response):
        if response.status < 207:
            image_data = await response.read()
            if imghdr.what(None, image_data):
                await self._save_to_file(filename, image_data)

    async def save_image(self, link):
        if re.match(r"^https?://(www.)?bing.com/th/id/OGC", link):
            if re_search := re.search(r"&amp;rurl=(.+)&amp;ehk=", link):
                link = unquote(re_search.group(1))
        filename = self.get_filename_from_url(link, folder=self.output_dir)
        ext = filename.suffix
        if not (ext and ext.lower() in self._valid_exts):
            filename = filename.with_suffix(".jpg")
        if filename.is_file():
            return
        try:
            await async_searcher(
                link,
                raise_for_status=True,
                timeout=aiohttp.ClientTimeout(total=8),
                evaluate=partial(self._handle_request, filename),
            )
        except (
            asyncio.TimeoutError,
            aiohttp.ClientResponseError,
            aiohttp.ClientConnectorCertificateError,
        ):
            pass
        except Exception as exc:
            LOGS.debug(f"Bing: Error in downloading {link}", exc_info=True)

    async def get_links(self):
        cached_urls = set()
        while len(cached_urls) < self.limit:
            extra_args = f"&first={self.page_counter}&count={self.limit}&adlt={self.hide_nsfw}{self.url_args}"
            request_url = f"https://www.bing.com/images/async?q={quote_plus(self.query)}{extra_args}"
            response = await async_searcher(request_url, headers=self.headers)
            if response == "":
                LOGS.info(
                    f"No more Image available for {self.query}. Page - {self.page_counter} | Downloaded - {len(cached_urls)}"
                )
                assert bool(cached_urls), f"No Images for '{self.query}'"
                return self._evaluate_links(cached_urls)

            img_links = re.findall("murl&quot;:&quot;(.*?)&quot;", response)
            for url in img_links:
                cached_urls.add(url)
            self.page_counter += 1

        assert bool(cached_urls), f"No Images for '{self.query}'"
        return self._evaluate_links(cached_urls)

    def _evaluate_links(self, links):
        links = list(links)
        shuffle(links)
        return links[: self.limit]

    async def download(self):
        self.output_dir = check_filename(f"resources/downloads/bing-{self.query}")
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        url_list = await self.get_links()
        dl_list = [url_list] if len(url_list) <= 4 else split_list(url_list, 4)
        for collection in dl_list:
            await asyncio.gather(
                *[self.save_image(url) for url in collection],
                return_exceptions=True,
            )

        return self.output_dir


@oreo_cmd(pattern="bing( (.*)|$)", manager=True)
async def bing_image(e):
    query = e.pattern_match.group(2)
    limit = 8
    if not query and e.reply_to:
        reply = await e.get_reply_message()
        if reply.text:
            query = reply.message
    if not query:
        return await e.eor("`give some text as well..`", time=5)

    msg = await e.eor(get_string("com_1"))
    img_type = "photo"
    arguments = ("doc", "gif", "nsfw", "clipart", "transparent", "line")
    args_dict = {i: False for i in arguments}
    for arg in arguments:
        pattern = re.compile(f"(?i)^ ?-{arg}")
        if re.match(pattern, query):
            re_sub = re.sub(pattern, "", query)
            args_dict[arg] = True
            query = re_sub.lstrip()

    as_doc, nsfw = args_dict.get("doc"), args_dict.get("nsfw")
    for _filter in ("clipart", "transparent", "line", "gif"):
        if args_dict.get(_filter):
            img_type = _filter
    del arguments, args_dict

    if ";" in query:
        query, limit = map(lambda i: i.strip(), query.split(";", maxsplit=1))
        limit = min(int(limit) if limit.isdigit() else 8, 99)

    bing_scp = BingScrapper(
        query=query,
        limit=limit,
        filter=img_type,
        hide_nsfw=not nsfw,
    )
    try:
        out_dir = await bing_scp.download()
        files = list(Path(out_dir).iterdir())
        if not files:
            return await msg.edit("`No files found on Server..`")
    except Exception as exc:
        LOGS.exception(exc)
        return await msg.edit(f"Error while Downloading Media: `{exc}`")

    total_files = len(files)
    # Sending gifs in album gives error and hence this exists
    photo_path, gif_path = [], []
    for path in files:
        _path = gif_path if path.suffix.lower() in (".gif", ".mp4") else photo_path
        _path.append(str(path))
    files = split_list(photo_path, 8) + gif_path
    del photo_path, gif_path

    await msg.edit(f"`Downloaded {total_files} files,\nUploading now..`")
    upload_count = 0
    reply_to = e.reply_to_msg_id or e.id
    for path in files:
        if type(path) == list:
            upload_count += len(path)
            caption = list(map(lambda _: "", path))
            caption[-1] = f"__**{query}** - ({upload_count}/{total_files})__"
        else:
            upload_count += 1
            caption = f"__**{query}** - ({upload_count}/{total_files})__"
        try:
            await e.client.send_file(
                e.chat_id,
                file=path,
                caption=caption,
                reply_to=reply_to,
                silent=e.reply_to,
                force_document=as_doc,
            )
        except Exception as exc:
            LOGS.exception(exc)
            continue
        finally:
            await asyncio.sleep(6)

    rmtree(out_dir, ignore_errors=True)
    await msg.edit(f"`Uploaded {img_type}s from Bing!`")
