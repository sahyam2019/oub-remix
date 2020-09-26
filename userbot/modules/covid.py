# Copyright (C) 2020 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.

from covid import Covid
from userbot import CMD_HELP
from userbot.events import register

def format_integer(number, thousand_separator="."):
    def reverse(string):
        string = "".join(reversed(string))
        return string

    s = reverse(str(number))
    count = 0
    result = ""
    for char in s:
        count = count + 1
        if count % 3 == 0:
            if len(s) == count:
                result = char + result
            else:
                result = thousand_separator + char + result
        else:
            result = char + result
    return result

@register(outgoing=True, pattern="^.covid (.*)")
async def corona(event):
    await event.edit("`Processing...`")
    country = event.pattern_match.group(1)
    covid = Covid(source="worldometers")
    country_data = covid.get_status_by_country_name(country)
    if country_data:
        output_text =  f"`⚠️Confirmed   : {format_integer(country_data['confirmed'])}`\n"
        output_text += f"`☢️Active      : {format_integer(country_data['active'])}`\n"
        output_text += f"`🤕Critical    : {format_integer(country_data['critical'])}`\n"
        output_text += f"`😟New Deaths  : {format_integer(country_data['new_deaths'])}`\n\n"
        output_text += f"`⚰️Deaths      : {format_integer(country_data['deaths'])}`\n"
        output_text += f"`😔New Cases   : {format_integer(country_data['new_cases'])}`\n"
        output_text += f"`😇Recovered   : {format_integer(country_data['recovered'])}`\n"
        output_text += f"`🧪Total tests : {format_integer(country_data['total_tests'])}`\n\n"
        output_text += f"Data provided by [Worldometer](https://www.worldometers.info/coronavirus/country/{country})"
    else:
        output_text = "No information yet about this country!"

    await event.edit(f"`Corona Virus Info in {country}:`\n\n{output_text}")

@register(outgoing=True, pattern="^.covid$")
async def corona(event):
    await event.edit("`Processing...`")
    country = "World"
    covid = Covid(source="worldometers")
    country_data = covid.get_status_by_country_name(country)
    if country_data:
        output_text =  f"`⚠️Confirmed   : {format_integer(country_data['confirmed'])}`\n"
        output_text += f"`☢️Active      : {format_integer(country_data['active'])}`\n"
        output_text += f"`🤕Critical    : {format_integer(country_data['critical'])}`\n"
        output_text += f"`😟New Deaths  : {format_integer(country_data['new_deaths'])}`\n\n"
        output_text += f"`⚰️Deaths      : {format_integer(country_data['deaths'])}`\n"
        output_text += f"`😔New Cases   : {format_integer(country_data['new_cases'])}`\n"
        output_text += f"`😇Recovered   : {format_integer(country_data['recovered'])}`\n"
        output_text += "`🧪Total tests : N/A`\n\n"
        output_text += f"Data provided by [Worldometer](https://www.worldometers.info/coronavirus/country/{country})"
    else:
        output_text = "No information yet about this country!"

    await event.edit(f"`Corona Virus Info in {country}:`\n\n{output_text}")


CMD_HELP.update({
        "covid":
        "`.covid `**<country>**"
        "\n`Usage: Get an information about covid-19 data in your country.`\n\n"
        "`.covid`"
        "\n`Usage: Get an information about covid-19 data in Worldwide.`\n"

    })
