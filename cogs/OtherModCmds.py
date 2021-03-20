import discord
from discord.ext import commands
from time import sleep

class OtherModCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Find Message Command
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def findmessage(self, ctx, id1: int):
        try:
            the_msg = await ctx.channel.fetch_message(id1)
            await the_msg.reply(content="Gotcha!")
        except:
            raise commands.BadArgument()

    # Find message error handling
    @findmessage.error
    async def findmessage_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the required permission!")
            return
        if isinstance(error, commands.BadArgument):
            await ctx.send("There was some issue with the id you sent!")
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Yo! You have to send me the id too!")
            return

    # Yes No Command!
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def yesno(self, ctx, *, text: str):
        channel = ctx.channel
        await ctx.message.delete()
        sent = await channel.send(text)
        await sent.add_reaction("<a:tick:809071236549443634>")
        await sent.add_reaction("<a:cross2:809071453059153972>")
        return

    # Error handling for yes no comamnd
    @yesno.error
    async def yesno_error(self, ctx, error):
        # If user got no permission, then it sends this.
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the permission to do so!")
            return

        # If used didn't send the text, then it sends this
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Yo you forgot the text!")

    # Add yes no command!
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def addyesno(self, ctx, the_id):
        msgid = the_id
        themsg = await ctx.fetch_message(int(msgid))
        await ctx.message.delete()
        await themsg.add_reaction("<a:tick:809071236549443634>")
        await themsg.add_reaction("<a:cross2:809071453059153972>")
        msg2 = await ctx.send("Added!")
        sleep(3)
        await msg2.delete()
        return

    # Error handling for Add yes no command
    @addyesno.error
    async def addyesno_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have enough permission to do so!")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You have to attach the id of the message too!")
            return

        if isinstance(error, commands.CommandError):
            await ctx.send("Some error occured! Try again later.")
            return

    # Prefix changer
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def prefix(self, ctx, prefixnew):
        # This and below function for changing prefixes
        def change_prefix(newprefix):
            self.bot.command_prefix = newprefix
        if prefixnew != "reset":
            change_prefix(prefixnew)
        # to reset to default prefix
        elif prefixnew == "reset":
            change_prefix("$")

        messagetosend = f"I just changed my prefix to `{self.bot.command_prefix}`"
        await ctx.send(messagetosend)
        return

    # Prefix changer error handling
    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'The prefix is `{self.bot.command_prefix}` !')
            return

        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "Noob you can't change the prefix and if you wanna know the prefix, ping me!"
            )
            return

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def msgtime(self, ctx, id1: int):
        await ctx.send(f"Time (in UTC) is: {discord.utils.snowflake_time(id1)}")
        return

    @msgtime.error
    async def msgtime_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("First get enough permissions lol!")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to send me the ID too!")
            return

        if isinstance(error, commands.BadArgument):
            await ctx.send("You check the ID again!")
            return

    # Say command
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def say(self, ctx, *, text: str):
        x = text
        if "{@}" in text:
            x = text.replace("{@}", "@")
        await ctx.send(x)
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(OtherModCmds(bot))