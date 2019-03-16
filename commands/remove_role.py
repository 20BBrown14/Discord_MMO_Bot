#remove_role.py

"""
Removed role Function Command

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@result: sends a message if role being removed is forbidden, or role was successfully removed
@result: deletes the triggering message always
@result: removes the specified roles if possible
"""
forbidden_roles = ['admin', 'mod'] #Add roles here that shouldn't be removed
async def command(client, message, delete_message):
  await delete_message(client, message)
  rolesRaw = message.content[12:]
  spaceIndex = 0
  requested_roles = rolesRaw.lower().split(',')
  print(requested_roles)
  for i in range(0, len(requested_roles)):
    requested_roles[i] = requested_roles[i].strip()
  requested_roles = list(dict.fromkeys(requested_roles))

  for role in requested_roles:
    role_to_remove = role
    if(role_to_remove.lower() in forbidden_roles):
      await client.send_message(message.author, "You cannot remove yourself from role '%s'" % role_to_remove)
      return

  roles_to_remove = []
  server_roles = message.server.roles
  for i in range(0, len(requested_roles)):
    for j in range(0, len(server_roles)):
      if(requested_roles[i] == server_roles[j].name.lower()):
        print(requested_roles[i])
        roles_to_remove.append(server_roles[j])

  print(roles_to_remove)
  if(len(roles_to_remove) > 0):
    removed_roles = []
    await client.remove_roles(message.author, *roles_to_remove)
    for role in roles_to_remove:
      removed_roles.append(role.name)
    response_message = "You have been successfully removed from, or were not a part of, the following roles: %s" % removed_roles
    await client.send_message(message.author, response_message)

TRIGGER = '!removerole'