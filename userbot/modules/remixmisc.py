#imported from github.com/ravana69/PornHub to userbot by @heyworld 
#please don't nuke my credits 😓
import requests
import bs4 
import re
import os
import asyncio
import zipfile
import time
import html
from io import BytesIO
from PyPDF2 import PdfFileWriter, PdfFileReader
from telethon import *
from userbot.events import register 
from pySmartDL import SmartDL
from userbot import CMD_HELP, bot, TEMP_DOWNLOAD_DIRECTORY
from telethon import events
from telethon.tl import functions, types
from urllib.parse import quote
from datetime import datetime, timedelta
from telethon.tl.types import UserStatusEmpty, UserStatusLastMonth, UserStatusLastWeek, UserStatusOffline, UserStatusOnline, UserStatusRecently, ChannelParticipantsKicked, ChatBannedRights
from time import sleep
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo
from telethon.tl.types import DocumentAttributeFilename
from userbot.modules.upload_download import progress, humanbytes, time_formatter
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.errors import PhotoInvalidDimensionsError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest

from telethon.tl.functions.messages import SendMediaRequest


import logging


logger = logging.getLogger(__name__)



if 1 == 1:
    name = "Profile Photos"
    client = bot



@register(outgoing=True, pattern="^.app(?: |$)(.*)")
async def apk(e):
    try:
        app_name = e.pattern_match.group(1)
        remove_space = app_name.split(' ')
        final_name = '+'.join(remove_space)
        page = requests.get("https://play.google.com/store/search?q="+final_name+"&c=apps")
        lnk = str(page.status_code)
        soup = bs4.BeautifulSoup(page.content,'lxml', from_encoding='utf-8')
        results = soup.findAll("div","ZmHEEd")
        app_name = results[0].findNext('div', 'Vpfmgd').findNext('div', 'WsMG1c nnK0zc').text
        app_dev = results[0].findNext('div', 'Vpfmgd').findNext('div', 'KoLSrc').text
        app_dev_link = "https://play.google.com"+results[0].findNext('div', 'Vpfmgd').findNext('a', 'mnKHRc')['href']
        app_rating = results[0].findNext('div', 'Vpfmgd').findNext('div', 'pf5lIe').find('div')['aria-label']
        app_link = "https://play.google.com"+results[0].findNext('div', 'Vpfmgd').findNext('div', 'vU6FJ p63iDd').a['href']
        app_icon = results[0].findNext('div', 'Vpfmgd').findNext('div', 'uzcko').img['data-src']
        app_details = "<a href='"+app_icon+"'>📲&#8203;</a>"
        app_details += " <b>"+app_name+"</b>"
        app_details += "\n\n<code>Developer :</code> <a href='"+app_dev_link+"'>"+app_dev+"</a>"
        app_details += "\n<code>Rating :</code> "+app_rating.replace("Rated ", "⭐ ").replace(" out of ", "/").replace(" stars", "", 1).replace(" stars", "⭐ ").replace("five", "5")
        app_details += "\n<code>Features :</code> <a href='"+app_link+"'>View in Play Store</a>"
        app_details += "\n\n===> @heyw𝖔rld <==="
        await e.edit(app_details, link_preview = True, parse_mode = 'HTML')
    except IndexError:
        await e.edit("No result found in search. Please enter **Valid app name**")
    except Exception as err:
        await e.edit("Exception Occured:- "+str(err))


        
