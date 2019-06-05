import challonge
import Game

class Playoffs:
    def __init__(self, teams):
        self.teams = teams

    async def tournament(self):
        chal = await challonge.get_user('Kcin14', 'M2ZyNWHKoTJJjkwdg6JCrxyljE3HoeDH0AZdD8oa')
        t = await chal.create_tournament("2243 Preseason 6A", "2243fa")
        participants = list()
        for team in self.teams:
            participants.append(await t.add_participant(team.name))
        await t.start()
        matches = await t.get_matches()
        for match in matches:
            parA = await t.get_participant(match.player1_id)
            parB = await t.get_participant(match.player2_id)
            teamA = None
            teamB = None
            for team in self.teams:
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
                for i in range(0, len(string) - 1):
                    name += string[i] + " "
                name = name[0:len(name) - 1]
                for participant in participants:
                    if name == participant.display_name:
                        await match.report_winner(participant, string[len(string) - 1])
                        break
        await t.finalize()
        rankings = await t.get_final_ranking()
        return rankings