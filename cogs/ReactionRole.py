import discord
from discord.ext import commands
import json

class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['rr','reactrole'])
    @commands.has_permissions(manage_roles=True)
    async def _reactrole(self, ctx, emoji, role : discord.Role, messageid):
        msg = await ctx.channel.fetch_message(messageid)
        await msg.add_reaction(emoji)
        with open('cogs/reactrole.json') as json_file:
            data = json.load(json_file)
            new_react_role = {
                'role_name': role.name,
                'role_id': role.id,
                'emoji': emoji,
                'message_id': messageid
            }

            data.append(new_react_role)

        with open('cogs/reactrole.json', 'w') as f:
            json.dump(data, f)

        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return
        with open('cogs/reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name and int(x['message_id']) == payload.message_id:
                    role = discord.utils.get(self.bot.get_guild(payload.guild_id).roles, id=x['role_id'])
                    await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        with open('cogs/reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name and int(x['message_id']) == payload.message_id:
                    role = discord.utils.get(self.bot.get_guild(payload.guild_id).roles, id=x['role_id'])
                    await self.bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)

def setup(bot):
    bot.add_cog(ReactionRole(bot))