# Copyright (C) 2020 X0rzAvi
# Based on the evaluators.py script so credit goes to the original creator
#
""" Userbot module for browsing internet from Telegram. """
 
import asyncio
from os import remove
from sys import executable
from userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID, TERM_ALIAS
from userbot.events import register
 
@register(outgoing=True, pattern="^.w3m(?: |$)(.*)")
async def terminal_runner(w3m):
    """ For .w3m command, browser the internet with w3m on your server. """
    curruser = TERM_ALIAS
    command = w3m.pattern_match.group(1)
    try:
        from os import geteuid
        uid = geteuid()
    except ImportError:
        uid = "This ain't it chief!"
 
    if w3m.is_channel and not w3m.is_group:
        await w3m.edit("`w3m command isn't permitted on channels!`")
        return
 
    if not command:
        await w3m.edit("``` Give a URL or use .help w3m for \
            an example.```")
        return
 
    if command in ("userbot.session", "config.env"):
        await w3m.edit("`That's a dangerous operation! Not Permitted!`")
        return
 
    process = await asyncio.create_subprocess_exec(
        "w3m",
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) \
        + str(stderr.decode().strip())
 
    if len(result) > 4096:
        output = open("output.txt", "w+")
        output.write(result)
        output.close()
        await w3m.client.send_file(
            w3m.chat_id,
            "output.txt",
            reply_to=w3m.id,
            caption="`Output too large, sending as file`",
        )
        remove("output.txt")
        return
 
    if uid == 0:
        await w3m.edit("`" f"{curruser}:~# w3m {command}" f"\n{result}" "`")
    else:
        await w3m.edit("`" f"{curruser}:~$ w3m {command}" f"\n{result}" "`")
 
    if BOTLOG:
        await w3m.client.send_message(
            BOTLOG_CHATID,
            "w3m with URL " + command + " was executed sucessfully",
        )
      