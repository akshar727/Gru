import nextcord as discord
from nextcord.ext import commands
import random

def get_embed(_title, _description, _color):
    return discord.Embed(title=_title, description=_description, color=_color)

class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["imposter"])
    @commands.cooldown(1,25, commands.BucketType.user)
    async def findimposter(self, ctx):
        """Impostors can sabotage the reactor, 
        which gives Crewmates 30–45 seconds to resolve the sabotage. 
        If it is not resolved in the allotted time, The Impostor(s) will win."""

        # determining
        embed1 = discord.Embed(title = "Who's the imposter?" , description = "Find out who the imposter is, before the reactor breaks down!" , color=0xff0000)
        
        # fields
        embed1.add_field(name = 'Red' , value= '<:red_crewmate:898322593147387934>' , inline=False)
        embed1.add_field(name = 'Blue' , value= '<:blue_crewmate:898322371637825617>' , inline=False)
        embed1.add_field(name = 'Lime' , value= '<:lime_crewmate:898322840401629185>' , inline=False)
        embed1.add_field(name = 'White' , value= '<:white_crewmate:898322074068713532>' , inline=False)
        
        # sending the message
        msg = await ctx.reply(embed=embed1)
        
        # emojis
        emojis = {
            'red': '<:red_crewmate:898322593147387934>',
            'blue': '<:blue_crewmate:898322371637825617>',
            'lime': '<:lime_crewmate:898322840401629185>',
            'white': '<:white_crewmate:898322074068713532>'
        }
        
        # who is the imposter?
        imposter = random.choice(list(emojis.items()))
        imposter = imposter[0]
        
        # adding choices
        for emoji in emojis.values():
            await msg.add_reaction(emoji)
        
        # a simple check, whether reacted emoji is in given choises.
        def check(reaction, user):
            self.reacted = reaction.emoji
            return user == ctx.author and str(reaction.emoji) in emojis.values()

        # waiting for the reaction to proceed
        try: 
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        
        except TimeoutError:
            # reactor meltdown - defeat
            description = "Reactor Meltdown.{0} was the imposter...".format(imposter.capitalize())
            embed = get_embed("Defeat", description, discord.Color.red())
            await ctx.reply(embed=embed)
        else:
            # victory
            if str(self.reacted) == emojis[imposter]:
                description = "**{0}** was the imposter...".format(imposter.capitalize())
                embed = get_embed("Victory", description, discord.Color.blue())
                await ctx.reply(embed=embed)

            # defeat
            else:
                for key, value in emojis.items(): 
                    if value == str(self.reacted):
                        description = "**{0}** was not the imposter...".format(key.capitalize())
                        embed = get_embed("Defeat", description, discord.Color.red())
                        await ctx.reply(embed=embed)
                        break


def setup(bot):
    bot.add_cog(games(bot))