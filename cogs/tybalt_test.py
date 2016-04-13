import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from .utils import checks
from .utils.tybalt import tybalt_call
from __main__ import user_allowed, send_cmd_help
import os

class TybaltTest:
    """TybaltTest."""

    def __init__(self, bot):
        self.bot = bot
        self.group_paths = fileIO("data/tybalt/test.json", "load")

    @commands.command(pass_context=True, no_pm=False)
    async def test(self, ctx, *data):
        """test dev command
        """
        path = self.group_paths['test']
        await tybalt_call(ctx, path, '!item', *data)

def setup(bot):
    n = TybaltTest(bot)
    bot.add_cog(n)