@register(outgoing=True, pattern="^.undlt(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    c = await event.get_chat()
    if c.admin_rights or c.creator:
        a = await bot.get_admin_log(event.chat_id,limit=1, search="", edit=False, delete=True)
        for i in a:
          await event.reply(i.original.action.message)
    else:
        await event.edit("You need administrative permissions in order to do this command")
        await asyncio.sleep(3)
        await event.delete()
        
@register(outgoing=True, pattern="^.calc(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input = event.pattern_match.group(1) #get input
    exp = "Given expression is " + input #report back input
    #lazy workaround to add support for two digits
    final_input = tuple(input)
    term1part1 = final_input[0]
    term1part2 = final_input[1]
    term1 = str(term1part1) + str(term1part2)
    final_term1 = (int(term1))
    operator = str(final_input[2])
    term2part1 = final_input[3]
    term2part2 = final_input[4]
    term2 = str(term2part1) + str(term2part2)
    final_term2 = (int(term2))
    #actual calculations go here
    if input == "help":
        await event.edit("Syntax .calc <term1><operator><term2>\nFor eg .calc 02*02 or 99*99 (the zeros are important) (two terms and two digits max)")
    elif operator == "*":
        await event.edit("Solution -->\n" + exp + "\n" + str(final_term1 * final_term2))
    elif operator == "-":
        await event.edit("Solution -->\n" + exp + "\n" + str(final_term1 - final_term2))
    elif operator == "+":
        await event.edit("Solution -->\n" + exp + "\n" + str(final_term1 + final_term2))
    elif operator == "/":
        await event.edit("Solution -->\n" + exp + "\n" + str(final_term1 / final_term2))
    elif operator == "%":
        await event.edit("Solution -->\n" + exp + "\n" + str(final_term1 % final_term2))
    else:
        await event.edit("use .calc help")
        
@register(outgoing=True, pattern="^.xcd(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    xkcd_id = None
    if input_str:
        if input_str.isdigit():
            xkcd_id = input_str
        else:
            xkcd_search_url = "https://relevantxkcd.appspot.com/process?"
            queryresult = requests.get(
                xkcd_search_url,
                params={
                    "action":"xkcd",
                    "query":quote(input_str)
                }
            ).text
            xkcd_id = queryresult.split(" ")[2].lstrip("\n")
    if xkcd_id is None:
        xkcd_url = "https://xkcd.com/info.0.json"
    else:
        xkcd_url = "https://xkcd.com/{}/info.0.json".format(xkcd_id)
    r = requests.get(xkcd_url)
    if r.ok:
        data = r.json()
        year = data.get("year")
        month = data["month"].zfill(2)
        day = data["day"].zfill(2)
        xkcd_link = "https://xkcd.com/{}".format(data.get("num"))
        safe_title = data.get("safe_title")
        transcript = data.get("transcript")
        alt = data.get("alt")
        img = data.get("img")
        title = data.get("title")
        output_str = """[\u2060]({})**{}**
[XKCD ]({})
Title: {}
Alt: {}
Day: {}
Month: {}
Year: {}""".format(img, input_str, xkcd_link, safe_title, alt, day, month, year)
        await event.edit(output_str, link_preview=True)
    else:
        await event.edit("xkcd n.{} not found!".format(xkcd_id))
        
        
@register(outgoing=True, pattern="^.remove(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return False
    input_str = event.pattern_match.group(1)
    if input_str:
        chat = await event.get_chat()
        if not (chat.admin_rights or chat.creator):
            await event.edit("`You aren't an admin here!`")
            return False
    p = 0
    b = 0
    c = 0
    d = 0
    e = []
    m = 0
    n = 0
    y = 0
    w = 0
    o = 0
    q = 0
    r = 0
    await event.edit("Searching Participant Lists.")
    async for i in bot.iter_participants(event.chat_id):
        p = p + 1
        #
        # Note that it's "reversed". You must set to ``True`` the permissions
        # you want to REMOVE, and leave as ``None`` those you want to KEEP.
        rights = ChatBannedRights(
            until_date=None,
            view_messages=True
        )
        if isinstance(i.status, UserStatusEmpty):
            y = y + 1
            if "y" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await event.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusLastMonth):
            m = m + 1
            if "m" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await event.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusLastWeek):
            w = w + 1
            if "w" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await event.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusOffline):
            o = o + 1
            if "o" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await event.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusOnline):
            q = q + 1
            if "q" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await event.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusRecently):
            r = r + 1
            if "r" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await event.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if i.bot:
            b = b + 1
            if "b" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await event.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        elif i.deleted:
            d = d + 1
            if "d" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await event.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                else:
                    c = c + 1
        elif i.status is None:
            n = n + 1
    if input_str:
        required_string = """Kicked {} / {} users
Deleted Accounts: {}
UserStatusEmpty: {}
UserStatusLastMonth: {}
UserStatusLastWeek: {}
UserStatusOffline: {}
UserStatusOnline: {}
UserStatusRecently: {}
Bots: {}
None: {}"""
        await event.edit(required_string.format(c, p, d, y, m, w, o, q, r, b, n))
        await asyncio.sleep(5)
    await event.edit("""Total= {} users
Number Of Deleted Accounts= {}
Status: Empty= {}
      : Last Month= {}
      : Last Week= {}
      : Offline= {}
      : Online= {}
      : Recently= {}
Number Of Bots= {}
Unidentified= {}""".format(p, d, y, m, w, o, q, r, b, n))


