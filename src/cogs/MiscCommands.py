import discord
import requests
from discord.ext import commands
from requests.exceptions import HTTPError


class MiscCommands(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    # Server Info Command!
    @commands.command(
        name="Server Information Command",
        description="A command to see the server's basic information.",
        usage="svinfo",
        aliases=[
            'svinfo',
            'serverinfo',
            'infoserver',
            'infosv',
            'si'
        ]
    )
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
            text=f"{self.bot.user.name}",
            icon_url=f"{self.bot.user.avatar_url}"
        )

        await ctx.send(embed=the_embed)

    # Avatar command!
    @commands.command(
        name="Avatar Command",
        description="A command to see someone's avatar. Also gives options to view the avatar in the preferred format in the browser.",
        usage="avatar [member]",
        aliases=[
            'avatar',
            'av'
        ]
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _avatar(self, ctx, member: discord.Member = None):
        url = str(member.avatar_url)
        png, jpg, webp = url, url, url

        giforwebp = ""

        if ".webp" in url:
            png = png.replace(".webp", ".png")
            jpg = jpg.replace(".webp", ".jpg")
            giforwebp = "webp"

        if ".gif" in url:
            png = png.replace(".gif", ".png")
            jpg = jpg.replace(".gif", ".jpg")
            giforwebp = "gif"

        the_embed = discord.Embed(title=f'Avatar for {member}',
                                  description="",
                                  color=0x00ff00)
        the_embed.add_field(
            name="***__Click below to open the image in your browser!__***",
            value=f"[png]({png}) | [jpg]({jpg}) | [{giforwebp}]({webp})")
        the_embed.set_image(url=member.avatar_url)
        the_embed.set_footer(
            text=f"{self.bot.user.name}",
            icon_url=f"{self.bot.user.avatar_url}"
        )

        return await ctx.send(embed=the_embed)

    # Avatar command error handling
    @_avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("You check the arguments!")
            return

    # Ping/Latency Command!
    @commands.command(
        name="Ping Command",
        description="A command which returns the latency.",
        usage="ping",
        aliases=[
            "ping",
            "latency"
        ]
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _ping(self, ctx):
        ping = round(self.bot.latency * 1000)
        await ctx.send(f":ping_pong: Pong! Latency is {ping}ms!")
        return

    # Joke Command
    @commands.command(
        name="Joke Command -1",
        description="A command which returns a random joke.",
        usage="joke",
        aliases=[
            "joke"
        ]
    )
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def _joke(self, ctx):
        try:
            joke = requests.get(
                'https://official-joke-api.appspot.com/random_joke').json()
        except HTTPError:
            await ctx.send("There was some issue with our Joke API! Please try again later!!")
            return
        else:
            await ctx.send(f'''
**{joke['setup']}**
||**{joke['punchline']}**||
''')

    # Backup Joke Command
    @commands.command(
        name="Joke Command -2",
        description="Also a joke command.",
        usage="joke2",
        aliases=[
            "joke2"
        ]
    )
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def _joke2(self, ctx):
        try:
            joke = requests.get(
                'https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,racist,sexist,explicit').json()
        except HTTPError:
            await ctx.send("There was some issue with our Joke API! Please try again later!!")
            return
        else:
            if joke['type'] == 'twopart':
                await ctx.send(f'''
**{joke['setup']}**
||**{joke['delivery']}**||
        ''')
                return

            else:
                await ctx.send(f"**{joke['joke']}**")
                return

    # Quote Command
    @commands.command(
        name="Quote Command",
        description="An quote command which returns a random quote with its author.",
        usage="quote",
        aliases=[
            "quote"
        ]
    )
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def _quote(self, ctx):
        try:
            try:
                quote = requests.get('http://api.quotable.io/random').json()
            except HTTPError:
                await ctx.send("There was some issue with our Quote API! Please try again later!!")
                return
            else:
                await ctx.send(f'''
    *{quote["content"]}*  - **{quote["author"]}**
                ''')
        except Exception as ex:
            print(ex)


def setup(bot):
    bot.add_cog(MiscCommands(bot))
