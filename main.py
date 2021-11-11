import os, discord, players, game

gamesList = []

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
    try:
      stats = players.get_stats(str(msg.author))
      quote_text = '>>> {}'.format(stats)
      await msg.channel.send(quote_text)
    except:
      await msg.channel.send("You do not have an account! \nPlease create one with **$register.** \n\n\nIf you have recently changed your discord name you will need to change it back or contact an admin for help.")





  # MATCH COMMANDS
  if msg.content.startswith("$setup"):
    await msg.channel.send(f'Please enter the amount of maps you\'d like to play. (Odd numbers only.)\nExample\n3')
    try:
      games = await client.wait_for("message")
      games = int(games.content)

      if (games % 2) == 0:
        print(games % 2)
        raise TypeError
      else:

        # CREATE GAME FUNCTION
        print("Creating a new game\nBest of {}".format(games))
        await msg.channel.send("Creating a new game\n**Best of {}**".format(games))


        gameName = "Game1"

        Game = game.Game(gameName, games, [0,0],[str(msg.author)],[])
        game.appendGame(Game)

        
        
        print(game.listGames())
    except TypeError:
      await msg.channel.send("Please enter an odd number.")

  if msg.content.startswith("$join"):
    await(msg.channel.send(f"Select a Match to join:\n{game.listGames()}"))
    match = await client.wait_for("message").content
    
    print(f"Match chosen = {match}")
    currentGame = game.selectGame(match)
    print(f"Associated Game Object = {currentGame}")
    print(currentGame.team1,currentGame.team2)
    
    await(msg.channel.send(f"Select a Team to join:\n{currentGame.listPlayers}"))
    teamChosen = await client.wait_for("message")
    teamChosen = teamChosen.content
    await(msg.channel.send(f"You Chose {teamChosen}"))

    

    
    
    
    


  # List Games
  if msg.content.startswith("$games"):
    try:
      await(msg.channel.send(game.listGames()))
    except:
      await(msg.channel.send("No Lobbies currently running."))

      

    
    





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
