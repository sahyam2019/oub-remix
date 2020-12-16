# Copyright (C) 2020 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.

# custom cmds by @Nitesh_231 for personal use 👀

""" Userbot module for having some fun with people. """
import asyncio
import html
import os
from random import choice, randint
from re import sub

from PIL import Image, ImageColor

from userbot import CMD_HELP, LOGS, bot
from userbot.events import register

# ================= CONSTANT =================

RAPE_STRINGS = [
    "`Rape Done Drink The Cum`",
    "`EK baat yaad rkhio, Chut ka Chakkar matlab maut se takkar`",
    "`The user has been successfully raped`",
    "`Dekho Bhaiyya esa hai! Izzat bachailo apni warna Gaand maar lenge tumhari`",
    "`Relax your Rear, ders nothing to fear,The Rape train is finally here`",
    "`Rape coming... Raped! haha 😆`",
    "`Kitni baar Rape krvyega mujhse?`",
    "`Tu Randi hai Sabko pta hai😂`",
    "`Don't rape too much bossdk, else problem....`",
    "`Tu sasti rendi hai Sabko pta hai😂`",
    "`Lodu Andha hai kya Yaha tera rape ho raha hai aur tu abhi tak yahi gaand mara raha hai lulz`",
]

ABUSE_STRINGS = [
    "`Madharchod`",
    "`Gaandu`",
    "`Randi ka bacha bsdk`",
    "`MUH Me lega Maderchod 🙂`",
    "`Chutiya he rah jaye ga`",
    "`Ja be Gaandu`",
    "`Ma ka Bharosa madharchod`",
    "Jyda gand na fulao BSDK`",
    "`mml`",
    "`You MotherFeker`",
    "`Muh Me Lega Bhosdike ?`"
    "`Kro Gandu giri kam nhi toh Gand Maar lenge tumhari hum😂`",
    "`Suno Lodu Jyda muh na chalo be muh me lawda pel Diyaa jayega`",
    "`Sharam aagyi toh aakhe juka lijia land me dam nhi hai apke toh Shilajit kha lijia`",
    "`Kahe Rahiman Kaviraaj C**t Ki Mahima Aisi,L**d Murjha Jaaye Par Ch**t Waisi Ki Waisi`",
    "`Chudakkad Raand Ki Ch**T Mein Pele L*Nd Kabeer, Par Aisa Bhi Kya Choda Ki Ban Gaye Fakeer`",
]

CHU_STRINGS = [
    "`Taare hai Asmaan me very very bright jaat na jla bskd dekh le apni hight.`",
    "`jindagi ki na toote lari iski lulli hoti nhi khadi`",
    "`Kbhi kbhi meri dil me khyaal ata hai ayse chutiyo ko kon paida kr jata hai😂.`",
    "`Saawan ka mahina pawan kare shor jake gand mara bskd kahi aur.`",
    "`Dil ke armaa ansuon me beh jaye tum bskd ke chutiye hi reh gye.`",
    "`Ishq Se Tabiyat Ne Zeest Ka Mazaa aya maine is lodu ko randi khane me paya.`",
    "`Mirza galib ki yeh khani hai tu bhosdika hai yeh sab ki jubani hai.`",
]

FUK_STRINGS = [
    "`It's better to let someone think you are an Idiot than to open your mouth and prove it.`",
    "`Talking to a liberal is like trying to explain social media to a 70 years old`",
    "`CHAND PE HAI APUN LAVDE.`",
    "`Pehle main tereko chakna dega, fir daru pilayega, fir jab aap dimag se nahi L*nd se sochoge, tab bolega..`",
    "`Pardhan mantri se number liya, parliament apne :__;baap ka hai...`",
    "`Cachaa Ooo bhosdi wale Chacha`",
    "`Aaisi Londiya Chodiye, L*nd Ka Aapa Khoye, Auro Se Chudi Na Ho, Biwi Wo Hi Hoye`",
    "`Nachoo Bhosdike Nachoo`",
    "`Jinda toh jaat ke baal bhi hai`",
    "`Sab ko pta tu randi ka baccha hai (its just a joke)`",
]

