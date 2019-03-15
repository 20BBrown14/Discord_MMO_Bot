#help.py

"""
Help function command

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@param channel: The channel to send the command response to
@result: sends a message with help information always
@result: deletes the triggering message always
"""
async def command(client, message, channel):
  await client.delete_message(message)
  help_commands = """Available commands:
      < `!help` >: *Displays this message*
      < `!addrole role1, role2, ...` >: *Gives the specified role to you*
      < `!removerole role1, role2, ...` >: *Removes the specified role from you*"""
  help_information = """Information:
    This bot was designed for an EverQuest2 Discord server.
    Contact Vixxle#8335 if you have questions. 
    Source Code: <https://github.com/20BBrown14/Discord_MMO_Bot>
    Help Message last updated: Mar 14, 2019"""
  await client.send_message(channel, help_commands + "\n" + help_information)

TRIGGER = '!help'
