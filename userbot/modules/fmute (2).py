# Copyright (C) 2020 KenHV
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

from sqlalchemy.exc import IntegrityError

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, disable_edited=True, pattern=r"^\.fmute(?: |$)(.*)")
async def fban(event):
    """Bans a user from connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import get_flist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    if (reply_msg := await event.get_reply_message()):
        fban_id = reply_msg.from_id
        reason = event.pattern_match.group(1)
    else:
        pattern = str(event.pattern_match.group(1)).split()
        fban_id = pattern[0]
        reason = ''.join(pattern[1:])

    self_user = await event.client.get_me()

    if fban_id == self_user.id or fban_id == "@" + self_user.username:
        return await event.edit(
            "**Error: This action has been prevented by remix self preservation protocols.**"
        )

    if isinstance(fban_id, int):
        user_link = f"[{fban_id}](tg://user?id={fban_id})"
    else:
        user_link = fban_id

    if len((fed_list := get_flist())) == 0:
        return await event.edit(
            "**You haven't connected to any federations yet!**")

    await event.edit(f"**Fbanning** {user_link}...")
    failed = []
    total = int(0)

    for i in fed_list:
        total += 1
        chat = int(i.chat_id)

        try:
            async with bot.conversation(chat) as conv:
                await conv.send_message(
                    f"/ban [{fban_id}](tg://user?id={fban_id}) {reason}")
                reply = await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id,
                                                message=reply,
                                                clear_mentions=True)

                if ("New FedBan" not in reply.text) and ("Starting a federation ban" not in reply.text) and (
                        "Start a federation ban" not in reply.text) and ("FedBan reason updated" not in reply.text):
                    failed.append(i.fed_name)
        except BaseException:
            failed.append(i.fed_name)

    reason = reason if reason else "Not specified."

    if failed:
        status = f"Failed to fban in {len(failed)} feds.\n"
        for i in failed:
            status += "• " + i + "\n"
    else:
        status = f"Success! Fbanned in {total} feds."

    await event.edit(
        f"**Fmuted **{user_link}!\n**Reason:** {reason}\n**Status:** {status}"
    )


@register(outgoing=True, disable_edited=True, pattern=r"^\.unfmute(?: |$)(.*)")
async def unfban(event):
    """Unbans a user from connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import get_flist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    if (reply_msg := await event.get_reply_message()):
        unfban_id = reply_msg.from_id
        reason = event.pattern_match.group(1)
    else:
        pattern = str(event.pattern_match.group(1)).split()
        unfban_id = pattern[0]
        reason = ''.join(pattern[1:])

    self_user = await event.client.get_me()

    if unfban_id == self_user.id or unfban_id == "@" + self_user.username:
        return await event.edit("**Wait, that's illegal**")

    if isinstance(unfban_id, int):
        user_link = f"[{unfban_id}](tg://user?id={unfban_id})"
    else:
        user_link = unfban_id

    if len((fed_list := get_flist())) == 0:
        return await event.edit(
            "**You haven't connected any groups yet!**")

    await event.edit(f"**Un-fmuting **{user_link}**...**")
    failed = []
    total = int(0)

    for i in fed_list:
        total += 1
        chat = int(i.chat_id)
        try:
            async with bot.conversation(chat) as conv:
                await conv.send_message(
                    f"/unmute [{unfban_id}](tg://user?id={unfban_id}) {reason}"
                )
                reply = await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id,
                                                message=reply,
                                                clear_mentions=True)

                if ("New un-Fmute" not in reply.text) and (
                        "I'll give" not in reply.text) and ("Un-FedBan" not in reply.text):
                    failed.append(i.fed_name)
        except BaseException:
            failed.append(i.fed_name)

    reason = reason if reason else "Not specified."

    if failed:
        status = f"Failed to unfmute in {len(failed)} groups.\n"
        for i in failed:
            status += "• " + i + "\n"
    else:
        status = f"Success! Un-fmuted in {total} feds."

    reason = reason if reason else "Not specified."
    await event.edit(
        f"**Un-fmuted** {user_link}!\n**Reason:** {reason}\n**Status:** {status}"
    )


@register(outgoing=True, pattern=r"^\.addfmute *(.*)")
async def addf(event):
    """Adds current chat to connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import add_flist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    if not (fed_name := event.pattern_match.group(1)):
        return await event.edit(
            "**Pass a name in order connect to this group!**")

    try:
        add_flist(event.chat_id, fed_name)
    except IntegrityError:
        return await event.edit(
            "**This group is already connected to federations list.**")

    await event.edit("**Added this group to federations list!**")


@register(outgoing=True, pattern=r"^\.delfmute$")
async def delf(event):
    """Removes current chat from connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import del_flist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    del_flist(event.chat_id)
    await event.edit("**Removed this group from mute list!**")


@register(outgoing=True, pattern=r"^\.listfmute$")
async def listf(event):
    """List all connected groups."""
    try:
        from userbot.modules.sql_helper.fban_sql import get_flist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    if len((fed_list := get_flist())) == 0:
        return await event.edit(
            "**You haven't connected to any groups yet!**")

    msg = "**Connected:**\n\n"

    for i in fed_list:
        msg += "• " + str(i.fed_name) + "\n"

    await event.edit(msg)


@register(outgoing=True, disable_edited=True, pattern=r"^\.clearf2$")
async def delf(event):
    """Removes all chats from connected mute."""
    try:
        from userbot.modules.sql_helper.fban_sql import del_flist_all
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    del_flist_all()
    await event.edit("**Disconnected from all connected mute!**")


CMD_HELP.update({"fban": "`.fmute` <id/username> <reason>"
                 "\nUsage: Mute user from connected groups."
                 "\nYou can reply to the user whom you want to fban or manually pass the username/id."
                 "\n\n`.unfmute` <id/username> <reason>"
                 "\nUsage: Same as fban but unbans the user"
                 "\n\n`.addfmute` <name>"
                 "\nUsage: Adds current group and stores it as <name> in connected mute."
                 "\nAdding one group is enough for one federation."
                 "\n\n`.delfmute`"
                 "\nUsage: Removes current group from connected mute list."
                 "\n\n`.listfmute`"
                 "\nUsage: Lists all connected groups by specified name."})
