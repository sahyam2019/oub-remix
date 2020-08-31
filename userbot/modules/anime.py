# Copyright (C) 2020 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import asyncio
import html
import json
import textwrap
from io import BytesIO, StringIO
from urllib.parse import quote as urlencode

import aiohttp
import bs4
import jikanpy
import requests
from html_telegraph_poster import TelegraphPoster
from jikanpy import Jikan
from jikanpy.exceptions import APIException
from telethon.errors.rpcerrorlist import FilePartsInvalidError
from telethon.tl.types import (DocumentAttributeAnimated,
                               DocumentAttributeFilename, MessageMediaDocument)
from telethon.utils import is_image, is_video

from userbot import CMD_HELP
from userbot.events import register

jikan = Jikan()

# Anime Helper


def getPosterLink(mal):
    # grab poster from kitsu
    kitsu = getKitsu(mal)
    image = requests.get(f"https://kitsu.io/api/edge/anime/{kitsu}").json()
    return image["data"]["attributes"]["posterImage"]["original"]


def getKitsu(mal):
    # get kitsu id from mal id
    link = f"https://kitsu.io/api/edge/mappings?filter[external_site]=myanimelist/anime&filter[external_id]={mal}"
    result = requests.get(link).json()["data"][0]["id"]
    link = f"https://kitsu.io/api/edge/mappings/{result}/item?fields[anime]=slug"
    kitsu = requests.get(link).json()["data"]["id"]
    return kitsu


def getBannerLink(mal, kitsu_search=True):
    # try getting kitsu backdrop
    if kitsu_search:
        kitsu = getKitsu(mal)
        image = f"http://media.kitsu.io/anime/cover_images/{kitsu}/original.jpg"
        response = requests.get(image)
        if response.status_code == 200:
            return image
    # try getting anilist banner
    query = """
    query ($idMal: Int){
        Media(idMal: $idMal){
            bannerImage
        }
    }
    """
    data = {"query": query, "variables": {"idMal": int(mal)}}
    image = requests.post("https://graphql.anilist.co",
                          json=data).json()["data"]["Media"]["bannerImage"]
    if image:
        return image
    return getPosterLink(mal)


def get_anime_manga(mal_id, search_type, _user_id):
    jikan = jikanpy.jikan.Jikan()
    if search_type == "anime_anime":
        result = jikan.anime(mal_id)
        trailer = result["trailer_url"]
        if trailer:
            LOL = f"<a href='{trailer}'>Trailer</a>"
        else:
            LOL = "<code>No Trailer Available</code>"
        image = getBannerLink(mal_id)
        studio_string = ", ".join(
            studio_info["name"] for studio_info in result["studios"]
        )
        producer_string = ", ".join(
            producer_info["name"] for producer_info in result["producers"]
        )
    elif search_type == "anime_manga":
        result = jikan.manga(mal_id)
        image = result["image_url"]
    caption = f"📺 <a href='{result['url']}'>{result['title']}</a>"
    if result["title_japanese"]:
        caption += f" ({result['title_japanese']})\n"
    else:
        caption += "\n"
    alternative_names = []
    if result["title_english"] is not None:
        alternative_names.append(result["title_english"])
    alternative_names.extend(result["title_synonyms"])
    if alternative_names:
        alternative_names_string = ", ".join(alternative_names)
        caption += f"\n<b>Also known as</b>: <code>{alternative_names_string}</code>"
    genre_string = ", ".join(genre_info["name"]
                             for genre_info in result["genres"])
    if result["synopsis"] is not None:
        synopsis = result["synopsis"].split(" ", 60)
        try:
            synopsis.pop(60)
        except IndexError:
            pass
        synopsis_string = " ".join(synopsis) + "..."
    else:
        synopsis_string = "Unknown"
    for entity in result:
        if result[entity] is None:
            result[entity] = "Unknown"
    if search_type == "anime_anime":
        caption += textwrap.dedent(
            f"""
        🆎 <b>Type</b>: <code>{result['type']}</code>
        📡 <b>Status</b>: <code>{result['status']}</code>
        🎙️ <b>Aired</b>: <code>{result['aired']['string']}</code>
        🔢 <b>Episodes</b>: <code>{result['episodes']}</code>
        💯 <b>Score</b>: <code>{result['score']}</code>
        🌐 <b>Premiered</b>: <code>{result['premiered']}</code>
        ⌛ <b>Duration</b>: <code>{result['duration']}</code>
        🎭 <b>Genres</b>: <code>{genre_string}</code>
        🎙️ <b>Studios</b>: <code>{studio_string}</code>
        💸 <b>Producers</b>: <code>{producer_string}</code>
        🎬 <b>Trailer:</b> {LOL}
        📖 <b>Synopsis</b>: <code>{synopsis_string}</code> <a href='{result['url']}'>Read More</a>
        """
        )
    elif search_type == "anime_manga":
        caption += textwrap.dedent(
            f"""
        🆎 <b>Type</b>: <code>{result['type']}</code>
        📡 <b>Status</b>: <code>{result['status']}</code>
        🔢 <b>Volumes</b>: <code>{result['volumes']}</code>
        📃 <b>Chapters</b>: <code>{result['chapters']}</code>
        💯 <b>Score</b>: <code>{result['score']}</code>
        🎭 <b>Genres</b>: <code>{genre_string}</code>
        📖 <b>Synopsis</b>: <code>{synopsis_string}</code>
        """
        )
    return caption, image


