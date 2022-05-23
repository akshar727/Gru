import re
import itertools
import math
import aiohttp
from backports.zoneinfo import ZoneInfo
import nextcord as discord
from nextcord.ext import commands, tasks
from nextcord.utils import get
import asyncio
from typing import Optional
from webserver import keep_alive
import datetime
from itertools import cycle
import os
import json
import random
from PIL import Image
from io import BytesIO
from googleapiclient.discovery import build
import urllib.parse, urllib.request
from num2words import num2words
from cogs.utils import http
import psutil
from easy_pil import Editor, Font, Canvas, load_image_async



api_key = "AIzaSyAhNZnU6pStK8eYcm83IeQAR_OEdhjJURw"

def get_prefix(client, message):
    with open("databases/prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

class GruBot(commands.Bot):
     async def is_owner(self, user: discord.User):
        if user.id == 717512097725939795:
            return True
        else:
            return False



client = GruBot(command_prefix=get_prefix, intents=discord.Intents.all(), case_insensitive=True)
client.remove_command("help")




@client.event
async def on_guild_join(guild):
    with open("databases/prefixes.json", "r") as f:
        prefixes = json.load(f)
    with open("databases/server_configs.json",'r') as f:
        configs = json.load(f)

    configs[str(guild.id)] = {}
    configs[str(guild.id)]["giveaway_role"] = "None"
    configs[str(guild.id)]["levels"] = False
    prefixes[str(guild.id)] = ','

    with open('databases/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    with open("databases/server_configs.json",'w') as f:
        json.dump(configs, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open("databases/prefixes.json", "r") as f:
        prefixes = json.load(f)
    with open("databases/server_configs.json",'r') as f:
        configs = json.load(f)
    del prefixes[str(guild.id)]
    with open('databases/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    with open('databases/levels.json', 'r') as f:
        levels = json.load(f)
    del levels[str(guild.id)]
    with open('databases/levels.json', 'w') as f:
        json.dump(levels, f, indent=4)
    del configs[str(guild.id)]
    with open("databases/server_configs.json",'w') as f:
        json.dump(configs, f, indent=4)



@client.command()
async def avatar(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author

    member_display_avatar_pic = member.display_avatar

    await ctx.send(member_display_avatar_pic)
    if member == client.user:
        await ctx.send("HEEEY THAT'S ME. I'M FAMOUS POOOOGGGGGG")


@client.command()
async def prefix(ctx, prefix=None):
    if ctx.author.id != ctx.guild.owner_id:
        return await ctx.send("Sorry, but only the owner of this server can change the prefix!")
    if prefix == None:
        await ctx.send("Please enter the new prefix.")
        return

    with open('databases/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('databases/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f"The prefix was changed to `{prefix}`")


status = cycle(
    ['Try ,help', 'Prefix - ,', 'Minecraft 1.19: The Wild Update', 'PoKeMon', 'Try @Gru', 'Bill Nye the Science Guy', 'Dank Memer', 'RTX 3090 ti','Warzone: Season 6', 'Minecraft 1.18: Caves and Cliffs', 'Call of Duty: Vanguard', 'Destiny 2: The Witch Queen', 'Battlefield 2042', "Tom Clancy's: Rainbow Six Extraction", 'Halo Infinite', 'Splitgate', 'Perfect Dark', 'Hitman', 'GTA 6', 'amogus', 'CS:GO', 'Team Fortress 2', 'Mortal Kombat', 'Injustice 3', 'Arkham Knight', 'Gotham Knights', 'Suicide Squad: Kill the Justice Leauge', 'Spiderman 2 PS5', 'Spiderman PS4', 'Spiderman: Miles Morales', 'Hogwarts Legacy', 'God of War: Ragnorak', 'Forza Horizon 5', 'Forza Motorsport 5', 'Far Cry 6', 'Jurassic World Evolution 2', "Marvel's Guardians of the Galaxy", "Marvel's Avengers", 'Dying Light 2', 'Back 4 Blood', 'Clash of Clans', 'Clash Royale', 'Xbox One', 'Xbox One S', 'Xbox One X', 'Xbox Series X', 'Xbox Series S', 'PS4', 'PS4 Pro', 'PS4 Slim', 'PS5', 'NextCord', 'Nintendo Switch', 'Nintendo Switch Lite', 'Wii U', 'Nintendo DS', 'Xbox 360', 'PS3', 'Da Computer','Pac-Man', 'Super Smash Bros Ultimate', 'Super Mario', 'Sonic the Hedgehog', 'Pong', 'Legend of Zelda: Breath of the Wild', 'Battlefront 3', 'Jedi Fallen Order 2', 'Mario Kart', 'Fallout', 'Elder Scrolls 6', 'Starfield', 'Star Citizen', 'Planetside 3', 'Fortnite Chapter 3', 'Demon Souls...', 'Cyberpunk 2069', 'Wolverine', 'Uncharted 5', 'FIFA', 'MADDEN', 'NHL', 'UFC', 'Lego Star Wars: The Skywalker Saga', 'Star Wars: Knights of the Old Republic Remake', 'Dead Space 4', 'Project 007', 'Dark Pictures Anthology', 'Riders Republic', 'Assasins Creed Infinity', 'The Last of Us: Part 3', 'Red Dead Redemption 3', 'Agent', 'Bully 2', 'Portal', 'Elden Ring', 'Borderlands 4', 'Deathloop', 'Redfall', 'Crash Bandicoot 5', 'Destiny 2: Lightfall', 'Destiny 3', 'Stalker 2', 'Bugsnax', 'Diablo', 'ARK', 'Overcooked', 'Gears 6', 'Animal Crossing: New Horizons', 'Metroid Dread', 'Street Fighter', 'Roblox', 'Tetris', 'Horizon Zero Dawn', 'Horizon Forbidden West', 'Horizon Zero Dawn', 'Terraria', 'Bioshock', 'Wicher 4', 'Resident Evil'])



@client.event
async def on_ready():
    change_status.start()
    uptimeCounter.start()
    print()
    print("Connected to {0.user}".format(client))
    client.load_extension("jishaku")


@tasks.loop(seconds=4)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


ts = 0
tm = 0
th = 0
td = 0

@tasks.loop(seconds=2.0)
async def uptimeCounter():

    global ts, tm, th, td
    ts += 2
    if ts == 60:
        ts = 0
        tm += 1
        if tm == 60:
            tm = 0
            th += 1
            if th == 24:
                th = 0
                td += 1

@uptimeCounter.before_loop
async def beforeUptimeCounter():
    await client.wait_until_ready()





@client.event
async def on_member_join(member):
    if not member.bot:
        try:
            await member.send(f'''Hi {member.name}, welcome to {member.guild.name}!''')
        except:
            print(f"Cannot send messages to {member}")

####################################################################
####################################################################
# Main code starts :)

mainshop = [{"name": "Watch", "price": 100, "description": "Time"},
            {"name": "Gaming chair", "price": 100, "description": "Comfort"},
            {"name": "Gaming desk", "price": 500, "description": "Comfort v2"},
            {"name": "Laptop", "price": 1000, "description": "Work"},
            {"name": "Iphone 13", "price": 2000, "description": "STYLE"},
            {"name": "Monitor", "price": 1000, "description": "Work"},
            {"name": "PC", "price": 10000, "description": "Gaming"},
            {"name": "MacBook Pro 13", "price": 15000, "description": "SUPER STYLE"},
            {"name": "Fishing Rod", "price":25000,"description":"Allows you to fish and catch sea animals!"},
            {"name": "Hunting Sniper", "price":27000,"description":"Allows you to hunt and catch land and aerial animals!"},
            {"name": "2x booster", "price": 50000, "description": "Get a 2x money booster **__Permanent__**"},
            {"name": "Ferrari", "price": 99999, "description": "Sports Car"},
            {"name": "5x booster", "price": 400000, "description": "Get a 5x money booster **__Permanent__**"},
            {"name": "Quantum computer", "price": 470000, "description": "ULTRA FAST COMPUTER"},
            {"name": "Gru trusts me role", "price": 500000,"description": "Allows you to see a exclusive channel for users with this role only!"},
            {"name": "Lamborghini", "price": 1000000, "description": "Ultra cool sports car"},
            {"name": "10x booster","price":3500000,"description":"Get a 10x money booster **__Permanent__**"}
            ]

animal_shop = [

    [
        {"name":"Wolf","sell_price": 2000},
        {"name":"Mountain Lion","sell_price":3200},
        {"name":"Chicken","sell_price": 3500},
        {"name":"Rabbit","sell_price":3700},
        {"name":"Deer","sell_price":4200},
        {"name":"Moose","sell_price":4900},
        {"name":"Angry Bird", "sell_price":8500},
        {"name":"Minion","sell_price":15000},
        {"name":"Bengal Tiger","sell_price":32000},
        {"name":"Evil Minion","sell_price":50000},
        {"name":"White Tiger","sell_price":65000},
        {"name":"Unicorn","sell_price":85000}
    ],

    
    [
        {"name":"Duck","sell_price":6000},
        {"name":"Mosasaurus","sell_price":500000},
        {"name":"Fish","sell_price":3400},
        {"name":"Nemo","sell_price":3600},
        {"name":"Great White Shark","sell_price":75000},
        {"name":"Blobfish","sell_price":10000},
        {"name":"Crab","sell_price":1500},
        {"name":"Shell","sell_price":250},
        {"name":"Garbage","sell_price":100},
        {"name":"Water Bottle","sell_price":3000},
        {"name":"Dumbo Octopus","sell_price": 35000}, 
        {"name":"Donald Duck","sell_price":3500}
        

    ],
    

    [  
      {"name":"Hawk","sell_price":5000},
      {"name":"Bat","sell_price":15000},
      {"name":"Mosquito","sell_price":1000},
      {"name":"Flying Lizard","sell_price":7000},
      {"name":"Bird","sell_price":2000},
      {"name":"Ladybug","sell_price":1500},
      {"name":"Bumblebee","sell_price":9500},
      {"name":"Hummingbird","sell_price":13500},
      {"name":"Eagle","sell_price":15000},
      {"name":"Pigeon","sell_price":5000},
      {"name":"Vulture","sell_price":17500},
      {"name":"Hummingbird","sell_price":13500},
      {"name":"Pterodactyl","sell_price":102000}
    ]
               ]




@client.command()
async def stats(ctx):
    global ts, tm, th, td
    e = discord.Embed(title="My Stats!",color=discord.Color.random())
    e.add_field(name="Days:",value=td,inline=True)
    e.add_field(name="Hours:",value=th,inline=True)
    e.add_field(name="Minutes:",value=tm,inline=True)
    e.add_field(name="Seconds:",value=ts,inline=True)
    e.add_field(name="CPU:",value=f"{psutil.cpu_percent()}%",inline=False)
    e.add_field(name="RAM:",value=f"{psutil.virtual_memory()[2]}%",inline=True)
    await ctx.reply(embed=e)
    
@client.command(aliases=['bal'])
async def balance(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    await open_account(ctx.author)
    await open_account(user)


    users = await get_bank_data()
    jobs = await get_job_data()
    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]
    booster_amt = users[str(user.id)]["booster"]
    job_name = jobs[str(user.id)]["job"]["name"]
    job_pay = jobs[str(user.id)]["job"]["pay"]
    
    em = discord.Embed(title=f"{user.display_name}'s Balance", color=discord.Color.green())
    if wallet_amt + bank_amt >= 1000000000000000:
        em.add_field(name="Wallet Balance", value=f"{float(wallet_amt)} Minions™")
        em.add_field(name='Bank Balance', value=f"{float(bank_amt)} Minions™")
        em.add_field(name='Job', value=job_name)
        em.add_field(name='Job salary', value=f"{float(job_pay)} Minions™ per hour")
        if booster_amt != 1:
            em.add_field(name='Booster', value=f'{float(booster_amt)}x')
    else:
        em.add_field(name="Wallet Balance", value=f"{int(wallet_amt)} Minions™")
        em.add_field(name='Bank Balance', value=f"{int(bank_amt)} Minions™")
        em.add_field(name='Job', value=job_name)
        em.add_field(name='Job salary', value=f"{int(job_pay)} Minions™ per hour")
        if booster_amt != 1:
            em.add_field(name='Booster', value=f'{int(booster_amt)}x')
    await ctx.send(embed=em)


@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    booster = users[str(user.id)]["booster"]

    earnings = random.randrange(1000)

    people = ["Elon Musk", "Jeff Bezos", "Mr Krabs", "Your mom", "Kylie Jenners", "Albert Einstein", "Mr Mosby",
              "Greg Heffley", "I the all mighty Gru Bot", "Rihanna"]

    person = random.choice(people)
    nums = [0, 1]
    trybeg = random.choice(nums)

    if trybeg == 0:
        message = f'"Oh you beggar take `{earnings * booster} Minions™`"'
        beg_embed = discord.Embed(description=message, color=discord.Color.random())
        beg_embed.set_author(name=person)
        if booster != 1:
            beg_embed.set_footer(
                text=f"You earned {earnings * (booster - 1)} extra Minions™ since you had a {booster}x booster!(Original amount:{earnings})")
        await ctx.reply(embed=beg_embed)
        users[str(user.id)]["wallet"] += earnings * booster

    else:
        message = 'no'
        beg_embed = discord.Embed(description=message, color=discord.Color.random())
        beg_embed.set_author(name=person)
        beg_embed.set_footer(text="imagine begging LOL")
        await ctx.reply(embed=beg_embed)

    with open("databases/mainbank.json", 'w') as f:
        json.dump(users, f, indent=4)


@client.event
async def on_command_error(ctx, error):
    modlog = client.get_channel(881208942104047649)
    # if isinstance(error, commands.CommandInvokeError):
    #     error = error.original
    if isinstance(error, commands.CommandNotFound):
        with open('databases/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.guild.id)]
        await ctx.send(f"Unknown command.Try {prefix}help for a list of commands")
        return
    elif isinstance(error, commands.CommandOnCooldown):
        if error.retry_after <= 60:
            em = discord.Embed(title=f"Slow it down bro!",
                               description="**Still on cooldown**, please try again in {:.2f}s".format(
                                   error.retry_after), color=discord.Color.green())
            await ctx.send(ctx.author.mention, embed=em)
        else:
            mins = int(error.retry_after // 60)
            secs = int(error.retry_after - (mins * 60))
            em = discord.Embed(title=f"Slow it down bro!",
                               description="**Still on cooldown**, please try again in {}m{}s".format(mins, secs),
                               color=discord.Color.green())
            await ctx.send(ctx.author.mention, embed=em)
        return
    elif isinstance(error, commands.RoleNotFound):
        await ctx.send(":x: Role not found.")
        return
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send(":x: No member found with that name.")
        return
    elif isinstance(error, commands.NotOwner):
        await ctx.send(":x: You are not allowed to do this! Only the owner of the bot can do this.")
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            ":x: Missing arguments! check ,help if you need to know about how to use the command.")
        client.get_command(ctx.invoked_with).reset_cooldown(ctx)
        return
    elif isinstance(error, commands.MissingPermissions):
        return await ctx.send("You do not have permission to do this!")
    elif isinstance(error, discord.Forbidden):
        return await ctx.send("I do not have permission to do this!")
    elif isinstance(error, commands.CommandError):
        await modlog.send(f"Error found: {error}")
        with open('databases/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.guild.id)]
        return await ctx.send(f"An error has occurred with the command! :(.Please check `{prefix}help` to make sure you are using the command correctly.")
    


facts = ["Gru likes his cup more than anything", "Gru will never get a wife", "Gru has 2000IQ", "Gru does not like kids",
         "Gru only refuels his ship once a week", "Gru's favorite minion is Bert","Minions have lots of IQ because they work all day"]

jobpays = {"Gru Gadgets Maker": 9000, "Gru Gadgets Tester": 12000, "Minion Refiner": 16000,
                           "Super Minion Refiner": 22000, "Minion Gadget Manager": 29000, "Gru Ship Mechanic": 35000,
                           "Gru Ship Pilot": 41000, "Minion Costume Maker": 45000, "Gru Assistant Hacker": 55000,
                           "Gru Hacker": 60000, "Gru Senior Hacker": 67000, "Gru's Barber": 69420,
                           "Gru Gadget Programmer": 79000, "Gru Code Compiler": 90000, "Gru Super Programmer": 102000,
                           "Gru Super Code Compiler": 117000,"Gru Enterprises™ Supervisor":137000,"Gru Enterprises™ Manager":155000,"Gru Enterprises™ CO":225000,"Gru Enterprises™ CEO":319000,"Gru Enterprises™ Super CEO":428000,"Gru Enterprises™ Owner":700000,"Gru™":1600000,"Groogle Programmer":3500000,"Gru Movie Director":3600000,"Groogle Owner":4300000,"Groogle Creator":6900000,"Groogle Custom Computer Language Programmer":10300000}

@client.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
async def work(ctx):
    with open('databases/prefixes.json') as f:
        prefixes = json.load(f)
    prefix = prefixes[str(ctx.guild.id)]
    await open_account(ctx.author)
    jobs = await get_job_data()
    user = ctx.author
    work_amt = jobs[str(user.id)]["job"]["pay"]
    work_name = jobs[str(user.id)]["job"]["name"]

    if work_name == 'None':
        await ctx.send(f"You don't have a job! Get one by doing `{prefix}get_job` !!")
        work.reset_cooldown(ctx)
        return

    def check(m):
        return m.channel == ctx.channel and m.author == ctx.author

    typeofwork = "memory"
    if typeofwork == 'memory':
        await ctx.reply(
            f'''**Working as a {work_name}** - Memory Game - A fact about  Gru things™  will come up on the screen! then it will disappear after a few seconds. Your job is to rewrite the fact!''')
        fact = random.choice(facts) + "\u200B"

        fact_sended = await ctx.send(f'**{fact}**')
        await asyncio.sleep(4)
        await fact_sended.delete()
        await asyncio.sleep(0.5)
        await ctx.send("Now, retype the sentence!")
        msg = None
        try:
            msg = await client.wait_for('message', check=check, timeout=20)
        except asyncio.TimeoutError:
            work_em = discord.Embed(title="Terrible job!",
                                    description=f"You were given `{int(work_amt / 3):,} Minions™` for 1/3 of an hour of pay",
                                    color=discord.Color.random())
            work_em.set_footer(text=f'Working as a {work_name}')
            await update_bank(ctx.author, int(work_amt / 3))
            await ctx.reply(embed=work_em)
            return
        if msg.content.lower() == fact.lower()[:-1]:
            promote_pay = random.randint(0, 8)
            promote_job = random.randint(0, 8)
            get_crate = random.randint(0,5)
            


            work_em = discord.Embed(title="Great job!",
                                    description=f"You were given `{work_amt:,} Minions™` for an hour of pay",
                                    color=discord.Color.random())
            work_em.set_footer(text=f'Working as a {work_name}')
            await update_bank(ctx.author, work_amt)
            await ctx.reply(embed=work_em)
            if get_crate == 5:
                with open('databases/lootboxes.json','r') as f:
                    lootboxes = json.load(f)
                crate_type = random.choice(["mythic","legendary","legendary","epic","epic","epic","epic","rare","rare","rare","rare","rare","rare","rare","uncommon","uncommon","uncommon","uncommon","uncommon","uncommon","uncommon","uncommon","uncommon","common","common","common","common","common","common","common","common","common","common"])
                await ctx.send(f"Your boss saw that you were doing so well, he gave you a **{crate_type.capitalize()}** <:chest:898333946557894716> lootbox!! :tada:")
                lootboxes[str(ctx.author.id)][crate_type] += 1
                with open('databases/lootboxes.json','w') as f:
                    json.dump(lootboxes, f, indent=4)

            if promote_job == 8 and work_name != "God Of Money" and work_name != "Groogle Custom Computer Language Programmer":
                new_job_name = ""
                if work_name == "Gru Gadgets Maker":
                    new_job_name = "Gru Gadgets Tester"
                elif work_name == "Gru Gadgets Tester":
                    new_job_name = "Minion Refiner"
                elif work_name == "Minion Refiner":
                    new_job_name = "Super Minion Refiner"
                elif work_name == "Super Minion Refiner":
                    new_job_name = "Minion Gadget Manager"
                elif work_name == "Minion Gadget Manager":
                    new_job_name = "Gru Ship Mechanic"
                elif work_name == "Gru Ship Mechanic":
                    new_job_name = "Gru Ship Pilot"
                elif work_name == "Gru Ship Pilot":
                    new_job_name = "Minion Costume Maker"
                elif work_name == "Minion Costume Maker":
                    new_job_name = "Gru Assistant Hacker"
                elif work_name == "Gru Assistant Hacker":
                    new_job_name = "Gru Hacker"
                elif work_name == "Gru Hacker":
                    new_job_name = "Gru Senior Hacker"
                elif work_name == "Gru Senior Hacker":
                    new_job_name = "Gru's Barber"
                elif work_name == "Gru's Barber":
                    new_job_name = "Gru Gadget Programmer"
                elif work_name == "Gru Gadget Programmer":
                    new_job_name = "Gru Code Compiler"
                elif work_name == "Gru Code Compiler":
                    new_job_name = "Gru Super Programmer"
                elif work_name == "Gru Super Programmer":
                    new_job_name = "Gru Super Code Compiler"
                elif work_name == "Gru Super Code Compiler":
                    new_job_name ="Gru Enterprises™ Supervisor"
                elif work_name == "Gru Enterprises™ Supervisor":
                    new_job_name = "Gru Enterprises™ Manager"
                elif work_name == "Gru Enterprises™ Manager":
                    new_job_name = "Gru Enterprises™ CO"
                elif work_name == "Gru Enterprises™ CO":
                    new_job_name = "Gru Enterprises™ CEO"
                elif work_name == "Gru Enterprises™ CEO":
                    new_job_name = "Gru Enterprises™ Super CEO"
                elif work_name == "Gru Enterprises™ Super CEO":
                    new_job_name = "Gru Enterprises™ Owner"
                elif work_name == "Gru Enterprises™ Owner":
                    new_job_name = "Gru™"
                elif work_name == "Gru™":
                    new_job_name = "Groogle Programmer"
                elif work_name == "Groogle Programmer":
                    new_job_name = "Gru Movie Director"
                elif work_name == "Gru Movie Director":
                    new_job_name = "Groogle Owner"
                elif work_name == "Groogle Owner":
                    new_job_name = "Groogle Creator"
                elif work_name == "Groogle Creator":
                    new_job_name = "Groogle Custom Computer Language Preogrammer"

                
                new_job_pay = jobpays[new_job_name]
                if work_amt > jobpays[work_name]:
                    new_job_pay += work_amt - jobpays[work_name]
                await ctx.send(f"You were doing so good that your manager has **PROMOTED** you to a {new_job_name}! You now make `{new_job_pay} Minions™` instead of `{work_amt} Minions™`! :tada: :tada:")
                if work_amt > jobpays[work_name]:
                    await ctx.send(
                        "Your base pay for this new job is higher because you got pay increases in your last job(s)!")
                jobs[str(user.id)]["job"]["pay"] = new_job_pay
                jobs[str(user.id)]["job"]["name"] = new_job_name
                with open('databases/jobs.json', 'w') as f:
                    json.dump(jobs, f, indent=4)
                return
            if promote_pay == 8:
                pay_increase1 = str(random.randrange(1, 7))
                pay_increase = pay_increase1 + "000"
                await ctx.reply(
                    f"Since you are doing really well in your work, your manager has decided to increase your pay by `{int(pay_increase):,} Minions™`!! :tada: :tada:")
                jobs[str(user.id)]["job"]["pay"] = work_amt + int(pay_increase)
                with open('databases/jobs.json', 'w') as f:
                    json.dump(jobs, f, indent=4)
            return

        if msg.content.lower() == fact.lower():
            return await ctx.send("I know you copy-pasted it!")
        else:
            work_em = discord.Embed(title="Terrible job!", description=f"You were given `{int(work_amt / 3)} Minions™` for 1/3 of an hour of pay", color=discord.Color.random())
            work_em.set_footer(text=f'Working as a {work_name.capitalize()}')
            await ctx.reply(embed=work_em)
            await update_bank(ctx.author, int(work_amt / 3))
            return      
            

@client.command()
async def jobs(ctx):
    page1=discord.Embed(title="Jobs in Gru Enterprisies™",description="These are all the jobs available.",color=discord.Color.random())
    p2 = {"Groogle Owner":4300000,"Groogle Creator":6900000,"Groogle Custom Computer Language Programmer":10300000}
    page2 = discord.Embed(title="Jobs in Gru Enterprisies™ (Page 2)",description="These are all the jobs available. (Page 2)",color=discord.Color.random())
    pages = [page1, page2]

    page1.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
    page1.set_footer(text="Page 1/2")

    page2.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
    page2.set_footer(text="Page 2/2")
    for i in jobpays:
        page1.add_field(name=f"Job Name: {i}",value=f"Salary per hour: {jobpays[i]:,}")
    for i in p2:
        page2.add_field(name=f"Job Name: {i}",value=f"Salary per hour: {jobpays[i]:,}")

    buttons = [u"\u23F9",u"\u2B05", u"\u27A1"] #start, exit, right
    current = 0
    msg = await ctx.send(f"{ctx.author.mention}",embed=pages[current])

    for button in buttons:
        await msg.add_reaction(button)

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)
        except asyncio.TimeoutError:
            pages[current].set_footer(text="Timed out :(")
            await msg.edit(embed=pages[current])
            break
        else:
            previous_page = current

            if reaction.emoji == u"\u2B05":
                if current > 0:
                    current -= 1

            elif reaction.emoji == u"\u27A1":
                if current < len(pages) - 1:
                    current += 1
            elif reaction.emoji == u"\u23F9":
                await msg.delete()
                break


            if current != previous_page:
                await msg.edit(embed=pages[current])

            for button in buttons:
                await msg.remove_reaction(button, ctx.author)

    



resigned_users = []


@client.command()
async def get_job(ctx):
    jobs = await get_job_data()
    user = ctx.author
    name = jobs[str(user.id)]["job"]["name"]
    if str(user.id) in resigned_users:
        await ctx.send("You have resigned recently so you can't get another job yet!")
        return
    if name == 'None' and str(user.id) not in resigned_users:
        await ctx.reply("Welcome to Gru enterprises!! :tada: You are now a Gru Gadgets Maker and earn 9000 per hour!")
        jobs[str(user.id)]["job"]["name"] = "Gru Gadgets Maker"
        jobs[str(user.id)]["job"]["pay"] = 9000
        with open('databases/jobs.json', 'w') as f:
            json.dump(jobs, f, indent=4)
        return
    else:
        await ctx.send(
            "You already have a job! You can do `resign` to get out of your job(**BEWARE** resigning and then rejoining Gru enterprises will put you back at a entry level job and pay)")


@client.command()
async def resign(ctx):
    jobs = await get_job_data()
    user = ctx.author
    name = jobs[str(user.id)]["job"]["name"]
    if name == 'None':
        await ctx.send("You don't have a job! You can get one by doing 'get_job'!!")
    else:
        await ctx.send("You are now unemployed.You cannot reapply for a job for the next 2 hours")
        jobs[str(user.id)]["job"]["name"] = 'None'
        jobs[str(user.id)]["job"]["pay"] = 0
        with open('databases/jobs.json', 'w') as f:
            json.dump(jobs, f, indent=4)
        resigned_users.append(str(user.id))
        await asyncio.sleep(10800)
        resigned_users.remove(str(user.id))


@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    p = await ctx.send('Done!')
    await asyncio.sleep(2)
    await p.delete()


@client.command(aliases=["commands"])
async def commands_amt(ctx):
    await ctx.reply(f"I have {len(client.commands)} commands!")


@client.command(aliases=['with'])
async def withdraw(ctx, amount=None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter an amount!")
        return
    amount = amount.lower()

    bal = await update_bank(ctx.author)

    if amount == 'max' or amount == 'all':
        amount = bal[1]
    else:
        try:
            amount = int(amount)
        except:
            return await ctx.send("That is an invalid amount!")

    if amount > bal[1]:
        await ctx.send(f'You do not have `{amount} Minions™` in your bank!')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return
    if amount == 0:
        return await ctx.send("You do not have any Minions™ in your bank!")

    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1 * amount, 'bank')
    await ctx.send(f':white_check_mark: {ctx.author.mention} You withdrew `{amount}  Minions™`')


@client.command(aliases=['dep'])
async def deposit(ctx, amount=None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter an amount!")
        return
    amount = amount.lower()
    bal = await update_bank(ctx.author)
    if amount == 'max' or amount == 'all':
        amount = bal[0]
    else:
        try:
            amount = int(amount)
        except:
            return await ctx.send("That is an invalid amount!")

    if amount > bal[0]:
        await ctx.send(f'You do not have `{amount} Minions™` in your wallet!')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return
    if amount == 0:
        return await ctx.send("You do not have any Minions™ in your wallet!")

    await update_bank(ctx.author, -1 * amount)
    await update_bank(ctx.author, amount, 'bank')
    await ctx.send(f':white_check_mark: {ctx.author.mention} You deposited `{amount} Minions™`')


@client.command()
async def send(ctx, member: discord.Member, amount=None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("Please enter an amount!")
        return
    amount = amount.lower()
    bal = await update_bank(ctx.author)
    if amount == 'all' or amount == 'max':
        amount = bal[0]

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author, -1 * amount, 'bank')
    await update_bank(member, amount, 'bank')
    await ctx.send(f':white_check_mark: {ctx.author.mention} You gave {member} {amount} coins')


@client.command(aliases=['steal'])
@commands.cooldown(1, 60, commands.BucketType.user)
async def rob(ctx, member: discord.Member):
    if member.bot:
        return await ctx.send("You are not allowed to steal from bots, back off my kind")
    await open_account(ctx.author)
    await open_account(member)
    bal = await update_bank(member)
    if member.id == 717512097725939795:
        rob.reset_cooldown(ctx)
        return await ctx.send("xD you can't rob him he is the owner of the bot!!!")

    if bal[0] < 100:
        await ctx.send('It is useless to rob him :(')
        rob.reset_cooldown(ctx)
        return
    if member == ctx.author:
        await ctx.send("Why are you trying to rob yourself?")
        rob.reset_cooldown(ctx)
        return

    earning = random.randrange(0, bal[0])

    await update_bank(ctx.author, earning)
    await update_bank(member, -1 * earning)
    await ctx.send(f':white_check_mark:{ctx.author.mention} You robbed {member} and got {earning} coins')


@client.command()
async def slots(ctx, amount=None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter an amount!")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return
    final = []
    for i in range(3):
        a = random.choice(['Q', 'O', 'X'])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] and final[1] == final[2]:
        await update_bank(ctx.author, 3 * amount)
        await ctx.send(f'JACKPOT!!! You won `{3 * amount} Minions™`!!! :tada: :D {ctx.author.mention}')

    elif final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
        await update_bank(ctx.author, 2 * amount)
        await ctx.send(f'You won `{2 * amount} Minions™` :) {ctx.author.mention}')
    else:
        await update_bank(ctx.author, -1 * amount)
        await ctx.send(f'You lose `{1 * amount} Minions™` :( {ctx.author.mention}')


@client.command(aliases=["store"])
async def shop(ctx):
    page1 = discord.Embed(title="Shop", color=discord.Color.random())

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        if name == "Gru trusts me role" and ctx.guild.id != 762829356812206090:
            pass
        else:
            page1.add_field(name=name, value=f"{int(price):,} Minions™ | {desc}")
    page1.set_footer(text="Page 1/3")

    page2 = discord.Embed(title="Animal Shop",description="These are all the animals you can find by hunting or fishing and the prices that you can sell them for.",color=discord.Color.random())
    page2.set_footer(text="Page 2/3")
    page2.add_field(name="Land Animals",value="These are all the land animals you can get by hunting.",inline=False)
    for _array in animal_shop[:-1]:
        if _array == animal_shop[1]:
            page2.add_field(name="Water Animals",value="These are all the water animals you can get by fishing.",inline=False)
        for animal in _array:
            name = animal["name"]
            sell = animal["sell_price"]
            page2.add_field(name=name,value=f"{int(sell):,} Minions™")

    page3 = discord.Embed(title="Animal Shop (Page 2)",description="These are all the animals you can find by hunting or fishing and the prices that you can sell them for.",color=discord.Color.random())
    page3.add_field(name="Water Animals (Part 2)", value="These are all the water animals you can get from fishing (Part 2)", inline=False)
    page3.set_footer(text="Page 3/3")
    for animal in animal_shop[1][-1:]:
        name = animal["name"]
        sell = animal["sell_price"]
        page3.add_field(name=name,value=f"{int(sell):,} Minions™")
    page3.add_field(name="Aerial Animals",value="These are all the aerial animals you can get by hunting.",inline=False)
    for animal in animal_shop[2]:
        name = animal["name"]
        sell = animal["sell_price"]
        page3.add_field(name=name,value=f"{int(sell):,} Minions™")

    pages = [page1, page2, page3]

    buttons = [u"\u23F9","\u23EA",u"\u2B05", u"\u27A1","\u23E9"] #start, exit, right
    current = 0
    msg = await ctx.send(embed=pages[current])

    for button in buttons:
        await msg.add_reaction(button)

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)
        except asyncio.TimeoutError:
            pages[current].set_footer(text="Timed out :(")
            await msg.edit(embed=pages[current])
            break
        else:
            previous_page = current

            if reaction.emoji == u"\u2B05":
                if current > 0:
                    current -= 1

            elif reaction.emoji == u"\u27A1":
                if current < len(pages) - 1:
                    current += 1
            elif reaction.emoji == u"\u23F9":
                await msg.delete()
                break
            elif reaction.emoji == "\u23E9":
                current = len(pages)-1
            elif reaction.emoji == "\u23EA":
                current=0

            if current != previous_page:
                await msg.edit(embed=pages[current])

            for button in buttons:
                await msg.remove_reaction(button, ctx.author)




@client.command()
async def buy(ctx, amount: Optional[int]=1, *, item):
    users = await get_bank_data()
    item = item.lower()
    if item == "2x booster":
        users = await get_bank_data()
        if users[str(ctx.author.id)]["booster"] < 2:
            if users[str(ctx.author.id)]["wallet"] >= 50000:
                users[str(ctx.author.id)]["wallet"] -= 50000
                users[str(ctx.author.id)]["booster"] = 2
                await ctx.send(":white_check_mark: You now have a booster for 2x the money!")
                with open('databases/mainbank.json', 'w') as f:
                    json.dump(users, f)
                return
            else:
                await ctx.send("You can't afford this!")
                return
        else:
            await ctx.send(":x: You already have a booster that's higher than this!")
            return
    if item == "5x booster":
        users = await get_bank_data()
        if users[str(ctx.author.id)]["booster"] < 5:
            if users[str(ctx.author.id)]["wallet"] >= 400000:
                users[str(ctx.author.id)]["wallet"] -= 400000
                users[str(ctx.author.id)]["booster"] = 5
                await ctx.send(":white_check_mark: You now have a booster for 5x the money!")
                with open('databases/mainbank.json', 'w') as f:
                    json.dump(users, f,indent=4)
                return
            else:
                await ctx.send("You can't afford this!")
                return
        else:
            await ctx.send(":x: You already have a booster that's higher than this!")
            return
    if item == "10x booster":
        users = await get_bank_data()
        if users[str(ctx.author.id)]["booster"] < 10:
            if users[str(ctx.author.id)]["wallet"] >= 3500000:
                users[str(ctx.author.id)]["wallet"] -= 3500000
                users[str(ctx.author.id)]["booster"] = 10
                await ctx.send(":white_check_mark: You now have a booster for 10x the money!")
                with open('databases/mainbank.json', 'w') as f:
                    json.dump(users, f,indent=4)
                return
            else:
                await ctx.send("You can't afford this!")
                return
        else:
            await ctx.send(":x: You already have a booster that's higher than this!")
            return
    if item == "gru trusts me role":
        if users[str(ctx.author.id)]["wallet"] < 500000:
            await ctx.send(":x: You can't afford this!")
            return
        else:
            if ctx.guild.id != 762829356812206090:
                return await ctx.send("This object is not available in your server!")
            roles = get(ctx.guild.roles, name="Gru trusts me")
            if roles in ctx.author.roles:
                await ctx.send(":x: You already have this rank!")
                return
            else:
                await ctx.send(":white_check_mark: You now have the Gru trusts me role and have access to a exclusive channel!")
                member = ctx.author
                users[str(ctx.author.id)]["wallet"] -= 500000
                with open('databases/mainbank.json', 'w') as f:
                    json.dump(users, f,indent=4)
                role = get(member.guild.roles, name="Gru trusts me")
                await ctx.author.add_roles(role)
                return

    await open_account(ctx.author)

    res = await buy_this(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            await ctx.send("That Object isn't there!")
            return
        if res[1] == 2:
            if amount == 1:
                await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}!")
            else:
                await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}s!")
            return

    if item == 'pc':
        item = item.upper()
    else:
        for items in mainshop:
            if items["name"].lower() == item.lower():
                item = items["name"]
        for items in animal_shop:
            for animal in items:
                if animal["name"].lower() == item.lower():
                    item = animal["name"]


    if item.lower() == 'watch' and amount > 1:
        item = item + "es"
    if amount > 1 and item.lower() != 'watches':
        item = item + "s"

    await ctx.send(f":white_check_mark: You just bought {amount} {item} for `{res[2]:,} Minions™`!")



@client.command(aliases=['inv'])
async def inventory(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
        await open_account(ctx.author)
    else:
        await open_account(user)

    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []

    em = discord.Embed(title="Your inventory", color=discord.Color.random())
    if user != ctx.author:
        em.title = f"{user.display_name}'s inventory"
    if len(bag) <= 25:
        for item in bag:
            name = item["item"]
            if name == 'Pc':
                name = name.upper()
            else:
                for items in mainshop:
                    if items["name"].lower() == name:
                        name = items["name"]
                for _array in animal_shop:
                    for animal_data in _array:
                        if animal_data["name"].lower() == name:
                            name = animal_data["name"]

            amount = item["amount"]
            em.add_field(name=name, value=f"Amount: {amount}")
        em.set_footer(text="Page 1/1")
        await ctx.send(embed=em)
        return

    elif len(bag) >= 26 and len(bag) <= 50:
        page2 = discord.Embed(title="Your inventory (Page 2)", color=discord.Color.random())
        if user != ctx.author:
            page2.title = f"{user.display_name}'s inventory (Page 2)"
        for item in itertools.islice(bag, 25):
            name = item["item"]
            if name == 'Pc':
                name = name.upper()
            else:
                for items in mainshop:
                    if items["name"].lower() == name:
                        name = items["name"]
                for _array in animal_shop:
                    for animal_data in _array:
                        if animal_data["name"].lower() == name:
                            name = animal_data["name"]
            
            amount = item["amount"]
            em.add_field(name=name, value=f"Amount: {amount}")
        em.set_footer(text="Page 1/2")
        i = len(bag)-25
        for item in bag[-i:]:
            name = item["item"]
            if name == 'Pc':
                name = name.upper()
            else:
                for items in mainshop:
                    if items["name"].lower() == name:
                        name = items["name"]
                for _array in animal_shop:
                    for animal_data in _array:
                        if animal_data["name"].lower() == name:
                            name = animal_data["name"]
            
            amount = item["amount"]
            page2.add_field(name=name, value=f"Amount: {amount}")
        page2.set_footer(text="Page 2/2")

        pages = [em, page2]

        buttons = [u"\u23F9",u"\u2B05", u"\u27A1"] #start, exit, right
        current = 0
        msg = await ctx.send(embed=pages[current])

        for button in buttons:
            await msg.add_reaction(button)

        while True:
            try:
                reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)
            except asyncio.TimeoutError:
                pages[current].set_footer(text="Timed out :(")
                await msg.edit(embed=pages[current])
                break
            else:
                previous_page = current

                if reaction.emoji == u"\u2B05":
                    if current > 0:
                        current -= 1
                elif reaction.emoji == u"\u27A1":
                    if current < len(pages) - 1:
                        current += 1
                elif reaction.emoji == u"\u23F9":
                    await msg.delete()
                    break



                if current != previous_page:
                    await msg.edit(embed=pages[current])

                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)

    elif len(bag) > 50:
        page2 = discord.Embed(title="Your inventory (Page 2)", color=discord.Color.random())
        page3 = discord.Embed(title="Your inventory (Page 3)", color=discord.Color.random())
        if user != ctx.author:
            page2.title = f"{user.display_name}'s inventory (Page 2)"
            page3.title= f"{user.display_name}'s inventory (Page 3)"
            
        for item in itertools.islice(bag, 25):
            name = item["item"]
            if name == 'Pc':
                name = name.upper()
            else:
                for items in mainshop:
                    if items["name"].lower() == name:
                        name = items["name"]
                for _array in animal_shop:
                    for animal_data in _array:
                        if animal_data["name"].lower() == name:
                            name = animal_data["name"]

            amount = item["amount"]
            em.add_field(name=name, value=f"Amount: {amount}")

        em.set_footer(text="Page 1/3")
        i = len(bag) -25
        i2 = len(bag) -50
        for item in bag[-i:]:
            name = item["item"]
            if name == 'Pc':
                name = name.upper()
            else:
                for items in mainshop:
                    if items["name"].lower() == name:
                        name = items["name"]
                for _array in animal_shop:
                    for animal_data in _array:
                        if animal_data["name"].lower() == name:
                            name = animal_data["name"]

            amount = item["amount"]
            page2.add_field(name=name, value=f"Amount: {amount}")
        page2.set_footer(text="Page 2/3")
        for item in bag[-i2:]:
            name = item["item"]
            if name == 'Pc':
                name = name.upper()
            else:
                for items in mainshop:
                    if items["name"].lower() == name:
                        name = items["name"]
                for _array in animal_shop:
                    for animal_data in _array:
                        if animal_data["name"].lower() == name:
                            name = animal_data["name"]
            amount = item["amount"]
            page3.add_field(name=name, value=f"Amount: {amount}")

        page3.set_footer(text="Page 3/3")
        pages = [em, page2, page3]

        buttons = [u"\u23F9","\u23EA",u"\u2B05", u"\u27A1","\u23E9"] #start, exit, right
        current = 0
        msg = await ctx.send(embed=pages[current])

        for button in buttons:
            await msg.add_reaction(button)

        while True:
            try:
                reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)
            except asyncio.TimeoutError:
                pages[current].set_footer(text="Timed out :(")
                await msg.edit(embed=pages[current])
                break
            else:
                previous_page = current

                if reaction.emoji == u"\u2B05":
                    if current > 0:
                        current -= 1

                elif reaction.emoji == u"\u27A1":
                    if current < len(pages) - 1:
                        current += 1
                elif reaction.emoji == u"\u23F9":
                    await msg.delete()
                    break
                elif reaction.emoji == "\u23E9":
                    current = len(pages)-1
                elif reaction.emoji == "\u23EA":
                    current=0

                if current != previous_page:
                    await msg.edit(embed=pages[current])

                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)




async def buy_this(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False, 1]

    cost = price * amount
    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0] < cost:
        return [False, 2]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]["bag"] = [obj]

    with open("databases/mainbank.json", "w") as f:
        json.dump(users, f, indent=4)

    await update_bank(user, cost * -1, "wallet")

    return [True, "Worked", cost]


