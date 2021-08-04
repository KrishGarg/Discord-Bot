import asyncio
import discord
from discord.ext import commands
import typing
from io import BytesIO
import aiohttp
import re
from cogs.utils.converters import EmojiURL

EMOJI_REGEX = re.compile(r'<a?:.+?:([0-9]{15,21})>')
EMOJI_NAME_REGEX = re.compile(r'[0-9a-zA-Z\_]{2,32}')

def emoji_name(argument, *, regex=EMOJI_NAME_REGEX):
    m = regex.match(argument)
    if m is None:
        raise commands.BadArgument('Invalid emoji name.')
    return argument


class OtherModCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Find Message Command
    @commands.command(
        name="Find Message Command",
        description="A command to find a message in the same channel with the message id.",
        usage="findmessage <message_id>",
        aliases=[
            "findmessage"
        ]
    )
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _findmessage(self, ctx, id1: int):
        try:
            the_msg = await ctx.channel.fetch_message(id1)
            await the_msg.reply(content="Gotcha!",mention_author=False)
        except:
            raise commands.BadArgument()

    # Find message error handling
    @_findmessage.error
    async def _findmessage_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the required permission!")
            return
        if isinstance(error, commands.BadArgument):
            await ctx.send("There was some issue with the id you sent!")
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Yo! You have to send me the id too!")
            return

    # Yes No Command!
    @commands.command(
        name="Yes No Poll Command",
        description="A command to make the bot send a message and add the tick and cross emojis to it.",
        usage="yesno <text>",
        aliases=[
            "yesno"
        ]
    )
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _yesno(self, ctx, *, text: str):
        channel = ctx.channel
        await ctx.message.delete()
        sent = await channel.send(text)
        await sent.add_reaction("<a:tick:809071236549443634>")
        await sent.add_reaction("<a:cross2:809071453059153972>")
        return

    # Error handling for yes no comamnd
    @_yesno.error
    async def _yesno_error(self, ctx, error):
        # If user got no permission, then it sends this.
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the permission to do so!")
            return

        # If used didn't send the text, then it sends this
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Yo you forgot the text!")

    # Add yes no command!
    @commands.command(
        name="Add Yes No Command",
        description="A command to add tick and cross emojis to an existing emojis.",
        usage="addyesno <message_id>",
        aliases=[
            "addyesno"
        ]
    )
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _addyesno(self, ctx, msgid: int):
        themsg = await ctx.fetch_message(msgid)
        await ctx.message.delete()
        await themsg.add_reaction("<a:tick:809071236549443634>")
        await themsg.add_reaction("<a:cross2:809071453059153972>")
        await ctx.send("Added!", delete_after=3)

    # Error handling for Add yes no command
    @_addyesno.error
    async def _addyesno_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have enough permission to do so!")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You have to attach the id of the message too!")
            return

        if isinstance(error, commands.CommandError):
            await ctx.send("Some error occured! Try again later.")
            return

    @commands.command(
        name="Message Time Command",
        description="A command to know the exact time, a message was sent.",
        usage="msgtime <message_id>",
        aliases=[
            "msgtime"
        ]
    )
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _msgtime(self, ctx, id1: int):
        await ctx.send(f"Time (in UTC) is: {discord.utils.snowflake_time(id1)}")
        return

    @_msgtime.error
    async def _msgtime_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("First get enough permissions lol!")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to send me the ID too!")
            return

        if isinstance(error, commands.BadArgument):
            await ctx.send("You check the ID again!")
            return

    @commands.command(
        name="Time difference Command",
        description="A command to find the time difference between two sent messages.",
        usage="timediff <message_id_1> <message_id_2>",
        aliases=[
            "timediff"
        ]
    )
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _timediff(self, ctx, id1: int, id2: int):
        datetime1 = discord.utils.snowflake_time(id1)
        datetime2 = discord.utils.snowflake_time(id2)
        if datetime1 > datetime2:
            time1,time2 = datetime1,datetime2
        else:
            time1,time2 = datetime2,datetime1
        difference = (time1-time2)
        await ctx.send(f'Hours: {difference.seconds//3600}\nMinutes: {(difference.seconds//60)%60}\nSeconds: {difference.seconds}\nMicroseconds: {difference.microseconds}')

    # Say command
    @commands.command(
        name="Say Command",
        description="A command to make the bot say something.",
        usage="say <text>",
        aliases=[
            "say"
        ]
    )
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _say(self, ctx, *, text: str):
        await ctx.send(text, allowed_mentions=discord.AllowedMentions(everyone=False))
        await ctx.message.delete()
        return

    @commands.command(
        name="Steal command",
        description="A command to steal an emoji.",
        usage="steal <name> <emoji/url>",
        aliases=[
            "steal"
        ]
    )
    async def _steal(self, ctx, name: emoji_name, *, emoji: EmojiURL):
        """Create an emoji for the server under the given name.
        You must have Manage Emoji permission to use this.
        The bot must have this permission too.
        """

        reason = f'Action done by {ctx.author} (ID: {ctx.author.id})'

        emoji_count = sum(e.animated == emoji.animated for e in ctx.guild.emojis)
        if emoji_count >= ctx.guild.emoji_limit:
            return await ctx.send('There are no more emoji slots in this server.')

        async with self.bot.session.get(emoji.url) as resp:
            if resp.status >= 400:
                return await ctx.send('Could not fetch the image.')
            if int(resp.headers['Content-Length']) >= (256 * 1024):
                return await ctx.send('Image is too big.')
            data = await resp.read()
            coro = ctx.guild.create_custom_emoji(name=name, image=data, reason=reason)
            async with ctx.typing():
                try:
                    created = await asyncio.wait_for(coro, timeout=10.0)
                except asyncio.TimeoutError:
                    return await ctx.send('Sorry, the bot is rate limited or it took too long.')
                except discord.HTTPException as e:
                    return await ctx.send(f'Failed to create emoji somehow: {e}')
                else:
                    return await ctx.send(f'Created {created}')


def setup(bot):
    bot.add_cog(OtherModCmds(bot))
