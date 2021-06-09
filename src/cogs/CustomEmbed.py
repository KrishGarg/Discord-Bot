import discord
from discord.ext import commands
import typing
from cogs.utils import converters
import shlex

class CustomEmbed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def onelineembed(self, ctx, channel: discord.TextChannel, color: typing.Union[commands.ColorConverter, converters.NameToColorConverter], *, text):
        header, description = shlex.split(text)
        em = discord.Embed(
            title=header,
            description=description,
            color=color
        )
        em.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar_url
        )
        em.set_footer(
            text=self.bot.user.name,
            icon_url=self.bot.user.avatar_url
        )
        await channel.send(embed=em)
        await ctx.message.delete()
        await ctx.send("Sent the message!", delete_after=3)

def setup(bot):
    bot.add_cog(CustomEmbed(bot))