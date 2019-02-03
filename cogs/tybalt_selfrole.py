import discord
from discord.ext import commands
from .utils import checks
from .utils.dataIO import dataIO
from __main__ import user_allowed, send_cmd_help, bot
import os

class TybaltSelfRole:
    """Tybalt Selfrole."""

    def __init__(self, bot):
        self.bot = bot
        self.file_path = "data/tybalt/selfrole.json"
        self.messages = dataIO.load_json(self.file_path)

    @checks.serverowner_or_permissions(administrator=True)
    @commands.command(pass_context=True, no_pm=True)
    async def selfrole(self, ctx):
        """Add selfrole message
        """

        title = "Give yourself your own roles"
        description = "To get one of the following roles, add the associated reaction to this message :\r\n\r\n"
        description += ":flag_us: NA role, for people playing on the NA Megaserver\r\n"
        description += ":flag_eu: EU role, for people playing on the EU Megaserver"
        em = discord.Embed(title=title, description=description, colour=0xF1C40F)

        message = await self.bot.send_message(ctx.message.channel, embed=em)
        self.messages.append(message.id)
        dataIO.save_json(self.file_path, self.messages)
        await self.bot.add_reaction(message, u"\U0001F1FA\U0001F1F8")
        await self.bot.add_reaction(message, u"\U0001F1EA\U0001F1FA")
        await self.bot.delete_message(ctx.message)

    @bot.event
    async def on_reaction_add(self, reaction, user):
        print("on reaction add")
        if reaction.message.id in self.messages and reaction.me == False:
            if reaction.custom_emoji == False:
                if reaction.emoji == u"\U0001F1FA\U0001F1F8":
                    self.add_role(user, reaction.message.server, "na")
                elif reaction.emoji == u"\U0001F1EA\U0001F1FA":
                    self.add_role(user, reaction.message.server, "eu")
    
    @bot.event
    async def on_reaction_remove(self, reaction, user):
        print("on reaction remove")
        if reaction.message.id in self.messages and reaction.me == False:
            if reaction.custom_emoji == False:
                if reaction.emoji == u"\U0001F1FA\U0001F1F8":
                    self.remove_role(user, reaction.message.server, "na")
                elif reaction.emoji == u"\U0001F1EA\U0001F1FA":
                    self.remove_role(user, reaction.message.server, "eu")


    def add_role(self, user, server, name):
        role = self.get_role_by_name(server, name)
        if (role is not None):
            self.bot.add_roles(user, [role])

    def remove_role(self, user, server, name):
        role = self.get_role_by_name(server, name)
        if (role is not None):
            self.bot.remove_roles(user, [role])

    def get_role_by_name(self, server, name):
        roles = server.roles
        for role in roles:
            if role.name.lower() == name.lower():
                return role
    
    def get_new_roles(self, roles, add, remove):
        new_roles = list(roles)
        for role in remove:
            if role in new_roles:
                new_roles.remove(role)
        for role in add:
            new_roles.append(role)
        return new_roles


def setup(bot):
    n = TybaltSelfRole(bot)
    bot.add_cog(n)
