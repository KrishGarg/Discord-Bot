from discord.ext import commands
import discord

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command()
    async def github(self, ctx):
        em = discord.Embed(
            title="My Github Repository!", 
            description="Thanks for showing interest in my source code! [Click Me](https://github.com/KrishGarg/Discord-Bot) to visit my github repository!",
            color=0x00ff00
        )
        em.set_footer(text=f"{self.bot.user.name}", icon_url=f"{self.bot.user.avatar_url}")
        await ctx.send(embed=em)

    @commands.command()
    async def invite(self, ctx):
        em = discord.Embed(
            title="Invite me to your server!",
            description="Thanks for showing interest in inviting me to your server! [Click Me](https://discord.com/oauth2/authorize?client_id=810187428086022254&scope=bot&permissions=8) to invite me to your server.",
            color=0x00ff00
        )
        em.set_footer(text=f"{self.bot.user.name}", icon_url=f"{self.bot.user.avatar_url}")
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Support(bot))