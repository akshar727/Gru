import nextcord as discord
from nextcord.ext import commands
import json
import re


def get_economy_embed(prefix):
    economy_embed = discord.Embed(title="Help Commands",description='All the **Economy** commands in the bot. (Page 1)', color=0x00ff00)
    economy_embed.add_field(name=f'{prefix}bankrob <user>', value='''Allows you to rob a user's bank''', inline=False)
    economy_embed.add_field(name=f'{prefix}work <job name>', value='Allows you to get a job a Gru enterprises™!', inline=False)
    economy_embed.add_field(name=f'{prefix}crates', value='Allows you to view all the crates you have.', inline=False)
    economy_embed.add_field(name=f'{prefix}open <type> <amount>', value='Allows you to open your crates!', inline=False)
    economy_embed.add_field(name=f'{prefix}crateinfo', value='Allows you to view the cash ranges of all the crates.', inline=False)
    economy_embed.add_field(name=f'{prefix}jobs', value='Shows a list of all jobs in Gru enterprises™!', inline=False)
    economy_embed.add_field(name=f'{prefix}work', value='''Allows you to work and make some money!''', inline=False)
    economy_embed.add_field(name=f'{prefix}balance [user] / {prefix}bal [user]', value='Allows you to see the balance of you and others.', inline=False)
    economy_embed.set_footer(text="Arguments that are surrounded in [] are optional. Page 1/3")

    economy_embed_2 = discord.Embed(title="Help Commands",description='All the **Economy** commands in the bot. (Page 2)', color=0x00ff00)
    economy_embed_2.add_field(name=f'{prefix}beg', value='To beg some money', inline=False)
    economy_embed_2.add_field(name=f'{prefix}deposit / {prefix}dep', value='To deposit money in bank', inline=False)
    economy_embed_2.add_field(name=f'{prefix}withdraw / {prefix}with', value='To withdraw money from bank', inline=False)
    economy_embed_2.add_field(name=f'{prefix}send', value='Send money to someone', inline=False)
    economy_embed_2.add_field(name=f'{prefix}rob <user>', value='Allows you to rob a user!', inline=False)
    economy_embed_2.add_field(name=f'{prefix}slots <amount>', value='To bet some money', inline=False)
    economy_embed_2.add_field(name=f'{prefix}shop', value='To view shop', inline=False)
    economy_embed_2.add_field(name=f'{prefix}buy [amount] <item>', value='To, buy an item', inline=False)
    economy_embed_2.set_footer(text="Arguments that are surrounded in [] are optional. Page 2/3")
    
    economy_embed_3 = discord.Embed(title="Help Commands",description='All the **Economy** commands in the bot. (Page 3)', color=0x00ff00)
    economy_embed_3.add_field(name=f'{prefix}sell [amount] <item>', value='Allows you to sell items you get.', inline=False)
    economy_embed_3.add_field(name=f'{prefix}inventory / {prefix}inv', value='Shows you inventory', inline=False)
    economy_embed_3.add_field(name=f'{prefix}leaderboard [amount] / {prefix}lb [amount]', value='''Allows you to see the richest people in the bot!The types are `all` to see all users in the leaderboard and `server` to see only users in this server.''', inline=False)
    economy_embed_3.add_field(name=f'{prefix}daily / {prefix}weekly', value='''Allows you to earn some Minions™️!''', inline=False)
    economy_embed_3.add_field(name=f'{prefix}hunt', value="Allows you to hunt for animals and sell them in the shop!", inline=False)
    economy_embed_3.add_field(name=f'{prefix}fish', value="Allows you to fish for animals and sell them in the shop!", inline=False)
    economy_embed_3.add_field(name=f'{prefix}work resign', value="Allows you to resign from your current job!", inline=False)
    economy_embed_3.add_field(name=f'{prefix}work list', value="Allows you to see all jobs!", inline=False)
    economy_embed_3.set_footer(text="Arguments that are surrounded in [] are optional. Page 3/3")
    ems = [economy_embed, economy_embed_2, economy_embed_3]
    return ems


