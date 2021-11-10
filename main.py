import os
import discord
import players




client = discord.Client()

@client.event
async def on_ready():
  print(f'Successfully logged in as {client.user}')


@client.event
async def on_message(msg):
  





  
  if msg.author == client.user:
    return
  if msg.content.startswith("$help"):
    await msg.channel.send(f'$register')
  if msg.content.startswith("$register"):
    await msg.channel.send(f'Please enter your ActivisionID')
    
    gamertag = await client.wait_for("message")
    
    #adds user to database
    out = players.add_player(str(msg.author),gamertag.content)
    await msg.channel.send(out)

    # update user prefix
    newNick = ("-{ELO}- {nick}".format(ELO=players.get_elo(str(msg.author)),nick = players.get_gamertag(str(msg.author))))
    await msg.author.edit(nick = newNick)
    
    
  if msg.content.startswith("$stats"):
    value = players.get_stats(str(msg.author))
    await msg.channel.send(value)




  # ADMIN COMMANDS
  if msg.content.startswith("$-clear"):
    await(msg.channel.send(players.clear()))
  if msg.content.startswith("$-list"):
    plist = players.list_users()
    await msg.channel.send(plist)
  if msg.content.startswith("$-del"):
    await msg.channel.send(f'Please enter the user you would like to delete.')
    user = await client.wait_for("message")

    out = players.del_player(user.content)
    await msg.channel.send(out)
  
    


client.run(os.environ['TOKEN'])
