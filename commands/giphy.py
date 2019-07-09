async def giphy_command(client, message, response_channel, delete_message, giphy_api_key):
  forbidden_gifs = ['/gamerescape', '/xivdb', '/giphy', '/tts', '/tenor', '/me', '/tableflip', '/unflip', '/shrug', '/nick']
    spaceIndex = messageContent.find(' ')
    if spaceIndex != -1 and messageContent[:spaceIndex] in forbidden_gifs:
      return
    elif spaceIndex == -1 and messageContent in forbidden_gifs:
      print("Returning due to forbidden gif search")
      return
    if('\n' in message.content):
      await client.send_message(message.author, "Forbidden search string used")
      return
    search_params = messageContent[1:]
    search_params_sb = ""
    first = True
    for i in range(0,len(search_params)):
      if search_params[i] == ' ':
        search_params_sb = search_params_sb + search_params[len(search_params_sb):i] + '+'
    search_params_sb = search_params_sb + search_params[len(search_params_sb):]
    data = json.loads((urllib.request.urlopen('http://api.giphy.com/v1/gifs/search?q='+search_params_sb+'&api_key=' + str(giphy_api_key) + '&limit=100').read()).decode('utf-8'))
    new_result = True
    if(len(data["data"]) <= 0 ):
      await client.send_message(author, "Sorry, but '"+messageContent[1:] + "' returned no results from Giphy.")
    else:
      url = json.dumps(data["data"][random.randint(0,len(data["data"])-1)]["url"], sort_keys = True, indent = 4)
      displayName = ''
      if(hasattr(author, 'nick')):
        displayName = author.nick
      else:
        displayName = author.name
      await client.send_message(message.channel, url[1:len(url)-1] + ' \'' + messageContent[1:] + '\' by ' + displayName + ' with ' + str(len(data["data"])) + ' results')
    if(message and message.channel.name):
      await delete_message(client, message)