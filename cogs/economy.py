from nextcord.ext import commands
import nextcord as discord

class Economy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Economy(bot))
        