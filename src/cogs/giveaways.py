from nextcord.ext import commands,tasks,application_checks
import nextcord as discord
from nextcord import Interaction, ChannelType, SlashOption
from nextcord.abc import GuildChannel
import asyncio
import humanfriendly
import time as pyTime
import json
import random
class Giveaway(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Giveaways Cog ready to use!")

    # TODO: Add to help
    @discord.slash_command(name="ping",description="Check the bot's ping!")
    async def ping(self, interaction: Interaction):
        em = discord.Embed(title="Bot Ping",color=discord.Color.random())
        em.add_field(name="My Api Latency is:",value=f"{round(self.bot.latency*1000)}ms")
        em.set_footer(text=f"Ping requested by {interaction.user}",icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=em)
    

    @discord.slash_command(name="giveaway",description="Base giveaway command [No function]")
    async def giveaway(self, interaction: discord.Interaction):
        return
    
    # TODO: Add to help
    @giveaway.subcommand(name="start",description="Start a giveaway!")
    @application_checks.has_permissions(manage_messages=True)
    async def start(self,interaction: Interaction, prize: str = SlashOption(description="The prize of the giveaway",required=True),channel: GuildChannel = SlashOption(channel_types=[ChannelType.text],description="In which channel should the giveaway be in?",required=True),time: str = SlashOption(description="How long should the giveaway go for? [Ex. 25s, 3h, 5d, 20m]",required=True),winners: int = SlashOption(description="How many people should win this giveaway?",required=True)):
        if not channel.permissions_for(interaction.user).send_messages:
            return await interaction.response.send_message("You do not have permissions to send messages in that channel!")
        time = humanfriendly.parse_timespan(time)
        epochEnd  = pyTime.time() + time
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("INSERT INTO giveaways VALUES (?, ?, ?, ?, ?, ?, ?, ?)",(epochEnd,prize,"",channel.id,interaction.guild.id,"",winners,0,))
            em = discord.Embed(
                title=':tada: New Giveaway! :tada:',
                description=f'{interaction.user.mention} is giving away **{prize}**!!\nThe giveaway ends at <t:{int(epochEnd)}:f> or <t:{int(epochEnd)}:R>\nWinner(s): {winners}\nClick the `Join Giveaway` button to join!',
                color=discord.Color.random())
            await interaction.response.send_message(f"Giveaway has been started in {channel.mention}",ephemeral=True)
            # view = JoinGiveaway(time,prize,interaction.guild.id,epochEnd,self.bot)
            msg = await channel.send(embed=em)
            # view.message = msg
            await cursor.execute("UPDATE giveaways SET message = ? WHERE guild = ? AND prize = ? AND time = ?",(msg.id,interaction.guild.id,prize,epochEnd))
        await self.bot.db.commit()


    
            



def setup(bot):
    bot.add_cog(Giveaway(bot))