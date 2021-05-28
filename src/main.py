import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import logging
import sqlite3

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

# Bot owners
bot.owner_ids = {453875226757955585, 506093256501755904}

bot.db = sqlite3.connect('main.db')
bot.c = bot.db.cursor()

bot.c.execute("""
        CREATE TABLE IF NOT EXISTS reactrole (
            role_name TEXT,
            role_id INTEGER,
            emoji TEXT,
            message_id INTEGER,
            guild_id INTEGER
        )""")
bot.db.commit()

bot.c.execute("""
        CREATE TABLE IF NOT EXISTS warnings (
            user_id INTEGER,
            reason TEXT,
            guild_id INTEGER
        )""")
bot.db.commit()

if __name__ == '__main__':
    print(os.listdir('/'))
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"Loaded {filename[:-3]}")

# Runs the bot on my token.
bot.run(os.getenv('TOKEN'))
