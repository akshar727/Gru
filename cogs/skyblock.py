import os
from .utils import http, config
import nextcord as discord
from nextcord.ext import commands
from datetime import date
from nextcord import Interaction, SlashOption,ChannelType
from nextcord.abc import GuildChannel



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


async def get_uuid(name):
    try:
        resp = await http.get(
            f"https://api.mojang.com/users/profiles/minecraft/{name}",res_method="json")
        uuid = resp["id"]

        return str(uuid)
    except KeyError:
        return None


async def get_name(name):
    resp = await http.get(
        f"https://api.mojang.com/users/profiles/minecraft/{name}",res_method="json")
    name = resp["name"]
    return str(name)


key = config.getenv("hypixel_api_key")


class Skyblock(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @discord.slash_command(name="networth",description="Gets the networth of a player in Hypixel Skyblock")
    async def networth(self, interaction: Interaction, name: str = discord.SlashOption(description="The player's username",required=True), profile: str = discord.SlashOption(description="Which profile to get data from.",required=False)):
        if get_uuid(name) == None:
            return await interaction.response.send_message(content=f"No user found with name {name}!")
        await interaction.response.send_message("<a:loading:898340114164490261>")
        true = get_name(name)
        data = await http.get(f"https://api.hypixel.net/skyblock/profiles?key={key}&uuid={get_uuid(name)}",res_method="json")
        if data['success'] == False:
            return await interaction.edit_original_message(
                content="The Hypixel API key is invalid. Please Contact Elon Musk#7655 to let them know to change it."
            )
        if profile == None:
            times = []
            for prof in data["profiles"]:
                save = prof["last_save"]
                times.append(save)
            last = max(times)
            profi = None
            for profilea in data["profiles"]:
                save = profilea["last_save"]
                if save == last:
                    profi = profilea
                    break
        else:
            profi = None
            for profilea in data["profiles"]:
                if profilea["cute_name"].lower() == profile.lower():
                    profi = profilea
                    break

        sa = profi["members"][get_uuid(name)]
        banking = ...
        try:
            banking = profi["banking"]["balance"]
        except KeyError:
            banking = None
        ac = await http.post(config.getenv("skyhelper_api_url"),json={"profileData": sa,"bankBalance":banking},res_method="json")
        

        try:
            dat = ac.json()['data']
        except KeyError:
            return await interaction.edit_original_message(content="The api is loading, please try again shortly!")
        categories = dat['types']
        storage = categories['storage']['items'][0:5]
        inv = categories['inventory']['items'][0:5]
        echest = categories['enderchest']['items'][0:5]
        armor = categories['armor']['items'][0:5]
        wd = categories['wardrobe']['items'][0:5]
        pets = categories['pets']['items'][0:5]
        talis = categories['accessories']['items'][0:5]
        equipments = categories['equipment']['items']

        datab = discord.Embed(title=f"Stats for {true} on {profi['cute_name']}")
        datab.set_thumbnail(url=f"https://mc-heads.net/head/{true}")
        datab.url = f"https://sky.shiiyu.moe/stats/{true}/{profi['cute_name']}"
        datab.color = 14298655
        datab.description = f"{true}'s networth is **${'{:,}'.format(round(dat['networth']))} ({shorten_num(int(dat['networth']))})**"
        datab.add_field(name="<:piggy_bank:937069548195180555>Purse",
                        value=shorten_num(int(dat['purse'])))
        if dat['bank'] == None:
            datab.add_field(name="<:gold_ingot:1041081773519540244>Bank",
                            value="Private")
        else:
            datab.add_field(name="<:gold_ingot:1041081773519540244>Bank",
                            value=shorten_num(int(dat['bank'])))
        datab.add_field(
            name="<:gemstone_sack:937069769327276032>Sacks",
            value=shorten_num(int(dat['types']['sacks']['total'])))
        #storage value
        its = ""
        ind = 0
        for item in storage:
            add = item["name"]
            for calc in item["calculation"]:
                if calc["id"] == "RECOMBOBULATOR_3000":
                    add += " <:recombobulator:937126148196958329>"
            add += f" → **{shorten_num(item['price'])}** \n"
            its += add
            ind += 1
            if ind == 5:
                break
        if (len(storage)) == 0:
            its = "No items"

        datab.add_field(
            name=
            f'<:storage:937118891438649404>Storage - **{shorten_num(int(dat["types"]["storage"]["total"]))}**',
            value=its,
            inline=False)


    #equipment value
        its = ""
        for item in equipments:
            add = item["name"]
            for calc in item["calculation"]:
                if calc["id"] == "RECOMBOBULATOR_3000":
                    add += " <:recombobulator:937126148196958329>"
            add += f" → **{shorten_num(item['price'])}** \n"
            its += add
        
        if (len(equipments)) == 0:
            its = "No items"

        datab.add_field(
            name=
            f'<:black_belt:1041091054310522891>Equipment - **{shorten_num(int(dat["types"]["equipment"]["total"]))}**',
            value=its,
            inline=False)

    # inventory value
        its = ""
        ind = 0
        for item in inv:
            add = item["name"]
            for calc in item["calculation"]:
                if calc["id"] == "RECOMBOBULATOR_3000":
                    add += " <:recombobulator:937126148196958329>"
            add += f" → **{shorten_num(item['price'])}** \n"
            its += add
            ind += 1
            if ind == 5:
                break
        if (len(inv)) == 0:
            its = "No items"
        datab.add_field(
            name=
            f'<:hyperion:1041084701944852593>Inventory - **{shorten_num(int(dat["types"]["inventory"]["total"]))}**',
            value=its,
            inline=False)
    # echest value
        its = ""
        ind = 0
        for item in echest:
            add = item["name"]
            for calc in item["calculation"]:
                if calc["id"] == "RECOMBOBULATOR_3000":
                    add += " <:recombobulator:937126148196958329>"
            add += f" → **{shorten_num(item['price'])}** \n"
            its += add
            ind += 1
            if ind == 5:
                break
        if (len(echest)) == 0:
            its = "No items"
        datab.add_field(
            name=
            f'<:ender_chest:937146821590020177>Enderchest - **{shorten_num(int(dat["types"]["enderchest"]["total"]))}**',
            value=its,
            inline=False)
    # armor value
        its = ""
        ind = 0
        for item in armor:

            add = item["name"]
            for calc in item["calculation"]:
                if calc["id"] == "RECOMBOBULATOR_3000":
                    add += " <:recombobulator:937126148196958329>"
            add += f" → **{shorten_num(item['price'])}** \n"
            its += add
            ind += 1
            if ind == 5:
                break
        if (len(armor)) == 0:
            its = "No items"
        datab.add_field(
            name=
            f'<:crimson_helmet:1041089378895802388>Armor - **{shorten_num(int(dat["types"]["armor"]["total"]))}**',
            value=its,
            inline=False)
    # wardrobe value
        its = ""
        ind = 0
        for item in wd:

            add = item["name"]
            for calc in item["calculation"]:
                if calc["id"] == "RECOMBOBULATOR_3000":
                    add += " <:recombobulator:937126148196958329>"
            add += f" → **{shorten_num(item['price'])}** \n"
            its += add
            ind += 1
            if ind == 5:
                break
        if (len(wd)) == 0:
            its = "No items"
        datab.add_field(
            name=
            f'<:crimson_chestplate:1041089513021255812>Wardrobe - **{shorten_num(int(dat["types"]["wardrobe"]["total"]))}**',
            value=its,
            inline=False)
    # pets value
        its = ""
        ind = 0
        for item in pets:

            add = item["name"]
            add += f" → **{shorten_num(item['price'])}** \n"
            its += add
            ind += 1
            if ind == 5:
                break
        if (len(pets)) == 0:
            its = "No items"
        datab.add_field(
            name=
            f'''<:golden_dragon:1041089609918074964>Pets - **{shorten_num(int(dat["types"]["pets"]["total"]))}**''',
            value=its,
            inline=False)
    # talismans value
        its = ""
        ind = 0
        for item in talis:

            add = item["name"]
            for calc in item["calculation"]:
                if calc["id"] == "RECOMBOBULATOR_3000":
                    add += " <:recombobulator:937126148196958329>"
            add += f" → **{shorten_num(item['price'])}** \n"
            its += add
            ind += 1
            if ind == 5:
                break
        if (len(talis)) == 0:
            its = "No items"
        datab.add_field(
            name=
            f'''<:master_skull_tier_7:1041089865414094948>Accessories - **{shorten_num(int(dat["types"]["accessories"]["total"]))}**''',
            value=its,
            inline=False)
        d3 = date.today()
        td = d3.strftime("%m/%d/%y")
        datab.set_footer(text=f"Profile: {profi['cute_name']} • {td}")
        await interaction.edit_original_message(embed=datab,content="")


def setup(bot):
    bot.add_cog(Skyblock(bot))
