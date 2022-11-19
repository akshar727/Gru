from nextcord.ext import commands
import nextcord as discord
import json
from easy_pil import Editor, Font, load_image_async,Text



def level_by_xp(xp):
    return xp**(1 / 4)


def xp_by_level(level):
    return level ** 4


async def get_rank(bot,user,guild):
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT level, xp, user FROM levels WHERE guild = ? ORDER BY level DESC, xp DESC LIMIT 1000",(guild.id,))
        data = await cursor.fetchall()
        if data:
            for pos,item in enumerate(data):
                if item[2] == user.id:
                    return pos+1
            return None



def custom_poppins(text):
    if len(text) < 30:
        return Font.poppins(size=35)
    if len(text) > 30:
        return Font.poppins(size=25)

async def get_lvl_card(lvl, exp, author,rank):
    _exp = ...
    total = ...
    exponent = 4
    next_lvl = lvl + 1
    next_lvl_xp = next_lvl**exponent
    current_xp = exp - (lvl)**exponent
    next_lvl_xp -= lvl**exponent
    total = next_lvl_xp
    _exp = current_xp
    if _exp < 0: _exp = 0
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
        'rank':rank
    }
    background = Editor("assets/bg.png")
    background.blur()
    profile_pic = await load_image_async(str(author.display_avatar.url))
    profile = Editor(profile_pic).resize((175, 175)).circle_image()
    poppins = custom_poppins(userData['name'])
    poppins_small = Font.poppins(size=30)
    background.paste(profile, (30, 62))
    background.rounded_corners(10)
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
    if rank != None:
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
        


    @commands.command(aliases=['rank', 'lvl'])
    async def level(self,ctx, member: discord.Member = None):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?", (ctx.guild.id,))
            levelsys = await cursor.fetchone()
            if levelsys and not levelsys[0]:
                # 0: False, 1: True
                return await ctx.reply("Levels are disabled in this server.")
        if not member:
            user = ctx.message.author
            async with self.bot.db.cursor() as cursor:
                await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?",(user.id,ctx.guild.id,))
                xp = await cursor.fetchone()
                await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?",(user.id,ctx.guild.id,))
                level = await cursor.fetchone()
                if not xp or not level:
                    await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)",(1,0,user.id,ctx.guild.id,))
                    await self.bot.db.commit()
                    xp = 0
                    level = 1
            try:
                xp = xp[0]
                level = level[0]
            except KeyError:
                xp = 0
                level = 1
            # this is to prevent showing numbers over 100% (when user levels up by sending this command)
            level_start = level
            level_end = int(int(xp)**(1/4))
            if level_start < level_end:
                level += 1

            rank = await get_rank(self.bot,ctx.author,ctx.guild)
            return await ctx.reply(file=await get_lvl_card(level, xp, ctx.author,rank))

        else:
            if member.bot:
                await ctx.reply("Bots aren't in the database!")
                return
            user = member
            async with self.bot.db.cursor() as cursor:
                await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?",(user.id,ctx.guild.id,))
                xp = await cursor.fetchone()
                await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?",(user.id,ctx.guild.id,))
                level = await cursor.fetchone()
                if not xp or not level:
                    await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)",(1,0,user.id,ctx.guild.id,))
                    await self.bot.db.commit()
                    xp = 0
                    level = 1
            try:
                xp = xp[0]
                level = level[0]
            except KeyError:
                xp = 0
                level = 1
            rank = await get_rank(self.bot,member,ctx.guild)
            return await ctx.reply(file=await get_lvl_card(level, xp, member,rank))
    @commands.group()
    async def lvlsys(self,ctx):
        return
    # TODO: ADD TO HELP
    @lvlsys.command(aliases=['e','en'])
    @commands.has_permissions(manage_guild=True)
    async def enable(self,ctx):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?", (ctx.guild.id,))
            levelsys = await cursor.fetchone()
            if levelsys:
                if levelsys[0]:
                    return await ctx.reply("The leveling system is already enabled!")
                await cursor.execute("UPDATE levelSettings SET levelsys = ? WHERE guild = ?",(True, ctx.guild.id,))
            else:
                await cursor.execute("INSERT INTO levelSettings VALUES (?, ?, ?, ?)",(True, 0, 0, ctx.guild.id,))
            await ctx.reply("The leveling system has been enabled!")
        await self.bot.db.commit()
    
    @lvlsys.command(aliases=['d','dis'])
    @commands.has_permissions(manage_guild=True)
    async def disable(self,ctx):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?", (ctx.guild.id,))
            levelsys = await cursor.fetchone()
            if levelsys:
                if not levelsys[0]:
                    return await ctx.reply("The leveling system is already disabled!")
                await cursor.execute("UPDATE levelSettings SET levelsys = ? WHERE guild = ?",(False, ctx.guild.id,))
            else:
                await cursor.execute("INSERT INTO levelSettings VALUES (?, ?, ?, ?)",(False, 0, 0, ctx.guild.id,))
            await ctx.reply("The leveling system has been disabled!")
        await self.bot.db.commit()

    @commands.command(aliases=['lvllb', 'levellb', 'llb'])
    async def levelleaderboard(self,ctx):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?", (ctx.guild.id,))
            levelsys = await cursor.fetchone()
            if levelsys and not levelsys[0]:
                # 0: False, 1: True
                return await ctx.reply("Levels are disabled in this server.")
            await cursor.execute("SELECT level, xp, user FROM levels WHERE guild = ? ORDER BY level DESC, xp DESC LIMIT 10",(ctx.guild.id,))
            data = await cursor.fetchall()
            if data:
                e = discord.Embed(
                    title="Level Leaderboard",
                    description=
                    f"These are the top {len(data)} users in this server with the highest XP.",
                    color=discord.Color.random())
                count = 0
                for table in data:
                    count += 1
                    user = ctx.guild.get_member(table[2])
                    e.add_field(name=f"{count}. {user.name}#{user.discriminator}",
                                value=f"Level: {table[0]}| XP: {round(table[1])}",
                                inline=False)
                await ctx.reply(embed=e)
            else:
                return await ctx.reply("Somehow, there are no users in the leveling system!")









def setup(bot):
    bot.add_cog(Levels(bot))