def get_poster(query):
    url_enc_name = query.replace(" ", "+")
    # Searching for query list in imdb
    page = requests.get(
        f"https://www.imdb.com/find?ref_=nv_sr_fn&q={url_enc_name}&s=all"
    )
    soup = bs4.BeautifulSoup(page.content, "lxml")
    odds = soup.findAll("tr", "odd")
    # Fetching the first post from search
    page_link = "http://www.imdb.com/" + \
        odds[0].findNext("td").findNext("td").a["href"]
    page1 = requests.get(page_link)
    soup = bs4.BeautifulSoup(page1.content, "lxml")
    # Poster Link
    image = soup.find("link", attrs={"rel": "image_src"}).get("href", None)
    if image is not None:
        # img_path = wget.download(image, os.path.join(Config.DOWNLOAD_LOCATION, 'imdb_poster.jpg'))
        return image


def post_to_telegraph(anime_title, html_format_content):
    post_client = TelegraphPoster(use_api=True)
    auth_name = "@GengKapak"
    bish = "https://t.me/GengKapak"
    post_client.create_api_token(auth_name)
    post_page = post_client.post(
        title=anime_title,
        author=auth_name,
        author_url=bish,
        text=html_format_content)
    return post_page["url"]


def replace_text(text):
    return text.replace(
        '"',
        "").replace(
        "\\r",
        "").replace(
            "\\n",
            "").replace(
                "\\",
        "")


