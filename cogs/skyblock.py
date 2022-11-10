import requests
import nextcord as discord
from nextcord.ext import commands
from datetime import date



def shorten_num(num):
    if num < 1000:
        return num
    elif num >= 1000 and num < 999999:
        fin = f"{round(num/1000, 2)}K"
        return fin
    elif num >= 1000000 and num < 999999999:
        fin = f"{round(num/1000000, 2)}M"
        return fin
    elif num >= 1000000000 and num < 999999999999:
        fin = f"{round(num/1000000000, 2)}B"
        return fin


def get_uuid(name):
    try:
        resp = requests.get(
            f"https://api.mojang.com/users/profiles/minecraft/{name}")
        uuid = resp.json()["id"]

        return str(uuid)

    except:
        return None


def get_name(name):
    resp = requests.get(
        f"https://api.mojang.com/users/profiles/minecraft/{name}")
    name = resp.json()["name"]
    return str(name)


key = "7eea9ca3-30f9-4003-a4d9-a39149c4a02c"


class Skyblock(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["nw"])
    async def networth(self, ctx, name=None, profileb=None):
        if name == None:
            return await ctx.reply("Please enter a name!")
        if get_uuid(name) == None:
            return await ctx.reply(f"No user found with name {name}!")
        loading = await ctx.reply("<a:loading:898340114164490261>")
        true = get_name(name)
        print(f"https://api.hypixel.net/skyblock/profiles?key={key}&uuid={get_uuid(name)}")
        data = requests.get(
            f"https://api.hypixel.net/skyblock/profiles?key={key}&uuid={get_uuid(name)}"
        )
        data = data.json()
        if data['success'] == False:
            await loading.delete()
            return await ctx.reply(
                "The Hypixel API key is invalid. Please Contact Elon Musk#7655 to let them know to change it."
            )
        if profileb == None:
            times = []
            for profile in data["profiles"]:
                save = profile["last_save"]
                times.append(save)
            last = max(times)
            profile = None
            for profilea in data["profiles"]:
                save = profilea["last_save"]
                if save == last:
                    profile = profilea
                    break
        else:
            profile = None
            for profilea in data["profiles"]:
                if profilea["cute_name"].lower() == profileb.lower():
                    profile = profilea
                    break

        sa = profile["members"][get_uuid(name)]


        ac = requests.post(
            "https://skyhelper-api.glitch.me/v2/networth?key=Satsang727!",
            json={"profileData": sa,"bankBalance":profile["banking"]["balance"]})

        global st, iv, ec, ar, war, pt, tl
        dat = ac.json()['data']
        cate = dat['types']
        st = False
        iv = False
        ec = False
        ar = False
        war = False
        pt = False
        tl = False
        if "storage" in cate.keys():
            storage = dat['types']["storage"]['items'][0:5]
            st = True
        if "inventory" in cate.keys():
            inv = dat['types']['inventory']['items'][0:5]
            iv = True
        if "enderchest" in cate.keys():
            echest = dat['types']['enderchest']['items'][0:5]
            ec = True
        if "armor" in cate.keys():
            armor = dat['types']['armor']['items'][0:5]
            ar = True
        if "wardrobe" in cate.keys():
            wd = dat['types']['wardrobe']['items'][0:5]
            war = True
        if "pets" in cate.keys():
            pets = dat['types']['pets']['items'][0:5]
            pt = True
        if "accessories" in cate.keys():
            talis = dat['types']['accessories']['items'][0:5]
            tl = True

        datab = discord.Embed(title=true)
        datab.set_thumbnail(url=f"https://mc-heads.net/head/{true}")
        datab.url = f"https://sky.shiiyu.moe/stats/{true}"
        datab.color = 14298655
        datab.description = f"{true}'s networth is **${'{:,}'.format(round(dat['networth']))} ({shorten_num(int(dat['networth']))})**"
        datab.add_field(name="<:piggy_bank:937069548195180555>Purse",
                        value=shorten_num(int(dat['purse'])))
        if dat['bank'] == None:
            datab.add_field(name="<:gold_ingot:937069660757700688>Bank",
                            value="<Private>")
        else:
            datab.add_field(name="<:gold_ingot:937069660757700688>Bank",
                            value=shorten_num(int(dat['bank'])))
        datab.add_field(
            name="<:gemstone_sack:937069769327276032>Sacks's Value",
            value=shorten_num(int(dat['types']['sacks']['total'])))
        #storage value
        if st:
            its = ""
            ind = 0
            for item in storage:
                add = item["name"]
                if "recomb" in item.keys():
                    add += " <:recombobulator:937126148196958329>"
                add += f" → {shorten_num(item['price'])} \n"
                its += add
                ind += 1
                if ind == 5:
                    break

            datab.add_field(
                name=
                f'<:storage:937118891438649404>Storage value - {shorten_num(int(dat["types"]["storage"]["total"]))}',
                value=its,
                inline=False)

        # inventory value
        if iv:
            its = ""
            ind = 0
            for item in inv:
                add = item["name"]
                if "recomb" in item.keys():
                    add += " <:recombobulator:937126148196958329>"
                add += f" → {shorten_num(item['price'])} \n"
                its += add
                ind += 1
                if ind == 5:
                    break
            datab.add_field(
                name=
                f'<:plasma_flux:937135595250139146>Inventory value - {shorten_num(int(dat["types"]["inventory"]["total"]))}',
                value=its,
                inline=False)
        # echest value
        if ec:
            its = ""
            ind = 0
            for item in echest:
                add = item["name"]
                if "recomb" in item.keys():
                    add += " <:recombobulator:937126148196958329>"
                add += f" → {shorten_num(item['price'])} \n"
                its += add
                ind += 1
                if ind == 5:
                    break
            datab.add_field(
                name=
                f'<:ender_chest:937146821590020177>Enderchest value - {shorten_num(int(dat["types"]["enderchest"]["total"]))}',
                value=its,
                inline=False)
        # armor value
        if ar:
            its = ""
            ind = 0
            for item in armor:

                add = item["name"]
                if "recomb" in item.keys():
                    add += " <:recombobulator:937126148196958329>"
                add += f" → {shorten_num(item['price'])} \n"
                its += add
                ind += 1
                if ind == 5:
                    break
            datab.add_field(
                name=
                f'<:superior_helmet:937147110053273722>Armor value - {shorten_num(int(dat["types"]["armor"]["total"]))}',
                value=its,
                inline=False)
        # wardrobe value
        if war:
            its = ""
            ind = 0
            for item in wd:

                add = item["name"]
                if "recomb" in item.keys():
                    add += " <:recombobulator:937126148196958329>"
                add += f" → {shorten_num(item['price'])} \n"
                its += add
                ind += 1
                if ind == 5:
                    break
            datab.add_field(
                name=
                f'<:diamond_chestplate:937183152668041256>Wardrobe value - {shorten_num(int(dat["types"]["wardrobe"]["total"]))}',
                value=its,
                inline=False)
        # pets value
        if pt:
            its = ""
            ind = 0
            for item in pets:

                add = item["name"]
                add += f" → {shorten_num(item['price'])} \n"
                its += add
                ind += 1
                if ind == 5:
                    break
            datab.add_field(
                name=
                f'''<:megalodon_pet:937184988615573574>Pet's value - {shorten_num(int(dat["types"]["pets"]["total"]))}''',
                value=its,
                inline=False)
        # talismans value
        if tl:
            its = ""
            ind = 0
            for item in talis:

                add = item["name"]
                if "recomb" in item.keys():
                    add += " <:recombobulator:937126148196958329>"
                add += f" → {shorten_num(item['price'])} \n"
                its += add
                ind += 1
                if ind == 5:
                    break
            datab.add_field(
                name=
                f'''<:hegemony_artifact:937187094739189800>Talisman's value - {shorten_num(int(dat["types"]["accessories"]["total"]))}''',
                value=its,
                inline=False)
        d3 = date.today()
        td = d3.strftime("%m/%d/%y")
        datab.set_footer(text=f"Profile: {profile['cute_name']} • {td}")
        await loading.delete()
        await ctx.reply(embed=datab)


def setup(bot):
    bot.add_cog(Skyblock(bot))
