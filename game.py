from replit import db
import players

gamesList = []


class Game():
    def __init__(self, name, games, score, team1, team2):
        self.name = name
        self.games = games
        self.score = score
        self.team1 = team1
        self.team2 = team2

    def listPlayers(self):
        out = '**Team 1:**\n'
        if not self.team1:
            out += "No Players"
        for i in self.team1:
            out += f"{players.show_player(i)}\n"
        out += '\n**Team 2:**\n'
        if not self.team2:
            out += "No Players"
        for i in self.team2:
            out += f"{players.show_player(i)}\n"
        if out == '':
            out = "No Players"
        return out

    def addPlayer(self, player, team):
        team1list = ["team 1",'1','team1']
        team2list = ["team 2",'2','team2']
        if team.lower() in team1list:
            self.team1.append(player)
        elif team.lower() in team2list:
            self.team2.append(player)
        else:
            print("Couldnt add player to team")
    def playerCount(self):
        total  = len(self.team1)+len(self.team2)
        return total


    #def listGames(self):
def appendGame(game):
    gamesList.append(game)
    print("Created game and added to list", game.name)


def listGames():
    out = ''
    for i in gamesList:
        out += f"{i.name} ({i.playerCount()})\n"
    return out





def selectGame(name):
    for i in gamesList:
        if i.name == name:
            return i
