import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot import bot, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY 
from userbot.events import register





@register(outgoing=True, pattern="^.sd(?: |$)(.*)")
async def lastname(steal):
    if steal.fwd_from:
        return 
    if not steal.reply_to_msg_id:
       await steal.edit("```Reply to any user message.```")
       return
    reply_message = await steal.get_reply_message() 
    if not reply_message.media:
       await steal.edit("```reply to media```")
       return
    chat = "@Stickerdownloadbot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await steal.edit("```Reply to actual users message.```")
       return
    await steal.edit("```wait```")
    async with bot.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=461843263))
              await bot.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await steal.reply("```Please unblock @Stickerdownloadbot and try again```")
              return
          if response.text.startswith("I"):
             await steal.edit("```invalid```")
          else: 
             await steal.edit(f"{response.message.message}")
