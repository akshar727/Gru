import requests
import nextcord as discord
from nextcord.ext import commands
from datetime import date



def shorten_num(num):
    if num < 1000:
        return num
    elif num >= 1000 and num < 999999:
        fin = f"{round(num/1000, 1)}K"
        return fin
    elif num >= 1000000 and num < 999999999:
        fin = f"{round(num/1000000, 1)}M"
        return fin
    elif num >= 1000000000 and num < 999999999999:
        fin = f"{round(num/1000000000, 1)}B"
        return fin

def get_uuid(name):
    try:
        resp = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}")
        uuid = resp.json()["id"]

        return str(uuid)

    except:
        return None



def get_name(name):
    resp = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}")
    name = resp.json()["name"]
    return str(name)


key = "d06df1bd-fe83-41c3-b9e5-9cac81b092af"




class Skyblock(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    
    @commands.command(aliases=["nw"])
    async def networth(self,ctx, name=None, profileb=None):
        if name == None:
            return await ctx.send("Please enter a name!")
        if get_uuid(name) == None:
            return await ctx.reply(f"No user found with name {name}!")
        loading = await ctx.send("<a:loading:898340114164490261>")
        true = get_name(name)
        data = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={key}&uuid={get_uuid(name)}")
        data = data.json()
        if data['success'] == False:
            await loading.delete()
            return await ctx.reply("The API key is invalid. Please Contact Elon Musk#7655 to let them know to change it.")
        if profileb == None:
            times = []
            for profile in data["profiles"]:
                save = profile["members"][get_uuid(name)]["last_save"]
                times.append(save)
            last = max(times)
            profile = None
            for profilea in data["profiles"]:
                save = profilea["members"][get_uuid(name)]["last_save"]
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
       
        try:
            sa["banking"] = profile["banking"]
        except:
            pass
            
        ac = requests.post("https://skyblock.acebot.xyz/api/networth/categories", json={"data":sa})
    
    
        global st, iv, ec, ar, war, pt, tl
        dat = ac.json()['data']
        cate = dat['categories']
        st = False
        iv = False
        ec = False
        ar = False
        war = False
        pt = False
        tl = False
        if "storage" in cate.keys():
            storage = dat['categories']["storage"]["top_items"]
            st = True
        if "inventory" in cate.keys():
            inv = dat['categories']['inventory']['top_items']
            iv = True
        if "enderchest" in cate.keys():
            echest = dat['categories']['enderchest']['top_items']
            ec = True
        if "armor" in cate.keys():
            armor = dat['categories']['armor']['top_items']
            ar = True
        if "wardrobe_inventory" in cate.keys():
            wd = dat['categories']['wardrobe_inventory']['top_items']
            war = True
        if "pets" in cate.keys():
            pets = dat['categories']['pets']['top_items']
            pt = True
        if "talismans" in cate.keys():
            talis = dat['categories']['talismans']['top_items']
            tl = True
    
        datab = discord.Embed(title=true)
        datab.set_thumbnail(url=f"https://mc-heads.net/head/{true}")
        datab.url = f"https://sky.shiiyu.moe/stats/{true}"
        datab.color = 14298655
        datab.description = f"{true}'s networth is **${'{:,}'.format(dat['networth'])} ({shorten_num(int(dat['networth']))})**"
        datab.add_field(name="<:piggy_bank:937069548195180555>Purse", value=shorten_num(int(dat['purse'])))
        if dat['bank'] == None:
            datab.add_field(name="<:gold_ingot:937069660757700688>Bank", value="<Private>")   
        else:
            datab.add_field(name="<:gold_ingot:937069660757700688>Bank", value=shorten_num(int(dat['bank'])))
        datab.add_field(name="<:gemstone_sack:937069769327276032>Sacks's Value", value=shorten_num(int(dat['sacks'])))
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
    
            datab.add_field(name=f'<:storage:937118891438649404>Storage value - {shorten_num(int(dat["categories"]["storage"]["total"]))}', value=its, inline=False)
        
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
            datab.add_field(name=f'<:plasma_flux:937135595250139146>Inventory value - {shorten_num(int(dat["categories"]["inventory"]["total"]))}', value=its, inline=False)
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
            datab.add_field(name=f'<:ender_chest:937146821590020177>Enderchest value - {shorten_num(int(dat["categories"]["enderchest"]["total"]))}', value=its, inline=False)
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
            datab.add_field(name=f'<:superior_helmet:937147110053273722>Armor value - {shorten_num(int(dat["categories"]["armor"]["total"]))}', value=its, inline=False)
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
            datab.add_field(name=f'<:diamond_chestplate:937183152668041256>Wardrobe value - {shorten_num(int(dat["categories"]["wardrobe_inventory"]["total"]))}', value=its, inline=False)
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
            datab.add_field(name=f'''<:megalodon_pet:937184988615573574>Pet's value - {shorten_num(int(dat["categories"]["pets"]["total"]))}''', value=its, inline=False)
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
            datab.add_field(name=f'''<:hegemony_artifact:937187094739189800>Talisman's value - {shorten_num(int(dat["categories"]["talismans"]["total"]))}''', value=its, inline=False)
        d3 = date.today()
        td = d3.strftime("%m/%d/%y")
        datab.set_footer(text=f"Profile: {profile['cute_name']} • {td}")
        await loading.delete()
        await ctx.reply(embed=datab)


def setup(bot):
    bot.add_cog(Skyblock(bot))
        