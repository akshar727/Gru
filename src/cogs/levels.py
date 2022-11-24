from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import nextcord as discord
from easy_pil import Editor, Font, load_image_async, Text


def level_by_xp(xp):
    return xp ** (1 / 4)


async def get_level_data(bot, user, guild):
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (user.id, guild.id,))
        xp = await cursor.fetchone()
        await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (user.id, guild.id,))
        level = await cursor.fetchone()
        if not xp or not level:
            await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)",
                                 (1, 0, user.id, guild.id,))
            await bot.db.commit()
            xp = 0
            level = 1
    try:
        xp = xp[0]
        level = level[0]
    except KeyError:
        xp = 0
        level = 1
    return [xp, level]


def xp_by_level(level):
    return level ** 4


async def get_rank(bot, user, guild):
    async with bot.db.cursor() as cursor:
        await cursor.execute(
            "SELECT level, xp, user FROM levels WHERE guild = ? ORDER BY level DESC, xp DESC LIMIT 1000", (guild.id,))
        data = await cursor.fetchall()
        if data:
            for pos, item in enumerate(data):
                if item[2] == user.id:
                    return pos + 1
            return None


def custom_poppins(text):
    if len(text) < 30:
        return Font.poppins(size=35)
    if len(text) > 30:
        return Font.poppins(size=25)


async def get_lvl_card(lvl, exp, author, rank):
    exponent = 4
    next_lvl = lvl + 1
    next_lvl_xp = next_lvl ** exponent
    current_xp = exp - lvl ** exponent
    next_lvl_xp -= lvl ** exponent
    total = next_lvl_xp
    _exp = current_xp
    if _exp < 0:
        _exp = 0
    per = round(float(_exp / total) * 100)
    border_radius = 20
    primary_color = "#ffffff"
    secondary_color = "#13ced1"
    accent_color = "#FF56B2"
    userData = {
        'name': f"{author.name}",
        'lvl': lvl,
        'xp': round(_exp),
        'next_lvl_xp': total,
        'percent': per,
        'rank': rank
    }
    background = Editor("assets/bg.png")
    background.blur()
    profile_pic = await load_image_async(str(author.display_avatar.url))
    profile = Editor(profile_pic).resize((175, 175)).circle_image()
    poppins = custom_poppins(userData['name'])
    poppins_small = Font.poppins(size=30)
    background.paste(profile, (30, 62))
    background.rectangle((200, 205),
                         width=650,
                         height=40,
                         color=primary_color,
                         radius=border_radius)
    if per > 3:
        background.bar((200, 205),
                       max_width=650,
                       height=40,
                       percentage=userData['percent'],
                       color=accent_color,
                       radius=border_radius)
    background.text((215, 150), userData['name'], font=poppins, color=primary_color)
    background.text((490, 215), f'{userData["percent"]}%', font=poppins_small, color=secondary_color)
    background.ellipse((30, 62), width=176, height=176, outline=accent_color, stroke_width=4)
    rank_level_texts = []
    if rank is not None:
        rank_level_texts.append(Text("Rank ", color=primary_color, font=poppins))
        rank_level_texts.append(Text(f"#{userData['rank']}", color=secondary_color, font=poppins))

    rank_level_texts += [Text("   Level ", color=primary_color, font=poppins),
                         Text(f"{userData['lvl']}", color=secondary_color, font=poppins)]

    background.multi_text((850, 30), texts=rank_level_texts, align="right")

    file = discord.File(fp=background.image_bytes, filename="levelcard.png")
    return file


