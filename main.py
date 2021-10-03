import re
import aiohttp
import nextcord as discord
from nextcord.ext import commands, tasks
from nextcord.utils import get
import asyncio
from typing import List
import datetime
from itertools import cycle
import os
import json
import random
from PIL import Image
from io import BytesIO
from googleapiclient.discovery import build
import urllib.parse, urllib.request
import bot_token
import string
import base64
from num2words import num2words
import alexflipnote
from cogs.utils import http

alex_api = alexflipnote.Client("JKY6JzdiMO5xBqkncoONDdvrlQj7LVaF0N5IFae2")
os.chdir("/Users/akshardesai/PycharmProjects/Akshar's_projects_and_games/bot/Economy-Bot/Economy_bot_code")

api_key = "AIzaSyAhNZnU6pStK8eYcm83IeQAR_OEdhjJURw"

def get_prefix(client, message):
    with open("databases/prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())
client.remove_command("help")


@client.event
async def on_guild_join(guild):
    with open("databases/prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = ','

    with open('databases/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open("databases/prefixes.json", "r") as f:
        prefixes = json.load(f)
    del prefixes[str(guild.id)]
    with open('databases/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    with open('databases/levels.json', 'r') as f:
        levels = json.load(f)
    del levels[str(guild.id)]
    with open('databases/levels.json', 'w') as f:
        json.dump(levels, f, indent=4)


@client.command()
async def avatar(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author

    member_display_avatar_pic = member.display_avatar

    await ctx.send(member_display_avatar_pic)
    if member == client.user:
        await ctx.send("HEEEY THAT'S ME. I'M FAMOUS POOOOGGGGGG")


@client.command()
async def change_prefix(ctx, prefix=None):
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
    ['Try ,help', 'Prefix - ,', 'Minecraft', 'PoKeMon', 'Try @GRU BOT'])

client.lava_nodes = [
    {
        'host': '52.52.235.172',
        'port': 2333,
        'rest_uri': f'http://52.52.235.172:2333/',
        'password': 'youshallnotpass',
        'identifier': 'MAIN',
        'region': 'US'
    }

]


@client.event
async def on_ready():
    change_status.start()
    print()
    print("Connected to {0.user}".format(client))
    client.load_extension("jishaku")
    while True:
        await asyncio.sleep(15)
        with open('databases/spam_detextion.txt', "r+") as file:
            file.truncate(0)


@tasks.loop(seconds=4)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_member_join(member):
    if member.bot:
        return
    else:
        await member.create_dm()
        await member.dm_channel.send(f'''Hi {member.name}, welcome to Akshar's Discord server!''')


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
            {"name": "2x booster", "price": 50000, "description": "Get a 2x money booster **__Permanent__**"},
            {"name": "Ferrari", "price": 99999, "description": "Sports Car"},
            {"name": "5x booster", "price": 400000, "description": "Get a 5x money booster **__Permanent__**"},
            {"name": "Quantum computer", "price": 470000, "description": "ULTRA FAST COMPUTER"},
            {"name": "Gru trusts me role", "price": 500000,
             "description": "Allows you to see a exclusive channel for users with this role only!"},
            {"name": "Lamborghini", "price": 1000000, "description": "Ultra cool sports car"}
            ]


@client.command(aliases=['bal'])
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()
    jobs = await get_job_data()
    job_name = jobs[str(user.id)]["job"]["name"]
    job_pay = jobs[str(user.id)]["job"]["pay"]

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]
    booster = users[str(user.id)]["booster"]

    em = discord.Embed(title=f"{ctx.author.display_name}'s Balance", color=discord.Color.red())
    em.add_field(name="Wallet Balance", value=wallet_amt)
    em.add_field(name='Bank Balance', value=bank_amt)
    em.add_field(name='Job', value=job_name)
    em.add_field(name='Job salary', value=job_pay)
    if booster != 1:
        em.add_field(name='Booster', value=f'{booster}x')
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
        message = f'"Oh you beggar take `{earnings * booster} Gru coins`"'
        beg_embed = discord.Embed(description=message, color=discord.Color.random())
        beg_embed.set_author(name=person)
        if booster != 1:
            beg_embed.set_footer(
                text=f"You earned {earnings * (booster - 1)} extra Gru coins since you had a {booster}x booster!(Original amount:{earnings})")
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
    if isinstance(error, commands.CommandNotFound):
        with open('databases/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.guild.id)]
        await ctx.send(f"Unknown command.Try {prefix}help for a list of commands")
        return
    if isinstance(error, commands.CommandOnCooldown):
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
    if isinstance(error, commands.RoleNotFound):
        await ctx.send(":x: Role not found.")
        return
    if isinstance(error, commands.MemberNotFound):
        await ctx.send(":x: No member found with that name.")
        return
    if isinstance(error, commands.MissingRole):
        await ctx.send(":x: You are not allowed to do this!")
        return
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send(":x: You are not allowed to do this!")
        return
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(
            ":x: Missing arguments! check ,help if you need to know about how to use the command. Or an error has occured :(.")
        await modlog.send(f'Error found   {error}')
        return


facts = ["Gru likes his cup more than anything", "Gru will never get a wife", "Gru has 100iq", "Gru does not like kids",
         "Gru only refuels his ship once a week", "Gru's favorite minion is bert"]


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
        fact = random.choice(facts)

        fact_sended = await ctx.send(f'**{fact}**')
        await asyncio.sleep(2)
        await fact_sended.delete()
        await asyncio.sleep(0.5)
        await ctx.send("Now, retype the sentence!")
        msg = None
        try:
            msg = await client.wait_for('message', check=check, timeout=20)
        except asyncio.TimeoutError:
            work_em = discord.Embed(title="Terrible job!",
                                    description=f"You were given `{int(work_amt / 3):,} Gru coins` for 1/3 of an hour of pay",
                                    color=discord.Color.random())
            work_em.set_footer(text=f'Working as a {work_name}')
            await update_bank(ctx.author, int(work_amt / 3))
            await ctx.reply(embed=work_em)
            return
        if msg.content.lower() == fact.lower():
            promote_pay = random.randint(0, 8)
            promote_job = random.randint(0, 10)
            work_em = discord.Embed(title="Great job!",
                                    description=f"You were given `{work_amt:,} Gru coins` for an hour of pay",
                                    color=discord.Color.random())
            work_em.set_footer(text=f'Working as a {work_name}')
            await update_bank(ctx.author, work_amt)
            await ctx.reply(embed=work_em)

            if promote_job == 10 and work_name != "God Of Money" and work_name != "Gru Super Code Compiler":
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
                jobpays = {"Gru Gadgets Maker": 9000, "Gru Gadgets Tester": 12000, "Minion Refiner": 16000,
                           "Super Minion Refiner": 22000, "Minion Gadget Manager": 29000, "Gru Ship Mechanic": 35000,
                           "Gru Ship Pilot": 41000, "Minion Costume Maker": 45000, "Gru Assistant Hacker": 55000,
                           "Gru Hacker": 60000, "Gru Senior Hacker": 67000, "Gru's Barber": 69420,
                           "Gru Gadget Programmer": 79000, "Gru Code Compiler": 90000, "Gru Super Programmer": 102000,
                           "Gru Super Code Compiler": 117000}
                new_job_pay = jobpays[new_job_name]
                if work_amt > jobpays[work_name]:
                    new_job_pay += work_amt - jobpays[work_name]
                await ctx.send(
                    f"You were doing so good that your manager has **PROMOTED** you to a {new_job_name}! You now make `{new_job_pay} Gru coins` instead of `{work_amt} Gru coins`! :tada: :tada:")
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
                    f"Since you are doing really well in your work, your manager has decided to increase your pay by `{int(pay_increase):,} Gru coins`!! :tada: :tada:")
                jobs[str(user.id)]["job"]["pay"] = work_amt + int(pay_increase)
                with open('databases/jobs.json', 'w') as f:
                    json.dump(jobs, f, indent=4)
                return
        else:
            work_em = discord.Embed(title="Terrible job!", description=f"You were given `{int(work_amt / 3)} Gru coins` for 1/3 of an hour of pay", color=discord.Color.random())
            work_em.set_footer(text=f'Working as a {work_name.capitalize()}')
            await ctx.reply(embed=work_em)
            await update_bank(ctx.author, int(work_amt / 3))
            return


@client.command()
async def jobs(ctx):
    await ctx.send(
        f"{ctx.author.mention} The jobs in Gru enterprises™ are\n\nGru Gadgets Maker | 9,000\nGru Gadgets Tester | 12,000\nMinion Refiner | 16,000\nSuper Minion Refiner | 22,000\nMinion Gadget Manager | 29,000\nGru Ship Mechanic | 35,000\nGru Ship Pilot | 41,000\nMinion Costume Maker | 45,000\nGru Assistant Hacker | 55,000\nGru Hacker | 60,000\nGru Senior Hacker | 67,000\nGru's Barber | 69,420\nGru Gadget Programmer | 79,000\nGru Code Compiler | 90,000\nGru Super Programmer | 102,000\nGru Super Code Compiler | 117,000")


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


@client.command()
async def commands_amt(ctx):
    await ctx.reply(f"I have {len(client.commands)} commands!")


@client.command(aliases=['with'])
async def withdraw(ctx, amount=None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)
    if amount == 'max':
        amount = bal[1]

    amount = int(amount)

    if amount > bal[1]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1 * amount, 'bank')
    await ctx.send(f':white_check_mark: {ctx.author.mention} You withdrew {amount} coins')


@client.command(aliases=['dep'])
async def deposit(ctx, amount=None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)
    if amount == 'max':
        amount = bal[0]

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author, -1 * amount)
    await update_bank(ctx.author, amount, 'bank')
    await ctx.send(f':white_check_mark: {ctx.author.mention} You deposited {amount} coins')


