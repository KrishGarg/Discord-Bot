import discord
from discord.ext import commands


class KickBanUnban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Kick Command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def kick(self, ctx, user: discord.Member, reason1="None Given"):

        if ctx.author.top_role.position <= user.top_role.position:
            await ctx.send("Lol you have kick perms but you are not as powerful as the guy you are trying to kick!")
            return

        usersdm = await user.create_dm()
        dm_embed = discord.Embed(
            title="YOU HAVE BEEN KICKED!",
            description=f'''
    You have been kicked from **{ctx.guild.name}**.
    Reason: {reason1}
    Banned By: {ctx.author.mention}
    ''',
            color=0x00ff00)
        dm_embed.set_footer(
                text=f"{self.bot.user.name}",
                icon_url=f"{self.bot.user.avatar_url}"
            )
        await usersdm.send(embed=dm_embed)
        await user.kick(
            reason=
            f'{reason1} -Kicked By {ctx.author.name}#{ctx.author.discriminator}')
        await ctx.send(
            f"I kicked {user.mention} with the reason given as `{reason1}`")

    # Kick Error handling
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "You can't kick anyone. Get enough permissions first lol.")
            return

        if isinstance(error, commands.BadArgument):
            await ctx.send("Yo check the arguments you sent me again!")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You have to send me his ID too lol!")
            return

        if isinstance(error, commands.CommandError):
            await ctx.send("Some error occured try again later!")

    # Ban Command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ban(self, ctx, user: discord.Member, *, reason1="None Given"):

        if ctx.author.top_role.position <= user.top_role.position:
            await ctx.send("Lol you have ban perms but you are not as powerful as the guy you are trying to ban!")
            return

        usersdm = await user.create_dm()
        dm_embed = discord.Embed(
            title="YOU HAVE BEEN BANNED!",
            description=f'''
    You have been banned from **{ctx.guild.name}**.
    Reason: {reason1}
    Banned By: {ctx.author.mention}
    ''',
            color=0x00ff00)
        dm_embed.set_footer(
            text=f"{self.bot.user.name}",
            icon_url=f"{self.bot.user.avatar_url}"
        )
        await usersdm.send(embed=dm_embed)
        await user.ban(
            reason=
            f'{reason1} -Banned By {ctx.author.name}#{ctx.author.discriminator}')
        await ctx.send(
            f"I banned {user.mention} with the reason given as `{reason1}`")

    # Ban Command Error handling
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "You can't ban anyone. Get enough permissions first lol.")
            return

        if isinstance(error, commands.BadArgument):
            await ctx.send("Yo check the arguments you sent me again!")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You have to send me his ID too lol!")
            return

        if isinstance(error, commands.CommandError):
            await ctx.send("Some error occured try again later!")

    # Unban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def unban(self, ctx, user_id: int, *, reason1="None Given"):
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(
                user=user,
                reason=
                f'{reason1} -Unbanned by {ctx.author.name}#{ctx.author.discriminator}'
            )
            await ctx.send(
                f"I unbanned {user} with the reason given as `{reason1}`")
        except:
            raise commands.BadArgument()

    # Unban command error handling
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You can't do that. Get enough permission first lol!")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You have to send me his ID too lol!")
            return

        if isinstance(error, commands.BadArgument):
            await ctx.send(
                "There was some issue in unbanning that person. Maybe check the ID again!"
            )


def setup(bot):
    bot.add_cog(KickBanUnban(bot))
