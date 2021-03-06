import time
# for cycling the statuses
from itertools import cycle

import discord
from discord.ext import commands, tasks

# Statuses to cycle through
statuses = cycle(['$help ← Default', 'Sup. I said SUP!'])


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # To change the status of the bot every 10 seconds
    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Game(next(statuses)))

    # On the bot being ready, it does somethings.
    @commands.Cog.listener()
    async def on_ready(self):
        print("We have logged in as {0.user}".format(self.bot))
        self.change_status.start()
        start_time = time.time()
        self.bot._start_time = start_time

        # Sends pings whenever it is rebooted.
        guild = self.bot.get_guild(770760891394031646)
        channel = guild.get_channel(844978173103439872)
        await channel.send("I was rebooted.")

    # To make the bot tell his prefix when pinged/mentioned
    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.mentioned_in(message):
            if not message.mention_everyone:
                ctx = await self.bot.get_context(message)
                if ctx.valid:
                    return
                await message.channel.send(f"My prefix for this server is `{self.bot.prefix(message.guild.id)}`.")

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
            await ctx.send(f"The command is on cooldown! Try again in {error.retry_after :,.2f} seconds.")
            return

def setup(bot):
    bot.add_cog(Events(bot))