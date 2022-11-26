import asyncio
import base64
import json
import random
import re
import string
import time
import urllib.parse
import urllib.request
from io import BytesIO

import aiohttp
import nextcord as discord
from easy_pil import Editor, load_image_async
from googleapiclient.discovery import build
from nextcord import SlashOption, Interaction
from nextcord.ext import commands
from num2words import num2words
import cooldowns

from src.utils import http, functions


class DropdownImageSelect(discord.ui.Select):
    def __init__(self, message, images, user):
        self.message = message
        self.images = images
        self.user = user

        options = [
            discord.SelectOption(label="1"),
            discord.SelectOption(label="2"),
            discord.SelectOption(label="3"),
            discord.SelectOption(label="4"),
            discord.SelectOption(label="5"),
            discord.SelectOption(label="6"),
            discord.SelectOption(label="7"),
            discord.SelectOption(label="8"),
            discord.SelectOption(label="9"),
        ]
        super().__init__(
            placeholder="Choose the image you want to see!",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        if not int(self.user) == int(interaction.user.id):
            return await interaction.response.send_message("You are not the owner of this select!", ephemeral=True)
        selection = int(self.values[0]) - 1
        image = BytesIO(base64.decodebytes(self.images[selection].encode("utf-8")))
        return await self.message.edit(content="Images generated by **https://craiyon.com**",
                                       file=discord.File(image, filename="generatedImage.png"),
                                       view=DropdownImageView(self.message, self.images, self.user))


class DropdownImageView(discord.ui.View):
    def __init__(self, message, images, user):
        super().__init__()
        self.message = message
        self.images = images
        self.user = user
        self.add_item(DropdownImageSelect(self.message, self.images, self.user))


def get_hacking_text(user):
    return {
        "Trying To Access Discord Files... [▓  ]": 0.9,
        "Trying To Access Discord Files... [▓▓  ]": 0.9,
        "Trying To Access Discord Files... [▓▓▓ ]": 0.9,
        "Trying To Access Discord Files... [▓▓▓▓ ]": 0.9,
        "Trying To Access Discord Files... [▓▓▓▓▓]": 0.9,
        "Successfully Accessed Discord Files! [▓▓▓▓▓]": 0.9,
        "Trying to Access Discord Files... SUCCESS": 1,
        "Trying To Access Discord/users... [▓  ]": 1.5,
        "Trying To Access Discord/users... [▓▓  ]": 1.5,
        "Trying To Access Discord/users... [▓▓▓ ]": 1.5,
        "Trying To Access Discord/users... [▓▓▓▓ ]": 1.5,
        "Trying To Access Discord/users... [▓▓▓▓▓]": 1.5,
        "Successfully Got Access to Discord/users! [▓▓▓▓▓]": 1.5,
        "Trying to Access Discord/users... SUCCESS": 1,
        f"Trying To Access Discord/users/{user.id}... [▓  ]": 1.5,
        f"Trying To Access Discord/users/{user.id}... [▓▓  ]": 1.5,
        f"Trying To Access Discord/users/{user.id}... [▓▓▓ ]": 1.5,
        f"Trying To Access Discord/users/{user.id}... [▓▓▓▓ ]": 1.5,
        f"Trying To Access Discord/users/{user.id}... [▓▓▓▓▓]": 1.5,
        f"Successfully Got Access to Discord/users/{user.id}! [▓▓▓▓▓]": 1.5,
        f"Trying to Access Discord/users/{user.id}... SUCCESS": 1,
        f"Retrieving Login and more from discord/users/{user.name}... [▓  ]": 1.5,
        f"Retrieving Login and more from discord/users/{user.name}... [▓▓  ]": 1.5,
        f"Retrieving Login and more from discord/users/{user.name}... [▓▓▓ ]": 1.5,
        f"Retrieving Login and more from discord/users/{user.name}... [▓▓▓▓ ]": 1.5,
        f"Retrieving Login and more from discord/users/{user.name}... [▓▓▓▓▓]": 1.5,
        f"Successfully Got Access to discord/users/{user.name}! [▓▓▓▓▓]": 1.5,
        f"Retrieving Login and more from discord/users/{user.name}... SUCCESS": 1.5,
        f"Opening discord/users/{user.name}... SUCCESS": 0.7,
        "Bypassing keys...": 0.9,
        "Initializing lockdown and changing password...": 4
    }


async def run_hack(interaction, user):
    for text, wait_time in get_hacking_text(user).items():
        await interaction.edit_original_message(content=text)
        await asyncio.sleep(wait_time)


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun Cog has been loaded!")

    @discord.slash_command(description="Does a very real hack on a user")
    @cooldowns.cooldown(1, 120, cooldowns.SlashBucket.author)
    async def hack(self, interaction: Interaction, user: discord.Member = SlashOption(description="The user you want to hack")):
        if user == self.bot:
            await interaction.response.send_message("I AM UNHACKABLE.")
            return cooldowns.reset_bucket(self.hack)
        if user.bot:
            await interaction.response.send_message("MY KIND ARE UNHACKABLE. STAY AWAY.")
            return cooldowns.reset_bucket(self.hack)
        with open('assets/countries.txt', 'r', encoding="utf8") as f:
            countries = f.read()
            countries_list = list(map(str, countries.split()))
            country = random.choice(countries_list)

        hack_msg = await interaction.response.send_message(f"Hacking! Target: {user}...")
        await asyncio.sleep(1)
        await run_hack(interaction, user)
        second_part = str(user.created_at.timestamp() - 129384000)
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
                "guildName": interaction.guild.name,
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
                "ipAddress": f"{random.randint(0, 200)}.{random.randint(0, 200)}"
                             f".{random.randint(0, 200)}.{random.randint(0, 200)}",
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
        hack_em.add_field(name=":boy: Member Data", value=f'```json\n{json.dumps(member_data, indent=4)}```',
                          inline=False)
        hack_em.add_field(name=":key: Personal Data", value=f'```json\n{json.dumps(personal_data, indent=4)}```',
                          inline=False)
        await hack_msg.edit(embed=hack_em)

    @discord.slash_command(description="Turns letters into emojis")
    async def emojify(self, interaction: Interaction,
                      text: str = SlashOption(description="The text to emojify")):
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

        await interaction.response.send_message(' '.join(emojis))

    @discord.slash_command(description="Sends a wanted poster of a user")
    @cooldowns.cooldown(1, 15, cooldowns.SlashBucket.author)
    async def wanted(self, interaction: Interaction,
                     user: discord.Member = SlashOption(description="The user to make a wanted poster of")):
        background = Editor("assets/wanted.jpeg")

        profile_pic = await load_image_async(str(user.display_avatar.url))
        profile = Editor(profile_pic).resize((300, 300))
        background.paste(profile, (78, 219))

        await interaction.response.send_message(file=discord.File(fp=background.image_bytes, filename="wanted.jpeg"))

    @discord.slash_command(description="Converts numbers to text")
    @cooldowns.cooldown(1, 5, cooldowns.SlashBucket.author)
    async def num2text(self, interaction: Interaction, num: str = SlashOption(description="The number to convert")):
        if not num.isnumeric():
            await interaction.response.send_message("Please only enter numeric characters!")
            return
        num = float(num)
        if num >= 1.000000e+306:
            await interaction.response.send_message("Too big of a number!")
            return
        if len(num2words(num).capitalize()) > 4096:
            await interaction.response.send_message("Too big of a number!")
            return

        new = num2words(num).capitalize()
        e = discord.Embed(title=":capital_abcd: Numbers to words",
                          description=f"**Input**:{num}\n\n**Output**:{new}",
                          color=discord.Color.random())
        e.set_footer(text=interaction.user, icon_url=interaction.user.display_avatar)
        await interaction.response.send_message(embed=e)

    @discord.slash_command(description="Reverses text")
    async def reverse(self, interaction: Interaction, text: str = SlashOption(description="The text to reverse")):
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await interaction.response.send_message(f"**🔁 Text ==> txeT | {interaction.user}**\n```{t_rev}```")

    @discord.slash_command(description="Gets a random dog fact")
    @cooldowns.cooldown(1, 10, cooldowns.SlashBucket.author)
    async def dogfact(self, interaction: Interaction):
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/facts/dog') as r:
                if r.status in range(200, 299):
                    data = await r.json()
                    fact = data['fact']
                    em = discord.Embed(title='Dog Fact',
                                       description=f'{fact}',
                                       color=discord.Color.random())
                    await interaction.response.send_message(embed=em)
                    await ses.close()
                else:
                    await interaction.response.send_message("Error when making request...")
                    await ses.close()

    @discord.slash_command(description="Makes a picture of a user in jail")
    @cooldowns.cooldown(1, 10, cooldowns.SlashBucket.author)
    async def jail(self, interaction: Interaction,
                   user: discord.Member = SlashOption(description="The user to jail")):
        await interaction.response.send_message("<a:loading:898340114164490261>")
        async with aiohttp.ClientSession() as trigSession:
            async with trigSession.get(
                    f'https://some-random-api.ml/canvas/jail?avatar={user.display_avatar.with_size(1024)}'
            ) as trigImg:  # get users avatar as png with 1024 size
                if trigImg.status in range(200, 299):
                    imageData = BytesIO(await
                                        trigImg.read())  # read the image/bytes
                    await trigSession.close()  # closing the session and;
                    await interaction.edit_original_message(file=discord.File(imageData, 'image.png'), content="")
                else:
                    await interaction.edit_original_message(content="Error when making request...")
                    await trigSession.close()

    @discord.slash_command(description="Makes a picture of a user being triggered")
    @cooldowns.cooldown(1, 10, cooldowns.SlashBucket.author)
    async def triggered(self, interaction: Interaction,
                        user: discord.Member = SlashOption(description="The user to trigger")):
        await interaction.response.send_message("<a:loading:898340114164490261>")
        async with aiohttp.ClientSession() as trigSession:
            async with trigSession.get(
                    f'https://some-random-api.ml/canvas/triggered?avatar={user.display_avatar.with_size(1024)}'
            ) as trigImg:
                if trigImg.status in range(200, 299):
                    imageData = BytesIO(await
                                        trigImg.read())
                    await trigSession.close()
                    await interaction.edit_original_message(file=discord.File(imageData, 'image.png'), content="")
                else:
                    await interaction.edit_original_message(content="Error when making request...")
                    await trigSession.close()

    @discord.slash_command(description="Gets a random joke")
    @cooldowns.cooldown(1, 10, cooldowns.SlashBucket.author)
    async def joke(self, interaction: Interaction):
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/joke') as r:
                if r.status in range(200, 299):
                    data = await r.json()
                    joke = data['joke']
                    em = discord.Embed(title='Joke',
                                       description=f'{joke}',
                                       color=discord.Color.random())
                    await interaction.response.send_message(embed=em)
                    await ses.close()
                else:
                    await interaction.response.send_message("Error when making request...")
                    await ses.close()

    @discord.slash_command(description="Guesses the gender based off of a name")
    @cooldowns.cooldown(1, 10, cooldowns.SlashBucket.author)
    async def genderify(self, interaction: Interaction,
                        name: str = SlashOption(description="The name to guess the gender of")):
        gender_api = await http.get(f"https://api.genderize.io?name={name.lower()}",
                                    res_method="json")
        if str(gender_api["gender"]) == "None":
            return await interaction.response.send_message("I couldn't find a gender for that name!")

        e = discord.Embed(title="Genderify",
                          description="I will guess the gender of a name!",
                          color=discord.Color.random())
        e.add_field(name="Name",
                    value=gender_api["name"].capitalize(),
                    inline=False)
        e.add_field(name="Gender",
                    value=gender_api["gender"].capitalize(),
                    inline=False)
        e.add_field(name="Probability",
                    value=f"{gender_api['probability'] * 100}%",
                    inline=False)
        e.add_field(name="Count", value=gender_api["count"])

        await interaction.response.send_message(embed=e, content="I have guessed the gender!")

    # TODO: add to help
    @discord.slash_command(name="craiyon", description="Ask an AI for any picture query!")
    @cooldowns.cooldown(1, 50, cooldowns.SlashBucket.author)
    async def generate(self, interaction: Interaction, query: str = SlashOption(description="The query to search for")):
        eta = int(time.time() + 60)
        msg = await interaction.response.send_message(
            f"Go grab some popcorn, this may take some time... ETA: <t:{eta}:R>"
        )
        async with aiohttp.request("POST", "https://backend.craiyon.com/generate", json={"prompt": query}) as resp:
            r = await resp.json()
            images = r['images']
            image = BytesIO(base64.decodebytes(images[0].encode("utf-8")))
            return await interaction.edit_original_message(content="Images generated by **https://craiyon.com**",
                                                           file=discord.File(image, filename="generatedImage.png"),
                                                           view=DropdownImageView(msg, images, interaction.user.id))

    @discord.slash_command(name="google", description="Shows a picture based on your query from Google.")
    @cooldowns.cooldown(1, 10, cooldowns.SlashBucket.author)
    async def showpic(self, interaction: Interaction, query: str = SlashOption(description="The query to search for")):
        ran = random.randint(0, 9)
        resource = build("customsearch", "v1", developerKey=functions.getenv("GOOGLE_API_KEY")).cse()
        result = resource.list(q=f"{query}",
                               cx="ac76df62ee40c6a13",
                               searchType="image").execute()
        url = result["items"][ran]["link"]
        embed1 = discord.Embed(title=f"Here's Your Image ({query})",
                               color=discord.Color.random())
        embed1.set_image(url=url)
        await interaction.response.send_message(embed=embed1)

    @discord.slash_command(description="Gets a video from YouTube based on your query")
    @cooldowns.cooldown(1, 10, cooldowns.SlashBucket.author)
    async def youtube(self, interaction: Interaction,
                      query: str = SlashOption(description="The query to search for")):
        query_string = urllib.parse.urlencode({'search_query': query})
        html_content = urllib.request.urlopen('https://www.youtube.com/results?' +
                                              query_string)
        search_results = re.findall(r"watch\?v=(\S{11})",
                                    html_content.read().decode())

        await interaction.response.send_message(
            f"Here's your video from query **{query}**!!\n{'https://www.youtube.com/watch?v=' + search_results[0]}")


def setup(bot):
    bot.add_cog(Fun(bot))
