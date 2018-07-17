import discord
from random import randint
from random import choice
from discord.ext import commands
from .utils import checks
from __main__ import user_allowed, send_cmd_help
import os
import urllib.parse


class TybaltChars:
    """TybaltChars."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def newchar(self, *filters):
        """Create a new random charactee
        Example:
        !newchar
        """
        races_prefix = ["an", "a", "a", "a", "a"]
        races = ["Asura", "Charr", "Human", "Norn", "Sylvari"]
        classes = ["Elementalist", "Engineer", "Guardian", "Mesmer", "Necromancer", "Ranger", "Revenant", "Thief", "Warrior"]

        special = randint(1, 20)
        if (special == 20):
            races = ["Mice", "Kitty", "Bookah", "Big Bookah", "Salad"]
            classes = ["MightBot", "Pianist", "Lootsticker", "Pink Butterflies", "Edgelord", "Bearbow", "9th Wheel", "Vaultspammer", "HundredBlader"]

            
        new_race = randint(0, 4)
        if "heavy" in (filter.lower() for filter in filters) or "soldier" in (filter.lower() for filter in filters):
            new_class = choice([2, 6, 8])
        elif "medium" in (filter.lower() for filter in filters) or "adventurer" in (filter.lower() for filter in filters):
            new_class = choice([1, 5, 7])
        elif "light" in (filter.lower() for filter in filters) or "scholar" in (filter.lower() for filter in filters):
            new_class = choice([0, 3, 4])
        else:
            new_class = randint(0, 8)

        await self.bot.say('You should play '+races_prefix[new_race]+' '+races[new_race] + ' ' + classes[new_class] + '.')

def setup(bot):
    n = TybaltChars(bot)
    bot.add_cog(n)