def get_moderation_embeds(prefix):
    page1 = discord.Embed(title="Help Commands", description='All the **Moderaation** commands in the bot. (Page 1)', color=0x00ff00)
    page1.add_field(name='gcreate <amount of time> <prize>',value='Allows you to create a giveaway. Requires Manage Guild')
    page1.add_field(name='reroll <giveaway message id>',value='Allows you reroll a giveaway. Can also be used to forcefully end a giveaway. Requires Manage Guild')
    page1.add_field(name='config',value='Allows you to change server configurations. Requires Manage Guild')
    page1.add_field(name='takerole <user> <role> ', value="Allows you to take a role away from someone. Requires Manage Roles.")
    page1.add_field(name='reactrole <emoji> <role> <message> ', value="Allows you to create reactions roles. Requires Manage Roles.")
    page1.add_field(name='scn / set_channel_name <original channel name> <new channel name> ', value="Allows you to change a channel's name. Requires Manage Channels.")
    page1.add_field(name='giverole <user> <role> ', value="Allows you to give a role to someone.**NOTE** You can only give roles up to your highest rank. Requires Manage Roles.")
    page1.add_field(name='prefix <prefix> ', value="Allows you to change the prefix of the bot in this server(**Owner only**)")
    page1.set_footer(text="Arguments that are surrounded in [] are optional. Page 1/2")
    
    page2 = discord.Embed(title="Help Commands", description='All the **Moderaation** commands in the bot. (Page 2)', color=0x00ff00)
    page2.add_field(name='kick <user> <reason> ', value="Allows you to kick a user with a reason. Requires Kick Users.")
    page2.add_field(name='ban <user> <reason> ', value="Allows you to ban a user with a reason. Requires Ban Users.")
    page2.add_field(name='unban <user> ', value="Allows you to unban a user. Requires Ban Users.")
    page2.add_field(name='mute <user> <time> ', value="Allows you to mute a user. Requires Manage Roles.")
    page2.add_field(name='unmute <user> <time>', value="Allows you to unmute a user. Requires Manage Roles.")
    page2.add_field(name='setup_tickets', value="Allows you to create a button for users to create tickets. Requires Manage Guild.")
    page2.set_footer(text="Arguments that are surrounded in [] are optional. Page 2/2")

    ems = [page1, page2]
    return ems





def get_music_embeds(prefix):
    page1 = discord.Embed(title="Help Commands", description='All the **Music** commands in the bot. (Page 1)', color=0x00ff00)
    page1.add_field(name=f"{prefix}play <query>",value="Allows you to play/add a song to the queue.", inline=False)
    page1.add_field(name=f"{prefix}pause",value="Pauses the music.", inline=False)
    page1.add_field(name=f"{prefix}resume",value="Resumes the music.", inline=False)
    page1.add_field(name=f"{prefix}disconnect / {prefix}dc", value="Disconnects the bot from the voice channel.", inline=False)
    page1.add_field(name=f"{prefix}loop",value="Toggles looping.", inline=False)
    page1.add_field(name=f"{prefix}panel",value="Opens an interactive panel to control the music.", inline=False)
    page1.add_field(name=f"{prefix}volume <volume>", value="Changes the volume of the music.", inline=False)
    page1.add_field(name=f"{prefix}skip",value="Skips the current song to the next one in the queue.", inline=False)
    page1.set_footer(text="Arguments that are surrounded in [] are optional. Page 1/2")
    
    page2 = discord.Embed(title="Help Commands", description='All the **Music** commands in the bot. (Page 2)', color=0x00ff00)
    page2.add_field(name=f"{prefix}queue / {prefix}q", value="Shows the queue for music.", inline=False)
    page2.add_field(name=f"{prefix}np / {prefix}nowplaying",value="Shows the currently playing song and details.", inline=False)

    pages = [page1, page2]
    return pages

