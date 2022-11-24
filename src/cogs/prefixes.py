import nextcord as discord
from nextcord import SlashOption, Interaction
from nextcord.ext import commands
from src.utils import config


class Prefixes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="prefix", description="Change the prefix for the bot in this server.")
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, interaction: Interaction,
                     prefix: str = SlashOption(description="The new prefix for the bot.", required=True),
                     space: bool = SlashOption(description="Whether or not to add a space after the prefix.",
                                               required=False)
                     ):
        if space:
            prefix = prefix + " "
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT prefix FROM prefixes WHERE guild = ?", (interaction.guild.id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("UPDATE prefixes SET prefix = ? WHERE guild = ?", (prefix, interaction.guild.id,))
                await interaction.response.send_message(f"The prefix has been updated to `{prefix}`")
            else:
                await cursor.execute("INSERT INTO prefixes (prefix, guild) VALUES (?, ?)", (
                    config.getenv("BOT_PREFIX"), interaction.guild.id,))
                await cursor.execute("SELECT prefix FROM prefixes WHERE guild = ?", (interaction.guild.id,))
                data = await cursor.fetchone()
                if data:
                    await cursor.execute("UPDATE prefixes SET prefix = ? WHERE guild = ?",
                                         (prefix, interaction.guild.id,))
                    await interaction.response.send_message(f"The prefix has been updated to `{prefix}`")
                else:
                    return
            await self.bot.db.commit()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        # with open("databases/server_configs.json", 'r') as f:
        #     configs = json.load(f)

        # configs[str(guild.id)] = {}
        # configs[str(guild.id)]["giveaway_role"] = "None"
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("INSERT INTO prefixes (prefix, guild) VALUES (?, ?)", (
                config.getenv("BOT_PREFIX"), guild.id,))
            await cursor.execute("INSERT INTO levelSettings VALUES (?, ?, ?, ?)", (False, 0, 0, guild.id,))
        await self.bot.db.commit()

        # with open("databases/server_configs.json", 'w') as f:
        #     json.dump(configs, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        # with open("databases/server_configs.json", 'r') as f:
        #     configs = json.load(f)
        # TODO: delete levels
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT prefix FROM prefixes WHERE guild = ?", (guild.id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("DELETE FROM prefixes WHERE guild = ?", (guild.id,))
            await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?", (guild.id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("DELETE FROM levelSettings WHERE guild = ?", (guild.id,))
        await self.bot.db.commit()

        # del configs[str(guild.id)]
        # with open("databases/server_configs.json", 'w') as f:
        #     json.dump(configs, f, indent=4)


def setup(bot):
    bot.add_cog(Prefixes(bot))