@client.command()
async def sell(ctx,amount: Optional[int]=1, *, item):
    await open_account(ctx.author)

    res = await sell_this(ctx.author, item, amount)
    if item == 'pc':
        item = item.upper()
    else:
        for items in mainshop:
            if items["name"].lower() == item.lower():
                item = items["name"]
        for items in animal_shop:
            for animal in items:
                if animal["name"].lower() == item.lower():
                    item = animal["name"]


    if item.lower() == 'watch' or item.lower() == "dumbo octopus" and amount > 1:
        item = item + "es"
    if amount > 1 and item.lower() != 'watches' and item.lower() != "dumbo octopus":
        item = item + "s"

    if not res[0]:
        if res[1] == 1:
            await ctx.send(":x: That Object isn't there!")
            return
        if res[1] == 2:
            await ctx.send(f":x: You don't have {amount} {item} in your bag.")
            return
        if res[1] == 3:
            await ctx.send(f":x: You don't have {item} in your bag.")
            return


    await ctx.send(f":white_check_mark: You just sold {amount} {item} for `{int(res[2]):,} Minions™`!")


async def sell_this(user, item_name, amount, price=None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price == None:
                price = 0.7 * item["price"]
            break
    for item in animal_shop:
        for animal in item:
            name = animal["name"].lower()
            if name == item_name:
                name_ = name
                if price == None:
                    price = animal["sell_price"]
                break

    if name_ == None:
        return [False, 1]

    cost = price * amount

    users = await get_bank_data()

    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False, 2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                if users[str(user.id)]["bag"][index]["amount"] == 0:
                    del users[str(user.id)]["bag"][index]
                t = 1
                break
            index += 1
        if t == None:
            return [False, 3]
    except:
        return [False, 3]

    with open("databases/mainbank.json", "w") as f:
        json.dump(users, f, indent=4)

    await update_bank(user, cost, "wallet")

    return [True, "Worked", cost]


async def open_account(user):
    users = await get_bank_data()
    jobs = await get_job_data()
    lootbox_data = await get_lootbox_data()

    if str(user.id) in users or user.bot:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = random.randint(0, 3000)
        users[str(user.id)]["bank"] = 0
        users[str(user.id)]["booster"] = 1
    if not str(user.id) in jobs:
            jobs[str(user.id)] = {}
            jobs[str(user.id)]["job"] = {}
            jobs[str(user.id)]["job"]["name"] = 'None'
            jobs[str(user.id)]["job"]["pay"] = 0
    if not str(user.id) in lootbox_data:
        lootbox_data[str(user.id)] = {}
        lootbox_data[str(user.id)]["common"] = 0
        lootbox_data[str(user.id)]["uncommon"] = 0
        lootbox_data[str(user.id)]["rare"] = 0
        lootbox_data[str(user.id)]["epic"] = 0
        lootbox_data[str(user.id)]["legendary"] = 0
        lootbox_data[str(user.id)]["mythic"] = 0
        lootbox_data[str(user.id)]["admin"] = 0

    with open('databases/mainbank.json', 'w') as f:
        json.dump(users, f, indent=4)
    with open('databases/jobs.json', 'w') as f:
        json.dump(jobs, f, indent=4)
    with open('databases/lootboxes.json', 'w') as f:
        json.dump(lootbox_data, f, indent=4)

    return True


async def get_bank_data():
    with open('databases/mainbank.json', 'r') as f:
        users = json.load(f)

    return users


async def get_job_data():
    with open('databases/jobs.json', 'r') as f:
        jobs = json.load(f)

    return jobs


async def get_lootbox_data():
    with open('databases/lootboxes.json', 'r') as f:
        lootbox_data = json.load(f)

    return lootbox_data


async def update_bank(user, change=0, mode='wallet'):
    users = await get_bank_data()

    users[str(user.id)][mode] += float(change)

    with open('databases/mainbank.json', 'w') as f:
        json.dump(users, f, indent=4)
    bal = users[str(user.id)]['wallet'], users[str(user.id)]['bank']
    return bal


@client.command(pass_context=True, aliases=['rguser', 'rgu'])
@commands.is_owner()
async def registeruser(ctx, user: discord.Member):
    id = str(user.id)
    users = await get_bank_data()
    if id not in users:
        await open_account(user)
        await ctx.send(":white_check_mark: They are now registered")
    else:
        await ctx.send(":x: They already have an account")
        return


@client.command(aliases=['unrg'])
@commands.is_owner()
async def unregisteruser(ctx, user: discord.Member):
    id = str(user.id)
    users = await get_bank_data()
    jobs = await get_job_data()
    lootbox_data = await get_lootbox_data()
    if id not in users:
        await ctx.send(":x: They don't have an account")
        return
    else:
        del users[str(user.id)]
        del jobs[str(user.id)]
        del lootbox_data[str(user.id)]

        await ctx.send(":white_check_mark: Ok their account is now deleted.")
        with open('databases/mainbank.json', 'w') as f:
            json.dump(users, f)
        with open('databases/jobs.json', 'w') as f:
            json.dump(jobs, f, indent=4)


@client.command()
@commands.is_owner()
async def give(ctx, user: discord.Member, amount: int, area: str = "wallet"):
    id = str(user.id)
    users = await get_bank_data()
    if area != 'bank' and area != 'wallet':
        await ctx.send(':x: Invalid area.Types: wallet, bank')
        return
    else:
        if id not in users:
            await ctx.send(":x: That user isn't registered")
        else:
            await ctx.send(f":white_check_mark: Gave {amount} Minions™ to user {user.display_name}'s {area}!")
            if area == 'wallet':
                await update_bank(user, amount, 'wallet')
            elif area == 'bank':
                await update_bank(user, amount, 'bank')


@client.command()
@commands.is_owner()
async def take(ctx, user: discord.Member, amount: int, area: str = "wallet"):
    id = str(user.id)
    users = await get_bank_data()
    wallet_amt = users[str(id)]["wallet"]
    bank_amt = users[str(id)]["bank"]
    if area != 'bank' and area != 'wallet':
        await ctx.send('Invalid area.Types: wallet, bank')
        return
    if area == 'bank' and bank_amt < amount:
        await ctx.send(":x: That makes the user have negative money so this action cannot be done.")
        return
    if area == 'wallet' and wallet_amt < amount:
        await ctx.send(":x: That makes the user have negative money so this action cannot be done.")
        return
    else:

        if id not in users:
            await ctx.send(":white_check_mark: That user isn't registered")
            return
        else:
            await ctx.send(f":white_check_mark: Took {amount} Minions™ from user {user.display_name}'s {area}!")
            if area == 'wallet':
                wallet_amt -= amount
                await update_bank(user, -1 * amount, 'wallet')
            elif area == 'bank':
                bank_amt -= amount
                await update_bank(user, -1 * amount, 'bank')


@client.command()
async def poop(ctx):
    await ctx.send(
        f"{ctx.author.mention} :poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop:")


@client.command(aliases=['viewbal', 'vb', 'vbal'])
async def viewbalance(ctx, user: discord.Member):
    id = str(user.id)
    users = await get_bank_data()
    jobs = await get_job_data()
    if not str(user.id) in jobs:
        jobs[str(user.id)] = {}
        jobs[str(user.id)]["job"] = {}
        jobs[str(user.id)]["job"]["name"] = 'None'
        jobs[str(user.id)]["job"]["pay"] = 0
        with open('databases/jobs.json', 'w') as f:
            json.dump(jobs, f, indent=4)

    if id not in users:
        await ctx.send(":x: That user isn't registered")
    else:
        wallet_amt = users[str(id)]["wallet"]
        bank_amt = users[str(id)]["bank"]
        booster_amt = users[str(id)]["booster"]
        job_name = jobs[str(user.id)]["job"]["name"]
        job_pay = jobs[str(user.id)]["job"]["pay"]
        em = discord.Embed(title=f"Showing balance of {user.display_name}", color=discord.Color.green())
        if wallet_amt + bank_amt >= 1000000000000000:
            em.add_field(name="Wallet Balance", value=f"{float(wallet_amt)} Minions™")
            em.add_field(name='Bank Balance', value=f"{float(bank_amt)} Minions™")
            em.add_field(name='Job', value=job_name)
            em.add_field(name='Job salary', value=f"{float(job_pay)} Minions™ per hour")
            if booster_amt != 1:
                em.add_field(name='Booster', value=f'{float(booster_amt)}x')
        else:
            em.add_field(name="Wallet Balance", value=f"{int(wallet_amt)} Minions™")
            em.add_field(name='Bank Balance', value=f"{int(bank_amt)} Minions™")
            em.add_field(name='Job', value=job_name)
            em.add_field(name='Job salary', value=f"{int(job_pay)} Minions™ per hour")
            if booster_amt != 1:
                em.add_field(name='Booster', value=f'{int(booster_amt)}x')
        await ctx.send(embed=em)


@client.command(aliases=['scn'])
@commands.has_permissions(manage_channels=True)
async def set_channel_name(ctx, channel: discord.TextChannel, *, new_name):
    await channel.edit(name=new_name)
    await ctx.send(":white_check_mark: Done!")


@client.command(aliases=['sb'])
@commands.is_owner()
async def setbooster(ctx, user: discord.Member, amount: int):
    id = str(user.id)
    users = await get_bank_data()
    if id not in users:
        await ctx.send(":x: That user isn't registered")
    else:
        await ctx.send(":white_check_mark: Done!")
        users[str(user.id)]["booster"] = amount

        with open('databases/mainbank.json', 'w') as f:
            json.dump(users, f)


@client.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def giverole(ctx, user: discord.Member, *, role: discord.Role):
    if role.position > ctx.author.top_role.position:  # if the role is above users top role it sends error
        return await ctx.send('**:x: | That role is above your top role!**')

    if role.position == ctx.author.top_role.position and ctx.author.id != 717512097725939795:
        await ctx.send("You can't do this!")
        return
    if role in user.roles:
        await ctx.send(":x: They already have this rank!")
        return
    else:
        await user.add_roles(role)
        await ctx.send(f":white_check_mark: {user.display_name} has been given a role called: {role.name}")


@client.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def takerole(ctx, user: discord.Member, *, role: discord.Role):
    if role.position > ctx.author.top_role.position:  # if the role is above users top role it sends error
        return await ctx.send('**:x: | That role is above your top role!**')
    if role in user.roles:
        await user.remove_roles(role)
        await ctx.send(f":white_check_mark: {user.display_name} has lost their {role.name} rank")
    else:
        await ctx.send(":x: They don't have this role!")


@client.command(aliases=["members"])
async def membercount(ctx):
    delta = datetime.datetime.now()
    embed = discord.Embed(
        title=('Member Count'),
        description=(f'There are currently **{ctx.guild.member_count}** members in the server!'),
        timestamp=delta,
        url='',
        color=discord.Color.dark_blue()
    )
    embed.set_footer(text='Our Community')
    await ctx.send(embed=embed)
    try:
        await ctx.message.delete()
    except:
        pass




@client.command(aliases=["lb"])
async def leaderboard(ctx, x:Optional[int]=10, type_of="all"):
    if type_of.lower() != "all" and type_of.lower() != "server":
        return await ctx.send("That is an invalid type! Types are `all` or `server`")
    users = await get_bank_data()
    if len(users) < x:
        x = len(users)

    leader_board = {}
    for user in users:
        leader_board[user] = users[user]["wallet"] + users[user]["bank"]


    users_who_are_in = []
    new = dict(sorted(leader_board.items(),key = lambda t: t[::-1]))
    final = sorted(new.items(), key=lambda x: x[1], reverse=True)
    final = dict(final)


    em = discord.Embed(title=f"Top {x} Richest People",
                       description="This is decided on the basis of raw money in the bank and wallet",
                       color=discord.Color(0xfa43ee))
    if type_of.lower() == "all":
        index = 1
        for key in final.keys():
            member = await client.fetch_user(int(key))
            if key == "739112359515390023":
                continue

            name = member.name
            em.add_field(name=f"{index}. {name}", value=f"{int(leader_board[key])}", inline=False)
            if index == x:
                break
            else:
                index += 1
    else:
        index = 1
        for key in final.keys():
            member = await client.fetch_user(int(key)) 
            if key == "739112359515390023":
                continue
            elif key == "717512097725939795" and ctx.author.id != 717512097725939795:
                continue
            name = member.name
            if member in ctx.guild.members:                 
                em.add_field(name=f"{index}. {name}", value=f"{int(leader_board[key])}", inline=False)                         
                users_who_are_in.append(member)
                if index == x:
                  break
                else:
                    index += 1
        em.title = f"Top {len(users_who_are_in)} Richest People In The Server"

    await ctx.send(embed=em)




@client.command()
async def emojify(ctx, *, text):
    emojis = []
    for s in text.lower():
        if s.isdecimal():
            num2emo = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six',
                       '7': 'seven', '8': 'eight', '9': 'nine'}
            emojis.append(f':{num2emo.get(s)}:')

        elif s.isalpha():
            emojis.append(f':regional_indicator_{s}:')
        elif s == '!':
            emojis.append(':grey_exclamation:')
        elif s == "#":
            emojis.append(":hash:")
        else:
            emojis.append(s)

    await ctx.send(' '.join(emojis))