@client.command()
async def send(ctx, member: discord.Member, amount=None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)
    if amount == 'all':
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
        await ctx.send("Please enter the amount")
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
        await ctx.send(f'JACKPOT!!! You won {3 * amount} Gru coins!!! :tada: :D {ctx.author.mention}')

    elif final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
        await update_bank(ctx.author, 2 * amount)
        await ctx.send(f'You won {2 * amount} Gru coins :) {ctx.author.mention}')
    else:
        await update_bank(ctx.author, -1 * amount)
        await ctx.send(f'You lose {1 * amount} Gru coins :( {ctx.author.mention}')


@client.command(aliases=["store"])
async def shop(ctx):
    em = discord.Embed(title="Shop", color=discord.Color.random())

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name=name, value=f"${price} | {desc}")

    await ctx.send(embed=em)


@client.command()
async def buy(ctx, amount=1, *, item):
    users = await get_bank_data()
    item = item.lower()
    if item == "2x booster":
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
        if users[str(ctx.author.id)]["booster"] < 5:
            if users[str(ctx.author.id)]["wallet"] >= 400000:
                users[str(ctx.author.id)]["wallet"] -= 400000
                users[str(ctx.author.id)]["booster"] = 5
                await ctx.send(":white_check_mark: You now have a booster for 5x the money!")
                with open('databases/mainbank.json', 'w') as f:
                    json.dump(users, f)
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
                    json.dump(users, f)
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
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return

    if item == 'pc':
        item = item.upper()
    else:
        item = item.capitalize()

    if item.lower() == 'watch' and amount > 1:
        item = item + "es"
    if amount > 1 and item.lower() != 'watches':
        item = item + "s"

    await ctx.send(f":white_check_mark: You just bought {amount} {item}")


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
    for item in bag:
        name = item["item"]
        name = name.capitalize()
        if name == 'Pc':
            name = name.upper()
        amount = item["amount"]
        em.add_field(name=name, value=amount)

    await ctx.send(embed=em)


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

    return [True, "Worked"]


