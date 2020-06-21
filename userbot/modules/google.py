import asyncio
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from userbot.events import register


@register(outgoing=True, pattern=r"^\.gs (.*)")
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Processing ...")
    # SHOW_DESCRIPTION = False
    input_str = event.pattern_match.group(1) # + " -inurl:(htm|html|php|pls|txt) intitle:index.of \"last modified\" (mkv|mp4|avi|epub|pdf|mp3)"
    input_url = "https://bots.shrimadhavuk.me/search/?q={}".format(input_str)
    headers = {"USER-AGENT": "remix"}
    response = requests.get(input_url, headers=headers).json()
    output_str = " "
    for result in response["results"]:
        text = result.get("title")
        url = result.get("url")
        description = result.get("description")
        image = result.get("image")
        output_str += " 👉🏻  [{}]({}) \n\n".format(text, url)
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit("searched Google for {} in {} seconds. \n{}".format(input_str, ms, output_str), link_preview=False)
    await asyncio.sleep(5)
    await event.edit("Google: {}\n{}".format(input_str, output_str), link_preview=False)
