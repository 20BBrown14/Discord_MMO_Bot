#library imports
import discord
import time

#local imports
import config
# command imports
from commands import help, add_role, remove_role

client = discord.Client()
discordApiKey = config.bot_token

@client.event
async def on_ready():
    #info
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print(len(client.messages))

@client.event
async def on_message(message):
  #message log
  message_content = message.content.lower()
  response_channel = message.channel if message.channel.name else message.author
  if(message.author != client.user and message.channel.name):
    message_string = "%s said \"%s\" in [%s#%s] @ %s" % (message.author.name, message_content, message.server.name, message.channel.name, time.ctime())
    print(message_string)
  elif(message.author != client.user and not message.channel.name):
    message_string = "%s said \"%s\" [privately] @ %s" % (message.author.name, message.content, time.ctime())
    print(message_string)
  #Is the message a command
  if(message_content == help.TRIGGER):
    await help.command(client, message, response_channel)
  if(message_content.startswith(add_role.TRIGGER)):
    await add_role.command(client, message)
  if(message.content.startswith(remove_role.TRIGGER)):
    await remove_role.command(client, message)
  

client.run(discordApiKey)