THANOS_STRINGS = [
    "`Mashoor Rand, Ne Arz Kiya Hai. Aane Wale Aate Hai, Jaane Wale Jaate Hai. Yaade Bas Unki Reh Jaati Hai, Jo G**Nd Sujaa Ke Jaate Hai`",
    "`Pani kam hai matkey me ga*d mardunga teri ek jatke me`",
    "`Aand kitne bhi bade ho, lund ke niche hi rehte hai`",
    "`Tum Ameer hum gareeb hum jhopdiwale Tum bhosiwale`",
    "`Sisi Bhari Gulab ki padi palang ke pass chodne wale chod gye ab q baitha udaas`",
    "`Phuloo Ka Raja Gulaab Kaato me Rehta hai Jeewan ka Nirmata jaato me rehta hai😂`",
    "`Chude hue maal ko yaad mt krna Jo Chut na de usse kabhi friyad mt karna jise chudna hai wo chud ke rhegi bekar me muth maar ke apni jindagi barbaad mt krna`",
    "`Gand mare gandu Chut mare Chutiya Sabse accha mutti 2 mint me chutti😛`",
    "`Marzi Ka Sex Pap Nahi Hota.. Piche Se Dalne Wala Kabhi Baap Nahi Hota.. Condom Zarur Lagana Mere Dost Qki.. Sex K Waqt Popat Ke Pass Dimag Nahi Hota.`",
    "`Uss Ne Hothon Se Chhu Kar Lowd* Pe Nasha Kar Diya; Lu*D Ki Baat To Aur Thi, Uss Ne To Jhato* Ko Bhi Khada Kar Diya!`",
]

