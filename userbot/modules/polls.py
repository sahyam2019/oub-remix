#imported from catuserbot 
import random

from telethon.errors.rpcbaseerrors import ForbiddenError
from telethon.errors.rpcerrorlist import PollOptionInvalidError
from telethon.tl.types import InputMediaPoll, Poll

from userbot import CMD_HELP, bot
from userbot.events import register
from userbot.utils.tools import Build_Poll

@register(outgoing=True, pattern="^.poll(?: |$)(.*)")
async def pollcreator(event):
    reply_to_id = None
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    string = "".join(event.text.split(maxsplit=1)[1:])
    if not string:
        options = Build_Poll(["Yah sure 😊✌️", "Nah 😏😕", "Whatever die sur 🥱🙄"])
        try:
            await bot.send_message(
                event.chat_id,
                file=InputMediaPoll(
                    poll=Poll(
                        id=random.getrandbits(32),
                        question="👆👆So do you guys agree with this?",
                        answers=options,
                    )
                ),
                reply_to=reply_to_id,
            )
            await event.delete()
        except PollOptionInvalidError:
            await event.edit("`A poll option used invalid data (the data may be too long).`"
            )
        except ForbiddenError:
            await event.edit("`This chat has forbidden the polls`")
        except Exception as e:
            await event.edit(str(e))
    else:
        entry = string.split(";")
        if len(entry) > 2 and len(entry) < 12:
            options = Build_Poll(entry[1:])
            try:
                await bot.send_message(
                    event.chat_id,
                    file=InputMediaPoll(
                        poll=Poll(
                            id=random.getrandbits(32),
                            question=entry[0],
                            answers=options,
                        )
                    ),
                    reply_to=reply_to_id,
                )
                await event.delete()
            except PollOptionInvalidError:
                await event.edit("`A poll option used invalid data (the data may be too long).`",
                )
            except ForbiddenError:
                await event.edit("`This chat has forbidden the polls`")
            except Exception as e:
                await event.edit(str(e))
        else:
            await event.edit("Make sure that you used Correct syntax `.poll question ; option1 ; option2`",
            )