@client.command()
async def sell(ctx, amount=1, *, item):
    await open_account(ctx.author)

    res = await sell_this(ctx.author, item, amount)
    if item == 'pc':
        item = item.upper()
    else:
        item = item.capitalize()
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
    if item.lower() == 'watch' and amount > 1:
        item = item + "es"
    if amount > 1 and item.lower() != 'watches':
        item = item + "s"

    await ctx.send(f":white_check_mark: You just sold {amount} {item}.")


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

    return [True, "Worked"]


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
        jobs[str(user.id)] = {}
        jobs[str(user.id)]["job"] = {}
        jobs[str(user.id)]["job"]["name"] = 'None'
        jobs[str(user.id)]["job"]["pay"] = 0
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

    users[str(user.id)][mode] += change

    with open('databases/mainbank.json', 'w') as f:
        json.dump(users, f, indent=4)
    bal = users[str(user.id)]['wallet'], users[str(user.id)]['bank']
    return bal


@client.command(pass_context=True, aliases=['rguser', 'rgu'])
@commands.has_any_role("Admin", "Owner", "Sr.Admin")
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
@commands.has_any_role("Owner")
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
@commands.has_any_role("Owner")
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
            await ctx.send(f":white_check_mark: Gave {amount} Gru coins to user {user.display_name}'s {area}!")
            if area == 'wallet':
                await update_bank(user, amount, 'wallet')
            elif area == 'bank':
                await update_bank(user, amount, 'bank')


@client.command()
@commands.has_any_role("Owner")
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
            await ctx.send(f":white_check_mark: Took {amount} Gru coins from user {user.display_name}'s {area}!")
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
        em.add_field(name='Wallet', value=f"{wallet_amt} Gru coins")
        em.add_field(name='Bank', value=f"{bank_amt} Gru coins")
        em.add_field(name='Job', value=job_name)
        em.add_field(name='Job salary', value=f'{job_pay} Gru coins per hour')
        if booster_amt != 1:
            em.add_field(name='Booster', value=f'{booster_amt}x')
        await ctx.send(embed=em)


@client.command(aliases=['scn'])
@commands.has_any_role("Admin", "Owner", "Sr.Admin", "Moderator")
async def set_channel_name(ctx, channel: discord.TextChannel, *, new_name):
    await channel.edit(name=new_name)
    await ctx.send(":white_check_mark: Done!")


@client.command(aliases=['sb'])
@commands.has_any_role("Owner")
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
@commands.has_any_role("Admin", "Owner", "Sr.Admin", "Moderator")
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
@commands.has_any_role("Admin", "Owner", "Sr.Admin", "Moderator")
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
        color=discord.Colour.dark_blue()
    )
    embed.set_footer(text='Our Community')
    await ctx.send(embed=embed)
    await ctx.message.delete()


amount = []


@client.command(aliases=["lb"])
async def leaderboard(ctx, x=10):
    users = await get_bank_data()
    if len(users) < x:
        x = len(users)
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]

        leader_board[total_amount] = name
        amount.append(total_amount)
        total.append(total_amount)

    total = sorted(total, reverse=True)

    em = discord.Embed(title=f"Top {x} Richest People",
                       description="This is decided on the basis of raw money in the bank and wallet",
                       color=discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]

        member = await client.fetch_user(id_)
        name = member.name
        em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed=em)


q_list = [
    '''Why do you want to become staff?''',
    'Do you have any previous experience?',
    'Will you use your role to gain advantages in ANY of the bots in this server?'
]

a_list = []


class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("I will submit the application!")
        self.value = "Confirmed"
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Cancelling")
        self.value = "Declined"
        self.stop()


