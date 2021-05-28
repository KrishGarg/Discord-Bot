from discord.ext import commands

# Will be completely remade.

class WelcomeLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(WelcomeLeave(bot))