def get_fun_embeds(prefix):
    page1 = discord.Embed(title="Help Commands", description='All the **Fun** commands in the bot. (Page 1)', color=0x00ff00)
    page1.add_field(name=f'{prefix}showpic <query> / {prefix}show <query>', value='Allows you to search a image on the web with a query', inline=False)
    page1.add_field(name=f'{prefix}youtube <query>', value='Allows you to search a video on youtube with a query', inline=False)

    page1.add_field(name=f'{prefix}hack <user>', value='Does a very real and serious hack(I swear)...', inline=False)
    page1.add_field(name=f'{prefix}num2text <number>', value='Converts numbers to words!', inline=False)
    page1.add_field(name=f'{prefix}reverse <text>', value='Reverses your text!', inline=False)
    page1.add_field(name=f'{prefix}wanted <user>', value='''Makes a wanted picture for that user!''', inline=False)
    page1.add_field(name=f'{prefix}level / {prefix}lvl / {prefix}rank', value='''Tells you your level with how much xp you have in that level!''', inline=False)
    page1.add_field(name=f'{prefix}lvllb', value='''Shows people in the server with the highest XP!''', inline=False)
    page1.set_footer(text="Arguments that are surrounded in [] are optional. Page 1/4")
    
    page2 = discord.Embed(title="Help Commands",description='All the **Fun** commands in the bot. (Page 2)', color=0x00ff00)
    page2.add_field(name=f'{prefix}guessing', value='''Opens up a guessing game!''', inline=False)
    page2.add_field(name=f'{prefix}calc', value='''Opens up a virtual calculator!''', inline=False)
    page2.add_field(name=f'{prefix}gayrate <user>', value='''Check how gay someone is!''', inline=False)
    page2.add_field(name=f'{prefix}avatar <user> ', value="Allows you to see someone's avatar picture!",inline=False)
    page2.add_field(name=f'{prefix}encode <method> <text>',value="Allows you to encode text!",inline=False)
    page2.add_field(name=f'{prefix}decode <method> <text>', value="Allows you to decode text!",inline=False)
    page2.add_field(name=f'{prefix}dogfact', value="Allows you to learn a fact about dogs!",inline=False)
    page2.add_field(name=f'{prefix}jail <user>', value="Sends a user to jail...",inline=False)
    page2.set_footer(text="Arguments that are surrounded in [] are optional. Page 2/4")
    
    page3 = discord.Embed(title="Help Commands",description='All the **Fun** commands in the bot. (Page 3)', color=0x00ff00)
    page3.add_field(name=f'{prefix}trigger <user> / {prefix}trigger <user>', value="Makes a user really triggered...",inline=False)
    page3.add_field(name=f'{prefix}joke', value="Gives you a joke!",inline=False)
    page3.add_field(name=f'{prefix}genderify <name> / {prefix}gender <name>', value="I guess your gender by your name!", inline=False)
    page3.add_field(name=f'{prefix}imposter', value="You have to find the imposter before the reactor has a meltdown!", inline=False)
    page3.add_field(name=f'{prefix}sqrt <number or expression>', value="Gives you the square root of a number or expression!", inline=False)
    page3.add_field(name=f'{prefix}spam', value="Type as many characters as you can in 30 seconds!", inline=False)
    page3.add_field(name=f'{prefix}gay <user>', value="Makes a gay overlay!", inline=False)
    page3.add_field(name=f'{prefix}stats', value='''Allows you to see the bot's stats!''', inline=False)
    page3.set_footer(text="Arguments that are surrounded in [] are optional. Page 3/4")
    
    page4 = discord.Embed(title="Help Commands",description='All the **Fun** commands in the bot. (Page 4)', color=0x00ff00)
    page4.add_field(name=f'{prefix}members', value='''Allows you to see how many people are in the server!''', inline=False)
    page4.add_field(name=f'{prefix}covid <country> / {prefix}covid19 <country>', value='''Allows you to see the covid statistics of a country!''', inline=False)
    page4.add_field(name=f'{prefix}roles', value='''Allows you to see all roles in the server!''', inline=False)
    page4.add_field(name=f'{prefix}lvllb', value='''Allows you to see all the top users with the highest levels in the server!''', inline=False)
    page4.set_footer(text="Arguments that are surrounded in [] are optional. Page 4/4")

    fun_pages = [page1, page2,page3, page4]
    return fun_pages


