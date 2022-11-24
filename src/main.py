import math
import aiohttp
import nextcord as discord
import asyncio
import datetime
import os
import json
import random
import psutil
# from zoneinfo import ZoneInfo
from nextcord.ext import commands
from nextcord.utils import get
from typing import Optional
from PIL import Image
from io import BytesIO
from num2words import num2words
from src.utils import http, config
import humanfriendly
import itertools
from gru_bot import GruBot
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)



async def get_prefix(bot, message):
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT prefix FROM prefixes WHERE guild = ?", (message.guild.id,))
        data = await cursor.fetchone()
        if data:
            return commands.when_mentioned_or(*mixed_case(data[0]))(client, message)
        else:
            # with open("databases/server_configs.json", 'r') as f:
            #     configs = json.load(f)

            # configs[str(message.guild.id)] = {}
            # configs[str(message.guild.id)]["giveaway_role"] = "None"
            try:
                await cursor.execute("INSERT INTO prefixes (prefix, guild) VALUES (?, ?)",
                                     (config.getenv("BOT_PREFIX"), message.guild.id,))
                await cursor.execute("SELECT prefix FROM prefixes WHERE guild = ?", (message.guild.id,))

                data = await cursor.fetchone()
                if data:
                    await cursor.execute("UPDATE prefixes SET prefix = ? WHERE guild = ?",
                                         (config.getenv("BOT_PREFIX"), message.guild.id,))
                    return commands.when_mentioned_or(*mixed_case(data[0]))(client, message)
            except Exception as e:
                print(e)
                return commands.when_mentioned_or(*mixed_case(config.getenv("BOT_PREFIX")))(client, message)

            # with open("databases/server_configs.json", 'w') as f:
            #     json.dump(configs, f, indent=4)
    await bot.db.commit()


def mixed_case(*args):
    total = []
    for string in args:
        a = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in string)))
        for x in list(a):
            total.append(x)

    return list(total)


client = GruBot(command_prefix=get_prefix,
                intents=discord.Intents.all(),
                case_insensitive=True)
client.remove_command("help")


@client.command()
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    member_display_avatar_pic = member.display_avatar

    await ctx.reply(member_display_avatar_pic)
    if member == client.user:
        await ctx.reply("HEEEY THAT'S ME. I'M FAMOUS POOOOGGGGGG")


def convert_str_to_number(x):
    total_stars = 0
    num_map = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    if x.isdigit():
        total_stars = int(x)
    else:
        if len(x) > 1:
            total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(total_stars)


####################################################################
####################################################################
# Main code starts :)


animal_shop = [
    [
        {
            "name": "Wolf",
            "sell_price": 2000
        }, {
        "name": "Mountain Lion",
        "sell_price": 3200
    }, {
        "name": "Chicken",
        "sell_price": 3500
    }, {
        "name": "Rabbit",
        "sell_price": 3700
    }, {
        "name": "Deer",
        "sell_price": 4200
    }, {
        "name": "Moose",
        "sell_price": 4900
    }, {
        "name": "Angry Bird",
        "sell_price": 8500
    }, {
        "name": "Minion",
        "sell_price": 15000
    }, {
        "name": "Bengal Tiger",
        "sell_price": 32000
    }, {
        "name": "Evil Minion",
        "sell_price": 50000
    }, {
        "name": "White Tiger",
        "sell_price": 65000
    }, {
        "name": "Unicorn",
        "sell_price": 85000
    }],
    [{
        "name": "Duck",
        "sell_price": 6000
    }, {
        "name": "Mosasaurus",
        "sell_price": 500000
    }, {
        "name": "Fish",
        "sell_price": 3400
    }, {
        "name": "Nemo",
        "sell_price": 3600
    }, {
        "name": "Great White Shark",
        "sell_price": 75000
    }, {
        "name": "Blobfish",
        "sell_price": 10000
    }, {
        "name": "Crab",
        "sell_price": 1500
    }, {
        "name": "Shell",
        "sell_price": 250
    }, {
        "name": "Garbage",
        "sell_price": 100
    }, {
        "name": "Water Bottle",
        "sell_price": 3000
    }, {
        "name": "Dumbo Octopus",
        "sell_price": 35000
    }, {
        "name": "Donald Duck",
        "sell_price": 3500
    }],
    [{
        "name": "Hawk",
        "sell_price": 5000
    }, {
        "name": "Bat",
        "sell_price": 15000
    }, {
        "name": "Mosquito",
        "sell_price": 1000
    }, {
        "name": "Flying Lizard",
        "sell_price": 7000
    }, {
        "name": "Bird",
        "sell_price": 2000
    }, {
        "name": "Ladybug",
        "sell_price": 1500
    }, {
        "name": "Bumblebee",
        "sell_price": 9500
    }, {
        "name": "Hummingbird",
        "sell_price": 13500
    }, {
        "name": "Eagle",
        "sell_price": 15000
    }, {
        "name": "Pigeon",
        "sell_price": 5000
    }, {
        "name": "Vulture",
        "sell_price": 17500
    }, {
        "name": "Hummingbird",
        "sell_price": 13500
    }, {
        "name": "Pterodactyl",
        "sell_price": 102000
    }]]


@client.command()
async def stats(ctx):
    e = discord.Embed(title="My Stats!", color=discord.Color.random())
    e.add_field(name="Days:", value=client.td, inline=True)
    e.add_field(name="Hours:", value=client.th, inline=True)
    e.add_field(name="Minutes:", value=client.tm, inline=True)
    e.add_field(name="Seconds:", value=client.ts, inline=True)
    e.add_field(name="CPU:", value=f"{psutil.cpu_percent()}%", inline=False)
    e.add_field(name="RAM:",
                value=f"{psutil.virtual_memory()[2]}%",
                inline=True)
    e.add_field(name="Version:",
                value=f"{config.getenv('BOT_VERSION')}",
                inline=False)
    await ctx.reply(embed=e)


