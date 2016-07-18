import discord
from discord.ext import commands
from .utils import checks
from __main__ import user_allowed, send_cmd_help
import os

class TybaltMegaserver:
    """TybaltMegaserver."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True, aliases=["NA"])
    async def na(self, ctx):
        """Join NA group/role

        Example:
        !na
        """
        author = ctx.message.author
        role_eu = self.get_role_by_name(ctx.message.server, "eu")
        role_uk = self.get_role_by_name(ctx.message.server, "uk")
        role_na = self.get_role_by_name(ctx.message.server, "na")
        try:
            if role_na not in author.roles :
                await self.bot.remove_roles(author, role_eu)
                await self.bot.remove_roles(author, role_uk)
                await self.bot.add_roles(author, role_na)
                await self.bot.say("Done ! You are now a NA player.")
            else :
                await self.bot.remove_roles(author, role_na)
                await self.bot.say("Well, you **were** a NA player.")
        except discord.Forbidden:
            await self.bot.say("I need permissions to edit roles first.")
        except Exception as e:
            print(e)
            await self.bot.say("Something went wrong.")

    @commands.command(pass_context=True, no_pm=True, aliases=["EU"])
    async def eu(self, ctx):
        """Join EU group/role

        Example:
        !eu
        """
        author = ctx.message.author
        role_eu = self.get_role_by_name(ctx.message.server, "eu")
        role_uk = self.get_role_by_name(ctx.message.server, "uk")
        role_na = self.get_role_by_name(ctx.message.server, "na")
        try:
            if role_uk in author.roles :
                await self.bot.say("Sorry, the borders are closed. Blame Brexit.")
            elif role_eu not in author.roles :
                await self.bot.remove_roles(author, role_uk)
                await self.bot.remove_roles(author, role_na)
                await self.bot.add_roles(author, role_eu)
                await self.bot.say("Done ! You are now a EU player.")
            else :
                await self.bot.remove_roles(author, role_eu)
                await self.bot.say("Well, you **were** a EU player.")
        except discord.Forbidden:
            await self.bot.say("I need permissions to edit roles first.")
        except Exception as e:
            print(e)
            await self.bot.say("Something went wrong.")

    @commands.command(pass_context=True, no_pm=True, aliases=["UK"])
    async def uk(self, ctx):
        """Join UK group/role

        Example:
        !uk
        """
        author = ctx.message.author
        role_eu = self.get_role_by_name(ctx.message.server, "eu")
        role_uk = self.get_role_by_name(ctx.message.server, "uk")
        role_na = self.get_role_by_name(ctx.message.server, "na")
        try:
            if role_uk not in author.roles :
                await self.bot.remove_roles(author, role_eu)
                await self.bot.remove_roles(author, role_na)
                await self.bot.add_roles(author, role_uk)
                await self.bot.say("Done ! You are now a UK player.")
            else :
                await self.bot.remove_roles(author, role_uk)
                await self.bot.say("Well, you **were** a UK player.")
        except discord.Forbidden:
            await self.bot.say("I need permissions to edit roles first.")
        except Exception as e:
            print(e)
            await self.bot.say("Something went wrong.")

    @commands.command(pass_context=True, no_pm=True)
    async def naisl(self, ctx):
        """Join NAISL group/role

        Example:
        !naisl
        """
        author = ctx.message.author
        role_eu = self.get_role_by_name(ctx.message.server, "eu")
        role_na = self.get_role_by_name(ctx.message.server, "na")
        try:
            await self.bot.remove_roles(author, role_eu)
            await self.bot.remove_roles(author, role_na)

            await self.bot.say("You just lost EU and NA role. Naisled it ! <@&167756221955178496>")
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
