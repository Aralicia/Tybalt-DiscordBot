import discord
import subprocess
import json
from discord.ext import commands
from .utils.dataIO import fileIO
from .utils import checks
from __main__ import user_allowed, send_cmd_help
import os

class TybaltGroup:
    """TybaltGroup."""

    def __init__(self, bot):
        self.bot = bot
        self.group_paths = fileIO("data/tybalt/groups.json", "load")

    @commands.command(pass_context=True, no_pm=True)
    async def test(self, ctx, *test):
        """test command
        """
        path = self.group_paths['test'];
        
        args = json.dumps({'author': {
            'name' : ctx.message.author.name,
            'id' : ctx.message.author.id,
        }, 'args':test})
        response = subprocess.check_output(["php", path, args]);
        data = json.loads(response.decode());
        if data.pmTo > 1:
            for pm in data.pmTo:
                await self.bot.send_message(pm, data.print);
        else:        
            await self.bot.say(data.print);

def setup(bot):
    n = TybaltGroup(bot)
    bot.add_cog(n)
