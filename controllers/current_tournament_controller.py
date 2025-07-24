from models.match import Match
from models.round import Round
from models.tournament import Tournament
from models.tournament_DAO import TournamentRepository
from utils.database import get_db_tournament
from utils.decorateur_try import decorator_try
from views.view_tournament import ViewTournament


class ControllerCurrentTournament:
    def __init__(self, app_controller):
        self.app = app_controller  # pas utiliser
        self.view = ViewTournament()
        self.db = get_db_tournament()
        self.repo_tournament = TournamentRepository(self.db)
        self.target: Tournament | None = None

    def validate_tournament(self):
        """
        vérifie si le tournoi cible (self.target) est pas valide:
        - possède des participants
        - s'il est fini
        - ou None dans ce cas, demande quel tournoi utiliser
        :return: bool
        """
        if self.target is None:
            self.target = self.get_tournament_target()
            if self.target is None:
                self.view.display_message("Aucun tournoi sélectionné. Retour au menu précédent.")
                return False
        if self.target.statut == "finished":
            self.target = None
            "Fin du menu tournoi en cours"
            return False
        if not self.target.list_participant:
            self.view.display_message("Ce tournoi n'a aucun participant. Retour au menu précédent.")
            return False
        return True

    @decorator_try
    def run(self):
        """Menu tournoi en cours"""
        title = ("Gestion du tournoi en cours\n"  
                 f"{self.target}\n"
                 "Choisissez une option:")
        options = {
            "Affichage du Round actuel et des matchs": self.detail_round,
            "Générer les matchs": self.round_generator,
            "Saisie des résultats": self.input_winner,
            "Premier Round ou suivant": self.next_round,
            "Classement": self.display_classement,
            "Retour": None
        }

        while True:
            if not self.validate_tournament():
                break
            choice = self.view.menu(title, options)
            if choice is None:
                break
            choice()

    def finished_tournament(self):
        """Définit le tournoi comme fini et met à jour la base de donnée"""
        self.target.statut = "finished"
        self.repo_tournament.update(self.target.tournament_name, self.target.to_dict())
        self.view.display_message("le tournoi est terminé")
        return None

    def list_current_tournament(self):
        """retourne une liste de tous les tournois en cours"""
        return [Tournament.from_dict(tournoi) for tournoi in self.repo_tournament.search_is("current")]

    def display_classement(self):
        classement = dict(sorted(self.target.classement.items(), key=lambda x: x[1], reverse=True))
        self.view.display_classement(classement)

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
        if not list_rounds:
            self.view.display_message("Aucun round et match n'a été généré")
            return
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
            self.repo_tournament.update(self.target.tournament_name, self.target.to_dict())
            self.view.display_message(f"Résultat du match: {winner}")

    def next_round(self):
        """met fin au round actuel et crée le round suivant vide (sans générer les matchs)"""
        list_rounds = self.target.rounds

        if not list_rounds:
            self.classement_generator()
            self.target.statut = "current"
            round_1 = Round("Round 1")
            round_1.start()
            self.target.rounds.append(round_1)
            self.repo_tournament.update(self.target.tournament_name, self.target.to_dict())
            self.view.display_message("Premier round créé. Veuillez maintenant générer les matchs.")
            return

        list_match = [
            match for match in list_rounds[-1].get_match_list()
            if match.score1 == 0 and match.score2 == 0
        ]
        if not list_rounds[-1].get_match_list():
            self.view.display_message("Aucun match n'a été généré")
            return
        if list_match:
            self.view.display_message("Il reste des matchs à jouer")
            return

        # Finir le round actuel
        round_current = self.target.rounds[-1]
        round_current.finish()
        self.view.display_message(f"{round_current.name} est fini")

        # Vérifier si on a atteint le nombre total de rounds
        if len(self.target.rounds) >= self.target.round_number :
            self.finished_tournament()
            return

        # Création du round suivant (VIDE, sans matchs encore)
        round_nb = len(self.target.rounds) + 1
        new_round = Round(f"Round {round_nb}")
        new_round.start()
        self.target.rounds.append(new_round)

        self.repo_tournament.update(self.target.tournament_name, self.target.to_dict())
        self.view.display_message(f"{new_round.name} a été créé. Veuillez maintenant générer les matchs.")

    def matchs_generator(self, list_players, current_round):
        """Génère les matchs d'un round grâce à une liste deja trié"""
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
                        current_round.list_match.append(m)
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
            lone_player = list_players[0]
            current_round.lone_player = lone_player
            self.target.classement[lone_player] += 1
            self.view.display_message(f"{lone_player.simple_str()} "
                                      f"n'a pas adversaire (cause: nombre impair de participant)"
                                      f"donc son score est de 1 ")
        self.view.display_message("Fin de la génération des matchs")

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
        """Génère les matchs pour le round en cours (sans créer un nouveau round)"""
        if not self.target.rounds:
            self.view.display_message("Aucun round n'existe. Veuillez commencer un round avant de générer les matchs.")
            return
        current_round = self.target.rounds[-1]
        # Vérifie si le round est terminé
        if current_round.date_time_end is not None:
            self.view.display_message("Le round actuel est terminé. Lancez le round suivant d'abord.")
            return
        # Vérifie si les matchs existent déjà
        if current_round.get_match_list():
            self.view.display_message("Les matchs du round actuel ont déjà été générés.")
            return
        # Génération des matchs
        list_player = self.sorted_list_participant()
        self.view.display_message(f"Génération des matchs pour le {current_round.name}")
        self.matchs_generator(list_player, current_round)
        self.repo_tournament.update(self.target.tournament_name, self.target.to_dict())

    def detail_round(self):
        """Affiche les informations du round en cours plus les matchs"""
        if not self.target.rounds:
            self.view.display_message("Aucun Round n'a été commencé")
        else:
            round_current = self.target.rounds[-1]
            self.view.display_round(round_current)

if __name__ == "__main__":
    pass