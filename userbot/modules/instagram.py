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

async def progress(current, total, event, start, type_of_ps, file_name=None):
    """Generic progress_callback for uploads and downloads."""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "[{0}{1}] {2}%\n".format(
            ''.join(["▰" for i in range(math.floor(percentage / 10))]),
            ''.join(["▱" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2))
        tmp = progress_str + \
            "{0} of {1}\nETA: {2}".format(
                humanbytes(current),
                humanbytes(total),
                time_formatter(estimated_total_time)
            )
        if file_name:
            await event.edit("{}\nFile Name: `{}`\n{}".format(
                type_of_ps, file_name, tmp))
        else:
            await event.edit("{}\n{}".format(type_of_ps, tmp))

def humanbytes(size):
    """Input size in bytes,
    outputs in a human readable format"""
    # https://stackoverflow.com/a/49361727/4723940
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " day(s), ") if days else "") + \
        ((str(hours) + " hour(s), ") if hours else "") + \
        ((str(minutes) + " minute(s), ") if minutes else "") + \
        ((str(seconds) + " second(s), ") if seconds else "") + \
        ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    return tmp[:-2]


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
    uploaded = 0
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
