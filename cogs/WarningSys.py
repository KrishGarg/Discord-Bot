import json

import discord
from discord.ext import commands

with open('cogs/reports.json', encoding='utf-8') as f:
    try:
        report = json.load(f)
    except ValueError:
        report = {}
        report['users'] = []


class WarningSys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Warn command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def warn(self, ctx, user: discord.Member, *reason: str):

        if ctx.author.top_role.position < user.top_role.position:
            await ctx.send("Lol you have warn perms but you are not as powerful as the guy you are trying to warn!")
            return

        try:
            if not reason:
                await ctx.send("Please provide a reason")
                return
            reason = ' '.join(reason)
            for current_user in report['users']:
                if current_user['name'] == user.name:
                    current_user['reasons'].append(reason)
                    break
            else:
                report['users'].append({
                    'name': user.name,
                    'reasons': [
                        reason,
                    ]
                })
            with open('cogs/reports.json', 'w+') as f:
                json.dump(report, f)
            await ctx.send(
                f"Warned Them! To check their warnings, use the `{self.bot.command_prefix}warnings` command."
            )
            warnydm = await user.create_dm()
            embe = discord.Embed(title="YOU HAVE BEEN WARNED!",
                                 color=0x00ff00,
                                 description=f'''
    You have been warned in **{ctx.guild.name}**!
    Reason Given: {reason}
    Warned By: {ctx.author.mention}
            ''')
            await warnydm.send(embed=embe)
        except:
            raise commands.CommandError()

    # Warn command error handling
    @warn.error
    async def warn_error(self, ctx, error):
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
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def warnings(self, ctx, user: discord.User):
        for current_user in report['users']:
            if user.name == current_user['name']:
                emb = discord.Embed(title=f"Warnings of {user.name}",
                                    color=0x00ff00,
                                    description=f'''
    **Number of Times Warned: ** {len(current_user['reasons'])}
    **Warning Reasons: ** 
    {"""

    """.join(current_user['reasons'])}
          ''')
                await ctx.send(embed=emb)
                break
        else:
            await ctx.send(f"{user.name} has never been reported!")

    # Warning command error handling
    @warnings.error
    async def warnings_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You missed some arguments looks like!")
            return


def setup(bot):
    bot.add_cog(WarningSys(bot))
