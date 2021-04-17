import asyncio

from discord.ext import commands


class TimeRel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def timer(self, ctx, time):
        if str(time).endswith('s'):
            timeinsec = int(str(time[:-1]))
        elif str(time).endswith('m'):
            timeinsec = int(str(time[:-1])) * 60
        elif str(time).endswith('h'):
            timeinsec = int(str(time[:-1])) * 60 * 60
        elif str(time).endswith('d'):
            timeinsec = int(str(time[:-1])) * 60 * 60 * 24
        elif str(time).endswith('w'):
            timeinsec = int(str(time[:-1])) * 60 * 60 * 24 * 7
        else:
            await ctx.send("Check the values you sent me again!")
            return

        if timeinsec > 604800:
            await ctx.send("Wanna break me?! Limit is 1 week!!")
            return
        themsg = await ctx.send(f"{timeinsec}s..")
        for i in range(timeinsec):
            timeinsec -= 1
            if timeinsec % 5 == 0:
                await themsg.edit(content=f"{timeinsec}s..")
            await asyncio.sleep(1)
        await themsg.delete()
        await ctx.send(f'{ctx.author.mention}, Timer is Up!')

    @timer.error
    async def timer_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Tell me how long the timer should last in seconds too!")
            return
        if isinstance(error, commands.BadArgument):
            await ctx.send("Umm. Check that time you sent me again dude.")
            return


def setup(bot):
    bot.add_cog(TimeRel(bot))