@register(outgoing=True, pattern=r"^\.anime ?(.*)")
async def anime(event):
    query = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    await event.edit("`Searching Anime...`")
    if query:
        pass
    elif reply:
        query = reply.text
    else:
        await event.edit("`Bruh.. What I am supposed to search ?`")
        await asyncio.sleep(6)
        await event.delete()
        return
    try:
        res = jikan.search("anime", query)
    except Exception as err:
        await event.edit(f"**Error:** \n`{err}`")
        return
    try:
        res = res.get("results")[0].get("mal_id")  # Grab first result
    except APIException:
        await event.edit("`Error connecting to the API. Please try again!`")
        return
    if res:
        anime = jikan.anime(res)
        title = anime.get("title")
        japanese = anime.get("title_japanese")
        anime.get("title_english")
        type = anime.get("type")
        duration = anime.get("duration")
        synopsis = anime.get("synopsis")
        source = anime.get("source")
        status = anime.get("status")
        episodes = anime.get("episodes")
        score = anime.get("score")
        rating = anime.get("rating")
        genre_lst = anime.get("genres")
        genres = ""
        for genre in genre_lst:
            genres += genre.get("name") + ", "
        genres = genres[:-2]
        studios = ""
        studio_lst = anime.get("studios")
        for studio in studio_lst:
            studios += studio.get("name") + ", "
        studios = studios[:-2]
        duration = anime.get("duration")
        premiered = anime.get("premiered")
        image_url = anime.get("image_url")
        trailer = anime.get("trailer_url")
        if trailer:
            bru = f"<a href='{trailer}'>Trailer</a>"
        else:
            pass
        url = anime.get("url")
    else:
        await event.edit("`No results Found!`")
        return
    rep = f"<b>{title}</b> - ({japanese})\n"
    rep += f"<b>Type:</b> <code>{type}</code>\n"
    rep += f"<b>Source:</b> <code>{source}</code>\n"
    rep += f"<b>Status:</b> <code>{status}</code>\n"
    rep += f"<b>Genres:</b> <code>{genres}</code>\n"
    rep += f"<b>Episodes:</b> <code>{episodes}</code>\n"
    rep += f"<b>Duration:</b> <code>{duration}</code>\n"
    rep += f"<b>Score:</b> <code>{score}</code>\n"
    rep += f"<b>Studio(s):</b> <code>{studios}</code>\n"
    rep += f"<b>Premiered:</b> <code>{premiered}</code>\n"
    rep += f"<b>Rating:</b> <code>{rating}</code>\n\n"
    rep += f"<a href='{image_url}'>\u200c</a>"
    rep += f"📖 <b>Synopsis</b>: <i>{synopsis}</i>\n"
    rep += f'<b>Read More:</b> <a href="{url}">MyAnimeList</a>'
    await event.edit(rep, parse_mode="HTML", link_preview=False)


@register(outgoing=True, pattern=r"^\.manga ?(.*)")
async def manga(event):
    query = event.pattern_match.group(1)
    await event.edit("`Searching Manga...`")
    if not query:
        await event.edit("`Bruh.. Gib me Something to Search`")
        return
    res = ""
    manga = ""
    try:
        res = jikan.search("manga", query).get("results")[0].get("mal_id")
    except APIException:
        await event.edit("`Error connecting to the API. Please try again!`")
        return ""
    if res:
        try:
            manga = jikan.manga(res)
        except APIException:
            await event.edit("`Error connecting to the API. Please try again!`")
            return ""
        title = manga.get("title")
        japanese = manga.get("title_japanese")
        type = manga.get("type")
        status = manga.get("status")
        score = manga.get("score")
        volumes = manga.get("volumes")
        chapters = manga.get("chapters")
        genre_lst = manga.get("genres")
        genres = ""
        for genre in genre_lst:
            genres += genre.get("name") + ", "
        genres = genres[:-2]
        synopsis = manga.get("synopsis")
        image = manga.get("image_url")
        url = manga.get("url")
        rep = f"<b>{title} ({japanese})</b>\n"
        rep += f"<b>Type:</b> <code>{type}</code>\n"
        rep += f"<b>Status:</b> <code>{status}</code>\n"
        rep += f"<b>Genres:</b> <code>{genres}</code>\n"
        rep += f"<b>Score:</b> <code>{score}</code>\n"
        rep += f"<b>Volumes:</b> <code>{volumes}</code>\n"
        rep += f"<b>Chapters:</b> <code>{chapters}</code>\n\n"
        rep += f"<a href='{image}'>\u200c</a>"
        rep += f"📖 <b>Synopsis</b>: <i>{synopsis}</i>\n"
        rep += f'<b>Read More:</b> <a href="{url}">MyAnimeList</a>'
        await event.edit(rep, parse_mode="HTML", link_preview=False)