@client.event
async def on_message(message):
    with open('databases/prefixes.json','r') as f:
        prefixes = json.load(f)
    try:
        prefix = prefixes[str(message.guild.id)]
        if ":loading:" in message.content and message.guild.id == 762829356812206090 and message.author.id != client.user.id and message.content[0] != prefix or ":rick_roll:" in message.content or ":loading:" in message.content and message.author.id != client.user.id and message.content[0] != prefix:
            send = message.content.replace(":loading:","<a:loading:898340114164490261>")
            send = send.replace(':rick_roll:','<a:rick_roll:898749226123669575>')
            await message.channel.send(f"{send}")
            await message.channel.send(f"`Sent by: {message.author}`")
            await message.delete()
    except:
        pass
    try:
        if message.mentions[0] == client.user and message.content == '<@874328552965820416>':
            with open("databases/prefixes.json", "r") as f:
                prefixes = json.load(f)
            pre = prefixes[str(message.guild.id)]
            await message.channel.send(f"My prefix for this server is `{pre}`")
    except Exception as e:
        pass
    try:
        if not message.author.bot:
            with open('databases/server_configs.json','r') as f:
                configs = json.load(f)
            with open('databases/levels.json', 'r') as f:
                levels = json.load(f)
                if configs[str(message.guild.id)]['levels'] == True:
                    await update_data(levels, message.author, message.guild)
                    await add_experience(levels, message.author, levels[str(message.guild.id)][str(message.author.id)]['level']*1.3, message.guild)
                    await level_up(levels, message.author, message.channel, message.guild)


        await client.process_commands(message)
    except:
        return


