import random
import challonge
import asyncio

class Team:
    def __init__(self, name, offense, defense):
        self.offense = offense
        self.defense = defense
        self.wins = 0
        self.loses = 0
        self.name = name
        self.pointsFor = 0

    def __eq__(self, other):
        if self.name == other.name:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.wins < other.wins:
            return True
        elif self.wins == other.wins:
            if self.pointsFor < other.pointsFor:
                return True
        else:
            return False

    def __gt__(self, other):
        if self.wins > other.wins:
            return True
        elif self.wins == other.wins:
            if self.pointsFor > other.pointsFor:
                return True
        else:
            return False

    def addPointsFor(self, points):
        self.pointsFor += points

    def win(self):
        self.wins += 1

    def loss(self):
        self.loses += 1

    def getName(self):
        return self.name

    def getOffense(self):
        return self.offense

    def getDefense(self):
        return self.defense

    def getRecord(self):
        return str(self.wins) +"-"+ str(self.loses)

class Game:
    def __init__(self, home, away):
        self.home = home
        self.away = away
        self.awayScore = 0
        self.homeScore = 0

    def fieldGoal(self, kickingTeam, yard):
        fg = random.randint(1, 100)
        yard += 17
        fgMade = False
        if yard < 20:
            fgMade = True
        elif yard < 30:
            if fg != 1:
                fgMade = True
        elif yard < 40:
            if fg > 6:
                fgMade = True
        elif yard < 50:
            if fg > 23:
                fgMade = True
        else:
            if fg > 36:
                fgMade = True
        if fgMade:
            print("The "+ kickingTeam.getName() + " have made a "+ str(yard) +" yard field goal!")
        else:
            print("The "+ kickingTeam.getName() + " have missed a "+ str(yard) +" yard field goal!")
        return fgMade

    def drive(self, offense, defense, homeTeam, inning):
        yard = 25
        down = 1
        toGo = 10
        while down < 5:
            #print("The "+ offense.getName() +" have the ball, "+ str(down) + " and "+ str(toGo) +" on the "+ str(yard))
            offenseRoll = random.randint(1, 100) + offense.getOffense()
            defenseRoll = random.randint(1, 100) + defense.getDefense()

            if offenseRoll > defenseRoll-inning:
                deviation = random.randint(1, 100)
                if deviation > 69:
                    yard += 11
                    down = 1
                    toGo = 10
                else:
                    toGo -= 5.5
                    yard += 5.5
                    down += 1
                if yard >= 100:
                    if homeTeam:
                        self.homeScore += 7
                    else:
                        self.awayScore += 7
                    print("TOUCHDOWN " + offense.getName())
                    break
                if toGo <= 0:
                    toGo = 10
                    down = 1
                if down == 4 and toGo > 0 and yard >= 60:
                    if self.fieldGoal(offense, 100 - yard):
                        if homeTeam:
                            self.homeScore += 3
                        else:
                            self.awayScore += 3
                    else:
                        break
            else:
                turnover = random.randint(0, 100)
                if turnover < 2:
                    print("THE " + offense.getName() + " TURN THE BALL OVER!")
                    break
                else:
                    down += 1

    def playGame(self):
        for inning in range(0, 9):
            self.drive(self.home, self.away, True, inning)
            self.drive(self.away, self.home, False, inning)


        overtime = False
        if self.homeScore == self.awayScore:
            print("Tied at "+ str(self.homeScore) +" at the end of regulation")
            overtime = True
            inning = 11

        while overtime and (self.homeScore == self.awayScore):
            self.drive(self.home, self.away, True, inning)
            self.drive(self.away, self.home, False, inning)
            inning += 1


        print("FINAL SCORE")
        print(self.home.getName() + " " + str(self.homeScore))
        print(self.away.getName() + " " + str(self.awayScore))
        print("\n")

        self.home.addPointsFor(self.homeScore)
        self.away.addPointsFor(self.awayScore)
        if self.homeScore > self.awayScore:
            self.home.win()
            self.away.loss()
            return self.home.getName() +" "+ str(self.homeScore) +"-"+ str(self.awayScore)
            #return self.home
        else:
            self.home.loss()
            self.away.win()
            return self.away.getName() +" "+ str(self.awayScore) +"-"+ str(self.homeScore)
            #return self.away


