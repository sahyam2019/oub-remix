# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#


import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot.events import register
from userbot import CMD_HELP


@register(outgoing=True, pattern="^.corona (.*)")
async def _(event):
    if event.fwd_from:
        return 
    input_str = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()
    chat = "@NovelCoronaBot"
    await event.edit("```Checking...```")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=1124136160))
              await event.client.send_message(chat, "{}".format(input_str))
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```Unblock (@NovelCoronaBot)```")
              return
          if response.text.startswith("Country"):
             await event.edit("😐**Country Not Found**😐")
          else: 
             await event.delete()
             await event.client.send_message(event.chat_id, response.message)

CMD_HELP.update(
    {"corona": ".corona [country]\n"
     "Usage: Corona Virus stats."})
