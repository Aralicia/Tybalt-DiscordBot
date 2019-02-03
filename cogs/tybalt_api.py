import discord
import subprocess
from discord.ext import commands
from discord.utils import get
from itertools import islice
from .utils.dataIO import fileIO
from .utils.tybalt import tybalt_call
from .utils import checks
from .tybalt.database import database
from .tybalt.gw2api import gw2api
from .tybalt.gw2embed import gw2embed
from .tybalt.gw2entities import gw2entities, EntityType
from .tybalt.tabmessage import tabmessages, TabMessage
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

    @commands.command(pass_context=True, no_pm=False)
    async def item(self, ctx, *data):
        """Describe a item

        Example:
        !item Sword
        """
        name = " ".join(data)

        message = TabMessage()
        embeds = []

        if name.isdigit():
            items = gw2entities.findById(name, EntityType.item())
        else:
            items = gw2entities.findByName(name, EntityType.item(), 9+25)

        if items[1] == 0:
            await self.bot.send_message(ctx.message.channel, "I've not found anything, sorry.")
        elif items[1] == 1:
            embed = await gw2embed.item(self.bot, items[0][0]['id'], None, ctx.message.server.emojis)
            await self.bot.send_message(ctx.message.channel, embed=embed)
        else:
            for idx, item in enumerate(islice(items[0], 9), start=1):
                embed = await gw2embed.item(self.bot, item['id'], None, ctx.message.server.emojis)
                message.addTab(embed, str(idx) + u"\u20E3")

            if items[1] > 9:
                extracount = items[1] - (9+25)
                if extracount < 0:
                    extracount = 0
                embed = await gw2embed.entityList(items[0][9:], extracount)
                message.addTab(embed, u"\U0001F4C4")

            await tabmessages.send(self.bot, message, ctx.message.channel)


    @commands.command(pass_context=True, no_pm=False)
    async def item_old(self, ctx, *item):
        """Describe a item

        Example:
        !item Sword
        """
        path = self.api_paths['item'];
        await tybalt_call(ctx, path, '!item', *item)

    @commands.command(pass_context=True, no_pm=False)
    async def recipe(self, ctx, *recipe):
        """Describe a recipe

        Example:
        !recipe wood
        """
        path = self.api_paths['recipe'];
        response = subprocess.check_output(["php", path] + list(recipe));
        await self.bot.say(response.decode());

    @commands.command(pass_context=True, no_pm=False)
    async def skin(self, ctx, *skin):
        """Describe a skin

        Example:
        !skin Heal Resonator
        """
        path = self.api_paths['skin'];
        response = subprocess.check_output(["php", path] + list(skin));
        await self.bot.say(response.decode());

    @commands.command(pass_context=True, no_pm=False)
    async def convert(self, ctx, *convert):
        """Show the content of the Chat Link

        Example:
        !convert [&BnMVAAA=]
        """
        path = self.api_paths['convert'];
        response = subprocess.check_output(["php", path] + list(convert));
        await self.bot.say(response.decode());

    @commands.command(pass_context=True, no_pm=False)
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
