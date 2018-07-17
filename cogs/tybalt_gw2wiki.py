import discord
from discord.ext import commands
from .utils import checks
from __main__ import user_allowed, send_cmd_help
import os
import urllib.parse
import aiohttp
import json


class TybaltWiki:
    """TybaltWiki."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def wiki(self, ctx, *search):
        """Search on the Guild Wars 2 wiki
        Example:
        !wiki "Game Updates"
        """

        try:
            await self.bot.type()

            msg = " ".join(search)
            f = { 'search' : msg}

            # uses the wiki API to do a real search. Links for articles are posted if there is any
            url = "https://wiki.guildwars2.com/api.php?action=opensearch&"+urllib.parse.urlencode(f)

            async with aiohttp.get(url, headers={}) as r:
                data = await r.text()
                status = r.status

            try:
                parsed = json.loads(data)
            except:
                parsed = json.loads('{}')

            res = ""

            if len(parsed[3]) > 0:
                for a in parsed[3]:
                    res = "{}\n<{}>".format(res,a)

                res = "Ok, I have found these results for \"{}\":\n{}".format(msg,res)
                await self.bot.say("{}".format(res))
  
            else:
                await self.bot.say("Hmm, nothing was found for \"{}\".".format(msg))

        except Exception as e:
            print(e)
            await self.bot.say("Something went wrong.")

def setup(bot):
    n = TybaltWiki(bot)
    bot.add_cog(n)