ABUSEHARD_STRINGS = [
    "`Madarchod Randi ke bacche.Oye bosdike madarchod bhen ke lode tere gand me lohe ka danda garam karke dalu randwe tujhetho gali ke kutte gand pe chut rakh ke katenge me bata raha hu tere lode pe madhu makkhi Katelode ke ando pe Road roller chale tu kab bathroom me muthne Jaye tho Tera loda ghir Jaye fir tere ando me se lizard ke bacche nikle teko kidnap Kare aur childporn banaye maa ke chuttad ke lode tere saat Johnny sins rape Kare aur jab wo teko anal de tab loda andar fas Jaye bkl tere jhaat pe waxing karunga me dhek lio fir jab tu chillayega na tab tere muh me Mai gai ka gobar dalunga sale tere gand ke balo pe tel laga ke jala du me teko Anaconda leke gand me dalu tho muh se nikle maa ke lode hamesha chutiyo jaisa bartav kartha he tu maa ke Dai chawal drugs tere gand Me dalunga thi tatti nahi nikle maa darchod kabhi teko Marne ka mouka mil gaya na tho bas I'll do my best to get that tatti outof you aur tere jaise chutio ko is duniya me jagaha bhi nahi maa ke lode bandarchod tere gand me chitiya Kate wo bhi bullet ants maadarchod samj nahi aaraha tere baap NE teko kya khake paida kiya Tha kesa chutiya he tu rand ke bacche teko shadi me khana khane na mile teko gand pe 4 thappad mare sab log aur blade se likhe I want anal madarchod bosdike maccharki tatte ke baal chutiye maa ke chut pe ghode ka Lund tere gand me jaltha hu koila Dale bhen ke lode MAA KI CHUT MAI TALWAR DUNGA BC CHUT FAT JAEGI AUR USME SE ITNA KHOON NIKLEGA MZA AJAEGA DEKHNE KA SALE MAA KE BHOSDE SE BAHR AJA FIR BAAP SE ZUBAN DA TERI MAA KI CHUT CHOD CHOD KE BHOSDABNADU MADARCHOD AUR USKE UPAR CENENT LAGADU KI TERE JESA GANDU INSAAN KABHI BAHR NA A SKE ESI GANDI CHUT MAI SE LODA LASUN MADRCHOD TERI MAA KI CHUT GASTI AMA KA CHUTIA BACHA TERI MAA KO CHOD CHOD K PAGAL KAR DUNGA MAA K LODY KISI SASTIII RANDII K BACHY TERI MAA KI CHOOT MAIN TEER MAARUN GANDU HARAMI TERI COLLEGE JATI BAJI KA ROAD PEY RAPE KARONGANDU KI OLAAD HARAM KI NASAL PAPA HUN TERA BHEN PESH KAR AB PAPA KO TERI MAA KKALE KUSS MAIN KIS`",
    "`Main roz teri behno ki banjar chut me apna lawda daalke andar haryali lata tha magar aaj unke ke baare me sunke mujhe bhut afsos huwa..ki unko ab bada loudha chahye..ab mera balatkaaari lawda lagataar 4 ghante tk apne muh me kon rakhega..vo teri behne hi thi jo apni kaali magar rasilli chut mere saamne khol deti aur zameen pe naagin ki tarah rengne lgti thi jaise ki kisine unki chut pe naariyal tod diya ho vo b bada wala mumbai ka naariyal..apni chennal maa ko b nhi bhej rahe mere paas to main kaixe tum logo se vaada karu ki main teri maa chodd dungaw..ab agar tun sach me chahta hai ki main tum dono k mc ki chut me dhammal karu to mera lawda apne muh me rakho aur kaho Sameer hamare sage papa hain... Aur agar tb b the apni maa ki kaali chut mere saamne nahi rakhi to tumhare ghar me ghuske tumhari maa ka balatkaar kar dungaw jaixe delhi me huwa tha...ab teri chudi hui kuttiyo ki tarah apni gaand hilaate hue mere aage kalapna mt ni to tumhari fatti bhoxdi me 100 ched karunga`",
    "`Taare hai Asmaan me very very bright jaat na jla bskd dekh le apni hight.`",
    "`Zindagi ki na toote lari iski lulli hoti nhi khadi`",
    "`Kbhi kbhi meri dil me khyaal ata hai ayse chutiyo ko kon paida kr jata hai😂.`",
    "`Saawan ka mahina pawan kare shor jake gand mara bskd kahi aur.`",
    "`Dil ke armaa ansuon me beh jaye tum bskd ke chutiye hi reh gye.`",
    "`Ishq Se Tabiyat Ne Zeest Ka Mazaa aya maine is lodu ko randi khane me paya.`",
    "`Mirza galib ki yeh khani hai tu bhosdika hai yeh sab ki jubani hai.`",
    "`Mashoor Rand, Ne Arz Kiya Hai. Aane Wale Aate Hai, Jaane Wale Jaate Hai. Yaade Bas Unki Reh Jaati Hai, Jo G**Nd Sujaa Ke Jaate Hai`",
    "`Pani kam hai matke me gand marlunga jhatke me.`",
    "`Aand kitne bhi bade ho, lund ke niche hi rehte hai`",
    "`Tum Ameer hum gareeb hum jhopdiwale Tum bhosiwale`",
    "`Sisi Bhari Gulab ki padi palang ke pass chodne wale chod gye ab q baitha udaas`",
    "`Phuloo Ka Raja Gulaab Kaato me Rehta hai Jeewan ka Nirmata jaato me rehta hai😂`",
    "`Chude hue maal ko yaad mt krna Jo Chut na de usse kabhi friyad mt karna jise chudna hai wo chud ke rhegi bekar me muth maar ke apni jindagi barbaad mt krna`",
    "`Gand mare gandu Chut mare Chutiya Sabse accha mutti 2 mint me chutti😛`",
    "`Marzi Ka Sex Pap Nahi Hota.. Piche Se Dalne Wala Kabhi Baap Nahi Hota.. Condom Zarur Lagana Mere Dost Qki.. Sex K Waqt Popat Ke Pass Dimag Nahi Hota.`",
    "`Uss Ne Hothon Se Chhu Kar Lowd* Pe Nasha Kar Diya; Lu*D Ki Baat To Aur Thi, Uss Ne To Jhato* Ko Bhi Khada Kar Diya!`",
]

