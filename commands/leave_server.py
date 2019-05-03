#leave_server.py

"""
Leave Server command

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@param channel: The channel to send the command response to
@param delete_message: Function to delete the given message 
@result: sends a message always
"""
async def command(client, message, channel, delete_message):
  await delete_message(client, message)
  if(message.author.id != '159785058381725696'):
    await client.send_message(message.author, "You do not have permissions to do that! Stop that, damnit!")
    return
  message_content = message.content
  server_to_leave = message_content[message_content.find(' ')+1:]
  connected_servers = client.servers
  for server in connected_servers:
    if(server.name.lower() == server_to_leave.lower()):
      client.leave_server(server)
      await client.send_message(message.author, "Successfully left server `%s`" % server_to_leave)
      return
  await client.send_message(message.author, "Not connected to a server with that name. Cannot leave.")
  return


TRIGGER = '!leaveserver'