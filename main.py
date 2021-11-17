import os, discord, players, game
from discord.ext import commands

client = discord.Client()
client = commands.Bot(command_prefix='$')


def userErrorMessage():
    return ">>> You do not have an account! \nPlease create one with **$register.** \n\n\n*If you have recently changed your discord name,\n you will need to **change it back** or **contact an admin for help.***"


def isNotAuthor(user, original):
    if user != original:
        return "> Only the original author may reply to this!"
    else:
        return False


@client.event
async def on_ready():
    print(f'Successfully logged in as {client.user}')


# updates the prefix of the username
async def update_prefix(user, msg):
    newNick = ("-{ELO}- {nick}".format(ELO=players.get_elo(user),
                                       nick=players.get_gamertag(user)))
    await msg.author.edit(nick=newNick)

#-- ACCOUNT COMMANDS --#

@client.command()
async def register(msg, *, gamertag):
    print(str(msg.author))
    #adds user to database
    out = players.add_player(str(msg.author), gamertag)
    await msg.channel.send(out)

    # update user prefix
    # requires username, message.
    update_prefix(msg.author, msg)


@client.command()
async def stats(msg):
    if not players.is_user(str(msg.author)):
        await msg.channel.send(userErrorMessage())
        return
    stats = players.get_stats(str(msg.author))
    quote_text = '>>> {}'.format(stats)
    await msg.channel.send(quote_text)




#--- GAME COMMANDS ---#


@client.command()
async def setup(msg, *, games):
    try:
        games = int(games)

        if (games % 2) == 0:
            print(games % 2)
            raise TypeError
        else:
            # CREATE GAME FUNCTION
            print("Creating a new game\nBest of {}".format(games))
            gameName = "Game1"

            Game = game.Game(gameName, games, [0, 0],
                                [str(msg.author)], [])
            game.appendGame(Game)

            await msg.channel.send(
                f">>> *creating a new game*\n\n**Best of {games}** \n Name: **{gameName}**\n use **$join {gameName}**")
            print(game.listGames())
    except:
        await msg.channel.send("Please enter an odd number.")
@client.command()
async def join(msg, *, gameName):
    originalAuthor = msg.author
    if len(game.gamesList) == 0:
        await (msg.channel.send(
            f">>> No games currently running!\n Use **$setup** to create a new game."
        ))
        return

    if gameName not in game.listGames():
        await (msg.channel.send(
            f">>> No game chosen. \nTry again with **$join**"))
        return

    print(f"Match chosen = {gameName}")
    currentGame = game.selectGame(gameName)
    print(f"Associated Game Object = {currentGame}")
    print(currentGame.team1, currentGame.team2)

    await (msg.channel.send(
        f">>> Select a Team to join:\n{currentGame.listPlayers()}"))
    teamChosen = await client.wait_for("message")
    teamChosen = teamChosen.content

    options = ['team 2','2','team2','team 1','1','team1']
    if teamChosen.lower() not in options:
        await (msg.channel.send("You need to enter Team 1, or Team 2"))
        return
    await (msg.channel.send(f"You Chose {teamChosen}"))
    ## Add user to team on game
    
    currentGame.addPlayer(str(msg.author), teamChosen)

@client.command()
async def games(msg):
    try:
        await (msg.channel.send(game.listGames()))
    except:
        await (msg.channel.send(">>> No Lobbies currently running.\n_Create one now with_ **$setup #**"))


#-- ADMIN COMMANDS --#



#@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    if msg.content.startswith("$help"):
        helpMsg = '>>> __**Account Commands**__\n**$register** - To register a new account.\n**$stats** - See your statistics.  \n\n\n__**Match Commands**__\n**$setup** - Setup a new match. \n**$join** - Join an existing match. \n**$start** - Start a new match. \n**$report** - Report which team won'
        await msg.channel.send(helpMsg)


    # MATCH COMMANDS
adminChannelID = 688961739391369276
@client.command()
async def clear(msg):
    if msg.channel.id != adminChannelID:
        return
    
    await (msg.channel.send(players.clear()))
@client.command()
async def delete(msg, *, user):
    if msg.channel.id != adminChannelID:
        return
    out = players.del_player(user)
    await msg.channel.send(out)
@client.command()
async def list(msg):
    if msg.channel.id != adminChannelID:
        return
    plist = players.list_users()
    print(msg.channel.id)
    await msg.channel.send(plist)


        

   

client.run(os.environ['TOKEN'])
