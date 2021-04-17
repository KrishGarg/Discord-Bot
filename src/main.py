import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import logging

# Loading the .env file to use the token
load_dotenv()

# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='../discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# Initializing the bot
bot = commands.Bot(command_prefix="$", help_command=None, intents=discord.Intents.all(), case_insensitive=True)

# Bot owner
bot.owner_id = 453875226757955585

# Using bot object to transfer data through cogs
bot._start_time = ''
bot._welcomemessagesenabled = False
bot._welcmsgch = 0
bot._leavemessagesenabled = False
bot._leavemsgch = 0

if __name__ == '__main__':
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"Loaded {filename[:-3]}")

# Runs the bot on my token.
bot.run(os.getenv('TOKEN'))
