from discord.ext import commands

def is_server_owner():
    def predicate(ctx):
        if ctx.author != ctx.bot.guild.owner:
            raise Exception("Not Owner")
        else:
            return True

    return commands.check(predicate)