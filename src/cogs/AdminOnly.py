import discord
from discord.ext import commands
import os

class AdminOnly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        name="Close Bot",
        description="A command to shut down the bot.",
        usage="logout",
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
    
    @_logout.error
    async def _logout_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Ha! No!")


    @commands.command(
        name="Spam in Chat",
        description="A command to spam some text in a channel. Bot Owner only.",
        usage="spam <count> <text>",
        aliases=[
            "spam"
        ],
        hidden=True
    )
    @commands.is_owner()
    async def _spam(self, ctx, count: int, *, text: str):
        await ctx.message.delete()
        for _ in range(count):
            await ctx.send(text)
        
        await ctx.send("Done! OwO")

    @_spam.error
    async def _spam_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("Lol only my owner can run this.")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing some arguments boss!")
            return

        if isinstance(error, commands.CommandError):
            await ctx.send("Some error occured boss!")
            return


    @commands.command(
        name="Reload all cogs",
        description="A command to reload all cogs. Bot Owner only.",
        usage="reloadall",
        aliases=[
            "reloadall"
        ],
        hidden=True
    )
    @commands.is_owner()
    async def _reloadall(self, ctx):
        x = await ctx.send("Reloading all cogs...")

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.bot.reload_extension(f'cogs.{filename[:-3]}')
                print(f"Reloaded {filename[:-3]}")

        await x.edit(content="Reloaded!")
        return


    @commands.command(
        name="Ghost Spammer",
        description="A command to spam and then delete the messages. Bot Owner only.",
        usage="ghostspammer <count> <text>",
        aliases=[
            "ghostspammer"
        ],
        hidden=True
    )
    @commands.is_owner()
    async def _ghostspammer(self, ctx, count: int, *, text: str):
        await ctx.message.delete()
        for _ in range(count):
            await ctx.send(text, delete_after=0.1)


    @commands.command(
        name="Ghost DM Spammer",
        description="A command to spam someone's dms and then delete those. Bot Owner only.",
        usage="ghostdmspammer <user> <count> <text>",
        aliases=[
            "ghostdmspammer"
        ]
    )
    @commands.is_owner()
    async def _ghostdmspammer(self, ctx, user: discord.Member,count: int, *, text: str):
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