def replaceTextBetween(originalText, delimeterA, delimterB, replacementText):
    try:
        leadingText = originalText.split(delimeterA)[0]
        trailingText = originalText.split(delimterB)[1]
    except:
        return originalText

    return leadingText + replacementText + trailingText


class HelpOptions(discord.ui.Select):
    def __init__(self, buttons):
        self.parent = buttons
        self.items = [discord.SelectOption(label="Economy",default=True),
                discord.SelectOption(label="Fun"),
                discord.SelectOption(label="Moderation"),
                discord.SelectOption(label="Music")]
        super().__init__(placeholder="Choose a category.",min_values=1,max_values=1,options=self.items)
        with open('databases/prefixes.json', 'r') as f:
            self.prefixes = json.load(f)
        

    async def callback(self, interaction: discord.Interaction) -> None:
        type = self.values[0]
        prefix = self.prefixes[str(interaction.guild_id)]
        if interaction.user != self.parent.author:
            await interaction.response.edit_message(view = self.parent)
            return await interaction.send("This is not your help menu.",ephemeral=True)
        if type == "Economy":
            self.options[0].default = True
            self.options[1].default = False
            self.options[2].default = False
            self.options[3].default = False
            self.parent.children[0].disabled = True
            self.parent.children[1].disabled = True
            self.parent.children[2].disabled = False
            self.parent.children[3].disabled = False
            em = get_economy_embed(prefix)
            for i in em:
                i.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
            self.current_embed = em[0]
            self.embeds = em
            await interaction.response.edit_message(embed=em[0],view=self.parent)
        elif type == "Fun":
            self.options[1].default = True
            self.options[2].default = False
            self.options[3].default = False
            self.options[0].default = False
            self.parent.children[0].disabled = True
            self.parent.children[1].disabled = True
            self.parent.children[2].disabled = False
            self.parent.children[3].disabled = False
            em = get_fun_embeds(prefix)
            for i in em:
                i.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
            self.current_embed = em[0]
            self.embeds = em
            await interaction.response.edit_message(embed=em[0],view = self.parent)
        elif type == "Music":
            self.options[3].default = True
            self.options[0].default = False
            self.options[1].default = False
            self.options[2].default = False
            self.parent.children[0].disabled = True
            self.parent.children[1].disabled = True
            self.parent.children[2].disabled = False
            self.parent.children[3].disabled = False
            em = get_music_embeds(prefix)
            for i in em:
                i.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
            self.current_embed = em[0]
            self.embeds = em
            await interaction.response.edit_message(embed=em[0],view = self.parent)
        elif type == "Moderation":
            self.options[2].default = True
            self.options[3].default = False
            self.options[0].default = False
            self.options[1].default = False
            self.parent.children[0].disabled = True
            self.parent.children[1].disabled = True
            self.parent.children[2].disabled = False
            self.parent.children[3].disabled = False
            em = get_moderation_embeds(prefix)
            for i in em:
                i.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
            self.current_embed = em[0]
            self.embeds = em
            await interaction.response.edit_message(embed=em[0],view = self.parent)

