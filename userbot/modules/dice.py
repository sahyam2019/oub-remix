#fix by @heyworld for OUB
#bug fixed by @d3athwarrior

from telethon.tl.types import InputMediaDice
#from uniborg.util import admin_cmd
from userbot.events import register 
from userbot import CMD_HELP, bot




# EMOJI CONSTANTS
DART = "🎯"
DICE = "🎲"
# EMOJI CONSTANTS


@register(outgoing=True, (pattern=f"^.{dice}|{dart})(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    reply_message = event
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    emoticon = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    await event.delete()
    r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
    if input_str:
        try:
            required_number = int(input_str)
            while not r.media.value == required_number:
                await r.delete()
                r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
        except:
            pass

        
CMD_HELP.update({
    "dice":
    ".dice\
\nUsage: hahaha just a magic."
})    