async def update_data(users, user, server):
    await open_account(user)
    if not str(server.id) in users:
        users[str(server.id)] = {}
        if not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1
    elif not str(user.id) in users[str(server.id)]:
        users[str(server.id)][str(user.id)] = {}
        users[str(server.id)][str(user.id)]['experience'] = 0
        users[str(server.id)][str(user.id)]['level'] = 1

    with open('databases/levels.json', 'w') as f:
        json.dump(users, f, indent=4)


async def add_experience(users, user, exp, server):
    users[str(user.guild.id)][str(user.id)]['experience'] += exp
    with open('databases/levels.json','w') as f:
        json.dump(users, f,indent=4)


async def level_up(users, user, channel, server):
    experience = users[str(user.guild.id)][str(user.id)]['experience']
    lvl_start = users[str(user.guild.id)][str(user.id)]['level']
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        await channel.send('Congratulations! {} has leveled up to **Level {}** and has a total of **{} xp**! :tada: :tada:'.format(user.mention, lvl_end, experience))
        with open('databases/lootboxes.json','r') as f:
                lootboxes = json.load(f)
        crate_type = random.choice(["mythic","legendary","legendary","epic","epic","epic","epic","rare","rare","rare","rare","rare","rare","rare","uncommon","uncommon","uncommon","uncommon","uncommon","uncommon","uncommon","uncommon","uncommon","common","common","common","common","common","common","common","common","common","common"])
        await channel.send(f"You earned a **{crate_type.capitalize()}** <:chest:898333946557894716> lootbox!! :tada:")
        lootboxes[str(user.id)][crate_type] += 1
        with open('databases/lootboxes.json','w') as f:
            json.dump(lootboxes, f, indent=4)
        users[str(user.guild.id)][str(user.id)]['level'] = lvl_end
        with open('databases/levels.json','w') as f:
            json.dump(users, f, indent=4)