class CategoriesView(discord.ui.View):
    def __init__(self, author):
        super().__init__(timeout=30)
        self.author = author
        self.select = HelpOptions(self)
        self.add_item(self.select)

    @discord.ui.button(emoji="<:left_two:982623041228013570>",style=discord.ButtonStyle.green, disabled=True)
    async def begin(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.author:
            return await interaction.response.send_message("This is not your help menu.",ephemeral=True)
        em = self.select.embeds[0]
        self.select.current_embed = em
        button.disabled = True
        self.children[1].disabled = True
        self.children[2].disabled = False
        self.children[3].disabled = False
        await interaction.response.edit_message(embed=em,view=self)
    @discord.ui.button(emoji="<:left_one:982623094235615232>",style=discord.ButtonStyle.green, disabled=True)
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.author:
            return await interaction.response.send_message("This is not your help menu.",ephemeral=True)
        em = self.select.embeds[self.select.embeds.index(self.select.current_embed)-1]
        self.select.current_embed = em
        if self.select.embeds[0] == em:
            button.disabled = True
            self.children[3].disabled = False
            self.children[0].disabled = True
            self.children[1].disabled = True
            self.children[2].disabled = False
        else:
            self.children[3].disabled = False
            self.children[0].disabled = False
            self.children[1].disabled = False
            self.children[2].disabled = False
        await interaction.response.edit_message(embed=em,view=self)
    @discord.ui.button(emoji="<:right_one:982622882469404683>",style=discord.ButtonStyle.green, disabled=False)
    async def forward(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.author:
            return await interaction.response.send_message("This is not your help menu.",ephemeral=True)
        em = self.select.embeds[self.select.embeds.index(self.select.current_embed)+1]
        self.select.current_embed = em
        if self.select.embeds[-1] == em:
            button.disabled = True
            self.children[3].disabled = True
            self.children[0].disabled = False
            self.children[1].disabled = False
        else:
            self.children[3].disabled = False
            self.children[0].disabled = False
            self.children[1].disabled = False
        await interaction.response.edit_message(embed=em,view=self)
    @discord.ui.button(emoji="<:right_two:982622978279899206>",style=discord.ButtonStyle.green, disabled=False)
    async def end(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.author:
            return await interaction.response.send_message("This is not your help menu.",ephemeral=True)
        em = self.select.embeds[-1]
        self.select.current_embed = em
        button.disabled = True
        self.children[2].disabled = True
        self.children[0].disabled = False
        self.children[1].disabled = False
        await interaction.response.edit_message(embed=em,view=self)
    async def on_timeout(self):
        try:
            for x in self.children:
                x.disabled = True
            self.select.disabled = True
            await self.message.edit(view=self)
        except:
            pass




class Info(commands.Cog):
    def __init__(self, client):
        self.client = client
        with open('databases/prefixes.json', 'r') as f:
            self.prefixes = json.load(f)

    @commands.Cog.listener()

    async def on_ready(self):
        print('Info Cog Loaded Succesfully')
        print("Bot is ready to use.")

    @commands.command(aliases=['help'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _help(self, ctx, query=None):
        prefix = self.prefixes[str(ctx.guild.id)]
        if query != None:
            selected = None
            all_pages= get_economy_embed(prefix) + get_moderation_embeds(prefix) + get_music_embeds(prefix) + get_fun_embeds(prefix)
            for page in all_pages:
                for field in page.fields:
                    original_text = field.name
                    original_text = original_text.replace(f"{prefix}","")
                    original_text = re.sub(' <[^>]+>', '', original_text)
                    original_text = re.sub(' \[[^\]]+]', '', original_text)
                    original_text = original_text.split(" / ")
                    space = False
                    for i in original_text:
                        if " " in i and i[len(i)-1] != " ":
                            space = True
                            break
                        elif i[len(i)-1] == " ":
                            original_text[original_text.index(i)] = i.replace(" ","").lower()
                            i = i.replace(" ","")
                    if space:
                        continue
                    if query.lower() in original_text:
                        selected = field
            if selected == None:
                self._help.reset_cooldown(ctx)
                return await ctx.send("Could not find a command with that query!")
            e = discord.Embed(title=f"The '{query.lower()}' command", color=discord.Color.random())
            e.add_field(name=f"Usage: ", value=f"{selected.name}", inline=False)
            e.add_field(name="Description: ",value=selected.value,inline=False)
            return await ctx.reply(embed=e)
        view = CategoriesView(ctx.author)
        view.message = await ctx.reply(f"You can type {prefix}help (any command) to view that command's info!",embed=get_economy_embed(self.prefixes[str(ctx.guild.id)])[0],view=view)

def setup(client):
    client.add_cog(Info(client))
