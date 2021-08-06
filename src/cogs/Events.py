import time
import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    # On the bot being ready, it does somethings.
    @commands.Cog.listener()
    async def on_ready(self):
        print("We have logged in as {0.user}".format(self.bot))
        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Game('$help ← Default'))
        start_time = time.time()
        self.bot._start_time = start_time

        # Sends pings whenever it is rebooted.
        guild = self.bot.get_guild(770760891394031646)
        channel = guild.get_channel(844978173103439872)
        await channel.send("I was rebooted.")

    # To make the bot tell his prefix when pinged/mentioned
    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.mentioned_in(message) and not message.mention_everyone:
            ctx = await self.bot.get_context(message)
            if ctx.valid:
                return
            await message.channel.send(f"My prefix for this server is `{await self.bot.prefix(message.guild.id)}`.")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            if (before.pinned and not after.pinned) or (not before.pinned and after.pinned):
                return
            await self.bot.process_commands(after)
        except:
            pass

    # Error handling (Atleast some of it)
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f"The command is on cooldown! Try again in {error.retry_after :,.2f} seconds.")

        # Soon will be changed and global error handling s00n:tm:
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"`{await self.bot.prefix(ctx.guild.id)}{ctx.command.aliases[0]} {ctx.command.signature}`.")


def setup(bot):
    bot.add_cog(Events(bot))
