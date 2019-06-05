import random

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
            offenseRoll = random.randint(1, 300) + offense.getOffense()
            defenseRoll = random.randint(1, 300) + defense.getDefense()

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
        for inning in range(0, 8):
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
            return self.away.getName() +" "+ str(self.homeScore) +"-"+ str(self.awayScore)
            #return self.away