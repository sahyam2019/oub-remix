# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.

import aiohttp
from userbot.events import register
from userbot import CMD_HELP


@register(pattern=r".git (.*)", outgoing=True)
async def github(event):
    URL = f"https://api.github.com/users/{event.pattern_match.group(1)}"
    chat = await event.get_chat()
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                await event.reply("`" + event.pattern_match.group(1) +
                                  " not found`")
                return

            result = await request.json()

            url = result.get("html_url", None)
            name = result.get("name", None)
            company = result.get("company", None)
            bio = result.get("bio", None)
            created_at = result.get("created_at", "Not Found")

            REPLY = f"GitHub Info for `{event.pattern_match.group(1)}`\
            \nUsername: `{name}`\
            \nBio: `{bio}`\
            \nURL: {url}\
            \nCompany: `{company}`\
            \nCreated at: `{created_at}`"

            if not result.get("repos_url", None):
                await event.edit(REPLY)
                return
            async with session.get(result.get("repos_url", None)) as request:
                result = request.json
                if request.status == 404:
                    await event.edit(REPLY)
                    return

                result = await request.json()

                REPLY += "\nRepos:\n"

                for nr in range(len(result)):
                    REPLY += f"[{result[nr].get('name', None)}]({result[nr].get('html_url', None)})\n"

                await event.edit(REPLY)


CMD_HELP.update({
    "hergit":
    "`.git`\
\nUsage: Like .data but for GitHub usernames.\
\n\n\"`.gcommit`\
\n\nUsage: GITHUB File Uploader Plugin for userbot. Heroku Automation should be Enabled. Else u r not that lazy , For lazy people\
\n\nInstructions:- Set GITHUB_ACCESS_TOKEN and GIT_REPO_NAME Variables in Heroku vars First\
\n\n`.gcommit` reply_to_any_plugin can be any type of file too. but for plugin must be in .py\
\n\n\"`.usage`"
"\nUsage: Check your heroku dyno hours remaining"
"\n\n`.set var` <NEW VAR> <VALUE>"
"\nUsage: add new variable or update existing value variable"
"\n!!! WARNING !!!, after setting a variable the bot will restarted"
"\n\n`.get var` or .get var <VAR>"
"\nUsage: get your existing varibles, use it only on your private group!"
"\nThis returns all of your private information, please be caution..."
"\n\n`.del var` <VAR>"
"\nUsage: delete existing variable"
"\n!!! WARNING !!!, after deleting variable the bot will restarted"
})
