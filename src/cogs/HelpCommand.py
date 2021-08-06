from discord.ext import commands


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    # Help Command!
    @commands.command(
        name="Help Command",
        description="A command to display help for all other commands!",
        usage="help [command]",
        aliases=[
            "help"
        ]
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _help(self, ctx, cmd=None):
        await ctx.send("S00n:tm:")


def setup(bot):
    bot.add_cog(HelpCommand(bot))
