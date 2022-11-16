from nextcord.ext import commands
import nextcord as discord
import asyncio



async def calculator_button(self, button, interaction):
    if len(self.calculator_embed.description + button.label) >= 4096:
            return
    if interaction.user.id == self.author.id:
        if self.calculator_embed.description == "0" and self.is_placeholder or self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
            self.calculator_embed.description = button.label
            self.is_placeholder = False
        else:
            self.calculator_embed.description += button.label
        await self.calculator_message.edit(embed=self.calculator_embed)



def calculator(exp):
    o = exp.replace('x', '*')
    o = o.replace('÷', '/')
    try:
        result = str(eval(o))
    except:
        result = "An error occurred"

    return result
class Calculator_Buttons(discord.ui.View):
    def __init__(self, author, message, embed, calculator_users):
        super().__init__(timeout=300)
        self.author = author
        self.calculator_message = message
        self.calculator_embed = embed
        self.is_placeholder = True
        self.calculator_users = calculator_users

    @discord.ui.button(label="1", style=discord.ButtonStyle.grey)
    async def one(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label="2", style=discord.ButtonStyle.grey)
    async def two(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label="3", style=discord.ButtonStyle.grey)
    async def three(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label="x", style=discord.ButtonStyle.blurple)
    async def mult(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label="Exit", style=discord.ButtonStyle.danger)
    async def exit(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            await self.calculator_message.edit("The calculator is closing...")
            for i in self.children:
                i.disabled = True
            self.calculator_users.remove(str(self.author.id))
            await self.calculator_message.edit(view=self)
            self.stop()

    @discord.ui.button(label="4", style=discord.ButtonStyle.grey, row=1)
    async def four(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label="5", style=discord.ButtonStyle.grey, row=1)
    async def five(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label="6", style=discord.ButtonStyle.grey, row=1)
    async def six(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label="÷", style=discord.ButtonStyle.blurple, row=1)
    async def div(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label="←", style=discord.ButtonStyle.danger, row=1)
    async def backbutton(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            if self.calculator_embed.description == "An error occurred" or self.calculator_embed.description == "Too big of a number":
                self.calculator_embed.description = "0"
                await self.calculator_message.edit(embed=self.calculator_embed)
                self.is_placeholder = True
                return
            if self.calculator_embed.description[:-1] == "":
                self.calculator_embed.description = "0"
                await self.calculator_message.edit(embed=self.calculator_embed)
                self.is_placeholder = True
                return
            self.calculator_embed.description = self.calculator_embed.description[:-1]
            await self.calculator_message.edit(embed=self.calculator_embed)

    @discord.ui.button(label="7", style=discord.ButtonStyle.grey, row=2)
    async def seven(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label="8", style=discord.ButtonStyle.grey, row=2)
    async def eight(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label="9", style=discord.ButtonStyle.grey, row=2)
    async def nine(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label="+", style=discord.ButtonStyle.blurple, row=2)
    async def plus(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label="Clear", style=discord.ButtonStyle.danger, row=2)
    async def clear(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            self.calculator_embed.description = "0"
            await self.calculator_message.edit(embed=self.calculator_embed)
            self.is_placeholder = True

    @discord.ui.button(label="000", style=discord.ButtonStyle.grey, row=3)
    async def three_zero(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label="//", style=discord.ButtonStyle.grey, row=3)
    async def floor_div(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label="(", style=discord.ButtonStyle.grey, row=3)
    async def left_paren(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label="**", style=discord.ButtonStyle.blurple, row=3)
    async def power(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label=")", style=discord.ButtonStyle.grey, row=3)
    async def right_paren(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label="00", style=discord.ButtonStyle.grey, row=4)
    async def two_zero(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label="0", style=discord.ButtonStyle.grey, row=4)
    async def one_zero(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label=".", style=discord.ButtonStyle.grey, row=4)
    async def point(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label="-", style=discord.ButtonStyle.blurple, row=4)
    async def minus(self, button: discord.ui.Button, interaction: discord.Interaction):
        await calculator_button(self,button,interaction)

    @discord.ui.button(label="=", style=discord.ButtonStyle.green, row=4)
    async def equals(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            if len(calculator(self.calculator_embed.description)) > 4096:
                self.calculator_embed.description = "Too big of a number"
                await self.calculator_message.edit(embed=self.calculator_embed)
            else:
                self.calculator_embed.description = calculator(self.calculator_embed.description)
                await self.calculator_message.edit(embed=self.calculator_embed)

    async def on_timeout(self):
        for x in self.children:
            x.disabled = True
        self.calculator_users.remove(str(self.author.id))
        try:
            await self.calculator_message.edit(view=self)
        except:
            pass



class Calculator(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.calculator_users = []

    @commands.command()
    async def calc(self,ctx):
        if f'{ctx.author.id}' in self.calculator_users:
            await ctx.reply("You already have a calculator open! Close it to open another one!")
            return
        self.calculator_users.append(f'{ctx.author.id}')
        try:
            await ctx.message.delete()
        except:
            pass
        e = discord.Embed(title=f"{ctx.author.name}'s calculator! | {ctx.author.id}", description="0",
                          color=discord.Color.random())
        p = await ctx.send("Calculator loading...", embed=e)
        view = Calculator_Buttons(ctx.author, p, e,self.calculator_users)
        await asyncio.sleep(1)
        await p.edit(view=view)
        await p.edit("Calculator Loaded!")


def setup(bot):
    bot.add_cog(Calculator(bot))
        