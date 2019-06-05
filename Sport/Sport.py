import random
import challonge
import asyncio
import Game
import Team
import Playoffs
from challonge.tournament import TournamentType

async def regularSeason(teams):
    chal = await challonge.get_user('Kcin14', 'M2ZyNWHKoTJJjkwdg6JCrxyljE3HoeDH0AZdD8oa')
    t = await chal.create_tournament("2243 Preseason 6", "2243f", TournamentType.round_robin)
    participants = list()
    for team in teams:
        participants.append(await t.add_participant(team.name))
    await t.start()
    matches = await t.get_matches()
    for match in matches:
        parA = await t.get_participant(match.player1_id)
        parB = await t.get_participant(match.player2_id)
        teamA = None
        teamB = None
        for team in teams:
            if parA.display_name == team.name:
                teamA = team
            elif parB.display_name == team.name:
                teamB = team
        g = Game.Game(teamA, teamB)
        string = g.playGame().split()
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
            for participant in participants:
                if name == participant.display_name:
                    await match.report_winner(participant, string[len(string) - 1])
                    break
    await t.finalize()
    rankings = await t.get_final_ranking()
    return rankings

def offSeason(teams):
    for team in teams:
        if team.getOffense() < 70:
            team.setOffense(team.getOffense() + random.randint(0, 10))
        elif team.getOffense() < 80:
            team.setOffense(team.getOffense() + random.randint(-5, 10))
        elif team.getOffense() < 90:
            team.setOffense(team.getOffense() + random.randint(-5, 5))
        else:
            team.setOffense(team.getOffense() + random.randint(-10, 5))

        if team.getDefense() < 70:
            team.setDefense(team.getDefense() + random.randint(0, 10))
        elif team.getDefense() < 80:
            team.setOffense(team.getDefense() + random.randint(-5, 10))
        elif team.getDefense() < 90:
            team.setDefense(team.getDefense() + random.randint(-5, 5))
        else:
            team.setDefense(team.getDefense() + random.randint(-10, 5))


year = "Teams.txt"
teams = list()
startFile = open(year, 'r')
for line in startFile:
    arr = line.split()
    if len(arr) == 3:
        teams.append(Team.Team(arr[0], int(arr[1]), int(arr[2])))
        #print(arr[0])
    else:
        name = ""
        for i in range(0, len(arr) - 2):
            name += arr[i] + " "
        name = name[0:len(name)-1]
        teams.append(Team.Team(name, int(arr[len(arr)-2]), int(arr[len(arr)-1])))
        #print(name)
offSeason(teams)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
rankings = loop.run_until_complete(regularSeason(teams))
playoffTeams = list()
counter = 0

for pair in rankings.values():
    for rankedTeam in pair:
        for team in teams:
            if rankedTeam.display_name == team.getName():
                print(team.getName() +" "+ team.getRecord())
                if counter < 8:
                    playoffTeams.append(team)
                counter += 1
                break
p = Playoffs.Playoffs(playoffTeams)
playoffRankings = loop.run_until_complete(p.tournament())


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