class Application_Options(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("I will send them a message that they were rejected")
        await asyncio.sleep(1)
        await interaction.delete_original_message()
        self.value = "Denied"
        self.stop()

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = "Accepted"
        self.username = interaction.user.id
        self.stop()


class Role_Options(discord.ui.View):
    def __init__(self, username):
        super().__init__()
        self.value = None
        self.username = username

    @discord.ui.button(label="Moderator", style=discord.ButtonStyle.danger)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.username == interaction.user.id:
            await interaction.response.send_message("I will send them a message and give them the Moderator rank!",
                                                    ephemeral=True)
            await asyncio.sleep(1)
            await interaction.delete_original_message()
            self.value = "Moderator"
            self.stop()

    @discord.ui.button(label="Admin", style=discord.ButtonStyle.blurple)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.username == interaction.user.id:
            await interaction.response.send_message("I will send them a message and give them the Admin rank!",
                                                    ephemeral=True)
            await asyncio.sleep(1)
            await interaction.delete_original_message()
            self.value = "Admin"
            self.stop()


active_applications = []


@client.command(aliases=['apply'])
async def staff_application(ctx):
    if ctx.guild.id != 762829356812206090:
        return await ctx.send("This command is not available in your server!")
    mod = get(ctx.guild.roles, name="Moderator")
    admin = get(ctx.guild.roles, name="Admin")
    sr_admin = get(ctx.guild.roles, name="Sr.Admin")
    if mod in ctx.author.roles or admin in ctx.author.roles or sr_admin in ctx.author.roles and ctx.author.id != 717512097725939795:
        await ctx.send("You are not allowed to apply!")
        return
    if str(ctx.author.id) in active_applications:
        await ctx.reply("You already have an application open!")
        return
    await ctx.message.delete()
    active_applications.append(str(ctx.author.id))

    submit_actions = Confirm()
    accept_or_deny = Application_Options()

    a_list = []
    submit_channel = client.get_channel(877974552137834526)
    channel = await ctx.author.create_dm()

    def check(m):
        return m.content is not None and m.channel == channel and m.content != question

    for question in q_list:
        await asyncio.sleep(0.6)
        await channel.send(question)
        msg = await client.wait_for('message', check=check)
        a_list.append(msg.content)

    submit_wait = True
    while submit_wait:
        await channel.send(
            'End of questions - press the submit button to submit the application, or press the cancel button to not send the application.',
            view=submit_actions)
        await submit_actions.wait()
        if submit_actions.value == 'Confirmed':
            submit_wait = False
            answers = "\n".join(f'{a}. {b}' for a, b in enumerate(a_list, 1))
            submit_msg = f'Application from {msg.author} \nThe answers are:\n{answers}'
            message = "\n".join(q_list)
            p = await submit_channel.send(f'The questions were\n{message}')
            delta = datetime.datetime.now()
            e = discord.Embed(title='Answers', description=submit_msg, timestamp=delta, color=discord.Color.blue())
            e.add_field(name='Actions', value='What would you like me to do?')
            await p.edit(embed=e, view=accept_or_deny)
            await accept_or_deny.wait()
            if accept_or_deny.value == 'Accepted':
                role_options = Role_Options(accept_or_deny.username)
                await p.edit(content='What role would you like to give them?', view=role_options)
                await role_options.wait()
                if role_options.value == 'Admin':
                    member = ctx.author
                    role = get(member.guild.roles, name="Admin")
                    await ctx.author.add_roles(role)
                    channl = await member.create_dm()
                    await channl.send(
                        "Congratulations!You have received the Admin rank in the server Private server for Akshar's friends!")
                    await asyncio.sleep(1)
                    await p.delete()
                    active_applications.remove(str(ctx.author.id))
                    break
                elif role_options.value == "Moderator":
                    member = ctx.author
                    role = get(member.guild.roles, name="Moderator")
                    await ctx.author.add_roles(role)
                    channl = await member.create_dm()
                    await channl.send(
                        "Congratulations!You have received the Moderator rank in the server Private server for Akshar's friends!")
                    await asyncio.sleep(1)
                    await p.delete()
                    active_applications.remove(str(ctx.author.id))
                    break
            elif accept_or_deny.value == "Denied":
                member = ctx.author
                channl = await member.create_dm()
                await channl.send(
                    "I'm sorry, but you were rejected for staff in the server Private server for Akshar's friends.")
                await asyncio.sleep(1)
                await p.delete()
                active_applications.remove(str(ctx.author.id))
                break
        elif submit_actions.value == 'Declined':
            active_applications.remove(str(ctx.author.id))
            return


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
    counter = 0
    with open('databases/spam_detextion.txt', "r+") as file:
        if not message.author.bot:
            for lines in file:
                if lines.strip("\n") == str(message.author.id):
                    counter += 1

        file.writelines(f"{str(message.author.id)}\n")
        if counter > 5 and str(message.author.id) != "717512097725939795" and message.author != client.user:
            await message.channel.send("Please stop spamming! Or you will get muted by a staff member")

    try:
        if message.mentions[0] == client.user and message.content == '<@!874328552965820416>':
            with open("databases/prefixes.json", "r") as f:
                prefixes = json.load(f)

            pre = prefixes[str(message.guild.id)]
            await message.channel.send(f"My prefix for this server is `{pre}`")
    except:
        pass
    try:
        if not message.author.bot:
            with open('databases/levels.json', 'r') as f:
                levels = json.load(f)
            await update_data(levels, message.author, message.guild)
            await add_experience(levels, message.author, 5, message.guild)
            await level_up(levels, message.author, message.channel, message.guild)

            with open('databases/levels.json', 'w') as f:
                json.dump(levels, f, indent=4)
        await client.process_commands(message)
    except:
        return


async def update_data(users, user, server):
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


async def add_experience(users, user, exp, server):
    users[str(user.guild.id)][str(user.id)]['experience'] += exp


async def level_up(users, user, channel, server):
    experience = users[str(user.guild.id)][str(user.id)]['experience']
    lvl_start = users[str(user.guild.id)][str(user.id)]['level']
    lvl_end = int(experience ** (1 / 4))
    if str(user.guild.id) != '757383943116030074':
        if lvl_start < lvl_end:
            await channel.send('Congratulations! {} has leveled up to **Level {}** and has a total of **{} xp**! :tada: :tada:'.format(user.mention, lvl_end, experience))
            users[str(user.guild.id)][str(user.id)]['level'] = lvl_end


@client.command(aliases=['rank', 'lvl'])
async def level(ctx, member: discord.Member = None):
    if not member:

        user = ctx.message.author
        with open('databases/levels.json', 'r') as f:
            users = json.load(f)

            lvl = users[str(ctx.guild.id)][str(user.id)]['level']
            exp = users[str(ctx.guild.id)][str(user.id)]['experience']

        embed = discord.Embed(title='Level {}'.format(lvl), description=f"{exp} XP ", color=discord.Color.green())
        embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
        await ctx.send(embed=embed)
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
        embed = discord.Embed(title='Level {}'.format(lvl), description=f"{exp} XP", color=discord.Color.green())
        embed.set_author(name=member, icon_url=member.display_avatar)

        await ctx.send(embed=embed)


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
            await ctx.send("You lost. Thanks for playing!")
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
@commands.has_any_role("Admin", "Owner", "Sr.Admin", "Moderator")
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
@commands.has_any_role("Admin", "Owner", "Sr.Admin", "Moderator")
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
@commands.has_any_role("Owner")
async def gcreate(ctx, time=None, *, prize=None):
    giveaway_role = get(ctx.author.guild.roles, name="Giveaway Ping")
    if time == None:
        return await ctx.send('Please include a time!')
    elif prize == None:
        return await ctx.send('Please include a prize!')
    embed = discord.Embed(title='New Giveaway!', description=f'{ctx.author.mention} is giving away **{prize}**!!',
                          color=discord.Color.random())
    time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    gawtime = int(time[:-1]) * time_convert[time[-1]]
    embed.set_footer(text=f'Giveaway ends in {time}.React with the "🎉" to enter!')
    gaw_msg = await ctx.send(f"{giveaway_role.mention}", embed=embed)

    await gaw_msg.add_reaction("🎉")
    await asyncio.sleep(gawtime)

    await ctx.send("Picking a random user!")
    await asyncio.sleep(1)

    new_gaw_msg = await ctx.channel.fetch_message(gaw_msg.id)

    users = await new_gaw_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    try:
        winner = random.choice(users)
    except:
        await ctx.send("No one won since no one entered!")
        return

    await ctx.send(f"YAYYYYY!!!! {winner.mention} has won the giveaway for **{prize}**!!")


@client.command()
@commands.has_any_role("Sr.Admin", "Owner")
async def kick(ctx, user: discord.Member = None, *, reason=None):
    if user == None:
        await ctx.send("Please enter a user!")
        return

    await user.kick(reason=reason)
    await ctx.send(f'Kicked {user.name} for reason {reason}')


@client.command()
@commands.has_any_role("Sr.Admin", "Owner")
async def ban(ctx, user: discord.Member = None, *, reason=None):
    if user == None:
        await ctx.send("Please enter a user!")
        return

    await user.ban(reason=reason)
    await ctx.send(f'Banned {user.name} for reason {reason}')


@client.command()
@commands.has_any_role("Sr.Admin", "Owner")
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
            await ctx.send(f":x: You failed to rob {user} and paid them {fail_losing} Gru coins!")
            await update_bank(user, fail_losing)
            await update_bank(ctx.author, fail_losing * -1)
        elif type == 1:
            await ctx.send(f":white_check_mark: You successfully robbed {user} and got {earning} Gru coins!")
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
@commands.has_any_role("Owner", "Sr.Admin", "Admin", "Moderator")
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
@commands.has_any_role("Owner", "Sr.Admin", "Admin", "Moderator")
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
        if admin_amt >= 1 or sradmin in ctx.author.roles or admin in ctx.author.roles or mod in ctx.author.roles or owner in ctx.author.roles:
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
    e = discord.Embed(title="Crate Info", description="These are the price range of all the crates.",
                      color=discord.Color.random())
    e.add_field(name="Common", value="2,000 - 5,000")
    e.add_field(name="Uncommon", value="5,000 - 10,000")
    e.add_field(name="Rare", value="30,000 - 50,000")
    e.add_field(name="Epic", value="50,000 - 100,000")
    e.add_field(name="Legendary", value="100,000 - 250,000")
    e.add_field(name="Mythic", value="200,000 - 300,000")
    e.add_field(name="Admin", value="900,000 - 1,000,000")
    await ctx.reply(embed=e)


@client.command()
async def opencrate(ctx, type=None, amount=None):
    user = ctx.author
    lootbox_data = await get_lootbox_data()
    total_lootboxes = lootbox_data[str(user.id)]["common"] + lootbox_data[str(user.id)]["uncommon"] + \
                      lootbox_data[str(user.id)]["rare"] + lootbox_data[str(user.id)]["epic"] + \
                      lootbox_data[str(user.id)]["legendary"] + lootbox_data[str(user.id)]["mythic"] + \
                      lootbox_data[str(user.id)]["admin"]

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
        if type == 'admin' or type == 'a':
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
                        value=f"You opened {amt} **Admin** crate(s) and got `{total_cash} Gru coins`!!! :tada:")
            await update_bank(ctx.author, total_cash)
            await ctx.reply(embed=e)
            lootbox_data[str(user.id)]["admin"] -= amt
            with open('databases/lootboxes.json', 'w') as f:
                json.dump(lootbox_data, f, indent=4)

        elif type == 'mythic' or type == 'm':
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
                        value=f"You opened {amt} **Mythic** crate(s) and got `{total_cash} Gru coins`!!! :tada:")
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
                        value=f"You opened {amt} **Legendary** crate(s) and got `{total_cash} Gru coins`!!! :tada:")
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
                        value=f"You opened {amt} **Epic** crate(s) and got `{total_cash} Gru coins`!!! :tada:")
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
                        value=f"You opened {amt} **Rare** crate(s) and got `{total_cash} Gru coins`!!! :tada:")
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
                        value=f"You opened {amt} **Uncommon** crate(s) and got `{total_cash} Gru coins`!!! :tada:")
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
                        value=f"You opened {amt} **Common** crate(s) and got `{total_cash} Gru coins`!!! :tada:")
            await update_bank(ctx.author, total_cash)
            await ctx.reply(embed=e)
            lootbox_data[str(user.id)]["common"] -= amt
            with open('databases/lootboxes.json', 'w') as f:
                json.dump(lootbox_data, f, indent=4)
        return

    amount = int(amount)
    if type == 'all' or type == 'a':
        # work on later
        print("testing")

    if type == "admin":
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
                    value=f"You opened {amount} **Admin** crate(s) and got `{total_cash} Gru coins`!!! :tada:")
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
                    value=f"You opened {amount} **Mythic** crate(s) and got `{total_cash} Gru coins`!!! :tada:")
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
                    value=f"You opened {amount} **Legendary** crate(s) and got `{total_cash} Gru coins`!!! :tada:")
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
                    value=f"You opened {amount} **Epic** crate(s) and got `{total_cash} Gru coins`!!! :tada:")
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
                    value=f"You opened {amount} **Rare** crate(s) and got `{total_cash} Gru coins`!!! :tada:")
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
                    value=f"You opened {amount} **Uncommon** crate(s) and got `{total_cash} Gru coins`!!! :tada:")
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
                    value=f"You opened {amount} **Common** crate(s) and got `{total_cash} Gru coins`!!! :tada:")
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


