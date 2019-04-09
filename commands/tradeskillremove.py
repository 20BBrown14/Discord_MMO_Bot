# tradeskillremove.py

import json
from fuzzywuzzy import fuzz
import os
#!tradeskilladd someName, level, class, notes
#!tradeskilladd help

tradeskills = ['carpenter', 'provisioner', 'woodworker', 'weaponsmith', 'armorer', 'tailor', 'alchemist', 'jeweler', 'sage', 'tinkerer', 'adorner']

async def unrecognized_tradeskill(client, bad_string, message):
  space_index = bad_string.strip().find(' ')
  if(space_index == -1):
    bad_name = bad_string.strip()
  elif(space_index > 0):
    bad_name = bad_string.strip()[:space_index].lower()
  potential_names = []
  for name in tradeskills:
    ratio = fuzz.ratio(bad_name, name.lower())
    print(name, ratio)
    if(ratio >= 60):
      potential_names.append(name)
  if(len(potential_names) > 0):
    await client.send_message(message.author, "Unrecognized tradeskill `%s`. Did you mean one of the following: `%s`" % (bad_string, ', '.join(potential_names)))
    return
    # fuzzy compare
  await client.send_message(message.author, "Unrecognized tradeskill `%s`. Please use a real eq2 tradeskill profession name" % bad_string)

async def tradeskill_help(client, message, channel):
  help_message = """
  `!tradeskillremove [name], [profession]` is used to remove an entry you made to the tradeskill information. The profession and name are both required.
  You must own the entry or be a server admin or mod to remove it.
  """
  await client.send_message(message.author, help_message)


async def command(client, message, channel, delete_message, tradeskill_information):
  await delete_message(client, message)

  #load tradeskill_info from file
  if(tradeskill_information == json.loads('{}') and os.path.exists('tradeskill_info.json')):
    f = open('tradeskill_info.json', 'r')
    tradeskill_information = json.loads(f.read())
    f.close()

  server_id = message.server.id
  if(not server_id in tradeskill_information):
    await client.send_message(message.author, "This server does not have any tradeskillers information so there is nothing that can be removed. Please try again later.")
    return tradeskill_information
  server_tradeskill_information = tradeskill_information[server_id]
  message_content = message.content.strip()
  if(message_content.find(' ') < 0):
    await tradeskill_help(client, message, channel)
    return tradeskill_information
  if(message_content[18:].lower().strip() == 'help'):
    await tradeskill_help(client, message, channel)
    return tradeskill_information
  arguments = message_content[18:].split(',')
  if(len(arguments) != 2):
    await tradeskill_help(client, message, channel)
    return tradeskill_information
  char_name = arguments[0].strip()
  char_profession = arguments[1].strip()
  print(char_name)
  print(char_profession)
  if(not char_profession in tradeskills):
    await unrecognized_tradeskill(client, char_profession, message)
    return tradeskill_information
  if(not char_profession in server_tradeskill_information):
    await client.send_message(message.author, "There are no %ss to attempt to delete. Please check your command and try again." % char_profession)
    return tradeskill_information
  if(not char_name in server_tradeskill_information[char_profession]):
    await client.send_message(message.author, "There is no character named %s with profession %s in the tradeskill records. Please check your command and try again." % (char_name, char_profession))
    return tradeskill_information
  author_permissions = message.author.server_permissions
  override = author_permissions.administrator or author_permissions.manage_server or author_permissions.kick_members or author_permissions.ban_members or author_permissions.mute_members or message.channel.permissions_for(message.author).administrator
  if(server_tradeskill_information[char_profession][char_name]['owner'] == message.author.id or override):
    del tradeskill_information[server_id][char_profession][char_name]
    if(tradeskill_information[server_id][char_profession] == json.loads('{}')):
      del tradeskill_information[server_id][char_profession]
      if(tradeskill_information[server_id] == json.loads('{}')):
        del tradeskill_information[server_id]
  else:
    await client.send_message(message.author, "You do not own this entry and cannot delete it. If you think this is an error talk to a server mod or bot admin")
    return tradeskill_information
  tradeskill_info_file = open('tradeskill_info.json', 'w')
  tradeskill_info_file.write(json.dumps(tradeskill_information))
  tradeskill_info_file.close()
  await client.send_message(message.author, "Successfully deleted entry from tradeskill information.")
  return tradeskill_information

TRIGGER = '!tradeskillremove'