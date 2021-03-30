import os

# The discord module
import discord
# Gets the commands and tasks module from the discord module
from discord.ext import commands

with open('token.txt', encoding='utf-8') as t:
    token = t.readlines()[0]

intents = discord.Intents.all()

# Initializing the bot
bot = commands.Bot(command_prefix="$", help_command=None, intents=intents)

# Bot owner
bot.owner_id = 453875226757955585

# Using bot object to transfer data through cogs
bot._start_time = ''
bot._welcomemessagesenabled = False
bot._welcmsgch = 0
bot._leavemessagesenabled = False
bot._leavemsgch = 0

if __name__ == '__main__':
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"Loaded {filename[:-3]}")

# Runs the bot on my token.
bot.run(token)
