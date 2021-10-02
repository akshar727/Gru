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

    @commands.command(aliases=['python', 'botinfo'])
    async def bot(self, ctx):
        values = psutil.virtual_memory()
        val2 = values.available * 0.001
        val3 = val2 * 0.001
        val4 = val3 * 0.001

        values2 = psutil.virtual_memory()
        value21 = values2.total
        values22 = value21 * 0.001
        values23 = values22 * 0.001
        values24 = values23 * 0.001

        embedve = discord.Embed(
            title="Bot Info", color=0x9370DB)
        embedve.add_field(
            name="Bot Latency", value=f"Bot latency - {round(self.client.latency * 1000)}ms", inline=False)
        embedve.add_field(name='Hosting Stats', value=f'Cpu usage- {psutil.cpu_percent(1)}%'
                          f'\n(Actual Cpu Usage May Differ)'
                          f'\n'

                          f'\nNumber of Cores - {psutil.cpu_count()} '
                          f'\nNumber of Physical Cores- {psutil.cpu_count(logical=False)}'
                          f'\n'

                          f'\nTotal ram- {round(values24, 2)} GB'
                          f'\nAvailable Ram - {round(val4, 2)} GB')

        await ctx.send(embed=embedve)

    @commands.command(aliases=['help'])
    async def _help(self, ctx,type=None):
        with open('databases/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.guild.id)]
        if type is None:
            embedvar = discord.Embed(title="Help Commands",description='All the commands in the bot.', color=0x00ff00)
            embedvar.add_field(name="Moderation",value=f"Do `{prefix}adminhelp` to see all the moderation commands(**staff only**).")
            embedvar.add_field(name="Economy",value=f"All the economy commands in the bot.Do `{prefix}help economy` to see them.")
            embedvar.add_field(name="Misc",value=f"All the miscellaneous commands in the bot.Do `{prefix}help misc` to see them.")
            embedvar.add_field(name="Fun",value=f"All the fun commands in the bot.Do `{prefix}help fun` to see them.")


            embedvar.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
            await ctx.send(embed=embedvar)
        elif type.lower() == "economy":
            embedvar = discord.Embed(title="Help Commands",description='All the **Economy** commands in the bot.', color=0x00ff00)
            embedvar.add_field(name=f'{prefix}bankrob <user>', value='''Allows you to rob a user's bank''', inline=False)
            embedvar.add_field(name=f'{prefix}get_job', value='Allows you to get a job a Gru enterprises™!', inline=False)
            embedvar.add_field(name=f'{prefix}crates', value='Allows you to view all the crates you have.', inline=False)
            embedvar.add_field(name=f'{prefix}opencrate <type> <amount>', value='Allows you to open your crates!', inline=False)
            embedvar.add_field(name=f'{prefix}crate_info', value='Allows you to view the cash ranges of all the crates.', inline=False)
            embedvar.add_field(name=f'{prefix}jobs', value='Shows a list of all jobs in Gru enterprises™!', inline=False)
            embedvar.add_field(name=f'{prefix}work', value='''Allows you to work and make some money!''', inline=False)
            embedvar.add_field(name=f'{prefix}balance / {prefix}bal', value='To see your balance', inline=False)
            embedvar.add_field(name=f'{prefix}beg', value='To beg some money', inline=False)
            embedvar.add_field(name=f'{prefix}deposit / {prefix}dep', value='To deposit money in bank', inline=False)
            embedvar.add_field(name=f'{prefix}withdraw / {prefix}with', value='To withdraw money from bank', inline=False)
            embedvar.add_field(name=f'{prefix}send', value='Send money to someone', inline=False)
            embedvar.add_field(name=f'{prefix}rob <user>', value='Allows you to rob a user!', inline=False)
            embedvar.add_field(name=f'{prefix}slots', value='To bet some money', inline=False)
            embedvar.add_field(name=f'{prefix}shop', value='To view shop', inline=False)
            embedvar.add_field(name=f'{prefix}buy <amount> <item>', value='To, buy an item', inline=False)
            embedvar.add_field(name=f'{prefix}sell', value='To sell an item', inline=False)
            embedvar.add_field(name=f'{prefix}inventory / {prefix}inv', value='To view your inventory', inline=False)
            embedvar.add_field(name=f'{prefix}viewbal <user>',value='''Allows you to view someone else's balance''',inline=False)
            embedvar.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
            await ctx.send(embed=embedvar)


        elif type.lower() == "fun":
            page1 = discord.Embed(title="Help Commands", description='All the **Fun** commands in the bot. (Page 1)', color=0x00ff00)
            page1.add_field(name=f'{prefix}showpic <query> / {prefix}show <query>', value='Allows you to search a image on the web with a query', inline=False)
            page1.add_field(name=f'{prefix}youtube <query>', value='Allows you to search a video on youtube with a query', inline=False)
            page1.add_field(name=f'{prefix}counter', value='Opens a virtual counter!', inline=False)
            page1.add_field(name=f'{prefix}color', value='Allows you to choose your favorite color!', inline=False)
            page1.add_field(name=f'{prefix}hack <user>', value='Does a very real and serious hack(I swear)...', inline=False)
            page1.add_field(name=f'{prefix}num2text <number>', value='Converts numbers to words!', inline=False)
            page1.add_field(name=f'{prefix}reverse <text>', value='Reverses your text!', inline=False)
            page1.add_field(name=f'{prefix}wanted <user>', value='''Makes a wanted picture for that user!''', inline=False)
            page1.add_field(name=f'{prefix}level / {prefix}lvl / {prefix}rank', value='''Tells you your level with how much xp you have in that level!''', inline=False)
            page1.add_field(name=f'{prefix}guessing', value='''Opens up a guessing game!''', inline=False)
            page1.add_field(name=f'{prefix}calc', value='''Opens up a virtual calculator!''', inline=False)

            
            page2 = discord.Embed(title="Help Commands",description='All the **Fun** commands in the bot. (Page 2)', color=0x00ff00)
            page2.add_field(name=f'{prefix}avatar <user> ', value="Allows you to see someone's avatar picture!",inline=False)
            page2.add_field(name=f'{prefix}encode',value="Allows you to encode text!")
            page2.add_field(name=f'{prefix}decode', value="Allows you to decode text!")
            page2.add_field(name=f'{prefix}dogfact', value="Allows you to learn a fact about dogs!",inline=False)
            page2.add_field(name=f'{prefix}jail <user>', value="Sends a user to jail...",inline=False)
            page2.add_field(name=f'{prefix}triggered <user> / {prefix}trigger <user>', value="Makes a user really triggered...",inline=False)
            page2.add_field(name=f'{prefix}joke', value="Gives you a joke!",inline=False)
            page2.add_field(name=f'{prefix}captcha <text>', value="Allows you to make your very own captcha!", inline=False)
            page2.add_field(name=f'{prefix}achievement <text> [icon]', value=f"Allows you to make a custom Minecraft™ achievement!View all icons by doing '{prefix}ac_icons'", inline=False)
            page2.add_field(name=f'{prefix}genderify <name> / {prefix}gender <name>', value="I guess your gender by your name!", inline=False)
            
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
            embedvar.add_field(name=f'{prefix}bot', value='To see bot info', inline=False)
            embedvar.add_field(name=f'{prefix}members', value='''Allows you to see how many people are in the server!''', inline=False)
            embedvar.add_field(name=f'{prefix}leaderboard / {prefix}lb', value='''Allows you to see the richest people!''', inline=False)
            embedvar.add_field(name=f'{prefix}apply', value='''Allows you to apply for staff.''', inline=False)
            embedvar.add_field(name=f'{prefix}covid <country> / {prefix}covid19 <country>', value='''Allows you to see the covid statistics of a country!''', inline=False)
            embedvar.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
            await ctx.send(embed=embedvar)







    @commands.command()
    @commands.has_any_role("Owner", "Admin", "Sr.Admin", "Moderator")
    async def adminhelp(self, ctx):
        embedvar = discord.Embed(title="Admin Help Commands", description='All the commands in the bot that admins and mods can use.', color=0x00ff00)
        embedvar.add_field(name='gcreate <amount of time> <prize>',value='Allows you to create a giveaway(Sr.Admin only)')
        embedvar.add_field(name='idtouser <id>', value='Allows you to get a user from their id.')
        embedvar.add_field(name='usertoid <user> ', value="Allows you to get a user's id")
        embedvar.add_field(name='takerole <user> <role> ', value="Allows you to take a role away from someone.**NOTE** taking a role away from another staff member could result in your rank being lost and a 2day mute.")
        embedvar.add_field(name='scn / set_channel_name  <original channel name> <new channel name> ', value="Allows you to change a channel's name")
        embedvar.add_field(name='giverole <user> <role> ', value="Allows you to give a role to someone.**NOTE** You can only give roles up to your highest rank.")
        embedvar.add_field(name='registeruser <user> / ,rgu <user> ', value="Allows you to register a user manually.Moderators cannot do this.")
        embedvar.add_field(name='change_prefix <prefix> ', value="Allows you to change the prefix of the bot in this server(**Owner only**)")
        embedvar.add_field(name='kick <user> <reason> ', value="Allows you to kick a user with a reason(**Owner and Sr.Admin only**)")
        embedvar.add_field(name='ban <user> <reason> ', value="Allows you to ban a user with a reason(**Owner and Sr.Admin only**)")
        embedvar.add_field(name='unban <user> ', value="Allows you to unban a user(**Owner and Sr.Admin only**)")
        embedvar.add_field(name='mute <user> ', value="Allows you to mute a user")
        embedvar.add_field(name='unmute <user> ', value="Allows you to unmute a user")
        embedvar.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
        await ctx.send(embed=embedvar)

    @adminhelp.error
    async def adminhelp_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("You can't view this!")
            return
def setup(client):
    client.add_cog(Info(client))
