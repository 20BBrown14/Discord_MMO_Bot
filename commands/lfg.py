#lfg.py

import datetime
import time

"""
Add role function command

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@param channel: The channel the discord will respond in
@param current_table: The current lfg table
@param lfg_message: The message containing the current table
@result: sends or edits the current table in a message to the lfg channel if possible
@result: sends message to use if a user error occured
@result: deletes the triggering message always
"""
HEADER = ['DISCORD', 'CHAR', 'CLASS', 'LEVEL', 'NOTES']

async def command(client, message, channel, current_table, lfg_message, delete_message):
  await delete_message(client, message)
  message_args_raw = message.content[5:] #get args from message
  message_args = message_args_raw.split(',') #split args into arrow

  def generate_table_string():
    table_string = ''
    for item in current_table[0]: #Add header to table string
      table_string = table_string + item + '\t'
    table_string = table_string + '\n'

    for i in range(1, len(current_table)): #For each row in table
      for j in range(2, len(current_table[i])): #Add each item to table string
        table_string = table_string + current_table[i][j] + '\t'
      table_string = table_string + '\n'
    return table_string

  async def clean_lfg_table():
    now = datetime.datetime.now()
    dirty = False
    for i in range(1, len(current_table)):
      difference = now - current_table[i][1]
      hours, remainder = divmod(difference.seconds, 3600)
      minutes, seconds = divmod(remainder, 60)
      if(minutes > 60):
        current_table.remove(current_table[i])
        current_table.remove(row)
        dirty = True
    if(dirty):
      print(dirty)
      if(not lfg_message == None):
        lfg_message = await client.edit_message(lfg_message, "```%s```" % generate_table_string())
      else:
        lfg_message = await client.send_message(channel, "```%s```" % generate_table_string())

  try: #check that args exist
    char_name = message_args[0]
    char_class = message_args[1]
    char_level = message_args[2]
  except:
    #failure
    for i in range(1, len(current_table)):
      if(message.author.id == current_table[i][0]):
        current_table.remove(current_table[i])
      if(not lfg_message == None):
        lfg_message = await client.edit_message(lfg_message, "```%s```" % generate_table_string())
      else:
        lfg_message = await client.send_message(channel, "```%s```" % generate_table_string())
      return current_table, lfg_message
    failure_message = 'Be sure to format the command as `!lfg [character name], [character class], [character level], [optional notes]` without brackets'
    await client.send_message(message.author, failure_message)
    return current_table, lfg_message
  if(len(message_args) > 3): #check if optional notes arg exists
    notes = message_args[3]

  for i in range(0, len(message_args)): #strip args
    message_args[i] = message_args[i].strip()
  if(len(current_table) <= 0): #If table doesn't have header, add one
    current_table.append(HEADER)

  for row in current_table: #If user already exists in table remove it
    if(message.author.id in row):
      current_table.remove(row)

  newRow = [message.author.id, message.timestamp, message.author.nick] #Add user id and user nick to row
  for item in message_args: #Append message args to new row
    newRow.append(item)
  current_table.append(newRow) #append new row to table
  await clean_lfg_table()

  if(not lfg_message == None):
    lfg_message = await client.edit_message(lfg_message, "```%s```" % generate_table_string())
  else:
    lfg_message = await client.send_message(channel, "```%s```" % generate_table_string())
  return current_table, lfg_message





TRIGGER = '!lfg'