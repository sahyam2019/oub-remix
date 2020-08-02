import pyaztro

from userbot.events import register

ASTRO = ""


@register(outgoing=True, disable_errors=True, pattern=r"^\.hc (.*)")
async def astro(e):
    await e.edit("Fetching data...")
    if not e.pattern_match.group(1):
        x = ASTRO
        if not x:
            await e.edit("Not Found.")
            return
    else:
        x = e.pattern_match.group(1)
    horoscope = pyaztro.Aztro(sign=x)
    mood = horoscope.mood
    lt = horoscope.lucky_time
    desc = horoscope.description
    col = horoscope.color
    com = horoscope.compatibility
    ln = horoscope.lucky_number

    result = (
        f"**Horoscope for `{x}`**:\n"
        f"**Mood :** `{mood}`\n"
        f"**Lucky Time :** `{lt}`\n"
        f"**Lucky Color :** `{col}`\n"
        f"**Lucky Number :** `{ln}`\n"
        f"**Compatibility :** `{com}`\n"
        f"**Description :** `{desc}`\n"
    )

    await e.edit(result)