# tradeskill.py


import json
from fuzzywuzzy import fuzz
import os

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
  `!tradeskill [profession/class (optional)]` is used to get the people who are of that tradeskill profession. Or all professions if no profession is provided with the command
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
    await client.send_message(message.author, "Nobody on this server has added themselves as a tradeskiller yet. Please try again later.")
    return
  server_tradeskill_information = tradeskill_information[server_id]
  message_content = message.content.strip().lower()
  wanted_profession = ''
  if(message_content.find(' ') > 0):
    wanted_profession = message_content[12:].strip()
    if(not wanted_profession in tradeskills):
      await unrecognized_tradeskill(client, wanted_profession, message)
      return
    if(not wanted_profession in server_tradeskill_information):
      await client.send_message(message.author, "Nobody on this server has added themselves as a %s yet. Maybe try again later." % wanted_profession)
      return
    profession_information = server_tradeskill_information[wanted_profession]
    tradeskill_chars = profession_information.keys()
    tradeskill_information_reply = '%ss on this server\n\n' % wanted_profession
    for char_name in tradeskill_chars:
      tradeskill_information_reply = tradeskill_information_reply + "%s: Level %s %s - %s\n" % (char_name, profession_information[char_name]['level'], wanted_profession, profession_information[char_name]['notes'])
    await client.send_message(message.author, tradeskill_information_reply)
  else:
    tradeskill_information_reply = 'All tradeskillers on this server. You can specify a profession with `!tradeskill [profession]`\n\n'
    for profession in server_tradeskill_information:
      tradeskill_information_reply = tradeskill_information_reply + '%ss\n' % profession
      profession_information = server_tradeskill_information[profession]
      for char_name in server_tradeskill_information[profession]:
        tradeskill_information_reply = tradeskill_information_reply + "%s: Level %s %s - %s\n" % (char_name, profession_information[char_name]['level'], profession, profession_information[char_name]['notes'])
    await client.send_message(message.author, tradeskill_information_reply)

TRIGGER = '!tradeskill'