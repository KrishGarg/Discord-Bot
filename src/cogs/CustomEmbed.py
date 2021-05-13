import discord
from discord.ext import commands
import typing
from cogs.utils import converters

class CustomEmbed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def embed(self, ctx, channel: discord.TextChannel, color: typing.Union[commands.ColorConverter, converters.NameToColorConverter], *, text):
        emb = discord.Embed(title='test', description='test', color=color)
        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(CustomEmbed(bot))