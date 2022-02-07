import discord
from discord.ext import commands
from modules.messagelistener import MessageListener

bot_token = open('token.txt', 'r').read().strip()
client = commands.Bot(command_prefix=';', intents=discord.Intents.all())

client.add_cog(MessageListener(client))

client.run(bot_token)
