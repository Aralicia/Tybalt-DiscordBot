import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from .utils import checks
from __main__ import user_allowed, send_cmd_help
import os
import random

class CustomCommands:
    """Custom commands."""

    def __init__(self, bot):
        self.bot = bot
        self.c_commands = fileIO("data/customcom/commands.json", "load")

    @commands.command(pass_context=True, no_pm=True)
    #@checks.mod_or_permissions(administrator=True)
    async def addcom(self, ctx, command : str, *, text):
        """Adds a custom command

        Example:
        !addcom yourcommand Text you want
        """
        server = ctx.message.server
        user = ctx.message.author
        username = '<@'+user.id+'>'
        command = command.lower()
        if command in self.bot.commands.keys():
            await self.bot.say("That command is already a standard command.")
            return
        if not server.id in self.c_commands:
            self.c_commands[server.id] = {}
        cmdlist = self.c_commands[server.id]
        if command not in cmdlist:
            cmdlist[command] = text
            self.c_commands[server.id] = cmdlist
            fileIO("data/customcom/commands.json", "save", self.c_commands)
            await self.bot.say("{} Custom command '{}' successfully added.".format(username, command))
        else:
            await self.bot.say("{} This command already exists. Use editcom to edit it.".format(username))

    @commands.command(pass_context=True, no_pm=True)
    #@checks.mod_or_permissions(administrator=True)
    async def editcom(self, ctx, command : str, *, text):
        """Edits a custom command

        Example:
        !editcom yourcommand Text you want
        """
        server = ctx.message.server
        user = ctx.message.author
        username = '<@'+user.id+'>'
        command = command.lower()
        if server.id in self.c_commands:
            cmdlist = self.c_commands[server.id]
            if command in cmdlist:
                cmdlist[command] = text
                self.c_commands[server.id] = cmdlist
                fileIO("data/customcom/commands.json", "save", self.c_commands)
                await self.bot.say("{} Custom command '{}' successfully edited.".format(username, command))
            else:
                await self.bot.say("{} That command doesn't exist. Use addcom [command] [text]".format(username))
        else:
             await self.bot.say("{} There are no custom commands in this server. Use addcom [command] [text]".format(username))

    @commands.command(pass_context=True, no_pm=True)
    #@checks.mod_or_permissions(administrator=True)
    async def delcom(self, ctx, command : str):
        """Deletes a custom command

        Example:
        !delcom yourcommand"""
        server = ctx.message.server
        user = ctx.message.author
        username = '<@'+user.id+'>'
        command = command.lower()
        if server.id in self.c_commands:
            cmdlist = self.c_commands[server.id]
            if command in cmdlist:
                cmdlist.pop(command, None)
                self.c_commands[server.id] = cmdlist
                fileIO("data/customcom/commands.json", "save", self.c_commands)
                await self.bot.say("{} Custom command '{}' successfully deleted.".format(username, command))
            else:
                await self.bot.say("{} That command doesn't exist.".format(username))
        else:
            await self.bot.say("{} There are no custom commands in this server. Use addcom [command] [text]".format(username))

    @commands.command(pass_context=True, no_pm=True, aliases=["customcom"])
    async def customcommands(self, ctx):
        """Shows custom commands list"""
        server = ctx.message.server
        user = ctx.message.author
        if server.id in self.c_commands:
            cmdlist = self.c_commands[server.id]
            if cmdlist:
                i = 0
                msg = ["```Custom commands:\n"]
                for cmd in sorted([cmd for cmd in cmdlist.keys()]):
                    if len(msg[i]) + len(ctx.prefix) + len(cmd) + 5 > 2000:
                        msg[i] += "```"
                        i += 1
                        msg.append("``` {}{}\n".format(ctx.prefix, cmd))
                    else:
                        msg[i] += " {}{}\n".format(ctx.prefix, cmd)
                msg[i] += "```"
                for cmds in msg:
                    await self.bot.whisper(cmds)
            else:
                await self.bot.say("There are no custom commands in this server. Use addcom [command] [text]")
        else:
            await self.bot.say("There are no custom commands in this server. Use addcom [command] [text]")

    @commands.command(pass_context=True, no_pm=True)
    async def randcom(self, ctx):
        """execute a random custom command"""
        server = ctx.message.server
        user = ctx.message.author
        username = '<@'+user.id+'>'
        if server.id in self.c_commands:
            cmdlist = self.c_commands[server.id]
            if cmdlist:
                msg = random.choice(list(cmdlist));
                await self.bot.send_message(ctx.message.channel, '{} !{} \n{}'.format(username, msg, cmdlist[msg]))

    async def checkCC(self, message):
        if message.author.id == self.bot.user.id or len(message.content) < 2 or message.channel.is_private:
            return

        if not user_allowed(message):
            return

        msg = message.content
        server = message.server
        user = message.author
        username = '<@'+user.id+'>'
        prefix = self.get_prefix(msg)

        if prefix and server.id in self.c_commands.keys():
            cmdlist = self.c_commands[server.id]
            cmd = msg[len(prefix):]
            if cmd in cmdlist.keys():
                await self.bot.send_message(message.channel, '{} {}'.format(username, cmdlist[cmd]))
            elif cmd.lower() in cmdlist.keys():
                await self.bot.send_message(message.channel, '{} {}'.format(username, cmdlist[cmd.lower()]))

    def get_prefix(self, msg):
        for p in self.bot.command_prefix:
            if msg.startswith(p):
                return p
        return False

def check_folders():
    if not os.path.exists("data/customcom"):
        print("Creating data/customcom folder...")
        os.makedirs("data/customcom")

def check_files():
    f = "data/customcom/commands.json"
    if not fileIO(f, "check"):
        print("Creating empty commands.json...")
        fileIO(f, "save", {})

def setup(bot):
    check_folders()
    check_files()
    n = CustomCommands(bot)
    bot.add_listener(n.checkCC, "on_message")
    bot.add_cog(n)
