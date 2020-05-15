# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# You can find misc modules, which dont fit in anything xD
""" Userbot module for other small commands. """

from random import randint
from time import sleep
from os import execl
import sys
import os
import io
import sys
import json
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot, GIT_REPO_NAME, ALIVE_NAME
from userbot.events import register
from userbot.utils import time_formatter
import urllib
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import re
from telethon.tl.types import MessageMediaPhoto
from PIL import Image



# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================

opener = urllib.request.build_opener()
useragent = 'Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.70 Mobile Safari/537.36'
opener.addheaders = [('User-agent', useragent)]


@register(outgoing=True, pattern="^.random")
async def randomise(items):
    """ For .random command, get a random item from the list of items. """
    itemo = (items.text[8:]).split()
    if len(itemo) < 2:
        await items.edit(
            "`2 or more items are required! Check .help random for more info.`"
        )
        return
    index = randint(1, len(itemo) - 1)
    await items.edit("**Query: **\n`" + items.text[8:] + "`\n**Output: **\n`" +
                     itemo[index] + "`")


@register(outgoing=True, pattern="^.sleep ([0-9]+)$")
async def sleepybot(time):
    """ For .sleep command, let the userbot snooze for a few second. """
    counter = int(time.pattern_match.group(1))
    await time.edit("`I am sulking and snoozing...`")
    if BOTLOG:
        str_counter = time_formatter(counter)
        await time.client.send_message(
            BOTLOG_CHATID,
            f"You put the bot to sleep for {str_counter}.",
        )
    sleep(counter)
    await time.edit("`OK, I'm awake now.`")


@register(outgoing=True, pattern="^.shutdown$")
async def killdabot(event):
    """ For .shutdown command, shut the bot down."""
    await event.edit("`Goodbye *Windows XP shutdown sound*....`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n"
                                        "Bot shut down")
    await bot.disconnect()


@register(outgoing=True, pattern="^.restart$")
async def killdabot(event):
    await event.edit("`*i would be back in a moment*`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n"
                                        "Bot Restarted")
    await bot.disconnect()
    # Spin a new instance of bot
    execl(sys.executable, sys.executable, *sys.argv)
    # Shut the existing one down
    exit()


@register(outgoing=True, pattern="^.community$")
async def bot_community(community):
    """ For .community command, just returns OG Paperplane's group link. """
    await community.edit(
        "Join RaphielGang's awesome userbot community: @userbot_support"
        "\nDo note that Paperplane Extended is an unoficial fork of their "
        "Paperplane project and it may get limited or no support for bugs.")


@register(outgoing=True, pattern="^.support$")
async def bot_support(wannahelp):
    """ For .support command, just returns the group link. """
    await wannahelp.edit(
        "Join the OpenUserBot Channel: @PaperPlaneExtended_news \
        \nJoin the OpenUserBot Chat: @PPE_Support")


@register(outgoing=True, pattern="^.creator$")
async def creator(e):
    await e.edit("[Heyworld](https://github.com/sahyam2019)")


@register(outgoing=True, pattern="^.readme$")
async def reedme(e):
    await e.edit(
        "Here's something for you to read:\n"
        "\n[OpenUserBot's README.md file](https://github.com/mkaraniya/OpenUserBot/blob/sql-extended/README.md)"
        "\n[Setup Guide - Basic](https://telegra.ph/How-to-host-a-Telegram-Userbot-11-02)"
        "\n[Setup Guide - Google Drive](https://telegra.ph/How-To-Setup-GDrive-11-02)"
        "\n[Setup Guide - LastFM Module](https://telegra.ph/How-to-set-up-LastFM-module-for-Paperplane-userbot-11-02)"
        "\n[Video Tutorial - 576p](https://mega.nz/#!ErwCESbJ!1ZvYAKdTEfb6y1FnqqiLhHH9vZg4UB2QZNYL9fbQ9vs)"
        "\n[Video Tutorial - 1080p](https://mega.nz/#!x3JVhYwR!u7Uj0nvD8_CyyARrdKrFqlZEBFTnSVEiqts36HBMr-o)"
        "\n[Special - Note](https://telegra.ph/Special-Note-11-02)")
    

# Copyright (c) Gegham Zakaryan | 2019
@register(outgoing=True, pattern="^.repeat (.*)")
async def repeat(rep):
    cnt, txt = rep.pattern_match.group(1).split(' ', 1)
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for i in range(0, replyCount - 1):
        replyText += toBeRepeated + "\n"

    await rep.edit(replyText)


@register(outgoing=True, pattern="^.repo$")
async def repo_is_here(wannasee):
    """ For .repo command, just returns the repo URL. """
    await wannasee.edit(
        "Click [here](https://github.com/sahyam2019/oub-remix) to open oub-remix's GitHub page."
    )

    
@register(outgoing=True, pattern="^.myrepo$")
async def myrepo_is_here(wannaseeme):
    """ For .myrepo command, just returns the repo URL. """
    await wannaseeme.edit(
        f'Click [here](https://github.com/{GIT_REPO_NAME}/tree/sql-extended/) to open {DEFAULTUSER}`s GitHub page'
    )

