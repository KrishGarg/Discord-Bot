import discord
from discord.ext import commands


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Help Command!
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx, cmd=None):
        await ctx.send("S00n:tm:")

def setup(bot):
    bot.add_cog(HelpCommand(bot))
