# raid.py

import datetime
import json
import os
# set raid timers

# { serverId: { raid_time: { time }, time_set: { someTime } } } 

# !raid set Friday, 6PM, CST Saturday, 7PM, CST
async def command(client, message, channel, delete_message, raid_info):
  await delete_message(client, message)
  message_server = message.server
  message_content = message.content
  now = datetime.datetime.now().timestamp()

  #load raid_info from file
  if(raid_info == json.loads('{}') and os.path.exists('raid_info.json')):
    f = open('raid_info.json', 'r')
    raid_info = json.loads(f.read())
    f.close()

  #set raid info
  if(message_content == '!raid'):
    if(message_server.id in raid_info):
      raid_time_string = raid_info[message_server.id]["raid_time"]
      raid_time_set = raid_info[message_server.id]["time_set"]
      time = datetime.datetime.fromtimestamp(int(raid_time_set))
      raid_time_author = raid_info[message_server.id]["author"]
      message_response = "Raids are %s. This was determined at %s by %s" % (raid_time_string, time, raid_time_author)
      await client.send_message(channel, message_response)
    else:
      await client.send_message(message.author, "Raid times have not been set for this server yet.")
  if(message_content[6:9].strip() == 'set'):
    author_permissions = message.author.server_permissions
    if(author_permissions.move_members and author_permissions.deafen_members and author_permissions.mute_members):
      new_raid_time = message_content[10:].strip()
      author = message.author.name
      if(message.author.nick):
        author = message.author.nick
      raid_info[message_server.id] = json.loads("{\"raid_time\": \"%s\", \"time_set\":\"%s\", \"author\":\"%s\"}" % (new_raid_time, str(int(now)), author))
      await client.send_message(message.author, 'Raid times have been set. Example response to `!raid`:')
      await client.send_message(message.author, 'Raids are %s. This was determined at %s by %s' % (new_raid_time, datetime.datetime.fromtimestamp(int(now)), author))
      info_file = open('raid_info.json', 'w')
      info_file.write(json.dumps(raid_info))
      info_file.close()
      return raid_info
    await client.send_message(message.author, 'You do not have permissions to set the raid information. Contact your Discord admins if you believe this is in error.')
  return raid_info


TRIGGER = '!raid'