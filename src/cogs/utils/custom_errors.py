from discord.ext import commands


class NameToColorFail(commands.CheckFailure):
    """
    This error is mainly used for the embed command
    when the user passes the color as name and some
    error happens.
    """
    pass


class NotGuildOwner(commands.CheckFailure):
    """
    This error is used for the check 'is_server_owner'.
    """
    pass


class CacheError(Exception):
    """
    CacheError A base/common error for the caching system.

    Extends
    -------
    Exception :
        A normal exception.
    """
    pass
