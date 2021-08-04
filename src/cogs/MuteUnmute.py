import asyncio

import discord
from discord.ext import commands


class MuteUnmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Create mute role command
    @commands.command(
        name="Create the Muterole command",
        description="A command to create the muterole for the server.",
        usage="muterole",
        aliases=[
            "muterole"
        ]
    )
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _muterole(self, ctx):
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

    @_muterole.error
    async def muterole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You ain't got enough permissions!")
            return

        if isinstance(error, commands.CommandError):
            await ctx.send("Some error occured! Try again later!")
            return

    # Mute command
    @commands.command(
        name="Mute Command",
        description="A command to mute a person.",
        usage="mute <member>",
        aliases=[
            "mute"
        ]
    )
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _mute(self, ctx, user: discord.Member = None):

        if ctx.author.top_role.position <= user.top_role.position:
            await ctx.send("Lol you have mute perms but you are not as powerful as the guy you are trying to mute!")
            return

        if not discord.utils.get(ctx.guild.roles, name="Muted"):
            await ctx.send(
                f"Looks like there is no 'Muted' role! To make me create one, send `{self.bot.prefix(ctx.guild.id)}muterole` and I will create one for you!"
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

        try:
            dmemb = discord.Embed(title="You were MUTED!", color=0x00ff00, description=f'''
You were muted in **{ctx.guild.name}** by {ctx.author.mention}!
You will stay muted till a moderator unmutes you!        
                ''')
            dmemb.set_footer(
                text=f"{self.bot.user.name}",
                icon_url=f"{self.bot.user.avatar_url}"
            )
            muteddm = await user.create_dm()
            await muteddm.send(embed=dmemb)
        except:
            pass

    @_mute.error
    async def _mute_error(self, ctx, error):
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
            await channel.set_permissions(discord.utils.get(channel.guild.roles, name="Muted"), send_messages=False,
                                          add_reactions=False)

    @commands.command(
        name="Unmute Command",
        description="A command to unmute a person.",
        usage="unmute <member>",
        aliases=[
            "unmute"
        ]
    )
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _unmute(self, ctx, user: discord.Member):

        if ctx.author.top_role.position <= user.top_role.position:
            await ctx.send("Lol you have unmute perms but you are not as powerful as the guy you are trying to unmute!")
            return

        if discord.utils.get(ctx.guild.roles, name="Muted") in user.roles:
            await user.remove_roles(
                discord.utils.get(ctx.guild.roles, name="Muted"))
            await ctx.send(f"Unmuted {user.mention}!")
            try:
                dmemb = discord.Embed(title="You were UNMUTED!", color=0x00ff00, description=f'''
            You were unmuted in **{ctx.guild.name}** by {ctx.author.mention}!   
                            ''')
                dmemb.set_footer(
                    text=f"{self.bot.user.name}",
                    icon_url=f"{self.bot.user.avatar_url}"
                )
                muteddm = await user.create_dm()
                await muteddm.send(embed=dmemb)
            except:
                pass
            return
        else:
            await ctx.send("There was an error while unmuting that user!")
            return

    @_unmute.error
    async def _unmute_error(self, ctx, error):
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

    # TempMute command
    @commands.command(
        name="TempMute Command",
        description="A command to temporarily mute a member.",
        usage="tempmute <member> <mutetime>",
        aliases=[
            "tempmute"
        ]
    )
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _tempmute(self, ctx, user: discord.Member, mutetime):

        if ctx.author.top_role.position <= user.top_role.position:
            await ctx.send("Lol you have temp mute perms but you are not as powerful as the guy you are trying to temp mute!")
            return

        if not discord.utils.get(ctx.guild.roles, name="Muted"):
            await ctx.send(
                f"Looks like there is no 'Muted' role! To make me create one, send `{self.bot.prefix(ctx.guild.id)}muterole` and I will create one for you!"
            )
            return

        if int(mutetime[:-1]) < 1:
            await ctx.send("Looks like the time to mute is too less. Try again!")
            return

        if not discord.utils.get(ctx.guild.roles, name="Muted") in user.roles:
            await user.add_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
        else:
            await ctx.send("He is already muted!")
            return

        if str(mutetime).endswith('s'):
            timeinsec = int(str(mutetime[:-1]))
            if mutetime[:-1] == 1:
                tester = 'second'
            else:
                tester = 'seconds'

        elif str(mutetime).endswith('m'):
            timeinsec = int(str(mutetime[:-1])) * 60
            if int(mutetime[:-1]) == 1:
                tester = 'minute'
            else:
                tester = 'minutes'

        elif str(mutetime).endswith('h'):
            timeinsec = int(str(mutetime[:-1])) * 60 * 60
            if int(mutetime[:-1]) == 1:
                tester = 'hour'
            else:
                tester = 'hours'

        elif str(mutetime).endswith('d'):
            timeinsec = int(str(mutetime[:-1])) * 60 * 60 * 24
            if int(mutetime[:-1]) == 1:
                tester = 'day'
            else:
                tester = 'days'

        elif str(mutetime).endswith('w'):
            timeinsec = int(str(mutetime[:-1])) * 60 * 60 * 24 * 7
            if int(mutetime[:-1]) == 1:
                tester = 'week'
            else:
                tester = 'weeks'

        else:
            await ctx.send("Check the time you sent me again!!")
            return

        timemsg = f'{mutetime[:-1]} {tester}'

        await ctx.send(f'''
      {user.mention} has been muted by {ctx.author.mention} for {timemsg}!
        ''')

        try:
            dmemb = discord.Embed(title="You were MUTED!", color=0x00ff00,description=f'''
    You were temporarily muted in **{ctx.guild.name}** by {ctx.author.mention} for {timemsg}!
            ''')
            dmemb.set_footer(
                text=f"{self.bot.user.name}",
                icon_url=f"{self.bot.user.avatar_url}"
            )
            muteddm = await user.create_dm()
            await muteddm.send(embed= dmemb)
        except:
            pass

        await asyncio.sleep(timeinsec)
        try:
            await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
        except:
            pass

    @_tempmute.error
    async def _tempmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Looks like you don't have enough permission to mute a person!")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Looks like you missed some arguments there buddy!!")
            return

        if isinstance(error, commands.BadArgument):
            await ctx.send("Looks like you gotta check the arguments you send me again!")
            return


def setup(bot):
    bot.add_cog(MuteUnmute(bot))
