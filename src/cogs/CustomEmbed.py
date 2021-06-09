import discord
from discord.ext import commands
import typing
from cogs.utils import converters
import shlex
import asyncio
from cogs.utils import custom_errors

class CustomEmbed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="One Line Embed",
        aliases=[
            "onelineembed",
            "olembed"
        ]
    )
    @commands.has_permissions(administrator=True)
    async def _onelineembed(self, ctx, channel: discord.TextChannel, color: typing.Union[commands.ColorConverter, converters.NameToColorConverter], *, title_and_description_separated_by_inverted_commas):
        header, description = shlex.split(title_and_description_separated_by_inverted_commas)
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

    @commands.command(
        name="Step-By-Step Embed Builder",
        aliases=[
            "embed",
            "sbsembed",
            "embedbuilder"
        ]
    )
    @commands.has_permissions(administrator=True)
    async def _embed(self, ctx):
        the_msg = await ctx.send('''
Lets start with the embed builder.
You will have 10 seconds to fill every field. If you have long text, have it copied to your clipboard.
The process will start in 5 seconds.
        ''')
        await asyncio.sleep(5)
        check = lambda m: m.author==ctx.author

        await the_msg.edit(content="Please send the channel in which the embed has to be sent to.")
        try:
            ch = await self.bot.wait_for('message', check=check, timeout=10.0)
        except asyncio.TimeoutError:
            return await the_msg.edit(content="Timeout. Try again later.")
        try:
            channel = await commands.TextChannelConverter().convert(ctx, ch.content)
        except commands.BadArgument:
            await ch.delete()
            return await the_msg.edit(content="That wasn't a valid channel tag/id. Try again later.")
        await ch.delete()
        # 'channel' variable is now a discord.TextChannel.

        await the_msg.edit(content="Please send the color for the embed. You can send the hex code (for eg. #ffffff) or the name (not recommended as some names may not be supported.)")
        try:
            clr = await self.bot.wait_for('message', check=check, timeout=10.0)
        except asyncio.TimeoutError:
            return await the_msg.edit(content="Timeout. Try again later.")
        try:
            color = await commands.ColourConverter().convert(ctx, clr.content)
        except commands.BadArgument:
            try:
                color = await converters.NameToColorConverter().convert(ctx, clr.content)
            except custom_errors.NameToColorFail:
                await clr.delete()
                return await the_msg.edit(content="I couldn't convert that to a valid color. Try again later.")
        await clr.delete()
        # 'color' variable is now a discord.Colour.

        await the_msg.edit(content="Please send the title for the embed.")
        try:
            tle = await self.bot.wait_for('message', check=check, timeout=10.0)
        except asyncio.TimeoutError:
            return await the_msg.edit(content="Timeout. Try again later.")
        title = tle.content
        await tle.delete()
        # 'title' variable has the title of the embed now.

        await the_msg.edit(content="Please send the description for the embed.")
        try:
            des = await self.bot.wait_for('message', check=check, timeout=10.0)
        except asyncio.TimeoutError:
            return await the_msg.edit(content="Timeout. Try again later.")
        description = des.content
        await des.delete()
        # 'description' variable has the description of the embed now.

        em = discord.Embed(
            title=title,
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
        await the_msg.edit(content=f"Embed sent to {channel.mention}!")
        await asyncio.sleep(3)
        await ctx.message.delete()
        await the_msg.delete()

def setup(bot):
    bot.add_cog(CustomEmbed(bot))