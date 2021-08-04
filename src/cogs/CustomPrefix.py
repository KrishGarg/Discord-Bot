from discord.ext import commands


def get_prefix(bot, message):
    bot.c.execute("SELECT prefix FROM prefixes WHERE guild_id = ?", (message.guild.id,))
    pref = bot.c.fetchone()

    if not pref:
        bot.c.execute("INSERT INTO prefixes VALUES (?, ?)", (message.guild.id, bot.DEFAULT_PREFIX))
        bot.db.commit()
        return commands.when_mentioned_or(bot.DEFAULT_PREFIX)(bot, message)
    return commands.when_mentioned_or(pref[0])(bot, message)


class CustomPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.c = bot.c

    @commands.command(
        name="Prefix Changer/Viewer",
        description="A command that helps the administrators of the server view/change the prefix for the guild. Please note that if you reinvite the bot, the prefix will change back to default.",
        usage="prefix [new prefix]",
        aliases=[
            "prefix"
        ]
    )
    @commands.has_permissions(administrator=True)
    async def _prefix(self, ctx, new_prefix: str = None):
        old_pref = self.bot.prefix(ctx.guild.id)
        if not new_prefix:
            return await ctx.send(f"Prefix for this server is `{old_pref}`.")
        self.c.execute("UPDATE prefixes SET prefix = ? WHERE guild_id = ?", (new_prefix, ctx.guild.id))
        self.db.commit()
        await ctx.send(f"New prefix for this server is: `{new_prefix}`")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.c.execute("INSERT INTO prefixes (guild_id, prefix) VALUES (?, ?)", (guild.id, self.bot.DEFAULT_PREFIX))
        self.db.commit()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        self.c.execute("DELETE FROM prefixes WHERE guild_id = ?", (guild.id, ))
        self.db.commit()

def setup(bot):
    bot.add_cog(CustomPrefix(bot))
