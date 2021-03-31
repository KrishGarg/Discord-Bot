from discord.ext import commands
import DiscordUtils

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
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        await ctx.author.voice.channel.connect()  # Joins author's voice channel
        await ctx.send(f'Joined your channel {ctx.author.mention}!')
        return

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send(f'Good Bye {ctx.author.mention}!')
        return

    @commands.command()
    async def play(self, ctx, *, url):
        try:
            player = music.get_player(guild_id=ctx.guild.id)
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
        except Exception as ex:
            print(ex)

    @commands.command()
    async def pause(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.pause()
        await ctx.send(f"Paused {song.name}")
        return

    @commands.command()
    async def resume(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.resume()
        await ctx.send(f"Resumed {song.name}")
        return

    @commands.command()
    async def stop(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        await player.stop()
        await ctx.send("Stopped")
        return

    @commands.command()
    async def loop(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.toggle_song_loop()
        if song.is_looping:
            await ctx.send(f"Enabled loop for {song.name}")
            return
        else:
            await ctx.send(f"Disabled loop for {song.name}")
            return

    @commands.command()
    async def queue(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        await ctx.send(f"{', '.join([song.name for song in player.current_queue()])}")
        return

    @commands.command()
    async def np(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = player.now_playing()
        await ctx.send(song.name)
        return

    @commands.command()
    async def skip(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        data = await player.skip(force=True)
        if len(data) == 2:
            await ctx.send(f"Skipped from {data[0].name} to {data[1].name}")
            return
        else:
            await ctx.send(f"Skipped {data[0].name}")
            return

    # Some issue with this command, will be fixed later.
    # @commands.command()
    # async def volume(self, ctx, vol):
    #     try:
    #         player = music.get_player(guild_id=ctx.guild.id)
    #         song, volume = await player.change_volume(float(vol / 100))  # volume should be a float between 0 to 1
    #         await ctx.send(f"Changed volume for {song.name} to {volume * 100}%")
    #         return
    #     except Exception as ex:
    #         print(ex)

    @commands.command()
    async def remove(self, ctx, index):
        try:
            player = music.get_player(guild_id=ctx.guild.id)
            song = await player.remove_from_queue(int(index))
            await ctx.send(f"Removed {song.name} from queue")
            return
        except Exception as ex:
            print(ex)

def setup(bot):
    bot.add_cog(MusicSystem(bot))