from nextcord.ext import commands
import nextcord as discord
import wavelink
from datetime import timedelta
import asyncio


class ControlPanel(discord.ui.View):
    def __init__(self, vc, ctx):
        super().__init__()
        self.vc = vc
        self.ctx = ctx
    
    @discord.ui.button(label="Resume/Pause", style=discord.ButtonStyle.blurple)
    async def resume_and_pause(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not interaction.user == self.ctx.author:
            return await interaction.response.send_message("You can't do that. run the command yourself to use these buttons", ephemeral=True)
        for child in self.children:
            child.disabled = False
        if self.vc.is_paused():
            await self.vc.resume()
            await interaction.message.edit(content="Resumed", view=self)
        else:
            await self.vc.pause()
            await interaction.message.edit(content="Paused", view=self)

    @discord.ui.button(label="Queue", style=discord.ButtonStyle.blurple)
    async def queue(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not interaction.user == self.ctx.author:
            return await interaction.response.send_message("You can't do that. run the command yourself to use these buttons", ephemeral=True)
        for child in self.children:
            child.disabled = False
        button.disabled = True
        if self.vc.queue.is_empty:
            return await interaction.response.send_message("The queue is empty!", ephemeral=True)
    
        em = discord.Embed(title="Queue")
        queue = self.vc.queue.copy()
        songCount = 0

        for song in queue:
            songCount += 1
            em.add_field(name=f"Song Num {str(songCount)}", value=f"`{song}`")
        await interaction.message.edit(embed=em, view=self)
    
    @discord.ui.button(label="Skip", style=discord.ButtonStyle.blurple)
    async def skip(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not interaction.user == self.ctx.author:
            return await interaction.response.send_message("You can't do that. run the command yourself to use these buttons", ephemeral=True)
        for child in self.children:
            child.disabled = False
        button.disabled = True
        if self.vc.queue.is_empty:
            return await interaction.response.send_message("The queue is empty!", ephemeral=True)

        try:
            next_song = self.vc.queue.get()
            await self.vc.play(next_song)
            await interaction.message.edit(content=f"Now Playing `{next_song}`", view=self)
        except Exception:
            return await interaction.response.send_message("The queue is empty!", ephemeral=True)
    
    @discord.ui.button(label="Disconnect", style=discord.ButtonStyle.red)
    async def disconnect(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not interaction.user == self.ctx.author:
            return await interaction.response.send_message("You can't do that. run the command yourself to use these buttons", ephemeral=True)
        for child in self.children:
            child.disabled = True
        await self.vc.disconnect()
        await interaction.message.edit(content="Disconnect", view=self)

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot,
                                            host='lavalinkinc.ml',
                                            port=443,
                                            password='incognito',
                                            https=True)

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node <{node.identifier}> is ready!")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self,player: wavelink.Player,track: wavelink.Track,reason):
        ctx = player.ctx
        vc: player = ctx.voice_client
        if vc.loop:
            return await vc.play(track)

        if vc.queue.is_empty:
            await asyncio.sleep(300)
            if not vc.is_playing():
                return await vc.disconnect()

        next_song = vc.queue.get()
        await vc.play(next_song)
        await ctx.send(f"Now playing: `{next_song.title}`")

    @commands.command()
    @commands.is_owner()
    async def play(self, ctx: commands.Context, *,
                   search: wavelink.YouTubeTrack):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(
                cls=wavelink.Player)
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Please join a voice channel!")
        else:
            vc: wavelink.Player = ctx.voice_client
        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(search)
            await ctx.send(f"Now playing: `{search.title}`")
        else:
            await vc.queue.put_wait(search)
            await ctx.send(f"Added `{search.title}` to the queue...")
        vc.ctx = ctx
        try:
            if vc.loop: return
        except:
            setattr(vc,"loop",False)


    @commands.command()
    async def panel(self, ctx: commands.Context):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(
                cls=wavelink.Player)
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Please join a voice channel!")
        else:
            vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            return await ctx.send("You're not playing any music!")
        
        em = discord.Embed(title="Music Panel", description="Control the bot by clicking on the buttons below")
        view = ControlPanel(vc, ctx)
        await ctx.send(embed=em, view=view)

    @commands.command()
    async def pause(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("You're not playing any music!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Please join a voice channel!")
        else:
            vc: wavelink.Player = ctx.voice_client
        await vc.pause()
        await ctx.send("I paused the music :D")

    @commands.command()
    async def resume(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("You're not playing any music!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Please join a voice channel!")
        else:
            vc: wavelink.Player = ctx.voice_client
        await vc.resume()
        await ctx.send("The music is back on!!")

    @commands.command(aliases=['dc', 'stop'])
    async def disconnect(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("You're not playing any music!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Please join a voice channel!")
        else:
            vc: wavelink.Player = ctx.voice_client
        await vc.disconnect()
        await ctx.send("The music has been stopped.")
    @commands.command()
    async def loop(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("You're not playing any music!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Please join a voice channel!")
        else:
            vc: wavelink.Player = ctx.voice_client

        try:
            vc.loop ^= True
        except Exception:
            setattr(vc,"loop",False)


        if vc.loop:
            return await ctx.send("Looping is now enabled!")
        else:
            return await ctx.send("Looping is now disabled!")

    @commands.command(aliases=['q'])
    async def queue(self,ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("You're not playing any music!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Please join a voice channel!")
        vc: wavelink.Player = ctx.voice_client
        if vc.queue.is_empty:
            return await ctx.send("The queue is empty.")
        em = discord.Embed(title="Queue",color=discord.Color.random())
        queue = vc.queue.copy()
        song_count = 0
        for song in queue:
            song_count += 1
            em.add_field(name=f"Song #{song_count}",value=f"{song}")

        return await ctx.send(embed=em)

    @commands.command(aliases=['vol'])
    async def volume(self, ctx: commands.Context, volume: int):
        if not ctx.voice_client:
            return await ctx.send("You're not playing any music!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Please join a voice channel!")
        else:
            vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing():
            return await ctx.send("I'm not playing any music!")

        if volume > 100:
            return await ctx.send("Hold on, thats wayyyy to high.")
        elif volume < 0:
            return await ctx.send("Just stop the music if you don't wanna hear anything.")

        await ctx.send(f"Set the volume to `{volume}%`!")
        try:
            await vc.set_volume(volume)
        except Exception as e:
            print(e)

    @commands.command()
    async def skip(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("You're not playing any music!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Please join a voice channel!")
        else:
            vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            return await ctx.send("I'm not playing any music!")
        try:
            await vc.stop()
            print(vc.is_playing())
        except Exception:
            return await ctx.send("The queue is empty!")
    @commands.command(aliases=["np","playing","current"])
    async def nowplaying(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("You're not playing any music!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Please join a voice channel!")
        else:
            vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            return await ctx.send("I'm not playing any music!")
        em = discord.Embed(title=f"Now Playing: {vc.track.title}",description=f"Artist {vc.track.author}", color=discord.Color.random())
        em.add_field(name="Duration",value=f"`{str(timedelta(seconds=vc.track.length))}`")
        em.add_field(name="Song URL",value=f"[Click Here]({str(vc.track.uri)})")
        return await ctx.send(embed=em)
        

def setup(bot):
    bot.add_cog(Music(bot))

