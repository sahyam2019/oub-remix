import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot import bot, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY 
from userbot.events import register




@register(outgoing=True, pattern="^.sd(?: |$)(.*)")
async def _(std):
   async def _(event):
    if std.fwd_from:
        return 
    if not std.reply_to_msg_id:
       await std.edit("```Reply to any user message.```")
       return
    reply_message = await std.get_reply_message() 
    if not reply_message.media:
       await event.edit("```Reply to text media```")
       return
    chat = "@Stickerdownloadbot"
    message_id_to_reply = std.message.reply_to_msg_id
    async with std.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(events.NewMessage(incoming=True,from_users=1031952739))
            await bot.forward_messages(chat, reply_message)
            response = await response 
           
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await std.reply("`Please unblock` @Stickerdownloadbot`...`")
            return
        if response.text.startswith("I"):
            await std.edit("`Invalid...`")
        else:
            downloaded_file_name = await std.client.download_media(
                                 response.media,
                                 TEMP_DOWNLOAD_DIRECTORY
            )
            await std.client.send_file(
                std.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=message_id_to_reply
            )
            """ - cleanup chat after completed - """
            try:
                msg_level
            except NameError:
                await std.client.delete_messages(conv.chat_id,
                                                 [msg.id, response.id])
            else:
                await std.client.delete_messages(
                    conv.chat_id,
                    [msg.id, response.id, r.id, msg_level.id])
    await std.delete()
    return os.remove(downloaded_file_name)
