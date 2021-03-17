import discord
from discord.ext import commands
import time, datetime, asyncio


class MiscCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    # Uptime Command
    @commands.command()
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - self.bot._start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=0x00ff00)
        embed.add_field(name="Uptime", value=text)
        embed.set_footer(
            text="OwO",
            icon_url=
            "https://cdn.discordapp.com/avatars/810187428086022254/dcc43fae4bc05ec1db81c516ded44224.png?size=1024"
        )
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + text)

    # Staff App Command
    @commands.command()
    async def staffapp(self,ctx):
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

    # Server Info Command!
    @commands.command(aliases=['svinfo', 'serverinfo', 'infoserver', 'infosv', 'si'])
    async def _svinfo(self, ctx):
        the_embed = discord.Embed(title="Server Info!", color=0x00ff00)
        the_embed.add_field(name="**__Server Name__**",
                            value=f'***{ctx.message.guild.name}***',
                            inline=True)
        the_embed.add_field(name="**__Server ID__**",
                            value=f'***{ctx.message.guild.id}***',
                            inline=True)
        the_embed.add_field(name="**__Server Description__**",
                            value=f'***{ctx.message.guild.description}***',
                            inline=False)
        the_embed.add_field(name="**__Members__**",
                            value=f'***{ctx.message.guild.member_count}***',
                            inline=True)
        the_embed.add_field(name="**__Text Channels__**",
                            value=f'***{len(ctx.message.guild.text_channels)}***',
                            inline=True)
        the_embed.add_field(name="**__Voice Channels__**",
                            value=f'***{len(ctx.message.guild.voice_channels)}***',
                            inline=True)
        region1 = str(ctx.guild.region).capitalize()
        the_embed.add_field(name="**__Region__**",
                            value=f'**{region1}**',
                            inline=True)
        the_embed.add_field(name="**__Boosts__**",
                            value=f'**{ctx.guild.premium_subscription_count}**',
                            inline=True)
        the_embed.set_author(name=ctx.message.author.name,
                             icon_url=ctx.message.author.avatar_url)
        the_embed.set_thumbnail(url=ctx.guild.icon_url)
        the_embed.set_footer(
            text="OwO",
            icon_url=
            "https://cdn.discordapp.com/avatars/810187428086022254/dcc43fae4bc05ec1db81c516ded44224.png?size=1024"
        )

        await ctx.send(embed=the_embed)

    # Say command
    @commands.command()
    async def say(self, ctx, *, text: str):
        x = text
        if "{@}" in text:
            x = text.replace("{@}", "@")
        await ctx.send(x)
        await ctx.message.delete()

    # Avatar command!
    @commands.command(aliases=['avatar', 'av'])
    async def _avatar(self, ctx, *, para=None):
        while True:
            try:
                mention1 = para
                a = mention1
                if "<@" in mention1 and ">" in mention1:
                    a = a.replace("<", "")
                    a = a.replace(">", "")
                    a = a.replace("@", "")

                if "!" in a:
                    a = a.replace("!", "")

            except Exception:
                the_user = ctx.message.author

            else:
                the_user = await bot.fetch_user(int(a))

            url = str(the_user.avatar_url)
            png = url
            jpg = url
            webp = url

            giforwebp = ""

            if ".webp" in url:
                png = png.replace(".webp", ".png")
                jpg = jpg.replace(".webp", ".jpg")
                giforwebp = "webp"

            if ".gif" in url:
                png = png.replace(".gif", ".png")
                jpg = jpg.replace(".gif", ".jpg")
                giforwebp = "gif"

            the_embed = discord.Embed(title=f'Avatar for {the_user}',
                                      description="")
            the_embed.add_field(
                name="***__Click below to open the image in your browser!__***",
                value=f"[png]({png}) | [jpg]({jpg}) | [{giforwebp}]({webp})")
            the_embed.set_image(url=the_user.avatar_url)

            await ctx.send(embed=the_embed)
            return

    # Avatar command error handling
    @_avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("You check the arguments!")
            return

        if isinstance(error, commands.CommandError):
            await ctx.send("Some error occured! Try again later!")
            return

    # Ping/Latency Command!
    @commands.command()
    async def ping(self, ctx):
        ping = round(self.bot.latency * 1000)
        await ctx.send(f":ping_pong: Pong! Latency is {ping}ms!")


def setup(bot):
    bot.add_cog(MiscCommands(bot))