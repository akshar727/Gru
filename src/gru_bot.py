from cogs.utils import config
import nextcord as discord
from nextcord.ext import commands
class GruBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persistent_views_added = False
    async def is_owner(self, user: discord.User):
        if user.id == int(config.getenv("BOT_OWNER_ID")):
            return True
        else:
            return False
