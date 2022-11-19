from cogs.utils import config
import nextcord as discord
from nextcord.ext import commands,tasks




ts = 0
tm = 0
th = 0
td = 0


class GruBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persistent_views_added = False
        self.change_status.start()
        self.uptimeCounter.start()
    async def is_owner(self, user: discord.User):
        if user.id == int(config.getenv("BOT_OWNER_ID")):
            return True
        else:
            return False

    @tasks.loop(seconds=4)
    async def change_status(self):
        await self.change_presence(activity=discord.Game("Try: @Gru | gru help"))
    @change_status.before_loop
    async def beforeChangeStatus(self):
        await self.wait_until_ready()

    @tasks.loop(seconds=2.0)
    async def uptimeCounter(self):
        global ts, tm, th, td
        ts += 2
        if ts == 60:
            ts = 0
            tm += 1
            if tm == 60:
                tm = 0
                th += 1
                if th == 24:
                    th = 0
                    td += 1
    @uptimeCounter.before_loop
    async def beforeUptimeCounter(self):
        await self.wait_until_ready()
