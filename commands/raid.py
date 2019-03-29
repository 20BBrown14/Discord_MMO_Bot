# raid.py

import datetime
import json
# set raid timers

# { serverId: { raid_time: { time }, time_set: { someTime } } } 

# !raid set Friday, 6PM, CST Saturday, 7PM, CST
async def command(client, message, channel, delete_message, raid_info):
  await delete_message(client, message)
  message_server = message.server
  message_content = message.content
  now = datetime.datetime.now().timestamp()

  #set raid info
  if(message_content == '!raid'):
    if(message_server.id in raid_info):
      raid_time_string = raid_info[message_server.id]["raid_time"]
      raid_time_set = raid_info[message_server.id]["time_set"]
      time = datetime.datetime.fromtimestamp(float(raid_time_set))
      raid_time_author = raid_info[message_server.id]["author"]
      message_response = "Raids are %s. This was determined at %s by %s" % (raid_time_string, time, raid_time_author)
    await client.send_message(channel, message_response)
  if(message_content[6:9].strip() == 'set'):
    new_raid_time = message_content[10:].strip()
    raid_info[message_server.id] = json.loads("{\"raid_time\": \"%s\", \"time_set\":\"%s\", \"author\":\"%s\"}" % (new_raid_time, str(now), message.author.nick))
    print(raid_info)
  return raid_info
TRIGGER = '!raid'