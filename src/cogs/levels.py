from nextcord.ext import commands
import nextcord as discord
import json
from easy_pil import Editor, Font, Canvas, load_image_async



def level_by_xp(xp):
    return xp**(1 / 4)


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
    next_lvl_xp = next_lvl**exponent
    current_xp = exp - (lvl)**exponent
    next_lvl_xp -= lvl**4
    total = next_lvl_xp
    _exp = current_xp
    if _exp < 0: _exp = 0
    per = round(float(_exp / total) * 100)
    border_radius = 20
    userData = {
        'name': f"{author.name}#{author.discriminator}",
        'lvl': lvl,
        'xp': int(_exp),
        'next_lvl_xp': total,
        'percent': per
    }
    background = Editor(Canvas((900, 300), color="#141414"))
    profile_pic = await load_image_async(str(author.display_avatar.url))
    profile = Editor(profile_pic).resize((150, 150)).circle_image()
    poppins = custom_poppins(userData['name'])
    poppins_small = Font.poppins(size=30)
    bar_color = "#ff0000"
    if userData['percent'] > 90:
        bar_color = "#0afc05"
    elif userData['percent'] > 80:
        bar_color = "#06d902"
    elif userData['percent'] > 75:
        bar_color = "#05b802"
    elif userData['percent'] > 50:
        bar_color = "#f4f73b"
    elif userData['percent'] > 25:
        bar_color = "#ffbe3b"
    card_right_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]
    background.polygon(card_right_shape, color="#545352")
    background.paste(profile, (30, 30))
    background.rectangle((30, 220),
                         width=650,
                         height=40,
                         color="#ffffff",
                         radius=border_radius)
    if per > 3:
        background.bar((30, 220),
                       max_width=650,
                       height=40,
                       percentage=userData['percent'],
                       color=bar_color,
                       radius=border_radius)
    background.text((200, 40), userData['name'], font=poppins, color="#ffffff")
    background.rectangle((200, 100), width=350, height=2, fill="#ffffff")
    background.text(
        (200, 130),
        f"Level: {userData['lvl']} | XP: {userData['xp']}/{userData['next_lvl_xp']}",
        font=poppins_small,
        color="#ffffff")

    file = discord.File(fp=background.image_bytes, filename="levelcard.png")
    return file

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot: return
        with open('databases/server_configs.json', 'r') as f:
            configs = json.load(f)
        if configs[str(message.guild.id)]['levels'] is False: return
        author = message.author
        guild = message.guild
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?",(author.id,guild.id,))
            xp = await cursor.fetchone()
            await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?",(author.id,guild.id,))
            level = await cursor.fetchone()

            if not xp or not level:
                await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)",(1,0,author.id,guild.id))
                await self.bot.db.commit()
            try:
                xp = xp[0]
                level = level[0]
            except TypeError:
                xp = 0
                level = 1
            
            xp += level * 1.3
            await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp,author.id,guild.id,))


            level_start = level
            level_end = int(xp**(1/4))
            if level_start < level_end:
                await message.channel.send('Congratulations! {} has leveled up to **Level {}** and has a total of **{} xp**! :tada: :tada:'.format(author.mention, level_end, round(xp))) 
                await cursor.execute("UPDATE levels SET level = ? WHERE user = ? AND guild = ?",(level_end,author.id,guild.id,))
        await self.bot.db.commit()
        await self.bot.process_commands(message)


    @commands.command(aliases=['rank', 'lvl'])
    async def level(self,ctx, member: discord.Member = None):
        with open('databases/server_configs.json', 'r') as f:
            configs = json.load(f)
        if not configs[str(ctx.guild.id)]['levels']:
            return await ctx.reply("Levels are disabled in this server.")
        if not member:

            user = ctx.message.author
            async with self.bot.db.cursor() as cursor:
                await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?",(user.id,ctx.guild.id,))
                xp = await cursor.fetchone()
                await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?",(user.id,ctx.guild.id,))
                level = await cursor.fetchone()
            if not xp or not level:
                await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)",(1,0,user.id,ctx.guild.id))
                await self.bot.db.commit()
            try:
                xp = xp[0]
                level = level[0]
            except KeyError:
                xp = 0
                level = 1
            return await ctx.reply(file=await get_lvl_card(level, xp, ctx.author))

        else:
            if member.bot:
                await ctx.reply("Bots aren't in the database!")
                return
            async with self.bot.db.cursor() as cursor:
                await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?",(user.id,ctx.guild.id,))
                xp = await cursor.fetchone()
                await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?",(user.id,ctx.guild.id,))
                level = await cursor.fetchone()

            if not xp or not level:
                await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)",(1,0,ctx.author.id,ctx.guild.id))
                await self.bot.db.commit()
                xp = 0
                level = 1

            return await ctx.reply(file=await get_lvl_card(level, xp, member))







def setup(bot):
    bot.add_cog(Levels(bot))