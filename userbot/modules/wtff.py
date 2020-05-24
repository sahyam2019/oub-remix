# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# You can find misc modules, which dont fit in anything xD
""" Userbot module for other small commands. """

from random import randint
from asyncio import sleep
from os import execl
import sys
import os
import io
import sys
import json
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import register

@register(outgoing=True, pattern="^.wtff$")
async def wtff(e):
    await e.edit("🤬               🤬\n🤬               🤬\n🤬               🤬\n🤬     🤬     🤬\n🤬🤬    🤬🤬\n\n🤬🤬🤬🤬\n       🤬\n       🤬\n       🤬\n       🤬\n\n🤬🤬🤬🤬\n🤬\n🤬🤬🤬\n🤬\n🤬")

        
    
    CMD_HELP.update({
    'wtff':
    '.wtff\
\nUsage: gives a nice WTF as output.'
})

#created by, S.A.Sohan
