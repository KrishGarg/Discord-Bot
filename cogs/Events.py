import discord
from discord.ext import commands, tasks
import time
# for cycling the statuses
from itertools import cycle

# Statuses to cycle through
statuses = cycle(['$help ← Default', 'Sup. I said SUP!'])

class Events(commands.Cog):
    def __init__(self,bot):
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

    # To make the bot tell his prefix when pinged/mentioned
    @commands.Cog.listener()
    async def on_message(self, message):
        mention = [f'<@!{self.bot.user.id}>', f'<@{self.bot.user.id}>']

        # Sends a message in which its prefix is written if the bot is pinged
        if message.content == mention[0] or message.content == mention[1]:
            messagetosend = f"You can use my commands by using `{self.bot.command_prefix}` as the prefix! Try `{self.bot.command_prefix}help` !"
            await message.channel.send(messagetosend)
            return

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            await self.bot.process_commands(after)
        except:
            pass

    # Error handling (Atleast some of it)
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(
                f"Yo I can't find that command. Try `{self.bot.command_prefix}help` for the list of commands available!"
            )

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"The command is on cooldown! Try again in {error.retry_after :,.2f} seconds.")
            return

def setup(bot):
    bot.add_cog(Events(bot))