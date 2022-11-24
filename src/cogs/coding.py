import base64
import binascii
import codecs
import nextcord as discord
from io import BytesIO
from nextcord.ext import commands
from nextcord.ext.commands.errors import BadArgument
from src.utils import http, config
import sys


def encode_rot13(text: str):
    """ Encode text with rot13 """
    return codecs.getencoder("rot-13")(text)[0]


def decode_rot13(text: bytes):
    """ Decode text with rot13 """
    return codecs.getdecoder("rot-13")(text)[0]


async def encrypt_out(ctx, convert: str, input_text):
    """ The main, modular function to control encrypt/decrypt commands """
    await ctx.trigger_typing()
    if len(input_text) > 1900:
        try:
            data = BytesIO(input_text.encode("utf-8"))
        except AttributeError:
            data = BytesIO(input_text)

        try:
            return await ctx.reply(content=f"📑 **{convert}**",
                                   file=discord.File(data, filename=config.timetext("Encryption")))
        except discord.HTTPException:
            return await ctx.reply(f"The file I returned was over 8 MB, sorry {ctx.author.name}...")

    try:
        return await ctx.reply(f"📑 **{convert}**```fix\n{input_text.decode('utf-8')}```")
    except AttributeError:
        return await ctx.reply(f"📑 **{convert}**```fix\n{input_text}```")


async def detect_file(ctx):
    """ Detect if user uploaded a file to convert longer text """
    file = ...
    if ctx.message.attachments:
        file = ctx.message.attachments[0].url

        if not file.endswith(".txt"):
            raise LookupError(".txt files only!")

    try:
        content = await http.get(file, no_cache=True)
    except Exception:
        raise UnboundLocalError("Invalid .txt file")

    if not content:
        raise BadArgument("File you've provided is empty")

    return content


