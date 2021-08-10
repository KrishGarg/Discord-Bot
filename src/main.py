import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import logging
import aiosqlite
import aiohttp
from cogs.CustomPrefix import get_prefix
from cogs.utils.helpers import Caching
from pprint import pprint
# Loading the .env file to use the token
load_dotenv()


# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Initializing the bot
bot = commands.Bot(command_prefix=get_prefix, help_command=None,
                   intents=discord.Intents.all(), case_insensitive=True,
                   status=discord.Status.dnd, activity=discord.Game('$help ← Default'))

# Bot owners
bot.owner_ids = {453875226757955585, 506093256501755904}

bot.DEFAULT_PREFIX = "$"


async def pref_help(guild_id: int):
    get = await bot.db.execute("SELECT prefix FROM prefixes WHERE guild_id = ?", (guild_id,))
    pref = await get.fetchone()
    if not pref:
        return bot.DEFAULT_PREFIX
    return pref[0]


bot.prefix = pref_help


async def bot_prepare():
    bot.ses = aiohttp.ClientSession()

    bot.db = await aiosqlite.connect('main.db')

    await bot.db.execute("""
            CREATE TABLE IF NOT EXISTS prefixes (
                guild_id INTEGER,
                prefix TEXT
            )""")
    await bot.db.commit()

    await bot.db.execute("""
            CREATE TABLE IF NOT EXISTS reactrole (
                role_name TEXT,
                role_id INTEGER,
                emoji TEXT,
                message_id INTEGER,
                guild_id INTEGER
            )""")
    await bot.db.commit()

    await bot.db.execute("""
            CREATE TABLE IF NOT EXISTS warnings (
                user_id INTEGER,
                reason TEXT,
                guild_id INTEGER
            )""")
    await bot.db.commit()

bot.loop.run_until_complete(bot_prepare())


async def cache_process():
    async def caching_objs():
        pref = await Caching.make_cleanly(connection=bot.db, table_name="prefixes")
        reactrole = await Caching.make_cleanly(connection=bot.db, table_name="reactrole")
        warnings = await Caching.make_cleanly(connection=bot.db, table_name="warnings")

        return pref, reactrole, warnings

    bot.prefixes_cache, bot.reactrole_cache, bot.warnings_cache = await caching_objs()
    prefixes_initial_data = await bot.prefixes_cache.get_fresh_data()
    reactrole_initial_data = await bot.reactrole_cache.get_fresh_data()
    warnings_initial_data = await bot.warnings_cache.get_fresh_data()
    pprint(prefixes_initial_data)
    print('-----------------------------')
    pprint(reactrole_initial_data)
    print('-----------------------------')
    pprint(warnings_initial_data)
    print('-----------------------------')

bot.loop.run_until_complete(cache_process())

if __name__ == '__main__':
    for filename in os.listdir(os.getcwd() + "/src/cogs"):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"Loaded {filename[:-3]}")

# Runs the bot on my token.
bot.run(os.getenv('TOKEN'))
