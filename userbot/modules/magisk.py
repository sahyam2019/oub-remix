# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands related to android"""

import re
from requests import get
from bs4 import BeautifulSoup

from userbot import CMD_HELP
from userbot.events import register

GITHUB = 'https://github.com'
DEVICES_DATA = 'https://raw.githubusercontent.com/androidtrackers/' \
               'certified-android-devices/master/devices.json'


@register(outgoing=True, pattern="^.magisk$")
async def magisk(request):
    """ magisk latest releases """
    magisk_dict = {
        "Stable":
        "https://raw.githubusercontent.com/topjohnwu/magisk_files/master/stable.json",
        "Beta":
        "https://raw.githubusercontent.com/topjohnwu/magisk_files/master/beta.json",
        "Canary (Release)":
        "https://raw.githubusercontent.com/topjohnwu/magisk_files/canary/release.json",
        "Canary (Debug)":
        "https://raw.githubusercontent.com/topjohnwu/magisk_files/canary/debug.json"
    }
    releases = 'Latest Magisk Releases:\n'
    for name, release_url in magisk_dict.items():
        data = get(release_url).json()
        releases += f'{name}: [ZIP v{data["magisk"]["version"]}]({data["magisk"]["link"]}) | ' \
                    f'[APK v{data["app"]["version"]}]({data["app"]["link"]}) | ' \
                    f'[Uninstaller]({data["uninstaller"]["link"]})\n'
    await request.edit(releases)



CMD_HELP.update({
        "magisk": 
        ".magisk"
        "\nUsage: see it urself.\n"
    })
