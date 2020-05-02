""" Userbot module for other small commands. """

from random import randint
from asyncio import sleep
from os import execl
import sys
import os
import io
import sys
import json
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot, GIT_REPO_NAME, ALIVE_NAME
from userbot.events import register


# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================

@register(outgoing=True, pattern="^.useitoub$")
async def usit(e):
    await e.edit(
        f"Here's something for {DEFAULTUSER} to use it for help_on_update on **OpenUserBot**:\n"
        "\n[Windows Method](https://telegra.ph/How-to-keep-repo-updated-while-keeping-your-changes-through-windows-cmd-method-04-01)"
        "\n[Termux Method](https://telegra.ph/How-to-keep-OpenUserBot-repo-updated-while-keeping-your-changes-through-Termux-method-04-01)"
        "\n[Kali Linux Method](https://telegra.ph/How-to-keep-OpenUserBot-repo-updated-while-keeping-your-changes-through-Termux-method-04-01)"
        "\n[Ubuntu Linux Method](https://telegra.ph/How-to-keep-OUB-repo-updated-while-keeping-your-changes-through-Ubuntu-Terminal-method-04-01-2)"
        "\n[Special - Note](https://telegra.ph/Special-Note-11-02)")
    
@register(outgoing=True, pattern="^.varoub$")
async def var(m):
    await m.edit(
        f"Here's a list of VARS for {DEFAULTUSER} on **OpenUserBot**:\n"
        "\n[HEROKU VARS](https://raw.githubusercontent.com/mkaraniya/OpenUserBot/sql-extended/bin/vars%20for%20oub.txt)")
    
    
CMD_HELP.update({
    "useitoub":
    ".useitoub\
\nUsage: Provide links to update repo guides while you keep your changes on the floor.\
\n.varoub\
\nUsage: Provide vars to cross check for you."
})
