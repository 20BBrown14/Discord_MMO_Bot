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

  help_commands_1 = """Available commands:
      < `!addrole role1, role2, ...` >: *Gives the specified role to you*

      < `!help` >: *Displays this message*

      < `!lfg charName, charClass, charLevel, notes(option)` > *Adds you to the lfg list*
          If you are already on this list just `!lfg` will remove you from the list
          `notes` option is not required
          1 hours old entries will be automatically removed
          Only 1 entry per user

      < `!listroles` >: *Lists available roles on this server*

      < `!pizza` >: *I don't know. Just do it.*

      < `!raid` >: *Responds with raid time if set by raid leaders*
          `!raid set <raid information>` is used by raid leaders to set raid information returned by `!raid` command.
          Discord users need permission to move, deafen, and mute in voice channels to use the `!raid set` option.

      < `!removerole role1, role2, ...` >: *Removes the specified role from you*"""
  help_commands_2 = """

      < `!tradeskill [profession(optional)]` >: *Lists all users on server who have declared themselves the provided profession.*
          Providing the profession is optional and if not provided will list all tradeskillers on this server

      < `!tradeskilladd [name], [level], [profession], [notes(optional)]` >: *Adds your entry to the tradeskill information*
          Providing the notes option is optional. A entry with the same name or profession will be overwritten if you owned the original entry.

      < `!tradeskillremove [name], [profession]` >: *Removes the provided character name and profession combo from the tradeskill information*
          You must either be an admin or own the original entry to remove it.

      < `!weather option=value` >: *Displays weather for location specified*
         Use `!weather help` for available weather options"""

  rule_information = """
    Applied rules:
      < `lfg_clean` >: *Removes any message from a channel named 'lfg'*"""

  help_information = """Information:
    This bot was designed for an EverQuest2 Discord server.
    Contact Vixxle#8335 if you have questions. 
    Source Code: <https://github.com/20BBrown14/Discord_MMO_Bot>
    Help Message last updated: Apr 9, 2019"""
  await client.send_message(message.author, help_commands_1)
  await client.send_message(message.author, help_commands_2)
  await client.send_message(message.author, rule_information)
  await client.send_message(message.author, help_information)

TRIGGER = '!help'
