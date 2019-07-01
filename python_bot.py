#library imports
import discord
import time
import json
from fuzzywuzzy import fuzz

#local imports
import config
# command imports
from commands import help, add_role, remove_role, lfg, list_roles, pizza, weather, raid, tradeskilladd, tradeskill, tradeskillremove, leave_server
from rules import lfg_channel_clean

client = discord.Client()
discordApiKey = config.bot_token
weather_api_key = config.weather_api_key

command_array = [help.TRIGGER, add_role.TRIGGER, remove_role.TRIGGER, lfg.TRIGGER, list_roles.TRIGGER,
                  pizza.TRIGGER, weather.TRIGGER, raid.TRIGGER, tradeskilladd.TRIGGER, tradeskill.TRIGGER,
                  tradeskillremove.TRIGGER, leave_server.TRIGGER]

version = '2019-07-01_1'

global lfg_table
global lfg_message
global weather_cache
global raid_info
global tradeskill_information

async def unrecognized_command(bad_string, message):
  print('unrecognized command')
  space_index = bad_string.strip().find(' ')
  if(space_index == -1):
    bad_command = bad_string.strip()
  elif(space_index > 0):
    bad_command = bad_string.strip()[:space_index].lower()
  potential_commands = []
  for command in command_array:
    ratio = fuzz.ratio(bad_command, command.lower())
    if(ratio >= 75):
      potential_commands.append(command)
  if(len(potential_commands) > 0):
    await client.send_message(message.author, "Unrecognized command `%s`. Did you mean one of the following: `%s`\nUse `!help` for a list of all commands." % (bad_string, (', '.join(potential_commands))))
    return
    # fuzzy compare
  await client.send_message(message.author, "Unrecognized command `%s`. Use `!help` to list available commands." % bad_string)

async def delete_message(client, message):
  try:
    client.get_message(message.channel, message.id)
    if(message.channel.name):
      if(not message.channel.name.lower() == 'bot_commands'):
        await client.delete_message(message)
  except:
    print('Message DNE')

@client.event
async def on_ready():
  global lfg_table
  global lfg_message
  global weather_cache
  global raid_info
  global tradeskill_information
  lfg_table = []
  lfg_message = None
  weather_cache = json.loads('{}')
  raid_info = json.loads('{}')
  tradeskill_information = json.loads('{}')
  client_game = discord.Game(name='(v%s) say !help' % version)
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
  global weather_cache
  global raid_info
  global tradeskill_information
  message_content = message.content.lower()
  space_index = message_content.find(' ')
  command_string = ''
  if(space_index > 0):
    command_string = message_content[:space_index].strip()
  else:
    command_string = message_content
  response_channel = message.channel if message.channel.name else message.author
  if(message.author != client.user and message.channel.name):
    message_string = "%s said \"%s\" in [%s#%s] @ %s" % (message.author.name, message_content, message.server.name, message.channel.name, time.ctime())
    print(message_string)
  elif(message.author != client.user and not message.channel.name):
    message_string = "%s said \"%s\" [privately] @ %s" % (message.author.name, message.content, time.ctime())
    print(message_string)
  #Apply any rules to the message
  if(lfg_channel_clean.APPLIES(client, message)):
    await lfg_channel_clean.rule(client, message, delete_message)
  #Is the message a command
  if(command_string == help.TRIGGER):
    await help.command(client, message, response_channel, delete_message)
  elif(command_string == (add_role.TRIGGER)):
    await add_role.command(client, message, delete_message)
  elif(command_string == (remove_role.TRIGGER)):
    await remove_role.command(client, message, delete_message)
  elif(command_string == (lfg.TRIGGER)):
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
  elif(command_string == (list_roles.TRIGGER)):
    await list_roles.command(client, message, response_channel, delete_message)
  elif(command_string == (pizza.TRIGGER)):
    await pizza.command(client, message, response_channel)
  elif(command_string == (weather.TRIGGER)):
    weather_cache = await weather.command(client, message, response_channel, delete_message, weather_cache, weather_api_key)
  elif(command_string == raid.TRIGGER):
    raid_info = await raid.command(client, message, response_channel, delete_message, raid_info)
  elif(command_string == tradeskilladd.TRIGGER):
    tradeskill_information = await tradeskilladd.command(client, message, response_channel, delete_message, tradeskill_information)
  elif(command_string == tradeskill.TRIGGER):
    await tradeskill.command(client, message, response_channel, delete_message, tradeskill_information)
  elif(command_string == tradeskillremove.TRIGGER):
    tradeskill_information = await tradeskillremove.command(client, message, response_channel, delete_message, tradeskill_information)
  elif(command_string == leave_server.TRIGGER):
    await leave_server.command(client, message, response_channel, delete_message)
  elif(command_string.startswith('!')): #Unrecognized command
    await delete_message(client, message)
    await unrecognized_command(message_content, message)
  

client.run(discordApiKey)
