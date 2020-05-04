from asyncio import sleep
from random import choice, getrandbits, randint
from re import sub
import random
from os import execl
import time
from telethon import events
from userbot import bot
from collections import deque
import requests
import sys
import os
import io
import html
import json
from PIL import ImageEnhance, ImageOps

from userbot import CMD_HELP
from userbot.events import register
from userbot.modules.admin import get_user_from_event


def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, '', inputString)


@register(outgoing=True, pattern="^.waifu(?: |$)(.*)")

async def waifu(animu):
#"""Generate random waifu sticker with the text!"""
     
    text = animu.pattern_match.group(1)
    if not text:
        if animu.is_reply:
            text = (await animu.get_reply_message()).message
        else:
            await animu.answer("`No text given, hence the waifu ran away.`")
            return
    animus = [20, 32, 33, 40, 41, 42, 58]
    sticcers = await bot.inline_query(
        "stickerizerbot", f"#{random.choice(animus)}{(deEmojify(text))}")
    await sticcers[0].click(animu.chat_id,
                            reply_to=animu.reply_to_msg_id,
                            silent=True if animu.is_reply else False,
                            hide_via=True)
    await animu.delete()
