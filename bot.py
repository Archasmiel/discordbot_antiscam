from discord.ext import commands
from modules.messagelistener import MessageListener

bot_token = open('token.txt', 'r').readline().strip()
client = commands.Bot(command_prefix=';')

client.add_cog(MessageListener(client))

client.run(bot_token)
