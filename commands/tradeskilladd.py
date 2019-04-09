# tradeskilladd.py

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
  `!tradeskilladd [name], [level], [profession/class], [notes(option)]` is used to add yourself to a list of tradeskillers that the bot can track to supply information to others.
  An example usage would be `!tradeskilladd Nibikk, 50, Provisioner, All books`
  This example command see that the in-game name is Nibikk, the level 50, the profession is Provisioner, and in the notes section is 'All books'
  Name, level, and profession/class are required to supply but notes is optional.
  To edit an entry already in the tradeskill information you must own it or be an admin.
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
  message_content = message.content.strip()
  if(message_content.find(' ') < 0):
    await tradeskill_help(client, message, channel)
    return tradeskill_information
  if(message_content[15:].lower().strip() == 'help'):
    await tradeskill_help(client, message, channel)
    return tradeskill_information
  arguments = message_content[15:].split(',')
  if(len(arguments) > 4 or len(arguments) < 3):
    await tradeskill_help(client, message, channel)
    return tradeskill_information
  char_name = arguments[0].strip()
  char_level = arguments[1].strip()
  char_profession = arguments[2].strip()
  if(not char_profession in tradeskills):
    await unrecognized_tradeskill(client, char_profession, message)
    return tradeskill_information
  char_notes = ''
  if(len(arguments) > 3):
    char_notes = arguments[3].strip()
  new_json_raw_string = '{"level": "%s", "notes": "%s", "owner": "%s"}' % (char_level, char_notes, str(message.author.id))
  if(server_id in tradeskill_information):
    if(char_profession in tradeskill_information[server_id]):
      if(char_name in tradeskill_information[server_id][char_profession]):
        stored_owner = tradeskill_information[server_id][char_profession][char_name][owner]
        if(not stored_owner == str(message.author.id)):
          await client.send_message(message.author, "There is already an entry with that character name and profession combination and you do not own it. If you think this is in error contact a server mod.")
          return tradeskill_information
      tradeskill_information[server_id][char_profession][char_name] = json.loads(new_json_raw_string)
    else:
      tradeskill_information[server_id][char_profession] = json.loads('{"%s": %s}' % (char_name, new_json_raw_string))
  else:
    tradeskill_information[server_id] = json.loads('{"%s": {"%s": %s}}' % (char_profession, char_name, new_json_raw_string))
  tradeskill_info_file = open('tradeskill_info.json', 'w')
  tradeskill_info_file.write(json.dumps(tradeskill_information))
  tradeskill_info_file.close()
  await client.send_message(message.author, "Successfully added entry to tradeskill information.")
  return tradeskill_information








TRIGGER = '!tradeskilladd'