class Counter(discord.ui.View):

    # Define the actual button
    # When pressed, this increments the number displayed until it hits 5.
    # When it hits 5, the counter button is disabled and it turns green.
    # note: The name of the function does not matter to the library
    @discord.ui.button(label='0', style=discord.ButtonStyle.red)
    async def count(self, button: discord.ui.Button, interaction: discord.Interaction):
        number = int(button.label) if button.label else 0
        if number + 1 >= 20:
            button.style = discord.ButtonStyle.green
            button.disabled = True
        button.label = str(number + 1)
        # Make sure to update the message with our updated selves
        await interaction.response.edit_message(view=self)


@client.command()
async def counter(ctx):
    """Starts a counter for pressing."""
    await ctx.send('Press!', view=Counter())


# Defines a custom Select containing colour options
# that the user can choose. The callback function
# of this class is called when the user changes their choice
class Dropdown(discord.ui.Select):
    def __init__(self):
        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Red', description='Your favourite color is red', emoji='🟥'),
            discord.SelectOption(label='Green', description='Your favourite color is green', emoji='🟩'),
            discord.SelectOption(label='Blue', description='Your favourite color is blue', emoji='🟦')
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Choose your favourite color...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        await interaction.response.send_message(f'Your favourite color is {self.values[0]}')


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown())


@client.command()
async def color(ctx):
    """Sends a message with our dropdown containing colours"""

    # Create the view containing our dropdown
    view = DropdownView()

    # Sending a message containing our view
    await ctx.send('Pick your favourite colour:', view=view)


