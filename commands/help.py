#help.py

"""
Help function command

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@param channel: The channel to send the command response to
@result: sends a message with help information always
@result: deletes the triggering message always
"""
async def command(client, message, channel, delete_message):
  await delete_message(client, message)
  help_commands = """Available commands:
      < `!help` >: *Displays this message*
      < `!addrole role1, role2, ...` >: *Gives the specified role to you*
      < `!removerole role1, role2, ...` >: *Removes the specified role from you*
      < `!lfg charName, charClass, charLevel, notes(option)` > *Adds you to the lfg list*
          If you are already on this list just `!lfg` will remove you from the list
          `notes` option is not required
          1 hours old entries will be automatically removed
          Only 1 entry per user
      < `!listroles` >: *Lists available roles on this server*
      < `!pizza` >: *I don't know. Just do it.*"""
  rule_information = """Applied rules:
      < `lfg_clean` >: *Removes any message from a channel named 'lfg'*"""
  help_information = """Information:
    This bot was designed for an EverQuest2 Discord server.
    Contact Vixxle#8335 if you have questions. 
    Source Code: <https://github.com/20BBrown14/Discord_MMO_Bot>
    Help Message last updated: Mar 20, 2019"""
  await client.send_message(message.author, help_commands + "\n" + rule_information + "\n" + help_information)

TRIGGER = '!help'
