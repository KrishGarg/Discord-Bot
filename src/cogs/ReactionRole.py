import discord
from discord.ext import commands
import aiosqlite


class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.db: aiosqlite.Connection = bot.db

    @commands.command(
        name="ReactRole Command",
        description="A command to set-up reaction role on a message.",
        usage="rr <emoji> <role> <message_id>",
        aliases=[
            'rr',
            'reactrole'
        ]
    )
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _reactrole(self, ctx, emoji, role: discord.Role, messageid):
        msg = await ctx.channel.fetch_message(messageid)
        await msg.add_reaction(emoji)
        await self.db.execute("INSERT INTO reactrole VALUES (?,?,?,?,?)", (role.name, role.id, str(emoji), messageid, ctx.guild.id))
        await self.db.commit()

        await ctx.message.delete()

    @_reactrole.error
    async def _reactrole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have enough permissions to do that.")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"I think you missed some arguments. I know this is a complicated command so to check the correct syntax, run `{await self.bot.prefix(ctx.guild.id)}help moderation` !")
            return

        if isinstance(error, commands.BadArgument):
            await ctx.send("Yo check the arguments you sent me again!")
            return

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return

        cur = await self.db.execute("SELECT * FROM reactrole WHERE guild_id = ?", (payload.guild_id,))
        data = await cur.fetchall()

        if not data:
            return
        else:
            for x in data:
                if x[2] == str(payload.emoji) and int(x[3]) == payload.message_id:
                    role = discord.utils.get(self.bot.get_guild(
                        payload.guild_id).roles, id=x[1])
                    await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        cur = await self.db.execute("SELECT * FROM reactrole WHERE guild_id = ?", (payload.guild_id,))
        data = await cur.fetchall()

        if not data:
            return
        else:
            for x in data:
                if str(payload.emoji)[-1:] in x[2] and int(x[3]) == payload.message_id:
                    role = discord.utils.get(self.bot.get_guild(
                        payload.guild_id).roles, id=x[1])
                    await self.bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)


def setup(bot):
    bot.add_cog(ReactionRole(bot))
