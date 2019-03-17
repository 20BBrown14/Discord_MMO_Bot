#library imports
import discord
import time

#local imports
import config
# command imports
from commands import help, add_role, remove_role, lfg, list_roles

client = discord.Client()
discordApiKey = config.bot_token

global lfg_table
global lfg_message

async def delete_message(client, message):
  if(message.channel.name):
    if(not message.channel.name.lower() == 'bot_commands'):
      await client.delete_message(message)

@client.event
async def on_ready():
  global lfg_table
  global lfg_message
  lfg_table = []
  lfg_message = None
  client_game = discord.Game(name='say !help')
  await client.change_status(game = client_game)
  #info
  print('Logged in as')
  print(client.user.name)
  print(client.user.id)
  print('------')
  print(len(client.messages))

@client.event
async def on_message(message):
  #message log
  global lfg_table
  global lfg_message
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
    await help.command(client, message, response_channel, delete_message)
  if(message_content.startswith(add_role.TRIGGER)):
    await add_role.command(client, message, delete_message)
  elif(message_content.startswith(remove_role.TRIGGER)):
    await remove_role.command(client, message, delete_message)
  elif(message_content.startswith(lfg.TRIGGER)):
    lfg_channel = None #refactor this out
    for channel in message.server.channels:
      if channel.name.lower() == 'lfg':
        lfg_channel = channel
        break
    if(not lfg_channel == None):
      lfg_table, lfg_message = await lfg.command(client, message, lfg_channel, lfg_table, lfg_message, delete_message)
    else:
      await delete_message(client, message)
      await client.send_message(message.author, 'This server does not have an lfg channel')
  elif(message_content == (list_roles.TRIGGER)):
    await list_roles.command(client, message, response_channel, delete_message)
  elif(message_content.startswith('!')):
    await delete_message(client, message)
    await client.send_message(message.author, "Unrecognized command `%s`. Use `!help` to list available commands." % message_content)
  

client.run(discordApiKey)