IWIS = [
    "┐(´д｀)┌",
    "┐(´～｀)┌",
    "┐(´ー｀)┌",
    "┐(￣ヘ￣)┌",
    "╮(╯∀╰)╭",
    "╮(╯_╰)╭",
    "┐(´д`)┌",
    "┐(´∀｀)┌",
    "ʅ(́◡◝)ʃ",
    "┐(ﾟ～ﾟ)┌",
    "┐('д')┌",
    "┐(‘～`;)┌",
    "ヘ(´－｀;)ヘ",
    "┐( -“-)┌",
    "ʅ（´◔౪◔）ʃ",
    "ヽ(゜～゜o)ノ",
    "ヽ(~～~ )ノ",
    "┐(~ー~;)┌",
    "┐(-。ー;)┌",
    r"¯\_(ツ)_/¯",
    r"¯\_(⊙_ʖ⊙)_/¯",
    r"¯\_༼ ಥ ‿ ಥ ༽_/¯",
    "乁( ⁰͡  Ĺ̯ ⁰͡ ) ㄏ",
]

GAMBAR_TITIT = """
🍆🍆
🍆🍆🍆
  🍆🍆🍆
    🍆🍆🍆
     🍆🍆🍆
       🍆🍆🍆
        🍆🍆🍆
         🍆🍆🍆
          🍆🍆🍆
          🍆🍆🍆
      🍆🍆🍆🍆
 🍆🍆🍆🍆🍆🍆
 🍆🍆🍆  🍆🍆🍆
    🍆🍆       🍆🍆
"""

# ===========================================


@register(outgoing=True, pattern="^.rape$")
async def raping(raped):
    """ Dont Rape Too much -_-"""
    await raped.edit(choice(RAPE_STRINGS))


@register(outgoing=True, pattern="^.fuk$")
async def chutiya(fuks):
    """ String for fhu only -_-"""
    await fuks.edit(choice(FUK_STRINGS))


@register(outgoing=True, pattern="^.chu$")
async def chutiya(chus):
    """ String for Chu only -_-"""
    await chus.edit(choice(CHU_STRINGS))


@register(outgoing=True, pattern="^.thanos$")
async def thanos(thanos):
    """ String for thanos only -_-"""
    await thanos.edit(choice(THANOS_STRINGS))


@register(outgoing=True, pattern="^.abusehard$")
async def fuckedd(abusehard):
    """ Dont Use this Too much bsdk -_-"""
    await abusehard.edit(choice(ABUSEHARD_STRINGS))


@register(outgoing=True, pattern="^.abuse$")
async def abusing(abused):
    """ Dont Abuse Too much bsdk -_-"""
    await abused.edit(choice(ABUSE_STRINGS))


@register(outgoing=True, pattern="^.iwi(?: |$)(.*)")
async def faces(siwis):
    """ IwI """
    textx = await siwis.get_reply_message()
    message = siwis.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await siwis.edit("` IwI no text given lamve,Gib Some text Motherfakaq! `")
        return

    reply_text = sub(r"(a|i|u|e|o)", "i", message)
    reply_text = sub(r"(A|I|U|E|O)", "I", reply_text)
    reply_text = sub(r"\!+", " " + choice(IWIS), reply_text)
    reply_text += " " + choice(IWIS)
    await siwis.edit(reply_text)


@register(outgoing=True, pattern="^.nikal$")
async def whoizme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("Nikal")
        await asyncio.sleep(0.3)
        await e.edit("lavde")
        await asyncio.sleep(0.2)
        await e.edit("pehli")
        await asyncio.sleep(0.5)
        await e.edit("fursat")
        await asyncio.sleep(0.2)
        await e.edit("me")
        await asyncio.sleep(0.3)
        await e.edit("nikal")
        await asyncio.sleep(0.3)
        await e.edit("🤬")
        await asyncio.sleep(0.3)
        await e.edit("Nikal lavde pehli fursat me nikal 🤬")

