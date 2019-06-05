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

    def setOffense(self, offense):
        self.offense = offense

    def setDefense(self, defense):
        self.defense = defense