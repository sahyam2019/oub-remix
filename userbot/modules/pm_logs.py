#This module was created by @spechide for Uniborg
"""Log PMs
this will now log chat msgs to your botlog chat id.
if you don't want chat logs than use `.nolog` , for opposite use `.log`. Default is .log enabled.
enjoy this now.
Thanks to @heyworld for a small correction"""

import asyncio
import os
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from telethon import events
from telethon.tl import functions, types
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register


NO_PM_LOG_USERS = []

#@borg.on(admin_cmd(incoming=True, func=lambda e: e.is_private))
@register(incoming=True, disable_edited=True)
async def monito_p_m_s(event):
    sender = await event.get_sender()
    if event.is_private and not (await event.get_sender()).bot:
        chat = await event.get_chat()
        if chat.id not in NO_PM_LOG_USERS and chat.id:
            try:
                e = await event.client.get_entity(int(BOTLOG_CHATID))
                fwd_message = await event.client.forward_messages(
                    e,
                    event.message,
                    silent=True
                )
            except Exception as e:
                LOGS.warn(str(e))

#@borg.on(admin_cmd(pattern="nolog ?(.*)"))
@register(pattern="^.nolog(?: |$)(.*)")
async def approve_p_m(event):
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    chat = await event.get_chat()
    if BOTLOG:
        if event.is_private:
            if chat.id not in NO_PM_LOG_USERS:
                NO_PM_LOG_USERS.append(chat.id)
                await event.edit("Won't Log Messages from this chat")
                await asyncio.sleep(3)
                await event.delete()

                
@register(pattern="^.log(?: |$)(.*)")
async def approve_p_m(event):
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    chat = await event.get_chat()
    if BOTLOG:
        if event.is_private:
            if chat.id in NO_PM_LOG_USERS:
                NO_PM_LOG_USERS.remove(chat.id)
                await event.edit("Will Log Messages from this chat")
                await asyncio.sleep(3)
                await event.delete()

CMD_HELP.update({
    "logpms":
    "If you don't want chat logs than use `.nolog` , for opposite use `.log`. Default is .log enabled\
\nUsage: This will now log chat msgs to your botlog chat id."
})    
