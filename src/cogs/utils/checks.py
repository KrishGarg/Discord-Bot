from discord.ext import commands
from .custom_errors import NotGuildOwner


def is_server_owner():
    def predicate(ctx):
        if ctx.author != ctx.bot.guild.owner:
            raise NotGuildOwner("Not the guild owner.")
        else:
            return True

    return commands.check(predicate)
