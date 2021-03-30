import discord
from discord.ext import commands


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Help Command!
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx, cmd=None):
        if cmd == None:
            commandshelptext = '''
    **{0}help :** Displays this message.
    **{0}help miscellaneous :** To bring up the miscellaneous command's help menu!
    **{0}help modaction :** To bring up the server moderating command's help menu!
    **{0}help someperm :** To bring up commands which need some specific permissions to be ran! These are mainly mod-only commands.
          '''.format(self.bot.command_prefix)

            the_embed = discord.Embed(title="↓ Help Menu ↓",
                                      description=commandshelptext,
                                      color=0x03fc49)
            the_embed.set_author(name=ctx.message.author.name,
                                 icon_url=ctx.message.author.avatar_url)
            the_embed.set_footer(
                text="OwO",
                icon_url=self.bot.user.avatar_url)
            await ctx.message.channel.send(embed=the_embed)
            return

        elif cmd.lower() == 'modaction':
            modhelp = '''
    **{0}purge [number of messages] :** `Manage Messages`^. Used to purge some messages in bulk.

    **{0}nuke :** `Manage Channels`^. Used to nuke a channel!

    **{0}kick [user] [reason] :** `Kick Members`^. Kicks the mentioned person with the reason given. If no reason is given, then the default set reason is `None Given`.

    **{0}ban [user] [reason] :** `Ban Members`^. Bans the mentioned person with the reason given. If no reason is given, then the defailt set reason is `None Given`.

    **{0}unban [user id] [reason] :** `Ban Members`^. Unbans the mentioned person with the reason given. If no reason is given, then the defailt set reason is `None Given`.

    **{0}warn [user] [reason] :** `Kick Members`^. Warns the mentioned person with the given reason. In this, giving a reason is compulsury.

    **{0}warnings [user] :** Shows the warnings the mentioned person has received till now.

    ^ **Member should have the required permission to run the command!**
            '''.format(self.bot.command_prefix)
            the_embed = discord.Embed(title="↓ Moderation (Action) Commands Help Menu ↓",
                                      description=modhelp,
                                      color=0x00ff00)
            the_embed.set_author(name=ctx.message.author.name,
                                 icon_url=ctx.message.author.avatar_url)
            the_embed.set_footer(
                text="OwO",
                icon_url=self.bot.user.avatar_url)

            await ctx.send(embed=the_embed)
            return

        elif cmd.lower() in ['miscellaneous','misc']:
            misctext = '''
    **{0}svinfo :** Returns some basic info of the server in which the command is ran.
    
    **{0}avatar [mention/id] :** Returns the avatar/profile picture of the person tagged. You can also use the ID of the person. If you just type `{0}avatar`, it will return your profile picture/avatar!
    
    **{0}ping :** Returns the ping/latency of the bot!
    
    **{0}uptime :** To know the bot's uptime!
    
    **{0}joke :** Returns a joke.
    
    **{0}joke2 :** Returns a joke (This is a backup command with another api.)
    
    **{0}quote :** Returns a quote.
            '''.format(self.bot.command_prefix)

            the_embed = discord.Embed(title="↓ Miscellaneous Commands Help Menu ↓",
                                      description=misctext,
                                      color=0x00ff00)
            the_embed.set_author(name=ctx.message.author.name,
                                 icon_url=ctx.message.author.avatar_url)
            the_embed.set_footer(
                text="OwO",
                icon_url=self.bot.user.avatar_url)

            await ctx.send(embed=the_embed)
            return

        elif cmd.lower() == 'someperm':
            text = '''
    **{0}say [text] :** `Administrator`^. Bot says whatever you said in place of [text]. Also if you don't want to double ping anyone, use '{{@}}' instead of '@' as I will replace {{@}} with @!
    
    **{0}prefix [new prefix] :** `Administrator`^. To change prefix (Type 'reset' in place of [new prefix] to reset to default prefix '$')

    **{0}yesno [text] :** `Manage Messages`^. To make the bot send a message and react to it with green tick and red cross. Useful for polls.
    
    **{0}addyesno [message id] :** `Manage Messages`^. To add the yes/no reactions to a specific message. Useful for polls with media and with-ping messages to prevent double-pings.
    
    **{0}findmessage [message id] :** `Manage Messages`^. Finds and replies to the message, whose id is supplied!
    
    **{0}msgtime [message id] :** `Manage Messages`^. Returns the time at which the message was sent.
    
    **{0}rr or {0}reactrole [emoji] [role id or tag] [message id] :** `Manage Roles`^. Adds a reaction role to a message. \*BETA*
            
    ^ **Member should have the required permission to run the command!**
            '''.format(self.bot.command_prefix)

            the_embed = discord.Embed(title="↓ Moderation (Some Perms) Commands Help Menu ↓",
                                      description=text,
                                      color=0x00ff00)
            the_embed.set_author(name=ctx.message.author.name,
                                 icon_url=ctx.message.author.avatar_url)
            the_embed.set_footer(
                text="OwO",
                icon_url=self.bot.user.avatar_url)

            await ctx.send(embed=the_embed)
            return

        else:
            await ctx.send("Fool check the category name again!")
        return

def setup(bot):
    bot.add_cog(HelpCommand(bot))
