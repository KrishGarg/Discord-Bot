import asyncio

from discord.ext import commands


class PurgeNuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Purge Command
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def purge(self, ctx, num: int):
        if 0 < num < 100:
            await ctx.channel.purge(limit=num + 1, bulk=True)
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
    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You can't run that!")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Attach the number of messages too idiot!")
            return

        if isinstance(error, commands.BadArgument):
            await ctx.send("Input was wrong! Check the command again!")

    # Nuke command
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nuke(self, ctx, errorHandling=None):
        if errorHandling is None:
            await ctx.reply(
                "Send me a conformation by sending `Yes`. You have 10 seconds! You can cancel this sending `No` or `Cancel`")

            def check(m):
                return m.author == ctx.author and m.content.lower() in ['yes','no','cancel']

            try:
                x = await self.bot.wait_for('message', check=check, timeout=10.0)
            except asyncio.TimeoutError:
                await ctx.send(
                    "I cancelled it because I didn't get any confirmation!")
                return

            if x.content.lower() == "yes":
                old_channel = ctx.channel
                new_channel = await old_channel.clone(reason="Has been NUKED!")
                await old_channel.delete()
                await new_channel.send("**NUKED!**")
                await new_channel.send("https://imgur.com/LIyGeCR")
                return

            else:
                await ctx.send("Noob! Always think before running these types of commands!!")
                return

        else:
            raise commands.CommandError()

    # Nuke command error handling
    @nuke.error
    async def nuke_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Ha! You can't do it!")
            return

        if isinstance(error, commands.CommandError):
            await ctx.send("Something went wrong! Did you gave more than required arguments?!")


def setup(bot):
    bot.add_cog(PurgeNuke(bot))
