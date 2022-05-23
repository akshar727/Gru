import base64
import binascii
import codecs
import nextcord as discord
from io import BytesIO
from nextcord.ext import commands
from nextcord.ext.commands.errors import BadArgument
from .utils import http, default
import json



class Encryption(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def encode(self, ctx):
        """ All encode methods """
        if ctx.invoked_subcommand is None:
            with open("/Users/akshardesai/PycharmProjects/Akshar's_projects_and_games/bot/Economy-Bot/Economy_bot_code/databases/prefixes.json", 'r') as f:
                prefixes = json.load(f)
            prefix = prefixes[str(ctx.guild.id)]
            em = discord.Embed(title="Encode Help",description=f"**{prefix}encode**\n\nAll encoding methods.\n\n**Commands**\n**{prefix}encode ascii85 <text>** - Encode in ASCII85\n**{prefix}encode base32 <text>** - Encode in base32\n**{prefix}encode base64 <text>** - Encode in base64\n**{prefix}encode base85 <text>** - Encode in base85\n**{prefix}encode hex <text>** - Encode in hex\n**{prefix}encode rot13 <text>** - Encode in rot13\n**{prefix}encode binary <text>** - Encode in binary",color=discord.Color.random()); em.set_footer(text=f"You can also upload .txt files to encode text also! You can view all the aliases of the encode/decode commands by doing '{prefix}encode aliases'.")
            await ctx.send(embed=em)

    @commands.group()
    async def decode(self, ctx):
        """ All decode methods """
        if ctx.invoked_subcommand is None:
            with open("/Users/akshardesai/PycharmProjects/Akshar's_projects_and_games/bot/Economy-Bot/Economy_bot_code/databases/prefixes.json", 'r') as f:
                prefixes = json.load(f)
            prefix = prefixes[str(ctx.guild.id)]
            em = discord.Embed(title="Decode Help",description=f"**{prefix}decode**\n\nAll decoding methods.\n\n**Commands**\n**{prefix}decode ascii85 <text>** - Decode in ASCII85\n**{prefix}decode base32 <text>** - Decode in base32\n**{prefix}decode base64 <text>** - Decode in base64\n**{prefix}decode base85 <text>** - Decode in base85\n**{prefix}decode hex <text>** - Decode in hex\n**{prefix}decode rot13 <text>** - Decode in rot13\n**{prefix}decode binary <text>** - Decode in binary",color=discord.Color.random()); em.set_footer(text=f"You can also upload .txt files to decode text also! You can view all the aliases of the decode/encode commands by doing '{prefix}encode aliases'.")
            await ctx.send(embed=em)

    @encode.command(name="aliases",aliases=["a"])
    async def coding_aliases(self, ctx):
        e = discord.Embed(title="All encoding types aliases",description="These are all the aliases of the methods to encode/decode text!",color=discord.Color.random())
        e.add_field(name="base32",value="Aliases:`b32`")
        e.add_field(name="base64",value="Aliases:`b64`")
        e.add_field(name="rot13", value="Aliases:`r13`")
        e.add_field(name="hex", value="Aliases:None")
        e.add_field(name="base85", value="Aliases:`b85`")
        e.add_field(name="ascii85", value="Aliases:`a85`")
        e.add_field(name="binary", value="Aliases:`bin`, `bi`")
        await ctx.send(embed=e)

    async def detect_file(self, ctx):
        """ Detect if user uploaded a file to convert longer text """
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

    async def encryptout(self, ctx, convert: str, input):
        """ The main, modular function to control encrypt/decrypt commands """
        await ctx.trigger_typing()
        if len(input) > 1900:
            try:
                data = BytesIO(input.encode("utf-8"))
            except AttributeError:
                data = BytesIO(input)

            try:
                return await ctx.send(content=f"📑 **{convert}**", file=discord.File(data, filename=default.timetext("Encryption")))
            except discord.HTTPException:
                return await ctx.send(f"The file I returned was over 8 MB, sorry {ctx.author.name}...")

        try:
            return await ctx.send(f"📑 **{convert}**```fix\n{input.decode('utf-8')}```")
        except AttributeError:
            return await ctx.send(f"📑 **{convert}**```fix\n{input}```")

    @encode.command(name="base32", aliases=["b32"])
    async def encode_base32(self, ctx, *, input: commands.clean_content = None):
        """ Encode in base32 """
        if not input:
            try:
                input = await self.detect_file(ctx)
            except:
                await ctx.send("Give me something to encode!")
                return

        await self.encryptout(
            ctx, "Text -> base32", base64.b32encode(input.encode("utf-8"))
        )

    @decode.command(name="base32", aliases=["b32"])
    async def decode_base32(self, ctx, *, input: commands.clean_content = None):
        """ Decode in base32 """
        if not input:
            try:
                input = await self.detect_file(ctx)
            except:
                await ctx.send("Give me something to decode!")
                return
        try:
            await self.encryptout(ctx, "base32 -> Text", base64.b32decode(input.encode("utf-8")))
        except Exception:
            await ctx.send(f"**{ctx.author.name}**, Invalid base32...")

    @encode.command(name="base64", aliases=["b64"])
    async def encode_base64(self, ctx, *, input: commands.clean_content = None):
        """ Encode in base64 """
        if not input:
            try:
                input = await self.detect_file(ctx)
            except:
                return await ctx.send("Give me something to encode!")
        await self.encryptout(
            ctx, "Text -> base64", base64.urlsafe_b64encode(input.encode("utf-8"))
        )

    @decode.command(name="base64", aliases=["b64"])
    async def decode_base64(self, ctx, *, input: commands.clean_content = None):
        """ Decode in base64 """
        if not input:
            try:
                input = await self.detect_file(ctx)
            except:
                return await ctx.send("Give me something to decode!")
        try:
            await self.encryptout(ctx, "base64 -> Text", base64.urlsafe_b64decode(input.encode("utf-8")))
        except Exception:
            await ctx.send(f"**{ctx.author.name}**, Invalid base64...")

    @encode.command(name="rot13", aliases=["r13"])
    async def encode_rot13(self, ctx, *, input: commands.clean_content = None):
        """ Encode in rot13 """
        if not input:
            try:
                input = await self.detect_file(ctx)
            except:
                return await ctx.send("Give me something to encode!")
        await self.encryptout(
            ctx, "Text -> rot13", codecs.decode(input, "rot_13")
        )

    @decode.command(name="rot13", aliases=["r13"])
    async def decode_rot13(self, ctx, *, input: commands.clean_content = None):
        """ Decode in rot13 """
        if not input:
            try:
                input = await self.detect_file(ctx)
            except:
                return await ctx.send("Give me something to decode!")
        try:
            await self.encryptout(ctx, "rot13 -> Text", codecs.decode(input, "rot_13"))
        except Exception:
            await ctx.send(f"**{ctx.author.name}**, Invalid rot13...")

    @encode.command(name="hex")
    async def encode_hex(self, ctx, *, input: commands.clean_content = None):
        """ Encode in hex """
        if not input:
            try:
                input = await self.detect_file(ctx)
            except:
                return await ctx.send("Give me something to encode!")
        await self.encryptout(
            ctx, "Text -> hex", binascii.hexlify(input.encode("utf-8"))
        )

    @decode.command(name="hex")
    async def decode_hex(self, ctx, *, input: commands.clean_content = None):
        """ Decode in hex """
        if not input:
            try:
                input = await self.detect_file(ctx)
            except:
                return await ctx.send("Give me something to decode!")
        try:
            await self.encryptout(ctx, "hex -> Text", binascii.unhexlify(input.encode("utf-8")))
        except Exception:
            await ctx.send(f"**{ctx.author.name}**, Invalid hex...")

    @encode.command(name="base85", aliases=["b85"])
    async def encode_base85(self, ctx, *, input: commands.clean_content = None):
        """ Encode in base85 """
        if not input:
            try:
                input = await self.detect_file(ctx)
            except:
                return await ctx.send("Give me something to encode!")
        await self.encryptout(
            ctx, "Text -> base85", base64.b85encode(input.encode("utf-8"))
        )

    @decode.command(name="base85", aliases=["b85"])
    async def decode_base85(self, ctx, *, input: commands.clean_content = None):
        """ Decode in base85 """
        if not input:
            try:
                input = await self.detect_file(ctx)
            except:
                return await ctx.send("Give me something to decode!")
        try:
            await self.encryptout(ctx, "base85 -> Text", base64.b85decode(input.encode("utf-8")))
        except Exception:
            await ctx.send(f"**{ctx.author.name}**, Invalid base85...")

    @encode.command(name="ascii85", aliases=["a85"])
    async def encode_ascii85(self, ctx, *, input: commands.clean_content = None):
        """ Encode in ASCII85 """
        if not input:
            try:
                input = await self.detect_file(ctx)
            except:
                return await ctx.send("Give me something to encode!")

        await self.encryptout(
            ctx, "Text -> ASCII85", base64.a85encode(input.encode("utf-8"))
        )

    @decode.command(name="ascii85", aliases=["a85"])
    async def decode_ascii85(self, ctx, *, input: commands.clean_content = None):
        """ Decode in ASCII85 """
        if not input:
            try:
                input = await self.detect_file(ctx)
            except:
                return await ctx.send("Give me something to decode!")
        try:
            await self.encryptout(ctx, "ASCII85 -> Text", base64.a85decode(input.encode("utf-8")))
        except Exception:
            await ctx.send(f"**{ctx.author.name}**, Invalid ASCII85...")

    @encode.command(name="binary",aliases=["bin","bi"])
    async def encode_binary(self, ctx, *, input: commands.clean_content = None):
        if not input:
            try:
                input = await self.detect_file(ctx)
            except:
                return await ctx.send("Give me something to encode!")

        m = bin(int.from_bytes(input.encode(), 'big')).replace('b', '')
        await self.encryptout(ctx, "Text -> Binary", m.encode("utf-8"))

    @decode.command(name="binary",aliases=["bin","bi"])
    async def decode_binary(self, ctx, *, input: commands.clean_content = None):
        if not input:
            try:
                input = await self.detect_file(ctx)
            except:
                return await ctx.send("Give me something to decode!")

        try:
            n = int(input.replace(" ", ""), 2)  # text being a command arg
            out=n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
        except Exception:
            return await ctx.send(f"**{ctx.author.name}**, Invalid binary...")

        await self.encryptout(ctx, "Binary -> Text", out.encode("utf-8"))


    @commands.command(aliases=["covid19"])
    async def covid(self, ctx, *, country: str):
        """Covid-19 Statistics for any countries"""
        async with ctx.channel.typing():
            r = await http.get(f"https://disease.sh/v3/covid-19/countries/{country.lower()}", res_method="json")

            if "message" in r:
                return await ctx.send(f"The API returned an error:\n{r['message']}")

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

            await ctx.send(
                f"**COVID-19** statistics in :flag_{r['countryInfo']['iso2'].lower()}: "
                f"**{country.capitalize()}** *({r['countryInfo']['iso3']})*",
                embed=embed
            )

    @commands.command(aliases=["joinme", "join", "botinvite"])
    async def invite(self, ctx):
        if f'{ctx.author.id}' == "717512097725939795":

            """ Invite me to your server """
            await ctx.send(
                f"**{ctx.author.name}**, use this URL to invite me\n<https://discord.com/api/oauth2/authorize?client_id=874328552965820416&permissions=8&scope=bot>")
        else:
            await ctx.send(
                'Currently, no one but the owner of this bot can invite me.')

def setup(bot):
    bot.add_cog(Encryption(bot))