def level_by_xp(xp):
    return xp ** (1/4)

def xp_by_level(level):
    return level ^ 4


def custom_poppins(text):
    if len(text) < 30:
        return Font.poppins(size=40)
    if len(text) > 30:
        return Font.poppins(size=30)


async def get_lvl_card(lvl, exp, author):
    _exp = ...
    total = ...
    exponent = 4
    next_lvl = lvl + 1
    next_lvl_xp = next_lvl ** exponent
    current_xp =  exp - (lvl) ** exponent
    next_lvl_xp -= lvl **4
    total = next_lvl_xp
    _exp = current_xp
    per = round(float(_exp/total)*100)
    border_radius = 20
    userData = {
        'name':f"{author.name}#{author.discriminator}",
        'lvl':lvl,
        'xp':int(_exp),
        'next_lvl_xp': total,
        'percent':per
    }
    background = Editor(Canvas((900,300),color="#141414"))
    profile_pic = await load_image_async(str(author.display_avatar.url))
    profile = Editor(profile_pic).resize((150,150)).circle_image()
    poppins = custom_poppins(userData['name'])
    poppins_small = Font.poppins(size=30)
    bar_color = "#ff0000"
    if userData['percent'] > 90:
        bar_color = "#0afc05"
    elif userData['percent'] > 80:
        bar_color = "#06d902"
    elif userData['percent'] > 75:
        bar_color="#05b802"
    elif userData['percent'] > 50:
        bar_color = "#f4f73b"
    elif userData['percent'] > 25:
        bar_color="#ffbe3b"
    card_right_shape = [(600,0),(750,300),(900,300),(900,0)]
    background.polygon(card_right_shape,color="#545352")
    background.paste(profile, (30,30))
    background.rectangle((30,220),width=650,height=40,color="#ffffff",radius=border_radius)
    if per >3:
        background.bar((30,220),max_width=650,height=40,percentage=userData['percent'],color=bar_color,radius=border_radius)
    background.text((200,40),userData['name'],font=poppins,color="#ffffff")
    background.rectangle((200,100),width=350,height=2,fill="#ffffff")
    background.text(
        (200,130),
        f"Level - {userData['lvl']} | XP - {userData['xp']}/{userData['next_lvl_xp']}",
        font=poppins_small,
        color="#ffffff"
    )

    file = discord.File(fp=background.image_bytes, filename="levelcard.png")
    return file      


@client.command(aliases=['rank', 'lvl'])
async def level(ctx, member: discord.Member = None):
    if not member:

        user = ctx.message.author
        with open('databases/levels.json', 'r') as f:
            users = json.load(f)

            lvl = users[str(ctx.guild.id)][str(user.id)]['level']
            exp = users[str(ctx.guild.id)][str(user.id)]['experience']
        return await ctx.send(file=await get_lvl_card(lvl,exp, ctx.author))

    else:
        with open('databases/levels.json', 'r') as f:
            users = json.load(f)
        if member.bot:
            await ctx.send("Bots aren't in the database!")
            return

        if not str(member.id) in users[str(member.guild.id)]:
            users[str(member.guild.id)][str(member.id)] = {}
            users[str(member.guild.id)][str(member.id)]['experience'] = 0
            users[str(member.guild.id)][str(member.id)]['level'] = 1
            with open('databases/levels.json','w')as f:
                json.dump(users, f, indent=4)

        lvl = users[str(ctx.guild.id)][str(member.id)]['level']
        exp = users[str(ctx.guild.id)][str(member.id)]['experience']

        return await ctx.send(file=await get_lvl_card(lvl,exp, member))



@client.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def wanted(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    wanted = Image.open("pictures/wanted.jpeg")

    asset = user.display_avatar.with_size(128)

    data = BytesIO(await asset.read())
    profilepic = Image.open(data)

    profilepic = profilepic.resize((300, 300))
    wanted.paste(profilepic, (78, 219))

    wanted.save("pictures/wantedpic.jpeg")

    await ctx.send(file=discord.File("pictures/wantedpic.jpeg"))
    await ctx.send(f"{user.display_name} has a bounty of 100k OMG POGGGGG!")
    await asyncio.sleep(0.5)
    if user == client.user:
        await ctx.send("Oh no that's me. I gotta RUNNNNN!!!!")
    wanted.close()


@client.command()
@commands.cooldown(1,30, commands.BucketType.user)
async def guessing(ctx):
    number = random.randint(0, 100)
    channel = ctx.message.channel

    def check(m):
        return m.content is not None and m.author == ctx.author and m.channel == channel

    tries = 10
    for i in range(0, 10):
        await ctx.send(f'Guess a number between 0 and 100. You have {tries} tries left')
        response = await client.wait_for('message', check=check)
        guess = int(response.content)
        if i == 9:
            await ctx.send(f"You lost. The number was {number}. Thanks for playing!")
            break
        if guess > number:
            await ctx.send('Your number is too big!')
            tries -= 1
        elif guess < number:
            await ctx.send('Your number is too small!')
            tries -= 1
        else:
            await ctx.send('Correct! You win. Thanks for playing!')
            break
    return



@client.command()
@commands.is_owner()
async def idtouser(ctx, id=None):
    if id is None:
        await ctx.send("Please enter an id.")
        return
    user = await client.fetch_user(id)
    await ctx.send(f"Original id:{id}, Username:{user.display_name}")




@idtouser.error
async def idtouser_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Unknown user")



@client.command()
@commands.is_owner()
async def usertoid(ctx, user: discord.Member = None):
    if user is None:
        await ctx.send("Please enter a user.")
        return
    else:
        id = user.id
        await ctx.send(f"Original name:{user.display_name}, id:{id}")



@usertoid.error
async def usertoid_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("Unknown user")



@client.command()
@commands.has_permissions(manage_guild=True)
async def gcreate(ctx, time=None, *, prize=None):
    with open('databases/server_configs.json','r') as f:
        configs = json.load(f)
    guild = ctx.guild
    giveaway_role = guild.get_role(configs[str(ctx.guild.id)]["giveaway_role"])
    time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    gawtime = int(time[:-1]) * time_convert[time[-1]]
    time_stamp = datetime.datetime.now(ZoneInfo("America/New_York")) + datetime.timedelta(seconds=gawtime)
    if time == None:
        return await ctx.send('Please include a time!')
    elif prize == None:
        return await ctx.send('Please include a prize!')
    embed = discord.Embed(title='New Giveaway!', description=f'{ctx.author.mention} is giving away **{prize}**!!',
                          color=discord.Color.random())
    embed.set_footer(text=f'Giveaway ends at {time_stamp.strftime("%A, %B %d %Y @ %H:%M:%S %p")}.\nReact with the "🎉" to enter!')
    if giveaway_role != None:
        gaw_msg = await ctx.send(f"{giveaway_role.mention}", embed=embed)
    else:
        gaw_msg = await ctx.send(embed=embed)

    await gaw_msg.add_reaction("🎉")
    await asyncio.sleep(gawtime)

    await ctx.send("Picking a random user!")
    await asyncio.sleep(1)
    embed.title = "GIVEAWAY ENDED"
    embed.set_footer(text=f'Giveaway ended at {time_stamp.strftime("%A, %B %d %Y @ %H:%M:%S %p")}')
    try:
        await gaw_msg.edit(embed=embed)
    except:
        return await ctx.send("Couldn't find the original giveaway message! :(")
    new_gaw_msg = await ctx.channel.fetch_message(gaw_msg.id)
    users = await new_gaw_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    if ctx.author in users:
        users.pop(users.index(ctx.author))
    try:
        winner = random.choice(users)
    except:
        await ctx.send("No one won since no one entered!")
        return
    e = discord.Embed(description="None",color=discord.Color.random())
    if len(users) == 1:
        e.description="1 entrant"
    else:
        e.description = f"{len(users)} entrants"
    embed.description += f"\nWinner: {winner.mention}"
    await gaw_msg.edit(embed=embed)

    await ctx.send(f"YAYYYYY!!!! {winner.mention} has won the giveaway for **{prize}**!!",embed=e)


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member = None, *, reason=None):
    if user == None:
        await ctx.send("Please enter a user!")
        return

    await user.kick(reason=reason)
    await ctx.send(f'Kicked {user.name} for reason {reason}')


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member = None, *, reason=None):
    if user == None:
        await ctx.send("Please enter a user!")
        return

    await user.ban(reason=reason)
    await ctx.send(f'Banned {user.name} for reason {reason}')