@register(outgoing=True, pattern=r"^\.(?:penis|dick)\s?(.)?")
async def emoji_penis(titit):
    emoji = titit.pattern_match.group(1)
    titid = GAMBAR_TITIT
    if emoji:
        titid = titid.replace("🍆", emoji)
    await titit.edit(titid)


@register(outgoing=True, pattern="^.gtfo$")
async def gtfo(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(
            "`\n███████████████████████████████ `"
            "`\n█▀▀▀▀▀▀▀█▀▀▀▀▀▀█▀▀▀▀▀▀▀█▀▀▀▀▀▀█ `"
            "`\n█───────█──────█───────█──────█ `"
            "`\n█──███──███──███──███▄▄█──██──█ `"
            "`\n█──███▄▄███──███─────███──██──█ `"
            "`\n█──██───███──███──██████──██──█ `"
            "`\n█──▀▀▀──███──███──██████──────█ `"
            "`\n█▄▄▄▄▄▄▄███▄▄███▄▄██████▄▄▄▄▄▄█ `"
            "`\n███████████████████████████████ `"
        )


@register(outgoing=True, pattern=r"^.F")
async def fcmd(e):
    if e.text[0].isalpha() or e.text[0] in ("/", "#", "@", "!"):
        return
    message = e.text

    if message[-1] == "p" and message[-2] == "F":
        await e.edit("🤦‍♂")
    elif message[-1] == "F":
        await e.edit("┏━━━┓\n┃┏━━┛\n┃┗━━┓\n┃┏━━┛\n┃┃\n┗┛")

    else:
        n = message[-1]
        out = ""
        for line in [5, 1, 1, 4, 1, 1, 1]:
            c = max(line, 1)
            out += (n * c) + "\n"
        await e.edit(html.escape(out))

@register(outgoing=True, pattern="^.paw$")
async def paw(pawed):
    if not pawed.text[0].isalpha() and pawed.text[0] not in ("/", "#", "@", "!"):
        await pawed.edit("`(=ↀωↀ=)`")


@register(outgoing=True, pattern="^.retard$")
async def retard(event):
    replied = await event.get_reply_message()
    if not replied:
        return await event.edit(
            "__Reply to someone so i can check how retarded they are!__"
        )
    sender = replied.sender
    reply = f"[{sender.first_name}](tg://user?id={sender.id}) __is {randint(0, 101)}% retarded!__"
    await event.edit(reply, link_preview=False)

@register(outgoing=True, pattern="^.tf$")
async def tf(focc):
    if not focc.text[0].isalpha() and focc.text[0] not in ("/", "#", "@", "!"):
        await focc.edit("`(̿▀̿ ̿Ĺ̯̿̿▀̿ ̿)̄ ` ")


@register(pattern="^.color(?: |$)(.*)", outgoing=True)
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
    if input_str.startswith("#"):
        try:
            usercolor = ImageColor.getrgb(input_str)
        except Exception as e:
            await event.edit(str(e))
            return False
        else:
            im = Image.new(mode="RGB", size=(1280, 720), color=usercolor)
            im.save("remix.png", "PNG")
            input_str = input_str.replace("#", "#COLOR_")
            await bot.send_file(
                event.chat_id,
                "remix.png",
                force_document=False,
                caption=input_str,
                reply_to=message_id,
            )
            os.remove("remix.png")
            await event.delete()
    else:
        await event.edit("Syntax: `.color <color_code>` example : `.color #ff0000`")

CMD_HELP.update({
    "memesreborn":
    "`.fuk`\
\nUsage: Greet Evrii Nibba in da house.\
\n\n`.iwi`\
\nUsage: gib text and see magik.\
\n\n`.rape .thanos .chu .abuse .abusehard`\
\nUsage: See it yourself nibba🌚.\
\n\n`.paw`\
\nUsage: try it.\
\n\n`.dick` or `.penis`\
\nUsage: nonsense\
\n\n`.retrard`\
\nUsage: Gibs retrad %\
\n\n`.color` code\
\nUsage: generates color."
})
