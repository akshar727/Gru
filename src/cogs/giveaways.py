from nextcord.ext import commands, application_checks
import nextcord as discord
from nextcord import Interaction, ChannelType, SlashOption, TextChannel
# from nextcord.abc import GuildChannel
# import asyncio
import humanfriendly
import time as py_time
import json
# import random


class JoinGiveaway(discord.ui.View):
    def __init__(self, time, name, guild, epoch_end, bot):
        super().__init__(timeout=time)
        self.name = name
        self.message = None
        self.guild = guild
        self.time = epoch_end
        self.bot = bot

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
            await self.message.edit(view=self)

    @discord.ui.button(label="Join Giveaway", style=discord.ButtonStyle.blurple, custom_id="join")
    async def join(self, _: discord.ui.Button, interaction: discord.Interaction):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT participants FROM giveaways WHERE guild = ? AND time = ? AND prize = ?",
                                 (self.guild, self.time, self.name,))
            data = await cursor.fetchone()
            if data:
                participants = data[0]
                try:
                    participants = json.loads(participants)
                except:
                    participants = []
                if interaction.user.id in participants:
                    await interaction.response.send_message("You have already joined this giveaway!", ephemeral=True)
                else:
                    participants.append(interaction.user.id)
                    await cursor.execute(
                        "UPDATE giveaways SET participants = ? WHERE guild = ? AND prize = ? AND time = ?",
                        (json.dumps(participants), self.guild, self.name, self.time))
                    await interaction.response.send_message("Congrats! You have joined this giveaway!", ephemeral=True)
            else:
                await interaction.response.send_message(
                    "This giveaway doesn't seem to exist, or it may have already ended.", ephemeral=True)
        await self.bot.db.commit()


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Giveaways Cog ready to use!")

    # TODO: Add to help
    @discord.slash_command(name="ping", description="Check the bot's ping!")
    async def ping(self, interaction: Interaction):
        em = discord.Embed(title="Bot Ping", color=discord.Color.random())
        em.add_field(name="My Api Latency is:", value=f"{round(self.bot.latency * 1000)}ms")
        em.set_footer(text=f"Ping requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=em)

    @discord.slash_command(name="giveaway", description="Base giveaway command [No function]")
    async def giveaway(self, interaction: discord.Interaction):
        return

    # TODO: Add to help
    @giveaway.subcommand(name="start", description="Start a giveaway!")
    @application_checks.has_permissions(manage_messages=True)
    async def start(self, interaction: Interaction,
                    prize: str = SlashOption(description="The prize of the giveaway", required=True),
                    channel: TextChannel = SlashOption(channel_types=[ChannelType.text],
                                                        description="In which channel should the giveaway be in?",
                                                        required=True),
                    time: str = SlashOption(description="How long should the giveaway go for? [Ex. 25s, 3h, 5d, 20m]",
                                            required=True),
                    winners: int = SlashOption(description="How many people should win this giveaway?", required=True)):
        if not channel.permissions_for(interaction.user).send_messages:
            return await interaction.response.send_message(
                "You do not have permissions to send messages in that channel!")
        time = humanfriendly.parse_timespan(time)
        epoch_end = py_time.time() + time
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("INSERT INTO giveaways VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                 (epoch_end, prize, "", "", channel.id, interaction.guild.id, winners, 0,))
            em = discord.Embed(
                title=':tada: New Giveaway! :tada:',
                description=f'{interaction.user.mention} is giving away **{prize}**!!\n'
                            f'The giveaway ends at <t:{int(epoch_end)}:f> or <t:{int(epoch_end)}:R>\n'
                            f'Winner(s): {winners}\nClick the `Join Giveaway` button to join!',
                color=discord.Color.random())
            await interaction.response.send_message(f"Giveaway has been started in {channel.mention}", ephemeral=True)
            view = JoinGiveaway(time, prize, interaction.guild.id, epoch_end, self.bot)
            msg = await channel.send(embed=em, view=view)
            view.message = msg
            await cursor.execute("UPDATE giveaways SET message = ? WHERE guild = ? AND prize = ? AND time = ?",
                                 (msg.id, interaction.guild.id, prize, epoch_end))
        await self.bot.db.commit()


def setup(bot):
    bot.add_cog(Giveaway(bot))
