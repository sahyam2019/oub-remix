# Copyright (C) 2020 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Port From UniBorg to UserBot by MoveAngel

import telethon
from asyncio.exceptions import TimeoutError

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import bot, CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.q")
async def quotess(qotli):
    if qotli.fwd_from:
        return
    if not qotli.reply_to_msg_id:
        return await qotli.edit("```Reply to any user message.```")
    reply_message = await qotli.get_reply_message()
    if not reply_message.text:
        return await qotli.edit("```Reply to text message```")
    chat = "@QuotLyBot"
    if reply_message.sender.bot:
        return await qotli.edit("```Reply to actual users message.```")
    await qotli.edit("```Making a Quote```")
    try:
        async with bot.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(
                        incoming=True,
                        from_users=1031952739))
                msg = await bot.forward_messages(chat, reply_message)
                response = await response
                """ - don't spam notif - """
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                return await qotli.reply("```Please unblock @QuotLyBot and try again```")
            if response.text.startswith("Hi!"):
                await qotli.edit("```Can you kindly disable your forward privacy settings for good?```")
            else:
                await qotli.delete()
                await bot.forward_messages(qotli.chat_id, response.message)
                await bot.send_read_acknowledge(qotli.chat_id)
                """ - cleanup chat after completed - """
                await qotli.client.delete_messages(conv.chat_id,
                                                   [msg.id, response.id])
    except TimeoutError:
        await qotli.edit()

CMD_HELP.update({
    "quotly":
    "`.q`\
\nUsage: Enhance ur text to sticker.\
\n\n`.pch`\
\nUsage: Better than quotly."
})