@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.name}#{user.discriminator}')


@client.command()
@commands.cooldown(1, 300, commands.BucketType.user)
async def bankrob(ctx, user: discord.Member):
    if user.bot:
        bankrob.reset_cooldown(ctx)
        return await ctx.send("You are not allowed to steal from bots, back off my kind")
    await open_account(ctx.author)
    await open_account(user)
    bal1 = await update_bank(user)
    bal = await update_bank(ctx.author)
    if user.id == 717512097725939795:
        bankrob.reset_cooldown(ctx)
        return await ctx.send("xD you can't rob him he is the owner of the bot!!!")
    if bal1[1] < 100:
        await ctx.send("It's useless to rob their bank!")
        bankrob.reset_cooldown(ctx)
        return
    else:
        earning = random.randrange(0, bal1[1])
        fail_losing = random.randrange(0, bal[0])

        type = random.randint(0, 1)
        if type == 0:
            await ctx.send(f":x: You failed to rob {user} and paid them {fail_losing} Minions™!")
            await update_bank(user, fail_losing)
            await update_bank(ctx.author, fail_losing * -1)
        elif type == 1:
            await ctx.send(f":white_check_mark: You successfully robbed {user} and got {earning} Minions™!")
            await update_bank(ctx.author, earning)
            await update_bank(user, earning * -1)


@client.command(aliases=["show"])
async def showpic(ctx, *, search):
    ran = random.randint(0, 9)
    resource = build("customsearch", "v1", developerKey=api_key).cse()
    result = resource.list(q=f"{search}", cx="ac76df62ee40c6a13", searchType="image").execute()
    url = result["items"][ran]["link"]
    embed1 = discord.Embed(title=f"Here Your Image ({search})", color=discord.Color.random())
    embed1.set_image(url=url)
    await ctx.send(embed=embed1)


@client.command()
async def youtube(ctx, *, search):
    query_string = urllib.parse.urlencode({'search_query': search})
    html_content = urllib.request.urlopen(
        'https://www.youtube.com/results?' + query_string
    )
    search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())

    await ctx.send(f"Here's your video from query {search}!!")
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])


@client.command()
async def roles(ctx):
    role_names = await ctx.guild.fetch_roles()
    role_names.sort(reverse=True)
    roles = "\n".join([str(r.mention) for r in role_names][:-1])

    e = discord.Embed(title=f"Roles [{len(role_names) - 1}]", description=roles, color=discord.Color.random())
    await ctx.send(embed=e, allowed_mentions=discord.AllowedMentions(roles=False))


@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    role = get(ctx.guild.roles, name="Muted")
    guild = ctx.guild
    if role not in guild.roles:
        perms = discord.Permissions(send_messages=False, speak=False)
        await guild.create_role(name="Muted", permissions=perms)
        if role in member.roles:
            await ctx.send("They are already muted!")
            return
        await member.add_roles(role)
        await ctx.send(f"🔨{member} was muted.")
    else:
        if role in member.roles:
            await ctx.send("They are already muted!")
            return
        await member.add_roles(role)
        await ctx.send(f"🔨{member} was muted.")


@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    role = get(ctx.guild.roles, name="Muted")
    if role not in member.roles:
        await ctx.send("They are not muted!")
        return
    else:
        await member.remove_roles(role)
        await ctx.send(f":white_check_mark:{member} was unmuted.")


@client.command()
async def update(ctx, user: discord.Member):
    lootbox_data = await get_lootbox_data()
    if not str(user.id) in lootbox_data:
        lootbox_data[str(user.id)] = {}
        lootbox_data[str(user.id)]["common"] = 0
        lootbox_data[str(user.id)]["uncommon"] = 0
        lootbox_data[str(user.id)]["rare"] = 0
        lootbox_data[str(user.id)]["epic"] = 0
        lootbox_data[str(user.id)]["legendary"] = 0
        lootbox_data[str(user.id)]["mythic"] = 0
        lootbox_data[str(user.id)]["admin"] = 0
        with open('databases/lootboxes.json', 'w') as f:
            json.dump(lootbox_data, f, indent=4)
        await ctx.send("Done!")


@client.command()
async def crates(ctx, user: discord.Member = None):
    await open_account(ctx.author)
    lootbox_data = await get_lootbox_data()
    if user is None:
        common_amt = lootbox_data[str(ctx.author.id)]["common"]
        uncommon_amt = lootbox_data[str(ctx.author.id)]["uncommon"]
        rare_amt = lootbox_data[str(ctx.author.id)]["rare"]
        epic_amt = lootbox_data[str(ctx.author.id)]["epic"]
        legendary_amt = lootbox_data[str(ctx.author.id)]["legendary"]
        mythic_amt = lootbox_data[str(ctx.author.id)]["mythic"]
        admin_amt = lootbox_data[str(ctx.author.id)]["admin"]
        e = discord.Embed(title=f"{ctx.author.name}'s Crates", color=discord.Color.random())

        e.add_field(name="Common", value=common_amt)
        e.add_field(name="Uncommon", value=uncommon_amt)
        e.add_field(name="Rare", value=rare_amt)
        e.add_field(name="Epic", value=epic_amt)
        e.add_field(name="Legendary", value=legendary_amt)
        e.add_field(name="Mythic", value=mythic_amt)
        sradmin = get(ctx.guild.roles, name="Sr.Admin")
        admin = get(ctx.guild.roles, name="Admin")
        mod = get(ctx.guild.roles, name="Moderator")
        owner = get(ctx.guild.roles, name="Owner")
        if admin_amt >= 1 or ctx.author.id == 717512097725939795:
            e.add_field(name="Admin", value=admin_amt)
        await ctx.reply(embed=e)

    else:
        common_amt = lootbox_data[str(user.id)]["common"]
        uncommon_amt = lootbox_data[str(user.id)]["uncommon"]
        rare_amt = lootbox_data[str(user.id)]["rare"]
        epic_amt = lootbox_data[str(user.id)]["epic"]
        legendary_amt = lootbox_data[str(user.id)]["legendary"]
        mythic_amt = lootbox_data[str(user.id)]["mythic"]
        admin_amt = lootbox_data[str(user.id)]["admin"]
        e = discord.Embed(title=f"{user.name}'s Crates", color=discord.Color.random())

        e.add_field(name="Common", value=common_amt)
        e.add_field(name="Uncommon", value=uncommon_amt)
        e.add_field(name="Rare", value=rare_amt)
        e.add_field(name="Epic", value=epic_amt)
        e.add_field(name="Legendary", value=legendary_amt)
        e.add_field(name="Mythic", value=mythic_amt)
        sradmin = get(ctx.guild.roles, name="Sr.Admin")
        admin = get(ctx.guild.roles, name="Admin")
        mod = get(ctx.guild.roles, name="Moderator")
        owner = get(ctx.guild.roles, name="Owner")
        if admin_amt >= 1 or sradmin in ctx.author.roles or admin in ctx.author.roles or mod in ctx.author.roles or owner in ctx.author.roles:
            e.add_field(name="Admin", value=admin_amt)
        await ctx.reply(embed=e)


@client.command()
async def crate_info(ctx):
    e = discord.Embed(title="Crate Info", description="These are the loot tables for all the crates.",
                      color=discord.Color.random())
    e.add_field(name="Common", value="2,000 - 5,000")
    e.add_field(name="Uncommon", value="5,000 - 10,000")
    e.add_field(name="Rare", value="30,000 - 50,000")
    e.add_field(name="Epic", value="50,000 - 100,000")
    e.add_field(name="Legendary", value="100,000 - 250,000")
    e.add_field(name="Mythic", value="200,000 - 300,000")
    e.add_field(name="Admin", value="900,000 - 1,000,000")
    await ctx.reply(embed=e)