class Playoffs:
    def __init__(self, firstSeed, secondSeed, thirdSeed, fourthSeed, fifthSeed, sixthSeed, seventhseed, eightseed):
        self.participants = [firstSeed.name, secondSeed.name, thirdSeed.name, fourthSeed.name, fifthSeed.name, sixthSeed.name, seventhseed.name, eightseed.name]
        self.teams = [firstSeed, secondSeed, thirdSeed, fourthSeed, fifthSeed, sixthSeed, seventhseed, eightseed]

    async def tournament(self):
        user = await challonge.get_user('Kcin14', 'M2ZyNWHKoTJJjkwdg6JCrxyljE3HoeDH0AZdD8oa')
        tournaments = await user.get_tournaments()
        t = tournaments[0]
        await t.add_participants(self.participants)
        '''
        print("WILD CARD ROUND")
        g1 = Game(self.thirdSeed, self.sixthSeed)
        g2 = Game(self.fourthSeed, self.fifthSeed)

        winnerA = g1.playGame()
        winnerB = g2.playGame()

        if winnerA == self.thirdSeed:
            g3 = Game(self.secondSeed, winnerA)
            g4 = Game(self.firstSeed, winnerB)
        elif winnerA == self.sixthSeed:
            g3 = Game(self.secondSeed, winnerB)
            g4 = Game(self.firstSeed, winnerA)

        print("DIVISIONAL ROUND")

        winnerC = g3.playGame()
        winnerD = g4.playGame()

        championship = Game(winnerC, winnerD)

        champion = championship.playGame()
        return champion.getName().upper()
        '''
        return "No One"

async def tournamentBuilder():
    chal = await challonge.get_user('Kcin14', 'M2ZyNWHKoTJJjkwdg6JCrxyljE3HoeDH0AZdD8oa')
    await chal.create_tournament("2243 Preseason 2", "2243a")

def userGames():
    userIn = ""
    while True:
        userIn = input("Enter Team 1\n")
        if userIn == 'q':
            break
        team2 = input("Enter Team 2\n")
        for team in teams:
            if team.name == userIn:
                teamA = team
            elif team.name == team2:
                teamB = team
        g = Game(teamA, teamB)
        g.playGame()

async def tournamentGetter(teams):
    user = await challonge.get_user('Kcin14', 'M2ZyNWHKoTJJjkwdg6JCrxyljE3HoeDH0AZdD8oa')
    tournaments = await user.get_tournaments()
    t = tournaments[len(tournaments)-1]
    #await t.reset()
    participants = list()
    for team in teams:
        participants.append(await t.add_participant(team.name))
    for par in await t.get_participants():
        print(par.display_name +" "+ str(par.id))
    await t.start()
    matches = await t.get_matches()
    for match in matches:
        para = await t.get_participant(match.player1_id)
        parb = await t.get_participant(match.player2_id)
        teamA = None
        teamB = None
        for team in teams:
            if para.display_name == team.name:
                teamA = team
            elif parb.display_name == team.name:
                teamB = team
        g = Game(teamA, teamB)
        string = g.playGame().split()
        print(string[0])
        if len(string) == 2:
            for participant in participants:
                if string[0] == participant.display_name:
                    await match.report_winner(participant, string[len(string) - 1])
                    break
        else:
            name = ""
            for i in range(0, len(string)-1):
                name += string[i] + " "
            name = name[0:len(name)-1]
            print(name)
            for participant in participants:
                if name == participant.display_name:
                    await match.report_winner(participant, string[len(string) - 1])
                    break



year = "Teams.txt"
teams = list()
startFile = open(year, 'r')
for line in startFile:
    arr = line.split()
    if len(arr) == 3:
        teams.append(Team(arr[0], int(arr[1]), int(arr[2])))
        #print(arr[0])
    else:
        name = ""
        for i in range(0, len(arr) - 2):
            name += arr[i] + " "
        name = name[0:len(name)-1]
        teams.append(Team(name, int(arr[len(arr)-2]), int(arr[len(arr)-1])))
        #print(name)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
champion = loop.run_until_complete(tournamentGetter(teams))

northeast = list()
easterncentral = list()
southeast = list()
northwest = list()
westerncentral = list()
southwest = list()

division = [northeast, northwest, easterncentral, northwest, westerncentral, southwest]

bottom = 0
top = 4
for div in division:
    for i in range(bottom, top):
        div.append(teams[i])
    bottom += 4
    top += 4

'''
for i in range(0, len(teams)):
    for j in range(i+1, len(teams)):
        g = Game(teams[i], teams[j])
        g.playGame()

for i in range(0, len(teams)):
    for j in range(0, len(teams)-i-1):
        if teams[j] > teams[j+1]:
            teams[j], teams[j + 1] = teams[j + 1], teams[j]

teams = list(reversed(teams))

print("")
for i in range(0, len(teams)):
    print(teams[i].getName() +": "+ teams[i].getRecord())


print("")
p = Playoffs(teams[0], teams[1], teams[2], teams[3], teams[4], teams[5], teams[6], teams[7])
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
champion = loop.run_until_complete(p.tournament())
print("THE " + champion + " ARE WORLD CHAMPIONS!")
'''



