#lfg_channel_clean.py

"""
lfg channel clean rule

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@param channel: The channel to send the response to
@param delete_message: The function to delete a message
@result: deletes a message always
"""
async def rule(client, message, delete_message):
  await delete_message(client, message)

def APPLIES(client, message):
  if(message.channel.name.lower() == 'lfg' and message.author != client.user):
    return True
  return False