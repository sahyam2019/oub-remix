
from telethon.tl.types import InputMediaDice
#from userbot.util import admin_cmd
from userbot.events import register
from userbot import bot, CMD_HELP



@register(outgoing=True, pattern="^.dice(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
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
        ".dice"
        "\nUsage: check yourself.\n"
    })
