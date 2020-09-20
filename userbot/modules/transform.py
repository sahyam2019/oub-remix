# Authored by @Khrisna_Singhal
# Ported from Userge by Alfiananda P.A
import os

from PIL import Image
from PIL import ImageOps

from userbot import bot
from userbot import CMD_HELP
from userbot import TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.utils.tools import check_media

Converted = TEMP_DOWNLOAD_DIRECTORY + "sticker.webp"


@register(outgoing=True, pattern=r"^\.ghost$")
async def ghost(ghost):
    if not ghost.reply_to_msg_id:
        await ghost.edit("`Reply to any media..`")
        return
    reply_message = await ghost.get_reply_message()
    if not reply_message.media:
        await ghost.edit("`reply to a image/sticker`")
        return
    await bot.download_file(reply_message.media)
    await ghost.edit("`Downloading Media..`")
    if ghost.is_reply:
        data = await check_media(reply_message)
        if isinstance(data, bool):
            await ghost.edit("`Unsupported Files...`")
            return
    else:
        await ghost.edit("`Reply to Any Media Sur`")
        return

    try:
        await ghost.edit("`Ghost is coming 😈 `")
        file_name = "ghost.png"
        downloaded_file_name = os.path.join(TEMP_DOWNLOAD_DIRECTORY, file_name)
        ghost_file = await bot.download_media(
            reply_message,
            downloaded_file_name,
        )
        im = Image.open(ghost_file).convert("RGB")
        im_invert = ImageOps.invert(im)
        im_invert.save(Converted)
        await ghost.client.send_file(
            ghost.chat_id,
            Converted,
            reply_to=ghost.reply_to_msg_id,
        )
        await ghost.delete()
        os.remove(ghost_file)
        os.remove(Converted)
    except BaseException:
        pass


@register(outgoing=True, pattern=r"^\.(mirror|flip)$")
async def mirrorflip(event):
    if not event.reply_to_msg_id:
        await event.edit("`Reply to Any media..`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("`reply to a image/sticker`")
        return
    await bot.download_file(reply_message.media)
    await event.edit("`Downloading Media..`")
    if event.is_reply:
        data = await check_media(reply_message)
        if isinstance(data, bool):
            await event.edit("`Unsupported Files...`")
            return
    else:
        await event.edit("`Reply to Any Media Sur`")
        return

    try:
        await event.edit("`Processing..`")
        cmd = event.pattern_match.group(1)
        file_name = "gambar.png"
        downloaded_file_name = os.path.join(TEMP_DOWNLOAD_DIRECTORY, file_name)
        mirror_flip_file = await bot.download_media(
            reply_message,
            downloaded_file_name,
        )
        im = Image.open(mirror_flip_file).convert("RGB")
        if cmd == "mirror":
            IMG = ImageOps.mirror(im)
        elif cmd == "flip":
            IMG = ImageOps.flip(im)
        IMG.save(Converted, quality=95)
        await event.client.send_file(event.chat_id,
                                     Converted,
                                     reply_to=event.reply_to_msg_id)
        await event.delete()
        os.remove(mirror_flip_file)
        os.remove(Converted)
    except BaseException:
        pass


@register(outgoing=True, pattern=r"^\.rotate(?: |$)(.*)")
async def rotate(event):
    if not event.reply_to_msg_id:
        await event.edit("`Reply to any media..`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("`reply to a image/sticker`")
        return
    await bot.download_file(reply_message.media)
    await event.edit("`Downloading Media..`")
    if event.is_reply:
        data = await check_media(reply_message)
        if isinstance(data, bool):
            await event.edit("`Unsupported Files...`")
            return
    else:
        await event.edit("`Reply to Any Media Sur`")
        return
    await event.edit("`Rotating your media..`")
    try:
        value = int(event.pattern_match.group(1))
        if value > 360:
            raise ValueError
    except ValueError:
        value = 90
    file_name = "gambar.png"
    downloaded_file_name = os.path.join(TEMP_DOWNLOAD_DIRECTORY, file_name)
    rotate = await bot.download_media(
        reply_message,
        downloaded_file_name,
    )
    im = Image.open(rotate).convert("RGB")
    IMG = im.rotate(value, expand=1)
    IMG.save(Converted, quality=95)
    await event.client.send_file(event.chat_id,
                                 Converted,
                                 reply_to=event.reply_to_msg_id)
    await event.delete()
    os.remove(rotate)
    os.remove(Converted)


CMD_HELP.update({
    "transform":
    ">`.ghost`"
    "\nUsage: Enchance your image to become a ghost!."
    "\n\n>`.flip`"
    "\nUsage: To flip your image"
    "\n\n>`.mirror`"
    "\nUsage: To mirror your image"
    "\n\n>`.rotate <value>`"
    "\nUsage: To rotate your image\n* The value is range 1-360 if not it'll give default value which is 90"
})
