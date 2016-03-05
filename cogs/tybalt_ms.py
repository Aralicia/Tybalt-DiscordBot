import discord
from discord.ext import commands
from .utils import checks
from __main__ import user_allowed, send_cmd_help
import os

class TybaltMegaserver:
    """TybaltMegaserver."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def na(self, ctx):
        """Join NA group/role

        Example:
        !na
        """
        author = ctx.message.author
        role_add = self.get_role_by_name(ctx.message.server, "na")
        role_remove = self.get_role_by_name(ctx.message.server, "eu")
        try:
            await self.bot.remove_roles(author, role_remove)
            await self.bot.add_roles(author, role_add)
            await self.bot.say("Done ! You are now a NA player.")
        except discord.Forbidden:
            await self.bot.say("I need permissions to edit roles first.")
        except Exception as e:
            print(e)
            await self.bot.say("Something went wrong.")

    @commands.command(pass_context=True, no_pm=True)
    async def eu(self, ctx):
        """Join EU group/role

        Example:
        !eu
        """
        author = ctx.message.author
        role_add = self.get_role_by_name(ctx.message.server, "eu")
        role_remove = self.get_role_by_name(ctx.message.server, "na")
        try:
            await self.bot.remove_roles(author, role_remove)
            await self.bot.add_roles(author, role_add)
            await self.bot.say("Done ! You are now a EU player.")
        except discord.Forbidden:
            await self.bot.say("I need permissions to edit roles first.")
        except Exception as e:
            print(e)
            await self.bot.say("Something went wrong.")

    def get_role_by_name(self, server, name):
        roles = server.roles
        for role in roles:
            if role.name.lower() == name.lower():
                return role


def setup(bot):
    n = TybaltMegaserver(bot)
    bot.add_cog(n)