@register(outgoing=True, pattern=r"^\.a(kaizoku|kayo) ?(.*)")
async def site_search(event):
    message = await event.get_reply_message()
    search_query = event.pattern_match.group(2)
    site = event.pattern_match.group(1)
    if search_query:
        pass
    elif message:
        search_query = message.text
    else:
        await event.edit("`Uuf Bro.. Gib something to Search`")
        return

    if site == "kaizoku":
        search_url = f"https://animekaizoku.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {"class": "post-title"})

        if search_result:
            result = f"<a href='{search_url}'>Click Here For More Results</a> <b>of</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>: \n\n"
            for entry in search_result:
                post_link = entry.a["href"]
                post_name = html.escape(entry.text.strip())
                result += f"• <a href='{post_link}'>{post_name}</a>\n"
                await event.edit(result, parse_mode="HTML")
        else:
            result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>"
            await event.edit(result, parse_mode="HTML")

    elif site == "kayo":
        search_url = f"https://animekayo.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {"class": "title"})

        result = f"<a href='{search_url}'>Click Here For More Results</a> <b>of</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>: \n\n"
        for entry in search_result:

            if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>"
                break

            post_link = entry.a["href"]
            post_name = html.escape(entry.text.strip())
            result += f"• <a href='{post_link}'>{post_name}</a>\n"
            await event.edit(result, parse_mode="HTML")


@register(outgoing=True, pattern=r"^\.char ?(.*)")
async def character(event):
    message = await event.get_reply_message()
    search_query = event.pattern_match.group(1)
    if search_query:
        pass
    elif message:
        search_query = message.text
    else:
        await event.edit("Format: `.char <character name>`")
        return

    try:
        search_result = jikan.search("character", search_query)
    except APIException:
        await event.edit("`Character not found.`")
        return
    first_mal_id = search_result["results"][0]["mal_id"]
    character = jikan.character(first_mal_id)
    caption = f"[{character['name']}]({character['url']})"
    if character["name_kanji"] != "Japanese":
        caption += f" ({character['name_kanji']})\n"
    else:
        caption += "\n"

    if character["nicknames"]:
        nicknames_string = ", ".join(character["nicknames"])
        caption += f"\n**Nicknames** : `{nicknames_string}`"
    about = character["about"].split(" ", 60)
    try:
        about.pop(60)
    except IndexError:
        pass
    about_string = " ".join(about)
    mal_url = search_result["results"][0]["url"]
    for entity in character:
        if character[entity] is None:
            character[entity] = "Unknown"
    caption += f"\n🔰**Extracted Character Data**🔰\n\n{about_string}"
    caption += f" [Read More]({mal_url})..."
    await event.delete()
    await event.client.send_file(
        event.chat_id,
        file=character["image_url"],
        caption=replace_text(caption),
        reply_to=event,
    )


@register(outgoing=True, pattern=r"^\.upcoming ?(.*)")
async def upcoming(message):
    rep = "<b>Upcoming anime</b>\n"
    later = jikan.season_later()
    anime = later.get("anime")
    for new in anime:
        name = new.get("title")
        url = new.get("url")
        rep += f"• <a href='{url}'>{name}</a>\n"
        if len(rep) > 1000:
            break
        await message.edit(rep, parse_mode="html")