@client.command(aliases=['bal'])
async def balance(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    else:
        await config.open_account(user)
    await config.open_account(ctx.author)
    users = await get_bank_data()
    async with client.db.cursor() as cursor:
        await cursor.execute("SELECT name, pay FROM jobs WHERE user = ?", (user.id,))
        job_data = await cursor.fetchone()
        await cursor.execute("SELECT wallet, bank, booster, max FROM mainbank WHERE user = ?", (user.id,))
        bank_data = await cursor.fetchone()
    job_name = job_data[0]
    job_pay = job_data[1]
    wallet = bank_data[0]
    bank = bank_data[1]
    booster = bank_data[2]
    max_amt = bank_data[3]

    em = discord.Embed(title=f"{user.display_name}'s Balance",
                       color=discord.Color.green())
    em.add_field(name="Wallet Balance",
                 value=f"{int(wallet):,} Minions™", inline=False)
    em.add_field(name='Bank Balance',
                 value=
                 f"{int(bank):,} **/** {int(max_amt):,} Minions™ `({round(float(int(bank) / int(max_amt)) * 100, 2)}% full)`"
                 , inline=False)
    em.add_field(name='Job', value=job_name, inline=False)
    em.add_field(name='Job salary',
                 value=f"{int(job_pay):,} Minions™ per hour", inline=False)
    if booster != 1:
        em.add_field(name='Booster', value=f'{float(booster) if not booster % 1 == 0 else int(booster):,}x',
                     inline=False)
    await ctx.reply(embed=em)


@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def beg(ctx):
    await config.open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    booster = users[str(user.id)]["booster"]

    earnings = random.randrange(1000)

    people = [
        "Elon Musk", "Jeff Bezos", "Mr Krabs", "Your mom", "Kylie Jenners",
        "Albert Einstein", "Mr Mosby", "Greg Heffley",
        "I the all mighty Gru Bot", "Rihanna"
    ]

    person = random.choice(people)
    nums = [0, 1]
    trybeg = random.choice(nums)

    if trybeg == 0:
        message = f'"Oh you beggar take `{(earnings * booster):,} Minions™`"'
        beg_embed = discord.Embed(description=message,
                                  color=discord.Color.random())
        beg_embed.set_author(name=person)
        if booster != 1:
            beg_embed.set_footer(
                text=
                f"You earned {(earnings * (booster - 1)):,} extra Minions™ since you had a {booster:,}x booster!"
            )
        await ctx.reply(embed=beg_embed)
        users[str(user.id)]["wallet"] += earnings * booster

    else:
        message = random.choice(
            ['no', 'ur mom', 'credit card is maxed', 'why u', 'nah bro', 'not today', 'nu uh', 'l bozo'])
        beg_embed = discord.Embed(description=message,
                                  color=discord.Color.random())
        beg_embed.set_author(name=person)
        beg_embed.set_footer(text="imagine begging LOL")
        await ctx.reply(embed=beg_embed)

    with open("databases/mainbank.json", 'w') as f:
        json.dump(users, f, indent=4)


@client.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    await update_bank(ctx.author, 40000)
    lootbox_data = await get_lootbox_data()
    lootbox_data[str(ctx.author.id)]["epic"] += 1
    with open('databases/lootboxes.json', 'w') as f:
        json.dump(lootbox_data, f, indent=4)
    await ctx.reply(
        "You just recieved `40,000 Minions™` and an `Epic` crate!")


@client.command()
@commands.cooldown(1, 86400 * 7, commands.BucketType.user)
async def weekly(ctx):
    await update_bank(ctx.author, 500000)
    lootbox_data = await get_lootbox_data()
    lootbox_data[str(ctx.author.id)]["legendary"] += 5
    with open('databases/lootboxes.json', 'w') as f:
        json.dump(lootbox_data, f, indent=4)
    await ctx.reply(
        "You just recieved `500,000 Minions™` and 5 `Legendary` crates!")


facts = [
    "Gru likes his cup more than anything", "Gru will never get a wife",
    "Gru has 2000IQ", "Gru does not like kids",
    "Gru only refuels his ship once a week", "Gru's favorite minion is Bert",
    "Minions have lots of IQ because they work all day"
]

fired_users = []


@client.group(invoke_without_command=True)
@commands.cooldown(1, 3600, commands.BucketType.user)
async def work(ctx, *, name: str = None):
    prefix = await config.get_prefix(client, ctx.guild.id)
    await config.open_account(ctx.author)
    jobs = await get_job_data()
    if ctx.author in fired_users:
        work.reset_cooldown(ctx)
        return await ctx.reply(
            "You have been fired recently, you have to wait 4 hours from your firing time, to be able to work.")
    user = ctx.author
    work_amt = jobs[str(user.id)]["job"]["pay"]
    work_name = jobs[str(user.id)]["job"]["name"]
    hours = jobs[str(user.id)]["job"]["hours"]
    fails = jobs[str(user.id)]["job"]["fails"]
    if fails == 3:
        jobs[str(user.id)]["job"]["name"] = "None"
        jobs[str(user.id)]["job"]["pay"] = 0
        jobs[str(user.id)]["job"]["fails"] = 0
        with open('databases/jobs.json', 'w') as f:
            json.dump(jobs, f, indent=4)
        await ctx.reply(
            f"You have been fired from your job as a {work_name}. You have to wait 4 hours before applying for another job.")
        fired_users.append(ctx.author)
        await asyncio.sleep(14400)
        fired_users.pop(fired_users.index(ctx.author))
    if name:
        for item in jobpays:
            if name.lower() in str(item.lower()):
                if work_name != "None":
                    work.reset_cooldown(ctx)
                    return await ctx.reply(
                        f"You need to resign first to apply for a new job! Run {prefix}work resign to resign!")
                _work = jobpays[item]
                if hours >= _work['hours']:
                    jobs[str(user.id)]["job"]["pay"] = _work['pay']
                    jobs[str(user.id)]["job"]["name"] = item
                    with open('databases/jobs.json', 'w') as f:
                        json.dump(jobs, f, indent=4)
                    work.reset_cooldown(ctx)
                    return await ctx.reply(
                        f"You are now a **{item}**. Your salary is now {_work['pay']:,} Minions™. Be careful not to fail too many times, or you will get fired!")
                work.reset_cooldown(ctx)
                return await ctx.reply("You have not unlocked this job yet, work more to unlock it!")

        for item in p2:
            if name.lower() in str(item.lower()):
                if work_name != "None":
                    work.reset_cooldown(ctx)
                    return await ctx.reply(
                        f"You need to resign first to apply for a new job! Run {prefix}work resign to resign!")
                _work = p2[item]
                if hours >= _work['hours']:
                    jobs[str(user.id)]["job"]["pay"] = _work['pay']
                    jobs[str(user.id)]["job"]["name"] = item
                    with open('databases/jobs.json', 'w') as f:
                        json.dump(jobs, f, indent=4)
                    work.reset_cooldown(ctx)
                    return await ctx.reply(
                        f"You are now a **{item}**. Your salary is now {_work['pay']:,} Minions™. Be careful not to fail too many times, or you will get fired!")
                work.reset_cooldown(ctx)
                return await ctx.reply("You have not unlocked this job yet, work more to unlock it!")
    if work_name == 'None':
        await ctx.reply(
            f"You don't have a job! Get one by doing `{prefix}work <job name>` !!")
        work.reset_cooldown(ctx)
        return

    def check(m):
        return m.channel == ctx.channel and m.author == ctx.author

    typeofwork = "memory"
    config.working_users.append(ctx.author)
    if typeofwork == 'memory':
        await ctx.reply(
            f'''**Working as a {work_name}** - Memory Game - A fact about Gru Things™ will come up on the screen! then it will disappear after a few seconds. Your job is to rewrite the fact!'''
        )
        fact = "\u200B" + random.choice(facts)

        fact_sended = await ctx.reply(f'**{fact}**')
        await asyncio.sleep(4)
        await fact_sended.delete()
        await asyncio.sleep(0.5)
        await ctx.reply("Now, retype the sentence!")
        msg = None
        try:
            msg = await client.wait_for('message', check=check, timeout=20)
        except asyncio.TimeoutError:
            work_em = discord.Embed(
                title="Terrible job!",
                description=
                f"You were given `{int(work_amt / 3):,} Minions™` for 1/3 of an hour of pay",
                color=discord.Color.random())
            work_em.set_footer(text=f'Working as a {work_name.title()}')
            jobs[str(user.id)]['job']['fails'] += 1
            with open('databases/jobs.json', 'w') as f:
                json.dump(jobs, f, indent=4)
            await update_bank(ctx.author, int(work_amt / 3))
            await ctx.reply(embed=work_em)
            return
        if msg.content.lower() == fact.lower():
            jobs[str(user.id)]['job']['fails'] += 1
            with open('databases/jobs.json', 'w') as f:
                json.dump(jobs, f, indent=4)
            return await ctx.reply("I know you copy-pasted it!")
        elif msg.content.lower() != fact.lower()[1:]:
            work_em = discord.Embed(
                title="Terrible job!",
                description=
                f"You were given `{int(work_amt / 3):,} Minions™` for 1/3 of an hour of pay",
                color=discord.Color.random())
            work_em.set_footer(text=f'Working as a {work_name.capitalize()}')
            jobs[str(user.id)]['job']['fails'] += 1
            with open('databases/jobs.json', 'w') as f:
                json.dump(jobs, f, indent=4)
            await ctx.reply(embed=work_em)
            await update_bank(ctx.author, int(work_amt / 3))
            return
        promote_pay = random.randint(0, 8)
        get_crate = random.randint(0, 5)
        work_em = discord.Embed(
            title="Great job!",
            description=
            f"You were given `{work_amt:,} Minions™` for an hour of pay",
            color=discord.Color.random())
        work_em.set_footer(text=f'Working as a {work_name.title()}')
        await update_bank(ctx.author, work_amt)
        jobs[str(user.id)]['job']['fails'] = 0
        with open('databases/jobs.json', 'w') as f:
            json.dump(jobs, f, indent=4)
        await ctx.reply(embed=work_em)
        if get_crate == 5:
            with open('databases/lootboxes.json', 'r') as f:
                lootboxes = json.load(f)
            crate_type = random.choice([
                "mythic", "legendary", "legendary", "epic", "epic", "epic",
                "epic", "rare", "rare", "rare", "rare", "rare", "rare",
                "rare", "uncommon", "uncommon", "uncommon", "uncommon",
                "uncommon", "uncommon", "uncommon", "uncommon", "uncommon",
                "common", "common", "common", "common", "common", "common",
                "common", "common", "common", "common"
            ])
            await ctx.reply(
                f"Your boss saw that you were doing so well, he gave you a **{crate_type.capitalize()}** <:chest:898333946557894716> lootbox!! :tada:"
            )
            lootboxes[str(ctx.author.id)][crate_type] += 1
            with open('databases/lootboxes.json', 'w') as f:
                json.dump(lootboxes, f, indent=4)
        new_job_name = ""
        job_unlocked = False
        jobs[str(user.id)]["job"]["hours"] += 1
        for i in jobpays:
            if jobpays[i]['hours'] == jobs[str(user.id)]["job"]["hours"]:
                job_unlocked = True
                new_job_name = i
        if job_unlocked:
            await ctx.reply(
                f"You have unlocked the **{new_job_name}** job! You can work at it after you resign from this job.")
        with open('databases/jobs.json', 'w') as f:
            json.dump(jobs, f, indent=4)
        if promote_pay == 8:
            num = random.randint(0, 1000)
            await ctx.reply(
                f"Since you are doing really well in your work, your manager has decided to give you a bonus of `{work_amt * 3 + num:,} Minions™`!! :tada: :tada:"
            )
            await update_bank(ctx.author, work_amt * 3 + num)


jobpays = {
    "Gru Gadgets Maker": {'pay': 9000, "hours": 0},
    "Gru Gadgets Tester": {'pay': 12000, "hours": 2},
    "Minion Refiner": {'pay': 16000, "hours": 5},
    "Super Minion Refiner": {'pay': 22000, "hours": 8},
    "Minion Gadget Manager": {'pay': 29000, "hours": 13},
    "Gru Ship Mechanic": {'pay': 35000, "hours": 14},
    "Gru Ship Pilot": {'pay': 41000, "hours": 17},
    "Minion Costume Maker": {'pay': 45000, "hours": 22},
    "Gru Assistant Hacker": {'pay': 55000, "hours": 26},
    "Gru Hacker": {'pay': 60000, "hours": 34},
    "Gru Senior Hacker": {'pay': 67000, "hours": 38},
    "Gru's Barber": {'pay': 69420, "hours": 45},
    "Gru Gadget Programmer": {'pay': 79000, "hours": 51},
    "Gru Code Compiler": {'pay': 90000, "hours": 58},
    "Gru Super Programmer": {'pay': 102000, "hours": 65},
    "Gru Super Code Compiler": {'pay': 117000, "hours": 72},
    "Gru Enterprises Supervisor": {'pay': 137000, "hours": 81},
    "Gru Enterprises Manager": {'pay': 155000, "hours": 90},
    "Gru Enterprises CO": {'pay': 225000, "hours": 102},
    "Gru Enterprises CEO": {'pay': 319000, "hours": 111},
    "Gru Enterprises Super CEO": {'pay': 428000, "hours": 119},
    "Gru Enterprises Owner": {'pay': 700000, "hours": 126},
    "Gru Costumer": {'pay': 1600000, "hours": 137},
    "Groogle Programmer": {'pay': 3500000, "hours": 150},
    "Gru Movie Director": {'pay': 3600000, "hours": 161},
}

p2 = {
    "Groogle Owner": {'pay': 4300000, "hours": 170},
    "Groogle Creator": {'pay': 6900000, "hours": 176},
    "Groogle Custom Computer Language Programmer": {'pay': 10300000, "hours": 200}
}


class Paginator(discord.ui.View):
    def __init__(self, author, embeds, curr):
        super().__init__(timeout=30)
        self.author = author
        self.embeds = embeds
        self.current_embed = curr
        self.message = None

    @discord.ui.button(emoji="<:left_two:982623041228013570>", style=discord.ButtonStyle.green, disabled=True)
    async def begin(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.author:
            return await interaction.response.send_message("This is not your menu.", ephemeral=True)
        em = self.embeds[0]
        self.current_embed = em
        button.disabled = True
        self.children[1].disabled = True
        self.children[2].disabled = False
        self.children[3].disabled = False
        await interaction.response.edit_message(embed=em, view=self)

    @discord.ui.button(emoji="<:left_one:982623094235615232>", style=discord.ButtonStyle.green, disabled=True)
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.author:
            return await interaction.response.send_message("This is not your menu.", ephemeral=True)
        em = self.embeds[self.embeds.index(self.current_embed) - 1]
        self.current_embed = em
        if self.embeds[0] == em:
            button.disabled = True
            self.children[3].disabled = False
            self.children[0].disabled = True
            self.children[1].disabled = True
            self.children[2].disabled = False
        else:
            self.children[3].disabled = False
            self.children[0].disabled = False
            self.children[1].disabled = False
            self.children[2].disabled = False
        await interaction.response.edit_message(embed=em, view=self)

    @discord.ui.button(emoji="<:right_one:982622882469404683>", style=discord.ButtonStyle.green, disabled=False)
    async def forward(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.author:
            return await interaction.response.send_message("This is not your menu.", ephemeral=True)
        em = self.embeds[self.embeds.index(self.current_embed) + 1]
        self.current_embed = em
        if self.embeds[-1] == em:
            button.disabled = True
            self.children[3].disabled = True
            self.children[0].disabled = False
            self.children[1].disabled = False
        else:
            self.children[3].disabled = False
            self.children[0].disabled = False
            self.children[1].disabled = False
        await interaction.response.edit_message(embed=em, view=self)

    @discord.ui.button(emoji="<:right_two:982622978279899206>", style=discord.ButtonStyle.green, disabled=False)
    async def end(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.author:
            return await interaction.response.send_message("This is not your menu.", ephemeral=True)
        em = self.embeds[-1]
        self.current_embed = em
        button.disabled = True
        self.children[2].disabled = True
        self.children[0].disabled = False
        self.children[1].disabled = False
        await interaction.response.edit_message(embed=em, view=self)

    async def on_timeout(self):
        try:
            for x in self.children:
                x.disabled = True
            await self.message.edit(view=self)
        except (discord.HTTPException, discord.Forbidden):
            pass


@work.command(inherit_hooks=True, aliases=['list', 'all'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def jobs(ctx):
    jobs = await get_job_data()
    page1 = discord.Embed(title="Jobs in Gru Enterprises™",
                          description="These are all the jobs available. Jobs next to the ❌ are locked.",
                          color=discord.Color.random())
    page2 = discord.Embed(
        title="Jobs in Gru Enterprises™ (Page 2)",
        description="These are all the jobs available. Jobs next to the ❌ are locked.",
        color=discord.Color.random())

    hours_worked = jobs[str(ctx.author.id)]['job']['hours']
    page1.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
    page1.set_footer(text="Page 1/2")

    page2.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
    page2.set_footer(text="Page 2/2")
    for i in jobpays:
        page1.add_field(name=f"{i}",
                        value=f"{jobpays[i]['pay']:,} Minions™ Per Hour {':x:' if jobpays[i]['hours'] > hours_worked else '<:check:985365213933097010>'}")
    for i in p2:
        page2.add_field(name=f"{i}",
                        value=f"{p2[i]['pay']:,} Minions™ Per Hour {':x:' if p2[i]['hours'] > hours_worked else '<:check:985365213933097010>'}")

    embeds = [page1, page2]
    cur = embeds[0]
    v = Paginator(ctx.author, embeds, cur)
    v.message = await ctx.reply(embed=cur, view=v)


resigned_users = []


@work.command(inherit_hooks=True)
async def resign(ctx):
    jobs = await get_job_data()
    user = ctx.author
    name = jobs[str(user.id)]["job"]["name"]
    prefix = await config.get_prefix(client, ctx.guild.id)
    if name == 'None':
        await ctx.reply(
            f"You don't have a job! You can get one by doing '{prefix}work <job name>'!!")
        work.reset_cooldown(ctx)
    else:
        await ctx.reply(
            "You are now unemployed. You cannot reapply for a job for the next 2 hours"
        )
        jobs[str(user.id)]["job"]["name"] = 'None'
        jobs[str(user.id)]["job"]["pay"] = 0
        with open('databases/jobs.json', 'w') as f:
            json.dump(jobs, f, indent=4)
        resigned_users.append(str(user.id))
        work.reset_cooldown(ctx)
        await asyncio.sleep(7200)
        resigned_users.remove(str(user.id))


@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send('Done!', delete_after=2)


@client.command(aliases=['with'])
async def withdraw(ctx, amount=None):
    await config.open_account(ctx.author)
    if amount == None:
        await ctx.reply("Please enter an amount!")
        return
    amount = amount.lower()

    bal = await update_bank(ctx.author)

    if amount == 'max' or amount == 'all':
        amount = bal[1]
    else:
        try:
            amount = convert_str_to_number(amount)
        except:
            return await ctx.reply("That is an invalid amount!")

    if amount > bal[1]:
        await ctx.reply(f'You do not have `{amount} Minions™` in your bank!')
        return
    if amount < 0:
        await ctx.reply('Amount must be positive!')
        return
    if amount == 0:
        return await ctx.reply("You canot withdraw 0 Minions™ from your bank!")

    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1 * amount, 'bank')
    bal = await update_bank(ctx.author)
    e = discord.Embed(title=f"{ctx.author}'s Withdrawal", color=discord.Color.random())
    e.add_field(name="Current Bank Balance", value=f"{int(bal[1]):,} Minions™️")
    e.add_field(name="Current Wallet Balance", value=f"{int(bal[0]):,} Minions™️", inline=True)
    e.add_field(name="Withdrawal Amount", value=f"{int(amount):,} Minions™️", inline=False)
    await ctx.reply(embed=e)


@client.command(aliases=['dep'])
async def deposit(ctx, amount=None):
    await config.open_account(ctx.author)
    if amount == None:
        await ctx.reply("Please enter an amount!")
        return
    amount = amount.lower()
    bal = await update_bank(ctx.author)
    if amount == 'max' or amount == 'all':
        amount = bal[0]
    else:
        try:
            amount = convert_str_to_number(amount)
        except:
            return await ctx.reply("That is an invalid amount!")
    if amount > bal[0]:
        await ctx.reply(f'You do not have `{amount} Minions™` in your wallet!')
        return
    if amount < 0:
        await ctx.reply('Amount must be positive!')
        return
    if amount == 0:
        return await ctx.reply("You cannot deposit 0 Minions™ to your bank!")
    if bal[1] + amount > bal[2]:
        depositable = bal[2] - bal[1]
        await update_bank(ctx.author, -1 * (bal[0] - depositable))
        await update_bank(ctx.author, depositable, 'bank')
        return await ctx.reply(
            f':white_check_mark: {ctx.author.mention} You deposited `{int(depositable):,} Minions™`'
        )
    await update_bank(ctx.author, -1 * amount)
    await update_bank(ctx.author, amount, 'bank')
    bal = await update_bank(ctx.author)
    e = discord.Embed(title=f"{ctx.author}'s Deposit", color=discord.Color.random())
    e.add_field(name="Current Bank Balance", value=f"{int(bal[1]):,} Minions™️")
    e.add_field(name="Current Wallet Balance", value=f"{int(bal[0]):,} Minions™️", inline=True)
    e.add_field(name="Deposit Amount", value=f"{int(amount):,} Minions™️", inline=False)
    await ctx.reply(embed=e)


@client.command()
async def send(ctx, member: discord.Member, amount=None):
    await config.open_account(ctx.author)
    await config.open_account(member)
    if amount == None:
        await ctx.reply("Please enter an amount!")
        return
    amount = amount.lower()
    bal = await update_bank(ctx.author)
    if amount == 'all' or amount == 'max':
        amount = bal[0]

    amount = convert_str_to_number(amount)

    if amount > bal[0]:
        await ctx.reply('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.reply('Amount must be positive!')
        return

    await update_bank(ctx.author, -1 * amount, 'bank')
    await update_bank(member, amount, 'bank')
    await ctx.reply(
        f':white_check_mark: {ctx.author.mention} You gave {member} {amount} Minions™️'
    )


@client.command(aliases=['steal'])
@commands.cooldown(1, 60, commands.BucketType.user)
async def rob(ctx, member: discord.Member):
    if member.bot:
        rob.reset_cooldown(ctx)
        return await ctx.reply(
            "You are not allowed to steal from bots, back off my kind")
    await config.open_account(ctx.author)
    await config.open_account(member)
    bal = await update_bank(member)
    user_bal = await update_bank(ctx.author)
    if user_bal[0] < 2000:
        rob.reset_cooldown(ctx)
        return await ctx.reply("You need at least `2000 Minions™️` to rob someone.")
    if member.id == 717512097725939795 and ctx.author.id != 972282561642496060:
        rob.reset_cooldown(ctx)
        return await ctx.reply(
            "xD you can't rob him he is the owner of the bot!!!")

    if bal[0] < 100:
        await ctx.reply('It is useless to rob him :(')
        rob.reset_cooldown(ctx)
        return
    if member == ctx.author:
        await ctx.reply("Why are you trying to rob yourself?")
        rob.reset_cooldown(ctx)
        return
    chance = random.choice([0, 1, 2, 3])
    earning = random.randrange(0, bal[0])
    users = await get_bank_data()
    try:
        inv = users[str(member.id)]["bag"]
        uno_rev = {}
        index = 0
        for item in inv:
            if item["item"] == "uno reverse card":
                uno_rev = item
                index = inv.index(item)
        if uno_rev == {}:
            raise Exception

        if uno_rev["amount"] > 0 and chance == 1:
            users[str(member.id)]["bag"][index]["amount"] -= 1
            if users[str(member.id)]["bag"][index]["amount"] == 0:
                users[str(member.id)]["bag"].remove(uno_rev)
            await dump_mainbank_data(users)
            await update_bank(member, earning)
            await ctx.reply(
                f':white_check_mark:{ctx.author.mention} You robbed {member} and got {earning:,} Minions™️'
            )
            await asyncio.sleep(1)
            await ctx.send(f"But, they had a **Uno reverse card!** You have lost {earning:,} Minions™ to them.")
            return
        else:
            await ctx.reply(
                f':x:{ctx.author.mention} You failed to rob {member} and lost 2000 Minions™️ to them.'
            )
            await update_bank(member, 2000)
            await update_bank(ctx.author, -2000)
            return
    except Exception:
        pass

    if chance == 1:
        await update_bank(ctx.author, earning)
        await update_bank(member, -1 * earning)
        await ctx.reply(
            f':white_check_mark:{ctx.author.mention} You robbed {member} and got {earning:,} Minions™️'
        )
    else:
        await ctx.reply(
            f':x:{ctx.author.mention} You failed to rob {member} and lost 2000 Minions™️ to them.'
        )
        await update_bank(member, 2000)
        await update_bank(ctx.author, -2000)


@client.command()
async def slots(ctx, amount=None):
    await config.open_account(ctx.author)
    if amount == None:
        await ctx.reply("Please enter an amount!")
        return

    bal = await update_bank(ctx.author)

    amount = convert_str_to_number(amount)

    if amount > bal[0]:
        await ctx.reply('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.reply('Amount must be positive!')
        return
    final = []
    for i in range(3):
        a = random.choice(['Q', 'O', 'X'])

        final.append(a)

    await ctx.reply(str(final))

    if final[0] == final[1] and final[1] == final[2]:
        await update_bank(ctx.author, 3 * amount)
        await ctx.reply(
            f'JACKPOT!!! You won `{3 * amount} Minions™`!!! :tada: :D {ctx.author.mention}'
        )

    elif final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
        await update_bank(ctx.author, 2 * amount)
        await ctx.reply(
            f'You won `{2 * amount} Minions™` :) {ctx.author.mention}')
    else:
        await update_bank(ctx.author, -1 * amount)
        await ctx.reply(
            f'You lose `{1 * amount} Minions™` :( {ctx.author.mention}')


@client.command(aliases=["store"])
async def shop(ctx):
    page1 = discord.Embed(title="Shop", color=discord.Color.random())

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        page1.add_field(name=name.title(),
                        value=f"{int(price):,} Minions™ | {desc}")
    page1.set_footer(text="Page 1/3")

    page2 = discord.Embed(
        title="Animal Shop",
        description=
        "These are all the animals you can find by hunting or fishing and the prices that you can sell them for.",
        color=discord.Color.random())
    page2.set_footer(text="Page 2/3")
    page2.add_field(
        name="Land Animals",
        value="These are all the land animals you can get by hunting.",
        inline=False)
    for _array in animal_shop[:-1]:
        if _array == animal_shop[1]:
            page2.add_field(
                name="Water Animals",
                value="These are all the water animals you can get by fishing.",
                inline=False)
        for animal in _array:
            name = animal["name"]
            sell = animal["sell_price"]
            page2.add_field(name=name.title(), value=f"{int(sell):,} Minions™")

    page3 = discord.Embed(
        title="Animal Shop (Page 2)",
        description=
        "These are all the animals you can find by hunting or fishing and the prices that you can sell them for.",
        color=discord.Color.random())
    page3.add_field(
        name="Water Animals (Part 2)",
        value=
        "These are all the water animals you can get from fishing (Part 2)",
        inline=False)
    page3.set_footer(text="Page 3/3")
    for animal in animal_shop[1][-1:]:
        name = animal["name"]
        sell = animal["sell_price"]
        page3.add_field(name=name.title(), value=f"{int(sell):,} Minions™")
    page3.add_field(
        name="Aerial Animals",
        value="These are all the aerial animals you can get by hunting.",
        inline=False)
    for animal in animal_shop[2]:
        name = animal["name"]
        sell = animal["sell_price"]
        page3.add_field(name=name.title(), value=f"{int(sell):,} Minions™")

    pages = [page1, page2, page3]
    paginator = Paginator(ctx.author, pages, pages[0])
    paginator.message = await ctx.reply(embed=pages[0], view=paginator)


@client.command()
async def buy(ctx, amount: Optional[int] = 1, *, item):
    users = await get_bank_data()
    item = item.lower()
    if amount < 1:
        return await ctx.reply("You need to sell at least more than one item!")
    if item == "2x booster" or '2x' in item:
        users = await get_bank_data()
        if users[str(ctx.author.id)]["booster"] < 2:
            if users[str(ctx.author.id)]["wallet"] >= 50000:
                users[str(ctx.author.id)]["wallet"] -= 50000
                users[str(ctx.author.id)]["booster"] = 2
                await ctx.reply(
                    ":white_check_mark: You now have a booster for 2x the money!"
                )
                with open('databases/mainbank.json', 'w') as f:
                    json.dump(users, f, indent=4)
                return
            else:
                await ctx.reply("You can't afford this!")
                return
        else:
            await ctx.reply(
                ":x: You already have a booster that's higher than this!")
            return
    if item == "bank record" or 'bank' in item or 'record' in item:
        users = await get_bank_data()
        if users[str(ctx.author.id)]["wallet"] >= 250000 * amount:
            users[str(ctx.author.id)]["wallet"] -= 250000 * amount
            new = random.randint(20000, 150000) * amount
            users[str(ctx.author.id)]["max"] += new
            await ctx.reply(
                f"You give your record{'s' if amount != 1 else ''} to the teller, and he increases your bank space by `{new:,} Minions™️`!")
            with open('databases/mainbank.json', 'w') as f:
                json.dump(users, f, indent=4)
            return
        else:
            await ctx.reply("You can't afford this!")
    if item == "5x booster" or '5x' in item:
        users = await get_bank_data()
        if users[str(ctx.author.id)]["booster"] < 5:
            if users[str(ctx.author.id)]["wallet"] >= 400000:
                users[str(ctx.author.id)]["wallet"] -= 400000
                users[str(ctx.author.id)]["booster"] = 5
                await ctx.reply(
                    ":white_check_mark: You now have a booster for 5x the money!"
                )
                with open('databases/mainbank.json', 'w') as f:
                    json.dump(users, f, indent=4)
                return
            else:
                await ctx.reply("You can't afford this!")
                return
        else:
            await ctx.reply(
                ":x: You already have a booster that's higher than this!")
            return
    if item == "10x booster" or '10x' in item:
        users = await get_bank_data()
        if users[str(ctx.author.id)]["booster"] < 10:
            if users[str(ctx.author.id)]["wallet"] >= 3500000:
                users[str(ctx.author.id)]["wallet"] -= 3500000
                users[str(ctx.author.id)]["booster"] = 10
                await ctx.reply(
                    ":white_check_mark: You now have a booster for 10x the money!"
                )
                with open('databases/mainbank.json', 'w') as f:
                    json.dump(users, f, indent=4)
                return
            else:
                await ctx.reply("You can't afford this!")
                return
        else:
            await ctx.reply(
                ":x: You already have a booster that's higher than this!")
            return
    await config.open_account(ctx.author)

    res = await buy_this(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            await ctx.reply("That item isn't in the shop!")
            return
        if res[1] == 2:
            await ctx.reply(
                f"You don't have enough money in your wallet to buy `{amount}x` {res[2].title()}!"
            )
    e = discord.Embed(title=f"{ctx.author.name}'s Purchase", color=discord.Color.random())
    e.description = f":white_check_mark: You just bought `{amount}x` {res[3].title()} for `{int(res[2]):,} Minions™`!"
    await ctx.reply(embed=e)


## 200 LINES
@client.command(aliases=['inv'])
async def inventory(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
        await config.open_account(ctx.author)
    else:
        await config.open_account(user)

    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except KeyError:
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
        await ctx.reply(embed=em)
        return

    elif len(bag) >= 26 and len(bag) <= 50:
        page2 = discord.Embed(title="Your inventory (Page 2)",
                              color=discord.Color.random())
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
        i = len(bag) - 25
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
        paginator = Paginator(ctx.author, pages, pages[0])
        paginator.message = await ctx.reply(embed=pages[0], view=paginator)


    elif len(bag) > 50:
        page2 = discord.Embed(title="Your inventory (Page 2)",
                              color=discord.Color.random())
        page3 = discord.Embed(title="Your inventory (Page 3)",
                              color=discord.Color.random())
        if user != ctx.author:
            page2.title = f"{user.display_name}'s inventory (Page 2)"
            page3.title = f"{user.display_name}'s inventory (Page 3)"

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
        i = len(bag) - 25
        i2 = len(bag) - 50
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
        paginator = Paginator(ctx.author, pages, pages[0])
        paginator.message = await ctx.reply(embed=pages[0], view=paginator)


async def buy_this(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name or item_name in name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False, 1, name_]

    cost = price * amount
    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0] < cost:
        return [False, 2, name_]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == name_:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item": name_, "amount": amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item": name_, "amount": amount}
        users[str(user.id)]["bag"] = [obj]

    with open("databases/mainbank.json", "w") as f:
        json.dump(users, f, indent=4)

    await update_bank(user, cost * -1, "wallet")

    return [True, "Worked", cost, name_]


@client.command()
async def sell(ctx, amount: Optional[int] = 1, *, item=None):
    await config.open_account(ctx.author)
    if amount < 1:
        return await ctx.reply("You need to sell at least more than one item!")
    if item.lower() == 'all' or item.lower() == 'max':
        bank_data = await get_bank_data()
        inv = bank_data[str(ctx.author.id)]['bag']
        for item in inv:
            pass

    res = await sell_this(ctx.author, item, amount)
    for items in mainshop:
        if items["name"].lower() == item.lower():
            item = items["name"]
    is_animal = False
    animal_obj = ...
    for items in animal_shop:
        for animal in items:
            if animal["name"].lower() == item.lower() or item.lower() in animal['name'].lower():
                is_animal = True
                item = animal["name"]
                animal_obj = animal

    bal = await update_bank(ctx.author)
    if not res[0]:
        if res[1] == 1:
            await ctx.reply(":x: That item isn't in the shop!")
            return
        if res[1] == 2:
            await ctx.reply(f":x: You don't have `{amount}x` {res[2].title()} in your inventory.")
            return
        if res[1] == 3:
            await ctx.reply(f":x: You don't have {res[2].title()} in your inventory.")
            return
    e = discord.Embed(title=f"{ctx.author.name}'s Sale", color=discord.Color.random())
    e.description = f":white_check_mark: You just sold `{amount}x` {res[3].title()} for `{int(res[2]):,} Minions™`!"
    if is_animal:
        e.set_footer(
            text=f"You got {int(res[2] - animal_obj['sell_price']):,} more minions because you had a {bal[3]:,}x booster!")
    await ctx.reply(embed=e)


async def sell_this(user, item_name, amount, price=None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name or item_name in name:
            name_ = name
            if price == None:
                price = 0.7 * item["price"]
            break
    is_animal = False
    for item in animal_shop:
        for animal in item:
            name = animal["name"].lower()
            if name == item_name or item_name in name:
                name_ = name
                is_animal = True
                if price == None:
                    price = animal["sell_price"]
                break

    if name_ == None:
        return [False, 1, name_]
    cost = ...

    users = await get_bank_data()

    bal = await update_bank(user)
    if is_animal:
        cost = price * amount * bal[3]
    else:
        cost = price * amount
    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == name_:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False, 2, name_]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                if users[str(user.id)]["bag"][index]["amount"] == 0:
                    del users[str(user.id)]["bag"][index]
                t = 1
                break
            index += 1
        if t == None:
            return [False, 3, name_]
    except:
        return [False, 3, name_]

    with open("databases/mainbank.json", "w") as f:
        json.dump(users, f, indent=4)

    await update_bank(user, cost, "wallet")

    return [True, "Worked", cost, name_]


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

    users[str(user.id)][mode] += int(change)

    with open('databases/mainbank.json', 'w') as f:
        json.dump(users, f, indent=4)
    bal = users[str(user.id)]['wallet'], users[str(user.id)]['bank'], users[str(user.id)]['max'], users[str(user.id)][
        'booster']
    return bal


@client.command(pass_context=True, aliases=['rguser', 'rgu'])
@commands.is_owner()
async def registeruser(ctx, user: discord.Member):
    id = str(user.id)
    users = await get_bank_data()
    if id not in users:
        await config.open_account(user)
        await ctx.reply(":white_check_mark: They are now registered")
    else:
        await ctx.reply(":x: They already have an account")
        return


@client.command(aliases=['unrg'])
@commands.is_owner()
async def unregisteruser(ctx, user: discord.Member):
    id = str(user.id)
    users = await get_bank_data()
    jobs = await get_job_data()
    lootbox_data = await get_lootbox_data()
    if id not in users:
        await ctx.reply(":x: They don't have an account")
        return
    else:
        del users[str(user.id)]
        del jobs[str(user.id)]
        del lootbox_data[str(user.id)]

        await ctx.reply(":white_check_mark: Ok their account is now deleted.")
        with open('databases/mainbank.json', 'w') as f:
            json.dump(users, f, indent=4)
        with open('databases/jobs.json', 'w') as f:
            json.dump(jobs, f, indent=4)


@client.command()
@commands.is_owner()
async def give(ctx, user: discord.Member, amount: int, area: str = "wallet"):
    id = str(user.id)
    users = await get_bank_data()
    if area != 'bank' and area != 'wallet':
        await ctx.reply(':x: Invalid area.Types: wallet, bank')
        return
    else:
        if id not in users:
            await ctx.reply(":x: That user isn't registered")
        else:
            await ctx.reply(
                f":white_check_mark: Gave {amount} Minions™ to user {user.display_name}'s {area}!"
            )
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
        await ctx.reply('Invalid area.Types: wallet, bank')
        return
    if area == 'bank' and bank_amt < amount:
        await ctx.reply(
            ":x: That makes the user have negative money so this action cannot be done."
        )
        return
    if area == 'wallet' and wallet_amt < amount:
        await ctx.reply(
            ":x: That makes the user have negative money so this action cannot be done."
        )
        return
    else:

        if id not in users:
            await ctx.reply(":white_check_mark: That user isn't registered")
            return
        else:
            await ctx.reply(
                f":white_check_mark: Took {amount} Minions™ from user {user.display_name}'s {area}!"
            )
            if area == 'wallet':
                wallet_amt -= amount
                await update_bank(user, -1 * amount, 'wallet')
            elif area == 'bank':
                bank_amt -= amount
                await update_bank(user, -1 * amount, 'bank')


@client.command()
async def poop(ctx):
    await ctx.reply(
        f"{ctx.author.mention} :poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop::poop:"
    )


@client.command(aliases=['scn'])
@commands.has_permissions(manage_channels=True)
async def set_channel_name(ctx,
                           channel: discord.TextChannel = None,
                           *,
                           new_name):
    if channel == None:
        channel = ctx.channel
    await channel.edit(name=new_name)
    await ctx.reply(":white_check_mark: Done!")


@client.command(aliases=['sb'])
@commands.is_owner()
async def setbooster(ctx, user: discord.Member, amount: int):
    id = str(user.id)
    users = await get_bank_data()
    if id not in users:
        await ctx.reply(":x: That user isn't registered")
    else:
        await ctx.reply(":white_check_mark: Done!")
        users[str(user.id)]["booster"] = amount

        with open('databases/mainbank.json', 'w') as f:
            json.dump(users, f, indent=4)


@client.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def giverole(ctx, user: discord.Member, *, role: discord.Role):
    if role.position > ctx.author.top_role.position:  # if the role is above users top role it sends error
        return await ctx.reply('**:x: | That role is above your top role!**')

    if role.position == ctx.author.top_role.position and ctx.author.id != 717512097725939795:
        await ctx.reply("You can't do this!")
        return
    if role in user.roles:
        await ctx.reply(":x: They already have this rank!")
        return
    else:
        await user.add_roles(role)
        await ctx.reply(
            f":white_check_mark: {user.display_name} has been given a role called: {role.name}"
        )


@client.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def takerole(ctx, user: discord.Member, *, role: discord.Role):
    if role.position > ctx.author.top_role.position:  # if the role is above users top role it sends error
        return await ctx.reply('**:x: | That role is above your top role!**')
    if role in user.roles:
        await user.remove_roles(role)
        await ctx.reply(
            f":white_check_mark: {user.display_name} has lost their {role.name} rank"
        )
    else:
        await ctx.reply(":x: They don't have this role!")


@client.command(aliases=["members"])
async def membercount(ctx):
    delta = datetime.datetime.now()
    embed = discord.Embed(
        title=('Member Count'),
        description=
        (f'There are currently **{ctx.guild.member_count}** members in the server!'
         ),
        timestamp=delta,
        url='',
        color=discord.Color.dark_blue())
    embed.set_footer(text='Our Community')
    await ctx.reply(embed=embed)
    try:
        await ctx.message.delete()
    except:
        pass


@client.command(aliases=["lb", "rich", 'top'])
async def leaderboard(ctx, x: Optional[int] = 10):
    users = await get_bank_data()
    if len(users) < x:
        x = len(users)

    leader_board = {}
    for user in users:
        us = client.get_user(int(user))
        if not us in ctx.guild.members:
            continue
        leader_board[user] = users[user]["wallet"] + users[user]["bank"]

    users_who_are_in = []
    new = dict(sorted(leader_board.items(), key=lambda t: t[::-1]))
    final = sorted(new.items(), key=lambda x: x[1], reverse=True)
    final = dict(final)

    em = discord.Embed(
        title=f"Top {x} Richest People",
        description=
        "This is decided on the basis of raw money in the bank and wallet",
        color=discord.Color(0xfa43ee))
    index = 1
    for key in final.keys():
        member = client.get_user(int(key))
        if key == "717512097725939795" and ctx.author.id != 717512097725939795:
            continue
        name = member.name
        if member in ctx.guild.members:
            em.add_field(name=f"{index}. {name}#{member.discriminator}",
                         value=f"`{int(leader_board[key]):,} Minions™️`",
                         inline=False)
            users_who_are_in.append(member)
            if index == x:
                break
            else:
                index += 1
    em.title = f"Top {len(users_who_are_in)} Richest People In The Server"
    await ctx.reply(embed=em)


@client.command()
async def emojify(ctx, *, text):
    emojis = []
    for s in text.lower():
        if s.isdecimal():
            num2emo = {
                '0': 'zero',
                '1': 'one',
                '2': 'two',
                '3': 'three',
                '4': 'four',
                '5': 'five',
                '6': 'six',
                '7': 'seven',
                '8': 'eight',
                '9': 'nine'
            }
            emojis.append(f':{num2emo.get(s)}:')

        elif s.isalpha():
            emojis.append(f':regional_indicator_{s}:')
        elif s == '!':
            emojis.append(':grey_exclamation:')
        elif s == '?':
            emojis.append(':grey_question:')
        elif s == "#":
            emojis.append(":hash:")
        else:
            emojis.append(s)

    await ctx.reply(' '.join(emojis))


# @client.command()
# @commands.has_permissions(manage_guild=True)
# async def reroll(ctx, message_id: int):
#     gaw_msg = ...
#     try:
#         gaw_msg = await ctx.channel.fetch_message(message_id)
#     except Exception as e:
#         return await ctx.reply(
#             "Cannot find the message with this ID in this channel!")
#     embed = None
#     try:
#         embed = gaw_msg.embeds[0]
#     except:
#         return await ctx.reply("Could not find the giveaway embed!")
#     if gaw_msg.author != client.user:
#         if gaw_msg.embeds[0].title != "New Giveaway!" and gaw_msg.embeds[
#                 0].title != "GIVEAWAY ENDED":
#             return await ctx.reply("This is not a giveaway message!")
#     author = client.get_user(
#         int(gaw_msg.embeds[0].description.split(' is giving away')[0].replace(
#             '<@!', '').replace('>', '').replace('<@','')))
#     await ctx.reply("Picking a random user!")
#     await asyncio.sleep(1)
#     embed.title = "GIVEAWAY ENDED"
#     embed.set_footer(
#         text=
#         f'Giveaway ended at {datetime.datetime.now(ZoneInfo("America/New_York")).strftime("%A, %B %d %Y @ %H:%M:%S %p")}'
#     )
#     with open('databases/giveaways.json') as f: 
#         g = json.load(f)
#     users = []
#     g[str(gaw_msg.id)]['ended'] = True
#     with open('databases/giveaways.json','w') as f: 
#         json.dump(g, f,indent=4)
#     for i in g[str(gaw_msg.id)]['users']:
#         user = client.get_user(int(i))
#         users.append(user)
#     try:
#         winner = random.choice(users)
#     except:
#         if not "Winner: " in embed.description:
#             embed.description += f"\nWinner: None"
#         else:
#             em = embed.description.partition("\nWinner: ")[0]
#         embed.description = em
#         embed.description += f"\nWinner: None"
#         await gaw_msg.edit(embed=embed)
#         await ctx.reply("No one won since no one entered!")
#         return
#     btn = JoinGiveaway(str(gaw_msg.id))
#     for i in btn.children:
#         i.disabled = True
#     prize = gaw_msg.embeds[0].description.partition("\nWinner: ")[0].split(
#         'is giving away')[1].replace(f"\n{len(users)} entrant{'s' if len(users) >1 else ''}",'')[:-2]
#     e = discord.Embed(description="None", color=discord.Color.random())
#     if len(users) == 1:
#         e.description = "1 entrant"
#     else:
#         e.description = f"{len(users)} entrants"
#     if not "Winner: " in embed.description:
#         embed.description += f"\nWinner: {winner.mention}"
#     else:
#         em = embed.description.partition("\nWinner: ")[0]
#         embed.description = em
#         embed.description += f"\nWinner: {winner.mention}"
#     await gaw_msg.edit(embed=embed,view=btn)
#     await ctx.reply(
#         f"YAYYYYY!!!! {winner.mention} has won the giveaway for{prize}!!",
#         embed=e)





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

    await ctx.reply(file=discord.File("pictures/wantedpic.jpeg"))
    await ctx.reply(f"{user.display_name} has a bounty of 100k OMG POGGGGG!")
    await asyncio.sleep(0.5)
    if user == client.user:
        await ctx.reply("Oh no that's me. I gotta RUNNNNN!!!!")
    wanted.close()


@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def guessing(ctx):
    number = random.randint(0, 100)
    channel = ctx.message.channel

    def check(m):
        return m.content is not None and m.author == ctx.author and m.channel == channel

    tries = 10
    for i in range(0, 10):
        await ctx.reply(
            f'Guess a number between 0 and 100. You have {tries} tries left')
        response = await client.wait_for('message', check=check)
        try:
            guess = int(response.content)
        except:
            return await ctx.reply("The game ended because you typed an invalid guess!")
        if i == 9:
            await ctx.reply(
                f"You lost. The number was {number}. Thanks for playing!")
            break
        if guess > number:
            await ctx.reply('Your number is too big!')
            tries -= 1
        elif guess < number:
            await ctx.reply('Your number is too small!')
            tries -= 1
        else:
            await ctx.reply('Correct! You win. Thanks for playing!')
            break
    return


@client.command()
@commands.is_owner()
async def idtouser(ctx, id=None):
    if id is None:
        await ctx.reply("Please enter an id.")
        return
    user = await client.fetch_user(id)
    await ctx.reply(f"Original id:{id}, Username:{user.display_name}")


@idtouser.error
async def idtouser_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.reply("Unknown user")


@client.command()
@commands.is_owner()
async def usertoid(ctx, user: discord.Member = None):
    if user is None:
        await ctx.reply("Please enter a user.")
        return
    else:
        id = user.id
        await ctx.reply(f"Original name:{user.display_name}, id:{id}")


@usertoid.error
async def usertoid_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.reply("Unknown user")


"""{

   'msg_id' : ['user_id','user_id','user_id','user_id']
}
"""


# class JoinGiveaway(discord.ui.View):
#     def __init__(self, msg_id):
#         super().__init__(timeout=None)
#         self.msg_id = msg_id
#     @discord.ui.button(label="Join Giveaway!", style=discord.ButtonStyle.green,custom_id='giveaway:join')
#     async def join(self, button: discord.ui.Button, interaction: discord.Interaction):
#         with open("databases/giveaways.json",'r') as f:
#             g = json.load(f)
#         if str(interaction.user.id) == g[str(self.msg_id)]['author']:
#             return await interaction.response.send_message("You cannot join your own giveaway!",ephemeral=True)
#         if str(interaction.user.id) in g[str(self.msg_id)]['users']:
#             return await interaction.response.send_message("You have already entered the giveaway!",ephemeral=True)
#         g[str(self.msg_id)]['users'].append(str(interaction.user.id))
#         msg, embed = None, None
#         try:
#             channel = client.get_channel(int(g[str(self.msg_id)]['channel']))
#             msg = await channel.fetch_message(int(self.msg_id))
#             embed = msg.embeds[0]
#         except:
#             del g[str(self.msg_id)]
#             with open("databases/giveaways.json",'w') as f:
#                 json.dump(g, f, indent=4)
#             return await interaction.response.send_message("Could not find the giveaway!",ephemeral=True)
#         embed.description = embed.description.split(f"\n{len(g[str(self.msg_id)]['users'])-1} entrant{'s' if len(g[str(self.msg_id)]['users'])-1 != 1 else ''}")[0]
#         embed.description += f"\n{len(g[str(self.msg_id)]['users'])} entrant{'s' if len(g[str(self.msg_id)]['users']) != 1 else ''}"
#         await msg.edit(embed=embed)
#         with open("databases/giveaways.json",'w') as f:
#             json.dump(g, f, indent=4)
#         return await interaction.response.send_message("You have entered the giveaway!",ephemeral=True)

#     @discord.ui.button(label="Leave Giveaway!", style=discord.ButtonStyle.red,custom_id='giveaway:leave')
#     async def leave(self, button: discord.ui.Button, interaction: discord.Interaction):
#         with open("databases/giveaways.json",'r') as f:
#             g = json.load(f)
#         if str(interaction.user.id) in g[str(self.msg_id)]['users']:
#             g[str(self.msg_id)]['users'].pop(g[str(self.msg_id)]['users'].index(str(interaction.user.id)))
#             with open("databases/giveaways.json",'w') as f:
#                 json.dump(g, f, indent=4)  
#             msg, embed = None, None
#             try:
#                 channel = client.get_channel(int(g[str(self.msg_id)]['channel']))
#                 msg = await channel.fetch_message(int(self.msg_id))
#                 embed = msg.embeds[0]
#             except:
#                 del g[str(self.msg_id)]
#                 with open("databases/giveaways.json",'w') as f:
#                     json.dump(g, f, indent=4)
#                 return await interaction.response.send_message("Could not find the giveaway!",ephemeral=True)  
#             embed.description = embed.description.split(f"\n{len(g[str(self.msg_id)]['users'])+1} entrant{'s' if len(g[str(self.msg_id)]['users'])+1 != 1 else ''}")[0]          
#             embed.description += f"\n{len(g[str(self.msg_id)]['users'])} entrant{'s' if len(g[str(self.msg_id)]['users']) != 1 else ''}"
#             await msg.edit(embed=embed)
#             return await interaction.response.send_message("You have left the giveaway!",ephemeral=True)
#         return await interaction.response.send_message("You have not entered the giveaway!",ephemeral=True)     

# @tasks.loop(seconds=1)
# async def check_giveaway_ended():
#     with open('databases/giveaways.json','r') as f:
#         g = json.load(f)
#     time = datetime.datetime.now(ZoneInfo("America/New_York")).timestamp()
#     try:
#         for giveaway in g:
#             i = g[giveaway]
#             if i['ended']:
#                 continue
#             if not time >= i['end']:
#                 continue
#             channel = client.get_channel(int(i['channel']))
#             gaw_msg = None
#             try:
#                 gaw_msg = await channel.fetch_message(int(giveaway))
#             except:
#                 del g[giveaway]
#                 with open('databases/giveaways.json','w') as f: 
#                     json.dump(g, f,indent=4)
#                 continue
#             embed = None
#             try:
#                 embed = gaw_msg.embeds[0]
#             except:
#                 del g[giveaway]
#                 with open('databases/giveaways.json','w') as f: 
#                     json.dump(g, f,indent=4)
#                 continue
#             btn = JoinGiveaway(int(giveaway))
#             await channel.send("Picking a random user!")
#             await asyncio.sleep(1)
#             embed.title = "GIVEAWAY ENDED"
#             for bt in btn.children:
#                 bt.disabled = True
#             g[giveaway]['ended'] = True

#             await gaw_msg.edit(view=btn)
#             embed.set_footer(
#                 text=
#                 f'Giveaway ended at {datetime.datetime.fromtimestamp(i["end"],ZoneInfo("America/New_York")).strftime("%A, %B %d %Y @ %H:%M:%S %p")}'
#             )
#             await gaw_msg.edit(embed=embed)
#             users = []
#             for i in g[str(gaw_msg.id)]['users']:
#                 user = client.get_user(int(i))
#                 users.append(user)
#             try:
#                 winner = random.choice(users)
#             except:
#                 embed.description += f"\nWinner: None"
#                 await gaw_msg.edit(embed=embed)
#                 await channel.send("No one won since no one entered!")
#                 continue
#             e = discord.Embed(description="None", color=discord.Color.random())
#             e.description = f"{len(users)} entrant{'s' if len(users) >1 else ''}"
#             embed.description += f"\nWinner: {winner.mention}"
#             await gaw_msg.edit(embed=embed)
#             prize = gaw_msg.embeds[0].description.partition("\nWinner: ")[0].split(
#             'is giving away')[1].replace(f"\n{len(users)} entrant{'s' if len(users) >1 else ''}",'')[:-2]
#             await channel.send(
#                 f"YAYYYYY!!!! {winner.mention} has won the giveaway for{prize}!!",
#                 embed=e)
#     except RuntimeError:
#         pass
#     with open('databases/giveaways.json','w') as f: 
#         json.dump(g, f,indent=4)


# @client.command()
# @commands.has_permissions(manage_guild=True)
# async def gcreate(ctx, time=None, *, prize=None):
#     with open('databases/server_configs.json', 'r') as f:
#         configs = json.load(f)
#     guild = ctx.guild
#     giveaway_role = guild.get_role(configs[str(ctx.guild.id)]["giveaway_role"])
#     
#     if giveaway_role != None:
#         gaw_msg = await ctx.reply(f"{giveaway_role.mention}", embed=embed)
#     else:
#         gaw_msg = await ctx.reply(embed=embed)
#     with open('databases/giveaways.json') as f: 
#         g = json.load(f)
#     g[str(gaw_msg.id)] = {'author':str(ctx.author.id),'users':[], 'channel':str(ctx.channel.id), 'end':time_stamp.timestamp(),'ended':False}
#     with open('databases/giveaways.json','w') as f:
#         json.dump(g, f, indent=4)
#     btn = JoinGiveaway(gaw_msg.id)

#     await gaw_msg.edit(view=btn)


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member = None, *, reason=None):
    if user == None:
        await ctx.reply("Please enter a user!")
        return

    await user.kick(reason=reason)
    await ctx.reply(f'Kicked {user.name} for reason {reason}')


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member = None, *, reason=None):
    if user == None:
        await ctx.reply("Please enter a user!")
        return

    if ctx.me.top_role.position > ctx.author.top_role.position:
        return await ctx.reply("I cannot ban this user aas they have a higher role than me!")

    if user.top_role.position > ctx.author.top_role.position:
        return await ctx.reply("You cannot ban that user as they have a higher role than you!")

    await user.ban(reason=reason)
    await ctx.reply(f'Banned {user.name} for reason {reason}')


@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
            await ctx.guild.unban(user)
            await ctx.reply(f'Unbanned {user.name}#{user.discriminator}')


@client.command()
@commands.cooldown(1, 300, commands.BucketType.user)
async def bankrob(ctx, user: discord.Member):
    if user.bot:
        bankrob.reset_cooldown(ctx)
        return await ctx.reply(
            "You are not allowed to steal from bots, back off my kind")
    await config.open_account(ctx.author)
    await config.open_account(user)
    bal1 = await update_bank(user)
    bal = await update_bank(ctx.author)
    if bal[0] < 5000:
        bankrob.reset_cooldown(ctx)
        return await ctx.reply("You need at least `5000 Minions™️` to bankrob someone.")
    if user.id == 717512097725939795:
        bankrob.reset_cooldown(ctx)
        return await ctx.reply(
            "xD you can't rob him he is the owner of the bot!!!")
    if bal1[1] < 100:
        await ctx.reply("It's useless to rob their bank!")
        bankrob.reset_cooldown(ctx)
        return
    else:
        earning = random.randrange(0, bal1[1])
        fail_losing = random.randrange(0, int(bal[0] / 2))

        type = random.randint(0, 1)
        if type == 0:
            await ctx.reply(
                f":x: You failed to rob {user} and paid them {fail_losing:,} Minions™!"
            )
            await update_bank(user, fail_losing)
            await update_bank(ctx.author, fail_losing * -1)
        elif type == 1:
            await ctx.reply(
                f":white_check_mark: You successfully robbed {user} and got {earning:,} Minions™!"
            )
            await update_bank(ctx.author, earning)
            await update_bank(user, earning * -1)


@client.command()
async def roles(ctx):
    role_names = await ctx.guild.fetch_roles()
    role_names.sort(reverse=True)
    roles = "\n".join([str(r.mention) for r in role_names][:-1])

    e = discord.Embed(title=f"Roles [{len(role_names) - 1}]",
                      description=roles,
                      color=discord.Color.random())
    await ctx.reply(embed=e,
                    allowed_mentions=discord.AllowedMentions(roles=False))


@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, time: str):
    _time = humanfriendly.parse_timespan(time)
    await member.timeout(timeout=discord.utils.utcnow() + datetime.timedelta(seconds=_time))
    await ctx.reply(f"🔨{member} was muted for {time}.")


@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    if not member.communication_disabled_until:
        return await ctx.reply(f":x:{member} is not muted.")
    await member.timeout(timeout=None)
    await ctx.reply(f":white_check_mark:{member} was unmuted.")


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
        await ctx.reply("Done!")


@client.command()
async def crates(ctx, user: discord.Member = None):
    await config.open_account(ctx.author)
    lootbox_data = await get_lootbox_data()
    if user is None:
        common_amt = lootbox_data[str(ctx.author.id)]["common"]
        uncommon_amt = lootbox_data[str(ctx.author.id)]["uncommon"]
        rare_amt = lootbox_data[str(ctx.author.id)]["rare"]
        epic_amt = lootbox_data[str(ctx.author.id)]["epic"]
        legendary_amt = lootbox_data[str(ctx.author.id)]["legendary"]
        mythic_amt = lootbox_data[str(ctx.author.id)]["mythic"]
        admin_amt = lootbox_data[str(ctx.author.id)]["admin"]
        e = discord.Embed(title=f"{ctx.author.name}'s Crates",
                          color=discord.Color.random())

        e.add_field(name="Common", value=common_amt)
        e.add_field(name="Uncommon", value=uncommon_amt)
        e.add_field(name="Rare", value=rare_amt)
        e.add_field(name="Epic", value=epic_amt)
        e.add_field(name="Legendary", value=legendary_amt)
        e.add_field(name="Mythic", value=mythic_amt)
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
        e = discord.Embed(title=f"{user.name}'s Crates",
                          color=discord.Color.random())

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
async def crateinfo(ctx):
    e = discord.Embed(
        title="Crate Info",
        description="These are the loot tables for all the crates.",
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
    total_lootboxes = lootbox_data[str(user.id)]["common"] + lootbox_data[str(
        user.id)]["uncommon"] + lootbox_data[str(
        user.id)]["rare"] + lootbox_data[str(
        user.id)]["epic"] + lootbox_data[str(
        user.id)]["legendary"] + lootbox_data[str(
        user.id)]["mythic"] + lootbox_data[str(
        user.id)]["admin"]

    if amount == None:
        amount = 1

    types = [
        "admin", "common", "c", "uncommon", "u", "rare", "r", "epic",
        "legendary", "l", "mythic", "m", "all", "a", "e"
    ]
    if type == None:
        await ctx.reply("Please enter something to open")
        return
    elif type.lower() not in types:
        await ctx.reply("Invalid crate type")
        return
    elif total_lootboxes == 0:
        await ctx.reply("You have no lootboxes to open")
        return
    if str(amount).lower() == 'a' or str(amount).lower() == 'all':
        if type.lower() == 'admin' or type.lower() == 'a':
            amt = lootbox_data[str(user.id)]["admin"]
            if amt == 0:
                await ctx.reply("You have no admin lootboxes!")
                return
            amounts = []
            for x in range(0, amt):
                amountofcash = random.randint(900000, 1000000)
                amounts.append(amountofcash)
            total_cash = sum(amounts)
            e = discord.Embed(title=f"{ctx.author.name}'s Crates",
                              color=discord.Color.random())
            e.add_field(
                name=f"{ctx.author.name}'s crate opening session!",
                value=
                f"You opened {amt} **Admin** {'crate' if amt == 1 else 'crates'} <:chest:898333946557894716> and got `{total_cash:,} Minions™`!!! :tada:"
            )
            await update_bank(ctx.author, total_cash)
            await ctx.reply(embed=e)
            lootbox_data[str(user.id)]["admin"] -= amt
            with open('databases/lootboxes.json', 'w') as f:
                json.dump(lootbox_data, f, indent=4)

        elif type.lower() == 'mythic' or type.lower() == 'm':
            amt = lootbox_data[str(user.id)]["mythic"]
            if amt == 0:
                await ctx.reply("You have no mythic lootboxes!")
                return
            amounts = []
            for x in range(0, amt):
                amountofcash = random.randint(200000, 300000)
                amounts.append(amountofcash)
            total_cash = sum(amounts)
            e = discord.Embed(title=f"{ctx.author.name}'s Crates",
                              color=discord.Color.random())
            e.add_field(
                name=f"{ctx.author.name}'s crate opening session!",
                value=
                f"You opened {amt} **Mythic** {'crate' if amt == 1 else 'crates'} <:chest:898333946557894716> and got `{total_cash:,} Minions™`!!! :tada:"
            )
            await update_bank(ctx.author, total_cash)
            await ctx.reply(embed=e)
            lootbox_data[str(user.id)]["mythic"] -= amt
            with open('databases/lootboxes.json', 'w') as f:
                json.dump(lootbox_data, f, indent=4)

        elif type.lower() == 'legendary' or type.lower() == 'l':
            amt = lootbox_data[str(user.id)]["legendary"]
            if amt == 0:
                await ctx.reply("You have no legendary lootboxes!")
                return
            amounts = []
            for x in range(0, amt):
                amountofcash = random.randint(100000, 200000)
                amounts.append(amountofcash)
            total_cash = sum(amounts)
            e = discord.Embed(title=f"{ctx.author.name}'s Crates",
                              color=discord.Color.random())
            e.add_field(
                name=f"{ctx.author.name}'s crate opening session!",
                value=
                f"You opened {amt} **Legendary** {'crate' if amt == 1 else 'crates'} <:chest:898333946557894716> and got `{total_cash:,} Minions™`!!! :tada:"
            )
            await update_bank(ctx.author, total_cash)
            await ctx.reply(embed=e)
            lootbox_data[str(user.id)]["legendary"] -= amt
            with open('databases/lootboxes.json', 'w') as f:
                json.dump(lootbox_data, f, indent=4)

        elif type.lower() == 'epic' or type.lower() == 'e':
            amt = lootbox_data[str(user.id)]["epic"]
            if amt == 0:
                await ctx.reply("You have no epic lootboxes!")
                return
            amounts = []
            for x in range(0, amt):
                amountofcash = random.randint(50000, 100000)
                amounts.append(amountofcash)
            total_cash = sum(amounts)
            e = discord.Embed(title=f"{ctx.author.name}'s Crates",
                              color=discord.Color.random())
            e.add_field(
                name=f"{ctx.author.name}'s crate opening session!",
                value=
                f"You opened {amt} **Epic** {'crate' if amt == 1 else 'crates'} <:chest:898333946557894716> and got `{total_cash:,} Minions™`!!! :tada:"
            )
            await update_bank(ctx.author, total_cash)
            await ctx.reply(embed=e)
            lootbox_data[str(user.id)]["epic"] -= amt
            with open('databases/lootboxes.json', 'w') as f:
                json.dump(lootbox_data, f, indent=4)

        elif type.lower() == 'rare' or type.lower() == 'r':
            amt = lootbox_data[str(user.id)]["rare"]
            if amt == 0:
                await ctx.reply("You have no rare lootboxes!")
                return
            amounts = []
            for x in range(0, amt):
                amountofcash = random.randint(30000, 50000)
                amounts.append(amountofcash)
            total_cash = sum(amounts)
            e = discord.Embed(title=f"{ctx.author.name}'s Crates",
                              color=discord.Color.random())
            e.add_field(
                name=f"{ctx.author.name}'s crate opening session!",
                value=
                f"You opened {amt} **Rare** {'crate' if amt == 1 else 'crates'} <:chest:898333946557894716> and got `{total_cash:,} Minions™`!!! :tada:"
            )
            await update_bank(ctx.author, total_cash)
            await ctx.reply(embed=e)
            lootbox_data[str(user.id)]["rare"] -= amt
            with open('databases/lootboxes.json', 'w') as f:
                json.dump(lootbox_data, f, indent=4)

        elif type.lower() == 'uncommon' or type.lower() == 'u':
            amt = lootbox_data[str(user.id)]["uncommon"]
            if amt == 0:
                await ctx.reply("You have no uncommon lootboxes!")
                return
            amounts = []
            for x in range(0, amt):
                amountofcash = random.randint(5000, 10000)
                amounts.append(amountofcash)
            total_cash = sum(amounts)
            e = discord.Embed(title=f"{ctx.author.name}'s Crates",
                              color=discord.Color.random())
            e.add_field(
                name=f"{ctx.author.name}'s crate opening session!",
                value=
                f"You opened {amt} **Uncommon** {'crate' if amt == 1 else 'crates'} <:chest:898333946557894716> and got `{total_cash:,} Minions™`!!! :tada:"
            )
            await update_bank(ctx.author, total_cash)
            await ctx.reply(embed=e)
            lootbox_data[str(user.id)]["uncommon"] -= amt
            with open('databases/lootboxes.json', 'w') as f:
                json.dump(lootbox_data, f, indent=4)

        elif type.lower() == "common" or type.lower() == "c":
            amt = lootbox_data[str(user.id)]["common"]
            if amt == 0:
                await ctx.reply("You have no common lootboxes!!")
                return
            amounts = []
            for x in range(0, amt):
                amountofcash = random.randint(2000, 5000)
                amounts.append(amountofcash)

            total_cash = sum(amounts)
            e = discord.Embed(title=f"{ctx.author.name}'s Crates",
                              color=discord.Color.random())
            e.add_field(
                name=f"{ctx.author.name}'s crate opening session!",
                value=
                f"You opened {amt} **Common** {'crate' if amt == 1 else 'crates'} <:chest:898333946557894716> and got `{total_cash:,} Minions™`!!! :tada:"
            )
            await update_bank(ctx.author, total_cash)
            await ctx.reply(embed=e)
            lootbox_data[str(user.id)]["common"] -= amt
            with open('databases/lootboxes.json', 'w') as f:
                json.dump(lootbox_data, f, indent=4)
        return

    amount = int(amount)
    if type.lower() == 'all':
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

        e = discord.Embed(title=f"{ctx.author.name}'s Crates",
                          color=discord.Color.random())
        e.add_field(
            name=f"{ctx.author.name}'s crate opening session!",
            value=
            f"You opened {len(amounts)} {'crate' if len(amounts) == 1 else 'crates'} <:chest:898333946557894716> and got `{sum(amounts)} Minions™`!!! :tada:"
        )
        await ctx.reply(embed=e)
        await update_bank(ctx.author, sum(amounts))
        with open('databases/lootboxes.json', 'w') as f:
            json.dump(lootbox_data, f, indent=4)
        return

    if type.lower() == "admin" or type.lower() == 'a':
        if amount > lootbox_data[str(user.id)]["admin"]:
            await ctx.reply("You don't have that many lootboxes!!")
            return
        amounts = []
        for x in range(0, amount):
            amountofcash = random.randint(900000, 1000000)
            amounts.append(amountofcash)

        total_cash = sum(amounts)
        e = discord.Embed(title=f"{ctx.author.name}'s Crates",
                          color=discord.Color.random())
        e.add_field(
            name=f"{ctx.author.name}'s crate opening session!",
            value=
            f"You opened {amount} **Admin** {'crate' if amount == 1 else 'crates'} <:chest:898333946557894716> and got `{total_cash:,} Minions™`!!! :tada:"
        )
        await update_bank(ctx.author, total_cash)
        await ctx.reply(embed=e)
        lootbox_data[str(user.id)]["admin"] -= amount
        with open('databases/lootboxes.json', 'w') as f:
            json.dump(lootbox_data, f, indent=4)

    if type.lower() == "mythic" or type.lower() == "m":
        if amount > lootbox_data[str(user.id)]["mythic"]:
            await ctx.reply("You don't have that many lootboxes!!")
            return
        amounts = []
        for x in range(0, amount):
            amountofcash = random.randint(200000, 300000)
            amounts.append(amountofcash)

        total_cash = sum(amounts)
        e = discord.Embed(title=f"{ctx.author.name}'s Crates",
                          color=discord.Color.random())
        e.add_field(
            name=f"{ctx.author.name}'s crate opening session!",
            value=
            f"You opened {amount} **Mythic** {'crate' if amount == 1 else 'crates'} <:chest:898333946557894716> and got `{total_cash:,} Minions™`!!! :tada:"
        )
        await update_bank(ctx.author, total_cash)
        await ctx.reply(embed=e)
        lootbox_data[str(user.id)]["mythic"] -= amount
        with open('databases/lootboxes.json', 'w') as f:
            json.dump(lootbox_data, f, indent=4)

    if type.lower() == "legendary" or type.lower() == "l":
        if amount > lootbox_data[str(user.id)]["legendary"]:
            await ctx.reply("You don't have that many lootboxes!!")
            return
        amounts = []
        for x in range(0, amount):
            amountofcash = random.randint(100000, 200000)
            amounts.append(amountofcash)

        total_cash = sum(amounts)
        e = discord.Embed(title=f"{ctx.author.name}'s Crates",
                          color=discord.Color.random())
        e.add_field(
            name=f"{ctx.author.name}'s crate opening session!",
            value=
            f"You opened {amount} **Legendary** {'crate' if amount == 1 else 'crates'} <:chest:898333946557894716> and got `{total_cash:,} Minions™`!!! :tada:"
        )
        await update_bank(ctx.author, total_cash)
        await ctx.reply(embed=e)
        lootbox_data[str(user.id)]["legendary"] -= amount
        with open('databases/lootboxes.json', 'w') as f:
            json.dump(lootbox_data, f, indent=4)

    if type.lower() == "epic" or type.lower() == "e":
        if amount > lootbox_data[str(user.id)]["epic"]:
            await ctx.reply("You don't have that many lootboxes!!")
            return
        amounts = []
        for x in range(0, amount):
            amountofcash = random.randint(50000, 100000)
            amounts.append(amountofcash)

        total_cash = sum(amounts)
        e = discord.Embed(title=f"{ctx.author.name}'s Crates",
                          color=discord.Color.random())
        e.add_field(
            name=f"{ctx.author.name}'s crate opening session!",
            value=
            f"You opened {amount} **Epic** {'crate' if amount == 1 else 'crates'} <:chest:898333946557894716> and got `{total_cash:,} Minions™`!!! :tada:"
        )
        await update_bank(ctx.author, total_cash)
        await ctx.reply(embed=e)
        lootbox_data[str(user.id)]["epic"] -= amount
        with open('databases/lootboxes.json', 'w') as f:
            json.dump(lootbox_data, f, indent=4)

    if type.lower() == "rare" or type.lower() == "r":
        if amount > lootbox_data[str(user.id)]["rare"]:
            await ctx.reply("You don't have that many lootboxes!!")
            return
        amounts = []
        for x in range(0, amount):
            amountofcash = random.randint(30000, 50000)
            amounts.append(amountofcash)

        total_cash = sum(amounts)
        e = discord.Embed(title=f"{ctx.author.name}'s Crates",
                          color=discord.Color.random())
        e.add_field(
            name=f"{ctx.author.name}'s crate opening session!",
            value=
            f"You opened {amount} **Rare** {'crate' if amount == 1 else 'crates'} <:chest:898333946557894716> and got `{total_cash:,} Minions™`!!! :tada:"
        )
        await update_bank(ctx.author, total_cash)
        await ctx.reply(embed=e)
        lootbox_data[str(user.id)]["rare"] -= amount
        with open('databases/lootboxes.json', 'w') as f:
            json.dump(lootbox_data, f, indent=4)

    if type.lower() == "uncommon" or type.lower() == "u":
        if amount > lootbox_data[str(user.id)]["uncommon"]:
            await ctx.reply("You don't have that many lootboxes!!")
            return
        amounts = []
        for x in range(0, amount):
            amountofcash = random.randint(5000, 10000)
            amounts.append(amountofcash)

        total_cash = sum(amounts)
        e = discord.Embed(title=f"{ctx.author.name}'s Crates",
                          color=discord.Color.random())
        e.add_field(
            name=f"{ctx.author.name}'s crate opening session!",
            value=
            f"You opened {amount} **Uncommon** {'crate' if amount == 1 else 'crates'} <:chest:898333946557894716> and got `{total_cash:,} Minions™`!!! :tada:"
        )
        await update_bank(ctx.author, total_cash)
        await ctx.reply(embed=e)
        lootbox_data[str(user.id)]["uncommon"] -= amount
        with open('databases/lootboxes.json', 'w') as f:
            json.dump(lootbox_data, f, indent=4)

    if type.lower() == "common" or type.lower() == "c":
        if amount > lootbox_data[str(user.id)]["common"]:
            await ctx.reply("You don't have that many lootboxes!!")
            return
        amounts = []
        for x in range(0, amount):
            amountofcash = random.randint(2000, 5000)
            amounts.append(amountofcash)

        total_cash = sum(amounts)
        e = discord.Embed(title=f"{ctx.author.name}'s Crates",
                          color=discord.Color.random())
        e.add_field(
            name=f"{ctx.author.name}'s crate opening session!",
            value=
            f"You opened {amount} **Common** {'crate' if amount == 1 else 'crates'} <:chest:898333946557894716> and got `{total_cash:,} Minions™`!!! :tada:"
        )
        await update_bank(ctx.author, total_cash)
        await ctx.reply(embed=e)
        lootbox_data[str(user.id)]["common"] -= amount
        with open('databases/lootboxes.json', 'w') as f:
            json.dump(lootbox_data, f, indent=4)


@opencrate.error
async def crate_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.reply("Your amount can't be text or a number with a decimal!"
                        )
        return


@client.command()
async def num2text(ctx, num: int = None):
    if num is None:
        await ctx.reply("Please enter a number!")
        return
    if num >= 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000:
        await ctx.reply("Too big of a number!")
        return
    if len(num2words(num).capitalize()) > 4096:
        await ctx.reply("Too big of a number!")
        return

    new = num2words(num).capitalize()
    e = discord.Embed(title=":capital_abcd: Numbers to words",
                      description=f"**Input**:{num}\n\n**Output**:{new}",
                      color=discord.Color.random())
    e.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
    await ctx.reply(embed=e)


@client.command()
async def reverse(ctx, *, msg=None):
    if msg is None:
        await ctx.reply("Please enter a message!")
        return
    t_rev = msg[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
    await ctx.reply(f"**🔁 Text ==> txeT | {ctx.author}**\n```{t_rev}```")


@client.command()
async def dogfact(ctx):
    async with aiohttp.ClientSession() as ses:
        async with ses.get('http://some-random-api.ml/facts/dog') as r:
            if r.status in range(200, 299):
                data = await r.json()
                fact = data['fact']
                em = discord.Embed(title='Dog Fact',
                                   description=f'{fact}',
                                   color=discord.Color.random())
                await ctx.reply(embed=em)
                await ses.close()
            else:
                await ctx.reply("Error when making request...")
                await ses.close()


@client.command()
async def jail(ctx, user: discord.Member = None):
    loading = await ctx.reply("<a:loading:898340114164490261>")
    if user is None:
        user = ctx.author
    async with aiohttp.ClientSession() as trigSession:
        async with trigSession.get(
                f'https://some-random-api.ml/canvas/jail?avatar={user.display_avatar.with_size(1024)}'
        ) as trigImg:  # get users avatar as png with 1024 size
            if trigImg.status in range(200, 299):
                imageData = BytesIO(await
                                    trigImg.read())  # read the image/bytes
                await trigSession.close()  # closing the session and;
                await ctx.reply(file=discord.File(imageData, 'image.png'))
                await loading.delete()
            else:
                await ctx.reply("Error when making request...")
                await trigSession.close()


@client.command(aliases=["trigger"])
async def triggered(ctx, user: discord.Member = None):
    loading = await ctx.reply("<a:loading:898340114164490261>")
    if user is None:
        user = ctx.author
    async with aiohttp.ClientSession() as trigSession:
        async with trigSession.get(
                f'https://some-random-api.ml/canvas/triggered?avatar={user.display_avatar.with_size(1024)}'
        ) as trigImg:
            if trigImg.status in range(200, 299):
                imageData = BytesIO(await
                                    trigImg.read())  # read the image/bytes
                await trigSession.close()  # closing the session and;
                await ctx.reply(file=discord.File(imageData, 'triggered.gif'))
                await loading.delete()
            else:
                await ctx.reply("Error when making request...")
                await trigSession.close()


@client.command()
async def joke(ctx):
    async with aiohttp.ClientSession as ses:
        async with ses.get('https://some-random-api.ml/joke') as r:
            if r.status in range(200, 299):
                data = await r.json()
                fact = data['joke']
                em = discord.Embed(title='Joke',
                                   description=f'{fact}',
                                   color=discord.Color.random())
                await ctx.reply(embed=em)
                await ses.close()
            else:
                await ctx.reply("Error when making request...")
                await ses.close()


@client.command()
@commands.has_permissions(manage_roles=True)
async def reactrole(ctx,
                    emoji=None,
                    role: discord.Role = None,
                    *,
                    message=None):
    prefix = await config.get_prefix(client, ctx.guild.id)

    if emoji == None or role == None or message == None and ctx.author.id == ctx.guild.owner_id:
        return await ctx.reply(
            f"Please enter an emoji role or message! The way you make a reaction role is `{prefix}reactrole <emoji> <role> <message>`."
        )

    if role.position >= ctx.me.top_role.position:
        return await ctx.reply(
            "I can't make a reaction role for that role because it is above or is my top role!"
        )

    emb = discord.Embed(description=message,
                        color=discord.Color.random(),
                        title="New Reaction Role!")
    emb.set_footer(text=f"Reacting will give you the {role.name} role!")
    try:
        await ctx.message.delete()
    except:
        pass
    msg = await ctx.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('databases/reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {
            'role_name': role.name,
            'role_id': role.id,
            'emoji': emoji,
            'message_id': msg.id
        }

        data.append(new_react_role)

    with open('databases/reactrole.json', 'w') as f:
        json.dump(data, f, indent=4)


async def dump_mainbank_data(data):
    with open('databases/mainbank.json', 'w') as f:
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
        await ctx.reply("Please enter a name!")
        return

    genderify = await http.get(f"https://api.genderize.io?name={name.lower()}",
                               res_method="json")
    if str(genderify["gender"]) == "None":
        return await ctx.reply("I don't have a gender for that name!")

    e = discord.Embed(title="Genderify",
                      description="I will guess the gender of a name!",
                      color=discord.Color.random())
    e.add_field(name="Name",
                value=genderify["name"].capitalize(),
                inline=False)
    e.add_field(name="Gender",
                value=genderify["gender"].capitalize(),
                inline=False)
    e.add_field(name="Probability",
                value=f"{genderify['probability'] * 100}%",
                inline=False)
    e.add_field(name="Count", value=genderify["count"])

    await ctx.reply("I have guessed the gender!!", embed=e)


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
    await ctx.reply(
        "Type as many characters you can in 30 seconds! I will tell you when to send the message for it to be counted."
    )
    await asyncio.sleep(1)
    countdown = await ctx.reply("3")
    await asyncio.sleep(1)
    await countdown.edit("2")
    await asyncio.sleep(1)
    await countdown.edit("1")
    await asyncio.sleep(1)
    await countdown.edit("TYPE!!!!")
    new_countdown = await ctx.reply("30")
    for num in range(30, -1, -1):
        await new_countdown.edit(f"{num}")
        await asyncio.sleep(1)
    await ctx.reply("Times up!")
    await ctx.reply(
        "Please send you message within 3 seconds or your run is disqualified!"
    )
    user_msg = None
    try:
        user_msg = await client.wait_for(
            'message',
            timeout=3,
            check=lambda message: message.author == ctx.author and message.
            channel == ctx.channel)
    except asyncio.TimeoutError:
        return await ctx.reply("You ran out of time to submit your message! :(")
    if len(user_msg.content) >= 1200:
        return await ctx.reply(
            "I know you didn't type all of this in a legit way...")
    await ctx.reply(
        f"Your message was **{len(user_msg.content)}** characters long!! :tada: :tada:"
    )


@client.command()
async def eadd(ctx, url: str = None, *, name=None):
    guild = ctx.guild
    if ctx.author.id == ctx.guild.owner_id:
        if name == None:
            return await ctx.reply("Please enter a name for the emoji!")
        if url == None:
            return await ctx.reply(
                "Please enter the url of the emoji you want to add to your server!"
            )
        try:
            async with aiohttp.ClientSession() as ses:
                async with ses.get(url) as r:
                    try:
                        imgOrGif = BytesIO(await r.read())
                        bValue = imgOrGif.getvalue()
                        if r.status in range(200, 299):
                            emoji = await guild.create_custom_emoji(image=bValue,
                                                                    name=name)
                            await ctx.reply(":white_check_mark: Emoji created!")
                            await ses.close()
                        else:
                            await ctx.reply(f"This id not work -_- | {r.status}")
                    except discord.HTTPException:
                        await ctx.reply("The file is too thicc :(")
        except:
            return await ctx.reply("Invalid URL!")
    else:
        await ctx.reply("Only server owners can create custom emojis!")


def calculator(exp):
    o = exp.replace('x', '*')
    o = o.replace('÷', '/')
    result = 0
    try:
        result = str(eval(o))
    except:
        result = "An error occurred"
    return result


@client.command()
async def sqrt(ctx, *, expression):
    try:
        return await ctx.reply(
            f"The square root \u221A of the expression/number {expression} is\n{math.sqrt(float(calculator(expression)))}"
        )
    except Exception as e:
        return await ctx.reply(f"An error occurred :( . ({e})")


@client.command()
@commands.is_owner()
async def exit(ctx):
    await ctx.reply("Logging out now...")
    await asyncio.sleep(1)
    await client.close()


@client.command()
async def gay(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    if user.id == 717512097725939795 and ctx.author != user:
        await ctx.reply(f"{ctx.author.mention} he's not gay, you are.")
        return
    loading = await ctx.reply("<a:loading:898340114164490261>")
    async with aiohttp.ClientSession() as gaySession:
        async with gaySession.get(
                f'https://some-random-api.ml/canvas/gay?avatar={user.display_avatar.url}'
        ) as gayImg:
            if gayImg.status in range(
                    200, 299):  # get users avatar as png with 1024 size
                imageData = BytesIO(await
                                    gayImg.read())  # read the image/bytes
                await gaySession.close()  # closing the session and;
                await ctx.reply(file=discord.File(imageData, 'gay.png')
                                )  # sending the file
                await loading.delete()
            else:
                await ctx.reply(
                    "An error occurred while fetching from the api! :(")


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
@commands.cooldown(1, 20, commands.BucketType.user)
async def hunt(ctx):
    vowels = ["a", "e", "i", "o", "u"]
    users = await get_bank_data()
    prefix = await config.get_prefix(client, ctx.guild.id)
    user = ctx.author
    has_weapon = False
    try:
        users[str(user.id)]['bag']
    except KeyError:
        users[str(user.id)]['bag'] = []
    for item in users[str(user.id)]["bag"]:
        if item["item"] == "hunting sniper":
            has_weapon = True
            break
        else:
            has_weapon = False
    if not has_weapon:
        hunt.reset_cooldown(ctx)
        return await ctx.reply(
            f"You don't have a hunting sniper! Buy one by doing `{prefix}buy hunting sniper`!"
        )
    chance = random.choice([0, 1, 2, 3])
    if chance != 0:
        return await ctx.reply("LOL all the animals ran away.")
    animal = random.choice(animal_shop[0] + animal_shop[2])
    if animal["name"][0].lower() in vowels:
        await ctx.reply(
            f"You went hunting in the woods and managed to kill an **{animal['name']}**!!"
        )
    else:
        await ctx.reply(
            f"You went hunting in the woods and managed to kill a **{animal['name']}**!!"
        )
    await give_animal(user, animal)


@client.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def fish(ctx):
    vowels = ["a", "e", "i", "o", "u"]
    special = ["garbage", "donald duck", "nemo"]
    users = await get_bank_data()
    prefix = await config.get_prefix(client, ctx.guild.id)
    user = ctx.author
    has_weapon = False
    try:
        users[str(user.id)]['bag']
    except KeyError:
        users[str(user.id)]['bag'] = []
    for item in users[str(user.id)]["bag"]:
        if item["item"] == "fishing rod":
            has_weapon = True
            break
        else:
            has_weapon = False
    if not has_weapon:
        fish.reset_cooldown(ctx)
        return await ctx.reply(
            f"You don't have a fishing rod! Buy one by doing `{prefix}buy fishing rod`!"
        )
    chance = random.choice([0, 1, 2, 3])
    if chance != 0:
        return await ctx.reply("LOL all the animals swam away.")
    animal = random.choice(animal_shop[1])
    if animal["name"][0].lower() in vowels:
        await ctx.reply(
            f"You went fishing in the ocean and managed to catch an **{animal['name']}**!!"
        )
    elif animal["name"].lower() in special:
        await ctx.reply(
            f"You went fishing in the ocean and managed to catch **{animal['name']}**!!"
        )
    else:
        await ctx.reply(
            f"You went fishing in the ocean and managed to catch a **{animal['name']}**!!"
        )
    await give_animal(user, animal)


@client.command()
async def gayrate(ctx, user: discord.Member):
    if user.id == 717512097725939795:
        percent = 0
    else:
        percent = random.randint(0, 100)
    e = discord.Embed(
        title="gay r8t machine",
        color=discord.Color.random(),
        description=f"{user.name} is {percent}% gay :gay_pride_flag:")
    await ctx.reply(embed=e)


@client.command()
async def credits(ctx):
    e = discord.Embed(
        title="Credits",
        description="These are all the things that made this bot!",
        color=discord.Color.random())
    p1 = await client.fetch_user(859310142633803806)
    creator = await client.fetch_user(int(config.getenv("BOT_OWNER_ID")))
    e.add_field(name='The Creator Of Basically Everything In This Bot',
                value=creator,
                inline=False)
    e.add_field(name="Creature ideas for when hunting or fishing",
                value=p1,
                inline=False)
    e.add_field(name="Starter Code",
                value="https://github.com/AyushSehrawat/Economy-Bot")
    await ctx.reply(embed=e)


@client.command(aliases=['conf', 'config'])
@commands.has_permissions(manage_guild=True)
async def config_cmd(ctx):
    with open('databases/server_configs.json', 'r') as f:
        configs = json.load(f)

    role = ctx.guild.get_role(configs[str(ctx.guild.id)]["giveaway_role"])
    mod_role = ctx.guild.get_role(configs[str(ctx.guild.id)]["mod_role"])
    e = discord.Embed(title="Your Server Configurations",
                      color=discord.Color.random())
    e.add_field(name="Giveaway Role", value=role.mention if role else role)
    e.add_field(name="Mod Role (Tickets)", value=mod_role.mention if mod_role else mod_role)
    await ctx.reply(embed=e,
                    allowed_mentions=discord.AllowedMentions(roles=False))
    await asyncio.sleep(1)
    await ctx.reply("Would you like to change the config? y/n")
    change_config = None
    try:
        change_config = await client.wait_for(
            'message',
            timeout=20,
            check=lambda message: message.author == ctx.author and message.
            channel == ctx.message.channel)
    except asyncio.TimeoutError:
        return
    change_config = change_config.content
    if change_config.lower() == "n":
        return await ctx.reply("Okay! I won't change anything.")
    elif change_config.lower() == 'y':
        await ctx.reply("Choose a configuration to change:")
        await ctx.reply(
            "Type `1` to change the giveaway role.\nType `2` to toggle the leveling system.\nType `3` to change the mod role."
        )
        change_config_type = ...
        try:
            change_config_type = await client.wait_for(
                'message',
                timeout=20,
                check=lambda message: message.author == ctx.author and message.
                channel == ctx.message.channel)
        except asyncio.TimeoutError:
            return
        change_config_type = int(change_config_type.content.lower().strip())
        if change_config_type == 1:
            await ctx.reply(
                "Mention the new role in your next message. (Or type None)")
            new_role = ...
            try:
                new_role = await client.wait_for(
                    'message',
                    timeout=20,
                    check=lambda message: message.author == ctx.author and
                                          message.channel == ctx.message.channel)
                if new_role.content.lower() == "none":
                    configs[str(ctx.guild.id)]['giveaway_role'] = "None"
                else:
                    new_role = discord.utils.get(ctx.guild.roles,
                                                 id=int(
                                                     new_role.content.replace(
                                                         "<@&",
                                                         "").replace(">", "")))
                    configs[str(ctx.guild.id)]['giveaway_role'] = new_role.id

            except asyncio.TimeoutError:
                return
            except ValueError:
                return await ctx.reply("Invalid Role.")
            await ctx.reply("Done!")
        elif change_config_type == 2:
            await ctx.reply("Enter the new value (true|on/false|off)")
            new_val = ...
            try:
                new_val = await client.wait_for(
                    'message',
                    timeout=20,
                    check=lambda message: message.author == ctx.author and
                                          message.channel == ctx.message.channel)
                configs[str(ctx.guild.id)]['levels'] = new_val.content.lower(
                ) == 'true' or new_val.content.lower() == "on"

            except asyncio.TimeoutError:
                return
            await ctx.reply("Done!")
        elif change_config_type == 3:
            await ctx.reply(
                "Mention the new role in your next message. (Or type None)")
            new_role = ...
            try:
                new_role = await client.wait_for(
                    'message',
                    timeout=20,
                    check=lambda message: message.author == ctx.author and
                                          message.channel == ctx.message.channel)
                if new_role.content.lower() == "none":
                    configs[str(ctx.guild.id)]['mod_role'] = "None"
                else:
                    new_role = discord.utils.get(ctx.guild.roles,
                                                 id=int(
                                                     new_role.content.replace(
                                                         "<@&",
                                                         "").replace(">", "")))
                    configs[str(ctx.guild.id)]['mod_role'] = new_role.id

            except asyncio.TimeoutError:
                return
            except ValueError:
                return await ctx.reply("Invalid Role.")
            await ctx.reply("Done!")
        else:
            await ctx.reply("Invalid config type!")
    else:
        await ctx.reply("Invalid response.")

    with open('databases/server_configs.json', 'w') as f:
        json.dump(configs, f, indent=4)

        # Main code ends


####################################################################
####################################################################

for filename in os.listdir("cogs"):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

token = config.getenv("BOT_TOKEN")
client.run(token)
