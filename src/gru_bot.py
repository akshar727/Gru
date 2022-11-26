from src.utils import functions
import nextcord as discord
from nextcord.ext import commands, tasks


class GruBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = None
        self.ts = 0
        self.tm = 0
        self.th = 0
        self.td = 0
        self.persistent_views_added = False
        self.change_status.start()
        self.uptime_counter.start()

    def get_uptime(self):
        return [self.ts, self.tm, self.th, self.td]

    async def is_owner(self, user: discord.User):
        if user.id == int(functions.getenv("BOT_OWNER_ID")):
            return True
        else:
            return False

    @tasks.loop(seconds=4)
    async def change_status(self):
        await self.change_presence(activity=discord.Game("Try: @Gru | gru help"))

    @change_status.before_loop
    async def before_change_status(self):
        await self.wait_until_ready()

    @tasks.loop(seconds=2.0)
    async def uptime_counter(self):
        self.ts += 2
        if self.ts == 60:
            self.ts = 0
            self.tm += 1
            if self.tm == 60:
                self.tm = 0
                self.th += 1
                if self.th == 24:
                    self.th = 0
                    self.td += 1

    @uptime_counter.before_loop
    async def before_uptime_counter(self):
        await self.wait_until_ready()
