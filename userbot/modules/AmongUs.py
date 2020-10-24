from .. import loader, utils
from requests import get
from io import BytesIO
from random import randint, choice
from PIL import Image, ImageFont, ImageDraw
from textwrap import wrap

class AmongUsMod(loader.Module):
    """Символ пмздабольства 2020"""
    strings = {
        "name": "Among Us"
    }

    async def client_ready(self, client, db):
        self.client = client

    
    @loader.owner
    async def sayliecmd(self, message):
        clrs = {'red': 1, 'lime': 2, 'green': 3, 'blue': 4, 'cyan': 5, 'brown': 6, 'purple': 7, 'pink': 8, 'orange': 9, 'yellow': 10, 'white': 11, 'black': 12}
        """текст или реплай"""
        clr = randint(1,12)
        text = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if text in clrs:
            clr = clrs[text]
            text = None
        if not text:
            if not reply:
                await bruh(message, message.sender)
                return
            if not reply.text:
                await bruh(message, reply.sender)
                return
            text = reply.raw_text
        
        if text.split(" ")[0] in clrs:
            clr = clrs[text.split(" ")[0]]
            text = " ".join(text.split(" ")[1:])
            
        if text == "colors":
            await message.edit("Доступные цвета:\n"+("\n".join([f"• <code>{i}</code>" for i in list(clrs.keys())])))
            return
        
        url = "https://raw.githubusercontent.com/KeyZenD/AmongUs/master/"
        font = ImageFont.truetype(BytesIO(get(url+"bold.ttf").content), 60)
        imposter = Image.open(BytesIO(get(f"{url}{clr}.png").content))
        text_ = "\n".join(["\n".join(wrap(part, 30)) for part in text.split("\n")])
        w, h = ImageDraw.Draw(Image.new("RGB", (1,1))).multiline_textsize(text_, font, stroke_width=2)
        text = Image.new("RGBA", (w+30, h+30))
        ImageDraw.Draw(text).multiline_text((15,15), text_, "#FFF", font, stroke_width=2, stroke_fill="#000")
        w = imposter.width + text.width + 10
        h = max(imposter.height, text.height)
        image = Image.new("RGBA", (w, h))
        image.paste(imposter, (0, h-imposter.height), imposter)
        image.paste(text, (w-text.width, 0), text)
        image.thumbnail((512, 512))
        output = BytesIO()
        output.name = "imposter.webp"
        image.save(output)
        output.seek(0)
        await message.delete()
        await message.client.send_file(message.to_id, output, reply_to=reply)
        
async def bruh(message, user):
    fn = user.first_name
    ln = user.last_name
    name = fn + (" "+ln if ln else "")
    name = "<b>"+name
    await message.edit(name+choice([" ", " не "])+"был предателем!</b>")