import asyncio

import discord
from discord.ext import commands

class PurgeNuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Purge Command
    @commands.command(
        name="Purge Messages Command",
        description="A command to delete some messages in bulk quickly.",
        usage="purge <number_of_messages_to_delete>",
        aliases=[
            "purge"
        ]
    )
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _purge(self, ctx, num: int, user: discord.Member = None):

        if user:
            check_func = lambda m: m.author == user and not m.pinned

        else:
            check_func = lambda m: not m.pinned

        if 0 < num < 100:
            await ctx.channel.purge(limit=num + 1, bulk=True, check=check_func)
            if user:
                await ctx.message.delete()
            await ctx.send("Purged! If there were any pinned messages, they would have been ignored!", delete_after=3)
            return

        elif num > 100:
            await ctx.send(
                "The number of messages to send was too high! Max is 100 at a time!"
            )
            return

        elif num < 0:
            await ctx.send("The number of messages to send was too low! Min is 1!")
            return

        elif num == 0:
            await ctx.send(
                "Discord's API can't help me in any way to delete `0` messages! Try a number between 1 - 99 instead!"
            )
            return

        elif num == 100:
            await ctx.send(
                "Discord's API can't help me in any way to delete `100` messages! Try a number between 1 - 99 instead!"
            )
            return

    # Purge Command error handling
    @_purge.error
    async def _purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You can't run that!")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Attach the number of messages too idiot!")
            return

        if isinstance(error, commands.BadArgument):
            await ctx.send("Input was wrong! Check the command again!")

    # Nuke command
    @commands.command(
        name="Nuke command",
        description="A command to delete and then remake a channel.",
        usage="nuke",
        aliases=[
            "nuke"
        ]
    )
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _nuke(self, ctx):
        await ctx.reply(
            "Send me a conformation by sending `Yes`. You have 10 seconds!")

        try:
            x = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.send(
                "I cancelled it because I didn't get any confirmation!")
            return

        if x.content.lower() == "yes":
            old_channel = ctx.channel
            new_channel = await old_channel.clone(reason="Has been NUKED!")
            await old_channel.delete()
            embed1 = discord.Embed(title="NUKED!",description=f'**This channel was nuked by {ctx.author.mention}.**',color=0x00ff00)
            embed1.set_footer(text=f'{self.bot.user.name}',icon_url=self.bot.user.avatar_url)
            embed1.set_image(url="https://media2.giphy.com/media/HhTXt43pk1I1W/giphy.gif?cid=ecf05e47l2gij7b6xv29vavlho3z6mxdi8bdm3o626p2pfcb&rid=giphy.gif&ct=g")
            await new_channel.send(embed=embed1)
            return

        else:
            await ctx.send("Noob! Always think before running these types of commands!!")
            return

    # Nuke command error handling
    @_nuke.error
    async def _nuke_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Ha! You can't do it!")
            return

        if isinstance(error, commands.CommandError):
            await ctx.send("Something went wrong! Did you gave more than required arguments?!")


def setup(bot):
    bot.add_cog(PurgeNuke(bot))
