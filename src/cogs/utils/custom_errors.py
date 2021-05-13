from discord.ext import commands

class NameToColorFail(commands.CheckFailure):
    """
    This error is mainly used for the embed command
    when the user passes the color as name and some
    error happens.
    """
    pass