@register(outgoing=True, pattern=r"^\.scanime ?(.*)")
async def get_anime(message):
    try:
        query = message.pattern_match.group(1)
    except IndexError:
        if message.reply_to_msg_id:
            query = await message.get_reply_message().text
        else:
            await message.reply(
                "You gave nothing to search. (｡ì _ í｡)\n `Usage: .scanime <anime name>`"
            )
            return
    except Exception as err:
        await message.edit(f"**Encountered an Unknown Exception**: \n{err}")
        return

    p_rm = await message.reply("`Searching Anime...`")
    f_mal_id = ""
    try:
        jikan = jikanpy.AioJikan()
        search_res = await jikan.search("anime", query)
        f_mal_id = search_res["results"][0]["mal_id"]
    except IndexError:
        await p_rm.edit(f"No Results Found for {query}")
        return
    except Exception as err:
        await p_rm.edit(f"**Encountered an Unknown Exception**: \n{err}")
        return

    results_ = await jikan.anime(f_mal_id)
    await jikan.close()
    await message.delete()

    # Get All Info of anime
    anime_title = results_["title"]
    jap_title = results_["title_japanese"]
    eng_title = results_["title_english"]
    type_ = results_["type"]
    results_["source"]
    episodes = results_["episodes"]
    status = results_["status"]
    results_["aired"].get("string")
    results_["duration"]
    rating = results_["rating"]
    score = results_["score"]
    synopsis = results_["synopsis"]
    results_["background"]
    producer_list = results_["producers"]
    studios_list = results_["studios"]
    genres_list = results_["genres"]

    # Info for Buttons
    mal_dir_link = results_["url"]
    trailer_link = results_["trailer_url"]

    main_poster = ""
    telegraph_poster = ""
    # Poster Links Search
    try:
        main_poster = get_poster(anime_title)
    except BaseException:
        pass
    try:
        telegraph_poster = getBannerLink(f_mal_id)
    except BaseException:
        pass
    # if not main_poster:
    main_poster = telegraph_poster
    if not telegraph_poster:
        telegraph_poster = main_poster

    genress_md = ""
    producer_md = ""
    studio_md = ""
    for i in genres_list:
        genress_md += f"{i['name']} "
    for i in producer_list:
        producer_md += f"[{i['name']}]({i['url']}) "
    for i in studios_list:
        studio_md += f"[{i['name']}]({i['url']}) "

    # Build synopsis telegraph post
    html_enc = ""
    html_enc += f"<img src = '{telegraph_poster}' title = {anime_title}/>"
    html_enc += "<br><b>» Synopsis: </b></br>"
    html_enc += f"<br><em>{synopsis}</em></br>"
    synopsis_link = post_to_telegraph(anime_title, html_enc)

    # Build captions:
    captions = f"""📺  `{anime_title}` - `{eng_title}` - `{jap_title}`
**🎭 Genre:** `{genress_md}`
**🆎 Type:** `{type_}`
**🔢 Episodes:** `{episodes}`
**📡 Status:** `{status}`
**🔞 Rating:** `{rating}`
**💯 Score:** `{score}`
[📖 Synopsis]({synopsis_link})
[🎬 Trailer]({trailer_link})
[📚 More Info]({mal_dir_link})
"""

    await p_rm.delete()
    await message.client.send_file(message.chat_id, file=main_poster, caption=captions)


@register(outgoing=True, pattern=r"^\.smanga ?(.*)")
async def manga(message):
    search_query = message.pattern_match.group(1)
    await message.get_reply_message()
    await message.edit("`Searching Manga..`")
    jikan = jikanpy.jikan.Jikan()
    search_result = jikan.search("manga", search_query)
    first_mal_id = search_result["results"][0]["mal_id"]
    caption, image = get_anime_manga(
        first_mal_id, "anime_manga", message.chat_id)
    await message.delete()
    await message.client.send_file(
        message.chat_id, file=image, caption=caption, parse_mode="HTML"
    )


@register(outgoing=True, pattern=r"^\.sanime ?(.*)")
async def anime(message):
    search_query = message.pattern_match.group(1)
    await message.get_reply_message()
    await message.edit("`Searching Anime..`")
    jikan = jikanpy.jikan.Jikan()
    search_result = jikan.search("anime", search_query)
    first_mal_id = search_result["results"][0]["mal_id"]
    caption, image = get_anime_manga(
        first_mal_id, "anime_anime", message.chat_id)
    try:
        await message.delete()
        await message.client.send_file(
            message.chat_id, file=image, caption=caption, parse_mode="HTML"
        )
    except BaseException:
        image = getBannerLink(first_mal_id, False)
        await message.client.send_file(
            message.chat_id, file=image, caption=caption, parse_mode="HTML"
        )


CMD_HELP.update({
    "anime":
    "`.anime` <anime>\
    \nUsage: Returns with Anime information.\
    \n\n`.manga` <manga name>\
    \nUsage: Returns with the Manga information.\
    \n\n`.akaizoku` or `.akayo` <anime name>\
    \nUsage: Returns with the Anime Download link.\
    \n\n`.char` <character name>\
    \nUsage: Return with character information.\
    \n\n`.upcoming`\
    \nUsage: Returns with Upcoming Anime information.\
    \n\n`.scanime` <anime> or .sanime <anime>\
    \nUsage: Search anime.\
    \n\n`.smanga` <manga>\
    \nUsage: Search manga."
})
