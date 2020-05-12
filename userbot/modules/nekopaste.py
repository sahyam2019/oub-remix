from requests import get, post, exceptions
import asyncio
import os
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, LOGS, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register

nekourl = "https://nekobin.com/"


@register(outgoing=True, pattern=r"^.npaste(?: |$)([\s\S]*)")
async def paste(pstl):
    """ For .npaste command, pastes the text directly to nekobin. """
    nekobin_final_url = ""
    match = pstl.pattern_match.group(1).strip()
    reply_id = pstl.reply_to_msg_id

    if not match and not reply_id:
        await pstl.edit("`noob i caanot paste void.`")
        return

    if match:
        message = match
    elif reply_id:
        message = (await pstl.get_reply_message())
        if message.media:
            downloaded_file_name = await pstl.client.download_media(
                message,
                TEMP_DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r"
            os.remove(downloaded_file_name)
        else:
            message = message.message

    # Nekobin
    await pstl.edit("`Pasting text . . .`")
    resp = post(nekourl + "documents", data=message.encode('utf-8'))

    if resp.status_code == 200:
        response = resp.json()
        key = response['key']
        nekobin_final_url = nekourl + key

        if response['isUrl']:
            reply_text = ("`Pasted successfully!`\n\n"
                          f"`Shortened URL:` {nekobin_final_url}\n\n"
                          "`Original(non-shortened) URLs`\n"
                          f"`Nekobin URL`: {nekourl}v/{key}\n")
        else:
            reply_text = ("`Pasted successfully!`\n\n"
                          f"`nekobin URL`: {nekobin_final_url}")
    else:
        reply_text = ("`Failed to reach nekobin`")

    await pstl.edit(reply_text)
    if BOTLOG:
        await pstl.client.send_message(
            BOTLOG_CHATID,
            f"NekoPaste query was executed successfully",
        )
