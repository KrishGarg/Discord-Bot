import discord
from discord.ext import commands
import asyncio

class MuteUnmute(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    # Create mute role command
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def muterole(self,ctx):
        if discord.utils.get(ctx.guild.roles, name="Muted"):
            await ctx.send("Hey looks like there is already a 'Muted' role!")
            return

        await ctx.send(
            "Send `Yes` to confirm the creation of the muted role! You have 20 seconds to reply!"
        )

        try:

            def check(m):
                return m.author == ctx.author and m.content.lower() == 'yes'

            confirmation = await self.bot.wait_for('message', check=check, timeout=20.0)
        except asyncio.TimeoutError:
            await ctx.send("The command timed out!")
            return
        else:
            pass

        sent = await ctx.send("Process started!")
        botmem = await ctx.guild.fetch_member(self.bot.user.id)
        botpos = botmem.top_role.position

        if botpos < 2:
            await ctx.send(
                "Put my role higher please and then run the command again!")
            return

        muterole = await ctx.guild.create_role(name="Muted",
                                               reason="Create Mute Role")
        await muterole.edit(position=botpos)

        try:
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(discord.utils.get(ctx.guild.roles,
                                                                name="Muted"),
                                              send_messages=False,
                                              add_reactions=False)
        except:
            pass

        await sent.edit(
            content=
            "I have created the muted role and its set so that anyone with that role won't be able to speak in any channel."
        )
        return

    @muterole.error
    async def muterole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You ain't got enough permissions!")
            return

        if isinstance(error, commands.CommandError):
            await ctx.send("Some error occured! Try again later!")
            return

    # Mute command
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, user: discord.Member = None, *, reason=None):
        if not discord.utils.get(ctx.guild.roles, name="Muted"):
            await ctx.send(
                f"Looks like there is no 'Muted' role! To make me create one, send `{self.bot.comamand_prefix}muterole` and I will create one for you!"
            )
            return

        if not discord.utils.get(ctx.guild.roles, name="Muted") in user.roles:
            await user.add_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
        else:
            await ctx.send("He is already muted!")
            return

        await ctx.send(f'''
      {user.mention} has been muted by {ctx.author.mention}!
        ''')

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You ain't got enough permissions!")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You missed some arguments looks like!")
            return

        if isinstance(error, commands.BadArgument):
            await ctx.send("I have some issues with those arguments! Check them!")
            return

        if isinstance(error, commands.CommandError):
            await ctx.send("Some error occured! Try again later!")
            return

    # To add the mute role conditions to every channel after it has been created!
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if discord.utils.get(channel.guild.roles, name="Muted"):
            await channel.set_permissions(discord.utils.get(channel.guild.roles, name="Muted"),send_messages = False, add_reactions = False)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, user: discord.Member):
        if discord.utils.get(ctx.guild.roles, name="Muted") in user.roles:
            await user.remove_roles(
                discord.utils.get(ctx.guild.roles, name="Muted"))
            await ctx.send(f"Unmuted {user.mention}!")
            return
        else:
            await ctx.send("There was an error while unmuting that user!")
            return

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You ain't got enough permissions!")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You missed some arguments looks like!")
            return

        if isinstance(error, commands.BadArgument):
            await ctx.send("I have some issues with those arguments! Check them!")
            return

        if isinstance(error, commands.CommandError):
            await ctx.send("Some error occured! Try again later!")
            return


def setup(bot):
    bot.add_cog(MuteUnmute(bot))