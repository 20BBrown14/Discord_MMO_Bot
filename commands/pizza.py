#pizza.py

"""
Pizza command

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@param channel: The channel to send the command response to
@result: sends a message always
"""
async def command(client, message, channel):
  await client.send_message(channel, "I don't have money for pizza. I'll get you back next Tuesday, though")

TRIGGER = '!pizza'