import discord
import subprocess
from discord.ext import commands
from .utils.dataIO import fileIO
from .utils import checks
from __main__ import user_allowed, send_cmd_help
import os

class TybaltApi:
    """TybaltApi."""

    def __init__(self, bot):
        self.bot = bot
        self.api_paths = fileIO("data/tybalt/api.json", "load")

    @commands.command(pass_context=True, no_pm=True)
    async def skill(self, ctx, skill:str):
        """Describe a skill

        Example:
        !skill Fireball
        """
        path = self.api_paths['skill'];
        response = subprocess.check_output(["php", path, skill]);
        await self.bot.say(response.decode());

def setup(bot):
    n = TybaltApi(bot)
    bot.add_cog(n)