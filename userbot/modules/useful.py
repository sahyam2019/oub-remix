# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""use cmd .load <plugin.py name>, .unload <plugin.py name>, send plugin <plugin.py name>, install <plugin.py name>."""
import asyncio
import traceback
import os
from datetime import datetime
from userbot import CMD_HELP
from userbot.events import register


DELETE_TIMEOUT = 5


#@borg.on(util.admin_cmd(pattern="load (?P<shortname>\w+)$"))       # pylint:disable=E0602
@register(outgoing=True, pattern=r"^.(\w+)load (.*)")         
async def load_reload(event):
    await event.delete()
    shortname = event.pattern_match["shortname"]
    try:
        if shortname in bot._plugins:  # pylint:disable=E0602
            bot.remove_plugin(shortname)  # pylint:disable=E0602
        bot.load_plugin(shortname)  # pylint:disable=E0602
        msg = await event.respond(f"Successfully (re)load plugin {shortname}")
        await asyncio.sleep(DELETE_TIMEOUT)
        await msg.delete()
    except Exception as e:  # pylint:disable=C0103,W0703
        trace_back = traceback.format_exc()
        # pylint:disable=E0602
        logger.warn(f"Failed to (re)load plugin {shortname}: {trace_back}")
        await event.respond(f"Failed to (re)load plugin {shortname}: {e}")


#@borg.on(util.admin_cmd(pattern="(?:unload|remove) (?P<shortname>\w+)$"))  # pylint:disable=E0602
@register(outgoing=True, pattern=r"^.(\w+)unload|remove (.*)")
async def remove(event):
    await event.delete()
    shortname = event.pattern_match["shortname"]
    if shortname == "_core":
        msg = await event.respond(f"Not removing {shortname}")
    elif shortname in bot._plugins:  # pylint:disable=E0602
        bot.remove_plugin(shortname)  # pylint:disable=E0602
        msg = await event.respond(f"Removed plugin {shortname}")
    else:
        msg = await event.respond(f"Plugin is {shortname} is not load...")
    await asyncio.sleep(DELETE_TIMEOUT)
    await msg.delete()


#@borg.on(util.admin_cmd(pattern="send plugin (?P<shortname>\w+)$"))  # pylint:disable=E0602
@register(outgoing=True, pattern=r"^.(\w+)send plugin (?P<shortname>) (.*)") 
async def send_plug_in(event):
    if event.fwd_from:
        return
    message_id = event.message.id
    input_str = event.pattern_match["shortname"]
    the_plugin_file = "./userbot/modules/{}.py".format(input_str)
    start = datetime.now()
    await event.client.send_file(  # pylint:disable=E0602
        event.chat_id,
        the_plugin_file,
        force_document=True,
        allow_cache=False,
        reply_to=message_id
    )
    end = datetime.now()
    time_taken_in_ms = (end - start).seconds
    await event.edit("Plugin uploaded {} in {} seconds".format(input_str, time_taken_in_ms))
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()


#@borg.on(util.admin_cmd(pattern="install plugin"))  # pylint:disable=E0602
@register(outgoing=True, pattern=r"^.(\w+)install plugin (.*)") 
async def install_plug_in(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(  # pylint:disable=E0602
                await event.get_reply_message(),
                bot._plugin_path  # pylint:disable=E0602
            )
            if "(" not in downloaded_file_name:
                bot.load_plugin_from_file(downloaded_file_name)  # pylint:disable=E0602
                await event.edit("Installed Plugin `{}`".format(os.path.basename(downloaded_file_name)))
            else:
                os.remove(downloaded_file_name)
                await event.edit("oh! plugin is not installed or it may be already installed check your github repo first.")
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
            os.remove(downloaded_file_name)
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()

    
CMD_HELP.update(
    {"load" : ".load <plugin.py name>\
    \nUsage: loads a plugin."})
CMD_HELP.update({"unload" : ".unload <plugin.py name>\
    \nUsage: unloads a plugin."})
CMD_HELP.update(
    {"send plugin": ".send plugin <plugin.py name>\
    \nUsage: send's a plugin."})
CMD_HELP.update(
    {"install": ".install <plugin.py name>\
    \nUsage: install's a plugin."})
