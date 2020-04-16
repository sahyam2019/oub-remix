"""@RollADie
Syntax: .dice"""
#from telethon.tl.types import InputMediaDice
import telethon
#from uniborg.util import admin_cmd
import telethon.tl.types
from telethon.tl.types import *
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import register




#@borg.on(admin_cmd(pattern="dice ?(.*)"))
@register(outgoing=True, pattern="^.dice$")
async def _(event):
    if event.fwd_from:
        return
        try:
            from telethon.tl.types import InputMediaDice
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice())
    if input_str:
        try:
            required_number = int(input_str)
            while not r.media.value == required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice())
        except:
            pass
            
CMD_HELP.update({
        "dice": 
        ".dice reply_message. \
          \n. "
    })
