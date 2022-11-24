import textwrap
from io import BytesIO
import random
from PIL import Image, ImageDraw, ImageFont


def create_captcha(text) -> BytesIO:
    front = Image.open("assets/alexflipnote/captcha/start.png")

    txt = Image.new("RGBA", (len(text) * 15, 189))

    fnt = ImageFont.truetype('assets/alexflipnote/_fonts/Roboto.ttf', 30)
    d = ImageDraw.Draw(txt)

    w, h = d.textsize(text, font=fnt)
    w = max(450, w)

    mid = Image.new("RGBA", (w + 201, 189), (255, 255, 255, 0))

    midd = Image.open("assets/alexflipnote/captcha/mid.png")
    end = Image.open("assets/alexflipnote/captcha/end.png")

    for i in range(0, w):
        mid.paste(midd, (i, 0))
    mid.paste(end, (w, 0))

    txt = Image.new("RGBA", (w + 201, 189), (255, 255, 255, 0))

    d = ImageDraw.Draw(txt)
    d.text((10, 73), text, font=fnt, fill=(0, 0, 0, 255))

    mid = Image.alpha_composite(mid, txt)

    im = Image.new("RGBA", (w + 323, 189))

    im.paste(front, (0, 0))
    im.paste(mid, (122, 0))

    bio = BytesIO()
    im.save(bio, "PNG")
    bio.seek(0)
    return bio


def create_drake(top, bottom, image_template: str = None) -> BytesIO:
    top_text = textwrap.fill(top, 13)
    bottom_text = textwrap.fill(bottom, 13)

    b = BytesIO()
    template_use = image_template if image_template else 'template.jpg'
    base = Image.open(f"assets/alexflipnote/drake/{template_use}").convert("RGBA")
    txtO = Image.new("RGBA", base.size, (255, 255, 255, 0))
    font = ImageFont.truetype("assets/alexflipnote/_fonts/verdana_edited.ttf", 35)

    top_pos = 85 + (-12 * len(top_text.split("\n")) + 10)
    bottom_pos = 335 + (-12 * len(bottom_text.split("\n")) + 10)

    canv = ImageDraw.Draw(txtO)
    canv.text((250, top_pos), top_text, font=font, fill="Black")
    canv.text((250, bottom_pos), bottom_text, font=font, fill="Black")

    out = Image.alpha_composite(base, txtO)

    out.save(b, "PNG")
    b.seek(0)
    return b


def create_calling(text):
    final_text = textwrap.fill(text, 33)
    b = BytesIO()

    base = Image.open("assets/alexflipnote/calling/template.jpg").convert("RGBA")
    txtO = Image.new("RGBA", base.size, (255, 255, 255, 0))
    font = ImageFont.truetype("assets/alexflipnote/_fonts/verdana_edited.ttf", 35)

    canv = ImageDraw.Draw(txtO)
    canv.text((5, 5), final_text, font=font, fill="Black")

    out = Image.alpha_composite(base, txtO)

    out.save(b, "PNG")
    b.seek(0)
    return b


helper_icons = {
    "1": "Grass block", "2": "Diamond", "3": "Diamond sword",
    "4": "Creeper", "5": "Pig", "6": "TNT",
    "7": "Cookie", "8": "Heart", "9": "Bed",
    "10": "Cake", "11": "Sign", "12": "Rail",
    "13": "Crafting bench", "14": "Redstone", "15": "Fire",
    "16": "Cobweb", "17": "Chest", "18": "Furnace",
    "19": "Book", "20": "Stone block", "21": "Wooden plank block",
    "22": "Iron ingot", "23": "Gold ingot", "24": "Wooden door",
    "25": "Iron Door", "26": "Diamond chestplate", "27": "Flint and steel",
    "28": "Glass bottle", "29": "Splash potion", "30": "Creeper spawnegg",
    "31": "Coal", "32": "Iron sword", "33": "Bow",
    "34": "Arrow", "35": "Iron chestplate", "36": "Bucket",
    "37": "Bucket with water", "38": "Bucket with lava", "39": "Bucket with milk",
    "40": "Diamond boots", "41": "Wooden hoe", "42": "Bread", "43": "Wooden sword",
    "44": "Bone", "45": "Oak log"
}


def create_achievement(title: str, ach: str, colour=(255, 255, 0, 255), icon: int = None):
    randomimage = icon if icon else random.randint(1, 45)
    front = Image.open(f"assets/alexflipnote/achievement/{randomimage}.png")

    txt = Image.new("RGBA", (len(ach) * 15, 64))

    fnt = ImageFont.truetype('assets/alexflipnote/_fonts/Minecraft.ttf', 16)
    d = ImageDraw.Draw(txt)

    w, h = d.textsize(ach, font=fnt)
    w = max(320, w)

    mid = Image.new("RGBA", (w + 20, 64), (255, 255, 255, 0))

    midd = Image.open("assets/alexflipnote/achievement/achmid.png")
    end = Image.open("assets/alexflipnote/achievement/achend.png")

    for i in range(0, w):
        mid.paste(midd, (i, 0))
    mid.paste(end, (w, 0))

    txt = Image.new("RGBA", (w + 20, 64), (255, 255, 255, 0))

    d = ImageDraw.Draw(txt)
    d.text((0, 9), title, font=fnt, fill=colour)
    d.text((0, 29), ach, font=fnt, fill=(255, 255, 255, 255))

    mid = Image.alpha_composite(mid, txt)

    im = Image.new("RGBA", (w + 80, 64))

    im.paste(front, (0, 0))
    im.paste(mid, (60, 0))

    bio = BytesIO()
    im.save(bio, "PNG")
    bio.seek(0)
    return bio


def create_scroll(content):
    f_text = textwrap.fill(content, 10)

    if len(f_text.split("\n")) > 6:
        return "Too many lines", 400

    base = Image.open("assets/alexflipnote/sot/template.jpg").convert("RGBA")
    txtO = Image.new("RGBA", base.size, (255, 255, 255, 0))
    font = ImageFont.truetype("assets/alexflipnote/_fonts/verdana_edited.ttf", 15)

    canv = ImageDraw.Draw(txtO)
    canv.text((95, 283), f_text, font=font, fill="Black")

    txtO = txtO.rotate(2, resample=Image.BICUBIC)
    out = Image.alpha_composite(base, txtO)

    b = BytesIO()
    out.save(b, "PNG")
    b.seek(0)
    return b
