#credits  @MarioDevs
import requests , re , random 

import urllib , os 

from telethon.tl import functions

from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
from userbot.events import register



import asyncio

from time import sleep

COLLECTION_STRING = [

  "Gravity Falls HD Wallpaper",

  "4k-sci-fi-wallpaper",

  "Anime Cat Girl Wallpaper",

  "To the Moon Wallpaper",

  "Fantasy Forest Wallpaper"

  "Japanese Scenery Wallpaper",

  "Caribbean Wallpaper Widescreen",

  "Hawaii HD Wallpaper 1920x1080",

  "Star Wars Art Wallpaper",

  "4K Anime Wallpapers"  

]

async def animepp():

    os.system("rm -rf donot.jpg")

    rnd = random.randint(0, len(COLLECTION_STRING) - 1)

    pack = COLLECTION_STRING[rnd]

    pc = requests.get("http://getwallpapers.com/collection/" + pack).text

    f = re.compile('/\w+/full.+.jpg')

    f = f.findall(pc)

    fy = "http://getwallpapers.com"+random.choice(f)

    print(fy)

    if not os.path.exists("f.ttf"):

        urllib.request.urlretrieve("https://github.com/rebel6969/mym/raw/master/Rebel-robot-Regular.ttf","f.ttf")

    urllib.request.urlretrieve(fy,"donottouch.jpg")

@register(outgoing=True, pattern="^.randpp(?: |$)(.*)")

async def main(event):

    await event.edit("**selecting random pp.......Check Your Dp After 20 Seconds") 

    while True:

        await animepp()

        file = await event.client.upload_file("donottouch.jpg")  

        await event.client(functions.photos.UploadProfilePhotoRequest( file))

        os.system("rm -rf donottouch.jpg")

        await asyncio.sleep(7200) #Edit this to your required needs