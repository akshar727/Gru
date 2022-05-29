import nextcord as discord
from nextcord.ext import commands
import psutil
import json
import asyncio





class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()

    async def on_ready(self):
        print('Info Cog Loaded Succesfully')
        print("Bot is ready to use.")
        

    @commands.command(aliases=['help'])
    async def _help(self, ctx,type=None):
        with open('databases/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.guild.id)]
        if type is None:
            embedvar = discord.Embed(title="Help Commands",description='All the commands in the bot.', color=0x00ff00)
            embedvar.add_field(name="Moderation",value=f"Do `{prefix}adminhelp` to see all the moderation commands(**staff only**)(**MAINTINENCE**).")
            embedvar.add_field(name="Economy",value=f"All the economy commands in the bot.Do `{prefix}help economy` to see them.")
            embedvar.add_field(name="Misc",value=f"All the miscellaneous commands in the bot.Do `{prefix}help misc` to see them.")
            embedvar.add_field(name="Fun",value=f"All the fun commands in the bot.Do `{prefix}help fun` to see them.")


            embedvar.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
            await ctx.send(embed=embedvar)
        elif type.lower() == "economy" or type.lower() == "eco":
            embedvar = discord.Embed(title="Help Commands",description='All the **Economy** commands in the bot.', color=0x00ff00)
            embedvar.add_field(name=f'{prefix}bankrob <user>', value='''Allows you to rob a user's bank''', inline=False)
            embedvar.add_field(name=f'{prefix}get_job', value='Allows you to get a job a Gru enterprises™!', inline=False)
            embedvar.add_field(name=f'{prefix}crates', value='Allows you to view all the crates you have.', inline=False)
            embedvar.add_field(name=f'{prefix}open <type> <amount>', value='Allows you to open your crates!', inline=False)
            embedvar.add_field(name=f'{prefix}crate_info', value='Allows you to view the cash ranges of all the crates.', inline=False)
            embedvar.add_field(name=f'{prefix}jobs', value='Shows a list of all jobs in Gru enterprises™!', inline=False)
            embedvar.add_field(name=f'{prefix}work', value='''Allows you to work and make some money!''', inline=False)
            embedvar.add_field(name=f'{prefix}balance / {prefix}bal', value='To see your balance', inline=False)
            embedvar.add_field(name=f'{prefix}beg', value='To beg some money', inline=False)
            embedvar.add_field(name=f'{prefix}deposit / {prefix}dep', value='To deposit money in bank', inline=False)
            embedvar.add_field(name=f'{prefix}withdraw / {prefix}with', value='To withdraw money from bank', inline=False)
            embedvar.add_field(name=f'{prefix}send', value='Send money to someone', inline=False)
            embedvar.add_field(name=f'{prefix}rob <user>', value='Allows you to rob a user!', inline=False)
            embedvar.add_field(name=f'{prefix}slots <amount>', value='To bet some money', inline=False)
            embedvar.add_field(name=f'{prefix}shop', value='To view shop', inline=False)
            embedvar.add_field(name=f'{prefix}buy [amount] <item>', value='To, buy an item', inline=False)
            embedvar.add_field(name=f'{prefix}sell <item>', value='To sell an item', inline=False)
            embedvar.add_field(name=f'{prefix}inventory / {prefix}inv', value='To view your inventory', inline=False)
            embedvar.add_field(name=f'{prefix}viewbal <user>',value='''Allows you to view someone else's balance''',inline=False)
            embedvar.add_field(name=f'{prefix}leaderboard [amount] [type] / {prefix}lb [amount] <type>', value='''Allows you to see the richest people in the bot!The types are `all` to see al users in the leaderboard and `server` to see only users in this server.''', inline=False)
            embedvar.add_field(name=f'{prefix}daily / {prefix}weekly', value='''Allows you to earn some Minions™️!''', inline=False)

            embedvar.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
            embedvar.set_footer(text="Arguments that are surrounded in [] are optional.")
            await ctx.send(embed=embedvar)


        elif type.lower() == "fun":
            page1 = discord.Embed(title="Help Commands", description='All the **Fun** commands in the bot. (Page 1)', color=0x00ff00)
            page1.add_field(name=f'{prefix}showpic <query> / {prefix}show <query>', value='Allows you to search a image on the web with a query', inline=False)
            page1.add_field(name=f'{prefix}youtube <query>', value='Allows you to search a video on youtube with a query', inline=False)

            page1.add_field(name=f'{prefix}hack <user>', value='Does a very real and serious hack(I swear)...', inline=False)
            page1.add_field(name=f'{prefix}num2text <number>', value='Converts numbers to words!', inline=False)
            page1.add_field(name=f'{prefix}reverse <text>', value='Reverses your text!', inline=False)
            page1.add_field(name=f'{prefix}wanted <user>', value='''Makes a wanted picture for that user!''', inline=False)
            page1.add_field(name=f'{prefix}level / {prefix}lvl / {prefix}rank', value='''Tells you your level with how much xp you have in that level!''', inline=False)
            page1.add_field(name=f'{prefix}lvllb', value='''Shows people in the server with the highest XP!''', inline=False)
            page1.add_field(name=f'{prefix}guessing', value='''Opens up a guessing game!''', inline=False)
            page1.add_field(name=f'{prefix}calc', value='''Opens up a virtual calculator!''', inline=False)
            page1.add_field(name=f'{prefix}gayrate <user>', value='''Check how gay someone is!''', inline=False)
            
            page2 = discord.Embed(title="Help Commands",description='All the **Fun** commands in the bot. (Page 2)', color=0x00ff00)
            page2.add_field(name=f'{prefix}avatar <user> ', value="Allows you to see someone's avatar picture!",inline=False)
            page2.add_field(name=f'{prefix}encode <method> <text>',value="Allows you to encode text!")
            page2.add_field(name=f'{prefix}decode <method> <text>', value="Allows you to decode text!")
            page2.add_field(name=f'{prefix}dogfact', value="Allows you to learn a fact about dogs!",inline=False)
            page2.add_field(name=f'{prefix}jail <user>', value="Sends a user to jail...",inline=False)
            page2.add_field(name=f'{prefix}trigger <user> / {prefix}trigger <user>', value="Makes a user really triggered...",inline=False)
            page2.add_field(name=f'{prefix}joke', value="Gives you a joke!",inline=False)
            page2.add_field(name=f'{prefix}genderify <name> / {prefix}gender <name>', value="I guess your gender by your name!", inline=False)
            page2.add_field(name=f'{prefix}imposter', value="You have to find the imposter before the reactor has a meltdown!", inline=False)
            page2.add_field(name=f'{prefix}sqrt <number/expression>', value="Gives you the square root of a number or expression!", inline=False)
            page2.add_field(name=f'{prefix}spam', value="Type as many characters as you can in 30 seconds!", inline=False)
            page2.add_field(name=f'{prefix}gay <user>', value="Makes a gay overlay!", inline=False)
            page2.add_field(name=f'{prefix}hunt', value="Allows you to hunt for animals and sell them in the shop!", inline=False)
        
            fun_pages = [page1, page2]
            
            page1.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
            page1.set_footer(text="Page 1/2")

            page2.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
            page2.set_footer(text="Page 2/2. Arguments that are surrounded in [] are optional.")

            buttons = [u"\u23F9",u"\u2B05", u"\u27A1"] #start, exit, right
            current = 0
            msg = await ctx.send(embed=fun_pages[current])

            for button in buttons:
                await msg.add_reaction(button)

            while True:
                try:
                    reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)
                except asyncio.TimeoutError:
                    fun_pages[current].set_footer(text="Timed out :(")
                    await msg.edit(embed=fun_pages[current])
                    break
                else:
                    previous_page = current

                    if reaction.emoji == u"\u2B05":
                        if current > 0:
                            current -= 1

                    elif reaction.emoji == u"\u27A1":
                        if current < len(fun_pages) - 1:
                            current += 1
                    elif reaction.emoji == u"\u23F9":
                        await msg.delete()
                        break


                    if current != previous_page:
                        await msg.edit(embed=fun_pages[current])

                    for button in buttons:
                        await msg.remove_reaction(button, ctx.author)

        elif type.lower() == "misc":
            embedvar = discord.Embed(title="Help Commands",description='All the **Misc** commands in the bot.', color=0x00ff00)
            embedvar.add_field(name=f'{prefix}stats', value='''Allows you to see the bot's stats!''', inline=False)
            embedvar.add_field(name=f'{prefix}members', value='''Allows you to see how many people are in the server!''', inline=False)
            embedvar.add_field(name=f'{prefix}covid <country> / {prefix}covid19 <country>', value='''Allows you to see the covid statistics of a country!''', inline=False)
            embedvar.add_field(name=f'{prefix}roles', value='''Allows you to see all roles in the server!''', inline=False)
            embedvar.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
            await ctx.send(embed=embedvar)







    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def adminhelp(self, ctx):
        ##FIXXXXXX
        embedvar = discord.Embed(title="Admin Help Commands", description='All the commands in the bot that users with permissions can use.', color=0x00ff00)
        embedvar.add_field(name='gcreate <amount of time> <prize>',value='Allows you to create a giveaway. Requires Manage Guild')
        embedvar.add_field(name='reroll <giveaway message id>',value='Allows you reroll a giveaway. Can also be used to forcefully end a giveaway. Requires Manage Guild')
        embedvar.add_field(name='config',value='Allows you to change server configurations. Requires Manage Guild')
        embedvar.add_field(name='takerole <user> <role> ', value="Allows you to take a role away from someone. Requires Manage Roles.")
        embedvar.add_field(name='reactrole <emoji> <role> <message> ', value="Allows you to create reactions roles. Requires Manage Roles.")
        embedvar.add_field(name='scn / set_channel_name  <original channel name> <new channel name> ', value="Allows you to change a channel's name. Requires Manage Channels.")
        embedvar.add_field(name='giverole <user> <role> ', value="Allows you to give a role to someone.**NOTE** You can only give roles up to your highest rank. Requires Manage Roles.")
        embedvar.add_field(name='prefix <prefix> ', value="Allows you to change the prefix of the bot in this server(**Owner only**)")
        embedvar.add_field(name='kick <user> <reason> ', value="Allows you to kick a user with a reason. Requires Kick Users.")
        embedvar.add_field(name='ban <user> <reason> ', value="Allows you to ban a user with a reason. Requires Ban Users.")
        embedvar.add_field(name='unban <user> ', value="Allows you to unban a user. Requires Ban Users.")
        embedvar.add_field(name='mute <user> ', value="Allows you to mute a user. Requires Manage Roles.")
        embedvar.add_field(name='unmute <user> ', value="Allows you to unmute a user. Requires Manage Roles.")
        embedvar.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
        await ctx.send(embed=embedvar)

    @adminhelp.error
    async def adminhelp_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You can't view this!")
            return
def setup(client):
    client.add_cog(Info(client))
