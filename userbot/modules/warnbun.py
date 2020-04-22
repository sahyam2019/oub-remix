#help will be added later don't kang

import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from userbot.events import register 
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot, ALIVE_NAME


@register(outgoing=True, pattern="^.warn1(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    mentions = "__You Have__  **1/3**  __warnings...__\n**Watch out!....**\n**Reason for warn:** __Porn Demand__"
    chat = await event.get_input_chat()
    async for x in bot.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()

@register(outgoing=True, pattern="^.warn2(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    mentions = "__You Have__  **2/3**  __warnings...__\n**Watch out!....**\n**Reason for warn:** __Porn Demand__"
    chat = await event.get_input_chat()
    async for x in bot.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()



@register(outgoing=True, pattern="^.warn3(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    mentions = "__You Have__  **3/3**  __warnings...__\n**Watch out!....**\n**Reason for warn:** __Porn Demand__"
    chat = await event.get_input_chat()
    async for x in bot.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()



@register(outgoing=True, pattern="^.warn0(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    mentions = "**Warning Resetted By Admin...**\n__You Have__  **0/3**  __warnings__"
    chat = await event.get_input_chat()
    async for x in bot.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()



