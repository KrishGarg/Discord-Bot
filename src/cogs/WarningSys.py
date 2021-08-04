import discord
from discord.ext import commands

class WarningSys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    # Warn command
    @commands.command(
        name="Warn Command",
        description="A command to warn a member.",
        usage="warn <member> [reason]",
        aliases=[
            "warn"
        ]
    )
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _warn(self, ctx, user: discord.Member, *, reason: str):

        if ctx.author.top_role.position <= user.top_role.position:
            await ctx.send("Lol you have warn perms but you are not as powerful as the guy you are trying to warn!")
            return

        try:
            if not reason:
                await ctx.send("Please provide a reason")
                return

            await self.db.execute("INSERT INTO warnings (user_id,reason,guild_id) VALUES (?,?,?)", (user.id, reason, ctx.guild.id))
            await self.db.commit()

            await ctx.send(
                f"Warned Them! To check their warnings, use the `{await self.bot.prefix(ctx.guild.id)}warnings` command."
            )

            try:
                warnydm = await user.create_dm()
                embe = discord.Embed(title="YOU HAVE BEEN WARNED!",
                                     color=0x00ff00,
                                     description=f'''
        You have been warned in **{ctx.guild.name}**!
        Reason Given: {reason}
        Warned By: {ctx.author.mention}
                ''')
                embe.set_footer(
                    text=f"{self.bot.user.name}",
                    icon_url=f"{self.bot.user.avatar_url}"
                )
                await warnydm.send(embed=embe)
            except discord.Forbidden:
                await ctx.send("By the way, their DMs are closed/ I can't send a DM to them so they might not know that they have been warned!")

        except:
            raise commands.CommandError()

    # Warn command error handling
    @_warn.error
    async def _warn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(
                ctx.message.author)
            await ctx.send(ctx.message.channel, text)
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

    # Warnings command
    @commands.command(
        name="Warnings Command",
        description="A command to see the warnings of a member.",
        usage="warnings <member>",
        aliases=[
            "warnings"
        ]
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _warnings(self, ctx, user: discord.User):
        cur = await self.db.execute("SELECT * FROM warnings WHERE user_id = ? AND guild_id = ?", (user.id, ctx.guild.id))
        user_reports = await cur.fetchall()

        if not user_reports:
            return await ctx.send(f"{user.name} has never been reported!")

        else:
            reasons = [x[1] for x in user_reports]
            reasonstr = "\n\n".join(reasons)

            emb = discord.Embed(title=f"Warnings of {user.name}",
                                color=0x00ff00,
                                description=f'''
                **Number of Times Warned: ** {len(user_reports)}
                **Warning Reasons: **
                {reasonstr}
                      ''')
            emb.set_footer(
                text=f"{self.bot.user.name}",
                icon_url=f"{self.bot.user.avatar_url}"
            )
            await ctx.send(embed=emb)

    # Warning command error handling
    @_warnings.error
    async def _warnings_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You missed some arguments looks like!")
            return


def setup(bot):
    bot.add_cog(WarningSys(bot))