class Encryption(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        sys.path.append("..")

    @commands.group()
    async def encode(self, ctx):
        """ All encode methods """
        if ctx.invoked_subcommand is None:
            prefix = await config.get_prefix(self.bot, ctx.guild.id)
            em = discord.Embed(title="Encode Help",
                               description=f"**{prefix}encode**\n\nAll encoding methods.\n\n"
                                           "**Commands**\n**{prefix}encode ascii85 <text>** - Encode in ASCII85\n**{"
                                           "prefix}encode base32 <text>** - Encode in base32\n**{prefix}encode base64 "
                                           "<text>** - Encode in base64\n**{prefix}encode base85 <text>** - Encode in "
                                           "base85\n**{prefix}encode hex <text>** - Encode in hex\n**{prefix}encode "
                                           "rot13 <text>** - Encode in rot13\n**{prefix}encode binary <text>** - "
                                           "Encode in binary",
                               color=discord.Color.random())
            em.set_footer(
                text=f"You can also upload .txt files to encode text also! You can view all the aliases of the "
                     f"encode/decode commands by doing '{prefix}encode aliases'.")
            await ctx.reply(embed=em)

    @commands.group()
    async def decode(self, ctx):
        """ All decode methods """
        if ctx.invoked_subcommand is None:
            prefix = await config.get_prefix(self.bot, ctx.guild.id)
            em = discord.Embed(title="Decode Help",
                               description=f"**{prefix}decode**\n\nAll decoding methods.\n\n"
                                           "**Commands**\n**{prefix}decode ascii85 <text>** - Decode in ASCII85\n**{"
                                           "prefix}decode base32 <text>** - Decode in base32\n**{prefix}decode base64 "
                                           "<text>** - Decode in base64\n**{prefix}decode base85 <text>** - Decode in "
                                           "base85\n**{prefix}decode hex <text>** - Decode in hex\n**{prefix}decode "
                                           "rot13 <text>** - Decode in rot13\n**{prefix}decode binary <text>** - "
                                           "Decode in binary",
                               color=discord.Color.random())
            em.set_footer(
                text=f"You can also upload .txt files to decode text also! You can view all the aliases of the "
                     f"decode/encode commands by doing '{prefix}encode aliases'.")
            await ctx.reply(embed=em)

    @encode.command(name="aliases", aliases=["a"])
    async def coding_aliases(self, ctx):
        e = discord.Embed(title="All encoding types aliases",
                          description="These are all the aliases of the methods to encode/decode text!",
                          color=discord.Color.random())
        e.add_field(name="base32", value="Aliases:`b32`")
        e.add_field(name="base64", value="Aliases:`b64`")
        e.add_field(name="rot13", value="Aliases:`r13`")
        e.add_field(name="hex", value="Aliases:None")
        e.add_field(name="base85", value="Aliases:`b85`")
        e.add_field(name="ascii85", value="Aliases:`a85`")
        e.add_field(name="binary", value="Aliases:`bin`, `bi`")
        await ctx.reply(embed=e)

    @encode.command(name="base32", aliases=["b32"])
    async def encode_base32(self, ctx, *, input_text: commands.clean_content = None):
        """ Encode in base32 """
        if not input_text:
            try:
                input_text = await detect_file(ctx)
            except:
                await ctx.reply("Give me something to encode!")
                return

        await encrypt_out(
            ctx, "Text -> base32", base64.b32encode(input_text.encode("utf-8"))
        )

    @decode.command(name="base32", aliases=["b32"])
    async def decode_base32(self, ctx, *, input_text: commands.clean_content = None):
        """ Decode in base32 """
        if not input_text:
            try:
                input_text = await detect_file(ctx)
            except:
                await ctx.reply("Give me something to decode!")
                return
        try:
            await encrypt_out(ctx, "base32 -> Text", base64.b32decode(input_text.encode("utf-8")))
        except Exception:
            await ctx.reply(f"**{ctx.author.name}**, Invalid base32...")

    @encode.command(name="base64", aliases=["b64"])
    async def encode_base64(self, ctx, *, input_text: commands.clean_content = None):
        """ Encode in base64 """
        if not input_text:
            try:
                input_text = await detect_file(ctx)
            except:
                return await ctx.reply("Give me something to encode!")
        await encrypt_out(
            ctx, "Text -> base64", base64.urlsafe_b64encode(input_text.encode("utf-8"))
        )

    @decode.command(name="base64", aliases=["b64"])
    async def decode_base64(self, ctx, *, input_text: commands.clean_content = None):
        """ Decode in base64 """
        if not input_text:
            try:
                input_text = await detect_file(ctx)
            except:
                return await ctx.reply("Give me something to decode!")
        try:
            await encrypt_out(ctx, "base64 -> Text", base64.urlsafe_b64decode(input_text.encode("utf-8")))
        except Exception:
            await ctx.reply(f"**{ctx.author.name}**, Invalid base64...")

    @encode.command(name="rot13", aliases=["r13"])
    async def encode_rot13(self, ctx, *, input_text: commands.clean_content = None):
        """ Encode in rot13 """
        if not input_text:
            try:
                input_text = await detect_file(ctx)
            except:
                return await ctx.reply("Give me something to encode!")
        await encrypt_out(
            ctx, "Text -> rot13", encode_rot13(input_text)
        )

    @decode.command(name="rot13", aliases=["r13"])
    async def decode_rot13(self, ctx, *, input_text: commands.clean_content = None):
        """ Decode in rot13 """
        if not input_text:
            try:
                input_text = await detect_file(ctx)
            except:
                return await ctx.reply("Give me something to decode!")
        try:
            await encrypt_out(ctx, "rot13 -> Text", bytes(decode_rot13(input_text)))
        except Exception:
            await ctx.reply(f"**{ctx.author.name}**, Invalid rot13...")

    @encode.command(name="hex")
    async def encode_hex(self, ctx, *, input_text: commands.clean_content = None):
        """ Encode in hex """
        if not input_text:
            try:
                input_text = await detect_file(ctx)
            except:
                return await ctx.reply("Give me something to encode!")
        await encrypt_out(
            ctx, "Text -> hex", binascii.hexlify(input_text.encode("utf-8"))
        )

    @decode.command(name="hex")
    async def decode_hex(self, ctx, *, input_text: commands.clean_content = None):
        """ Decode in hex """
        if not input_text:
            try:
                input_text = await detect_file(ctx)
            except:
                return await ctx.reply("Give me something to decode!")
        try:
            await encrypt_out(ctx, "hex -> Text", binascii.unhexlify(input_text.encode("utf-8")))
        except Exception:
            await ctx.reply(f"**{ctx.author.name}**, Invalid hex...")

    @encode.command(name="base85", aliases=["b85"])
    async def encode_base85(self, ctx, *, input_text: commands.clean_content = None):
        """ Encode in base85 """
        if not input_text:
            try:
                input_text = await detect_file(ctx)
            except:
                return await ctx.reply("Give me something to encode!")
        await encrypt_out(
            ctx, "Text -> base85", base64.b85encode(input_text.encode("utf-8"))
        )

    @decode.command(name="base85", aliases=["b85"])
    async def decode_base85(self, ctx, *, input_text: commands.clean_content = None):
        """ Decode in base85 """
        if not input_text:
            try:
                input_text = await detect_file(ctx)
            except:
                return await ctx.reply("Give me something to decode!")
        try:
            await encrypt_out(ctx, "base85 -> Text", base64.b85decode(input_text.encode("utf-8")))
        except Exception:
            await ctx.reply(f"**{ctx.author.name}**, Invalid base85...")

    @encode.command(name="ascii85", aliases=["a85"])
    async def encode_ascii85(self, ctx, *, input_text: commands.clean_content = None):
        """ Encode in ASCII85 """
        if not input_text:
            try:
                input_text = await detect_file(ctx)
            except:
                return await ctx.reply("Give me something to encode!")

        await encrypt_out(
            ctx, "Text -> ASCII85", base64.a85encode(input_text.encode("utf-8"))
        )

    @decode.command(name="ascii85", aliases=["a85"])
    async def decode_ascii85(self, ctx, *, input_text: commands.clean_content = None):
        """ Decode in ASCII85 """
        if not input_text:
            try:
                input_text = await detect_file(ctx)
            except:
                return await ctx.reply("Give me something to decode!")
        try:
            await encrypt_out(ctx, "ASCII85 -> Text", base64.a85decode(input_text.encode("utf-8")))
        except Exception:
            await ctx.reply(f"**{ctx.author.name}**, Invalid ASCII85...")

    @encode.command(name="binary", aliases=["bin", "bi"])
    async def encode_binary(self, ctx, *, input_text: commands.clean_content = None):
        if not input_text:
            try:
                input_text = await detect_file(ctx)
            except:
                return await ctx.reply("Give me something to encode!")

        m = bin(int.from_bytes(input_text.encode(), 'big')).replace('b', '')
        await encrypt_out(ctx, "Text -> Binary", m.encode("utf-8"))

    @decode.command(name="binary", aliases=["bin", "bi"])
    async def decode_binary(self, ctx, *, input_text: commands.clean_content = None):
        if not input_text:
            try:
                input_text = await detect_file(ctx)
            except:
                return await ctx.reply("Give me something to decode!")

        try:
            n = int(input_text.replace(" ", ""), 2)  # text being a command arg
            out = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
        except Exception:
            return await ctx.reply(f"**{ctx.author.name}**, Invalid binary...")

        await encrypt_out(ctx, "Binary -> Text", out.encode("utf-8"))

    @commands.command(aliases=["covid19"])
    async def covid(self, ctx, *, country: str):
        """Covid-19 Statistics for any countries"""
        async with ctx.channel.typing():
            r = await http.get(f"https://disease.sh/v3/covid-19/countries/{country.lower()}", res_method="json")

            if "message" in r:
                return await ctx.reply(f"The API returned an error:\n{r['message']}")

            json_data = [
                ("Total Cases", r["cases"]), ("Total Deaths", r["deaths"]),
                ("Total Recover", r["recovered"]), ("Total Active Cases", r["active"]),
                ("Total Critical Condition", r["critical"]), ("New Cases Today", r["todayCases"]),
                ("New Deaths Today", r["todayDeaths"]), ("New Recovery Today", r["todayRecovered"])
            ]

            embed = discord.Embed(
                description=f"The information provided was last updated <t:{int(r['updated'] / 1000)}:R>",
                color=discord.Color.random()
            )

            for name, value in json_data:
                embed.add_field(
                    name=name, value=f"{value:,}" if isinstance(value, int) else value
                )

            await ctx.reply(
                f"**COVID-19** statistics in :flag_{r['countryInfo']['iso2'].lower()}: "
                f"**{country.capitalize()}** *({r['countryInfo']['iso3']})*",
                embed=embed
            )

    @commands.command(aliases=["joinme", "join", "botinvite"])
    async def invite(self, ctx):
        if f'{ctx.author.id}' == "717512097725939795":

            """ Invite me to your server """
            await ctx.reply(
                f"**{ctx.author.name}**, use this URL to invite me\n<{config.getenv('discord_inv_link')}>")
        else:
            await ctx.reply(
                'Currently, no one but the owner of this bot can invite me.')


def setup(bot):
    bot.add_cog(Encryption(bot))