class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="level", description="Get yours or other's level cards")
    async def lvl(self, interaction: Interaction,
                  member: discord.Member = SlashOption(name="member", description="Member to get level card of",
                                                       required=False)
                  ):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?", (interaction.guild.id,))
            levelsys = await cursor.fetchone()
            if levelsys and not levelsys[0]:
                # 0: False, 1: True
                return await interaction.response.send_message("Levels are disabled in this server.")
        if not member:
            user = interaction.user
            lvl_data = await get_level_data(self.bot, user, interaction.guild)
            level = lvl_data[1]
            xp = lvl_data[0]
            # this is to prevent showing numbers over 100% (when user levels up by sending this command)
            level_start = level
            level_end = int(int(xp) ** (1 / 4))
            if level_start < level_end:
                level += 1

            rank = await get_rank(self.bot, user, interaction.guild)
            return await interaction.response.send_message(file=await get_lvl_card(level, xp, user, rank))

        else:
            if member.bot:
                return await interaction.response.send_message("Bots aren't in the database!")
            user = member
            lvl_data = await get_level_data(self.bot, user, interaction.guild)
            level = lvl_data[1]
            xp = lvl_data[0]
            rank = await get_rank(self.bot, member, interaction.guild)
            return await interaction.response.send_message(file=await get_lvl_card(level, xp, member, rank))

    @discord.slash_command(name="lvlsys", description="Base level system command [No function]")
    async def lvlsys(self, interaction: discord.Interaction):
        return

    # TODO: ADD TO HELP
    @lvlsys.subcommand(name="enable", description="Enable the level system.")
    @commands.has_permissions(manage_guild=True)
    async def enable(self, interaction: Interaction):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?", (interaction.guild.id,))
            levelsys = await cursor.fetchone()
            if levelsys:
                if levelsys[0]:
                    return await interaction.response.send_message("The leveling system is already enabled!")
                await cursor.execute("UPDATE levelSettings SET levelsys = ? WHERE guild = ?",
                                     (True, interaction.guild.id,))
            else:
                await cursor.execute("INSERT INTO levelSettings VALUES (?, ?, ?, ?)",
                                     (True, 0, 0, interaction.guild.id,))
            await interaction.response.send_message("The leveling system has been enabled!")
        await self.bot.db.commit()

    @lvlsys.subcommand(name="disable", description="Disable the level system.")
    @commands.has_permissions(manage_guild=True)
    async def disable(self, interaction: Interaction):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?", (interaction.guild.id,))
            levelsys = await cursor.fetchone()
            if levelsys:
                if not levelsys[0]:
                    return await interaction.response.send_message("The leveling system is already disabled!")
                await cursor.execute("UPDATE levelSettings SET levelsys = ? WHERE guild = ?",
                                     (False, interaction.guild.id,))
            else:
                await cursor.execute("INSERT INTO levelSettings VALUES (?, ?, ?, ?)",
                                     (False, 0, 0, interaction.guild.id,))
            await interaction.response.send_message("The leveling system has been disabled!")
        await self.bot.db.commit()

    @discord.slash_command(name="level_leaderboard", description="Get a leaderboard with the users that have the "
                                                                 "highest level and xp.") 
    async def _levelleaderboard(self, interaction: Interaction):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?", (interaction.guild.id,))
            levelsys = await cursor.fetchone()
            if levelsys and not levelsys[0]:
                # 0: False, 1: True
                return await interaction.response.send_message("Levels are disabled in this server.")
            await cursor.execute(
                "SELECT level, xp, user FROM levels WHERE guild = ? ORDER BY level DESC, xp DESC LIMIT 10",
                (interaction.guild.id,))
            data = await cursor.fetchall()
            if data:
                e = discord.Embed(
                    title="Level Leaderboard",
                    description=f"These are the top {len(data)} users in this server with the highest XP.",
                    color=discord.Color.random())
                count = 0
                for table in data:
                    count += 1
                    user = interaction.guild.get_member(table[2])
                    e.add_field(name=f"{count}. {user.name}#{user.discriminator}",
                                value=f"Level: {table[0]}| XP: {round(table[1])}",
                                inline=False)
                await interaction.response.send_message(embed=e)
            else:
                return await interaction.response.send_message("Somehow, there are no users in the leveling system!")

    @discord.slash_command(name="rewards", description="Get a list of all the rewards you can get from leveling up.")
    async def _rewards(self, interaction: Interaction):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?", (interaction.guild.id,))
            levelsys = await cursor.fetchone()
            if levelsys and not levelsys[0]:
                # 0: False, 1: True
                return await interaction.response.send_message("Levels are disabled in this server.")
            await cursor.execute("SELECT * FROM levelSettings WHERE guild = ? ORDER BY levelReq",
                                 (interaction.guild.id,))
            roleLevels = await cursor.fetchall()
            if not roleLevels:
                return await interaction.response.send_message("There are no role levels that have been setup for "
                                                               "this server!")
            em = discord.Embed(title="Role Levels",
                               description="The roles that you can get from leveling up in this server.",
                               color=discord.Color.random())
            for role in roleLevels:
                if role[1] != 0:
                    em.add_field(name=f"Level {role[2]}", value=f"{interaction.guild.get_role(role[1]).mention}",
                                 inline=False)
            await interaction.response.send_message(embed=em)

    @lvlsys.subcommand(name="role", description="Set a role to be given to a user when they reach a certain level.")
    @commands.has_permissions(manage_messages=True)
    async def setrole(self, interaction: Interaction,
                      level: int = SlashOption(description="The level that this will be the reward for"),
                      role: discord.Role = SlashOption(description="The role that will be given to the user.")):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?", (interaction.guild.id,))
            levelsys = await cursor.fetchone()
            if levelsys and not levelsys[0]:
                # 0: False, 1: True
                return await interaction.response.send_message("Levels are disabled in this server.")
            await cursor.execute("SELECT role FROM levelSettings WHERE role = ? and guild = ?",
                                 (role.id, interaction.guild.id,))
            roleTF = await cursor.fetchone()
            await cursor.execute("SELECT role FROM levelSettings WHERE levelReq = ? and guild = ?",
                                 (level, interaction.guild.id,))
            levelTF = await cursor.fetchone()
            if roleTF or levelTF:
                return await interaction.response.send_message("A reward for the level already exists!")
            await cursor.execute("INSERT INTO levelSettings VALUES (?, ?, ?, ?)",
                                 (True, role.id, level, interaction.guild.id,))
            await self.bot.db.commit()
        await interaction.response.send_message("That level reward was created!")

    @lvlsys.subcommand(name="remove", description="Remove a role reward from a level.")
    @commands.has_permissions(manage_messages=True)
    async def remrole(self, interaction: Interaction,
                      level: int = SlashOption(description="The level that the reward was originally for.")):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?", (interaction.guild.id,))
            levelsys = await cursor.fetchone()
            if levelsys and not levelsys[0]:
                # 0: False, 1: True
                return await interaction.response.send_message("Levels are disabled in this server.")
            await cursor.execute("SELECT role FROM levelSettings WHERE levelReq = ? and guild = ?",
                                 (level, interaction.guild.id,))
            levelTF = await cursor.fetchone()
            if levelTF:
                await cursor.execute("DELETE FROM levelSettings WHERE levelReq = ? and guild = ?",
                                     (level, interaction.guild.id,))
                await interaction.response.send_message("That level reward has been deleted!")
            else:
                await interaction.response.send_message("There is not a reward for the level requirement!")
            await self.bot.db.commit()


def setup(bot):
    bot.add_cog(Levels(bot))
