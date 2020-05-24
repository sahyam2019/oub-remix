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

@register(outgoing=True, pattern="^.covid (.*)")
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("```Reply to any user message.```")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit("```Reply to text message```")
       return
    chat = '@NovelCoronaBot'
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("```Reply to actual users message.```")
       return
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
        ".covid <country>"
        "\nUsage: Get an information about data covid-19 in your country.\n"
    })
