from discord.ext import commands


class WelcomeLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['welcomechannel', 'welcch'])
    @commands.has_permissions(administrator=True)
    async def _welcomechannel(self, ctx):
        if self.bot._welcomemessagesenabled == False:
            self.bot._welcomemessagesenabled = True
            await ctx.send("Welcome messages has been enabled in the current channel.")
            self.bot._welcmsgch = ctx.channel.id
        else:
            self.bot._welcomemessagesenabled = False
            await ctx.send("Welcome messages has been disabled.")
            self.bot._welcmsgch = 0

    @_welcomechannel.error
    async def _welcomechannel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have enough permission to do so.")
            return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.bot._welcmsgch == 0:
            pass
        else:
            channel = self.bot.get_channel(self.bot._welcmsgch)
            await channel.send(f"Welcome {member.mention}! Enjoy your stay with us in **{member.guild.name}**.")

    @commands.command(aliases=['leavechannel', 'leavech'])
    @commands.has_permissions(administrator=True)
    async def _leavechannel(self, ctx):
        if self.bot._leavemessagesenabled == False:
            self.bot._leavemessagesenabled = True
            await ctx.send("Leave messages has been enabled in the current channel.")
            self.bot._leavemsgch = ctx.channel.id
        else:
            self.bot._leavemessagesenabled = False
            await ctx.send("Leave messages has been disabled.")
            self.bot._leavemsgch = 0

    @_leavechannel.error
    async def _leavechannel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have enough permission to do so.")
            return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if self.bot._leavemsgch == 0:
            pass
        else:
            channel = self.bot.get_channel(self.bot._welcmsgch)
            await channel.send(f"{member.mention} has left us! Hope they come back!")


def setup(bot):
    bot.add_cog(WelcomeLeave(bot))
