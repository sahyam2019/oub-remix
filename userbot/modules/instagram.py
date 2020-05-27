# Copyright (C) 2019 The Raphielscape Company LLC.
# Copyright (C) 2020 azrim.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.

from instalooter.looters import ProfileLooter
import os
import time
import asyncio
import subprocess
import math

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.tl.types import DocumentAttributeVideo
from userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID, TEMP_DOWNLOAD_DIRECTORY, LOGS
from userbot.events import register
from userbot.utils import progress, humanbytes, time_formatter

@register(outgoing=True, pattern=r"^.ig(?: |$)(.*)")
async def instagram_dl(igdl):
    """ To downloading photos from instagram account """
    uname = igdl.pattern_match.group(1)
    input_str = TEMP_DOWNLOAD_DIRECTORY
    if not os.path.exists(input_str):
        os.makedirs(input_str)
    try:
        await igdl.edit(f"`Getting info.....`")
        looter = ProfileLooter(uname)
        looter.download('TEMP_DOWNLOAD_DIRECTORY', media_count=5)

    except ValueError:
        await igdl.edit(f"**Account {uname} Not Found.**\nPlease enter correct username.")
        return
        
    except RuntimeError:
        await igdl.edit(f"**Can't Catch Media.**\nAccount {uname} is Private.")
        return

    await igdl.edit("Processing ...")
    lst_of_files = []
    for r, d, f in os.walk(input_str):
        for file in f:
            lst_of_files.append(os.path.join(r, file))
        for file in d:
            lst_of_files.append(os.path.join(r, file))
    LOGS.info(lst_of_files)
    #uploaded = 0
    countf = "{}".format(len(lst_of_files))
    count = int(countf)
    if count == 0:
        await igdl.edit("**No Media Found**\nSorry this account doesn't have any content")
    else:
        await igdl.edit(
            "Found {} files. Uploading will start soon. Please wait!".format(
                len(lst_of_files)))
        for single_file in lst_of_files:
            if os.path.exists(single_file):
                # https://stackoverflow.com/a/678242/4723940
                caption_rts = os.path.basename(single_file)
                c_time = time.time()
                if not caption_rts.lower().endswith(".mp4"):
                    await igdl.client.send_file(
                        igdl.chat_id,
                        single_file,
                        caption=f"[{uname}](https://instagram.com/{uname})",
                        force_document=True,
                        allow_cache=False,
                        progress_callback=lambda d, t: asyncio.get_event_loop(
                        ).create_task(
                            progress(d, t, igdl, c_time, "Uploading...",
                                single_file)))
                    os.remove(single_file)


CMD_HELP.update({
    "instagram":
    ".ig <username>\
\nUsage: Downloads 10 pictures from Instagram account."
})
