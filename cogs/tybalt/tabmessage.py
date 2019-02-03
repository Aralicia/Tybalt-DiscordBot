import discord
from __main__ import bot

class TabMessage:
    def __init__(self):
        self.tabs = []
        self.client = None
        self.channel = None
        self.message = None

    def addTab(self, page, emoji):
        self.tabs.append({'page':page, 'emoji':emoji})

    def setClient(self, client):
        self.client = client

    def setChannel(self, channel):
        self.channel = channel

    async def send(self):
        if len(self.tabs) > 0 and self.client is not None and self.channel is not None:
            firstpage = self.tabs[0]['page']
            if isinstance(firstpage, discord.Embed):
                self.message = await self.client.send_message(self.channel, embed=firstpage)
            else:
                self.message = await self.client.send_message(self.channel, firstpage)
            for tab in self.tabs:
                await self.client.add_reaction(self.message, tab['emoji'])
            return self.message.id
        return None
    
    async def handleReaction(self, reaction, user):
        if (user.bot == False):
            for tab in self.tabs:
                if reaction.emoji == tab['emoji']:
                    if isinstance(tab['page'], discord.Embed):
                        await self.client.edit_message(reaction.message, embed=tab['page'])
                    else:
                        await self.client.edit_message(reaction.message, new_content=tab['page'])
        if (reaction.me == False):
            await self.client.remove_reaction(reaction.message, reaction.emoji, reaction, user)



class TabMessages:
    def __init__(self):
        self.messages = {}

    async def send(self, client, message, channel):
        message.setClient(client)
        message.setChannel(channel)
        result = await message.send()
        if result is not None:
            self.messages[result] = message

    @bot.event
    async def on_reaction_add(reaction, user):
        if reaction.message.id in tabmessages.messages:
            await tabmessages.messages[reaction.message.id].handleReaction(reaction, user)

tabmessages = TabMessages()

