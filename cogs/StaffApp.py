import discord
from discord.ext import commands
import asyncio

class StaffApp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Staff App Command
    @commands.command()
    async def staffapp(self, ctx):
        emb1 = discord.Embed(title="Staff Application!", description="React to the below 📜 paper to start the process! If you can't start the process, there may be some other person applying so please wait!", color= 0x00ff00)
        emb1.set_footer(text='OwO', icon_url=f'{self.bot.user.avatar_url}')
        emb = await ctx.send(embed=emb1)
        await emb.add_reaction('📜')
        await ctx.message.delete()
        def check(reaction, user):
            return str(reaction.emoji) == '📜'
        while True:
            rr1, applier = await self.bot.wait_for('reaction_add', check=check)
            applier_dm = await applier.create_dm()
            await applier_dm.send("This is a test message")

def setup(bot):
    bot.add_cog(StaffApp(bot))