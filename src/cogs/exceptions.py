import cooldowns
from nextcord.ext import commands
import nextcord as discord
import traceback
import datetime
from src.utils import functions


class Exceptions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
            with open("databases/errors.txt", 'a') as f:
                traceback.print_exception(type(error),
                                          error,
                                          error.__traceback__,
                                          file=f)
                f.write("\n")
            traceback.print_exception(type(error),
                                      error,
                                      error.__traceback__)
        elif isinstance(error, commands.CommandNotFound):
            if ctx.author in functions.working_users:
                return functions.working_users.pop(functions.working_users.index(ctx.author))
            prefix = await functions.get_prefix(self.bot, ctx.guild.id)
            await ctx.reply(
                f"Unknown command. Try {prefix}help for a list of commands")
            return
        elif isinstance(error, commands.CommandOnCooldown) or isinstance(error, cooldowns.exceptions.CallableOnCooldown):
            tim = datetime.datetime.now() + datetime.timedelta(seconds=error.retry_after)
            _str = f"<t:{int(tim.timestamp())}:R>"
            if error.retry_after <= 60:
                em = discord.Embed(
                    title=f"Slow it down bro!",
                    description="**Still on cooldown**, please try again in {:.2f}s, or {}"
                    .format(error.retry_after, _str),
                    color=discord.Color.green())
                await ctx.reply(ctx.author.mention, embed=em)
            elif error.retry_after <= 3600:
                mins = int(error.retry_after // 60)
                secs = int(error.retry_after - (mins * 60))
                em = discord.Embed(
                    title=f"Slow it down bro!",
                    description="**Still on cooldown**, please try again in {}m {}s, or {}"
                    .format(mins, secs, _str),
                    color=discord.Color.green())
                await ctx.reply(ctx.author.mention, embed=em)
            elif error.retry_after <= 86400:
                time = error.retry_after
                hrs = int(time // 3600)
                time -= hrs * 3600
                mins = int(time // 60)
                time -= mins * 60
                secs = int(time)
                em = discord.Embed(
                    title=f"Slow it down bro!",
                    description="**Still on cooldown**, please try again in {}h {}m {}s, or {}"
                    .format(hrs, mins, secs, _str),
                    color=discord.Color.green())
                await ctx.reply(ctx.author.mention, embed=em)
            else:
                time = error.retry_after
                days = int(time // 86400)
                time -= days * 86400
                hrs = int(time // 3600)
                time -= hrs * 3600
                mins = int(time // 60)
                time -= mins * 60
                secs = int(time)
                em = discord.Embed(
                    title=f"Slow it down bro!",
                    description="**Still on cooldown**, please try again in {}d {}h {}m {}s, or {}"
                    .format(days, hrs, mins, secs, _str),
                    color=discord.Color.green())
                em.set_footer(text=f"That is at {_str}!")
                await ctx.reply(ctx.author.mention, embed=em)
            return
        elif isinstance(error, commands.RoleNotFound):
            await ctx.reply(":x: Role not found.")
            return
        elif isinstance(error, commands.MemberNotFound):
            await ctx.reply(":x: No member found with that name.")
            return
        elif isinstance(error, commands.NotOwner):
            await ctx.reply(
                ":x: You are not allowed to do this! Only the owner of the bot can do this."
            )
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            prefix = await functions.get_prefix(self.bot, ctx.guild.id)
            await ctx.reply(
                f":x: Missing arguments! check {prefix}help if you need to know about how to use the command."
            )
            try:
                self.bot.get_command(ctx.invoked_with).reset_cooldown(ctx)
            except:
                pass
            return
        elif isinstance(error, commands.MissingPermissions):
            missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in error.missing_permissions
            ]
            if len(missing) > 2:
                fmt = "{}, and {}".format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = " and ".join(missing)
            return await ctx.reply(
                f"You do not have permission to do this! You require the **{fmt}** permissions to do this."
            )
        elif isinstance(error, discord.Forbidden):
            return await ctx.reply(f"I do not have permission to do this!")
        elif isinstance(error, commands.CommandError):
            # await modlog.send(f"Error found: {error}\n")
            with open("databases/errors.txt", 'a') as f:
                traceback.print_exception(type(error),
                                          error,
                                          error.__traceback__,
                                          file=f)
                f.write("\n")
            try:
                self.bot.get_command(ctx.invoked_with).reset_cooldown(ctx)
            except:
                pass
            prefix = await functions.get_prefix(self.bot, ctx.guild.id)
            return await ctx.reply(
                f"An error has occurred with the command!."
                f"Please check `{prefix}help` to make sure you are using the command correctly. Error reported."
            )
        else:
            raise error


def setup(bot):
    bot.add_cog(Exceptions(bot))
