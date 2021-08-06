import discord
from discord.ext import commands
from colour import Color
from .custom_errors import *
import yarl


class NameToColorConverter(commands.Converter):
    """
    This converter is used to convert names of colors
    to discord.Colour type.
    It first uses the colour module to get the color
    object from the name, then we use its hex code to
    make the discord.Colour object.
    """
    async def convert(self, ctx, argument):
        try:
            c = Color(argument)
        except ValueError:
            raise NameToColorFail('Color given was not recognised.')
        else:
            '''
            Below system is there to convert 3 digit hexes,
            like #ff0 to #ffff00 so that we can easily
            convert this to 0xffff00 format and send that
            to discord.Colour function.
            '''
            temphex = '#'
            if len(c.hex) == 4:
                for digit in c.hex:
                    if digit == '#':
                        continue
                    temphex += digit+digit
            else:
                temphex = c.hex
            hex1 = temphex.replace('#', '0x')

            hexify = int(hex1, 16)
            try:
                x = discord.Color(hexify)
            except TypeError:
                raise NameToColorFail('Conversion to discord color failed.')
            return x


class EmojiURL:
    def __init__(self, *, animated, url):
        self.url = url
        self.animated = animated

    @classmethod
    async def convert(cls, ctx, argument):
        try:
            partial = await commands.PartialEmojiConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                url = yarl.URL(argument)
                if url.scheme not in ('http', 'https'):
                    raise RuntimeError
                path = url.path.lower()
                if not path.endswith(('.png', '.jpeg', '.jpg', '.gif')):
                    raise RuntimeError
                return cls(animated=url.path.endswith('.gif'), url=url)
            except Exception:
                raise commands.BadArgument(
                    'Not a valid or supported emoji URL.') from None
        else:
            return cls(animated=partial.animated, url=str(partial.url))
