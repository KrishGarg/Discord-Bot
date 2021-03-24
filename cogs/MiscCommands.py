import datetime
import time

import discord
from discord.ext import commands


class MiscCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Uptime Command
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
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

    # Server Info Command!
    @commands.command(aliases=['svinfo', 'serverinfo', 'infoserver', 'infosv', 'si'])
    @commands.cooldown(1, 20, commands.BucketType.user)
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

    # Avatar command!
    @commands.command(aliases=['avatar', 'av'])
    @commands.cooldown(1, 10, commands.BucketType.user)
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
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        ping = round(self.bot.latency * 1000)
        await ctx.send(f":ping_pong: Pong! Latency is {ping}ms!")


def setup(bot):
    bot.add_cog(MiscCommands(bot))