async def ban_user(chat_id, i, rights):
    try:
        await bot(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)
       
@register(outgoing=True, pattern="^.grab(?: |$)(.*)")
async def potocmd(event):
        """Gets the profile photos of replied users, channels or chats"""
        id = "".join(event.raw_text.split(maxsplit=2)[1:])
        user = await event.get_reply_message()
        chat = event.input_chat
        if user:
            photos = await event.client.get_profile_photos(user.sender)
        else:
            photos = await event.client.get_profile_photos(chat)
        if id.strip() == "":
            try:
                await event.client.send_file(event.chat_id, photos)
            except a:
                photo = await event.client.download_profile_photo(chat)
                await bot.send_file(event.chat_id, photo)
        else:
            try:
                id = int(id)
                if id <= 0:
                    await event.edit("`ID number you entered is invalid`")
                    return
            except:
                 await event.edit("`lol wtf`")
                 return
            if int(id) <= (len(photos)):
                send_photos = await event.client.download_media(photos[id - 1])
                await bot.send_file(event.chat_id, send_photos)
            else:
                await event.edit("`No photo found of that Nigga , now u Die`")
                return
@register(outgoing=True, pattern="^.watermark(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    bot = await event.edit("Processing ...")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if not os.path.isdir("./downloads/"):
        os.makedirs("./downloads/")
    if event.reply_to_msg_id:
        start = datetime.now()
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await bot.download_media(
                reply_message,
                TEMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, bot, c_time, "trying to download")
                )
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await bot.edit(str(e))
        else:
            end = datetime.now()
            ms = (end - start).seconds
            await bot.edit("Stored the pdf to `{}` in {} seconds.".format(downloaded_file_name, ms))
            watermark(
                inputpdf=downloaded_file_name,
                outputpdf='./downloads/' + reply_message.file.name,
                watermarkpdf='./bin/watermark.pdf'
            )
        # filename = sorted(get_lst_of_files('./downloads/' + reply_message.file.name, []))
        #filename = filename + "/"
        await event.edit("Uploading now")
        caption_rts = os.path.basename(watermark_path + reply_message.file.name)
        await bot.send_file(
            event.chat_id,
            watermark_path + reply_message.file.name,
            reply_to=event.message.id,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "trying to upload")
            )
        )
        # r=root, d=directories, f = files
        # for single_file in filename:
        #     if os.path.exists(single_file):
        #         # https://stackoverflow.com/a/678242/4723940
        #         caption_rts = os.path.basename(single_file)
        #         force_document = False
        #         supports_streaming = True
        #         document_attributes = []
        #         if single_file.endswith((".mp4", ".mp3", ".flac", ".webm")):
        #             metadata = extractMetadata(createParser(single_file))
        #             duration = 0
        #             width = 0
        #             height = 0
        #             if metadata.has("duration"):
        #                 duration = metadata.get('duration').seconds
        #             if os.path.exists(thumb_image_path):
        #                 metadata = extractMetadata(createParser(thumb_image_path))
        #                 if metadata.has("width"):
        #                     width = metadata.get("width")
        #                 if metadata.has("height"):
        #                     height = metadata.get("height")
        #             document_attributes = [
        #                 DocumentAttributeVideo(
        #                     duration=duration,
        #                     w=width,
        #                     h=height,
        #                     round_message=False,
        #                     supports_streaming=True
        #                 )
        #             ]
        #         try:
        #             await bot.send_file(
        #                 event.chat_id,
        #                 single_file,
        #                 caption=f"`{caption_rts}`",
        #                 force_document=force_document,
        #                 supports_streaming=supports_streaming,
        #                 allow_cache=False,
        #                 reply_to=event.message.id,
        #                 attributes=document_attributes,
        #                 # progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
        #                 #     progress(d, t, event, c_time, "trying to upload")
        #                 # )
        #             )
        #         except Exception as e:
        #             await bot.send_message(
        #                 event.chat_id,
        #                 "{} caused `{}`".format(caption_rts, str(e)),
        #                 reply_to=event.message.id
        #             )
        #             # some media were having some issues
        #             continue
        #         os.remove(single_file)
        # os.remove(downloaded_file_name)