@client.command(aliases=["open"])
async def opencrate(ctx, type=None, amount=None):
    user = ctx.author
    lootbox_data = await get_lootbox_data()
    total_lootboxes = lootbox_data[str(user.id)]["common"] + lootbox_data[str(user.id)]["uncommon"] + lootbox_data[str(user.id)]["rare"] + lootbox_data[str(user.id)]["epic"] + lootbox_data[str(user.id)]["legendary"] + lootbox_data[str(user.id)]["mythic"] + lootbox_data[str(user.id)]["admin"]

    if amount == None:
        amount = 1

    types = ["admin", "common", "c", "uncommon", "u", "rare", "r", "epic", "legendary", "l", "mythic", "m", "all", "a",
             "e"]
    if type == None:
        await ctx.reply("Please enter something to open")
        return
    elif type.lower() not in types:
        await ctx.reply("Invalid crate type")
        return
    elif total_lootboxes == 0:
        await ctx.reply("You have no lootboxes to open")
        return
    if amount == 'a':
        if type.lower() == 'admin' or type.lower() == 'a':
            amt = lootbox_data[str(user.id)]["admin"]
            if amt == 0:
                await ctx.send("You have no admin lootboxes!")
                return
            amounts = []
            for x in range(0, amt):
                amountofcash = random.randint(900000, 1000000)
                amounts.append(amountofcash)
            total_cash = sum(amounts)
            e = discord.Embed(title=f"{ctx.author.name}'s Crates", color=discord.Color.random())
            e.add_field(name=f"{ctx.author.name}'s crate opening session!",
                        value=f"You opened {amt} **Admin** crate(s) <:chest:898333946557894716> and got `{total_cash} Minions™`!!! :tada:")
            await update_bank(ctx.author, total_cash)
            await ctx.reply(embed=e)
            lootbox_data[str(user.id)]["admin"] -= amt
            with open('databases/lootboxes.json', 'w') as f:
                json.dump(lootbox_data, f, indent=4)

        elif type.lower() == 'mythic' or type.lower() == 'm':
            amt = lootbox_data[str(user.id)]["mythic"]
            if amt == 0:
                await ctx.send("You have no mythic lootboxes!")
                return
            amounts = []
            for x in range(0, amt):
                amountofcash = random.randint(200000, 300000)
                amounts.append(amountofcash)
            total_cash = sum(amounts)
            e = discord.Embed(title=f"{ctx.author.name}'s Crates", color=discord.Color.random())
            e.add_field(name=f"{ctx.author.name}'s crate opening session!",
                        value=f"You opened {amt} **Mythic** crate(s) <:chest:898333946557894716> and got `{total_cash} Minions™`!!! :tada:")
            await update_bank(ctx.author, total_cash)
            await ctx.reply(embed=e)
            lootbox_data[str(user.id)]["mythic"] -= amt
            with open('databases/lootboxes.json', 'w') as f:
                json.dump(lootbox_data, f, indent=4)

        elif type == 'legendary' or type == 'l':
            amt = lootbox_data[str(user.id)]["legendary"]
            if amt == 0:
                await ctx.send("You have no legendary lootboxes!")
                return
            amounts = []
            for x in range(0, amt):
                amountofcash = random.randint(100000, 200000)
                amounts.append(amountofcash)
            total_cash = sum(amounts)
            e = discord.Embed(title=f"{ctx.author.name}'s Crates", color=discord.Color.random())
            e.add_field(name=f"{ctx.author.name}'s crate opening session!",
                        value=f"You opened {amt} **Legendary** crate(s) <:chest:898333946557894716> and got `{total_cash} Minions™`!!! :tada:")
            await update_bank(ctx.author, total_cash)
            await ctx.reply(embed=e)
            lootbox_data[str(user.id)]["legendary"] -= amt
            with open('databases/lootboxes.json', 'w') as f:
                json.dump(lootbox_data, f, indent=4)

        elif type == 'epic' or type == 'e':
            amt = lootbox_data[str(user.id)]["epic"]
            if amt == 0:
                await ctx.send("You have no epic lootboxes!")
                return
            amounts = []
            for x in range(0, amt):
                amountofcash = random.randint(50000, 100000)
                amounts.append(amountofcash)
            total_cash = sum(amounts)
            e = discord.Embed(title=f"{ctx.author.name}'s Crates", color=discord.Color.random())
            e.add_field(name=f"{ctx.author.name}'s crate opening session!",
                        value=f"You opened {amt} **Epic** crate(s) <:chest:898333946557894716> and got `{total_cash} Minions™`!!! :tada:")
            await update_bank(ctx.author, total_cash)
            await ctx.reply(embed=e)
            lootbox_data[str(user.id)]["epic"] -= amt
            with open('databases/lootboxes.json', 'w') as f:
                json.dump(lootbox_data, f, indent=4)

        elif type == 'rare' or type == 'r':
            amt = lootbox_data[str(user.id)]["rare"]
            if amt == 0:
                await ctx.send("You have no rare lootboxes!")
                return
            amounts = []
            for x in range(0, amt):
                amountofcash = random.randint(30000, 50000)
                amounts.append(amountofcash)
            total_cash = sum(amounts)
            e = discord.Embed(title=f"{ctx.author.name}'s Crates", color=discord.Color.random())
            e.add_field(name=f"{ctx.author.name}'s crate opening session!",
                        value=f"You opened {amt} **Rare** crate(s) <:chest:898333946557894716> and got `{total_cash} Minions™`!!! :tada:")
            await update_bank(ctx.author, total_cash)
            await ctx.reply(embed=e)
            lootbox_data[str(user.id)]["rare"] -= amt
            with open('databases/lootboxes.json', 'w') as f:
                json.dump(lootbox_data, f, indent=4)

        elif type == 'uncommon' or type == 'u':
            amt = lootbox_data[str(user.id)]["uncommon"]
            if amt == 0:
                await ctx.send("You have no uncommon lootboxes!")
                return
            amounts = []
            for x in range(0, amt):
                amountofcash = random.randint(5000, 10000)
                amounts.append(amountofcash)
            total_cash = sum(amounts)
            e = discord.Embed(title=f"{ctx.author.name}'s Crates", color=discord.Color.random())
            e.add_field(name=f"{ctx.author.name}'s crate opening session!",
                        value=f"You opened {amt} **Uncommon** crate(s) <:chest:898333946557894716> and got `{total_cash} Minions™`!!! :tada:")
            await update_bank(ctx.author, total_cash)
            await ctx.reply(embed=e)
            lootbox_data[str(user.id)]["uncommon"] -= amt
            with open('databases/lootboxes.json', 'w') as f:
                json.dump(lootbox_data, f, indent=4)

        elif type == "common" or type == "c":
            amt = lootbox_data[str(user.id)]["common"]
            if amt == 0:
                await ctx.reply("You have no common lootboxes!!")
                return
            amounts = []
            for x in range(0, amt):
                amountofcash = random.randint(2000, 5000)
                amounts.append(amountofcash)

            total_cash = sum(amounts)
            e = discord.Embed(title=f"{ctx.author.name}'s Crates", color=discord.Color.random())
            e.add_field(name=f"{ctx.author.name}'s crate opening session!",
                        value=f"You opened {amt} **Common** crate(s) <:chest:898333946557894716> and got `{total_cash} Minions™`!!! :tada:")
            await update_bank(ctx.author, total_cash)
            await ctx.reply(embed=e)
            lootbox_data[str(user.id)]["common"] -= amt
            with open('databases/lootboxes.json', 'w') as f:
                json.dump(lootbox_data, f, indent=4)
        return

    amount = int(amount)
    if type == 'all':
        amounts = []
        if lootbox_data[str(user.id)]["admin"] != 0:
            for x in range(0, lootbox_data[str(user.id)]["admin"]):
                amountofcash = random.randint(900000, 1000000)
                amounts.append(amountofcash)
            lootbox_data[str(user.id)]["admin"] = 0

        if lootbox_data[str(user.id)]["mythic"] != 0:
            for x in range(0, lootbox_data[str(user.id)]["mythic"]):
                amountofcash = random.randint(200000, 300000)
                amounts.append(amountofcash)
            lootbox_data[str(user.id)]["mythic"] = 0

        if lootbox_data[str(user.id)]["legendary"] != 0:
            for x in range(0, lootbox_data[str(user.id)]["legendary"]):
                amountofcash = random.randint(100000, 200000)
                amounts.append(amountofcash)
            lootbox_data[str(user.id)]["legendary"] = 0

        if lootbox_data[str(user.id)]["epic"] != 0:
            for x in range(0, lootbox_data[str(user.id)]["epic"]):
                amountofcash = random.randint(50000, 100000)
                amounts.append(amountofcash)
            lootbox_data[str(user.id)]["epic"] = 0

        if lootbox_data[str(user.id)]["rare"] != 0:
            for x in range(0, lootbox_data[str(user.id)]["rare"]):
                amountofcash = random.randint(30000, 50000)
                amounts.append(amountofcash)
            lootbox_data[str(user.id)]["rare"] = 0

        if lootbox_data[str(user.id)]["uncommon"] != 0:
            for x in range(0, lootbox_data[str(user.id)]["uncommon"]):
                amountofcash = random.randint(5000, 10000)
                amounts.append(amountofcash)
            lootbox_data[str(user.id)]["uncommon"] = 0

        if lootbox_data[str(user.id)]["common"] != 0:
            for x in range(0, lootbox_data[str(user.id)]["common"]):
                amountofcash = random.randint(2000, 5000)
                amounts.append(amountofcash)
            lootbox_data[str(user.id)]["common"] = 0

        e = discord.Embed(title=f"{ctx.author.name}'s Crates", color=discord.Color.random())
        e.add_field(name=f"{ctx.author.name}'s crate opening session!",
                    value=f"You opened {len(amounts)} crate(s) <:chest:898333946557894716> and got `{sum(amounts)} Minions™`!!! :tada:")
        await ctx.reply(embed=e)
        await update_bank(ctx.author, sum(amounts))
        with open('databases/lootboxes.json','w') as f:
            json.dump(lootbox_data, f, indent=4)
        return
        





    if type == "admin" or type.lower() == 'a':
        if amount > lootbox_data[str(user.id)]["admin"]:
            await ctx.reply("You don't have that many lootboxes!!")
            return
        amounts = []
        for x in range(0, amount):
            amountofcash = random.randint(900000, 1000000)
            amounts.append(amountofcash)

        total_cash = sum(amounts)
        e = discord.Embed(title=f"{ctx.author.name}'s Crates", color=discord.Color.random())
        e.add_field(name=f"{ctx.author.name}'s crate opening session!",
                    value=f"You opened {amount} **Admin** crate(s) <:chest:898333946557894716> and got `{total_cash} Minions™`!!! :tada:")
        await update_bank(ctx.author, total_cash)
        await ctx.reply(embed=e)
        lootbox_data[str(user.id)]["admin"] -= amount
        with open('databases/lootboxes.json', 'w') as f:
            json.dump(lootbox_data, f, indent=4)

    if type == "mythic" or type == "m":
        if amount > lootbox_data[str(user.id)]["mythic"]:
            await ctx.reply("You don't have that many lootboxes!!")
            return
        amounts = []
        for x in range(0, amount):
            amountofcash = random.randint(200000, 300000)
            amounts.append(amountofcash)

        total_cash = sum(amounts)
        e = discord.Embed(title=f"{ctx.author.name}'s Crates", color=discord.Color.random())
        e.add_field(name=f"{ctx.author.name}'s crate opening session!",
                    value=f"You opened {amount} **Mythic** crate(s) <:chest:898333946557894716> and got `{total_cash} Minions™`!!! :tada:")
        await update_bank(ctx.author, total_cash)
        await ctx.reply(embed=e)
        lootbox_data[str(user.id)]["mythic"] -= amount
        with open('databases/lootboxes.json', 'w') as f:
            json.dump(lootbox_data, f, indent=4)

    if type == "legendary" or type == "l":
        if amount > lootbox_data[str(user.id)]["legendary"]:
            await ctx.reply("You don't have that many lootboxes!!")
            return
        amounts = []
        for x in range(0, amount):
            amountofcash = random.randint(100000, 200000)
            amounts.append(amountofcash)

        total_cash = sum(amounts)
        e = discord.Embed(title=f"{ctx.author.name}'s Crates", color=discord.Color.random())
        e.add_field(name=f"{ctx.author.name}'s crate opening session!",
                    value=f"You opened {amount} **Legendary** crate(s) <:chest:898333946557894716> and got `{total_cash} Minions™`!!! :tada:")
        await update_bank(ctx.author, total_cash)
        await ctx.reply(embed=e)
        lootbox_data[str(user.id)]["legendary"] -= amount
        with open('databases/lootboxes.json', 'w') as f:
            json.dump(lootbox_data, f, indent=4)

    if type == "epic" or type == "e":
        if amount > lootbox_data[str(user.id)]["epic"]:
            await ctx.reply("You don't have that many lootboxes!!")
            return
        amounts = []
        for x in range(0, amount):
            amountofcash = random.randint(50000, 100000)
            amounts.append(amountofcash)

        total_cash = sum(amounts)
        e = discord.Embed(title=f"{ctx.author.name}'s Crates", color=discord.Color.random())
        e.add_field(name=f"{ctx.author.name}'s crate opening session!",
                    value=f"You opened {amount} **Epic** crate(s) <:chest:898333946557894716> and got `{total_cash} Minions™`!!! :tada:")
        await update_bank(ctx.author, total_cash)
        await ctx.reply(embed=e)
        lootbox_data[str(user.id)]["epic"] -= amount
        with open('databases/lootboxes.json', 'w') as f:
            json.dump(lootbox_data, f, indent=4)

    if type == "rare" or type == "r":
        if amount > lootbox_data[str(user.id)]["rare"]:
            await ctx.reply("You don't have that many lootboxes!!")
            return
        amounts = []
        for x in range(0, amount):
            amountofcash = random.randint(30000, 50000)
            amounts.append(amountofcash)

        total_cash = sum(amounts)
        e = discord.Embed(title=f"{ctx.author.name}'s Crates", color=discord.Color.random())
        e.add_field(name=f"{ctx.author.name}'s crate opening session!",
                    value=f"You opened {amount} **Rare** crate(s) <:chest:898333946557894716> and got `{total_cash} Minions™`!!! :tada:")
        await update_bank(ctx.author, total_cash)
        await ctx.reply(embed=e)
        lootbox_data[str(user.id)]["rare"] -= amount
        with open('databases/lootboxes.json', 'w') as f:
            json.dump(lootbox_data, f, indent=4)

    if type == "uncommon" or type == "u":
        if amount > lootbox_data[str(user.id)]["uncommon"]:
            await ctx.reply("You don't have that many lootboxes!!")
            return
        amounts = []
        for x in range(0, amount):
            amountofcash = random.randint(5000, 10000)
            amounts.append(amountofcash)

        total_cash = sum(amounts)
        e = discord.Embed(title=f"{ctx.author.name}'s Crates", color=discord.Color.random())
        e.add_field(name=f"{ctx.author.name}'s crate opening session!",
                    value=f"You opened {amount} **Uncommon** crate(s) <:chest:898333946557894716> and got `{total_cash} Minions™`!!! :tada:")
        await update_bank(ctx.author, total_cash)
        await ctx.reply(embed=e)
        lootbox_data[str(user.id)]["uncommon"] -= amount
        with open('databases/lootboxes.json', 'w') as f:
            json.dump(lootbox_data, f, indent=4)

    if type == "common" or type == "c":
        if amount > lootbox_data[str(user.id)]["common"]:
            await ctx.reply("You don't have that many lootboxes!!")
            return
        amounts = []
        for x in range(0, amount):
            amountofcash = random.randint(2000, 5000)
            amounts.append(amountofcash)

        total_cash = sum(amounts)
        e = discord.Embed(title=f"{ctx.author.name}'s Crates", color=discord.Color.random())
        e.add_field(name=f"{ctx.author.name}'s crate opening session!",
                    value=f"You opened {amount} **Common** crate(s) <:chest:898333946557894716> and got `{total_cash} Minions™`!!! :tada:")
        await update_bank(ctx.author, total_cash)
        await ctx.reply(embed=e)
        lootbox_data[str(user.id)]["common"] -= amount
        with open('databases/lootboxes.json', 'w') as f:
            json.dump(lootbox_data, f, indent=4)


@opencrate.error
async def crate_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.reply("Your amount can't be text or a number with a decimal!")
        return


@client.command()
async def num2text(ctx, num: int = None):
    if num is None:
        await ctx.send("Please enter a number!")
        return
    if num >= 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000:
        await ctx.send("Too big of a number!")
        return
    if len(num2words(num).capitalize()) > 4096:
        await ctx.send("Too big of a number!")
        return

    new = num2words(num).capitalize()
    e = discord.Embed(title=":capital_abcd: Numbers to words", description=f"**Input**:{num}\n\n**Output**:{new}",
                      color=discord.Color.random())
    e.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
    await ctx.send(embed=e)


@client.command()
async def reverse(ctx, *, msg=None):
    if msg is None:
        await ctx.send("Please enter a message!")
        return
    t_rev = msg[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
    await ctx.send(f"**🔁 Text ==> txeT | {ctx.author}**\n```{t_rev}```")


@client.command()
async def dogfact(ctx):
    async with aiohttp.ClientSession() as ses:
        async with ses.get('http://some-random-api.ml/facts/dog') as r:
            if r.status in range(200, 299):
                data = await r.json()
                fact = data['fact']
                em = discord.Embed(title='Dog Fact', description=f'{fact}', color=discord.Color.random())
                await ctx.send(embed=em)
                await ses.close()
            else:
                await ctx.send("Error when making request...")
                await ses.close()


@client.command()
async def jail(ctx, user: discord.Member = None):
    loading = await ctx.send("<a:loading:898340114164490261>")
    if user is None:
        user = ctx.author
    async with aiohttp.ClientSession() as trigSession:
        async with trigSession.get(
                f'https://some-random-api.ml/canvas/jail?avatar={user.display_avatar.with_size(1024)}') as trigImg:  # get users avatar as png with 1024 size
            if trigImg.status in range(200, 299):
                imageData = BytesIO(await trigImg.read())  # read the image/bytes
                await trigSession.close()  # closing the session and;
                await ctx.reply(file=discord.File(imageData, 'image.png'))
                await loading.delete()
            else:
                await ctx.send("Error when making request...")
                await trigSession.close()


@client.command(aliases=["trigger"])
async def triggered(ctx, user: discord.Member = None):
    loading = await ctx.send("<a:loading:898340114164490261>")
    if user is None:
        user = ctx.author
    async with aiohttp.ClientSession() as trigSession:
        async with trigSession.get(
                f'https://some-random-api.ml/canvas/triggered?avatar={user.display_avatar.with_size(1024)}') as trigImg:
            if trigImg.status in range(200, 299):
                imageData = BytesIO(await trigImg.read())  # read the image/bytes
                await trigSession.close()  # closing the session and;
                await ctx.reply(file=discord.File(imageData, 'triggered.gif'))
                await loading.delete()
            else:
                await ctx.send("Error when making request...")
                await trigSession.close()


@client.command()
async def joke(ctx):
    async with aiohttp.ClientSession() as ses:
        async with ses.get('https://some-random-api.ml/joke') as r:
            if r.status in range(200, 299):
                data = await r.json()
                fact = data['joke']
                em = discord.Embed(title='Joke', description=f'{fact}', color=discord.Color.random())
                await ctx.send(embed=em)
                await ses.close()
            else:
                await ctx.send("Error when making request...")
                await ses.close()



@client.event  # This event runs whenever a user updates: status, game playing, avatar, nickname or role
async def on_member_update(before, after):
    n = after.nick
    try:
        if n != before.nick:
            if n.lower().replace(" ","").count("gru") > 0:
                await after.edit(nick="NO ONE ELSE CAN BE GRU YOU BOZO")
            if n.lower().count("akshar") or n.lower().count("fuck") or n.lower().count("bitch") or n.lower().count(
                    "ass") or n.lower().count("f3ck") or n.lower().count("a s s") or n.lower().count(
                    "f u c k") or n.lower().count("b i t c h") or n.lower().count("f2ck") > 0:  # If username contains tim
                last = before.nick
                if last:  # If they had a username before change it back to that
                    await after.edit(nick="NICKNAME NOT ALLOWED")
                else:  # Otherwise set it to "NO STOP THAT"
                    await after.edit(nick="NO STOP THAT")
    except Exception as e:
        print(e)


@client.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        pass

    else:
        with open('databases/reactrole.json','r') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name or x['emoji'] == f"<:{payload.emoji.name}:{payload.emoji.id}>" or x['emoji'] == f"<a:{payload.emoji.name}:{payload.emoji.id}>":
                    role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])
                    if role:
                        await payload.member.add_roles(role)
                    else:
                        del x


