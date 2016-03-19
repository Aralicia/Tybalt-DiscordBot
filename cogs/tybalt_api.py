import discord
import subprocess
from discord.ext import commands
from .utils.dataIO import fileIO
from .utils.tybalt import tybalt_call
from .utils import checks
from __main__ import user_allowed, send_cmd_help
import os

class TybaltApi:
    """TybaltApi."""

    def __init__(self, bot):
        self.bot = bot
        self.api_paths = fileIO("data/tybalt/api.json", "load")

    @commands.command(pass_context=True, no_pm=False)
    async def skill(self, ctx, *skill):
        """Describe a skill

        Example:
        !skill Fireball
        """
        path = self.api_paths['skill'];
        await tybalt_call(ctx, path, '!skill', *skill)

    @commands.command(pass_context=True, no_pm=False)
    async def trait(self, ctx, *trait):
        """Describe a trait

        Example:
        !trait Heal Resonator
        """
        path = self.api_paths['trait'];
        await tybalt_call(ctx, path, '!trait', *trait)

    @commands.command(pass_context=True, no_pm=True)
    async def item(self, ctx, *item):
        """Describe a item

        Example:
        !item Sword
        """
        path = self.api_paths['item'];
        response = subprocess.check_output(["php", path] + list(item));
        await self.bot.say(response.decode());

    @commands.command(pass_context=True, no_pm=True)
    async def recipe(self, ctx, *recipe):
        """Describe a recipe

        Example:
        !recipe wood
        """
        path = self.api_paths['recipe'];
        response = subprocess.check_output(["php", path] + list(recipe));
        await self.bot.say(response.decode());

    @commands.command(pass_context=True, no_pm=True)
    async def skin(self, ctx, *skin):
        """Describe a skin

        Example:
        !skin Heal Resonator
        """
        path = self.api_paths['skin'];
        response = subprocess.check_output(["php", path] + list(skin));
        await self.bot.say(response.decode());

    @commands.command(pass_context=True, no_pm=True)
    async def convert(self, ctx, *convert):
        """Show the content of the Chat Link

        Example:
        !convert [&BnMVAAA=]
        """
        path = self.api_paths['convert'];
        response = subprocess.check_output(["php", path] + list(convert));
        await self.bot.say(response.decode());

    @commands.command(pass_context=True, no_pm=True)
    async def spec(self, ctx, *spec):
        """Describe a specialization

        Example:
        !spec Explosives
        """
        path = self.api_paths['spec'];
        response = subprocess.check_output(["php", path] + list(spec));
        await self.bot.say(response.decode());        

def setup(bot):
    n = TybaltApi(bot)
    bot.add_cog(n)
