import nextcord as discord
from nextcord.ext import commands
from src.utils import functions
import random


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['bal'])
    async def balance(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        else:
            await functions.open_account(user)
        await functions.open_account(ctx.author)
        bank_data = await functions.update_bank(user)
        wallet, bank, booster, max_amt = bank_data[0], bank_data[1], bank_data[3], bank_data[4]
        job_data = await functions.get_job(user)
        job_name, job_pay = job_data[0], job_data[1]

        em = discord.Embed(title=f"{user.display_name}'s Balance",
                           color=discord.Color.green())
        em.add_field(name="Wallet Balance",
                     value=f"{int(wallet):,} Minions™", inline=False)
        em.add_field(name='Bank Balance',
                     value=f"{int(bank):,} **/** {int(max_amt):,} Minions™"
                           f" `({round(float(int(bank) / int(max_amt)) * 100, 2)}% full)`", inline=False)
        em.add_field(name='Job', value=job_name, inline=False)
        em.add_field(name='Job salary',
                     value=f"{int(job_pay):,} Minions™ per hour", inline=False)
        if booster != 1:
            em.add_field(name='Booster', value=f'{float(booster) if not booster % 1 == 0 else int(booster):,}x',
                         inline=False)
        await ctx.reply(embed=em)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        await functions.open_account(ctx.author)
        user = ctx.author
        bank_data = await functions.update_bank(user)
        booster = bank_data[3]

        earnings = random.randrange(1000)

        people = [
            "Elon Musk", "Jeff Bezos", "Mr Krabs", "Your mom", "Kylie Jenners",
            "Albert Einstein", "Mr Mosby", "Greg Heffley",
            "I the all mighty Gru Bot", "Rihanna"
        ]

        person = random.choice(people)
        nums = [0, 1]
        trybeg = random.choice(nums)

        if trybeg == 0:
            message = f'"Oh you beggar take `{(earnings * booster):,} Minions™`"'
            beg_embed = discord.Embed(description=message,
                                      color=discord.Color.random())
            beg_embed.set_author(name=person)
            if booster != 1:
                beg_embed.set_footer(
                    text=f"You earned {(earnings * (booster - 1)):,} extra Minions™ since you had a {booster:,}x "
                         f"booster! "
                )
            await ctx.reply(embed=beg_embed)
            await functions.update_bank(ctx.author, earnings * booster)
        else:
            message = random.choice(
                ['no', 'ur mom', 'credit card is maxed', 'why u', 'nah bro', 'not today', 'nu uh', 'l bozo'])
            beg_embed = discord.Embed(description=message,
                                      color=discord.Color.random())
            beg_embed.set_author(name=person)
            beg_embed.set_footer(text="imagine begging LOL")
            await ctx.reply(embed=beg_embed)

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        await functions.update_bank(ctx.author, 40000)
        await functions.add_lootbox(ctx.author, "epic", 1)
        await ctx.reply(
            "You just recieved `40,000 Minions™` and an `Epic` crate!")

    @commands.command()
    @commands.cooldown(1, 86400 * 7, commands.BucketType.user)
    async def weekly(self, ctx):
        await functions.update_bank(ctx.author, 500000)
        await functions.add_lootbox(ctx.author, "legendary", 5)
        await ctx.reply(
            "You just recieved `500,000 Minions™` and 5 `Legendary` crates!")

    @commands.command(aliases=['with'])
    async def withdraw(self, ctx, amount=None):
        await functions.open_account(ctx.author)
        if amount is None:
            await ctx.reply("Please enter an amount!")
            return
        amount = amount.lower()

        bal = await functions.update_bank(ctx.author)

        if amount == 'max' or amount == 'all':
            amount = bal[1]
        else:
            try:
                amount = functions.convert_str_to_number(amount)
            except ValueError:
                return await ctx.reply("That is an invalid amount!")

        if amount > bal[1]:
            await ctx.reply(f'You do not have `{amount} Minions™` in your bank!')
            return
        if amount < 0:
            await ctx.reply('Amount must be positive!')
            return
        if amount == 0:
            return await ctx.reply("You canot withdraw 0 Minions™ from your bank!")

        await functions.update_bank(ctx.author, amount)
        await functions.update_bank(ctx.author, -1 * amount, 'bank')
        bal = await functions.update_bank(ctx.author)
        e = discord.Embed(title=f"{ctx.author}'s Withdrawal", color=discord.Color.random())
        e.add_field(name="Current Bank Balance", value=f"{int(bal[1]):,} Minions™️")
        e.add_field(name="Current Wallet Balance", value=f"{int(bal[0]):,} Minions™️", inline=True)
        e.add_field(name="Withdrawal Amount", value=f"{int(amount):,} Minions™️", inline=False)
        await ctx.reply(embed=e)

    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, amount=None):
        await functions.open_account(ctx.author)
        if amount is None:
            await ctx.reply("Please enter an amount!")
            return
        amount = amount.lower()
        bal = await functions.update_bank(ctx.author)
        if amount == 'max' or amount == 'all':
            if bal[0] > bal[2]:  # checks if the users balance is greater than the max the bank can hold
                amount = bal[2] - bal[1]
            else:
                amount = bal[0]
        else:
            try:
                amount = functions.convert_str_to_number(amount)
            except ValueError:
                return await ctx.reply("That is an invalid amount!")
        if amount > bal[0]:
            await ctx.reply(f'You do not have `{amount} Minions™` in your wallet!')
            return
        if amount < 0:
            await ctx.reply('Amount must be positive!')
            return
        if amount == 0:
            return await ctx.reply("You cannot deposit 0 Minions™ to your bank!")
        if bal[1] + amount > bal[2]:
            depositable = bal[2] - bal[1]
            await functions.update_bank(ctx.author, -1 * (bal[0] - depositable))
            await functions.update_bank(ctx.author, depositable, 'bank')
            e = discord.Embed(title=f"{ctx.author}'s Deposit", color=discord.Color.random())
            e.add_field(name="Current Bank Balance", value=f"{int(bal[1]):,} Minions™️")
            e.add_field(name="Current Wallet Balance", value=f"{int(bal[0]):,} Minions™️", inline=True)
            e.add_field(name="Deposit Amount", value=f"{int(amount):,} Minions™️", inline=False)
            return await ctx.reply(embed=e)
        else:
            await functions.update_bank(ctx.author, -1 * amount)
            await functions.update_bank(ctx.author, amount, 'bank')
        bal = await functions.update_bank(ctx.author)
        e = discord.Embed(title=f"{ctx.author}'s Deposit", color=discord.Color.random())
        e.add_field(name="Current Bank Balance", value=f"{int(bal[1]):,} Minions™️")
        e.add_field(name="Current Wallet Balance", value=f"{int(bal[0]):,} Minions™️", inline=True)
        e.add_field(name="Deposit Amount", value=f"{int(amount):,} Minions™️", inline=False)
        await ctx.reply(embed=e)

    @commands.command()
    async def send(self, ctx, member: discord.Member, amount=None):
        await functions.open_account(ctx.author)
        await functions.open_account(member)
        if amount is None:
            await ctx.reply("Please enter an amount!")
            return
        amount = amount.lower()
        bal = await functions.update_bank(ctx.author)
        if amount == 'all' or amount == 'max':
            amount = bal[0]

        amount = functions.convert_str_to_number(amount)

        if amount > bal[0]:
            await ctx.reply('You do not have sufficient balance')
            return
        if amount < 0:
            await ctx.reply('Amount must be positive!')
            return

        await functions.update_bank(ctx.author, -1 * amount, 'wallet')
        await functions.update_bank(member, amount, 'wallet')
        await ctx.reply(
            f':white_check_mark: You gave {member} {amount:,} Minions™️'
        )

    @commands.command()
    async def slots(self, ctx, amount=None):
        await functions.open_account(ctx.author)
        if amount is None:
            await ctx.reply("Please enter an amount!")
            return

        bal = await functions.update_bank(ctx.author)

        amount = functions.convert_str_to_number(amount)

        if amount > bal[0]:
            await ctx.reply('You do not have sufficient balance')
            return
        if amount < 0:
            await ctx.reply('Amount must be positive!')
            return
        final = []
        for i in range(3):
            a = random.choice(['Q', 'O', 'X'])

            final.append(a)

        await ctx.reply(str(final))

        if final[0] == final[1] and final[1] == final[2]:
            await functions.update_bank(ctx.author, 3 * amount)
            await ctx.reply(
                f'JACKPOT!!! You won `{3 * amount} Minions™`!!! :tada: :D {ctx.author.mention}'
            )

        elif final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
            await functions.update_bank(ctx.author, 2 * amount)
            await ctx.reply(
                f'You won `{2 * amount} Minions™` :) {ctx.author.mention}')
        else:
            await functions.update_bank(ctx.author, -1 * amount)
            await ctx.reply(
                f'You lose `{1 * amount} Minions™` :( {ctx.author.mention}')


def setup(bot):
    bot.add_cog(Economy(bot))
