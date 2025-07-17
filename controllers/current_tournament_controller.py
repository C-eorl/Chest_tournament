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
        self.classement_generator()
        title = ("Gestion du tournoi en cours\n"  
                 f"{self.target}\n"
                 "Choisissez une option:")
        option = {
            "Affichage du Round actuel et des matchs": self.detail_round,
            "Générer les matchs": self.round_generator,
            "Saisie des résultats": self.input_winner,
            "Round suivant": self.next_round,
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
        Affiche tous les matchs non joués d'un round pour pouvoir en sélectionner un et désigner le résultat.
        Puis mets à jour le classement
        :return: None
        """
        list_rounds = self.target.rounds
        list_match = [
            match for match in list_rounds[-1].get_match_list()
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

    def next_round(self):
        """met fin au round actuelle et lance le prochain"""
        round_current =  self.target.rounds[-1]
        round_current.finish()
        self.view.display_message(f"{round_current.name} est fini")
        self.view.display_message(f"Veuillez générer les prochains matchs pour le round {len(self.target.rounds) + 1}")

    def matchs_generator(self, list_players):
        """Génère les matchs d'un round grâce à une liste deja trié"""
        round_nb = len(self.target.rounds) + 1
        round = Round(f"round {round_nb}")
        round.start()
        while len(list_players) >= 2:
            match_found = False

            for i in range(len(list_players)):
                for j in range(i+1, len(list_players)):

                    player_A = list_players[i]
                    player_B = list_players[j]
                    pair = tuple(sorted([player_A, player_B], key=lambda p: p.name))
                    if pair not in self.target.match_history:
                        # Match créé
                        m = Match(player_A, player_B)
                        round.list_match.append(m)
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
        self.target.rounds.append(round)

    def classement_generator(self):
        """remplie le dictionnaire des participants et initialise les scores à 0.0"""
        for player in self.target.list_participant:
            self.target.classement[player] = 0.0

    def sorted_list_participant(self):
        """renvoie une liste des participants triée par ordre décroissant"""
        sorted_list = dict(sorted(self.target.classement.items(), key=lambda x: x[1], reverse=True))
        list_player = []
        for player in sorted_list.keys():
            list_player.append(player)
        return list_player

    def round_generator(self):
        # si 1er round, list mélanger puis generation de match
        if len(self.target.rounds) == 0:
            list_player = self.target.list_participant[:]
            random.shuffle(list_player)
            self.matchs_generator(list_player)
        # sinon list trié par odre décroissant de score puis generation de match
        else:
            list_player = self.sorted_list_participant()
            self.matchs_generator(list_player)
        self.repo_tournament.update(self.target.tournament_name, self.target.to_dict())

    def detail_round(self):
        if not self.target.rounds:
            self.view.display_message("Aucun Round n'a été commencé")
        else:
            round_current = self.target.rounds[-1]
            self.view.display_round(round_current)

if __name__ == "__main__":
    pass