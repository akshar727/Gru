from nextcord.ext import commands
from .utils import config


class Prefixes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def prefix(self,ctx, prefix=None):
        if ctx.author.id != ctx.guild.owner_id:
            return await ctx.reply(
                "Sorry, but only the owner of this server can change the prefix!")
        if prefix == None:
            await ctx.reply("Please enter the new prefix.")
            return

        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT prefix FROM prefixes WHERE guild = ?", (ctx.guild.id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("UPDATE prefixes SET prefix = ? WHERE guild = ?",(prefix,ctx.guild.id,))
                await ctx.reply(f"The prefix has been updated to `{prefix}`")
            else:
                await cursor.execute("INSERT INTO prefixes (prefix, guild) VALUES (?, ?)",(config.getenv("BOT_PREFIX"), ctx.guild.id,))
                await cursor.execute("SELECT prefix FROM prefixes WHERE guild = ?", (ctx.guild.id,))
                data = await cursor.fetchone()
                if data:
                    await cursor.execute("UPDATE prefixes SET prefix = ? WHERE guild = ?",(prefix,ctx.guild.id,))
                    await ctx.reply(f"The prefix has been updated to `{prefix}`")
                else:
                    return
            await self.bot.db.commit()


    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        
        # with open("databases/server_configs.json", 'r') as f:
        #     configs = json.load(f)

        # configs[str(guild.id)] = {}
        # configs[str(guild.id)]["giveaway_role"] = "None"
        # configs[str(guild.id)]["levels"] = False
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("INSERT INTO prefixes (prefix, guild) VALUES (?, ?)",(config.getenv("BOT_PREFIX"),guild.id))
        await self.bot.db.commit()

        # with open("databases/server_configs.json", 'w') as f:
        #     json.dump(configs, f, indent=4)


    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        # with open("databases/server_configs.json", 'r') as f:
        #     configs = json.load(f)
        # TODO: delete levels
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT prefix FROM prefixes WHERE guild = ?",(guild.id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("DELETE FROM prefixes WHERE guild = ?",(guild.id,))
        await self.bot.db.commit()
    
        # del configs[str(guild.id)]
        # with open("databases/server_configs.json", 'w') as f:
        #     json.dump(configs, f, indent=4)


        



def setup(bot):
    bot.add_cog(Prefixes(bot))