@register(outgoing=True, pattern="^.raw$")
async def raw(event):
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    with io.BytesIO(str.encode(the_real_message)) as out_file:
        out_file.name = "raw_message_data.txt"
        await event.edit(
            "`Check the userbot log for the decoded message data !!`")
        await event.client.send_file(
            BOTLOG_CHATID,
            out_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            caption="`Here's the decoded message data !!`")

@register(outgoing=True, pattern=r"^.reverse(?: |$)(\d*)")
async def okgoogle(img):
    """ For .reverse command, Google search images and stickers. """
    if os.path.isfile("okgoogle.png"):
        os.remove("okgoogle.png")

    message = await img.get_reply_message()
    if message and message.media:
        photo = io.BytesIO()
        await bot.download_media(message, photo)
    else:
        await img.edit("`Reply to photo or sticker nigger.`")
        return

    if photo:
        await img.edit("`Processing...`")
        try:
            image = Image.open(photo)
        except OSError:
            await img.edit('`Unsupported sexuality, most likely.`')
            return
        name = "okgoogle.png"
        image.save(name, "PNG")
        image.close()
        # https://stackoverflow.com/questions/23270175/google-reverse-image-search-using-post-request#28792943
        searchUrl = 'https://www.google.com/searchbyimage/upload'
        multipart = {
            'encoded_image': (name, open(name, 'rb')),
            'image_content': ''
        }
        response = requests.post(searchUrl,
                                 files=multipart,
                                 allow_redirects=False)
        fetchUrl = response.headers['Location']

        if response != 400:
            await img.edit("`Image successfully uploaded to Google. Maybe.`"
                           "\n`Parsing source now. Maybe.`")
        else:
            await img.edit("`Google told me to fuck off.`")
            return

        os.remove(name)
        match = await ParseSauce(fetchUrl +
                                 "&preferences?hl=en&fg=1#languages")
        guess = match['best_guess']
        imgspage = match['similar_images']

        if guess and imgspage:
            await img.edit(f"[{guess}]({fetchUrl})\n\n`Looking for images...`")
        else:
            await img.edit("`Couldn't find anything for your uglyass.`")
            return

        if img.pattern_match.group(1):
            lim = img.pattern_match.group(1)
        else:
            lim = 3
        images = await scam(match, lim)
        yeet = []
        for i in images:
            k = requests.get(i)
            yeet.append(k.content)
        try:
            await img.client.send_file(entity=await
                                       img.client.get_input_entity(img.chat_id
                                                                   ),
                                       file=yeet,
                                       reply_to=img)
        except TypeError:
            pass
        await img.edit(
            f"[{guess}]({fetchUrl})\n\n[Visually similar images]({imgspage})")


async def ParseSauce(googleurl):
    """Parse/Scrape the HTML code for the info we want."""

    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, 'html.parser')

    results = {'similar_images': '', 'best_guess': ''}

    try:
        for similar_image in soup.findAll('input', {'class': 'gLFyf'}):
            url = 'https://www.google.com/search?tbm=isch&q=' + \
                urllib.parse.quote_plus(similar_image.get('value'))
            results['similar_images'] = url
    except BaseException:
        pass

    for best_guess in soup.findAll('div', attrs={'class': 'r5a77d'}):
        results['best_guess'] = best_guess.get_text()

    return results


async def scam(results, lim):

    single = opener.open(results['similar_images']).read()
    decoded = single.decode('utf-8')

    imglinks = []
    counter = 0

    pattern = r'^,\[\"(.*[.png|.jpg|.jpeg])\",[0-9]+,[0-9]+\]$'
    oboi = re.findall(pattern, decoded, re.I | re.M)

    for imglink in oboi:
        counter += 1
        if not counter >= int(lim):
            imglinks.append(imglink)
        else:
            break

    return imglinks

CMD_HELP.update({
    "misc":
    "`.random` <item1> <item2> ... <itemN>\
\nUsage: Get a random item from the list of items.\
\n\n`.sleep` <seconds>\
\nusage:Userbots get tired too. Let yours snooze for a few seconds.\
\n\n`.shutdown`\
\nUsage: Shutdowns the bot temporarily\
\n\n`.support`\
\nUsage: if you need help, use this command\
\n\n`.community`\
\nUsage: Join the awesome OpenUserBot community !!\
\n\n`.repo`\
\nUsage: If you are curious what makes the userbot work, this is what you need !!\
\n\n`.myrepo`\
\nUsage: If you are curious which is your personal repo, this is what you have.\
\n\n`.readme`\
\nUsage: Provide links to setup the userbot and it's modules.\
\n\n`.creator`\
\nUsage: Know who created this awesome userbot !!\
\n\n`.repeat` <no.> <text>\
\nUsage: Repeats the text for a number of times. Don't confuse this with spam tho.\
\n\n`.restart`\
\nUsage: Restarts the bot !!\
\n\n`.raw`\
\nUsage: Get detailed JSON-like formatted data about replied message.\
\n\n`.reverse`\
\nUsage: Reply to a pic/sticker to revers-search it on Google Images !!"    
})
