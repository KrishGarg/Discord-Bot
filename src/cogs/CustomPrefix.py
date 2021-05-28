from discord.ext import commands


def get_prefix(bot, message):
    bot.c.execute("SELECT prefix FROM prefixes WHERE guild_id = ?", (message.guild.id,))
    pref = bot.c.fetchone()

    if not pref:
        bot.c.execute("INSERT INTO prefixes VALUES (?, ?)", (message.guild.id, "$"))
        bot.db.commit()
        return commands.when_mentioned_or("$")(bot, message)
    return commands.when_mentioned_or(pref[0])(bot, message)


class CustomPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.c = bot.c

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, new_prefix: str = None):
        old_pref = self.bot.prefix(ctx.guild.id)
        if not new_prefix:
            return await ctx.send(f"Prefix for this server is `{old_pref}`.")
        self.c.execute("UPDATE prefixes SET prefix = ? WHERE guild_id = ?", (new_prefix, ctx.guild.id))
        self.db.commit()
        await ctx.send(f"New prefix for this server is: `{new_prefix}`")

def setup(bot):
    bot.add_cog(CustomPrefix(bot))
