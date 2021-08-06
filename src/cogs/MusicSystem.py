from discord.ext import commands
import DiscordUtils
from DiscordUtils.Music import NotConnectedToVoice

'''
This entire system is built with the help of DiscordUtils module
and their documentation.
A big and special thanks to them. 
If you want to use the module, here is the link to this module's 
github repository: https://github.com/toxicrecker/DiscordUtils
'''

music = DiscordUtils.Music()


class MusicSystem(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(
        name="Join the VC Command",
        description="A command which makes the bot join your voice channel.",
        usage="join",
        aliases=[
            "join"
        ]
    )
    async def _join(self, ctx):
        try:
            await ctx.author.voice.channel.connect()  # Joins author's voice channel
            await ctx.send(f'Joined your channel {ctx.author.mention}!')
            return
        except Exception:
            await ctx.send("Some issue was there when trying to join your voice channel!")

    @commands.command(
        name="Leave the VC Command",
        description="A command which makes the bot leave the voice channel.",
        usage="leave",
        aliases=[
            "leave",
            "disconnect",
            "dc"
        ]
    )
    async def _leave(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send(f'Good Bye {ctx.author.mention}!')
        return

    @commands.command(
        name="Play the Music Command",
        description="A command that plays the music. The user can either send the youtube link or the name of the song. If the user sends the name, it will lookup for the query on youtube and return the 1st result.",
        usage="play <song_name or youtube_link>",
        aliases=[
            "play"
        ]
    )
    async def _play(self, ctx, *, url):
        player = music.get_player(guild_id=ctx.guild.id)
        try:
            if not music.get_player(guild_id=ctx.guild.id):
                player = music.create_player(ctx)
            if not ctx.voice_client.is_playing():
                await player.queue(url, search=True)
                song = await player.play()
                await ctx.send(f"Playing {song.name}")
                return
            else:
                song = await player.queue(url, search=True)
                await ctx.send(f"Queued {song.name}")
                return
        except NotConnectedToVoice:
            return await ctx.send(f"The bot is not in a voice channel! Please join a voice channel and run `{await self.bot.prefix(ctx.guild.id)}join`.")

    @_play.error
    async def play_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send("You forgot to send me the song name/link!")
        if error == "'NoneType' object is not subscriptable":
            return await ctx.send("There was some issue with playing that song.")

    @commands.command(
        name="Pause the Music Command",
        description="A command which pauses the music the bot is currently playing.",
        usage="pause",
        aliases=[
            "pause"
        ]
    )
    async def _pause(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if not player:
            return await ctx.send("I don't think I am playing anything!")
        song = await player.pause()
        await ctx.send(f"Paused {song.name}")
        return

    @commands.command(
        name="Resume a Music Command",
        description="A command which resumes the paused music.",
        usage="resume",
        aliases=[
            "resume",
            "continue"
        ]
    )
    async def _resume(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if not player:
            return await ctx.send("I don't I have anything to play!")
        song = await player.resume()
        await ctx.send(f"Resumed {song.name}")
        return

    @commands.command(
        name="Stop the Music Command",
        description="A command to stop the music currently playing. Also removes the song from the queue.",
        usage="stop",
        aliases=[
            "stop"
        ]
    )
    async def stop(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if not player:
            return await ctx.send("I don't think I am playing anything!")
        await player.stop()
        await ctx.send("Stopped")
        return

    @commands.command(
        name="Loop The Current Song Command",
        description="A command to loop the currently playing command.",
        usage="loop",
        aliases=[
            "loop"
        ]
    )
    async def _loop(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.toggle_song_loop()
        if song.is_looping:
            await ctx.send(f"Enabled loop for {song.name}")
            return
        else:
            await ctx.send(f"Disabled loop for {song.name}")
            return

    @commands.command(
        name="View Queue Command",
        description="A command to see the current queue.",
        usage="queue",
        aliases=[
            "queue"
        ]
    )
    async def _queue(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if not player:
            return await ctx.send("I don't think I am playing anything!")
        await ctx.send(f"{', '.join([song.name for song in player.current_queue()])}")
        return

    @commands.command(
        name="View Now Playing Command",
        description="A command to see which song is currently being played.",
        usage="nowplaying",
        aliases=[
            "np",
            "nowplaying"
        ]
    )
    async def _np(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if not player:
            return await ctx.send("I don't think I am playing anything!")
        song = player.now_playing()
        await ctx.send(song.name)
        return

    @commands.command(
        name="Skip the Current Song Command",
        description="A command which skips the currently playing song.",
        usage="skip",
        aliases=[
            "skip"
        ]
    )
    async def _skip(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if not player:
            return await ctx.send("I don't think I am playing anything!")
        data = await player.skip(force=True)
        if len(data) == 2:
            await ctx.send(f"Skipped from {data[0].name} to {data[1].name}")
            return
        else:
            await ctx.send(f"Skipped {data[0].name}")
            return

    @commands.command(
        name="Volume Command",
        description="A command to change the volume of the music.",
        usage="volume <0-100>",
        aliases=[
            "volume"
        ]
    )
    async def _volume(self, ctx, vol):
        player = music.get_player(guild_id=ctx.guild.id)
        if not player:
            return await ctx.send("I don't think I am playing anything!")
        if not player:
            return await ctx.send("I don't think I am playing anything!")
        if float(vol) > 100:
            return await ctx.send("Sorry but the max volume that you can set is 100.")
        # volume should be a float between 0 to 1
        song, volume = await player.change_volume(float(vol) / 100.0)
        await ctx.send(f"Changed volume for {song.name} to {volume * 100}%")
        return

    @commands.command(
        name="Remove a Song From Queue Command",
        description="A command to remove a song from the queue.",
        usage="remove <index>",
        aliases=[
            "remove"
        ]
    )
    async def _remove(self, ctx, index):
        player = music.get_player(guild_id=ctx.guild.id)
        if not player:
            return await ctx.send("I don't think I am playing anything!")
        try:
            song = await player.remove_from_queue(int(index))
        except ValueError:
            return await ctx.send("I don't think I recieved a valid index!")
        await ctx.send(f"Removed {song.name} from queue")
        return


def setup(bot):
    bot.add_cog(MusicSystem(bot))
