import os
import aiohttp
from dotenv import load_dotenv
import discord
from discord.ext import commands
import logging

from cogs.CustomPrefix import get_prefix

# Loading the .env file to use the token
load_dotenv()

# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='../discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Initializing the bot
bot = commands.Bot(command_prefix=get_prefix, help_command=None, intents=discord.Intents.all(), case_insensitive=True)

# Bot owners
bot.owner_ids = {453875226757955585, 506093256501755904}

bot.DEFAULT_PREFIX = "$"

def pref_help(guild_id: int):
    bot.c.execute("SELECT prefix FROM prefixes WHERE guild_id = ?", (guild_id,))
    pref = bot.c.fetchone()
    if not pref:
        return bot.DEFAULT_PREFIX
    return pref[0]


bot.prefix = pref_help

bot.ses = aiohttp.ClientSession()

if __name__ == '__main__':
    print(os.listdir('/'))
    for filename in os.listdir('/cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"Loaded {filename[:-3]}")

# Runs the bot on my token.
bot.run(os.getenv('TOKEN'))
