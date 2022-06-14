
from nextcord.ext import commands
import nextcord as discord
import asyncio
import random
import base64
import string
import json

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command(aliases=["heck"])
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def hack(self,ctx, user: discord.Member = None):
        if user is None:
            await ctx.reply("Please enter a user to hack!(Unless you want to hack air)")
            self.hack.reset_cooldown(ctx)
            return
        if user == self.bot:
            await ctx.reply("I AM UNHACKABLE.")
            return self.hack.reset_cooldown(ctx)
        if user.bot:
            await ctx.reply("MY KIND ARE UNHACKABLE. STAY AWAY.")
            return self.hack.reset_cooldown(ctx)
        with open('databases/countries.txt', 'r') as f:
            countries = f.read()
            countries_list = list(map(str, countries.split()))
            country = random.choice(countries_list)
    
        hack_msg = await ctx.reply(f"Hacking! Target: {user}...")
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
        await asyncio.sleep(0.7)
        await hack_msg.edit("Bypassing keys...")
        await asyncio.sleep(0.9)
        await hack_msg.edit("Initializing lockdown and changing password...")
        await asyncio.sleep(4)
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


def setup(bot):
    bot.add_cog(Fun(bot))
        