@client.event
async def on_raw_reaction_remove(payload):
    with open('databases/reactrole.json','r') as react_file:
        data = json.load(react_file)
        for x in data:
            if x['emoji'] == payload.emoji.name or x['emoji'] == f"<:{payload.emoji.name}:{payload.emoji.id}>" or x['emoji'] == f"<a:{payload.emoji.name}:{payload.emoji.id}>":
                role = discord.utils.get(client.get_guild(
                    payload.guild_id).roles, id=x['role_id'])

                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)


@client.command()
@commands.has_permissions(manage_roles=True)
async def reactrole(ctx, emoji=None, role: discord.Role = None, *, message=None):
    with open('databases/prefixes.json') as f:
        prefixes = json.load(f)
    prefix = prefixes[str(ctx.guild.id)]
    
    if emoji == None or role == None or message == None and ctx.author.id == ctx.guild.owner_id:
        return await ctx.send(f"Please enter an emoji role or message! The way you make a reaction role is `{prefix}reactrole <emoji> <role> <message>`.")
        
    if role.position >= ctx.me.top_role.position:
        return await ctx.send("I can't make a reaction role for that role because it is above or is my top role!")

    emb = discord.Embed(description=message, color=discord.Color.random(), title="New Reaction Role!")
    emb.set_footer(text=f"Reacting will give you the {role.name} role!")
    try:
        await ctx.message.delete()
    except:
        pass
    msg = await ctx.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('databases/reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name,
                          'role_id': role.id,
                          'emoji': emoji,
                          'message_id': msg.id}

        data.append(new_react_role)

    with open('databases/reactrole.json', 'w') as f:
        json.dump(data, f, indent=4)


@client.event
async def on_raw_message_delete(payload):
    with open('databases/reactrole.json', 'r') as f:
        reaction_roles = json.load(f)
    msgs = [reaction_role_id["message_id"] for reaction_role_id in reaction_roles]
    if payload.message_id not in msgs:
        return
    else:
        for i in range(len(reaction_roles)):
            if reaction_roles[i]["message_id"] == payload.message_id:
                del reaction_roles[i]
                break
        with open('databases/reactrole.json', 'w') as f:
            json.dump(reaction_roles, f, indent=4)


async def dump_mainbank_data(data):
    with open('databases/mainbank.json', 'w') as f:
        json.dump(data, f, indent=4)


async def dump_level_data(data):
    with open('databases/levels.json', 'w') as f:
        json.dump(data, f, indent=4)


async def dump_lootbox_data(data):
    with open('databases/lootboxes.json', 'w') as f:
        json.dump(data, f, indent=4)


async def dump_job_data(data):
    with open('databases/jobs.json', 'w') as f:
        json.dump(data, f, indent=4)


@client.command(aliases=["gender"])
async def genderify(ctx, *, name=None):
    if name is None:
        await ctx.send("Please enter a name!")
        return

    genderify = await http.get(f"https://api.genderize.io?name={name.lower()}", res_method="json")
    if str(genderify["gender"]) == "None":
        return await ctx.send("I don't have a gender for that name!")

    e = discord.Embed(title="Genderify", description="I will guess the gender of a name!", color=discord.Color.random())
    e.add_field(name="Name", value=genderify["name"].capitalize(), inline=False)
    e.add_field(name="Gender", value=genderify["gender"].capitalize(), inline=False)
    e.add_field(name="Probability", value=f"{genderify['probability'] * 100}%", inline=False)
    e.add_field(name="Count", value=genderify["count"])

    await ctx.send("I have guessed the gender!!", embed=e)


@client.event
async def on_raw_bulk_message_delete(payload):
    deleted_msg_ids = [id for id in payload.message_ids]
    with open('databases/reactrole.json', 'r') as f:
        roles = json.load(f)
    reaction_role_ids = [id["message_id"] for id in roles]
    for id in deleted_msg_ids:
        for reactrole_id in reaction_role_ids:
            if id == reactrole_id:
                for i in roles:
                    if i["message_id"] == reactrole_id:
                        roles.remove(i)
                    with open('databases/reactrole.json', 'w') as f:
                        json.dump(roles, f, indent=4)



@client.command()
async def spam(ctx):
    await ctx.send("Type as many characters you can in 30 seconds! I will tell you when to send the message for it to be counted.")
    await asyncio.sleep(1)
    countdown = await ctx.send("3")
    await asyncio.sleep(1)
    await countdown.edit("2")
    await asyncio.sleep(1)
    await countdown.edit("1")
    await asyncio.sleep(1)
    await countdown.edit("TYPE!!!!")
    new_countdown = await ctx.send("30")
    for num in range(30,-1,-1):
        await new_countdown.edit(f"{num}")
        await asyncio.sleep(1)
    await ctx.send("Times up!")
    await ctx.send("Please send you message within 3 seconds or your run is disqualified!")
    user_msg = None
    try:
        user_msg = await client.wait_for('message',timeout=3,check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
    except asyncio.TimeoutError:
        return await ctx.send("You ran out of time to submit your message! :(")
    if len(user_msg.content) >= 900:
        return await ctx.send("I know you didn't type all of this in a legit way...")
    await ctx.send(f"Your message was **{len(user_msg.content)}** characters long!! :tada: :tada:")


@client.command()
async def eadd(ctx, url: str=None, *, name=None):
    guild = ctx.guild
    if ctx.author.id == ctx.guild.owner_id:
        if name == None:
            return await ctx.send("Please enter a name for the emoji!")
        if url == None:
            return await ctx.send("Please enter the url of the emoji you want to add to your server!")
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url) as r:
                try:
                    imgOrGif = BytesIO(await r.read())
                    bValue = imgOrGif.getvalue()
                    if r.status in range(200, 299):
                        emoji = await guild.create_custom_emoji(image=bValue, name=name)
                        await ctx.send(":white_check_mark: Emoji created!")
                        await ses.close()
                    else:
                        await ctx.send(f"This id not work -_- | {r.status}")
                except discord.HTTPException:
                    await ctx.send("The file is too thicc :(")
    else:
        await ctx.send("Only server owners can create custom emojis!")



@client.command()
async def sqrt(ctx, expression):
    try:
        return await ctx.send(f"The square root \u221A of the expression/number {expression} is\n{math.sqrt(float(calculator(expression)))}")
    except:
        return await ctx.send("An error occurred :( .")


@client.command()
@commands.is_owner()
async def exit(ctx):
    await ctx.send("Logging out now...")
    await asyncio.sleep(1)
    await client.close()



@client.command()
async def gay(ctx, user: discord.Member=None):
    if user == None:
        user = ctx.author
    if user.id == 717512097725939795 and ctx.author != user:
        await ctx.send(f"{ctx.author.mention} he's not gay, you are.")
        return
    loading = await ctx.send("<a:loading:898340114164490261>")
    async with aiohttp.ClientSession() as gaySession:
        async with gaySession.get(f'https://some-random-api.ml/canvas/gay?avatar={user.display_avatar.url}') as gayImg:
            if gayImg.status in range(200,299): # get users avatar as png with 1024 size
                imageData = BytesIO(await gayImg.read()) # read the image/bytes
                await gaySession.close() # closing the session and;
                await ctx.reply(file=discord.File(imageData, 'gay.png')) # sending the file
                await loading.delete()
            else:
                await ctx.send("An error occurred while fetching from the api! :(")





async def give_animal(user, animal):
    animal_name = animal["name"].lower()
    users = await get_bank_data()

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == animal_name:
                old_amt = thing["amount"]
                new_amt = old_amt + 1
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item": animal_name, "amount": 1}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item": animal_name, "amount": 1}
        users[str(user.id)]["bag"] = [obj]

    with open("databases/mainbank.json", "w") as f:
        json.dump(users, f, indent=4)

    return [True, "Worked"]

@client.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def hunt(ctx):
    vowels = ["a","e","i","o","u"]
    users = await get_bank_data()
    with open('databases/prefixes.json','r') as f:
        prefixes = json.load(f)
    prefix = prefixes[str(ctx.guild.id)]
    user = ctx.author
    has_weapon = False
    for item in users[str(user.id)]["bag"]:
        if item["item"] == "hunting sniper":
            has_weapon = True
            break
        else:
            has_weapon = False
    if not has_weapon:
        hunt.reset_cooldown(ctx)
        return await ctx.send(f"You don't have a hunting sniper! Buy one by doing `{prefix}buy hunting sniper`!")

    animal = random.choice(animal_shop[0]+animal_shop[2])
    if animal["name"][0].lower() in vowels: 
        await ctx.send(f"You went hunting in the woods and managed to kill an **{animal['name']}**!!")
    else:
        await ctx.send(f"You went hunting in the woods and managed to kill a **{animal['name']}**!!")
    await give_animal(user, animal)



@client.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def fish(ctx):
    vowels = ["a","e","i","o","u"]
    special = ["garbage", "donald duck","nemo"]
    users = await get_bank_data()
    with open('databases/prefixes.json','r') as f:
        prefixes = json.load(f)
    prefix = prefixes[str(ctx.guild.id)]
    user = ctx.author
    has_weapon = False
    for item in users[str(user.id)]["bag"]:
        if item["item"] == "fishing rod":
            has_weapon = True
            break
        else:
            has_weapon = False
    if not has_weapon:
        fish.reset_cooldown(ctx)
        return await ctx.send(f"You don't have a fishing rod! Buy one by doing `{prefix}buy fishing rod`!")

    animal = random.choice(animal_shop[1])
    if animal["name"][0].lower() in vowels:
        await ctx.send(f"You went fishing in the ocean and managed to catch an **{animal['name']}**!!")
    elif animal["name"].lower() in special:
        await ctx.send(f"You went fishing in the ocean and managed to catch **{animal['name']}**!!")
    else:
        await ctx.send(f"You went fishing in the ocean and managed to catch a **{animal['name']}**!!")
    await give_animal(user, animal)


@client.command()
async def gayrate(ctx, user: discord.Member):
    if user.id == 457330033875353601:
        percent = 4757458784575999999999977897878976457478395758345738957348934578945378934578934578984374547573347878347534875357843578458734785378378547354573894537845378
    elif user.id == 717512097725939795:
        percent = 0
    else:
        percent = random.randint(0,100)
    e = discord.Embed(title="gay r8t machine",color=discord.Color.random(),description=f"{user.name} is {percent}% gay :gay_pride_flag:")
    await ctx.send(embed=e)



@client.command()
async def credits(ctx):
    e = discord.Embed(title="Credits",description="These are all the things that made this bot!",color=discord.Color.random())
    atharv = await client.fetch_user(859310142633803806)
    akshar = await client.fetch_user(717512097725939795)
    e.add_field(name = 'The Creator Of Basically Everything In This Bot', value = akshar,inline=False)
    e.add_field(name = "The Playing Cycle", value=atharv,inline=False)
    e.add_field(name = "Creature ideas for when hunting or fishing", value=atharv,inline=False)
    e.add_field(name="Starter Code",value="https://github.com/AyushSehrawat/Economy-Bot")
    await ctx.reply(embed=e)


@client.command()
@commands.has_permissions(manage_guild=True)
async def config(ctx):
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 717512097725939795:
        with open('databases/server_configs.json','r') as f:
            configs = json.load(f)

        role = ctx.guild.get_role(configs[str(ctx.guild.id)]["giveaway_role"])
        e = discord.Embed(title="Your Server Configurations",color=discord.Color.random())
        if role != None:
            e.add_field(name="Giveaway Role",value=role.mention)
        else:
            e.add_field(name="Giveaway Role",value=role)
        e.add_field(name="Leveling",value=configs[str(ctx.guild.id)]['levels'])
        await ctx.reply(embed=e)
        await asyncio.sleep(1)
        await ctx.send("Would you like to change the config? y/n")
        change_config = None
        try:
            change_config = await client.wait_for('message',timeout=20, check=lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
        except asyncio.TimeoutError:
            return
        change_config = change_config.content
        if change_config.lower() == "n":
            return await ctx.send("Okay! I won't change anything.")
        else:
            await ctx.send("Choose a configuration to change:")



    else:
        return await ctx.send("Only the owner of the server can see this!")

    

            # Main code ends
####################################################################
####################################################################


for filename in os.listdir("cogs"):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        
keep_alive()
token = os.environ["discord_bot_token"]
client.run(token)