def watermark(inputpdf, outputpdf, watermarkpdf):
    watermark = PdfFileReader(watermarkpdf)
    watermarkpage = watermark.getPage(0)
    pdf = PdfFileReader(inputpdf)
    pdfwrite = PdfFileWriter()
    for page in range(pdf.getNumPages()):
        pdfpage = pdf.getPage(page)
        pdfpage.mergePage(watermarkpage)
        pdfwrite.addPage(pdfpage)
    with open(outputpdf, 'wb') as fh:
        pdfwrite.write(fh)

def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst


@register(outgoing=True, pattern="^.res(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("```Reply to a Link.```")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit("```Reply to a Link```")
       return
    chat = "@CheckRestrictionsBot"
    sender = reply_message.sender
    await event.edit("```Processing```")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=894227130))
              await event.client.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("`RIP Check Your Blacklist Boss`")
              return
          if response.text.startswith(""):
             await event.edit("Am I Dumb Or Am I Dumb?")
          else: 
             await event.delete()
             await event.client.send_message(event.chat_id, response.message)
            
            
@register(outgoing=True, pattern="^.clone(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        await event.edit(str(error_i_a))
        return False
    user_id = replied_user.user.id
    profile_pic = await event.client.download_profile_photo(user_id, TEMP_DOWNLOAD_DIRECTORY)
    # some people have weird HTML in their names
    first_name = html.escape(replied_user.user.first_name)
    # https://stackoverflow.com/a/5072031/4723940
    # some Deleted Accounts do not have first_name
    if first_name is not None:
        # some weird people (like me) have more than 4096 characters in their names
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.user.last_name
    # last_name is not Manadatory in @Telegram
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
      last_name = "⁪⁬⁮⁮⁮⁮ ‌‌‌‌"
    # inspired by https://telegram.dog/afsaI181
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = html.escape(replied_user.about)
    await bot(functions.account.UpdateProfileRequest(
        first_name=first_name
    ))
    await bot(functions.account.UpdateProfileRequest(
        last_name=last_name
    ))
    await bot(functions.account.UpdateProfileRequest(
        about=user_bio
    ))
    n = 1
    pfile = await bot.upload_file(profile_pic)  # pylint:disable=E060      
    await bot(functions.photos.UploadProfilePhotoRequest(  # pylint:disable=E0602
        pfile
    ))
    #message_id_to_reply = event.message.reply_to_msg_id
    #if not message_id_to_reply:
    #    message_id_to_reply = event.message.id
    #await borg.send_message(
    #  event.chat_id,
    #  "Hey ? Whats Up !",
    #  reply_to=message_id_to_reply,
    #  )
    await event.delete()
    await bot.send_message(
      event.chat_id,
      "**cloned like pero.**",
      reply_to=reply_message
      )

async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.from_id or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        else:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.from_id
                )
            )
            return replied_user, None
    else:
        input_str = None
        try:
            input_str = event.pattern_match.group(1)
        except IndexError as e:
            return None, e
        if event.message.entities is not None:
            mention_entity = event.message.entities
            probable_user_mention_entity = mention_entity[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            else:
                try:
                    user_object = await event.client.get_entity(input_str)
                    user_id = user_object.id
                    replied_user = await event.client(GetFullUserRequest(user_id))
                    return replied_user, None
                except Exception as e:
                    return None, e
        elif event.is_private:
            try:
                user_id = event.chat_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e
        else:
            try:
                user_object = await event.client.get_entity(int(input_str))
                user_id = user_object.id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e
            
            
CMD_HELP.update({
    "remixmisc":
    ".app\
\nUsage: type .app name and get app details.\
\n\n.undlt\
\nUsage: undo deleted message but u need admin permission.\
\n\n.calc\
\nUsage:.calc <term1><operator><term2>\nFor eg .calc 02*02 or 99*99 (the zeros are important) (two terms and two digits max).\
\n\n.remove\
\nUsage:.remove d or y or m or w or o or q or r.\n(d=deletedaccount y=userstatsempty m=userstatsmonth w=userstatsweek o=userstatsoffline q=userstatsonline r=userstatsrecently).\
\n\n.xcd\
\nUsage: type xcd <query>.ps:i have no damm idea how it works 🤷\
\n\n.grab <count>\
\nUsage:replay .grab or .grab <count> to grab profile picture.\
\n\n.watermark\
\nusage: still fixing 😔\
\n\n.clone @username\
\nusage: clone you whole freking account except username so stay safe\
\n\n.res\
\nusage: type account,channel,group or bot username and reply with .res and check restriction\
\n\n\n PS: I will add more xD" 
})
