import discord
from discord.ext import commands
import asyncio

class StaffApp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Staff App Command
    @commands.command()
    async def staffapp(self, ctx):
        try:
            await ctx.send(
                "Send `Yes` to confirm/start the staff application! You have 5 seconds to reply with yes."
            )

            def check(message):
                return ctx.author == message.author and message.content.lower(
                ) == "yes"

            msg = await self.bot.wait_for('message', check=check, timeout=5.0)
        except asyncio.TimeoutError:
            await ctx.send("Next time rethink before sending that command!")
            return
        else:
            pass

        try:
            dm = await ctx.author.create_dm()
            app = "Consider this as the staff app. I am too lazy to fill it rn kekw. Also you have 20 mins to fill this app and if you get late. don't worry just run the command again and have the answers copied."
            await dm.send(app)
            await ctx.send("Please check your dms to continue the application!")
        except:
            await ctx.send("Open your dms bruh!")
            return

        try:

            def check2(m):
                return m.author == ctx.author and m.guild == None

            the_app = await self.bot.wait_for('message', check=check2, timeout=1200.0)
        except asyncio.TimeoutError:
            await ctx.send("Action Timeouted!")
            await dm.send("Action Timeouted!")
            return
        else:
            pass

        await dm.send("We have received your application!")
        logchannel = await self.bot.fetch_channel(820756992897450005)
        emb = discord.Embed(title='Staff App Received!',
                            description=f'''
    **App from {ctx.author.mention}!**

    {the_app.content}
      ''',
                            color=0x00ff00)
        await logchannel.send(embed=emb)
        return

def setup(bot):
    bot.add_cog(StaffApp(bot))