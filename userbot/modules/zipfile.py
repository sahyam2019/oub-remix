# Copyright (C) 2020 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Port from UniBorg to Userbot by yincen17

""" `UNZIPPER`  Coded by @By_Azade code rewritten my SnapDragon7410 """

import asyncio
import zipfile
from userbot.events import register
from datetime import date
import time
import os
from userbot import TEMP_DOWNLOAD_DIRECTORY, ZIP_DOWNLOAD_DIRECTORY, bot, CMD_HELP
from telethon.tl.types import DocumentAttributeVideo
from userbot.utils import progress
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

thumb_image_path = TEMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"
extracted = TEMP_DOWNLOAD_DIRECTORY + "extracted/"
if not os.path.isdir(extracted):
    os.makedirs(extracted)

# ====================
today = date.today()
# ====================


@register(outgoing=True, pattern=r"^\.compress(?: |$)(.*)")
async def _(event):
    # Prevent Channel Bug to use update
    if event.is_channel and not event.is_group:
        await event.edit("`Compress Command isn't permitted on channels`")
        return
    if event.fwd_from:
        return
    if not event.is_reply:
        await event.edit("`Reply to a file to compress it.`")
        return
    mone = await event.edit("`Processing...`")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await bot.download_media(
                reply_message,
                TEMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "[DOWNLOADING]")
                ),
            )
            directory_name = downloaded_file_name
            await event.edit(
                f"Downloaded to `{directory_name}`" "`\ncompressing file...`"
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
    zipfile.ZipFile(directory_name + ".zip", "w", zipfile.ZIP_DEFLATED).write(
        directory_name
    )
    c_time = time.time()
    await bot.send_file(
        event.chat_id,
        directory_name + ".zip",
        force_document=True,
        allow_cache=False,
        reply_to=event.message.id,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, mone, c_time, "[UPLOADING]")
        ),
    )
    await event.edit("`Done!!`")
    await asyncio.sleep(7)
    await event.delete()


@register(outgoing=True, pattern=r"^\.unzip(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    mone = await event.edit("Processing ...")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        reply_message = await event.get_reply_message()
        try:
            time.time()
            downloaded_file_name = await bot.download_media(
                reply_message,
                TEMP_DOWNLOAD_DIRECTORY,

            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
        else:
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit("Stored the zip to `{}` in {} seconds.".format(downloaded_file_name, ms))

        with zipfile.ZipFile(downloaded_file_name, 'r') as zip_ref:
            zip_ref.extractall(extracted)
        filename = sorted(get_lst_of_files(extracted, []))
        #filename = filename + "/"
        await event.edit("Unzipping now")
        # r=root, d=directories, f = files
        for single_file in filename:
            if os.path.exists(single_file):
                # https://stackoverflow.com/a/678242/4723940
                caption_rts = os.path.basename(single_file)
                force_document = True
                supports_streaming = False
                document_attributes = []
                if single_file.endswith((".mp4", ".mp3", ".flac", ".webm")):
                    metadata = extractMetadata(createParser(single_file))
                    duration = 0
                    width = 0
                    height = 0
                    if metadata.has("duration"):
                        duration = metadata.get('duration').seconds
                    if os.path.exists(thumb_image_path):
                        metadata = extractMetadata(
                            createParser(thumb_image_path))
                        if metadata.has("width"):
                            width = metadata.get("width")
                        if metadata.has("height"):
                            height = metadata.get("height")
                    document_attributes = [
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True
                        )
                    ]
                try:
                    await bot.send_file(
                        event.chat_id,
                        single_file,
                        caption=f"UnZipped `{caption_rts}`",
                        force_document=force_document,
                        supports_streaming=supports_streaming,
                        allow_cache=False, reply_to=event.message.id,
                        attributes=document_attributes,
                        # progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        #     progress(d, t, event, c_time, "trying to upload")
                        # )
                    )
                except Exception as e:
                    await bot.send_message(
                        event.chat_id,
                        "{} caused `{}`".format(caption_rts, str(e)),
                        reply_to=event.message.id
                    )
                    # some media were having some issues
                    continue
                os.remove(single_file)
        os.remove(downloaded_file_name)


@register(outgoing=True, pattern=r"^\.addzip(?: |$)(.*)")
async def addzip(add):
    """ Copyright (c) 2020 azrim @github"""
    # Prevent Channel Bug to use update
    if add.is_channel and not add.is_group:
        await add.edit("`Command isn't permitted on channels`")
        return
    if add.fwd_from:
        return
    if not add.is_reply:
        await add.edit("`Reply to a file to compress it.`")
        return
    mone = await add.edit("`Processing...`")
    if not os.path.isdir(ZIP_DOWNLOAD_DIRECTORY):
        os.makedirs(ZIP_DOWNLOAD_DIRECTORY)
    if add.reply_to_msg_id:
        reply_message = await add.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await bot.download_media(
                reply_message,
                ZIP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "[DOWNLOADING]")
                ),
            )
            success = str(downloaded_file_name).replace("./zips/", "")
            await add.edit(f"`{success} Successfully added to list`")
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
            return


@register(outgoing=True, pattern=r"^\.upzip(?: |$)(.*)")
async def upload_zip(up):
    if not os.path.isdir(ZIP_DOWNLOAD_DIRECTORY):
        await up.edit("`Files not found`")
        return
    mone = await up.edit("`Zipping File...`")
    input_str = up.pattern_match.group(1)
    curdate = today.strftime("%m%d%y")
    title = str(input_str) if input_str else "zipfile" + f"{curdate}"
    zipf = zipfile.ZipFile(title + '.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(ZIP_DOWNLOAD_DIRECTORY, zipf)
    zipf.close()
    c_time = time.time()
    await bot.send_file(
        up.chat_id,
        title + ".zip",
        force_document=True,
        allow_cache=False,
        reply_to=up.message.id,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, mone, c_time, "[UPLOADING]", input_str)
        ),
    )
    os.rmdir(ZIP_DOWNLOAD_DIRECTORY)
    await up.delete()


@register(outgoing=True, pattern=r"^\.rmzip(?: |$)(.*)")
async def remove_dir(rm):
    if not os.path.isdir(ZIP_DOWNLOAD_DIRECTORY):
        await rm.edit("`Directory not found`")
        return
    os.rmdir(ZIP_DOWNLOAD_DIRECTORY)
    await rm.edit("`Zip list removed`")


def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
            os.remove(os.path.join(root, file))


CMD_HELP.update({
    "zipfile":
        "`.compress` **[optional: <reply to file>]**\
            \nUsage: make files to zip.\
            \n`.unzip` **<reply to zipped file>**\
            \nUsage: unzip the zipped files.\
            \n`.addzip` **<reply to file>**\
            \nUsage: add files to zip list.\
            \n`.upzip` **[optional: <zip title>]**\
            \nUsage: upload zip list.\
            \n`.rmzip` **[optional: <zip title>]**\
            \nUsage: clear zip list."
})
