import os, discord, players, game

gamesList = []

client = discord.Client()
def userErrorMessage():
    return ">>> You do not have an account! \nPlease create one with **$register.** \n\n\nIf you have recently changed your discord name you will need to change it back or contact an admin for help."
@client.event
async def on_ready():
  print(f'Successfully logged in as {client.user}')


@client.event
async def on_message(msg):
  if msg.author == client.user:
    return
  if msg.content.startswith("$help"):
      helpMsg = '>>> __**Account Commands**__\n**$register** - To register a new account.\n**$stats** - See your statistics.  \n\n\n__**Match Commands**__\n**$setup** - Setup a new match. \n**$join** - Join an existing match. \n**$start** - Start a new match. \n**$report** - Report which team won'
      await msg.channel.send(helpMsg)
  if msg.content.startswith("$register"):
    if players.is_user(msg.author):
        accountExists = ">>>You already have an account!\nUse **$stats** to see your statistics."
        await msg.channel.send(accountExists)
        return

    out = '> Please enter your ActivisionID'
    await msg.channel.send(out)
    
    gamertag = await client.wait_for("message")
    
    #adds user to database
    out = players.add_player(str(msg.author),gamertag.content)
    await msg.channel.send(out)

    # update user prefix
    newNick = ("-{ELO}- {nick}".format(ELO=players.get_elo(str(msg.author)),nick = players.get_gamertag(str(msg.author))))
    await msg.author.edit(nick = newNick)
    
    
  if msg.content.startswith("$stats"):
    print(msg.author)
    #if not players.is_user(msg.author):
    #    await msg.channel.send(userErrorMessage())
    #    return
    stats = players.get_stats(str(msg.author))
    quote_text = '>>> {}'.format(stats)
    await msg.channel.send(quote_text)







  # MATCH COMMANDS
  if msg.content.startswith("$setup"):
    
   

    await msg.channel.send(f'>>> Please enter the amount of maps you\'d like to play. (Odd numbers only.)\nExample\n**3**')
    try:
      games = await client.wait_for("message")
      games = int(games.content)

      if (games % 2) == 0:
        print(games % 2)
        raise TypeError
      else:

        # CREATE GAME FUNCTION
        print("Creating a new game\nBest of {}".format(games))
        
        gameName = "Game1"

        Game = game.Game(gameName, games, [0,0],[str(msg.author)],[])
        game.appendGame(Game)

        await msg.channel.send(">>> Creating a new game\n\n**Best of {}** \n Name: **{}**\n use **$join** then enter name.".format(games,gameName))
        
        print(game.listGames())
    except TypeError:
      await msg.channel.send("Please enter an odd number.")

  if msg.content.startswith("$join"):
    
    await(msg.channel.send(f">>> Select a Match to join:\n**{game.listGames()}**"))
    match = await client.wait_for("message")
    match = match.content
    
    print(f"Match chosen = {match}")
    currentGame = game.selectGame(match)
    print(f"Associated Game Object = {currentGame}")
    print(currentGame.team1,currentGame.team2)
    
    await(msg.channel.send(f">>>Select a Team to join:\n{currentGame.listPlayers()}"))
    teamChosen = await client.wait_for("message")
    teamChosen = teamChosen.content
    await(msg.channel.send(f"You Chose {teamChosen}"))

    ## Add user to team on game
    currentGame.addPlayer(str(msg.author), teamChosen)

    
    
    
    


  # List Games
  if msg.content.startswith("$games"):
    
    try:
        await(msg.channel.send(game.listGames()))
    except:
        await(msg.channel.send("No Lobbies currently running."))

      

    
    





  # ADMIN COMMANDS
  adminChannelID=688961739391369276
  
  if msg.content.startswith("$-clear") and msg.channel.id == adminChannelID:
      await(msg.channel.send(players.clear()))
  if msg.content.startswith("$-list") and msg.channel.id == adminChannelID:
      plist = players.list_users()
      print(msg.channel.id)
      await msg.channel.send(plist)
  if msg.content.startswith("$-del") and msg.channel.id == adminChannelID:
    await msg.channel.send(f'Please enter the user you would like to delete.')
    user = await client.wait_for("message")

    out = players.del_player(user.content)
    await msg.channel.send(out)
  
    


client.run(os.environ['TOKEN'])
