import discord
import subprocess
import json
from discord.ext import commands
import os

async def tybalt_call(ctx, path, cmd, *data):
    datalist = list(data)
    datalist.insert(0, '!skill')
    args = json.dumps({'author': {
        'name' : ctx.message.author.name,
        'id' : ctx.message.author.id,
    }, 'commandline' : datalist})
    response = subprocess.check_output(["php", path, args])
    data = json.loads(response.decode());
    if len(data['message']) > 0:
        for msg in data['message']:
            await ctx.bot.say(msg)
    if len(data['private']) > 0:
        members = ctx.bot.get_all_members();
        for msg in data['private']:
            for member in members:
                if msg['receiver'] == member.id :
                    await ctx.bot.send_message(member, msg['message'])

