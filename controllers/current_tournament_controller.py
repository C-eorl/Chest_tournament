from models.match import Match
from models.round import Round
from models.tournament import Tournament
from models.tournament_DAO import TournamentRepository

from utils.database import get_db_tournament
from utils.decorateur_try import decorator_try
from utils.exit_menu import retour

from views.view_tournament import ViewTournament

import random

class ControllerCurrentTournament:
    def __init__(self, app_controller):
        self.app = app_controller  # pas utiliser
        self.view = ViewTournament()
        self.db = get_db_tournament()
        self.repo_tournament = TournamentRepository(self.db)
        self.target: Tournament | None = None

    @decorator_try
    def run(self):
        """Menu tournoi en cours"""
        if self.target is None:
            self.target = self.get_tournament_target()
        title = ("Gestion du tournoi en cours\n"       # ajouter f{self target} au titre avec style 
                 "Choisissez une option:")
        option = {
            "Affichage du Round actuel et des matchs": NotImplemented,
            "Génèrez les matchs": self.generate_matchs,
            "Saisie des résultats": self.input_winner,
            "Round suivant": NotImplemented,
            "Mettre fin au tournoi": self.finished_tournament,
            "Retour": retour
        }
        self.view.menu(title, option)


    def finished_tournament(self):
        """Définit le tournoi comme fini et met a jour la base de donnée"""
        self.target.statut = "finished"
        self.repo_tournament.update(self.target.tournament_name, self.target.to_dict())
        self.view.display_message("le tournoi est terminé")
        retour()

    def list_current_tournament(self):
        """retourne une liste de tous les tournois en cours"""
        return [Tournament.from_dict(tournoi) for tournoi in self.repo_tournament.search_is("current")]

    def get_tournament_target(self) -> Tournament:
        """renvoie le tournoi en cours ciblé pour l'utiliser"""
        current_tournaments = self.list_current_tournament()
        return self.view.display_selected_tournament(current_tournaments)

    def input_winner(self):
        """
        Affiche tous les matchs non joué d'un round pour pouvoir en sélectionner 1 et désigner le résultat.
        Puis mets à jour le classement
        :return:
        """

        r = self.target.rounds
        list_match = [
            match for match in r[-1].get_list_match()
            if match.score1 == 0 and match.score2 == 0
        ]
        if not list_match:
            self.view.display_message("Tous les matchs ont été joué. Passez au Round suivant.")
        else:
            match = self.view.display_selected_data(list_match)
            data = [match.player1, match.player2, "Match nul"]
            winner = self.view.display_selected_data(data)
            match.get_result(winner)
            for player_score in match.tuple_return():
                self.target.classement[player_score[0]] += player_score[1]



    def generate_matchs(self, list_players):
        """Génère les matchs d'un round """
        round_nb = len(self.target.rounds) + 1
        r = Round(f"round {round_nb}")

        while len(list) >= 2:
            match_found = False

            for i in range(len(list_players)):
                for j in range(i+1, len(list_players)):

                    player_A = list_players[i]
                    player_B = list_players[j]
                    pair = tuple(sorted([player_A, player_B]))
                    if pair not in self.target.match_history:
                        # Match créé
                        m = Match(player_A, player_B)
                        r.list_match.append(m)
                        self.target.match_history.add(pair)
                        list_players.remove(player_A)
                        list_players.remove(player_B)
                        match_found = True
                        break
                if match_found:
                    break
            if not match_found:
                break
        if len(list_players) == 1:
            self.target.classement[list_players[0]] += 1
        self.target.rounds.append(r)


    def generate_classement(self):
        """remplie le dictionnaire des participants et initialise les scores a 0.0"""
        for player in self.target.list_participant:
            self.target.classement[player] = 0.0

    def sorted_list_participant(self):
        """renvoie une liste des participants triée par ordre décroissant"""
        sorted_list = dict(sorted(self.target.classement.items(), key=lambda x: x[1], reverse=True))
        list_player = []
        for player in sorted_list.keys():
            list_player.append(player)
        return list_player

    def lancement_round(self):
        self.generate_classement()
        if len(self.target.rounds) == 0:
            list_player = self.target.list_participant[:]
            random.shuffle(list_player)
            self.generate_matchs(list_player)
        else:
            list_player = self.sorted_list_participant()
            self.generate_matchs(list_player)
        self.input_winner()

if "__name__" == "__main__":
    pass