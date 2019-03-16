#list_roles.py

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
async def command(client, message, channel, delete_message):
  await delete_message(client, message)
  server_roles = message.server.roles
  server_role_names = []
  for role in server_roles:
    server_role_names.append(role.name)
  await client.send_message(message.author, "Available roles are: %s" % (str(server_role_names)))

TRIGGER = '!listroles'