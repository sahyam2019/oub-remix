# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#


from datetime import datetime
from covid import Covid
from telethon import events
from userbot import CMD_HELP
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot.events import register

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
              await event.client.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```Please unblock me (@NovelCoronaBot) u Nigga```")
              return
          if response.text.startswith("Country"):
             await event.edit("Something Went Wrong Check [This Post](https://t.me/TechnoAyanBoT/22?single)")
          else: 
             await event.delete()
             await event.client.send_message(event.chat_id, response.message)


CMD_HELP.update({
        "covid": 
        "`.covid`"
        "\nUsage:First type country name then reply with covid.\n"
    })
