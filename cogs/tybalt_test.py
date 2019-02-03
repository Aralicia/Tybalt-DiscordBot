import discord
from discord.ext import commands
from discord.utils import get
from itertools import islice
from .utils.dataIO import fileIO
from .utils import checks
from .utils.tybalt import tybalt_call
from .tybalt.database import database
from .tybalt.gw2api import gw2api
from .tybalt.gw2embed import gw2embed
from .tybalt.gw2entities import gw2entities, EntityType
from .tybalt.tabmessage import tabmessages, TabMessage
from __main__ import user_allowed, send_cmd_help
import os

class TybaltTest:
    """TybaltTest."""
    

    def __init__(self, bot):
        self.bot = bot
        self.group_paths = fileIO("data/tybalt/test.json", "load")

    @commands.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def test(self, ctx, *data):
        """test dev command
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
        # U+1F4C4
        #await self.bot.send_message(ctx.message.channel, embed=embeds[0])

        #cursor = database.get_cursor()
        #query = ("SELECT api_id, name FROM entity WHERE type = %s ORDER BY RAND() LIMIT 1")
        #cursor.execute(query, ("item",))
        #for (api_id, name) in cursor:
        #    print(api_id)
        #    data = await gw2api.call('{}/{}'.format('items', api_id))
        #    await self.bot.say(data)

        #path = self.group_paths['test']
        #await tybalt_call(ctx, path, '!item', *data)
    

def setup(bot):
    n = TybaltTest(bot)
    bot.add_cog(n)