# Defines a custom button that contains the logic of the game.
# The ['TicTacToe'] bit is for type hinting purposes to tell your IDE or linter
# what the type of `self.view` is. It is not required.
class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        # A label is required, but we don't need one so a zero-width space is used
        # The row parameter tells the View which row to place the button under.
        # A View can only contain up to 5 rows -- each row can only have 5 buttons.
        # Since a Tic Tac Toe grid is 3x3 that means we have 3 rows and 3 columns.
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed
    # This is part of the "meat" of the game logic
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = 'X won!'
            elif winner == view.O:
                content = 'O won!'
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


# This is our actual board View
class TicTacToe(discord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


@client.command()
async def tic(ctx):
    """Starts a tic-tac-toe game with yourself."""
    await ctx.send('Tic Tac Toe: X goes first', view=TicTacToe())


calculator_users = []


def calculator(exp):
    o = exp.replace('x', '*')
    o = o.replace('÷', '/')
    try:
        result = str(eval(o))
    except:
        result = "An error occurred"

    return result


class Calculator_Buttons(discord.ui.View):
    def __init__(self, author, message, embed):
        super().__init__(timeout=300)
        self.author = author
        self.calculator_message = message
        self.calculator_embed = embed
        self.is_placeholder = True

    @discord.ui.button(label="1", style=discord.ButtonStyle.grey)
    async def one(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="2", style=discord.ButtonStyle.grey)
    async def two(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="3", style=discord.ButtonStyle.grey)
    async def three(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="x", style=discord.ButtonStyle.blurple)
    async def mult(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="Exit", style=discord.ButtonStyle.danger)
    async def exit(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            await self.calculator_message.edit("The calculator is closing...")
            await asyncio.sleep(1)
            await self.calculator_message.delete()
            calculator_users.remove(str(self.author.id))
            self.stop()

    @discord.ui.button(label="4", style=discord.ButtonStyle.grey, row=1)
    async def four(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="5", style=discord.ButtonStyle.grey, row=1)
    async def five(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="6", style=discord.ButtonStyle.grey, row=1)
    async def six(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="÷", style=discord.ButtonStyle.blurple, row=1)
    async def div(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="←", style=discord.ButtonStyle.danger, row=1)
    async def backbutton(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = "0"
                await self.calculator_message.edit(embed=self.calculator_embed)
                self.is_placeholder = True
                return
            if self.calculator_embed.description[:-1] == "":
                self.calculator_embed.description = "0"
                await self.calculator_message.edit(embed=self.calculator_embed)
                self.is_placeholder = True
                return
            self.calculator_embed.description = self.calculator_embed.description[:-1]
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="7", style=discord.ButtonStyle.grey, row=2)
    async def seven(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="8", style=discord.ButtonStyle.grey, row=2)
    async def eight(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="9", style=discord.ButtonStyle.grey, row=2)
    async def nine(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="+", style=discord.ButtonStyle.blurple, row=2)
    async def plus(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="Clear", style=discord.ButtonStyle.danger, row=2)
    async def clear(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            self.calculator_embed.description = "0"
            await self.calculator_message.edit(embed=self.calculator_embed)
            self.is_placeholder = True

    @discord.ui.button(label="000", style=discord.ButtonStyle.grey, row=3)
    async def three_zero(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="0000", style=discord.ButtonStyle.grey, row=3)
    async def four_zero(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="(", style=discord.ButtonStyle.grey, row=3)
    async def left_paren(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="**", style=discord.ButtonStyle.blurple, row=3)
    async def power(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label=")", style=discord.ButtonStyle.grey, row=3)
    async def right_paren(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="00", style=discord.ButtonStyle.grey, row=4)
    async def two_zero(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="0", style=discord.ButtonStyle.grey, row=4)
    async def one_zero(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label=".", style=discord.ButtonStyle.grey, row=4)
    async def point(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="-", style=discord.ButtonStyle.blurple, row=4)
    async def minus(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.calculator_embed.description + button.label) >= 4096:
            return
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = button.label
                self.is_placeholder = False
            else:
                self.calculator_embed.description += button.label
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="=", style=discord.ButtonStyle.green, row=4)
    async def equals(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            if len(calculator(self.calculator_embed.description)) > 4096:
                self.calculator_embed.description = "Too big of a number"
                await self.calculator_message.edit(embed=self.calculator_embed)
            else:
                self.calculator_embed.description = calculator(self.calculator_embed.description)
                await self.calculator_message.edit(embed=self.calculator_embed)

    async def on_timeout(self):
        for x in self.children:
            x.disabled = True
        calculator_users.remove(str(self.author.id))
        await self.calculator_message.edit(view=self)


@client.command()
async def calc(ctx):
    if f'{ctx.author.id}' in calculator_users:
        await ctx.send("You already have a calculator open! Close it to open another one!")
        return
    calculator_users.append(f'{ctx.author.id}')
    await ctx.message.delete()
    e = discord.Embed(title=f"{ctx.author.name}'s calculator! | {ctx.author.id}", description="0",
                      color=discord.Color.random())
    p = await ctx.send("Calculator loading...", embed=e)
    view = Calculator_Buttons(ctx.author, p, e)
    await asyncio.sleep(1)
    await p.edit(view=view)
    await p.edit("Calculator Loaded!")


@client.command(aliases=["heck"])
@commands.cooldown(1, 120, commands.BucketType.user)
async def hack(ctx, user: discord.Member = None):
    if user is None:
        await ctx.send("Please enter a user to hack!(Unless you want to hack air)")
        hack.reset_cooldown(ctx)
        return
    with open('databases/countries.txt', 'r') as f:
        countries = f.read()
        countries_list = list(map(str, countries.split()))
        country = random.choice(countries_list)

    hack_msg = await ctx.send(f"Hacking! Target: {user}...")
    await asyncio.sleep(1)
    await hack_msg.edit("Trying To Access Discord Files... [▓  ]")
    await asyncio.sleep(0.9)
    await hack_msg.edit("Trying To Access Discord Files... [▓▓  ]")
    await asyncio.sleep(0.9)
    await hack_msg.edit("Trying To Access Discord Files... [▓▓▓ ]")
    await asyncio.sleep(0.9)
    await hack_msg.edit("Trying To Access Discord Files... [▓▓▓▓ ]")
    await asyncio.sleep(0.9)
    await hack_msg.edit("Trying To Access Discord Files... [▓▓▓▓▓]")
    await asyncio.sleep(0.9)
    await hack_msg.edit("Successfully Accessed Discord Files! [▓▓▓▓▓]")
    await asyncio.sleep(0.9)
    await hack_msg.edit("Trying to Access Discord Files... SUCCESS")
    await asyncio.sleep(1)
    await hack_msg.edit("Trying To Access Discord/users... [▓  ]")
    await asyncio.sleep(1.5)
    await hack_msg.edit("Trying To Access Discord/users... [▓▓  ]")
    await asyncio.sleep(1.5)
    await hack_msg.edit("Trying To Access Discord/users... [▓▓▓ ]")
    await asyncio.sleep(1.5)
    await hack_msg.edit("Trying To Access Discord/users... [▓▓▓▓ ]")
    await asyncio.sleep(1.5)
    await hack_msg.edit("Trying To Access Discord/users... [▓▓▓▓▓]")
    await asyncio.sleep(1.5)
    await hack_msg.edit("Successfully Got Access to Discord/users! [▓▓▓▓▓]")
    await asyncio.sleep(1.5)
    await hack_msg.edit("Trying to Access Discord/users... SUCCESS")
    await asyncio.sleep(1)
    await hack_msg.edit(f"Trying To Access Discord/users/{user.id}... [▓  ]")
    await asyncio.sleep(1.5)
    await hack_msg.edit(f"Trying To Access Discord/users/{user.id}... [▓▓  ]")
    await asyncio.sleep(1.5)
    await hack_msg.edit(f"Trying To Access Discord/users/{user.id}... [▓▓▓ ]")
    await asyncio.sleep(1.5)
    await hack_msg.edit(f"Trying To Access Discord/users/{user.id}... [▓▓▓▓ ]")
    await asyncio.sleep(1.5)
    await hack_msg.edit(f"Trying To Access Discord/users/{user.id}... [▓▓▓▓▓]")
    await asyncio.sleep(1.5)
    await hack_msg.edit(f"Successfully Got Access to Discord/users/{user.id}! [▓▓▓▓▓]")
    await asyncio.sleep(1.5)
    await hack_msg.edit(f"Trying to Access Discord/users/{user.id}... SUCCESS")
    await asyncio.sleep(1.5)
    await hack_msg.edit("Trying to Access Discord/users... SUCCESS")
    await asyncio.sleep(1)
    await hack_msg.edit(f"Retrieving Login and more from discord/users/{user.name}... [▓  ]")
    await asyncio.sleep(1.5)
    await hack_msg.edit(f"Retrieving Login and more from discord/users/{user.name}... [▓▓  ]")
    await asyncio.sleep(1.5)
    await hack_msg.edit(f"Retrieving Login and more from discord/users/{user.name}... [▓▓▓ ]")
    await asyncio.sleep(1.5)
    await hack_msg.edit(f"Retrieving Login and more from discord/users/{user.name}... [▓▓▓▓ ]")
    await asyncio.sleep(1.5)
    await hack_msg.edit(f"Retrieving Login and more from discord/users/{user.name}... [▓▓▓▓▓]")
    await asyncio.sleep(1.5)
    await hack_msg.edit(f"Successfully Got Access to discord/users/{user.name}! [▓▓▓▓▓]")
    await asyncio.sleep(1.5)
    await hack_msg.edit(f"Retrieving Login and more from discord/users/{user.name}... SUCCESS")
    await asyncio.sleep(1.5)
    await hack_msg.edit(f"discord/users/{user.name}... SUCCESS")
    await hack_msg.edit("Bypassing keys...")
    await asyncio.sleep(0.9)
    await hack_msg.edit("Initializing lockdown and changing password...")
    await asyncio.sleep(4)
    second_part = str(datetime.datetime.now().timestamp() - 129384000)
    second_part_bytes = second_part.encode("ascii")
    base64_bytes_second_part = base64.b64encode(second_part_bytes)
    final = base64_bytes_second_part.decode("ascii")
    user_data = {
        "user": {
            "username": str(user.name),
            "id": str(user.id),
            "discriminator": str(user.discriminator),
            "bot": str(user.bot),
            "tag": str(user),
            "avatar": str(user.display_avatar.key),
            "avatarURL": str(user.display_avatar.url),
            "createdAt": str(user.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")),
            "flags": {
                "raw": user.public_flags.value,
                "staff": user.public_flags.staff,
                "partner": user.public_flags.partner,
                "hypesquadEvents": user.public_flags.hypesquad,
                "bugHunter": user.public_flags.bug_hunter,
                "bugHunterLevel2": user.public_flags.bug_hunter_level_2,
                "hypesquadBravery": user.public_flags.hypesquad_bravery,
                "hypesquadBalance": user.public_flags.hypesquad_balance,
                "hypesquadBrilliance": user.public_flags.hypesquad_brilliance,
                "earlySupporter": user.public_flags.early_supporter,
                "teamUser": user.public_flags.team_user,
                "system": user.public_flags.system,
                "verifiedBot": user.public_flags.verified_bot,
                "verifiedBotDeveloper": user.public_flags.verified_bot_developer,
                "earlyVerifiedBotDeveloper": user.public_flags.early_verified_bot_developer
            }
        }
    }
    desktop_status = user.desktop_status
    mobile_status = user.mobile_status
    raw_status = user.raw_status
    status = user.status

    member_data = {
        "member": {
            "joinedAt": str(user.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")),
            "activity": str(user.activity),
            "guildName": ctx.guild.name,
            "nick": str(user.nick),
            "pending": str(user.pending),
            "status": str(status),
            "rawStatus": str(raw_status),
            "mobileStatus": str(mobile_status),
            "isOnMobile": str(user.is_on_mobile()),
            "desktopStatus": str(desktop_status),
            "webStatus": str(user.web_status),
            "topRoleColor": str(user.top_role.color),
            "totalRoles": len(user.roles),
            "mention": f"<@{user.id}>",
            "displayName": user.display_name,
            "topRole": str(user.top_role)
        }
    }
    coms = ["gmail.com", "outlook.com", "yahoo.com", "hotmail.com"]
    fake_token = ""
    fake_password = ""
    last = ""
    for x in range(0, 27):
        letter_or_num = random.choice(string.ascii_letters + string.digits)
        last += letter_or_num
    user_id = str(user.id)
    user_id_bytes = user_id.encode("ascii")
    base64_bytes = base64.b64encode(user_id_bytes)
    base64_string = base64_bytes.decode("ascii")
    fake_token += f"{base64_string}.{final}.{last}"

    for x in range(0, 14):
        letter = random.choice(string.ascii_letters)
        fake_password += letter

    personal_data = {
        "personal": {
            "ipAdress": f"{random.randint(0, 200)}.{random.randint(0, 200)}.{random.randint(0, 200)}.{random.randint(0, 200)}",
            "country": country,
            "device": random.choice(["Chromebook", "Iphone", "Ipad", "Samsung", "MacOS", "Windows", "Nokia"]),
            "emailAddress": f"{user.name}@{random.choice(coms)}",
            "password": fake_password,
            "token": fake_token
        }
    }
    hack_em = discord.Embed(title=f":unlock: Successfully Hacked {user}!",
                            description=f"{user.mention}|Here's the info I got from discord's database:",
                            color=discord.Color.yellow())
    hack_em.add_field(name=":bust_in_silhouette: User Data", value=f'```json\n{json.dumps(user_data, indent=4)}```')
    hack_em.add_field(name=":boy: Member Data", value=f'```json\n{json.dumps(member_data, indent=4)}```', inline=False)
    hack_em.add_field(name=":key: Personal Data", value=f'```json\n{json.dumps(personal_data, indent=4)}```',
                      inline=False)
    await hack_msg.edit(embed=hack_em)


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
    if user is None:
        return await ctx.send("Please enter a user!(unless you want to put yourself in jail)")
    await ctx.trigger_typing()
    async with aiohttp.ClientSession() as trigSession:
        async with trigSession.get(
                f'https://some-random-api.ml/canvas/jail?avatar={user.display_avatar.with_size(1024)}') as trigImg:  # get users avatar as png with 1024 size
            if trigImg.status in range(200, 299):
                imageData = BytesIO(await trigImg.read())  # read the image/bytes
                await trigSession.close()  # closing the session and;
                await ctx.reply(file=discord.File(imageData, 'image.png'))
            else:
                await ctx.send("Error when making request...")
                await trigSession.close()


@client.command(aliases=["trigger"])
async def triggered(ctx, user: discord.Member = None):
    if user is None:
        return await ctx.send("Please enter a user!(unless you want to trigger yourself)")
    await ctx.trigger_typing()
    async with aiohttp.ClientSession() as trigSession:
        async with trigSession.get(
                f'https://some-random-api.ml/canvas/triggered?avatar={user.display_avatar.with_size(1024)}') as trigImg:
            if trigImg.status in range(200, 299):
                imageData = BytesIO(await trigImg.read())  # read the image/bytes
                await trigSession.close()  # closing the session and;
                await ctx.reply(file=discord.File(imageData, 'triggered.gif'))
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


@client.command()
async def captcha(ctx, *, text=None):
    if text is None:
        await ctx.send("Please enter some text!")
        return
    await ctx.trigger_typing()
    captcha = await alex_api.captcha(text)
    captcha_bytes = await captcha.read()

    await ctx.send(f"Rendered by **{ctx.author.name}**", file=discord.File(captcha_bytes, filename="captcha.png"))


@client.command(aliases=["ac"])
@commands.cooldown(1, 15, commands.BucketType.user)
async def achievement(ctx, text: str = None, icon=None):
    if text is None:
        return await ctx.send("Please enter some text!")
    await ctx.trigger_typing()
    image = await alex_api.achievement(text=text, icon=icon)
    image_bytes = await image.read()
    file = discord.File(image_bytes, "achievement.png")
    await ctx.send(f"Rendered by **{ctx.author.name}**", file=file)


@client.command()
async def ac_icons(ctx):
    await ctx.send(file=discord.File("databases/icons.txt"))


@client.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def supreme(ctx, *, text: str = None):
    if text is None:
        await ctx.send("Please enter some text!")
        supreme.reset_cooldown(ctx)
        return
    await ctx.trigger_typing()
    embed = discord.Embed(title=f"Rendered by **{ctx.author.name}**", color=discord.Color.random()).set_image(
        url="attachment://supreme.png")
    image = discord.File(await (await alex_api.supreme(text=text)).read(), "supreme.png")
    await ctx.send(embed=embed, file=image)


@client.event  # This event runs whenever a user updates: status, game playing, avatar, nickname or role
async def on_member_update(before, after):
    n = after.nick
    try:
        if n != before.nick:  # Check if they updated their username
            if n.lower().count("akshar") or n.lower().count("fuck") or n.lower().count("bitch") or n.lower().count(
                    "ass") or n.lower().count("f3ck") or n.lower().count("a s s") or n.lower().count(
                    "f u c k") or n.lower().count("b i t c h") > 0:  # If username contains tim
                last = before.nick
                if last:  # If they had a username before change it back to that
                    await after.edit(nick="NICKNAME NOT ALLOWED")
                else:  # Otherwise set it to "NO STOP THAT"
                    await after.edit(nick="NO STOP THAT")
    except:
        pass


@client.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        pass

    else:
        with open('databases/reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):
    with open('databases/reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:
            if x['emoji'] == payload.emoji.name:
                role = discord.utils.get(client.get_guild(
                    payload.guild_id).roles, id=x['role_id'])

                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)


@client.command()
@commands.has_permissions(administrator=True, manage_roles=True)
async def reactrole(ctx, emoji=None, role: discord.Role = None, *, message=None):
    if emoji is None or role is None or message is None:
        return await ctx.send("Please enter an emoji role or message!")
    if role.position >= ctx.me.top_role.position:
        return await ctx.send("I can't make a reaction role for that role because it is above or is my top role!")

    emb = discord.Embed(description=message, color=discord.Color.random(), title="New Reaction Role!")
    msg = await ctx.channel.send(embed=emb)
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



            # Main code ends
####################################################################
####################################################################


for filename in os.listdir("cogs"):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(bot_token.token)
