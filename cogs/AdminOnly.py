from discord.ext import commands


class AdminOnly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Emergency shutdown command
    @commands.command(aliases=['disconnect', 'close', 'stopbot'])
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send(f"See you later {ctx.author.mention}!")
        await self.bot.logout()

    # Emergency shutdown error handling
    @logout.error
    async def logout_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Ha! No!")

    # Spam command!
    @commands.command()
    @commands.is_owner()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def spam(self, ctx, count: int, *, text: str):
        await ctx.message.delete()
        for i in range(count):
            await ctx.send(text)
        else:
            await ctx.send("Done! OwO")

    # Spam command error conditions and replies
    @spam.error
    async def spam_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("Lol only my owner can run this.")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing some arguments boss!")
            return

        if isinstance(error, commands.CommandError):
            await ctx.send("Some error occured boss!")
            return


def setup(bot):
    bot.add_cog(AdminOnly(bot))
