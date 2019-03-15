#add_role.py

"""
Add role function command

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@result: sends a message if roll being added is forbidden, or roll was successfully added
@result: deletes the triggering message always
@result: Gives user specified roll if possible
"""
forbidden_roles = ['admin', 'mod'] #Add roles here that can't be requested
async def command(client, message):
  await client.delete_message(message)
  rolesRaw = message.content[9:]
  spaceIndex = 0
  requested_roles = rolesRaw.lower().split(',')
  for i in range(0, len(requested_roles)):
    requested_roles[i] = requested_roles[i].strip()
  requested_roles = list(dict.fromkeys(requested_roles))
  for role in requested_roles:
    role_to_add = role
    if(role_to_add.lower() in forbidden_roles):
      await client.send_message(message.author, "You cannot add yourself to role '%s'" % role_to_add)
      return

  roles_to_add = []
  server_roles = message.server.roles
  for i in range(0, len(requested_roles)):
    for j in range(0, len(server_roles)):
      if(requested_roles[i] == server_roles[j].name.lower()):
        roles_to_add.append(server_roles[j])

  if(len(roles_to_add) > 0):
    added_roles = []
    await client.add_roles(message.author, *roles_to_add)
    for role in roles_to_add:
      added_roles.append(role.name)
    response_message = "You have been successfully added to, or already a part of, the following roles: %s" % added_roles
    await client.send_message(message.author, response_message)

TRIGGER = '!addrole'