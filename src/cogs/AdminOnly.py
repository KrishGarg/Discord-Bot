import discord
from discord.ext import commands
import os

class AdminOnly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Emergency shutdown command
    @commands.command(
        aliases=[
            'disconnect',
            'close',
            'stopbot',
            'logout'
            ],
        hidden=True
        )
    @commands.is_owner()
    async def _logout(self, ctx):
        await ctx.send(f"See you later {ctx.author.mention}!")
        self.bot.db.close()
        await self.bot.close()

    # Emergency shutdown error handling
    @_logout.error
    async def logout_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Ha! No!")

    # Spam command!
    @commands.command(hidden=True)
    @commands.is_owner()
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

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reloadall(self, ctx):
        x = await ctx.send("Reloading all cogs...")

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.bot.reload_extension(f'cogs.{filename[:-3]}')
                print(f"Reloaded {filename[:-3]}")

        await x.edit(content="Reloaded!")
        return

    @commands.command(hidden=True)
    @commands.is_owner()
    async def ghostspammer(self, ctx, count: int, *, text: str):
        await ctx.message.delete()
        for _ in range(count):
            await ctx.send(text, delete_after=0.1)

    @commands.command()
    @commands.is_owner()
    async def ghostdmspammer(self, ctx, user: discord.Member,count: int, *, text: str):
        await ctx.message.delete()
        dm = await user.create_dm()
        try:
            for _ in range(count):
                await dm.send(text, delete_after=0.1)

            await ctx.send(f'{ctx.author.mention}, done the work xd.',delete_after=5)

        except:
            await ctx.send("I think they have their dms closed!")
            return
        return

def setup(bot):
    bot.add_cog(AdminOnly(bot))
